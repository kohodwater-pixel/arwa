//! ComfyUI integration: one HTTP/WebSocket client, and one adapter per model family.
//! Adapters differ in workflow graph, model files and limits; nothing outside this module assumes
//! that two models share a workflow.
pub mod client;
pub mod wan22;

use crate::error::Result;
use serde::Serialize;
use serde_json::Value;

#[derive(Debug, Clone, Serialize)]
pub struct ModelFile {
    /// ComfyUI model folder, as used by GET /models/{folder}
    pub folder: &'static str,
    pub name: &'static str,
}

#[derive(Debug, Clone, Serialize)]
pub struct ModelInfo {
    pub id: &'static str,
    pub label: &'static str,
    pub family: &'static str,
    /// LoRA files are only compatible within the same lora_family.
    pub lora_family: &'static str,
    pub licence: &'static str,
    pub tasks: &'static [&'static str],
    pub fps: u32,
    pub max_frames: u32,
    /// frame counts must be frame_step * n + 1
    pub frame_step: u32,
    pub sizes: &'static [(&'static str, u32, u32)],
    pub min_vram_gb: u32,
    pub steps: u32,
    pub required_nodes: &'static [&'static str],
    pub files: &'static [ModelFile],
    pub source: &'static str,
    pub status: &'static str,
}

#[derive(Debug, Clone)]
pub struct GenerationRequest {
    pub prompt: String,
    pub negative_prompt: String,
    pub aspect: String,
    pub seconds: f64,
    pub seed: u64,
    /// File name returned by ComfyUI after uploading the reference image (image-to-video).
    pub start_image: Option<String>,
    /// (file name inside ComfyUI's loras folder, strength)
    pub loras: Vec<(String, f64)>,
    pub filename_prefix: String,
}

pub trait ModelAdapter: Send + Sync {
    fn info(&self) -> ModelInfo;
    /// Builds the API-format workflow graph for POST /prompt.
    fn workflow(&self, req: &GenerationRequest) -> Result<Value>;
    /// Node id whose output carries the finished video in /history.
    fn output_node(&self) -> &'static str;
}

pub fn adapters() -> Vec<Box<dyn ModelAdapter>> {
    vec![Box::new(wan22::Ti2v5b), Box::new(wan22::I2v14bLightning)]
}
pub fn adapter(id: &str) -> Option<Box<dyn ModelAdapter>> {
    adapters().into_iter().find(|a| a.info().id == id)
}

/// Frames for a duration: rounded up to the model's step rule and capped at its maximum.
pub fn frames_for(info: &ModelInfo, seconds: f64) -> u32 {
    let want = (seconds * info.fps as f64).round().max(1.0) as u32;
    let n = ((want.saturating_sub(1)) as f64 / info.frame_step as f64).ceil() as u32;
    (n * info.frame_step + 1).min(info.max_frames)
}
pub fn max_seconds(info: &ModelInfo) -> f64 {
    info.max_frames as f64 / info.fps as f64
}
