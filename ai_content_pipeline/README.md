# CALYCO — Fully Automated AI Content Engine

**Build intelligent, high-quality content at scale with zero manual intervention.**

CALYCO is a production-ready, end-to-end AI content pipeline that automates the entire process: trend research → article writing → image generation → quality assurance → export. Perfect for content teams, agencies, and brands looking to streamline their editorial workflow.

## 🎯 Key Features

- ✅ **Single-Command Execution** – `python main.py` runs the complete pipeline end-to-end
- ✅ **Interactive CLI Menu** – Full control with options to run parts, regenerate, preview, and export
- ✅ **High-Quality Image Generation** – Professional pastel gradient variants with automatic selection
- ✅ **AI-Powered Content** – OpenAI integration with intelligent fallbacks (no API keys required)
- ✅ **Comprehensive QA** – Readability scoring, originality detection, image ranking
- ✅ **Web Preview** – Beautiful Flask interface at `http://localhost:8000`
- ✅ **Production Outputs** – 13+ files including HTML, JSON, schema.org markup, FAQs, social captions

## 📋 Prerequisites

- **Python 3.10+** (tested on 3.12)
- **pip** (Python package manager)
- Optional: **OPENAI_API_KEY** (for advanced text generation; fallbacks work perfectly without it)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd /workspaces/Calyco

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r ai_content_pipeline/requirements.txt
```

### 2. Run Full Pipeline (Single Command)

```bash
cd /workspaces/Calyco
python -m ai_content_pipeline.main
```

This generates:
- ✓ Trend analysis (pytrends)
- ✓ Competitor research (feedparser)
- ✓ 700+ word article (HTML + JSON)
- ✓ FAQ with 6 Q&A pairs
- ✓ 3 social media captions
- ✓ Hero image (2 variants, auto-selected)
- ✓ Metadata with JSON-LD schema
- ✓ QA reports (readability, originality, keywords)

---

## 🎮 Interactive CLI Menu

For granular control, use the menu-driven interface:

```bash
python -m ai_content_pipeline.main --menu
```

**Options:**
```
1) Run full pipeline (data → content → image → QA)
2) Run data collection only
3) Regenerate article content
4) Regenerate image variants
5) Preview outputs
6) Start web preview server (Flask)
7) Export ZIP for submission
0) Exit
```

---

## 🌐 Web Preview (Flask)

Start the interactive web interface:

```bash
export FLASK_APP=ai_content_pipeline.app
flask run --port=8000
```

Or select option 6 from the CLI menu.

---

## 📂 Output Files

All generated content is saved to `ai_content_pipeline/outputs/`:

```
outputs/
├── article.json          # Article metadata with schema.org markup
├── article.html          # Styled, ready-to-publish HTML
├── faq.json              # 6 Q&A pairs in HTML format
├── social_captions.txt   # 3 Instagram-ready captions with CTAs
├── hero.png              # Selected hero image (1200×628px)
├── hero_variant_A.png    # Blush & Sage variant
├── hero_variant_B.png    # Sky & Lavender variant
├── metadata.json         # SEO metadata + JSON-LD schema
├── image_metadata.json   # Image details and alt-text options
├── image_ranking.json    # Image selection reasoning
├── qa_report.json        # Readability, originality, SEO keywords
├── final_qa.json         # Final quality assurance summary
├── trend_summary.json    # Trend analysis data
├── competitor_feeds.json # Competitor research
└── run_log.txt           # Complete pipeline execution log
```

---

## 🔧 Configuration

### API Keys (Optional)

Copy `.env.example` to `.env` and fill in API keys:

```bash
cp ai_content_pipeline/.env.example .env
```

Without API keys, the pipeline runs perfectly in DEMO-FALLBACK mode with deterministic generation.

---

## 📹 Demo Video Script (2–4 Minutes)

```
[INTRO - 10s]
"Hi! This is the CALYCO AI Content Pipeline—a fully automated system 
that generates professional articles, images, and metadata in seconds."

[RUN PIPELINE - 40s]
Execute: python -m ai_content_pipeline.main
Show: Real-time logs as each step completes

[PREVIEW OUTPUTS - 30s]
Show: Generated article.html and hero.png

[WEB PREVIEW - 30s]
Open: http://localhost:8000
Show: Flask interface with complete outputs

[EXPORT & FINISH - 15s]
Show: ZIP export and summary
```

---

## 🔐 Fallback Behavior

If API keys are missing, the pipeline uses deterministic generation:
- ✓ Professional 700+ word articles from templates
- ✓ High-quality Pillow gradient images
- ✓ All outputs marked as DEMO-FALLBACK in metadata

---

## 📦 Dependencies

```
flask>=2.0, requests>=2.0, beautifulsoup4>=4.9
feedparser>=6.0, pytrends>=4.8, openai>=0.27, Pillow>=9.0
```

---

## 🚀 Next Steps

1. Run: `python -m ai_content_pipeline.main`
2. Preview: `python -m ai_content_pipeline.main --menu`
3. View web: `flask run --port=8000`
4. Export: Select option 7 from menu

**Ready? Run:** `python -m ai_content_pipeline.main`

