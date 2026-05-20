#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

for name in [
    "video1_manual_vs_automation.html",
    "video2_4_types_testing.html",
    "phase2_selenium_webdriver.html",
    "phase3_testng_pom.html",
]:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\s*const stopSpeakBtn = document\.getElementById\('stopSpeakBtn'\);\n", "\n", text)
    text = text.replace("            stopSpeakBtn.hidden = true;\n", "")
    text = re.sub(
        r"""        function speak\(\) \{
            const slide = slides\[currentSlide\];
            if \(!slide\.querySelector\('\.narration-box'\)\) return;
            stopSpeakBtn\.hidden = false;
            VietnameseTTS\.speakSlide\(ttsPage, currentSlide, \{
                onEnd: function \(\) \{ stopSpeakBtn\.hidden = true; \}
            \}\);
        \}""",
        """        function speak() {
            const slide = slides[currentSlide];
            if (!slide.querySelector('.narration-box')) return;
            VietnameseTTS.speakSlide(ttsPage, currentSlide);
        }""",
        text,
    )
    text = re.sub(
        r"\s*stopSpeakBtn\.addEventListener\('click', function \(\) \{\s*"
        r"VietnameseTTS\.stop\(\);\s*stopSpeakBtn\.hidden = true;\s*\}\);\n",
        "\n",
        text,
    )
    path.write_text(encoding="utf-8", data=text)
    print("js patched", name)
