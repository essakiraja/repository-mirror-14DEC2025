import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List
from models import CodeMetrics
from config import CODE_EXTENSIONS, EXCLUDED_DIRS
import lizard

class CodeAnalyzer:
    def __init__(self, repo_path: str, primary_language: str = None):
        self.repo_path = Path(repo_path)
        self.primary_language = primary_language
        self.code_extensions = self._get_relevant_extensions()
    
    def _get_relevant_extensions(self) -> set:
        if self.primary_language and self.primary_language.lower() in CODE_EXTENSIONS:
            return set(CODE_EXTENSIONS[self.primary_language.lower()])
        
        all_exts = set()
        for exts in CODE_EXTENSIONS.values():
            all_exts.update(exts)
        return all_exts
    
    def should_analyze(self, path: Path) -> bool:
        if any(excluded in path.parts for excluded in EXCLUDED_DIRS):
            return False
        
        return path.suffix in self.code_extensions
    
    def count_lines(self, content: str) -> Dict[str, int]:
        lines = content.split('\n')
        total = len(lines)
        blank = sum(1 for line in lines if not line.strip())
        
        comment_patterns = [
            r'^\s*#',
            r'^\s*//',
            r'^\s*/\*',
            r'^\s*\*',
            r'^\s*"""',
            r"^\s*'''",
        ]
        
        comment = 0
        in_block_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            if '"""' in stripped or "'''" in stripped:
                in_block_comment = not in_block_comment
                comment += 1
                continue
            
            if in_block_comment:
                comment += 1
                continue
            
            for pattern in comment_patterns:
                if re.match(pattern, line):
                    comment += 1
                    break
        
        code = total - blank - comment
        
        return {
            'total': total,
            'code': max(0, code),
            'comment': comment,
            'blank': blank
        }
    
    def analyze_complexity(self, file_path: Path) -> Dict:
        try:
            analysis = lizard.analyze_file(str(file_path))
            
            complexities = [func.cyclomatic_complexity for func in analysis.function_list]
            function_lengths = [func.length for func in analysis.function_list]
            
            distribution = defaultdict(int)
            for cc in complexities:
                if cc <= 5:
                    distribution['low'] += 1
                elif cc <= 10:
                    distribution['medium'] += 1
                elif cc <= 20:
                    distribution['high'] += 1
                else:
                    distribution['very_high'] += 1
            
            return {
                'functions': len(analysis.function_list),
                'avg_complexity': sum(complexities) / len(complexities) if complexities else 0,
                'max_complexity': max(complexities) if complexities else 0,
                'avg_function_length': sum(function_lengths) / len(function_lengths) if function_lengths else 0,
                'distribution': dict(distribution)
            }
        except Exception as e:
            return {
                'functions': 0,
                'avg_complexity': 0,
                'max_complexity': 0,
                'avg_function_length': 0,
                'distribution': {}
            }
    
    def analyze(self) -> CodeMetrics:
        total_lines = 0
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        files_analyzed = 0
        
        all_complexities = []
        all_function_lengths = []
        total_functions = 0
        complexity_dist = defaultdict(int)
        
        file_lengths = []
        
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                
                if not self.should_analyze(file_path):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    line_counts = self.count_lines(content)
                    total_lines += line_counts['total']
                    code_lines += line_counts['code']
                    comment_lines += line_counts['comment']
                    blank_lines += line_counts['blank']
                    
                    file_lengths.append(line_counts['total'])
                    
                    complexity_data = self.analyze_complexity(file_path)
                    total_functions += complexity_data['functions']
                    
                    if complexity_data['avg_complexity'] > 0:
                        all_complexities.append(complexity_data['avg_complexity'])
                    
                    if complexity_data['avg_function_length'] > 0:
                        all_function_lengths.append(complexity_data['avg_function_length'])
                    
                    for key, value in complexity_data['distribution'].items():
                        complexity_dist[key] += value
                    
                    files_analyzed += 1
                
                except Exception as e:
                    continue
        
        avg_file_length = sum(file_lengths) / len(file_lengths) if file_lengths else 0
        avg_function_length = sum(all_function_lengths) / len(all_function_lengths) if all_function_lengths else 0
        avg_complexity = sum(all_complexities) / len(all_complexities) if all_complexities else 0
        max_complexity = max(all_complexities) if all_complexities else 0
        
        comment_ratio = comment_lines / code_lines if code_lines > 0 else 0
        
        return CodeMetrics(
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            avg_file_length=round(avg_file_length, 2),
            avg_function_length=round(avg_function_length, 2),
            comment_ratio=round(comment_ratio, 3),
            files_analyzed=files_analyzed,
            functions_count=total_functions,
            classes_count=0,
            avg_complexity=round(avg_complexity, 2),
            max_complexity=int(max_complexity),
            complexity_distribution=dict(complexity_dist)
        )