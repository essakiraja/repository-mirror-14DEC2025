import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
from models import FileStructure
from config import KEY_FILES, EXCLUDED_DIRS, EXCLUDED_EXTENSIONS, CODE_EXTENSIONS

class StructureAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.all_extensions = set()
        for exts in CODE_EXTENSIONS.values():
            self.all_extensions.update(exts)
    
    def should_exclude(self, path: Path) -> bool:
        parts = path.parts
        for part in parts:
            if part in EXCLUDED_DIRS:
                return True
        
        if path.suffix in EXCLUDED_EXTENSIONS:
            return True
        
        return False
    
    def is_code_file(self, path: Path) -> bool:
        return path.suffix in self.all_extensions
    
    def calculate_depth(self, path: Path) -> int:
        try:
            relative = path.relative_to(self.repo_path)
            return len(relative.parts) - 1
        except ValueError:
            return 0
    
    def find_key_files(self) -> Dict[str, bool]:
        found_files = {}
        
        for category, filenames in KEY_FILES.items():
            found_files[category] = False
            for filename in filenames:
                file_path = self.repo_path / filename
                if file_path.exists():
                    found_files[category] = True
                    break
        
        return found_files
    
    def analyze(self) -> FileStructure:
        total_files = 0
        total_code_files = 0
        depths = []
        directories = 0
        file_types = defaultdict(int)
        file_sizes = []
        
        for root, dirs, files in os.walk(self.repo_path):
            root_path = Path(root)
            
            if self.should_exclude(root_path):
                dirs[:] = []
                continue
            
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            if dirs:
                directories += len(dirs)
            
            for file in files:
                file_path = root_path / file
                
                if self.should_exclude(file_path):
                    continue
                
                total_files += 1
                depth = self.calculate_depth(file_path)
                depths.append(depth)
                
                ext = file_path.suffix or 'no_extension'
                file_types[ext] += 1
                
                if self.is_code_file(file_path):
                    total_code_files += 1
                
                try:
                    size = file_path.stat().st_size
                    file_sizes.append((str(file_path.relative_to(self.repo_path)), size))
                except:
                    pass
        
        max_depth = max(depths) if depths else 0
        avg_depth = sum(depths) / len(depths) if depths else 0
        
        largest_files = sorted(file_sizes, key=lambda x: x[1], reverse=True)[:10]
        
        key_files_present = self.find_key_files()
        
        return FileStructure(
            total_files=total_files,
            total_code_files=total_code_files,
            max_depth=max_depth,
            avg_depth=round(avg_depth, 2),
            directories=directories,
            key_files_present=key_files_present,
            file_types=dict(file_types),
            largest_files=largest_files
        )