import gradio as gr

from imaginary_ai.config import DEFAULTS
from imaginary_ai.config import TASK_MODEL_SPECS
from imaginary_ai.config import TaskType
from imaginary_ai.runtime import PipelineManager
from imaginary_ai.runtime import generate_image
from imaginary_ai.runtime import generate_video


MANAGER = PipelineManager()


def _spec_choices(task_type: TaskType):
    return [(spec.label, spec.key) for spec in TASK_MODEL_SPECS[task_type]]


def _spec_map(task_type: TaskType):
    return {spec.key: spec for spec in TASK_MODEL_SPECS[task_type]}


def _model_hint(task_type: TaskType, model_key: str) -> str:
    spec = _spec_map(task_type)[model_key]
    native_resolution = (
        f"{spec.default_width}x{spec.default_height}" if spec.default_width and spec.default_height else "modellintern"
    )
    target_resolution = (
        f"{spec.target_width}x{spec.target_height}" if spec.target_width and spec.target_height else native_resolution
    )
    strategy_label = "Upscaling" if spec.render_strategy == "upscale" else "Native Ausgabe"
    return (
        f"{spec.label} | Lizenz: {spec.license_name} | Empfohlener VRAM: ca. "
        f"{spec.recommended_vram_gb} GB | Strategie: {strategy_label} | Native Basis: {native_resolution} | "
        f"Zielausgabe: {target_resolution} | {spec.notes}"
    )


def _run_text_to_image(model_key, prompt, steps, guidance, seed):
    spec = _spec_map("text_to_image")[model_key]
    result = generate_image(
        manager=MANAGER,
        spec=spec,
        prompt=prompt,
        source_image=None,
        mask_image=None,
        num_inference_steps=steps,
        guidance_scale=guidance,
        strength=DEFAULTS["image_strength"],
        seed=seed,
    )
    return result.image, result.info


def _run_image_to_image(model_key, prompt, source_image, mask_image, steps, guidance, strength, seed):
    spec = _spec_map("image_to_image")[model_key]
    result = generate_image(
        manager=MANAGER,
        spec=spec,
        prompt=prompt,
        source_image=source_image,
        mask_image=mask_image if spec.supports_mask else None,
        num_inference_steps=steps,
        guidance_scale=guidance,
        strength=strength,
        seed=seed,
    )
    return result.image, result.info


def _run_text_to_video(model_key, prompt, steps, guidance, frames, fps, seed):
    spec = _spec_map("text_to_video")[model_key]
    result = generate_video(
        manager=MANAGER,
        spec=spec,
        prompt=prompt,
        source_image=None,
        num_inference_steps=steps,
        guidance_scale=guidance,
        strength=DEFAULTS["video_strength"],
        num_frames=frames,
        fps=fps,
        seed=seed,
    )
    return result.video_path, result.info


def _run_image_to_video(model_key, prompt, source_image, steps, guidance, strength, frames, fps, seed):
    spec = _spec_map("image_to_video")[model_key]
    result = generate_video(
        manager=MANAGER,
        spec=spec,
        prompt=prompt,
        source_image=source_image,
        num_inference_steps=steps,
        guidance_scale=guidance,
        strength=strength,
        num_frames=frames,
        fps=fps,
        seed=seed,
    )
    return result.video_path, result.info


def build_demo():
    with gr.Blocks(title="Imaginary Local Media AI") as demo:
        gr.Markdown(
            """
            # Imaginary Local Media AI
            Eine lokal gehostete Open-Source-Workstation fuer:
            - Text zu Bild
            - Bild zu Bild
            - Text zu Video
            - Bild zu Video

            Empfohlene Basis:
            - Bilder: `FLUX.2 klein 4B`
            - Starkes Editing: `FLUX.1 Kontext [dev]`
            - Video: `Wan2.1`

            Laufzeitprinzip:
            - Voll lokal auf deinem Rechner
            - Android-Zugriff ueber Browser im gleichen Netzwerk moeglich
            - Keine externe SaaS-Moderation oder Cloud-Filter in dieser App-Schicht
            """
        )

        with gr.Tab("Text zu Bild"):
            t2i_model = gr.Dropdown(choices=_spec_choices("text_to_image"), value="sdxl-turbo-lite", label="Modell")
            t2i_hint = gr.Textbox(value=_model_hint("text_to_image", "sdxl-turbo-lite"), interactive=False, label="Hinweis")
            t2i_prompt = gr.Textbox(label="Prompt", lines=3)
            with gr.Row():
                t2i_steps = gr.Slider(1, 60, value=DEFAULTS["image_steps"], step=1, label="Inference Steps")
                t2i_guidance = gr.Slider(1.0, 10.0, value=DEFAULTS["image_guidance"], step=0.1, label="Guidance")
                t2i_seed = gr.Number(value=DEFAULTS["seed"], precision=0, label="Seed")
            t2i_run = gr.Button("Bild generieren")
            t2i_output = gr.Image(type="pil", label="Ergebnis")
            t2i_info = gr.Textbox(interactive=False, label="Info")
            t2i_model.change(fn=lambda key: _model_hint("text_to_image", key), inputs=t2i_model, outputs=t2i_hint)
            t2i_run.click(
                fn=_run_text_to_image,
                inputs=[t2i_model, t2i_prompt, t2i_steps, t2i_guidance, t2i_seed],
                outputs=[t2i_output, t2i_info],
            )

        with gr.Tab("Bild zu Bild"):
            i2i_model = gr.Dropdown(choices=_spec_choices("image_to_image"), value="sdxl-turbo-lite", label="Modell")
            i2i_hint = gr.Textbox(value=_model_hint("image_to_image", "sdxl-turbo-lite"), interactive=False, label="Hinweis")
            i2i_image = gr.Image(type="pil", label="Ausgangsbild")
            i2i_mask = gr.Image(type="pil", label="Maske fuer Inpainting (nur Kontext Inpaint)")
            i2i_prompt = gr.Textbox(label="Prompt", lines=3)
            with gr.Row():
                i2i_steps = gr.Slider(1, 60, value=DEFAULTS["image_steps"], step=1, label="Inference Steps")
                i2i_guidance = gr.Slider(1.0, 10.0, value=DEFAULTS["image_guidance"], step=0.1, label="Guidance")
                i2i_strength = gr.Slider(0.1, 1.0, value=DEFAULTS["image_strength"], step=0.05, label="Strength")
                i2i_seed = gr.Number(value=DEFAULTS["seed"], precision=0, label="Seed")
            i2i_run = gr.Button("Bearbeitung starten")
            i2i_output = gr.Image(type="pil", label="Ergebnis")
            i2i_info = gr.Textbox(interactive=False, label="Info")
            i2i_model.change(fn=lambda key: _model_hint("image_to_image", key), inputs=i2i_model, outputs=i2i_hint)
            i2i_run.click(
                fn=_run_image_to_image,
                inputs=[i2i_model, i2i_prompt, i2i_image, i2i_mask, i2i_steps, i2i_guidance, i2i_strength, i2i_seed],
                outputs=[i2i_output, i2i_info],
            )

        with gr.Tab("Text zu Video"):
            t2v_model = gr.Dropdown(choices=_spec_choices("text_to_video"), value="wan-t2v-1-3b", label="Modell")
            t2v_hint = gr.Textbox(value=_model_hint("text_to_video", "wan-t2v-1-3b"), interactive=False, label="Hinweis")
            t2v_prompt = gr.Textbox(label="Prompt", lines=3)
            with gr.Row():
                t2v_steps = gr.Slider(1, 60, value=DEFAULTS["video_steps"], step=1, label="Inference Steps")
                t2v_guidance = gr.Slider(1.0, 10.0, value=DEFAULTS["video_guidance"], step=0.1, label="Guidance")
                t2v_frames = gr.Slider(16, 81, value=DEFAULTS["video_frames"], step=1, label="Frames")
                t2v_fps = gr.Slider(8, 24, value=DEFAULTS["video_fps"], step=1, label="FPS")
                t2v_seed = gr.Number(value=DEFAULTS["seed"], precision=0, label="Seed")
            t2v_run = gr.Button("Video generieren")
            t2v_output = gr.Video(label="Ergebnis")
            t2v_info = gr.Textbox(interactive=False, label="Info")
            t2v_model.change(fn=lambda key: _model_hint("text_to_video", key), inputs=t2v_model, outputs=t2v_hint)
            t2v_run.click(
                fn=_run_text_to_video,
                inputs=[t2v_model, t2v_prompt, t2v_steps, t2v_guidance, t2v_frames, t2v_fps, t2v_seed],
                outputs=[t2v_output, t2v_info],
            )

        with gr.Tab("Bild zu Video"):
            i2v_model = gr.Dropdown(choices=_spec_choices("image_to_video"), value="wan-i2v-14b-480p", label="Modell")
            i2v_hint = gr.Textbox(
                value=_model_hint("image_to_video", "wan-i2v-14b-480p"),
                interactive=False,
                label="Hinweis",
            )
            i2v_image = gr.Image(type="pil", label="Ausgangsbild")
            i2v_prompt = gr.Textbox(label="Prompt", lines=3)
            with gr.Row():
                i2v_steps = gr.Slider(1, 60, value=DEFAULTS["video_steps"], step=1, label="Inference Steps")
                i2v_guidance = gr.Slider(1.0, 10.0, value=DEFAULTS["video_guidance"], step=0.1, label="Guidance")
                i2v_strength = gr.Slider(0.1, 1.0, value=DEFAULTS["video_strength"], step=0.05, label="Strength")
                i2v_frames = gr.Slider(16, 81, value=DEFAULTS["video_frames"], step=1, label="Frames")
                i2v_fps = gr.Slider(8, 24, value=DEFAULTS["video_fps"], step=1, label="FPS")
                i2v_seed = gr.Number(value=DEFAULTS["seed"], precision=0, label="Seed")
            i2v_run = gr.Button("Video aus Bild generieren")
            i2v_output = gr.Video(label="Ergebnis")
            i2v_info = gr.Textbox(interactive=False, label="Info")
            i2v_model.change(fn=lambda key: _model_hint("image_to_video", key), inputs=i2v_model, outputs=i2v_hint)
            i2v_run.click(
                fn=_run_image_to_video,
                inputs=[i2v_model, i2v_prompt, i2v_image, i2v_steps, i2v_guidance, i2v_strength, i2v_frames, i2v_fps, i2v_seed],
                outputs=[i2v_output, i2v_info],
            )

    return demo
