#!/usr/bin/env python3
import sys
import json
import argparse
from repository_mirror import RepositoryMirror

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║              REPOSITORY MIRROR - MVP v1.0                ║
║     Deterministic Repository Analysis & Scoring System   ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_summary(output: dict):
    print(f"\n{'='*70}")
    print(f"ANALYSIS RESULTS")
    print(f"{'='*70}")
    print(f"\nRepository: {output['metadata']['repository']['name']}")
    print(f"Owner: {output['metadata']['repository']['owner']}")
    print(f"Language: {output['metadata']['repository']['primary_language']}")
    print(f"\n{'─'*70}")
    print(f"OVERALL SCORE: {output['score']}/100")
    print(f"TIER: {output['tier']}")
    print(f"CONFIDENCE: {output['confidence']}")
    print(f"{'─'*70}")
    
    print(f"\n{output['summary']}")
    
    print(f"\n{'─'*70}")
    print("DIMENSION SCORES:")
    print(f"{'─'*70}")
    for dim_name, dim_data in output['metadata']['dimensions'].items():
        bar_length = int(dim_data['percentage'] * 30)
        bar = '█' * bar_length + '░' * (30 - bar_length)
        print(f"  {dim_name:30s} [{bar}] {dim_data['percentage']:.0%} ({dim_data['weighted_score']:.1f}/100)")
    
    print(f"\n{'─'*70}")
    print("STRENGTHS:")
    print(f"{'─'*70}")
    for i, strength in enumerate(output['strengths'], 1):
        print(f"  {i}. {strength}")
    
    print(f"\n{'─'*70}")
    print("WEAKNESSES:")
    print(f"{'─'*70}")
    for i, weakness in enumerate(output['weaknesses'], 1):
        print(f"  {i}. {weakness}")
    
    print(f"\n{'─'*70}")
    print("IMPROVEMENT ROADMAP:")
    print(f"{'─'*70}")
    for item in output['roadmap'][:5]:
        print(f"\n  Priority {item['priority']} - {item['effort']} Effort, {item['impact']} Impact")
        print(f"  → {item['action']}")
        print(f"    Rationale: {item['rationale']}")
    
    print(f"\n{'='*70}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Repository Mirror - Analyze GitHub repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://github.com/user/repo
  python main.py https://github.com/user/repo --output result.json
  python main.py https://github.com/user/repo --quiet --output result.json

Environment Variables:
  GITHUB_TOKEN    GitHub personal access token (optional, for higher rate limits)
        """
    )
    
    parser.add_argument(
        'repo_url',
        help='GitHub repository URL (e.g., https://github.com/user/repo)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output JSON file path (optional)',
        default=None
    )
    
    parser.add_argument(
        '-q', '--quiet',
        help='Suppress console output (only save to file)',
        action='store_true'
    )
    
    parser.add_argument(
        '--token',
        help='GitHub personal access token (overrides GITHUB_TOKEN env var)',
        default=None
    )
    
    args = parser.parse_args()
    
    if not args.quiet:
        print_banner()
    
    try:
        mirror = RepositoryMirror(github_token=args.token)
        
        analysis = mirror.analyze(args.repo_url)
        
        output = mirror.generate_output(analysis)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            if not args.quiet:
                print(f"\nResults saved to: {args.output}")
        
        if not args.quiet:
            print_summary(output)
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        return 130
    
    except Exception as e:
        print(f"\nERROR: {str(e)}", file=sys.stderr)
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())