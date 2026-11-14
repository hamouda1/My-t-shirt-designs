"""
Niche Router for Pinterest Print-On-Demand Apparel Automation
=============================================================
Maps design keywords and themes to target Pinterest accounts and verified Board IDs.
Supports multi-account routing across marrytreasures, habiboumez, and GlowFormWellness.
"""

import re
from typing import Dict, Any, Optional

NICHE_REGISTRY = {
    # Specific subject niches
    "cats": {
        "keywords": ["cat", "kitten", "kitty", "feline", "meow", "witchy cat", "coffee cat", "cat mom", "black cat"],
        "account": "marrytreasures",
        "board_id": "677440037639070445",
        "board_name": "Funny Cat Lover Gifts & Novelty Graphic Shirts",
        "recommended_template": "streetwear-polaroid",
        "category_label": "Cat Lover Aesthetics",
        "default_palette": "terracotta",
        "weight_boost": 5
    },
    "vintage_cars": {
        "keywords": ["car", "cars", "vintage car", "classic car", "muscle car", "racing", "garage", "mechanic", "mustang"],
        "account": "marrytreasures",
        "board_id": "677440037639166340",
        "board_name": "Vintage Car Shirts & Classic Car Enthusiast Gifts",
        "recommended_template": "split-detail-zoom",
        "category_label": "Vintage Auto & Garage",
        "default_palette": "navy",
        "weight_boost": 5
    },
    "sarcastic": {
        "keywords": ["sarcastic", "sarcasm", "funny", "introvert", "humor", "joke", "meme", "quote", "mood"],
        "account": "marrytreasures",
        "board_id": "677440037639094964",
        "board_name": "Funny Sarcastic Shirts & Humorous Novelty Gifts",
        "recommended_template": "split-detail-zoom",
        "category_label": "Novelty & Sarcastic Tees",
        "default_palette": "slate"
    },
    "streetwear": {
        "keywords": ["streetwear", "grunge", "y2k", "urban", "cyberpunk", "tokyo", "skater", "aesthetic tee"],
        "account": "marrytreasures",
        "board_id": "677440037639070616",
        "board_name": "Trending Graphic Tees & Streetwear Fits",
        "recommended_template": "dark-noir-streetwear",
        "category_label": "Urban Streetwear Fits",
        "default_palette": "slate"
    },
    "retro_90s": {
        "keywords": ["retro", "vintage", "90s", "80s", "nostalgia", "cassette", "synthwave", "vaporwave"],
        "account": "habiboumez",
        "board_id": "1093037840753522211",
        "board_name": "Vintage Retro Tees & 90s Aesthetic Fits",
        "recommended_template": "streetwear-polaroid",
        "category_label": "Vintage Retro Fits",
        "default_palette": "amber"
    },
    "fitness": {
        "keywords": ["walking", "walk", "fitness", "gym", "pilates", "workout", "activewear", "athleisure"],
        "account": "marrytreasures",
        "board_id": "677440037639068349",
        "board_name": "Walking Club Graphic Tees & Daily Fitness Gifts",
        "recommended_template": "outfit-inspo-guide",
        "category_label": "Active Lifestyle & Gym",
        "default_palette": "emerald"
    },
    "scifi_alien": {
        "keywords": ["alien", "area 51", "ufo", "space", "galaxy", "extraterrestrial", "cosmic"],
        "account": "marrytreasures",
        "board_id": "677440037637741879",
        "board_name": "Alien Area 51 Graphic Tees & UFO Aesthetic Shirts",
        "recommended_template": "dark-noir-streetwear",
        "category_label": "Sci-Fi & Cosmic Fits",
        "default_palette": "slate"
    },
    "thanksgiving": {
        "keywords": ["thanksgiving", "turkey", "gobble", "pumpkin", "pumpkins", "autumn harvest", "fall season", "squash", "fall foliage", "feast mode", "autumnal"],
        "account": "marrytreasures",
        "board_id": "677440037639168259",
        "board_name": "Thanksgiving Turkey Shirts & Autumn Feast Tees",
        "recommended_template": "outfit-inspo-guide",
        "category_label": "Thanksgiving & Autumn Fits",
        "default_palette": "amber",
        "weight_boost": 8
    },
    "coffee_tea": {
        "keywords": ["iced coffee", "chill brew", "matcha", "barista", "latte", "coffee lover", "morning beverage"],
        "account": "marrytreasures",
        "board_id": "677440037639094964",
        "board_name": "Funny Sarcastic Shirts & Humorous Novelty Gifts",
        "recommended_template": "color-variants-swatches",
        "category_label": "Coffee & Matcha Aesthetics",
        "default_palette": "terracotta",
        "weight_boost": 6
    },
    "running_fitness": {
        "keywords": ["running club", "running", "runner", "marathon", "turtle graphic", "jogging", "walking club", "daily fitness"],
        "account": "marrytreasures",
        "board_id": "677440037639068349",
        "board_name": "Walking Club Graphic Tees & Daily Fitness Gifts",
        "recommended_template": "outfit-inspo-guide",
        "category_label": "Active Lifestyle & Fitness",
        "default_palette": "emerald",
        "weight_boost": 6
    },
    "bridal_party": {
        "keywords": ["bride", "bachelorette", "bridal", "bachelorette party", "wedding crew", "bride weekend"],
        "account": "marrytreasures",
        "board_id": "677440037639189659",
        "board_name": "Bridal Shower & Bachelorette Cards",
        "recommended_template": "streetwear-polaroid",
        "category_label": "Bachelorette & Bride Era Fits",
        "default_palette": "burgundy",
        "weight_boost": 6
    },
    "nurses": {
        "keywords": ["nurse", "stethoscope", "healthcare", "hospital", "scrub", "rn life"],
        "account": "marrytreasures",
        "board_id": "677440037639094964",
        "board_name": "Funny Sarcastic Shirts & Humorous Novelty Gifts",
        "recommended_template": "split-detail-zoom",
        "category_label": "Healthcare & Nurse Appreciation",
        "default_palette": "burgundy",
        "weight_boost": 6
    },
    "kindness": {
        "keywords": ["kindness", "be kind", "positive", "mental health", "good vibes", "sunshine", "peace"],
        "account": "marrytreasures",
        "board_id": "677440037638812209",
        "board_name": "Kindness Graphic Tees & Be Kind Aesthetic Shirts",
        "recommended_template": "color-variants-swatches",
        "category_label": "Positive Vibes & Inspo",
        "default_palette": "amber"
    },
    "mom_gifts": {
        "keywords": ["mom", "mother", "mom life", "mama", "mothers day", "best mom"],
        "account": "marrytreasures",
        "board_id": "677440037639127728",
        "board_name": "Mother's Day Gift Ideas & Best Mom Life Shirts",
        "recommended_template": "outfit-inspo-guide",
        "category_label": "Mom Life & Gift Ideas",
        "default_palette": "burgundy"
    },
    "art_creative": {
        "keywords": ["artist", "art lover", "creative", "painter", "sketch", "museum", "drawing"],
        "account": "marrytreasures",
        "board_id": "677440037637593903",
        "board_name": "Artist Graphic Tees & Creative Art Lover Gifts",
        "recommended_template": "arch-editorial",
        "category_label": "Creative Art & Design",
        "default_palette": "terracotta"
    }
}

DEFAULT_FALLBACK = {
    "niche": "streetwear",
    "account": "marrytreasures",
    "board_id": "677440037639070616",
    "board_name": "Trending Graphic Tees & Streetwear Fits",
    "recommended_template": "dark-noir-streetwear",
    "category_label": "Trending Streetwear",
    "default_palette": "slate"
}

def detect_niche(text_or_filename: str) -> Dict[str, Any]:
    """
    Scans a filename, design title, or keyword string against the niche registry.
    Returns full routing metadata including account, board_id, and template.
    """
    clean_text = text_or_filename.lower().replace("_", " ").replace("-", " ")
    
    # Check for direct keyword matches (longer keywords prioritized)
    best_match = None
    best_score = 0
    
    for niche_key, data in NICHE_REGISTRY.items():
        score = 0
        boost = data.get("weight_boost", 0)
        for kw in data["keywords"]:
            if re.search(r'\b' + re.escape(kw) + r'\b', clean_text):
                score += len(kw) * 3 + boost
            elif kw in clean_text:
                score += len(kw) + boost
        
        if score > best_score:
            best_score = score
            best_match = {**data, "niche": niche_key}
            
    if best_match:
        return best_match
        
    return DEFAULT_FALLBACK.copy()

if __name__ == "__main__":
    test_samples = [
        "witchy_black_cat_coffee_retro_tee.png",
        "vintage_mustang_muscle_car_1969.png",
        "introvert_sarcastic_humor_shirt.png",
        "morning_walking_club_routine.png",
        "unknown_urban_cyberpunk_hoodie.png"
    ]
    print("--- Testing Niche Router ---")
    for s in test_samples:
        res = detect_niche(s)
        print(f"Input: {s}")
        print(f"  -> Niche: {res['niche']} | Account: {res['account']}")
        print(f"  -> Board: {res['board_name']} (ID: {res['board_id']})")
        print(f"  -> Template: {res['recommended_template']}\n")
