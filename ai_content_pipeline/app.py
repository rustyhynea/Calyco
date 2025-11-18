from flask import Flask, send_from_directory, render_template_string, jsonify
import os
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / 'outputs'
app = Flask(__name__)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CALYCO Preview</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f9f5f5 0%, #f5f1f1 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-radius: 8px;
            margin-bottom: 40px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .section {
            background: white;
            padding: 40px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #d4a5a5;
        }
        .hero-image {
            width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .article-content {
            color: #555;
            line-height: 1.8;
        }
        .article-content h3 {
            color: #34495e;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        .article-content p {
            margin-bottom: 15px;
        }
        .metadata {
            background: #f5f1f1;
            padding: 20px;
            border-radius: 4px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat {
            background: linear-gradient(135deg, #e8d4d4 0%, #f5e5e5 100%);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #d4a5a5;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .files-list {
            list-style: none;
            padding: 0;
        }
        .files-list li {
            padding: 10px;
            background: #f9f5f5;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 4px solid #d4a5a5;
        }
        .files-list li:before {
            content: "📁 ";
            margin-right: 8px;
        }
        .footer {
            text-align: center;
            padding: 30px 20px;
            color: #999;
            font-size: 0.9em;
        }
        .footer a {
            color: #d4a5a5;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 CALYCO Content Preview</h1>
        <p>AI-Generated Interior Design Article & Visuals</p>
    </div>
    
    <div class="container">
        <!-- Article Section -->
        <div class="section">
            <h2>📄 Generated Article</h2>
            {% if article %}
                <div class="article-content">
                    {{ article|safe }}
                </div>
            {% else %}
                <p style="color: #999;">No article generated yet. Run the pipeline first.</p>
            {% endif %}
        </div>
        
        <!-- Hero Image Section -->
        {% if hero_exists %}
        <div class="section">
            <h2>🖼️ Hero Image</h2>
            <img src="/hero.png" alt="Generated hero image" class="hero-image">
            <p style="color: #999; font-size: 0.9em; text-align: center;">
                A sunlit modern living room featuring soft pastel walls and natural design elements
            </p>
        </div>
        {% endif %}
        
        <!-- Statistics -->
        {% if stats %}
        <div class="section">
            <h2>📊 Content Statistics</h2>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{{ stats.word_count }}</div>
                    <div class="stat-label">Words</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{{ stats.readability|round(1) }}</div>
                    <div class="stat-label">Readability Score</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{{ stats.originality }}</div>
                    <div class="stat-label">Originality %</div>
                </div>
            </div>
        </div>
        {% endif %}
        
        <!-- Metadata -->
        {% if metadata %}
        <div class="section">
            <h2>📋 Metadata & Schema</h2>
            <div class="metadata">
                {{ metadata_json|safe }}
            </div>
        </div>
        {% endif %}
        
        <!-- Generated Files -->
        <div class="section">
            <h2>📁 Generated Output Files</h2>
            <ul class="files-list">
                {% for file in files %}
                <li>{{ file }}</li>
                {% endfor %}
            </ul>
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by CALYCO AI Content Pipeline | 
        <a href="https://github.com/rustyhynea/calyco" target="_blank">View on GitHub</a></p>
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    """Main preview page with article and metadata"""
    article_path = OUT / 'article.html'
    hero_exists = (OUT / 'hero.png').exists()
    
    article_html = ""
    metadata = None
    metadata_json = ""
    stats = {}
    files = []
    
    try:
        if article_path.exists():
            full_html = article_path.read_text(encoding='utf-8')
            # Extract body content
            import re
            match = re.search(r'<body[^>]*>(.*?)</body>', full_html, re.S)
            if match:
                article_html = match.group(1)
        
        md_path = OUT / 'metadata.json'
        if md_path.exists():
            metadata = json.load(open(md_path, 'r', encoding='utf-8'))
            metadata_json = f"<pre>{json.dumps(metadata, ensure_ascii=False, indent=2)}</pre>"
        
        qa_path = OUT / 'qa_report.json'
        if qa_path.exists():
            stats = json.load(open(qa_path, 'r', encoding='utf-8'))
        
        files = sorted([p.name for p in OUT.iterdir() if p.is_file()])
    except Exception as e:
        pass
    
    return render_template_string(
        HTML_TEMPLATE,
        article=article_html,
        hero_exists=hero_exists,
        stats=stats,
        metadata=metadata,
        metadata_json=metadata_json,
        files=files
    )


@app.route('/hero.png')
def hero():
    """Serve hero image"""
    try:
        return send_from_directory(OUT, 'hero.png')
    except Exception:
        return "Hero image not found", 404


@app.route('/outputs/<path:filename>')
def outputs(filename):
    """Serve files from outputs directory"""
    try:
        return send_from_directory(OUT, filename)
    except Exception:
        return "File not found", 404


@app.route('/api/metadata')
def api_metadata():
    """API endpoint for metadata"""
    try:
        md_path = OUT / 'metadata.json'
        if md_path.exists():
            return jsonify(json.load(open(md_path, 'r', encoding='utf-8')))
    except Exception:
        pass
    return jsonify({})


@app.route('/api/article')
def api_article():
    """API endpoint for article data"""
    try:
        art_path = OUT / 'article.json'
        if art_path.exists():
            return jsonify(json.load(open(art_path, 'r', encoding='utf-8')))
    except Exception:
        pass
    return jsonify({})


@app.route('/api/stats')
def api_stats():
    """API endpoint for QA statistics"""
    try:
        qa_path = OUT / 'qa_report.json'
        if qa_path.exists():
            return jsonify(json.load(open(qa_path, 'r', encoding='utf-8')))
    except Exception:
        pass
    return jsonify({})


if __name__ == '__main__':
    app.run(port=8000, debug=False)
