"""
AegisLens - Privacy Guard Redaction Engine
Detects and masks sensitive credentials and PII on outgoing screen frames.
"""

import re
import cv2
import numpy as np

class PrivacyGuard:
    def __init__(self):
        self.regex_rules = {
            "API_KEY": re.compile(r"(sk-[a-zA-Z0-9]{24,}|AKIA[0-9A-Z]{16})"),
            "INVOICE_TOTAL": re.compile(r"(₹|\$)\s?[0-9,]+(\.[0-9]{2})?"),
            "SECRET_BEARER": re.compile(r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}"),
        }

    def sanitize_text(self, raw_text: str) -> str:
        clean_text = raw_text
        for category, pattern in self.regex_rules.items():
            clean_text = pattern.sub(f"[REDACTED: {category}]", clean_text)
        return clean_text

    def redact_frame_region(self, frame: np.ndarray, boxes: list) -> np.ndarray:
        redacted = frame.copy()
        for (x, y, w, h) in boxes:
            x, y, w, h = max(0, x), max(0, y), max(1, w), max(1, h)
            roi = redacted[y:y+h, x:x+w]
            if roi.size > 0:
                blurred = cv2.GaussianBlur(roi, (45, 45), 0)
                redacted[y:y+h, x:x+w] = blurred
                cv2.rectangle(redacted, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(redacted, "[MASKED ON NPU]", (x, max(y - 6, 12)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
        return redacted

if __name__ == "__main__":
    guard = PrivacyGuard()
    sample = "Live share: token sk-live98472918472194812 with billing total ₹84,500."
    print("Incoming :", sample)
    print("Sanitized:", guard.sanitize_text(sample))