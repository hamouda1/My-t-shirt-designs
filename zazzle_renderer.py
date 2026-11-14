import urllib.parse
import urllib.request
import subprocess
import re
from typing import Optional, Tuple

def get_zazzle_dynamic_render(
    pid: str,
    associate_id: str,
    template_param: str,
    cdn_image_url: str,
    max_dim: int = 1000,
    tracking_code: str = "pin_render"
) -> Tuple[str, str, str]:
    """
    Leverages Zazzle's official Dynamic Creation & RealView Rendering Engine:
      1. Calls Linkover endpoint to register the remote CDN image and obtain internal Image GUID.
      2. Queries Zazzle's official RealView renderer (rlv.zcache.com) for photorealistic output.
    Returns:
      (guid, zazzle_product_url, official_render_image_url)
    """
    encoded_cdn = urllib.parse.quote(cdn_image_url, safe='')
    linkover_url = (
        f"https://www.zazzle.com/api/create/at-{associate_id}?"
        f"rf={associate_id}&"
        f"ax=Linkover&"
        f"pd={pid}&"
        f"ed=true&"
        f"tc={tracking_code}&"
        f"{template_param}={encoded_cdn}"
    )

    # Follow 301 redirect to extract the assigned Zazzle Image GUID
    cmd = [
        "curl.exe", "-s",
        "-o", "NUL",
        "-w", "%{redirect_url}",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        linkover_url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    redirect_url = res.stdout.strip()
    if not redirect_url:
        raise RuntimeError("Zazzle Linkover did not return redirect URL")

    # Extract GUID from redirect
    guid_match = re.search(rf'{template_param}=([a-f0-9\-]+)', redirect_url, re.I)
    if not guid_match:
        # Fallback to any UUID pattern
        guid_match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', redirect_url, re.I)

    if not guid_match:
        raise ValueError(f"Could not extract Zazzle Image GUID from redirect: {redirect_url}")

    guid = guid_match.group(1)

    # Official Zazzle RealView Render URL
    official_render_url = f"https://rlv.zcache.com/svc/view?pid={pid}&max_dim={max_dim}&{template_param}={guid}"

    return guid, redirect_url, official_render_url

if __name__ == "__main__":
    test_cdn = "https://raw.githubusercontent.com/hamouda1/My-t-shirt-designs/main/designs/Turkey%20Time%20Thanksgiving%20Feast%20Funny%20Foodie%20Holiday%20Graphic%20Art.png"
    guid, prod_url, render_url = get_zazzle_dynamic_render(
        pid="256252753051729445",
        associate_id="238209628121657582",
        template_param="t_tshirttemp_iid",
        cdn_image_url=test_cdn
    )
    print("Zazzle GUID:", guid)
    print("Product URL:", prod_url)
    print("Official Render URL:", render_url)
