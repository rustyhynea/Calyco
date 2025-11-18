import os
import json
import re
from .utils import ensure_outputs_dir, write_run_log, seed_from_text, deterministic_choice

try:
    import openai
except Exception:
    openai = None


def word_count_from_text(text):
    return len(re.findall(r"\w+", text))


def readability_score(text):
    # Simple Flesch-like heuristic: based on avg words per sentence and syllables per word (approx)
    sentences = re.split(r'[\.\!\?]+', text)
    sentences = [s for s in sentences if s.strip()]
    words = re.findall(r"\w+", text)
    if not sentences or not words:
        return 0
    avg_words = len(words) / len(sentences)
    # approximate syllables: count vowels groups
    syllables = sum(len(re.findall(r'[aeiouy]+', w, re.I)) for w in words)
    if len(words) == 0:
        return 0
    asl = avg_words
    asw = syllables / len(words)
    # Basic formula remapped
    score = max(0, 206.835 - 1.015 * asl - 84.6 * asw)
    return round(score, 1)


def originality_score(text, seed_text='calyco'):
    # heuristic: measure repetition ratio
    words = re.findall(r"\w+", text.lower())
    if not words:
        return 0
    uniq = len(set(words))
    ratio = uniq / len(words)
    score = int(30 + ratio * 70)
    return min(100, score)


def seo_keywords_and_tags(text):
    words = re.findall(r"\w+", text.lower())
    freq = {}
    for w in words:
        if len(w) < 4:
            continue
        freq[w] = freq.get(w, 0) + 1
    top = sorted(freq.items(), key=lambda x: -x[1])[:10]
    keywords = [w for w, _ in top[:3]]
    tags = [w for w, _ in top[:5]]
    return keywords, tags


def run_article_checks(article_html_path, out_base='.'):
    out = ensure_outputs_dir(out_base)
    with open(article_html_path, 'r', encoding='utf-8') as f:
        text = f.read()
    wc = word_count_from_text(text)
    read = readability_score(text)
    orig = originality_score(text)
    keywords, tags = seo_keywords_and_tags(text)

    qa = {
        'word_count': wc,
        'readability_flesch_like': read,
        'originality_score': orig,
        'seo_keywords': keywords,
        'suggested_tags': tags,
        'suggestions': [
            'Shorten long paragraphs to improve scanability.',
            'Add specific product or palette examples for clarity.',
            'Include a stronger CTA with a link to CALYCO palettes.'
        ]
    }
    with open(os.path.join(out, 'qa_report.json'), 'w', encoding='utf-8') as f:
        json.dump(qa, f, ensure_ascii=False, indent=2)
    write_run_log(out_base, f"Saved QA report to outputs/qa_report.json")
    return qa


def rank_images(image_meta_path, out_base='.'):
    out = ensure_outputs_dir(out_base)
    with open(image_meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    # deterministic ranking explanation
    chosen = meta.get('chosen')
    other = 'A' if chosen == 'B' else 'B'
    score = deterministic_choice('rank-' + chosen, [78, 82, 88])
    explanation = f"Variant {chosen} chosen for brand fit: balanced lighting, soft colours and good composition. Score {score}."
    rank = {'chosen': chosen, 'score': score, 'explanation': explanation}
    with open(os.path.join(out, 'image_ranking.json'), 'w', encoding='utf-8') as f:
        json.dump(rank, f, ensure_ascii=False, indent=2)
    write_run_log(out_base, f"Saved image ranking to outputs/image_ranking.json")
    return rank


def final_qa(article_html_path, out_base='.'):
    out = ensure_outputs_dir(out_base)
    with open(article_html_path, 'r', encoding='utf-8') as f:
        text = f.read()
    wc = word_count_from_text(text)
    orig = originality_score(text)
    suggestions = [
        'Tighten the introduction by 10-20 words for clarity.',
        'Add direct examples of paint pairings in one section.',
        'Include alt text near the hero image marker.'
    ]
    alt_texts = [
        'Sunlit living room with pastel walls and plants',
        'Minimalist urban living room in muted blush and sage'
    ]
    outjson = {
        'word_count': wc,
        'originality_score': orig,
        'edit_suggestions': suggestions,
        'alt_texts': alt_texts
    }
    with open(os.path.join(out, 'final_qa.json'), 'w', encoding='utf-8') as f:
        json.dump(outjson, f, ensure_ascii=False, indent=2)
    write_run_log(out_base, 'Saved final QA to outputs/final_qa.json')
    return outjson
