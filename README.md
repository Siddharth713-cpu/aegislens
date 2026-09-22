# AegisLens: Edge-Native Multimodal Copilot

[![Platform](https://img.shields.io/badge/Platform-Windows_ARM64-0078D4)](https://microsoft.com)
[![Hardware Target](https://img.shields.io/badge/Target-HP_OmniBook_X-0096D6)](https://hp.com)
[![Accelerator](https://img.shields.io/badge/NPU-Hexagon_45_TOPS-D9381E)](https://qualcomm.com)
[![Qualcomm AI Hub](https://img.shields.io/badge/AI_Hub-Profile_jgd3j01lp-6366F1)](https://aihub.qualcomm.com)

> Private by design. Useful in real time. Optimized for Snapdragon®-powered HP PCs (HP OmniBook X).  
> Built by **Siddharth Goyal** for the **Snapdragon® AI Lab Build & Present Challenge**.

---

## 📌 Project Overview



AegisLens is an on-device multimodal meeting assistant designed to keep sensitive screen shares, audio, and meeting context strictly within the local hardware boundary. By offloading speech recognition, visual credential redaction, and semantic recall to the \*\*45 TOPS Hexagon NPU\*\* on \*\*Snapdragon X Series HP PCs (HP OmniBook X)\*\*, it maintains low latency and preserves battery life without streaming unredacted data to cloud APIs.



## 🛠️ Architecture & Dataflow

```text
[ WASAPI Audio Loopback ] ──> [ Whisper-Small W8A16 ] ────┐
                                                         ├──> [ Llama 3.2 1B W4 ] ──> [ WinUI 3 UI / Tasks ]
[ DXGI Screen Capture  ] ──> [ YOLOv8 W8A8 Vision Guard] ┘             │
                                                                       ▼
                                                       [ MiniLM-v2 (384-D) + SQLite Index ]
                                                                       │
                                                       (100% On-Device / Zero Cloud Egress)
```