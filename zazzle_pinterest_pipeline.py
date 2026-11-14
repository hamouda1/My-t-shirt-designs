"""
End-to-End Zazzle-to-Pinterest POD Publishing Pipeline
======================================================
Official 3-Step Lifecycle:
  1. Bind Artwork to Zazzle Product Template via Zazzle Creation API
     -> Fetches Zazzle's authentic photorealistic rendered front view (rlv.zcache.com).
  2. Embed the Official Zazzle Render into HTML Pin Engine
     -> Renders 1000x1500 high-converting Pinterest pin mockup with SEO & branding.
  3. Publish Live or Schedule across Niche-Matched Pinterest Boards.
"""

import os
import sys
import json
import base64
import time
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "html_pin_engine"))

from niche_router import detect_niche
import seo_engine
from zazzle_renderer import get_zazzle_dynamic_render
from engine import HTMLPinEngine, PALETTES
from github_storage import GitHubStorage

PINTEREST_DIR = Path(r"C:\Users\KIZMO STORE\Documents\pinterest")
if str(PINTEREST_DIR) not in sys.path:
    sys.path.insert(0, str(PINTEREST_DIR))
from pinterest_api import PinterestAPI

ACCOUNTS_FILE = PINTEREST_DIR / "accounts.json"

ZAZZLE_PID = "256252753051729445"  # Hanes Crew 5250 Black T-Shirt
ZAZZLE_ASSOCIATE_ID = "238209628121657582"
ZAZZLE_PARAM = "t_tshirttemp_iid"

class ZazzlePinterestPipeline:
    def __init__(self, browser_channel="msedge"):
        self.engine = HTMLPinEngine(browser_channel=browser_channel)
        self.storage = GitHubStorage()
        self.output_dir = ROOT_DIR / "html_pin_engine" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.renders_cache = ROOT_DIR / "zazzle_renders"
        self.renders_cache.mkdir(parents=True, exist_ok=True)
        self.accounts_data = self._load_accounts()

    def _load_accounts(self) -> Dict[str, Any]:
        if ACCOUNTS_FILE.exists():
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("accounts", {})
        return {}

    def process_design(
        self,
        artwork_filename_or_path: str,
        cdn_url: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Executes the complete 3-step automated pipeline.
        """
        print("\n" + "=" * 70)
        print(f"🚀 PIPELINE START: {Path(artwork_filename_or_path).name}")
        print("=" * 70)

        # 1. Niche & Routing Identification
        niche_info = detect_niche(artwork_filename_or_path)
        niche_key = niche_info["niche"]
        account_name = niche_info["account"]
        board_id = niche_info["board_id"]
        board_name = niche_info["board_name"]
        template_name = niche_info["recommended_template"]
        palette = PALETTES.get(niche_info.get("default_palette"), PALETTES["terracotta"])

        print(f"🔍 [Step 0] Niche: {niche_key.upper()} -> Board: {board_name} ({account_name})")

        # 2. Ensure design is on GitHub Raw CDN
        effective_cdn = cdn_url
        if not effective_cdn:
            local_p = Path(artwork_filename_or_path)
            if local_p.exists():
                print(f"📤 Uploading design to GitHub CDN: {local_p.name}...")
                effective_cdn = self.storage.upload_image(local_p, local_p.name)
            else:
                effective_cdn = f"https://raw.githubusercontent.com/hamouda1/My-t-shirt-designs/main/designs/{local_p.name}"

        print(f"🌐 CDN Source: {effective_cdn}")

        # -------------------------------------------------------------
        # STEP 1: Bind Artwork to Zazzle Template via Creation API
        # -------------------------------------------------------------
        print("\n⚙️ [Step 1/3] Binding Artwork to Zazzle Template via Creation API...")
        guid, product_url, official_render_url = get_zazzle_dynamic_render(
            pid=ZAZZLE_PID,
            associate_id=ZAZZLE_ASSOCIATE_ID,
            template_param=ZAZZLE_PARAM,
            cdn_image_url=effective_cdn,
            max_dim=1000,
            tracking_code=f"pin_{account_name}_{niche_key[:8]}"
        )
        print(f"   ✅ Zazzle Generated Image GUID: {guid}")
        print(f"   🎯 Zazzle Customer Destination: {product_url}")

        # Download Zazzle's authentic RealView render (with view=front for centered chest print)
        front_render_url = f"{official_render_url}&view=front"
        clean_name = Path(artwork_filename_or_path).stem
        local_render_path = self.renders_cache / f"zazzle_render_{clean_name}.jpg"

        print("   📥 Fetching Official Zazzle Photorealistic Front Render...")
        cmd = [
            "curl.exe", "-s",
            "-H", "Accept: image/*",
            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            front_render_url,
            "-o", str(local_render_path)
        ]
        subprocess.run(cmd, check=True)
        print(f"   ✅ Zazzle Render Saved: {local_render_path.name} ({local_render_path.stat().st_size/1024:.1f} KB)")

        # -------------------------------------------------------------
        # STEP 2: Embed Zazzle Output into HTML Pin Generator
        # -------------------------------------------------------------
        print("\n🎨 [Step 2/3] Embedding Official Zazzle Render into HTML Pin Generator...")
        pin_title = seo_engine.generate_pin_title(clean_name, niche_key)
        pin_desc = seo_engine.generate_pin_description(niche_key, board_name, account_name)
        alt_text = seo_engine.generate_alt_text(clean_name, niche_key, template_name)

        # Convert Zazzle render to Base64 Data URI for instant, foolproof Playwright rendering
        with open(local_render_path, "rb") as f:
            b64_render = base64.b64encode(f.read()).decode("utf-8")
        render_data_uri = f"data:image/jpeg;base64,{b64_render}"

        timestamp = int(time.time())
        output_pin_path = self.output_dir / f"pin_{niche_key}_{timestamp}.png"

        render_func = getattr(self.engine, f"render_{template_name.replace('-', '_')}", None)
        if not render_func:
            render_func = lambda **kwargs: self.engine._render_single(template_name, **kwargs)

        render_func(
            title=pin_title,
            category=niche_info["category_label"],
            image_url=render_data_uri,
            domain=account_name.upper(),
            palette=palette,
            output_path=output_pin_path
        )
        print(f"   ✅ 1000x1500 Pin Mockup Rendered: {output_pin_path.name} ({output_pin_path.stat().st_size/1024:.1f} KB)")

        # -------------------------------------------------------------
        # STEP 3: Publish Live or Queue for Scheduled Drip
        # -------------------------------------------------------------
        if dry_run:
            print("\n⏸️ [Step 3/3] DRY RUN: Pin generated and ready for scheduling.")
            return {
                "status": "ready_to_schedule",
                "pin_path": str(output_pin_path),
                "title": pin_title,
                "description": pin_desc,
                "alt_text": alt_text,
                "board_id": board_id,
                "board_name": board_name,
                "account": account_name,
                "link": product_url,
                "guid": guid
            }

        print(f"\n📤 [Step 3/3] Publishing Live Pin to Pinterest ({account_name})...")
        token = self.accounts_data.get(account_name, {}).get("access_token")
        if not token:
            token = os.environ.get("PINTEREST_ACCESS_TOKEN")
        if not token:
            raise ValueError(f"No access token for account '{account_name}'")

        with open(output_pin_path, "rb") as f:
            b64_pin = base64.b64encode(f.read()).decode("utf-8")

        p_api = PinterestAPI(token=token)
        res = p_api.create_pin(
            board_id=board_id,
            title=pin_title,
            description=pin_desc,
            link=product_url,
            image_base64=b64_pin,
            alt_text=alt_text
        )

        pin_id = res.get("id")
        pin_url = f"https://www.pinterest.com/pin/{pin_id}/"

        print("=" * 70)
        print("🎉 SUCCESS: OFFICIAL ZAZZLE POD PIN PUBLISHED!")
        print(f"📌 Pin ID       : {pin_id}")
        print(f"🔗 Pin URL      : {pin_url}")
        print(f"🎯 Board        : {board_name}")
        print(f"🛍️ Product Link : {product_url}")
        print("=" * 70)

        return {
            "status": "success",
            "pin_id": pin_id,
            "pin_url": pin_url,
            "board_id": board_id,
            "board_name": board_name,
            "pin_path": str(output_pin_path),
            "zazzle_link": product_url
        }

if __name__ == "__main__":
    pipeline = ZazzlePinterestPipeline()
    # Test on Turkey Time design with the true 3-step engine
    test_cdn = "https://raw.githubusercontent.com/hamouda1/My-t-shirt-designs/main/designs/Turkey%20Time%20Thanksgiving%20Feast%20Funny%20Foodie%20Holiday%20Graphic%20Art.png"
    pipeline.process_design(
        artwork_filename_or_path="Turkey Time Thanksgiving Feast Funny Foodie Holiday Graphic Art.png",
        cdn_url=test_cdn,
        dry_run=False
    )
