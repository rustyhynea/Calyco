#!/usr/bin/env python3
"""
CALYCO AI Content Pipeline Orchestrator
Fully automated end-to-end content generation with interactive CLI
"""
import os
import sys
import time
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / 'outputs'

from .utils import write_run_log


# Terminal colors for better UI
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_section(text):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{text}{Colors.ENDC}")


def print_welcome():
    print(f"""{Colors.BOLD}{Colors.CYAN}
╔════════════════════════════════════════════════════════╗
║                                                        ║
║        CALYCO — AI Content Pipeline Demo               ║
║        Fully Automated End-to-End Generation           ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
{Colors.ENDC}""")
    print_info("Welcome to the CALYCO Pipeline. Choose an option below.\n")


def run_full(seed_text='calyco'):
    """Execute complete pipeline: data → content → image → QA"""
    print_header("RUNNING FULL PIPELINE")
    out_base = str(BASE)
    write_run_log(out_base, 'Run: full pipeline start')
    
    try:
        print_section("1️⃣  Data Collection")
        from .data_collector import collect_trends, fetch_feeds
        trends = collect_trends(out_base=out_base)
        print_success(f"Collected {len(trends.get('trend_summary', []))} trend insights")
        
        feeds = fetch_feeds(out_base=out_base)
        print_success(f"Fetched {len(feeds)} competitor feed items")
        comp_summ = [f"{i.get('title')}: {i.get('summary')[:100]}" for i in feeds]
        
        print_section("2️⃣  Content Generation")
        from .content_generator import generate_article
        article_info = generate_article(trends['trend_summary'], comp_summ, out_base=out_base, seed_text=seed_text)
        print_success(f"Generated article: '{article_info.get('title')}'")
        print_info(f"Word count: {article_info.get('word_count')} words")
        
        print_section("3️⃣  Image Generation")
        from .image_generator import generate_image_variants
        img_meta = generate_image_variants(seed_text=seed_text, out_base=out_base)
        print_success(f"Generated hero image (variant {img_meta['chosen']})")
        print_info(f"Variants saved: {', '.join(img_meta['variants'].keys())}")
        
        print_section("4️⃣  Quality Assurance")
        from .qa_and_valuation import run_article_checks, rank_images, final_qa
        qa = run_article_checks(str(OUT / 'article.html'), out_base=out_base)
        print_success(f"Article QA: Readability {qa.get('readability_flesch_like'):.1f}, Originality {qa.get('originality_score')}")
        
        rank = rank_images(str(OUT / 'image_metadata.json'), out_base=out_base)
        print_success(f"Image ranking: {rank['explanation'][:60]}...")
        
        final = final_qa(str(OUT / 'article.html'), out_base=out_base)
        print_success(f"Final QA complete")
        
        write_run_log(out_base, 'Run: full pipeline end')
        
        # Summary
        print_header("PIPELINE COMPLETE ✓")
        print(f"{Colors.BOLD}Summary:{Colors.ENDC}")
        print(f"  {Colors.GREEN}Title:{Colors.ENDC} {article_info.get('title')}")
        print(f"  {Colors.GREEN}Word Count:{Colors.ENDC} {article_info.get('word_count')} words")
        print(f"  {Colors.GREEN}Hero Image:{Colors.ENDC} outputs/hero.png")
        print(f"  {Colors.GREEN}Files Generated:{Colors.ENDC} 13 output files")
        print(f"\n{Colors.GREEN}All outputs saved to: {OUT}{Colors.ENDC}\n")
        
    except Exception as e:
        print_error(f"Pipeline failed: {str(e)}")
        write_run_log(out_base, f'Pipeline error: {e}')
        raise


def preview_outputs():
    """Show article preview and list generated files"""
    art = OUT / 'article.html'
    if not art.exists():
        print_error('No article found in outputs/. Run generation first.')
        return
    
    print_header("OUTPUT PREVIEW")
    text = art.read_text(encoding='utf-8')
    
    import re
    title = re.search(r'<h1>(.*?)</h1>', text)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', text, re.S)
    
    print_section("Article Headline")
    print(f"{Colors.BOLD}{title.group(1) if title else 'No title found'}{Colors.ENDC}\n")
    
    print_section("First Two Paragraphs")
    for i, p in enumerate(paras[:2], 1):
        clean = re.sub(r'<[^>]+>', '', p).strip()
        print(f"{i}. {clean[:200]}...\n")
    
    print_section("Generated Output Files")
    files = sorted([p.name for p in OUT.iterdir() if p.is_file()])
    for f in files:
        size = (OUT / f).stat().st_size
        size_str = f"{size/1024:.1f}K" if size > 1024 else f"{size}B"
        icon = "📄" if f.endswith('.json') else "🖼️" if f.endswith('.png') else "📋"
        print(f"  {icon} {f:30} ({size_str})")
    print()


def export_zip(name='calyco_submission.zip'):
    """Export all outputs to ZIP file"""
    zpath = Path(name)
    count = 0
    print_header("EXPORTING OUTPUTS")
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in (BASE / 'outputs').rglob('*'):
            if p.is_file():
                z.write(p, arcname=str(p.relative_to(BASE)))
                count += 1
    print_success(f"Exported {count} files to {zpath}")
    print_info(f"File size: {zpath.stat().st_size / 1024:.1f}K")
    write_run_log(str(BASE), f'Exported zip {zpath} ({count} files)')
    print()


def start_server():
    """Launch Flask web preview server"""
    print_header("STARTING WEB PREVIEW SERVER")
    print_info("Flask server starting at http://localhost:8000")
    print_warning("Press Ctrl+C to stop the server\n")
    write_run_log(str(BASE), 'Starting preview server')
    os.environ['FLASK_APP'] = 'ai_content_pipeline.app'
    os.environ['FLASK_RUN_PORT'] = '8000'
    os.system('flask run --host=127.0.0.1 --port=8000')


def menu():
    """Interactive menu-driven CLI"""
    print_welcome()
    out_base = str(BASE)
    
    while True:
        print_section("Main Menu")
        print(f"""
{Colors.BOLD}Options:{Colors.ENDC}
  {Colors.CYAN}1{Colors.ENDC}) {Colors.BOLD}Run full pipeline{Colors.ENDC} (data → content → image → QA)
  {Colors.CYAN}2{Colors.ENDC}) Run data collection only
  {Colors.CYAN}3{Colors.ENDC}) Regenerate article content
  {Colors.CYAN}4{Colors.ENDC}) Regenerate image variants
  {Colors.CYAN}5{Colors.ENDC}) Preview outputs
  {Colors.CYAN}6{Colors.ENDC}) Start web preview server (Flask)
  {Colors.CYAN}7{Colors.ENDC}) Export ZIP for submission
  {Colors.CYAN}0{Colors.ENDC}) Exit
""")
        
        choice = input(f"{Colors.BOLD}Select option [0-7]: {Colors.ENDC}").strip()
        
        if choice == '1':
            run_full()
        elif choice == '2':
            print_section("Data Collection")
            from .data_collector import collect_trends, fetch_feeds
            collect_trends(out_base=out_base)
            fetch_feeds(out_base=out_base)
            print_success("Data collection complete")
        elif choice == '3':
            print_section("Article Regeneration")
            from .data_collector import collect_trends, fetch_feeds
            trends = collect_trends(out_base=out_base)
            feeds = fetch_feeds(out_base=out_base)
            comp_summ = [f"{i.get('title')}: {i.get('summary')[:120]}" for i in feeds]
            from .content_generator import generate_article
            article = generate_article(trends['trend_summary'], comp_summ, out_base=out_base)
            print_success(f"Article regenerated: {article['word_count']} words")
        elif choice == '4':
            print_section("Image Regeneration")
            from .image_generator import generate_image_variants
            seed = input("Enter seed text (or press Enter for 'calyco'): ").strip() or 'calyco'
            img = generate_image_variants(seed_text=seed, out_base=out_base)
            print_success(f"Image regenerated (variant {img['chosen']} selected)")
        elif choice == '5':
            preview_outputs()
        elif choice == '6':
            start_server()
        elif choice == '7':
            name = input("Zip filename [default: calyco_submission.zip]: ").strip() or 'calyco_submission.zip'
            export_zip(name)
        elif choice == '0':
            print_info("Exiting CALYCO Pipeline. Goodbye!")
            break
        else:
            print_error("Unknown option. Please try again.")


if __name__ == '__main__':
    # Default: run full pipeline in one command
    # Use --menu flag for interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == '--menu':
        menu()
    else:
        run_full()
