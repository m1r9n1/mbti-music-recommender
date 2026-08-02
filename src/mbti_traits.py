"""MBTI type to trait-keyword mapping, used to build retrieval queries."""

from typing import Dict, List

MBTI_TRAIT_KEYWORDS: Dict[str, List[str]] = {
    "INFP": ["idealistic", "introspective", "dreamy", "sensitive", "romantic"],
    "INFJ": ["empathetic", "introspective", "intuitive", "deep-connection", "reflective"],
    "ENFP": ["optimistic", "warm", "adventurous", "spontaneous", "energetic"],
    "ENFJ": ["compassionate", "inspiring", "community-minded", "sincere", "warm"],
    "INTJ": ["visionary", "strategic", "analytical", "independent", "contemplative"],
    "INTP": ["analytical", "curious", "imaginative", "detached", "overthinking"],
    "ENTJ": ["ambitious", "driven", "commanding", "competitive", "resilient"],
    "ENTP": ["inventive", "witty", "unconventional", "bold", "energetic"],
    "ISFP": ["gentle", "artistic", "sensitive", "laid-back", "tender"],
    "ISFJ": ["devoted", "warm", "nostalgic", "loyal", "grounded"],
    "ESFP": ["playful", "vibrant", "confident", "carefree", "social"],
    "ESFJ": ["supportive", "cheerful", "dependable", "community-minded", "warm"],
    "ISTP": ["independent", "gritty", "minimalist", "resilient", "blunt"],
    "ISTJ": ["steady", "disciplined", "principled", "methodical", "reserved"],
    "ESTP": ["bold", "spontaneous", "thrill-seeking", "charismatic", "action-driven"],
    "ESTJ": ["direct", "goal-driven", "practical", "structured", "decisive"],
}


def build_query_text(mbti_type: str) -> str:
    """Builds a retrieval query string from an MBTI type's trait keywords."""
    mbti_type = mbti_type.upper()
    if mbti_type not in MBTI_TRAIT_KEYWORDS:
        raise ValueError(f"Unknown MBTI type: {mbti_type}")
    return ", ".join(MBTI_TRAIT_KEYWORDS[mbti_type])
