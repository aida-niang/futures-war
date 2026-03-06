"""
Vocabulary and prompt templates
Includes professor-provided vocabulary from banque_de_prompts
"""

# Marseille vocabulary (expanded from banque_de_prompts)
MARSEILLE_VOCABULARY = {
    "locations": [
        "Vieux Port",
        "Basilique Notre-Dame de la Garde",
        "Cannebière",
        "Fort Saint-Jean",
        "Château d'If",
        "Panier neighborhood",
        "Pharo palace",
        "MuCEM museum",
        "Corniche Kennedy",
        "Saint-Jean castle",
        "harbor boats",
        "pastel houses",
        "Mediterranean coast",
        "limestone cliffs",
        "fishing village",
        "urban waterfront",
        "historic traboules",
        "Lyon Confluence",
        "Saint-Étienne industrial",
    ],
    "elements": [
        "harbor boats",
        "Mediterranean light",
        "breezy seaside",
        "warm tones",
        "cinematic close-up",
        "ancient stone walls",
        "urban regeneration",
        "lighthouse beacon",
        "fishing nets",
        "sailboats",
        "fishing harbor",
        "bustling market",
        "arched passages",
        "cobblestone squares",
    ]
}

# Futurism vocabulary (expanded from ComfyUI workflow & banque_de_prompts)
FUTURISME_VOCABULARY = {
    "aesthetics": [
        "neon cyberpunk",
        "solarpunk",
        "future vision",
        "holographic",
        "digital overlay",
        "augmented reality",
        "transparent surfaces",
        "glowing elements",
        "sleek modern",
        "tech-integrated",
        "biomimetic design",
        "floating structures",
        "luminescent",
        "chromatic shifts",
        "kinetic art",
    ],
    "tech_elements": [
        "AI-assisted",
        "holographic projection",
        "smart interfaces",
        "neural networks",
        "quantum computing",
        "biodegradable tech",
        "modular systems",
        "energy harvesting",
        "smart materials",
        "nano-structures",
        "cloud computing",
        "digital consciousness",
        "IoT sensors",
        "blockchain integration",
    ],
    "atmosphere": [
        "future-forward",
        "innovation hub",
        "technological harmony",
        "digital transformation",
        "sustainable innovation",
        "smart city",
        "connected ecosystem",
        "intelligent infrastructure",
        "data-driven",
        "autonomous systems",
        "ubiquitous computing",
        "ambient intelligence",
    ]
}

# Sustainable & Education vocabulary (from banque_de_prompts - Future School)
EDUCATION_VOCABULARY = {
    "school_elements": [
        "learning garden",
        "outdoor classroom",
        "collaborative workspace",
        "maker space",
        "digital lab",
        "green courtyard",
        "inclusive design",
        "student-centered",
        "active learning",
        "hands-on projects",
        "peer collaboration",
        "discovery learning",
        "mentorship moments",
        "interdisciplinary",
    ],
    "sustainability": [
        "climate-adaptive",
        "solar panels",
        "rainwater harvesting",
        "permeable surfaces",
        "urban green spaces",
        "biodiversity",
        "carbon-neutral",
        "renewable energy",
        "waste reduction",
        "ecosystem restoration",
        "circular economy",
        "zero-waste design",
        "local materials",
    ],
    "social_elements": [
        "community hub",
        "intergenerational",
        "co-development",
        "citizen participation",
        "shared resources",
        "local knowledge",
        "cooperative work",
        "cultural center",
        "public engagement",
        "democratic design",
    ]
}

# Prompt templates
PROMPT_TEMPLATES = [
    "A stunning {marseille} scene showing {element}, {atmosphere}, with {tech}, in {lighting}",
    "{marseille} reimagined with {futurisme}: {tech} integrated naturally, {atmosphere} energy, {lighting}",
    "Documentary-style shot of {marseille}, enhanced with {futurisme} elements and {tech}, {atmosphere} mood",
    "Cinematic {marseille} vista featuring {element}, {futurisme} aesthetic, {atmosphere} ambiance",
    "{edu_element} in {marseille}, incorporating {tech} and {futurisme}, {lighting} quality",
    "Solarpunk vision of {marseille}: {element} reimagined with {tech}, {sustainability} focus",
]

# Lighting modifiers
LIGHTING_MODIFIERS = [
    "golden hour light",
    "soft diffused daylight",
    "warm afternoon glow",
    "cool morning light",
    "dusk ambiance",
    "neon-lit",
    "bioluminescent",
    "cinematic lighting",
    "documentary realism",
    "film noir aesthetic",
    "35mm analog grain",
    "HDR enhanced",
]

# Style modifiers (from ComfyUI workflow)
STYLE_MODIFIERS = [
    "pixel art style",
    "photorealistic",
    "cinematic",
    "documentary",
    "watercolor",
    "oil painting",
    "digital art",
    "anime aesthetic",
    "retro futurism",
    "synthwave",
    "cyberpunk",
    "steampunk",
]

# Quality descriptors
QUALITY_DESCRIPTORS = [
    "ultra-detailed",
    "high resolution",
    "sharp focus",
    "professional lighting",
    "award-winning",
    "museum quality",
    "cinematic composition",
    "balanced exposure",
]


def build_enriched_prompt(text: str, marseille_words: list, futurisme_words: list, style: str = "futuristic") -> str:
    """
    Build enriched prompt from components
    
    Args:
        text: Original text
        marseille_words: Words/phrases from Marseille vocabulary
        futurisme_words: Words/phrases from Futurisme vocabulary
        style: Style modifier
        
    Returns:
        Enriched prompt string
    """
    import random
    
    # Build prompt parts
    prompt = text
    
    # Add Marseille context
    if marseille_words:
        marseille_context = " with " + ", ".join(random.sample(marseille_words, min(2, len(marseille_words))))
        prompt += marseille_context
    
    # Add futurisme elements
    if futurisme_words:
        futurisme_context = ", featuring " + " and ".join(random.sample(futurisme_words, min(2, len(futurisme_words))))
        prompt += futurisme_context
    
    # Add style
    prompt += f", {style} aesthetic"
    
    return prompt
