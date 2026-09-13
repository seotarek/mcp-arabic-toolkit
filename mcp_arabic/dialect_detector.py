import re
from typing import Dict, Any, Tuple

class ArabicDialectDetector:
    """Heuristic dialect classification across MSA, Egyptian, Levantine, Gulf, and Maghrebi."""
    
    DIALECT_MARKERS = {
        "Egyptian (EGY)": {
            "keywords": ["عايز", "عاوز", "كده", "دلوقتي", "ازيك", "علشان", "عشان", "ايه", "ليه", "بتاع", "برضه", "مش", "قوي", "خالص", "جدع", "طب"],
            "prefixes": ["ه", "م"],
            "regex": [r'\bمش\s+\w+', r'\b(عايز|عاوز)\b', r'\b(ايه|ليه)\b']
        },
        "Levantine (LEV)": {
            "keywords": ["شو", "شلونك", "بدي", "هيك", "هلق", "هلا", "مشان", "عم", "كتير", "منيح", "هاد", "هادا", "وينك"],
            "prefixes": ["عم"],
            "regex": [r'\bشو\s+\w+', r'\bبدي\b', r'\bعم\s+\w+']
        },
        "Gulf (GLF)": {
            "keywords": ["شلونك", "وشنو", "شخبارك", "وايد", "ابي", "ودي", "الحين", "زين", "صج", "شنو", "سالفة", "ريال", "دريشة"],
            "prefixes": [],
            "regex": [r'\b(شلونك|شخبارك)\b', r'\bوايد\b', r'\bشنو\b']
        },
        "Maghrebi (MAG)": {
            "keywords": ["ديال", "باش", "واخا", "زوين", "بزاف", "كيداير", "برشا", "شكون", "دابا", "علاش", "مزيان"],
            "prefixes": [],
            "regex": [r'\b(ديال|بزاف|واخا|زوين)\b', r'\bبرشا\b']
        }
    }

    @staticmethod
    def detect(text: str) -> Dict[str, Any]:
        lowered = text.strip()
        scores = {"Modern Standard Arabic (MSA)": 1.0}
        
        for dialect, rules in ArabicDialectDetector.DIALECT_MARKERS.items():
            dialect_score = 0
            for word in rules["keywords"]:
                if re.search(r'\b' + re.escape(word) + r'\b', lowered):
                    dialect_score += 2
            for reg in rules["regex"]:
                if re.search(reg, lowered):
                    dialect_score += 3
            if dialect_score > 0:
                scores[dialect] = dialect_score

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_dialect, top_score = sorted_scores[0]
        confidence = 0.50 if top_dialect == "Modern Standard Arabic (MSA)" else min(0.95, 0.40 + (top_score * 0.12))
        
        return {
            "detected_dialect": top_dialect,
            "confidence": round(confidence, 2),
            "distribution": {k: v for k, v in sorted_scores}
        }
