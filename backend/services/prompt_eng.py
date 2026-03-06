"""
Prompt Engineering Service
Enriches user input with Marseille/futurisme vocabulary
"""

import random
from utils.prompts import (
    build_enriched_prompt,
    MARSEILLE_VOCABULARY,
    FUTURISME_VOCABULARY,
    STYLE_MODIFIERS
)


class PromptEngineer:
    """Handles prompt enrichment and transformation"""

    @staticmethod
    def enrich(text: str, style: str = "futuristic") -> dict:
        """
        Transform simple text into rich AI-prompt
        
        Args:
            text: Original user input
            style: Style to apply (futuristic, cyberpunk, utopian, dystopian)
            
        Returns:
            dict with enriched prompt and metadata
        """
        # Get enriched version
        marseille_elements = MARSEILLE_VOCABULARY.get('elements', [])
        futurisme_aesthetics = FUTURISME_VOCABULARY.get('aesthetics', [])
        
        marseille_words = random.sample(marseille_elements, min(2, len(marseille_elements))) if marseille_elements else []
        futurisme_words = random.sample(futurisme_aesthetics, min(2, len(futurisme_aesthetics))) if futurisme_aesthetics else []
        enriched = build_enriched_prompt(text, marseille_words, futurisme_words, style)
        
        # Add style modifier (pick from list)
        style_mod = random.choice(STYLE_MODIFIERS) if STYLE_MODIFIERS else "artistic"
        enriched += f", {style_mod}"
        
        # Add random Marseille location
        marseille_locations = MARSEILLE_VOCABULARY.get('locations', ['Marseille'])
        marseille_location = random.choice(marseille_locations) if marseille_locations else 'Marseille'
        marseille_spirit = random.choice(marseille_words) if marseille_words else 'vibrant'
        
        enriched = f"{enriched}, inspired by {marseille_location} and {marseille_spirit}"
        
        return {
            'original': text,
            'enriched': enriched,
            'keywords': marseille_words + futurisme_words,
            'style': style,
            'marseille_elements': [marseille_location, marseille_spirit]
        }


def enrich_prompt(text: str, style: str = "futuristic") -> dict:
    """Convenience function for prompt enrichment"""
    return PromptEngineer.enrich(text, style)
