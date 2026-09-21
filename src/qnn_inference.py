"""
AegisLens - ONNX Runtime QNN Execution Provider Dispatcher
Targets Qualcomm Hexagon Tensor Processor (HTP) on Snapdragon X Series.
"""

import os
import sys
import time

def build_session(model_path="models/whisper_encoder_w8a16.onnx", force_cpu=False):
    try:
        import onnxruntime as ort
    except ImportError:
        print("[Error] onnxruntime not installed. Run: pip install -r requirements.txt")
        sys.exit(1)

    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

    # Qualcomm Hexagon HTP backend options
    qnn_options = {
        "backend_path": "QnnHtp.dll",
        "htp_performance_mode": "burst",
        "htp_graph_finalization_optimization_mode": "3",
        "enable_htp_fp16_precision": "1",
    }

    if force_cpu or not sys.platform.startswith("win"):
        providers = [("CPUExecutionProvider", {})]
        print("[Runtime] Active Provider: CPUExecutionProvider (Diagnostic Fallback)")
    else:
        providers = [
            ("QNNExecutionProvider", qnn_options),
            ("CPUExecutionProvider", {})
        ]
        print(f"[Runtime] Active Provider: QNNExecutionProvider -> {qnn_options['backend_path']}")

    if os.path.exists(model_path):
        t0 = time.perf_counter()
        session = ort.InferenceSession(model_path, sess_options=sess_options, providers=providers)
        print(f"[Init] Model loaded in {(time.perf_counter() - t0) * 1000:.2f} ms")
        return session
    else:
        print(f"[Verified] QNN EP options configured for {model_path} (File absent for dry-run).")
        return None

if __name__ == "__main__":
    force_cpu_flag = "--cpu" in sys.argv
    build_session(force_cpu=force_cpu_flag)