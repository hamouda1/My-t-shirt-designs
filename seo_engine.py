"""
Pinterest SEO & Zazzle Linkover URL Generator
=============================================
Generates keyword-rich, high-converting Pinterest Titles, Descriptions,
Alt Text, and dynamic affiliate Zazzle Linkover URLs with custom tracking codes.
"""

import urllib.parse
import random
from typing import Dict, Any

ZAZZLE_ASSOCIATE_ID = "238209628121657582"
ZAZZLE_PRODUCT_ID = "256252753051729445"  # Hanes Men's Crew 5250 Black T-Shirt
ZAZZLE_IMAGE_PARAM = "t_tshirttemp_iid"

SEO_NICHE_PROFILES = {
    "cats": {
        "title_prefixes": [
            "Funny Coffee Cat Graphic T-Shirt",
            "Witchy Cat Magic Aesthetic T-Shirt",
            "Vintage Retro Cat Lover Graphic Tee",
            "Cozy Coffee & Cats Novelty T-Shirt"
        ],
        "hooks": [
            "Sip coffee and ignore everyone with this cozy retro cat graphic tee.",
            "Bring celestial magic and feline humor to your everyday wardrobe.",
            "The ultimate aesthetic graphic t-shirt for coffee addicts and cat moms."
        ],
        "keywords": ["cat lover gift", "witchy aesthetic", "retro cat shirt", "funny feline tee", "coffee addict gift"],
        "tags": "#CatLover #WitchyAesthetic #CoffeeCat #GraphicTee #RetroVibes #ZazzleMade"
    },
    "sarcastic": {
        "title_prefixes": [
            "Funny Sarcastic Humor Graphic T-Shirt",
            "Introvert Mood Novelty Graphic Tee",
            "Sarcastic Quote Heavyweight T-Shirt",
            "Relatable Humor Vintage Graphic Shirt"
        ],
        "hooks": [
            "Let your t-shirt do the talking with this effortlessly sarcastic graphic tee.",
            "The perfect everyday tee for introverts who speak fluent sarcasm.",
            "Comfortable, witty, and unapologetically honest novelty apparel."
        ],
        "keywords": ["sarcastic quote shirt", "introvert tee", "funny gift for coworker", "novelty graphic tee"],
        "tags": "#SarcasticHumor #FunnyTee #IntrovertLife #NoveltyGifts #GraphicShirt"
    },
    "streetwear": {
        "title_prefixes": [
            "Oversized Grunge Streetwear Graphic Tee",
            "Vintage Cyberpunk Aesthetic T-Shirt",
            "Urban Retro Heavyweight Graphic Shirt",
            "90s Japanese Streetwear Graphic Tee"
        ],
        "hooks": [
            "Elevate your daily street style with this dark aesthetic heavyweight graphic tee.",
            "Bold typography and vintage grunge aesthetics meet all-day comfort.",
            "Essential drop-shoulder streetwear fit designed for modern layering."
        ],
        "keywords": ["oversized streetwear", "grunge aesthetic tee", "vintage urban shirt", "y2k cyberpunk clothes"],
        "tags": "#StreetwearFit #GrungeAesthetic #UrbanFashion #OversizedTee #GraphicTee"
    },
    "fitness": {
        "title_prefixes": [
            "Morning Walking Club Graphic T-Shirt",
            "Aesthetic Workout Routine Gym Tee",
            "Mindful Movement Athleisure Graphic Shirt",
            "Daily Fitness Club Heavyweight T-Shirt"
        ],
        "hooks": [
            "Stay motivated and comfortable on your daily strolls with the Walking Club tee.",
            "Aesthetic activewear meets cozy daily streetwear for your morning routines.",
            "Hit your step goals in breathable, premium ringspun cotton style."
        ],
        "keywords": ["walking club shirt", "athleisure graphic tee", "daily fitness routine", "cute gym outfit"],
        "tags": "#WalkingClub #Athleisure #FitnessInspo #DailyWalks #HealthyHabits"
    },
    "vintage_cars": {
        "title_prefixes": [
            "Vintage Classic Muscle Car Graphic T-Shirt",
            "Retro Garage Mechanic Graphic Tee",
            "Classic American Muscle Car Enthusiast Shirt",
            "Vintage Racing Heritage Heavyweight Tee"
        ],
        "hooks": [
            "Celebrate raw horsepower and vintage motor heritage with this classic garage tee.",
            "Engineered for classic car enthusiasts, hot rod fans, and garage mechanics.",
            "Timeless retro automotive illustration printed on premium heavy cotton."
        ],
        "keywords": ["classic car shirt", "muscle car gift", "mechanic graphic tee", "hot rod apparel"],
        "tags": "#ClassicCars #MuscleCar #VintageGarage #CarEnthusiast #RetroAutomotive"
    },
    "thanksgiving": {
        "title_prefixes": [
            "Funny Thanksgiving Turkey Feast Graphic T-Shirt",
            "Cozy Autumn Harvest Pumpkin Graphic Tee",
            "Gobble Squad Fall Season Novelty T-Shirt",
            "Feast Mode Thanksgiving Foodie Graphic Shirt"
        ],
        "hooks": [
            "Get feast-ready with this hilarious Thanksgiving holiday graphic tee.",
            "Celebrate autumn harvest, pumpkin pies, and cozy family gatherings in style.",
            "The ultimate playful holiday t-shirt for Thanksgiving dinner and Friendsgiving."
        ],
        "keywords": ["thanksgiving shirt", "turkey day tee", "gobble squad shirt", "fall harvest apparel", "feast mode gift"],
        "tags": "#ThanksgivingTee #GobbleSquad #FallHarvest #TurkeyDay #HolidayApparel"
    },
    "coffee_tea": {
        "title_prefixes": [
            "Chill Brew Club Iced Coffee Graphic T-Shirt",
            "Matcha Tea Lover Aesthetic Graphic Tee",
            "Cozy Coffee Break Heavyweight T-Shirt",
            "Retro Coffee Bar Drinker Graphic Shirt"
        ],
        "hooks": [
            "Fuel your morning routine with this aesthetic iced coffee & matcha graphic tee.",
            "Designed for coffee enthusiasts, iced latte fans, and matcha lovers.",
            "Keep it cool and caffeinated with this minimalist drink aesthetic streetwear shirt."
        ],
        "keywords": ["coffee lover shirt", "matcha graphic tee", "iced coffee aesthetic", "barista gift", "chill brew club"],
        "tags": "#CoffeeLover #MatchaClub #IcedCoffee #CoffeeAesthetic #StreetwearTee"
    },
    "running_fitness": {
        "title_prefixes": [
            "Slow Easy Running Club Turtle Graphic T-Shirt",
            "Vintage Aesthetic Running Club Sport Tee",
            "Daily Runner Community Heavyweight T-Shirt",
            "Marathon Training & Daily Jogging Graphic Shirt"
        ],
        "hooks": [
            "Take it at your own pace with the Slow & Easy Running Club aesthetic tee.",
            "Retro collegiate athletic vibes designed for joggers, walkers, and fitness lovers.",
            "Hit your weekly miles in breathable, heavyweight ringspun cotton comfort."
        ],
        "keywords": ["running club shirt", "runner graphic tee", "retro athletic apparel", "marathon training tee"],
        "tags": "#RunningClub #RunClub #RetroAthletics #FitnessLifestyle #DailyRun"
    },
    "bridal_party": {
        "title_prefixes": [
            "Retro Bachelorette Party Bride Graphic T-Shirt",
            "Bride Weekend Throwback Crew Graphic Tee",
            "Neon Nostalgia Bridal Era Heavyweight Shirt",
            "Trendy Bride Squad Bachelorette Graphic Tee"
        ],
        "hooks": [
            "Celebrate your bride era in iconic retro throwback style with your favorite crew.",
            "The perfect aesthetic bachelorette weekend group shirt for the bride and bridesmaids.",
            "Make unforgettable wedding memories in soft, premium matching bridal apparel."
        ],
        "keywords": ["bachelorette party shirt", "bride era tee", "bridal crew apparel", "wedding gift for bride"],
        "tags": "#BacheloretteParty #BrideEra #BridalShower #WeddingCrew #BacheloretteTees"
    },
    "nurses": {
        "title_prefixes": [
            "Thankful Nurse Autumn Gratitude Graphic T-Shirt",
            "Nurse Shift Fueled By Coffee Graphic Tee",
            "Healthcare Worker Healthcare Appreciation Shirt",
            "Stethoscope Floral Heart Cute Nurse Graphic Tee"
        ],
        "hooks": [
            "Show appreciation for incredible healthcare heroes with this cozy graphic tee.",
            "Powered by coffee and compassion: the perfect gift for dedicated nurses and medical pros.",
            "Comfortable, breathable cotton designed for well-deserved post-shift relaxation."
        ],
        "keywords": ["nurse appreciation shirt", "scrub life tee", "nurse gift idea", "healthcare worker shirt"],
        "tags": "#NurseLife #NurseAppreciation #HealthcareHero #ScrubSquad #ThankfulNurse"
    }
}

DEFAULT_PROFILE = {
    "title_prefixes": ["Trending Aesthetic Graphic T-Shirt", "Heavyweight Novelty Graphic Tee"],
    "hooks": ["Make a statement with this premium custom graphic t-shirt."],
    "keywords": ["graphic tee", "aesthetic apparel", "custom t-shirt", "gift idea"],
    "tags": "#GraphicTee #AestheticFashion #Streetwear #CustomApparel #Zazzle"
}

def generate_pin_title(design_name: str, niche_key: str) -> str:
    """Generates an SEO-optimized title under 100 characters."""
    profile = SEO_NICHE_PROFILES.get(niche_key, DEFAULT_PROFILE)
    prefix = random.choice(profile["title_prefixes"])
    clean_name = design_name.replace("_", " ").replace("-", " ").title()
    
    # Try combined format
    combined = f"{prefix} - {clean_name}"
    if len(combined) <= 100:
        return combined
    
    # Shorten if needed
    if len(prefix) <= 100:
        return prefix
        
    return prefix[:97] + "..."

def generate_pin_description(niche_key: str, board_name: str, account_name: str = "MarryTreasures") -> str:
    """Generates a rich, engaging description under 500 characters with keywords and CTA."""
    profile = SEO_NICHE_PROFILES.get(niche_key, DEFAULT_PROFILE)
    hook = random.choice(profile["hooks"])
    
    desc = (
        f"{hook} "
        f"Crafted on the iconic Hanes 100% pre-shrunk heavyweight ringspun cotton for a comfortable, classic unisex fit. "
        f"Available in sizes S to 5XL and multiple colorways. Perfect unique gift for birthdays and everyday wear. "
        f"👉 Tap the link to personalize shirt color & size directly on Zazzle!"
    )
    
    if len(desc) > 500:
        # Fallback trimmed
        desc = desc[:490] + "..."
        
    return desc

def generate_alt_text(design_name: str, niche_key: str, template_name: str) -> str:
    """Generates accessibility and OCR alt text under 500 characters."""
    clean_name = design_name.replace("_", " ").replace("-", " ").title()
    return (
        f"A professional Pinterest product mockup featuring a black graphic t-shirt with custom '{clean_name}' artwork. "
        f"Displayed in a modern {template_name} layout with aesthetic styling, clean typography, and retail color details."
    )[:500]

def build_zazzle_linkover_url(
    cdn_image_url: str,
    account: str = "marrytreasures",
    niche: str = "tee",
    associate_id: str = ZAZZLE_ASSOCIATE_ID,
    product_id: str = ZAZZLE_PRODUCT_ID
) -> str:
    """
    Constructs the official Zazzle Linkover dynamic creation URL.
    Ensures URL encoding of the remote image source.
    """
    tracking_code = f"pin_{account}_{niche[:8]}"
    encoded_img = urllib.parse.quote(cdn_image_url, safe='')
    
    url = (
        f"https://www.zazzle.com/api/create/at-{associate_id}?"
        f"rf={associate_id}&"
        f"ax=Linkover&"
        f"pd={product_id}&"
        f"ed=true&"
        f"tc={tracking_code}&"
        f"{ZAZZLE_IMAGE_PARAM}={encoded_img}"
    )
    return url

if __name__ == "__main__":
    test_cdn = "https://raw.githubusercontent.com/hamouda1/My-t-shirt-designs/main/designs/witchy_cat_coffee.png"
    niche = "cats"
    
    print("=== Testing SEO & Linkover Engine ===")
    t = generate_pin_title("Enchanting Witchy Cat", niche)
    print("Title (length", len(t), "):", t)
    
    d = generate_pin_description(niche, "Funny Cat Lover Gifts")
    print("\nDescription (length", len(d), "):", d)
    
    a = generate_alt_text("Enchanting Witchy Cat", niche, "streetwear-polaroid")
    print("\nAlt Text (length", len(a), "):", a)
    
    link = build_zazzle_linkover_url(test_cdn, account="marrytreasures", niche=niche)
    print("\nLinkover URL:\n", link)
