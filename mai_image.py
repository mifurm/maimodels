"""Generate a small marketing image campaign with MAI-Image-2.6."""

import argparse
import base64
import binascii
import os
from pathlib import Path
from typing import TypedDict

import requests
from dotenv import load_dotenv


class MarketingSample(TypedDict):
    name: str
    width: int
    height: int
    prompt: str


def banana_card_sample(name: str, art_direction: str) -> MarketingSample:
    return {
        "name": name,
        "width": 1536,
        "height": 1024,
        "prompt": (
            "Front-facing premium credit card concept for the fictional lifestyle brand "
            "BANANA. Make an original banana illustration the unmistakable centerpiece "
            f"of the card using this art direction: {art_direction} "
            "Integrate a realistic embedded chip and contactless symbol into the design. "
            "Professional studio product photography, crisp card edges, controlled "
            "reflections, and a complementary presentation background. Show only "
            'intentionally nonfunctional display details: brand name "BANANA", '
            'cardholder "JAMIE SUN", and masked number "••••  ••••  ••••  8080". '
            "No bank name, no payment-network logo, no expiration date, no security "
            "code, no real company branding, no watermark. Landscape composition, "
            "polished commercial advertising quality."
        ),
    }


SAMPLES: tuple[MarketingSample, ...] = (
    {
        "name": "product-launch",
        "width": 1536,
        "height": 1024,
        "prompt": (
            "Premium commercial campaign hero image for a fictional wireless speaker "
            "called AURA. A sculptural matte-black speaker floats above a mirror-like "
            "surface, surrounded by translucent amber sound waves and subtle mist. "
            "Dramatic warm rim lighting, deep charcoal background, realistic materials, "
            "luxury product photography, clean negative space on the left. Include only "
            'the crisp, correctly spelled headline "FEEL EVERY DETAIL" and a small '
            '"AURA" wordmark. Landscape composition, polished global brand advertising, '
            "no other text, no logos, no watermark."
        ),
    },
    {
        "name": "skincare-social",
        "width": 1024,
        "height": 1024,
        "prompt": (
            "High-end social media advertisement for a fictional skincare serum named "
            "LUMENA. Frosted glass bottle with pearlescent serum on pale travertine, "
            "surrounded by water droplets, white camellias, and soft cream fabric. "
            "Morning sunlight creates elegant caustics and delicate shadows. "
            "Photorealistic macro product photography, fresh ivory and sage palette. "
            'The bottle label reads exactly "LUMENA" and "RADIANCE SERUM". Balanced '
            "square composition, premium editorial art direction, no other text, "
            "no watermark."
        ),
    },
    {
        "name": "city-poster",
        "width": 1024,
        "height": 1536,
        "prompt": (
            "Vertical tourism campaign poster for the fictional coastal city of Solara. "
            "A stylish diverse group of adult friends walks through a sunlit modern "
            "waterfront market, with colorful architecture, palms, ocean reflections, "
            "and cinematic golden-hour atmosphere. Authentic candid expressions, "
            "photorealistic editorial travel photography, vibrant coral and turquoise "
            "color grade. Add an elegant poster headline at the top reading exactly "
            '"FIND YOUR SUNSHINE" and a smaller line "SOLARA AWAITS". Sophisticated '
            "layout with excellent text legibility, no other text, no logos, no watermark."
        ),
    },
    {
        "name": "tech-credit-card",
        "width": 1536,
        "height": 1024,
        "prompt": (
            "Front-facing premium credit card concept for a fictional technology brand "
            "named NOVA. The card features an original flowing ribbon emblem, an "
            "ethereal aurora landscape in deep blue, violet, and cyan, subtle metallic "
            "foil details, a realistic contactless symbol, and an embedded chip. "
            "Studio product photography with soft reflections, dramatic edge lighting, "
            "and a clean dark gradient background. Show only intentionally nonfunctional "
            'display details: the brand name "NOVA", cardholder "ALEX MORGAN", and '
            'masked number "••••  ••••  ••••  2048". No bank name, no payment-network '
            "logo, no expiration date, no security code, no real company branding, "
            "no watermark. Landscape composition, polished global advertising quality."
        ),
    },
    {
        "name": "banana-credit-card",
        "width": 1536,
        "height": 1024,
        "prompt": (
            "Front-facing premium credit card concept for a fictional lifestyle brand "
            "named BANANA. A tasteful original golden banana emblem is embossed near "
            "the upper-left corner. The card artwork shows layered tropical leaves, "
            "sunlit yellow gradients, subtle pearl texture, and refined black accents. "
            "Include a realistic embedded chip and contactless symbol. Luxury studio "
            "product photography, soft shadows, precise reflections, dark neutral "
            "background, and dramatic edge lighting. Show only intentionally "
            'nonfunctional display details: the brand name "BANANA", cardholder '
            '"JAMIE SUN", and masked number "••••  ••••  ••••  8080". No bank name, '
            "no payment-network logo, no expiration date, no security code, no real "
            "company branding, no watermark. Landscape composition, highly polished "
            "commercial advertising quality."
        ),
    },
    banana_card_sample(
        "banana-card-elegant",
        (
            "An elegant single banana drawn with delicate champagne-gold linework on "
            "warm ivory enamel, surrounded by restrained embossed botanical curves, "
            "small pearl highlights, and generous negative space."
        ),
    ),
    banana_card_sample(
        "banana-card-rock",
        (
            "An energetic banana formed from torn concert-poster textures, black ink "
            "strokes, electric yellow paint, subtle chrome studs, and dramatic red "
            "accents on a distressed charcoal surface."
        ),
    ),
    banana_card_sample(
        "banana-card-modern",
        (
            "A modern geometric banana assembled from smooth cobalt, yellow, and white "
            "shapes, with a precise grid, bold color blocking, clean typography, and "
            "a satin architectural finish."
        ),
    ),
    banana_card_sample(
        "banana-card-minimal",
        (
            "A tiny sculptural banana icon debossed into a monochrome butter-yellow "
            "surface, with soft-touch material, nearly invisible tonal gradients, "
            "ultrathin details, and abundant quiet space."
        ),
    ),
    banana_card_sample(
        "banana-card-art-deco",
        (
            "A symmetrical fan-shaped banana motif in polished gold and black lacquer, "
            "framed by stepped arches, sunburst geometry, emerald enamel accents, and "
            "luxurious 1920s-inspired ornament."
        ),
    ),
    banana_card_sample(
        "banana-card-cyber",
        (
            "A luminous holographic banana built from cyan and magenta light trails, "
            "floating above a deep midnight circuit pattern with iridescent foil, "
            "glass-like layers, and sleek futuristic depth."
        ),
    ),
    banana_card_sample(
        "banana-card-watercolor",
        (
            "A joyful hand-painted banana in expressive yellow watercolor washes, with "
            "visible paper grain, loose green leaves, soft pigment blooms, and tasteful "
            "splashes across a clean porcelain-white card."
        ),
    ),
    banana_card_sample(
        "banana-card-tropical",
        (
            "A richly detailed ripe banana among lush monstera leaves, hibiscus petals, "
            "and warm sunset rays, using vivid emerald, coral, and golden colors with "
            "layered photographic depth."
        ),
    ),
    banana_card_sample(
        "banana-card-luxury",
        (
            "A three-dimensional banana jewel sculpted from brushed 24-karat-gold-like "
            "metal and dark onyx, set against deep forest-green leather with precise "
            "foil borders and subtle gemstone highlights."
        ),
    ),
    banana_card_sample(
        "banana-card-pop",
        (
            "A playful oversized banana illustration with original bold comic shapes, "
            "halftone dots, punchy yellow, hot pink, and turquoise blocks, energetic "
            "motion lines, and upbeat contemporary pop graphics."
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate polished marketing images with MAI-Image-2.6."
    )
    parser.add_argument(
        "--sample",
        choices=("all", "banana-collection", *(sample["name"] for sample in SAMPLES)),
        default="all",
        help=(
            "Generate one concept, all banana cards, or the complete campaign "
            "(default: all)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("generated/mai-image-2.6"),
        help="Directory for generated PNG files.",
    )
    parser.add_argument(
        "--web-grounding",
        action="store_true",
        help="Let MAI-Image-2.6 use Bing context for current real-world details.",
    )
    return parser.parse_args()


def require_environment(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} must be set in the .env file.")
    return value


def generation_url(endpoint: str) -> str:
    endpoint = endpoint.rstrip("/")
    generation_path = "/mai/v1/images/generations"
    if endpoint.endswith(generation_path):
        return endpoint
    return f"{endpoint}{generation_path}"


def generate_image(
    *,
    endpoint: str,
    api_key: str,
    deployment_name: str,
    sample: MarketingSample,
    web_grounding: bool,
) -> bytes:
    response = requests.post(
        generation_url(endpoint),
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,
        },
        json={
            "model": deployment_name,
            "prompt": sample["prompt"],
            "width": sample["width"],
            "height": sample["height"],
            "web_grounding": web_grounding,
        },
        timeout=300,
    )
    response.raise_for_status()

    result = response.json()
    data = result.get("data")
    if not isinstance(data, list) or not data:
        raise RuntimeError("MAI Image returned no generated image data.")

    first_image = data[0]
    if not isinstance(first_image, dict):
        raise RuntimeError("MAI Image returned an unexpected image result.")

    encoded_image = first_image.get("b64_json")
    if not isinstance(encoded_image, str):
        raise RuntimeError("MAI Image response is missing data[0].b64_json.")

    try:
        return base64.b64decode(encoded_image, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise RuntimeError("MAI Image returned invalid base64 image data.") from exc


def main() -> None:
    load_dotenv()
    args = parse_args()

    endpoint = require_environment("AZURE_MAI_IMAGE_ENDPOINT")
    api_key = require_environment("AZURE_MAI_IMAGE_API_KEY")
    deployment_name = require_environment("AZURE_MAI_IMAGE_DEPLOYMENT")

    if args.sample == "all":
        selected_samples = SAMPLES
    elif args.sample == "banana-collection":
        selected_samples = tuple(
            sample for sample in SAMPLES if sample["name"].startswith("banana-")
        )
    else:
        selected_samples = tuple(
            sample for sample in SAMPLES if sample["name"] == args.sample
        )
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for sample in selected_samples:
        print(
            f"Generating {sample['name']} "
            f"({sample['width']}x{sample['height']})..."
        )
        image = generate_image(
            endpoint=endpoint,
            api_key=api_key,
            deployment_name=deployment_name,
            sample=sample,
            web_grounding=args.web_grounding,
        )
        output_path = args.output_dir / f"{sample['name']}.png"
        output_path.write_bytes(image)
        print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
