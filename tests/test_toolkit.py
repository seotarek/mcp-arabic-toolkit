import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mcp_arabic.normalizer import ArabicNormalizer
from mcp_arabic.dialect_detector import ArabicDialectDetector
from mcp_arabic.server import handle_call_tool

class TestArabicToolkit(unittest.TestCase):
    def test_normalization(self):
        sample = "الإِنْسَانُ بِالعِلْمِ يَسْعَىٰ"
        norm = ArabicNormalizer.normalize(sample)
        self.assertEqual(norm, "الانسان بالعلم يسعي")
        
    def test_strip_diacritics(self):
        sample = "مَرْحَبًا بِكُمْ"
        clean = ArabicNormalizer.strip_diacritics(sample)
        self.assertEqual(clean, "مرحبا بكم")

    def test_dialect_detection(self):
        egyptian = "ازيك يا جدع عامل ايه دلوقتي؟"
        res = ArabicDialectDetector.detect(egyptian)
        self.assertEqual(res["detected_dialect"], "Egyptian (EGY)")
        self.assertGreater(res["confidence"], 0.70)
        
        levantine = "شو اخبارك وكيفك شو عم تعمل هلق؟"
        res2 = ArabicDialectDetector.detect(levantine)
        self.assertEqual(res2["detected_dialect"], "Levantine (LEV)")

    def test_tool_calling(self):
        res = handle_call_tool("arabic_detect_dialect", {"text": "عايز اروح البيت دلوقتي عشان مستعجل"})
        self.assertEqual(res["detected_dialect"], "Egyptian (EGY)")

if __name__ == '__main__':
    unittest.main()
