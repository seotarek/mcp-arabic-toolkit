import re
from typing import Dict, Any

class ArabicNormalizer:
    """High-speed Arabic text normalization and cleaning."""
    
    TASHKEEL = re.compile(r'[\u064B-\u0652\u0670\u0640]')
    ALEF_PATTERNS = re.compile(r'[\u0622\u0623\u0625\u0671]')
    YAA_PATTERNS = re.compile(r'[\u0649]')
    TAA_MARBUTA = re.compile(r'[\u0629]')
    MULTIPLE_SPACES = re.compile(r'\s+')

    @staticmethod
    def strip_diacritics(text: str) -> str:
        """Removes all Harakat (Tashkeel) and Tatweel from Arabic text."""
        return ArabicNormalizer.TASHKEEL.sub('', text)

    @staticmethod
    def normalize(text: str, unify_alef: bool = True, unify_yaa: bool = True, unify_taa: bool = False) -> str:
        """Normalizes common variations of Arabic characters."""
        cleaned = text
        if unify_alef:
            cleaned = ArabicNormalizer.ALEF_PATTERNS.sub('ا', cleaned)
        if unify_yaa:
            cleaned = ArabicNormalizer.YAA_PATTERNS.sub('ي', cleaned)
        if unify_taa:
            cleaned = ArabicNormalizer.TAA_MARBUTA.sub('ه', cleaned)
        
        cleaned = ArabicNormalizer.TASHKEEL.sub('', cleaned)
        cleaned = ArabicNormalizer.MULTIPLE_SPACES.sub(' ', cleaned).strip()
        return cleaned
