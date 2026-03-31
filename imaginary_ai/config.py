from dataclasses import dataclass
from typing import Literal


TaskType = Literal["text_to_image", "image_to_image", "text_to_video", "image_to_video"]


@dataclass(frozen=True)
class ModelSpec:
    key: str
    label: str
    repo_id: str
    pipeline_class: str
    family: str
    license_name: str
    supports_mask: bool
    recommended_vram_gb: int
    default_width: int | None
    default_height: int | None
    target_width: int | None
    target_height: int | None
    render_strategy: str
    notes: str


TASK_LABELS = {
    "text_to_image": "Text zu Bild",
    "image_to_image": "Bild zu Bild",
    "text_to_video": "Text zu Video",
    "image_to_video": "Bild zu Video",
}


TASK_MODEL_SPECS: dict[TaskType, list[ModelSpec]] = {
    "text_to_image": [
        ModelSpec(
            key="sdxl-turbo-lite",
            label="SDXL Turbo Lite",
            repo_id="stabilityai/sdxl-turbo",
            pipeline_class="AutoPipelineForText2Image",
            family="image",
            license_name="Stability AI Community",
            supports_mask=False,
            recommended_vram_gb=8,
            default_width=512,
            default_height=512,
            target_width=512,
            target_height=512,
            render_strategy="native",
            notes="Fast fallback profile for current hardware and future Android-lite workflows.",
        ),
        ModelSpec(
            key="flux2-klein",
            label="FLUX.2 klein 4B",
            repo_id="black-forest-labs/FLUX.2-klein-4B",
            pipeline_class="Flux2KleinPipeline",
            family="image",
            license_name="Apache-2.0",
            supports_mask=False,
            recommended_vram_gb=13,
            default_width=None,
            default_height=None,
            target_width=None,
            target_height=None,
            render_strategy="native",
            notes="Open primary image model for local text-to-image and reference-based image generation.",
        ),
    ],
    "image_to_image": [
        ModelSpec(
            key="sdxl-turbo-lite",
            label="SDXL Turbo Lite",
            repo_id="stabilityai/sdxl-turbo",
            pipeline_class="AutoPipelineForImage2Image",
            family="image",
            license_name="Stability AI Community",
            supports_mask=False,
            recommended_vram_gb=8,
            default_width=512,
            default_height=512,
            target_width=512,
            target_height=512,
            render_strategy="native",
            notes="Fast image-to-image fallback profile for current hardware and future Android-lite workflows.",
        ),
        ModelSpec(
            key="flux2-klein",
            label="FLUX.2 klein 4B",
            repo_id="black-forest-labs/FLUX.2-klein-4B",
            pipeline_class="Flux2KleinPipeline",
            family="image",
            license_name="Apache-2.0",
            supports_mask=False,
            recommended_vram_gb=13,
            default_width=None,
            default_height=None,
            target_width=None,
            target_height=None,
            render_strategy="native",
            notes="Primary open image-to-image model with Apache-2.0 license.",
        ),
        ModelSpec(
            key="flux-kontext",
            label="FLUX.1 Kontext [dev]",
            repo_id="black-forest-labs/FLUX.1-Kontext-dev",
            pipeline_class="FluxKontextPipeline",
            family="image",
            license_name="FLUX.1 dev Non-Commercial",
            supports_mask=False,
            recommended_vram_gb=16,
            default_width=None,
            default_height=None,
            target_width=None,
            target_height=None,
            render_strategy="native",
            notes="Stronger instruction-based editing, but non-commercial.",
        ),
        ModelSpec(
            key="flux-kontext-inpaint",
            label="FLUX.1 Kontext Inpaint [dev]",
            repo_id="black-forest-labs/FLUX.1-Kontext-dev",
            pipeline_class="FluxKontextInpaintPipeline",
            family="image",
            license_name="FLUX.1 dev Non-Commercial",
            supports_mask=True,
            recommended_vram_gb=16,
            default_width=None,
            default_height=None,
            target_width=None,
            target_height=None,
            render_strategy="native",
            notes="Masked inpainting and targeted object replacement, but non-commercial.",
        ),
    ],
    "text_to_video": [
        ModelSpec(
            key="wan-t2v-1-3b",
            label="Wan2.1 T2V 1.3B",
            repo_id="Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
            pipeline_class="WanPipeline",
            family="video",
            license_name="Apache-2.0",
            supports_mask=False,
            recommended_vram_gb=9,
            default_width=832,
            default_height=480,
            target_width=832,
            target_height=480,
            render_strategy="native",
            notes="Consumer-GPU-friendly video model and the best starting point for local text-to-video.",
        ),
        ModelSpec(
            key="wan-t2v-14b",
            label="Wan2.1 T2V 14B [Heavy]",
            repo_id="Wan-AI/Wan2.1-T2V-14B-Diffusers",
            pipeline_class="WanPipeline",
            family="video",
            license_name="Apache-2.0",
            supports_mask=False,
            recommended_vram_gb=24,
            default_width=1280,
            default_height=720,
            target_width=1280,
            target_height=720,
            render_strategy="native",
            notes="Higher-quality text-to-video option for bigger GPUs. Heavy on older cards.",
        ),
        ModelSpec(
            key="wan-t2v-14b-1080p",
            label="Wan2.1 T2V 14B 1080P via Upscaling [Heavy]",
            repo_id="Wan-AI/Wan2.1-T2V-14B-Diffusers",
            pipeline_class="WanPipeline",
            family="video",
            license_name="Apache-2.0",
            supports_mask=False,
            recommended_vram_gb=24,
            default_width=1280,
            default_height=720,
            target_width=1920,
            target_height=1080,
            render_strategy="upscale",
            notes="Uses native 720P generation and then upscales to 1080P for an HD delivery profile. Heavy on older cards.",
        ),
    ],
    "image_to_video": [
        ModelSpec(
            key="wan-i2v-14b-480p",
            label="Wan2.1 I2V 14B 480P [Heavy/Experimentell]",
            repo_id="Wan-AI/Wan2.1-I2V-14B-480P-Diffusers",
            pipeline_class="WanImageToVideoPipeline",
            family="video",
            license_name="Apache-2.0",
            supports_mask=False,
            recommended_vram_gb=24,
            default_width=832,
            default_height=480,
            target_width=832,
            target_height=480,
            render_strategy="native",
            notes="Best open local image-to-video option in this stack, but substantially heavier and experimental on 8 GB GPUs.",
        ),
        ModelSpec(
            key="wan-i2v-14b-720p",
            label="Wan2.1 I2V 14B 720P [Heavy/Experimentell]",
            repo_id="Wan-AI/Wan2.1-I2V-14B-720P-Diffusers",
            pipeline_class="WanImageToVideoPipeline",
            family="video",
            license_name="Apache-2.0",
            supports_mask=False,
            recommended_vram_gb=24,
            default_width=1280,
            default_height=720,
            target_width=1280,
            target_height=720,
            render_strategy="native",
            notes="Native 720P image-to-video option with significantly higher memory demand and experimental status on older cards.",
        ),
        ModelSpec(
            key="wan-i2v-14b-1080p",
            label="Wan2.1 I2V 14B 1080P via Upscaling [Heavy/Experimentell]",
            repo_id="Wan-AI/Wan2.1-I2V-14B-720P-Diffusers",
            pipeline_class="WanImageToVideoPipeline",
            family="video",
            license_name="Apache-2.0",
            supports_mask=False,
            recommended_vram_gb=24,
            default_width=1280,
            default_height=720,
            target_width=1920,
            target_height=1080,
            render_strategy="upscale",
            notes="Uses native 720P generation and then upscales to 1080P for HD export. Experimental on older cards.",
        ),
    ],
}


NEGATIVE_PROMPT = (
    "Bright tones, overexposed, static, blurred details, subtitles, paintings, low quality, ugly, "
    "deformed, disfigured, extra fingers, fused fingers, still picture, messy background"
)


DEFAULTS = {
    "image_steps": 4,
    "image_guidance": 0.0,
    "image_strength": 0.9,
    "video_steps": 4,
    "video_guidance": 5.0,
    "video_strength": 0.8,
    "video_frames": 9,
    "video_fps": 8,
    "seed": 42,
}
