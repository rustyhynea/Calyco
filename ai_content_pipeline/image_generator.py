import os
import io
from PIL import Image, ImageDraw, ImageFilter
from .utils import ensure_outputs_dir, write_run_log, seed_from_text, deterministic_choice
from . import prompts

try:
    import openai
except Exception:
    openai = None


def _make_gradient(path, size=(1200, 628), colours=('255,230,230', '220,245,230'), variant='A'):
    """Create a high-quality gradient image with subtle texturing"""
    img = Image.new('RGB', size, color=0)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Base gradient
    for y in range(size[1]):
        t = y / float(size[1])
        r1, g1, b1 = [int(x) for x in colours[0].split(',')]
        r2, g2, b2 = [int(x) for x in colours[1].split(',')]
        r = int(r1 * (1 - t) + r2 * t)
        g = int(g1 * (1 - t) + g2 * t)
        b = int(b1 * (1 - t) + b2 * t)
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    
    # Add subtle vignette for depth
    vignette = Image.new('RGBA', size, (0, 0, 0, 0))
    vignette_draw = ImageDraw.Draw(vignette)
    for y in range(size[1]):
        alpha = int((y / size[1]) * 15) if y < size[1] // 2 else int(((size[1] - y) / size[1]) * 15)
        vignette_draw.line([(0, y), (size[0], y)], fill=(0, 0, 0, alpha))
    
    img = Image.alpha_composite(img.convert('RGBA'), vignette).convert('RGB')
    
    # Subtle blur for softness
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    img.save(path, quality=95)
    return path


def generate_image_variants(seed_text='calyco', out_base='.'):
    out = ensure_outputs_dir(out_base)
    write_run_log(out_base, 'Starting image generation (high-quality variants)')
    variants = {}
    
    # Professional colour palettes inspired by nature and pastels
    palette_variants = {
        'A': {
            'colours': ('245,235,240', '220,245,230'),  # Blush to sage gradient
            'name': 'Blush & Sage',
            'description': 'Warm blush transitioning to cool sage - balanced and sophisticated'
        },
        'B': {
            'colours': ('240,245,250', '230,240,250'),  # Pale blue to lavender
            'name': 'Sky & Lavender',
            'description': 'Serene sky blue with soft lavender undertones - calming and modern'
        }
    }
    
    # try API; if not available, fallback to generated gradients
    for key in ['A', 'B']:
        p = os.path.join(out, f'hero_variant_{key}.png')
        palette = palette_variants[key]
        try:
            # If openai image API available
            if openai and os.environ.get('IMG_API_KEY'):
                openai.api_key = os.environ.get('IMG_API_KEY')
                prompt = prompts.IMAGE_VARIANTS.get(key)
                resp = openai.Image.create(prompt=prompt, size='1200x628')
                b64 = resp['data'][0]['b64_json']
                import base64
                imgdata = base64.b64decode(b64)
                with open(p, 'wb') as f:
                    f.write(imgdata)
                write_run_log(out_base, f'Generated image variant {key} via API')
            else:
                # High-quality gradient fallback
                _make_gradient(p, colours=palette['colours'], variant=key)
                write_run_log(out_base, f'Generated image variant {key} ({palette["name"]}) via gradient')
        except Exception as e:
            write_run_log(out_base, f'Image API error for variant {key}: {e}')
            _make_gradient(p, colours=palette['colours'], variant=key)
        variants[key] = p

    # Deterministic ranking using seed
    chosen = deterministic_choice(seed_text + '-image-rank', ['A', 'B'])
    final_path = os.path.join(out, 'hero.png')
    # copy chosen variant
    from shutil import copyfile
    copyfile(variants[chosen], final_path)

    alt_options = [
        'A modern, sunlit living room featuring soft pastel walls in muted blush and sage green, with natural wood furniture, potted indoor plants, linen textiles, and warm morning light creating a serene, sophisticated atmosphere.',
        'A contemporary urban apartment interior with gentle pastel-coloured walls in soft lavender and cream, showcasing minimalist furniture, geometric artwork, and natural textures that create a calm, refined environment.'
    ]

    meta = {
        'variants': {k: os.path.basename(p) for k, p in variants.items()},
        'chosen': chosen,
        'hero_path': 'outputs/hero.png',
        'alt_texts': alt_options,
        'credit': 'Generated hero image showcasing pastel design concepts',
        'palette_info': {
            'A': palette_variants['A']['description'],
            'B': palette_variants['B']['description']
        }
    }
    with open(os.path.join(out, 'image_metadata.json'), 'w', encoding='utf-8') as f:
        import json
        json.dump(meta, f, ensure_ascii=False, indent=2)
    write_run_log(out_base, f"Saved hero.png (variant {chosen}) and image metadata")
    return meta
