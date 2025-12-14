#!/usr/bin/env python3

import json
from repository_mirror import RepositoryMirror

def analyze_repository(repo_url: str, output_file: str = None):
    print(f"\n{'='*70}")
    print(f"ANALYZING: {repo_url}")
    print(f"{'='*70}\n")
    
    mirror = RepositoryMirror()
    
    analysis = mirror.analyze(repo_url)
    
    output = mirror.generate_output(analysis)
    
    print(f"\n{'='*70}")
    print(f"RESULTS")
    print(f"{'='*70}")
    print(f"\nScore: {output['score']}/100")
    print(f"Tier: {output['tier']}")
    print(f"Confidence: {output['confidence']}")
    
    print(f"\n{'-'*70}")
    print("Dimension Breakdown:")
    print(f"{'-'*70}")
    for dim_name, dim_data in output['metadata']['dimensions'].items():
        print(f"  {dim_name:30s}: {dim_data['percentage']:.0%} (weighted: {dim_data['weighted_score']:.1f})")
        print(f"    → {dim_data['reasoning']}")
    
    print(f"\n{'-'*70}")
    print("Top 3 Strengths:")
    print(f"{'-'*70}")
    for i, strength in enumerate(output['strengths'][:3], 1):
        print(f"  {i}. {strength}")
    
    print(f"\n{'-'*70}")
    print("Top 3 Weaknesses:")
    print(f"{'-'*70}")
    for i, weakness in enumerate(output['weaknesses'][:3], 1):
        print(f"  {i}. {weakness}")
    
    print(f"\n{'-'*70}")
    print("Top 3 Roadmap Items:")
    print(f"{'-'*70}")
    for item in output['roadmap'][:3]:
        print(f"\n  Priority {item['priority']}: {item['action']}")
        print(f"    Effort: {item['effort']}, Impact: {item['impact']}")
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n\nFull results saved to: {output_file}")
    
    print(f"\n{'='*70}\n")
    
    return output

def main():
    repositories = [
        "https://github.com/pallets/flask",
        "https://github.com/expressjs/express",
        "https://github.com/torvalds/linux"
    ]
    
    print("""
╔══════════════════════════════════════════════════════════╗
║         Repository Mirror - Example Usage               ║
╚══════════════════════════════════════════════════════════╝

This script demonstrates analyzing multiple repositories.
    """)
    
    results = []
    
    for i, repo_url in enumerate(repositories, 1):
        print(f"\n[{i}/{len(repositories)}] Processing: {repo_url}")
        
        try:
            output_file = f"analysis_result_{i}.json"
            result = analyze_repository(repo_url, output_file)
            results.append({
                'url': repo_url,
                'score': result['score'],
                'tier': result['tier'],
                'file': output_file
            })
        except Exception as e:
            print(f"\nERROR analyzing {repo_url}: {str(e)}")
            results.append({
                'url': repo_url,
                'score': None,
                'tier': 'Error',
                'file': None
            })
    
    print(f"\n{'='*70}")
    print("COMPARISON SUMMARY")
    print(f"{'='*70}\n")
    
    results.sort(key=lambda x: x['score'] if x['score'] is not None else -1, reverse=True)
    
    for i, result in enumerate(results, 1):
        score_str = f"{result['score']}/100" if result['score'] is not None else "N/A"
        print(f"{i}. {result['url']}")
        print(f"   Score: {score_str} | Tier: {result['tier']}")
        if result['file']:
            print(f"   Results: {result['file']}")
        print()

if __name__ == '__main__':
    main()