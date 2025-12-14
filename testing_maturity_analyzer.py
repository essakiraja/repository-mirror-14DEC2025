import os
import re
from pathlib import Path
from typing import List, Dict
from models import TestingMetrics, MaturityMetrics
from config import (
    TEST_INDICATORS, LINTER_CONFIGS, PACKAGE_MANAGERS,
    CONFIG_FILES, REAL_WORLD_INDICATORS, EXCLUDED_DIRS, CODE_EXTENSIONS
)

class TestingMaturityAnalyzer:
    def __init__(self, repo_path: str, primary_language: str = None):
        self.repo_path = Path(repo_path)
        self.primary_language = primary_language
        self.all_files = []
        self.all_dirs = []
        self._scan_repository()
    
    def _scan_repository(self):
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            self.all_dirs.extend([os.path.join(root, d) for d in dirs])
            self.all_files.extend([os.path.join(root, f) for f in files])
    
    def detect_test_files(self) -> tuple:
        has_test_dir = False
        test_files = []
        
        for dir_path in self.all_dirs:
            dir_name = os.path.basename(dir_path).lower()
            if any(indicator in dir_name for indicator in TEST_INDICATORS):
                has_test_dir = True
        
        for file_path in self.all_files:
            file_name = os.path.basename(file_path).lower()
            if any(indicator in file_name for indicator in TEST_INDICATORS):
                test_files.append(file_path)
        
        return has_test_dir, len(test_files)
    
    def detect_ci_cd(self) -> tuple:
        ci_cd_tools = []
        
        ci_cd_patterns = {
            '.github/workflows': 'GitHub Actions',
            '.gitlab-ci.yml': 'GitLab CI',
            '.travis.yml': 'Travis CI',
            'Jenkinsfile': 'Jenkins',
            '.circleci': 'CircleCI',
            'azure-pipelines.yml': 'Azure Pipelines',
            '.drone.yml': 'Drone CI',
            'bitbucket-pipelines.yml': 'Bitbucket Pipelines'
        }
        
        for pattern, tool in ci_cd_patterns.items():
            check_path = self.repo_path / pattern
            if check_path.exists():
                ci_cd_tools.append(tool)
        
        return len(ci_cd_tools) > 0, ci_cd_tools
    
    def detect_linters(self) -> tuple:
        linter_tools = []
        
        relevant_configs = []
        if self.primary_language and self.primary_language.lower() in LINTER_CONFIGS:
            relevant_configs = LINTER_CONFIGS[self.primary_language.lower()]
        else:
            for configs in LINTER_CONFIGS.values():
                relevant_configs.extend(configs)
        
        for config_file in relevant_configs:
            check_path = self.repo_path / config_file
            if check_path.exists():
                linter_tools.append(config_file)
        
        return len(linter_tools) > 0, linter_tools
    
    def detect_package_managers(self) -> tuple:
        found_managers = []
        
        relevant_managers = []
        if self.primary_language and self.primary_language.lower() in PACKAGE_MANAGERS:
            relevant_managers = PACKAGE_MANAGERS[self.primary_language.lower()]
        else:
            for managers in PACKAGE_MANAGERS.values():
                relevant_managers.extend(managers)
        
        for manager_file in relevant_managers:
            check_path = self.repo_path / manager_file
            if check_path.exists():
                found_managers.append(manager_file)
        
        return len(found_managers) > 0, found_managers
    
    def detect_config_examples(self) -> bool:
        for config_file in CONFIG_FILES:
            check_path = self.repo_path / config_file
            if check_path.exists():
                return True
        return False
    
    def detect_deployment_config(self) -> tuple:
        deployment_files = [
            'Dockerfile', 'docker-compose.yml', '.dockerignore',
            'Procfile', 'app.yaml', 'app.yml',
            'Makefile', 'deploy.sh', 'deployment.yaml'
        ]
        
        found_tools = []
        for deploy_file in deployment_files:
            check_path = self.repo_path / deploy_file
            if check_path.exists():
                found_tools.append(deploy_file)
        
        k8s_path = self.repo_path / 'k8s'
        if k8s_path.exists() and k8s_path.is_dir():
            found_tools.append('k8s/')
        
        kubernetes_path = self.repo_path / 'kubernetes'
        if kubernetes_path.exists() and kubernetes_path.is_dir():
            found_tools.append('kubernetes/')
        
        return len(found_tools) > 0, found_tools
    
    def detect_real_world_features(self) -> Dict[str, bool]:
        features = {}
        
        for feature_type, indicators in REAL_WORLD_INDICATORS.items():
            features[feature_type] = False
            
            for indicator in indicators:
                for dir_path in self.all_dirs:
                    if indicator.lower() in dir_path.lower():
                        features[feature_type] = True
                        break
                
                if features[feature_type]:
                    break
                
                for file_path in self.all_files:
                    if indicator.lower() in file_path.lower():
                        features[feature_type] = True
                        break
                
                if features[feature_type]:
                    break
        
        return features
    
    def analyze_error_handling(self) -> float:
        code_extensions = set()
        for exts in CODE_EXTENSIONS.values():
            code_extensions.update(exts)
        
        files_with_error_handling = 0
        total_code_files = 0
        
        error_patterns = [
            r'\btry\b',
            r'\bcatch\b',
            r'\bexcept\b',
            r'\bfinally\b',
            r'\bthrow\b',
            r'\braise\b',
            r'\.catch\(',
            r'\.then\(',
            r'\bError\b',
            r'\bException\b'
        ]
        
        for file_path in self.all_files[:100]:
            path_obj = Path(file_path)
            
            if path_obj.suffix not in code_extensions:
                continue
            
            total_code_files += 1
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                for pattern in error_patterns:
                    if re.search(pattern, content):
                        files_with_error_handling += 1
                        break
            except:
                continue
        
        if total_code_files == 0:
            return 0.0
        
        return round(files_with_error_handling / total_code_files, 2)
    
    def analyze_testing(self) -> TestingMetrics:
        has_test_dir, test_files_count = self.detect_test_files()
        has_ci_cd, ci_cd_tools = self.detect_ci_cd()
        has_linter, linter_tools = self.detect_linters()
        
        code_extensions = set()
        for exts in CODE_EXTENSIONS.values():
            code_extensions.update(exts)
        
        code_files = sum(1 for f in self.all_files if Path(f).suffix in code_extensions)
        
        test_ratio = test_files_count / code_files if code_files > 0 else 0
        
        return TestingMetrics(
            has_test_directory=has_test_dir,
            test_files_count=test_files_count,
            test_to_code_ratio=round(test_ratio, 3),
            has_ci_cd=has_ci_cd,
            ci_cd_tools=ci_cd_tools,
            has_linter_config=has_linter,
            linter_tools=linter_tools
        )
    
    def analyze_maturity(self) -> MaturityMetrics:
        has_package_mgr, package_managers = self.detect_package_managers()
        has_config_example = self.detect_config_examples()
        has_deployment, deployment_tools = self.detect_deployment_config()
        real_world_features = self.detect_real_world_features()
        error_handling_score = self.analyze_error_handling()
        
        return MaturityMetrics(
            has_package_manager=has_package_mgr,
            package_managers=package_managers,
            has_config_example=has_config_example,
            has_deployment_config=has_deployment,
            deployment_tools=deployment_tools,
            real_world_features=real_world_features,
            error_handling_score=error_handling_score
        )