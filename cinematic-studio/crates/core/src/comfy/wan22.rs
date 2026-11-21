//! Wan 2.2 adapters for ComfyUI's built-in nodes.
//!
//! Source of the graphs: the official ComfyUI workflow templates (Comfy-Org/workflow_templates @ f77d47c,
//! `video_wan2_2_5B_ti2v.json` and `video_wan2_2_14B_i2v.json`) and the node definitions in
//! Comfy-Org/ComfyUI @ afcb984 (comfy_extras/nodes_wan.py, nodes_video.py), read on 2026-11-21.
//! Node inputs and model file names are taken from those files. These graphs have NOT yet been run
//! against a live ComfyUI server by us; the first real generation is the acceptance test.
use super::{frames_for, GenerationRequest, ModelAdapter, ModelFile, ModelInfo};
use crate::error::{err, Result};
use serde_json::{json, Value};

/// Default negative prompt shipped in the official Wan 2.2 templates (Chinese, as published).
pub const DEFAULT_NEGATIVE: &str = "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走";

fn size(info: &ModelInfo, aspect: &str) -> Result<(u32, u32)> {
    info.sizes.iter().find(|(a, _, _)| *a == aspect).map(|(_, w, h)| (*w, *h)).ok_or_else(|| crate::error::AppError::new("aspect_not_supported", format!("{} does not generate {aspect}", info.label)))
}
fn negative(req: &GenerationRequest) -> String {
    if req.negative_prompt.trim().is_empty() { DEFAULT_NEGATIVE.to_string() } else { format!("{}, {}", req.negative_prompt.trim(), DEFAULT_NEGATIVE) }
}
/// Chains LoraLoaderModelOnly nodes after a model node; returns the id of the last node in the chain.
fn add_loras(graph: &mut serde_json::Map<String, Value>, mut model: String, loras: &[(String, f64)], prefix: &str) -> String {
    for (i, (name, strength)) in loras.iter().enumerate() {
        let id = format!("{prefix}{i}");
        graph.insert(id.clone(), json!({ "class_type": "LoraLoaderModelOnly", "inputs": { "model": [model, 0], "lora_name": name, "strength_model": strength } }));
        model = id;
    }
    model
}
fn save_nodes(graph: &mut serde_json::Map<String, Value>, images: (&str, u32), fps: u32, prefix: &str) {
    graph.insert("create".into(), json!({ "class_type": "CreateVideo", "inputs": { "images": [images.0, images.1], "fps": fps } }));
    // `format` is a dynamic combo whose codec choice is the nested input `format.codec`; the node also still
    // accepts the older top-level `codec`. Both are sent so the request is valid on either side of that change.
    graph.insert("save".into(), json!({ "class_type": "SaveVideo", "inputs": { "video": ["create", 0], "filename_prefix": prefix, "format": "mp4", "format.codec": "h264", "codec": "h264" } }));
}

/// Wan 2.2 TI2V-5B: text-to-video and image-to-video in one model, 1280x704 at 24 fps.
pub struct Ti2v5b;
impl ModelAdapter for Ti2v5b {
    fn info(&self) -> ModelInfo {
        ModelInfo {
            id: "wan22-ti2v-5b", label: "Wan 2.2 TI2V-5B", family: "wan22", lora_family: "wan22-5b", licence: "Apache-2.0",
            tasks: &["t2v", "i2v"], fps: 24, max_frames: 121, frame_step: 4,
            sizes: &[("16:9", 1280, 704), ("9:16", 704, 1280)],
            min_vram_gb: 24, steps: 20,
            required_nodes: &["UNETLoader", "CLIPLoader", "VAELoader", "CLIPTextEncode", "ModelSamplingSD3", "Wan22ImageToVideoLatent", "KSampler", "VAEDecode", "CreateVideo", "SaveVideo"],
            files: &[
                ModelFile { folder: "diffusion_models", name: "wan2.2_ti2v_5B_fp16.safetensors" },
                ModelFile { folder: "text_encoders", name: "umt5_xxl_fp8_e4m3fn_scaled.safetensors" },
                ModelFile { folder: "vae", name: "wan2.2_vae.safetensors" },
            ],
            source: "official template video_wan2_2_5B_ti2v.json", status: "graph from the official template; not yet run by us",
        }
    }
    fn output_node(&self) -> &'static str { "save" }
    fn workflow(&self, req: &GenerationRequest) -> Result<Value> {
        let info = self.info();
        let (w, h) = size(&info, &req.aspect)?;
        if req.prompt.trim().is_empty() { return err("bad_request", "the prompt is empty"); }
        let mut g = serde_json::Map::new();
        g.insert("unet".into(), json!({ "class_type": "UNETLoader", "inputs": { "unet_name": info.files[0].name, "weight_dtype": "default" } }));
        g.insert("clip".into(), json!({ "class_type": "CLIPLoader", "inputs": { "clip_name": info.files[1].name, "type": "wan", "device": "default" } }));
        g.insert("vae".into(), json!({ "class_type": "VAELoader", "inputs": { "vae_name": info.files[2].name } }));
        let model = add_loras(&mut g, "unet".into(), &req.loras, "lora");
        g.insert("shift".into(), json!({ "class_type": "ModelSamplingSD3", "inputs": { "model": [model, 0], "shift": 8.0 } }));
        g.insert("pos".into(), json!({ "class_type": "CLIPTextEncode", "inputs": { "clip": ["clip", 0], "text": req.prompt } }));
        g.insert("neg".into(), json!({ "class_type": "CLIPTextEncode", "inputs": { "clip": ["clip", 0], "text": negative(req) } }));
        let mut latent = json!({ "vae": ["vae", 0], "width": w, "height": h, "length": frames_for(&info, req.seconds), "batch_size": 1 });
        if let Some(img) = &req.start_image {
            g.insert("image".into(), json!({ "class_type": "LoadImage", "inputs": { "image": img } }));
            latent["start_image"] = json!(["image", 0]);
        }
        g.insert("latent".into(), json!({ "class_type": "Wan22ImageToVideoLatent", "inputs": latent }));
        g.insert("sample".into(), json!({ "class_type": "KSampler", "inputs": { "model": ["shift", 0], "positive": ["pos", 0], "negative": ["neg", 0], "latent_image": ["latent", 0],
            "seed": req.seed, "steps": info.steps, "cfg": 5.0, "sampler_name": "uni_pc", "scheduler": "simple", "denoise": 1.0 } }));
        g.insert("decode".into(), json!({ "class_type": "VAEDecode", "inputs": { "samples": ["sample", 0], "vae": ["vae", 0] } }));
        save_nodes(&mut g, ("decode", 0), info.fps, &req.filename_prefix);
        Ok(Value::Object(g))
    }
}

/// Wan 2.2 I2V-A14B with the 4-step LightX2V LoRAs, as in the official 14B image-to-video template:
/// two expert models (high noise for steps 0-2, low noise for steps 2-4), 16 fps, 81 frames.
pub struct I2v14bLightning;
impl ModelAdapter for I2v14bLightning {
    fn info(&self) -> ModelInfo {
        ModelInfo {
            id: "wan22-i2v-a14b-4step", label: "Wan 2.2 I2V-A14B (4-step)", family: "wan22", lora_family: "wan22-a14b-i2v", licence: "Apache-2.0",
            tasks: &["i2v"], fps: 16, max_frames: 81, frame_step: 4,
            sizes: &[("16:9", 1280, 720), ("9:16", 720, 1280), ("1:1", 640, 640)],
            min_vram_gb: 24, steps: 4,
            required_nodes: &["UNETLoader", "CLIPLoader", "VAELoader", "CLIPTextEncode", "ModelSamplingSD3", "LoraLoaderModelOnly", "WanImageToVideo", "KSamplerAdvanced", "LoadImage", "VAEDecode", "CreateVideo", "SaveVideo"],
            files: &[
                ModelFile { folder: "diffusion_models", name: "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors" },
                ModelFile { folder: "diffusion_models", name: "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors" },
                ModelFile { folder: "text_encoders", name: "umt5_xxl_fp8_e4m3fn_scaled.safetensors" },
                ModelFile { folder: "vae", name: "wan_2.1_vae.safetensors" },
                ModelFile { folder: "loras", name: "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors" },
                ModelFile { folder: "loras", name: "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors" },
            ],
            source: "official template video_wan2_2_14B_i2v.json (4-step LoRA branch)", status: "graph from the official template; not yet run by us",
        }
    }
    fn output_node(&self) -> &'static str { "save" }
    fn workflow(&self, req: &GenerationRequest) -> Result<Value> {
        let info = self.info();
        let (w, h) = size(&info, &req.aspect)?;
        let Some(img) = &req.start_image else { return err("reference_required", "this model is image-to-video: the scene needs a visual reference") };
        if req.prompt.trim().is_empty() { return err("bad_request", "the prompt is empty"); }
        let mut g = serde_json::Map::new();
        g.insert("unet_high".into(), json!({ "class_type": "UNETLoader", "inputs": { "unet_name": info.files[0].name, "weight_dtype": "default" } }));
        g.insert("unet_low".into(), json!({ "class_type": "UNETLoader", "inputs": { "unet_name": info.files[1].name, "weight_dtype": "default" } }));
        g.insert("clip".into(), json!({ "class_type": "CLIPLoader", "inputs": { "clip_name": info.files[2].name, "type": "wan", "device": "default" } }));
        g.insert("vae".into(), json!({ "class_type": "VAELoader", "inputs": { "vae_name": info.files[3].name } }));
        g.insert("fast_high".into(), json!({ "class_type": "LoraLoaderModelOnly", "inputs": { "model": ["unet_high", 0], "lora_name": info.files[4].name, "strength_model": 1.0 } }));
        g.insert("fast_low".into(), json!({ "class_type": "LoraLoaderModelOnly", "inputs": { "model": ["unet_low", 0], "lora_name": info.files[5].name, "strength_model": 1.0 } }));
        let high = add_loras(&mut g, "fast_high".into(), &req.loras, "lora_h");
        let low = add_loras(&mut g, "fast_low".into(), &req.loras, "lora_l");
        g.insert("shift_high".into(), json!({ "class_type": "ModelSamplingSD3", "inputs": { "model": [high, 0], "shift": 5.0 } }));
        g.insert("shift_low".into(), json!({ "class_type": "ModelSamplingSD3", "inputs": { "model": [low, 0], "shift": 5.0 } }));
        g.insert("pos".into(), json!({ "class_type": "CLIPTextEncode", "inputs": { "clip": ["clip", 0], "text": req.prompt } }));
        g.insert("neg".into(), json!({ "class_type": "CLIPTextEncode", "inputs": { "clip": ["clip", 0], "text": negative(req) } }));
        g.insert("image".into(), json!({ "class_type": "LoadImage", "inputs": { "image": img } }));
        g.insert("i2v".into(), json!({ "class_type": "WanImageToVideo", "inputs": { "positive": ["pos", 0], "negative": ["neg", 0], "vae": ["vae", 0], "width": w, "height": h,
            "length": frames_for(&info, req.seconds), "batch_size": 1, "start_image": ["image", 0] } }));
        g.insert("sample_high".into(), json!({ "class_type": "KSamplerAdvanced", "inputs": { "model": ["shift_high", 0], "positive": ["i2v", 0], "negative": ["i2v", 1], "latent_image": ["i2v", 2],
            "add_noise": "enable", "noise_seed": req.seed, "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable" } }));
        g.insert("sample_low".into(), json!({ "class_type": "KSamplerAdvanced", "inputs": { "model": ["shift_low", 0], "positive": ["i2v", 0], "negative": ["i2v", 1], "latent_image": ["sample_high", 0],
            "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable" } }));
        g.insert("decode".into(), json!({ "class_type": "VAEDecode", "inputs": { "samples": ["sample_low", 0], "vae": ["vae", 0] } }));
        save_nodes(&mut g, ("decode", 0), info.fps, &req.filename_prefix);
        Ok(Value::Object(g))
    }
}
