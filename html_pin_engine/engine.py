"""
HTML/CSS Pin Rendering Engine (Playwright Headless Browser Edition)
==================================================================
Renders high-converting, responsive Pinterest pins (1000x1500) using
HTML5, CSS3 Grid/Flexbox, and Google Web Fonts via headless Edge/Chromium.

Now featuring 10 distinct template architectures:
 1. arch-editorial           (Luxury Frame Editorial)
 2. minimal-ui               (Clean Modern Storefront Card)
 3. dynamic-overlap          (Stage Banner with Layer Overlap)
 4. spotlight-1plus3         (1 Hero + 3 Sub-Cards Roundup)
 5. collage-quad             (2x2 Grid Quad Collage)
 6. streetwear-polaroid      (Vintage Polaroid & Washi Tape)
 7. split-detail-zoom        (Split Screen: Full Shirt + Print Detail)
 8. dark-noir-streetwear     (Cyber Dark Mode Brutalist Streetwear)
 9. outfit-inspo-guide       (How To Style & Outfit Moodboard)
 10. color-variants-swatches (Multi-Color Swatches Retail Card)
"""

import os
import sys
import json
import base64
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ENGINE_DIR = Path(__file__).parent
TEMPLATES_DIR = ENGINE_DIR / "templates"

# 6 High-Converting Aesthetic Palettes
PALETTES = {
    "terracotta": {"bg": "#F4EFEA", "accent": "#C84B31", "name": "Sand Beige & Terracotta"},
    "navy":       {"bg": "#EEF2F5", "accent": "#1B3B6F", "name": "Ice Grey & Royal Navy"},
    "emerald":    {"bg": "#F1F5F2", "accent": "#2D6A4F", "name": "Fog Green & Emerald"},
    "burgundy":   {"bg": "#F6F0F4", "accent": "#6D2E46", "name": "Dusty Rose & Burgundy"},
    "amber":      {"bg": "#FDF6EC", "accent": "#D97706", "name": "Warm Cream & Amber"},
    "slate":      {"bg": "#EEF1F4", "accent": "#1E293B", "name": "Minimal Slate Noir"}
}

DEFAULT_PALETTE_LIST = list(PALETTES.values())

class HTMLPinEngine:
    def __init__(self, browser_channel="msedge"):
        self.browser_channel = browser_channel
        self.templates = {}
        self._load_templates()

    def _load_templates(self):
        for tpl_file in TEMPLATES_DIR.glob("*.html"):
            with open(tpl_file, "r", encoding="utf-8") as f:
                self.templates[tpl_file.stem] = f.read()

    def _get_browser(self, p):
        try:
            return p.chromium.launch(headless=True, channel=self.browser_channel)
        except Exception:
            try:
                return p.chromium.launch(headless=True, channel="chrome")
            except Exception:
                return p.chromium.launch(headless=True)

    def render_html_to_png(self, html_content, output_path=None, as_base64=False, wait_ms=2000):
        """Renders raw HTML string to PNG bytes, file, or Base64."""
        with sync_playwright() as p:
            browser = self._get_browser(p)
            try:
                page = browser.new_page(viewport={"width": 1000, "height": 1500}, device_scale_factor=1)
                page.set_content(html_content, wait_until="domcontentloaded")
                if wait_ms > 0:
                    page.wait_for_timeout(wait_ms)

                if output_path:
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    png_bytes = page.screenshot(path=str(output_path))
                else:
                    png_bytes = page.screenshot()

                if as_base64:
                    return base64.b64encode(png_bytes).decode("utf-8")
                return png_bytes
            finally:
                browser.close()

    def _render_single(self, template_key, title, category, image_url, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        pal = palette or PALETTES["terracotta"]
        tpl = self.templates.get(template_key)
        if not tpl:
            raise FileNotFoundError(f"Template '{template_key}.html' not found in templates directory")

        html = tpl
        html = html.replace("{{BG_COLOR}}", pal["bg"])
        html = html.replace("{{ACCENT_COLOR}}", pal["accent"])
        html = html.replace("{{CATEGORY}}", category)
        html = html.replace("{{TITLE}}", title)
        html = html.replace("{{IMAGE_URL}}", image_url)
        html = html.replace("{{DOMAIN_NAME}}", domain)

        return self.render_html_to_png(html, output_path=output_path, as_base64=as_base64)

    # Core Templates
    def render_arch_editorial(self, title, category, image_url, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        return self._render_single("arch-editorial", title, category, image_url, domain, palette, output_path, as_base64)

    def render_minimal_ui(self, title, category, image_url, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        return self._render_single("minimal-ui", title, category, image_url, domain, palette, output_path, as_base64)

    def render_dynamic_overlap(self, title, category, image_url, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        return self._render_single("dynamic-overlap", title, category, image_url, domain, palette, output_path, as_base64)

    # New Specialized T-Shirt & Apparel Templates
    def render_streetwear_polaroid(self, title, category, image_url, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        return self._render_single("streetwear-polaroid", title, category, image_url, domain, palette, output_path, as_base64)

    def render_split_detail_zoom(self, title, category, image_url, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        return self._render_single("split-detail-zoom", title, category, image_url, domain, palette, output_path, as_base64)

    def render_dark_noir_streetwear(self, title, category, image_url, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        return self._render_single("dark-noir-streetwear", title, category, image_url, domain, palette, output_path, as_base64)

    def render_outfit_inspo_guide(self, title, category, image_url, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        return self._render_single("outfit-inspo-guide", title, category, image_url, domain, palette, output_path, as_base64)

    def render_color_variants_swatches(self, title, category, image_url, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        return self._render_single("color-variants-swatches", title, category, image_url, domain, palette, output_path, as_base64)

    # Multi-Item Collage Templates
    def render_spotlight_1plus3(self, collection_title, category, hero_image, sub_images, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        pal = palette or PALETTES["slate"]
        tpl = self.templates.get("spotlight-1plus3")
        if not tpl:
            raise FileNotFoundError("spotlight-1plus3.html template not found")

        sub1 = sub_images[0] if len(sub_images) > 0 else hero_image
        sub2 = sub_images[1] if len(sub_images) > 1 else sub1
        sub3 = sub_images[2] if len(sub_images) > 2 else sub2

        html = tpl
        html = html.replace("{{BG_COLOR}}", pal["bg"])
        html = html.replace("{{ACCENT_COLOR}}", pal["accent"])
        html = html.replace("{{CATEGORY}}", category)
        html = html.replace("{{COLLECTION_TITLE}}", collection_title)
        html = html.replace("{{IMAGE_1}}", hero_image)
        html = html.replace("{{IMAGE_2}}", sub1)
        html = html.replace("{{IMAGE_3}}", sub2)
        html = html.replace("{{IMAGE_4}}", sub3)
        html = html.replace("{{DOMAIN_NAME}}", domain)

        return self.render_html_to_png(html, output_path=output_path, as_base64=as_base64)

    def render_collage_quad(self, collection_title, category, images, domain="MARRYTREASURES", palette=None, output_path=None, as_base64=False):
        pal = palette or PALETTES["emerald"]
        tpl = self.templates.get("collage-quad")
        if not tpl:
            raise FileNotFoundError("collage-quad.html template not found")

        img1 = images[0] if len(images) > 0 else ""
        img2 = images[1] if len(images) > 1 else img1
        img3 = images[2] if len(images) > 2 else img2
        img4 = images[3] if len(images) > 3 else img3

        html = tpl
        html = html.replace("{{BG_COLOR}}", pal["bg"])
        html = html.replace("{{ACCENT_COLOR}}", pal["accent"])
        html = html.replace("{{CATEGORY}}", category)
        html = html.replace("{{COLLECTION_TITLE}}", collection_title)
        html = html.replace("{{IMAGE_1}}", img1)
        html = html.replace("{{IMAGE_2}}", img2)
        html = html.replace("{{IMAGE_3}}", img3)
        html = html.replace("{{IMAGE_4}}", img4)
        html = html.replace("{{DOMAIN_NAME}}", domain)

        return self.render_html_to_png(html, output_path=output_path, as_base64=as_base64)

    def render_batch(self, items, output_dir):
        """Fast batch rendering of all template types using a single browser instance."""
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        results = []

        with sync_playwright() as p:
            browser = self._get_browser(p)
            try:
                page = browser.new_page(viewport={"width": 1000, "height": 1500}, device_scale_factor=1)
                for item in items:
                    tpl_type = item.get("type", "minimal-ui")
                    filename = item.get("filename", f"pin_{int(time.time()*1000)}.png")
                    out_path = out_dir / filename
                    
                    pal = item.get("palette") or PALETTES.get(item.get("palette_name", "terracotta"), PALETTES["terracotta"])
                    
                    tpl = self.templates.get(tpl_type)
                    if not tpl:
                        print(f"  [!] Skipped unknown template: {tpl_type}")
                        continue
                        
                    html = tpl
                    html = html.replace("{{BG_COLOR}}", pal["bg"]).replace("{{ACCENT_COLOR}}", pal["accent"])
                    html = html.replace("{{CATEGORY}}", item.get("category", "Graphic Tees"))
                    html = html.replace("{{DOMAIN_NAME}}", item.get("domain", "MARRYTREASURES"))
                    
                    if "collage" in tpl_type or "spotlight" in tpl_type:
                        html = html.replace("{{COLLECTION_TITLE}}", item.get("title", ""))
                        imgs = item.get("images", [item.get("image_url", "")] * 4)
                        for i in range(4):
                            u = imgs[i] if i < len(imgs) else imgs[0]
                            html = html.replace(f"{{{{IMAGE_{i+1}}}}}", u)
                    else:
                        html = html.replace("{{TITLE}}", item.get("title", ""))
                        html = html.replace("{{IMAGE_URL}}", item.get("image_url", ""))

                    page.set_content(html, wait_until="domcontentloaded")
                    page.wait_for_timeout(2000)
                    page.screenshot(path=str(out_path))
                    results.append(str(out_path))
                    print(f"  [+] Rendered ({tpl_type}): {filename}", flush=True)
            finally:
                browser.close()

        return results
