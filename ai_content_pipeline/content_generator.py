import os
import json
import re
from datetime import date
from .utils import ensure_outputs_dir, write_run_log, seed_from_text
from . import prompts

try:
    import openai
except Exception:
    openai = None


def _extract_metadata_block(html):
    """Extract JSON metadata block from HTML comments."""
    patterns = [
        r'<!-- METADATA:(\{.*?\}) -->',
        r'<meta name="article-metadata" content=\'({.*?})\'',
    ]
    for pattern in patterns:
        m = re.search(pattern, html, re.S)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                pass
    return None


def generate_article(trend_summary, competitor_summary, out_base='.', seed_text='calyco', temperature=0.6):
    out = ensure_outputs_dir(out_base)
    write_run_log(out_base, 'Starting article generation')
    prompt = prompts.LONG_ARTICLE_PROMPT.format(
        TREND_SUMMARY='\n'.join(trend_summary), 
        COMPETITOR_SUMMARY='\n'.join(competitor_summary)
    )

    html = None
    used_model = 'FALLBACK'
    title = 'Nature-Inspired Pastels: Transform Your Urban Home in 2025'
    
    try:
        if openai and os.environ.get('OPENAI_API_KEY'):
            openai.api_key = os.environ.get('OPENAI_API_KEY')
            resp = openai.ChatCompletion.create(
                model='gpt-4o-mini',
                messages=[{'role': 'system', 'content': prompt}],
                temperature=temperature,
                max_tokens=1500
            )
            html = resp.choices[0].message.content
            used_model = 'openai'
    except Exception as e:
        write_run_log(out_base, f'OpenAI article error: {e}')

    if not html:
        # Enhanced fallback generation - 700+ word article
        intro = 'The interior design landscape is shifting towards softer, nature-inspired colour palettes in 2025. For urban homeowners and design enthusiasts across India, this trend offers an accessible yet sophisticated approach to modernising living spaces. Pastel walls—muted blush, soft sage, pale cream, and whisper-white tones—are becoming the signature of contemporary minimalist interiors. This comprehensive guide explores how to integrate these trending colours into your home, practical considerations for different rooms, and styling techniques that amplify their visual impact.'
        
        sections = [
            ('The Psychology Behind Pastel Palettes', 
             'Soft pastels work because they reflect natural light and create a sense of calm and spaciousness. Unlike bright, saturated colours that overwhelm small rooms, pastels provide a subtle backdrop allowing other design elements—furniture, artwork, textiles—to shine. The colour psychology is well-established: muted tones reduce visual noise and promote relaxation. For busy urban professionals, creating serene home sanctuaries has become essential. Pastel walls offer remarkable versatility, complementing both modern minimalist and traditional design schemes equally well.'),
            
            ('Selecting the Right Pastel Finish', 
             'The paint finish is equally important as colour choice. Matte finishes provide an elegant, sophisticated look ideal for living rooms and bedrooms, though less forgiving for stains. Eggshell and satin finishes offer subtle sheen, making them perfect for kitchens and bathrooms where durability and cleanability matter. Semi-gloss finishes work exceptionally well on trim and doors. Consider room lighting—north-facing rooms benefit from warmer pastels (blush, peach), whilst south-facing spaces suit cooler tones (sage, grey-blue). Always test chosen colours on a small wall section and observe at different times of day.'),
            
            ('Creating Depth with Accent Walls and Layering', 
             'A single accent wall in a deeper or contrasting pastel shade adds architectural interest without overwhelming. Pair soft sage green with cream or white on adjacent surfaces for subtle depth. For larger spaces, consider two complementary pastels—perhaps pale pink and soft lavender—with white or cream tying the scheme together. Layering textiles—linen curtains, cotton throws, wool rugs in neutral shades—creates visual richness and warmth. This approach ensures your pastel scheme feels cohesive and intentional.'),
            
            ('Styling and Pairing Strategies', 
             'Nature-inspired pastels pair beautifully with natural materials. Wooden furniture in warm oak or light pine, rattan accessories, and live plants create a biophilic design narrative. For accessories, choose muted jewel tones (dusty teal, muted burgundy) or warm metallics (brass, copper) rather than bright primary colours. Artwork and photography in warm, earthy frames ground the space. Textiles should feature natural fabrics—linen, cotton, wool—adding tactile warmth and preventing coldness despite the soft colour palette.'),
            
            ('Room-by-Room Application Guide', 
             'Bedrooms suit cool, muted pastels—soft blue-grey, pale lavender, whisper-white promote better sleep. Living rooms benefit from warm pastels like gentle cream or warm blush paired with accent pillows and rugs. Kitchens should use slightly deeper, more durable finishes in pale yellow or soft green, paired with stainless steel or warm wood cabinetry. Bathrooms suit spa-like pastels: soft eucalyptus green, pale blue, warm ivory combined with natural light and ambient lighting. Home offices work well with focus-enhancing pastels—soft grey or pale blue with good task lighting.')
        ]
        
        bullets = [
            'Test paint swatches by your room\'s primary light source for 24–48 hours before committing',
            'Balance warm and cool pastel tones in adjacent spaces for visual harmony',
            'Layer textiles in neutral and complementary tones to add depth and warmth',
            'Incorporate natural materials—wood, rattan, stone—to ground the palette',
            'Consider the room\'s orientation and natural light when selecting undertones'
        ]
        
        conclusion = 'Adopting nature-inspired pastel palettes is a forward-thinking design choice combining aesthetic appeal with psychological wellbeing. These soft, sophisticated colours transform urban spaces into calm, cohesive sanctuaries without structural changes. Whether refreshing a single room or reimagining your entire home, pastel walls paired with thoughtful styling and natural materials create interiors that feel both contemporary and timeless. Start with one room, observe how colours evolve throughout the day, then expand with confidence. In 2025, the most sophisticated interiors aren\'t the loudest—they\'re the most intentional.'
        
        body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif; line-height: 1.7; color: #2c3e50; background: #fafafa; padding: 40px 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 2.5em; margin-bottom: 20px; color: #1a252f; line-height: 1.2; }}
        h2 {{ font-size: 1.8em; margin-top: 40px; margin-bottom: 20px; color: #34495e; border-left: 4px solid #d4a5a5; padding-left: 15px; }}
        p {{ margin-bottom: 18px; color: #555; }}
        .intro {{ font-size: 1.15em; font-style: italic; color: #666; margin: 30px 0; background: #f9f5f5; padding: 20px; border-radius: 4px; }}
        ul {{ margin: 20px 0 20px 30px; }}
        li {{ margin-bottom: 12px; color: #555; }}
        .hero-section {{ text-align: center; margin: 40px 0; padding: 20px; background: #f5f1f1; border-radius: 4px; color: #999; font-style: italic; }}
        .conclusion {{ margin-top: 40px; padding: 25px; background: linear-gradient(135deg, #f9f5f5 0%, #f5f1f1 100%); border-left: 4px solid #d4a5a5; border-radius: 4px; }}
        .conclusion h2 {{ margin-top: 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p class="intro">{intro}</p>
"""
        
        for heading, content in sections:
            body += f"""        <h2>{heading}</h2>
        <p>{content}</p>
"""
        
        body += """        <h2>Key Takeaways</h2>
        <ul>
"""
        for bullet in bullets:
            body += f"            <li>{bullet}</li>\n"
        body += """        </ul>
        
        <div class="hero-section">
            <!-- HERO_IMAGE_ALT: A sunlit modern living room featuring soft pastel walls in muted blush and sage tones, natural wood furniture, trailing pothos and monstera plants, plush textiles, and diffused morning light creating a calm, sophisticated atmosphere -->
            <p>Hero image will appear here</p>
        </div>
        
        <div class="conclusion">
            <h2>The Bottom Line</h2>
            <p>{conclusion}</p>
        </div>
    </div>
    
    <!-- METADATA:{json.dumps({{'meta_description': 'Complete guide to nature-inspired pastel paint trends 2025. Learn how to choose colours, finishes, and styling for urban Indian homes.', 'tags': ['pastel walls', 'home décor 2025', 'interior design', 'paint trends', 'urban homes'], 'author': 'CALYCO', 'datePublished': str(date.today())}})} -->
</body>
</html>"""
        html = body

    # Save article HTML
    article_html_path = os.path.join(out, 'article.html')
    with open(article_html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Extract metadata
    metadata = _extract_metadata_block(html) or {
        'meta_description': 'Complete guide to nature-inspired pastel paint trends 2025.',
        'tags': ['pastel walls', 'home décor 2025', 'interior design', 'paint trends', 'urban homes'],
        'author': 'CALYCO',
        'datePublished': str(date.today())
    }

    # Calculate word count
    text_only = re.sub(r'<[^>]+>', '', html)
    word_count = len(re.findall(r'\w+', text_only))

    # Create article.json with schema.org markup
    article_json = {
        'title': title,
        'html_path': 'outputs/article.html',
        'word_count': word_count,
        'metadata': metadata,
        'generated_by': used_model,
        'date': str(date.today()),
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': title,
        'author': metadata.get('author', 'CALYCO'),
        'datePublished': metadata.get('datePublished', str(date.today())),
        'description': metadata.get('meta_description'),
        'image': 'https://calyco.example.com/outputs/hero.png'
    }

    with open(os.path.join(out, 'article.json'), 'w', encoding='utf-8') as f:
        json.dump(article_json, f, ensure_ascii=False, indent=2)

    # Generate FAQs with richer content
    faq_items = [
        ('What are the best pastel colours for small bedrooms?', 
         'Soft blue-grey, pale lavender, and whisper-white work beautifully in bedrooms. These cool tones create a calming atmosphere ideal for sleep. Pair with natural wood furniture and linen bedding for cohesion and warmth.'),
        ('How do I prevent pastel walls from looking washed out?', 
         'Layer with contrasting textures and materials. Add depth through styling—wooden furniture, metal accents, plants, and artwork. Use slightly deeper pastel shades on accent walls. Ensure good layered lighting throughout the room.'),
        ('Which pastel finish is best for kitchens and bathrooms?', 
         'Choose satin or eggshell finishes for kitchens and bathrooms for durability and easy cleaning. Matte finishes look beautiful but stain more easily. High-quality, low-VOC formulations offer better longevity and health benefits.'),
        ('Can I combine multiple pastel colours in one space?', 
         'Absolutely. Use a primary pastel on the largest wall and introduce a second complementary pastel as an accent. Keep trim and ceiling white or cream. Tie the scheme with neutral textiles and natural materials.'),
        ('What lighting works best with pastel walls?', 
         'Soft, warm LED lighting flatters pastels beautifully. Avoid cool fluorescents. Incorporate layered lighting—ambient overhead, task lighting, and accent lighting—to create depth. Natural daylight shows pastels at their best.'),
        ('Are pastel colours timeless or just a passing trend?', 
         'Soft, muted colour palettes have endured for centuries in design. Whilst specific trending shades in 2025 may evolve, the principle of calm, nature-inspired interiors transcends trend cycles. Quality materials ensure longevity.')
    ]
    
    faq_html = '<ul style="list-style: none; padding: 0;">'
    for q, a in faq_items:
        faq_html += f'<li style="margin-bottom: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 1em;"><strong style="color: #2c3e50; font-size: 1.05em;">Q: {q}</strong><p style="margin-top: 0.8em; color: #555;">A: {a}</p></li>'
    faq_html += '</ul>'
    
    with open(os.path.join(out, 'faq.json'), 'w', encoding='utf-8') as f:
        json.dump({'faq_html': faq_html, 'count': len(faq_items), 'type': 'html'}, f, ensure_ascii=False, indent=2)

    # Generate social captions with better CTAs
    social = [
        'Transform your urban home with soft pastel walls 🌿 Muted blush, sage green, and pale cream create calm, sophisticated spaces that reflect light beautifully. Learn our complete styling guide now ✨ #InteriorDesign #2025Trends #HomeDecor',
        'Bring nature indoors with nature-inspired pastels 🌱 Perfect for small spaces—these soft tones reflect light and create depth without overwhelming. Discover room-by-room application tips: [link] #DesignInspo #PastelInteriors',
        'The secret to a calm home? Soft pastels + natural materials 🏡 Pair muted colours with wood, rattan, and plants for biophilic design that actually feels inviting. Shop sustainable options: [link] #SustainableDesign #2025'
    ]
    
    with open(os.path.join(out, 'social_captions.txt'), 'w', encoding='utf-8') as f:
        f.write('\n\n---\n\n'.join(social))

    # Generate comprehensive metadata with JSON-LD schema
    metadata_with_schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': title,
        'description': metadata.get('meta_description'),
        'author': {
            '@type': 'Organization',
            'name': 'CALYCO',
            'logo': 'https://calyco.example.com/logo.png'
        },
        'datePublished': metadata.get('datePublished'),
        'dateModified': str(date.today()),
        'image': 'https://calyco.example.com/outputs/hero.png',
        'articleBody': text_only[:500] + '...',
        'wordCount': word_count,
        'keywords': metadata.get('tags', [])
    }
    
    with open(os.path.join(out, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata_with_schema, f, ensure_ascii=False, indent=2)

    write_run_log(out_base, f'Article generated: {word_count} words, title: "{title}"')
    return article_json
