import gc
import os
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Any

import numpy as np
import torch
from diffusers import AutoencoderKLWan
from diffusers.utils import export_to_video
from PIL import Image
from transformers import CLIPVisionModel

from imaginary_ai.config import DEFAULTS
from imaginary_ai.config import ModelSpec
from imaginary_ai.config import NEGATIVE_PROMPT
from imaginary_ai.media import ensure_output_dir


@dataclass
class GenerationResult:
    image: Image.Image | None = None
    video_path: str | None = None
    info: str = ""


class PipelineManager:
    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}
        self._active_key: str | None = None

    def _resolve_device(self) -> str:
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"

    def _resolve_dtype(self, family: str, device: str) -> torch.dtype:
        if device != "cuda":
            return torch.float32
        if family == "video":
            return torch.bfloat16
        if torch.cuda.is_bf16_supported():
            return torch.bfloat16
        return torch.float16

    def _clear_if_switching(self, key: str) -> None:
        if self._active_key == key:
            return
        if self._active_key is None:
            return
        pipe = self._cache.pop(self._active_key, None)
        self._active_key = None
        if pipe is not None:
            del pipe
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    def _load_pipeline_class(self, class_name: str):
        diffusers_module = import_module("diffusers")
        return getattr(diffusers_module, class_name)

    def _local_files_only(self) -> bool:
        return os.getenv("IMAGINARY_LOCAL_FILES_ONLY", "0") == "1" or os.getenv("HF_HUB_OFFLINE", "0") == "1"

    def _build_video_pipeline(self, spec: ModelSpec, dtype: torch.dtype):
        pipeline_cls = self._load_pipeline_class(spec.pipeline_class)
        local_files_only = self._local_files_only()
        if spec.pipeline_class == "WanPipeline":
            vae = AutoencoderKLWan.from_pretrained(
                spec.repo_id, subfolder="vae", torch_dtype=torch.float32, local_files_only=local_files_only
            )
            return pipeline_cls.from_pretrained(
                spec.repo_id, vae=vae, torch_dtype=dtype, local_files_only=local_files_only
            )
        if spec.pipeline_class == "WanImageToVideoPipeline":
            vae = AutoencoderKLWan.from_pretrained(
                spec.repo_id, subfolder="vae", torch_dtype=torch.float32, local_files_only=local_files_only
            )
            image_encoder = CLIPVisionModel.from_pretrained(
                spec.repo_id, subfolder="image_encoder", torch_dtype=torch.float32, local_files_only=local_files_only
            )
            return pipeline_cls.from_pretrained(
                spec.repo_id, vae=vae, image_encoder=image_encoder, torch_dtype=dtype, local_files_only=local_files_only
            )
        raise ValueError(f"Unsupported video pipeline: {spec.pipeline_class}")

    def get_pipeline(self, spec: ModelSpec):
        cache_key = f"{spec.key}:{spec.pipeline_class}"
        self._clear_if_switching(cache_key)
        if cache_key in self._cache:
            self._active_key = cache_key
            return self._cache[cache_key]

        device = self._resolve_device()
        dtype = self._resolve_dtype(spec.family, device)
        if spec.family == "video":
            pipe = self._build_video_pipeline(spec, dtype)
        else:
            pipeline_cls = self._load_pipeline_class(spec.pipeline_class)
            loader_kwargs: dict[str, Any] = {
                "torch_dtype": dtype,
                "local_files_only": self._local_files_only(),
            }
            if spec.key == "sdxl-turbo-lite":
                loader_kwargs["use_safetensors"] = True
                if device == "cuda":
                    loader_kwargs["variant"] = "fp16"
            pipe = pipeline_cls.from_pretrained(spec.repo_id, **loader_kwargs)

        if device == "cuda":
            try:
                pipe.enable_model_cpu_offload()
            except Exception:
                pipe.to(device)
        else:
            pipe.to(device)

        self._cache[cache_key] = pipe
        self._active_key = cache_key
        return pipe


def _seed_generator(seed: int) -> torch.Generator:
    return torch.Generator(device="cpu").manual_seed(int(seed))


def _resize_for_wan(pipe, image: Image.Image, target_height: int, target_width: int) -> Image.Image:
    rgb = image.convert("RGB")
    aspect_ratio = rgb.height / rgb.width
    max_area = target_height * target_width
    mod_value = pipe.vae_scale_factor_spatial * pipe.transformer.config.patch_size[1]
    height = round(np.sqrt(max_area * aspect_ratio)) // mod_value * mod_value
    width = round(np.sqrt(max_area / aspect_ratio)) // mod_value * mod_value
    return rgb.resize((max(width, mod_value), max(height, mod_value)))


def _upscale_frames_if_needed(frames, target_width: int | None, target_height: int | None):
    if not target_width or not target_height:
        return frames
    first_frame = frames[0]
    if isinstance(first_frame, Image.Image):
        current_size = first_frame.size
    else:
        current_size = (int(first_frame.shape[1]), int(first_frame.shape[0]))
    if current_size == (target_width, target_height):
        return frames

    upscaled_frames = []
    for frame in frames:
        pil_frame = frame if isinstance(frame, Image.Image) else Image.fromarray(frame)
        upscaled_frames.append(pil_frame.resize((target_width, target_height), Image.Resampling.LANCZOS))
    return upscaled_frames


def generate_image(
    manager: PipelineManager,
    spec: ModelSpec,
    prompt: str,
    source_image: Image.Image | None,
    mask_image: Image.Image | None,
    num_inference_steps: int,
    guidance_scale: float,
    strength: float,
    seed: int,
) -> GenerationResult:
    prompt = (prompt or "").strip()
    if not prompt:
        raise ValueError("Ein Prompt ist erforderlich.")

    pipe = manager.get_pipeline(spec)
    args: dict[str, Any] = {
        "prompt": prompt,
        "num_inference_steps": int(num_inference_steps),
        "guidance_scale": float(guidance_scale),
        "generator": _seed_generator(seed),
    }
    if spec.default_width and spec.default_height:
        args["width"] = int(spec.default_width)
        args["height"] = int(spec.default_height)
    if source_image is not None:
        args["image"] = source_image.convert("RGB")
        args.pop("width", None)
        args.pop("height", None)
    if mask_image is not None:
        args["mask_image"] = mask_image.convert("RGB")
        args["strength"] = float(strength)

    result = pipe(**args).images[0]
    info = (
        f"Modell: {spec.label} | Lizenz: {spec.license_name} | Empfohlener VRAM: ca. "
        f"{spec.recommended_vram_gb} GB"
    )
    return GenerationResult(image=result, info=info)


def generate_video(
    manager: PipelineManager,
    spec: ModelSpec,
    prompt: str,
    source_image: Image.Image | None,
    num_inference_steps: int,
    guidance_scale: float,
    strength: float,
    num_frames: int,
    fps: int,
    seed: int,
) -> GenerationResult:
    prompt = (prompt or "").strip()
    if not prompt:
        raise ValueError("Ein Prompt ist erforderlich.")

    pipe = manager.get_pipeline(spec)
    args: dict[str, Any] = {
        "prompt": prompt,
        "negative_prompt": NEGATIVE_PROMPT,
        "num_inference_steps": int(num_inference_steps),
        "guidance_scale": float(guidance_scale),
        "num_frames": int(num_frames),
        "generator": _seed_generator(seed),
    }

    if spec.pipeline_class == "WanImageToVideoPipeline":
        if source_image is None:
            raise ValueError("Bild-zu-Video braucht ein Ausgangsbild.")
        target_height = spec.default_height or 480
        target_width = spec.default_width or 832
        resized = _resize_for_wan(pipe, source_image, target_height=target_height, target_width=target_width)
        args["image"] = resized
        args["height"] = resized.height
        args["width"] = resized.width
        args["strength"] = float(strength)
    else:
        args["height"] = spec.default_height or 480
        args["width"] = spec.default_width or 832

    frames = pipe(**args).frames[0]
    frames = _upscale_frames_if_needed(frames, spec.target_width, spec.target_height)
    output_dir = ensure_output_dir()
    output_path = Path(output_dir) / f"{spec.key}-{seed}.mp4"
    export_to_video(frames, str(output_path), fps=int(fps or DEFAULTS["video_fps"]))

    info = (
        f"Modell: {spec.label} | Lizenz: {spec.license_name} | Empfohlener VRAM: ca. "
        f"{spec.recommended_vram_gb} GB | Native Basis: {spec.default_width}x{spec.default_height} | "
        f"Zielausgabe: {spec.target_width}x{spec.target_height} | "
        f"Strategie: {'Upscaling' if spec.render_strategy == 'upscale' else 'Native Ausgabe'} | Ausgabe: {output_path}"
    )
    return GenerationResult(video_path=str(output_path), info=info)
