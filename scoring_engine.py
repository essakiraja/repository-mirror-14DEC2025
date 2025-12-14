from typing import List
from models import (
    DimensionScore, FileStructure, CodeMetrics, GitMetrics,
    TestingMetrics, MaturityMetrics
)
from config import SCORING_WEIGHTS, TIER_THRESHOLDS, CONFIDENCE_THRESHOLDS

class ScoringEngine:
    def __init__(self):
        self.weights = SCORING_WEIGHTS
    
    def score_code_quality(self, code_metrics: CodeMetrics) -> DimensionScore:
        max_score = 100
        score = 0
        signals = {}
        reasons = []
        
        if code_metrics.comment_ratio >= 0.15:
            score += 25
            signals['comment_ratio'] = 'excellent'
            reasons.append(f"Good comment ratio ({code_metrics.comment_ratio:.1%})")
        elif code_metrics.comment_ratio >= 0.08:
            score += 15
            signals['comment_ratio'] = 'adequate'
            reasons.append(f"Adequate comment ratio ({code_metrics.comment_ratio:.1%})")
        else:
            score += 5
            signals['comment_ratio'] = 'poor'
            reasons.append(f"Low comment ratio ({code_metrics.comment_ratio:.1%})")
        
        if code_metrics.avg_complexity <= 5:
            score += 30
            signals['complexity'] = 'low'
            reasons.append(f"Low average complexity ({code_metrics.avg_complexity:.1f})")
        elif code_metrics.avg_complexity <= 10:
            score += 20
            signals['complexity'] = 'moderate'
            reasons.append(f"Moderate complexity ({code_metrics.avg_complexity:.1f})")
        else:
            score += 10
            signals['complexity'] = 'high'
            reasons.append(f"High complexity ({code_metrics.avg_complexity:.1f})")
        
        if code_metrics.avg_file_length <= 300:
            score += 20
            signals['file_length'] = 'optimal'
            reasons.append(f"Good file length ({code_metrics.avg_file_length:.0f} lines)")
        elif code_metrics.avg_file_length <= 500:
            score += 12
            signals['file_length'] = 'acceptable'
        else:
            score += 5
            signals['file_length'] = 'long'
            reasons.append(f"Files are long ({code_metrics.avg_file_length:.0f} lines avg)")
        
        if code_metrics.avg_function_length <= 30:
            score += 15
            signals['function_length'] = 'optimal'
            reasons.append("Functions are concise")
        elif code_metrics.avg_function_length <= 50:
            score += 10
            signals['function_length'] = 'acceptable'
        else:
            score += 3
            signals['function_length'] = 'long'
            reasons.append(f"Functions are long ({code_metrics.avg_function_length:.0f} lines)")
        
        if code_metrics.max_complexity > 20:
            score -= 10
            reasons.append(f"Some functions are very complex (max: {code_metrics.max_complexity})")
        
        high_complexity_ratio = code_metrics.complexity_distribution.get('high', 0) + \
                                code_metrics.complexity_distribution.get('very_high', 0)
        if high_complexity_ratio > code_metrics.functions_count * 0.2:
            score -= 5
            reasons.append("Many functions have high complexity")
        
        score += 10
        
        score = max(0, min(score, max_score))
        percentage = score / max_score
        weighted = percentage * self.weights['code_quality'] * 100
        
        reasoning = "; ".join(reasons) if reasons else "Code quality metrics analyzed"
        
        return DimensionScore(
            name="Code Quality",
            score=score,
            max_score=max_score,
            percentage=round(percentage, 3),
            weight=self.weights['code_quality'],
            weighted_score=round(weighted, 2),
            signals=signals,
            reasoning=reasoning
        )
    
    def score_structure_modularity(self, file_structure: FileStructure) -> DimensionScore:
        max_score = 100
        score = 0
        signals = {}
        reasons = []
        
        if file_structure.total_files == 0:
            return DimensionScore(
                name="Structure & Modularity",
                score=0,
                max_score=max_score,
                percentage=0,
                weight=self.weights['structure_modularity'],
                weighted_score=0,
                signals={},
                reasoning="No files found in repository"
            )
        
        if 5 <= file_structure.total_files <= 50:
            score += 25
            signals['file_count'] = 'optimal'
            reasons.append("Well-sized project")
        elif file_structure.total_files <= 100:
            score += 20
            signals['file_count'] = 'good'
        elif file_structure.total_files > 200:
            score += 10
            signals['file_count'] = 'large'
            reasons.append("Large project with many files")
        else:
            score += 15
            signals['file_count'] = 'moderate'
        
        if 2 <= file_structure.max_depth <= 5:
            score += 25
            signals['depth'] = 'optimal'
            reasons.append(f"Good directory depth ({file_structure.max_depth})")
        elif file_structure.max_depth <= 7:
            score += 18
            signals['depth'] = 'acceptable'
        elif file_structure.max_depth > 10:
            score += 8
            signals['depth'] = 'too_deep'
            reasons.append(f"Deep directory nesting ({file_structure.max_depth} levels)")
        else:
            score += 15
            signals['depth'] = 'moderate'
        
        code_ratio = file_structure.total_code_files / file_structure.total_files
        if code_ratio >= 0.6:
            score += 20
            signals['code_ratio'] = 'high'
            reasons.append("High proportion of code files")
        elif code_ratio >= 0.3:
            score += 15
            signals['code_ratio'] = 'moderate'
        else:
            score += 8
            signals['code_ratio'] = 'low'
        
        organization_score = 0
        if file_structure.directories >= 3:
            organization_score += 15
            reasons.append("Well-organized with multiple directories")
        elif file_structure.directories >= 1:
            organization_score += 10
        else:
            organization_score += 3
            reasons.append("Flat structure with few directories")
        
        score += organization_score
        
        extension_diversity = len(file_structure.file_types)
        if extension_diversity >= 5:
            score += 15
            signals['diversity'] = 'high'
        elif extension_diversity >= 3:
            score += 10
            signals['diversity'] = 'moderate'
        else:
            score += 5
            signals['diversity'] = 'low'
        
        score = max(0, min(score, max_score))
        percentage = score / max_score
        weighted = percentage * self.weights['structure_modularity'] * 100
        
        reasoning = "; ".join(reasons) if reasons else "Structure metrics analyzed"
        
        return DimensionScore(
            name="Structure & Modularity",
            score=score,
            max_score=max_score,
            percentage=round(percentage, 3),
            weight=self.weights['structure_modularity'],
            weighted_score=round(weighted, 2),
            signals=signals,
            reasoning=reasoning
        )
    
    def score_documentation(self, file_structure: FileStructure) -> DimensionScore:
        max_score = 100
        score = 0
        signals = {}
        reasons = []
        
        key_files = file_structure.key_files_present
        
        if key_files.get('readme', False):
            score += 40
            signals['readme'] = True
            reasons.append("README present")
        else:
            signals['readme'] = False
            reasons.append("Missing README")
        
        if key_files.get('license', False):
            score += 20
            signals['license'] = True
            reasons.append("LICENSE present")
        else:
            signals['license'] = False
            reasons.append("Missing LICENSE")
        
        if key_files.get('contributing', False):
            score += 15
            signals['contributing'] = True
            reasons.append("CONTRIBUTING guide present")
        else:
            signals['contributing'] = False
        
        if key_files.get('changelog', False):
            score += 10
            signals['changelog'] = True
            reasons.append("CHANGELOG present")
        else:
            signals['changelog'] = False
        
        if key_files.get('code_of_conduct', False):
            score += 10
            signals['code_of_conduct'] = True
        else:
            signals['code_of_conduct'] = False
        
        doc_indicators = ['.md', '.rst', '.txt']
        doc_files = sum(count for ext, count in file_structure.file_types.items() 
                       if ext in doc_indicators)
        
        if doc_files >= 5:
            score += 5
            reasons.append("Multiple documentation files")
        elif doc_files >= 2:
            score += 3
        
        score = max(0, min(score, max_score))
        percentage = score / max_score
        weighted = percentage * self.weights['documentation'] * 100
        
        reasoning = "; ".join(reasons) if reasons else "Documentation assessed"
        
        return DimensionScore(
            name="Documentation",
            score=score,
            max_score=max_score,
            percentage=round(percentage, 3),
            weight=self.weights['documentation'],
            weighted_score=round(weighted, 2),
            signals=signals,
            reasoning=reasoning
        )
    
    def score_testing_maintainability(self, testing: TestingMetrics, 
                                     code_metrics: CodeMetrics) -> DimensionScore:
        max_score = 100
        score = 0
        signals = {}
        reasons = []
        
        if testing.has_test_directory:
            score += 25
            signals['test_directory'] = True
            reasons.append("Test directory present")
        else:
            signals['test_directory'] = False
            reasons.append("No test directory found")
        
        if testing.test_to_code_ratio >= 0.3:
            score += 25
            signals['test_coverage'] = 'excellent'
            reasons.append(f"High test coverage ({testing.test_to_code_ratio:.1%})")
        elif testing.test_to_code_ratio >= 0.15:
            score += 15
            signals['test_coverage'] = 'good'
            reasons.append(f"Moderate test coverage ({testing.test_to_code_ratio:.1%})")
        elif testing.test_to_code_ratio > 0:
            score += 8
            signals['test_coverage'] = 'low'
            reasons.append(f"Low test coverage ({testing.test_to_code_ratio:.1%})")
        else:
            signals['test_coverage'] = 'none'
            reasons.append("No tests detected")
        
        if testing.has_ci_cd:
            score += 20
            signals['ci_cd'] = True
            reasons.append(f"CI/CD configured ({', '.join(testing.ci_cd_tools)})")
        else:
            signals['ci_cd'] = False
            reasons.append("No CI/CD configuration")
        
        if testing.has_linter_config:
            score += 15
            signals['linter'] = True
            reasons.append("Linter configured")
        else:
            signals['linter'] = False
            reasons.append("No linter configuration")
        
        if code_metrics.avg_complexity <= 8:
            score += 15
            signals['maintainability'] = 'high'
            reasons.append("Low complexity improves maintainability")
        elif code_metrics.avg_complexity <= 15:
            score += 10
            signals['maintainability'] = 'moderate'
        else:
            score += 5
            signals['maintainability'] = 'low'
            reasons.append("High complexity reduces maintainability")
        
        score = max(0, min(score, max_score))
        percentage = score / max_score
        weighted = percentage * self.weights['testing_maintainability'] * 100
        
        reasoning = "; ".join(reasons) if reasons else "Testing and maintainability assessed"
        
        return DimensionScore(
            name="Testing & Maintainability",
            score=score,
            max_score=max_score,
            percentage=round(percentage, 3),
            weight=self.weights['testing_maintainability'],
            weighted_score=round(weighted, 2),
            signals=signals,
            reasoning=reasoning
        )
    
    def score_git_practices(self, git_metrics: GitMetrics) -> DimensionScore:
        max_score = 100
        score = 0
        signals = {}
        reasons = []
        
        if git_metrics.total_commits == 0:
            return DimensionScore(
                name="Git Practices",
                score=0,
                max_score=max_score,
                percentage=0,
                weight=self.weights['git_practices'],
                weighted_score=0,
                signals={},
                reasoning="No commit history"
            )
        
        if git_metrics.total_commits >= 20:
            score += 20
            signals['commit_count'] = 'high'
            reasons.append(f"Healthy commit history ({git_metrics.total_commits} commits)")
        elif git_metrics.total_commits >= 10:
            score += 15
            signals['commit_count'] = 'moderate'
        elif git_metrics.total_commits >= 5:
            score += 10
            signals['commit_count'] = 'low'
        else:
            score += 5
            signals['commit_count'] = 'very_low'
            reasons.append(f"Few commits ({git_metrics.total_commits})")
        
        good_message_ratio = git_metrics.good_commit_messages / git_metrics.total_commits
        if good_message_ratio >= 0.7:
            score += 25
            signals['message_quality'] = 'excellent'
            reasons.append("Excellent commit message quality")
        elif good_message_ratio >= 0.5:
            score += 18
            signals['message_quality'] = 'good'
            reasons.append("Good commit messages")
        elif good_message_ratio >= 0.3:
            score += 10
            signals['message_quality'] = 'moderate'
        else:
            score += 5
            signals['message_quality'] = 'poor'
            reasons.append("Poor commit message quality")
        
        if git_metrics.commit_frequency_trend == 'active':
            score += 20
            signals['activity'] = 'active'
            reasons.append("Recently active development")
        elif git_metrics.commit_frequency_trend == 'moderate':
            score += 12
            signals['activity'] = 'moderate'
        elif git_metrics.commit_frequency_trend == 'inactive':
            score += 5
            signals['activity'] = 'inactive'
            reasons.append("Low recent activity")
        else:
            score += 10
            signals['activity'] = 'unknown'
        
        incremental_ratio = git_metrics.incremental_commits / max(git_metrics.total_commits, 1)
        if incremental_ratio >= 0.7:
            score += 20
            signals['commit_style'] = 'incremental'
            reasons.append("Incremental development approach")
        elif incremental_ratio >= 0.4:
            score += 12
            signals['commit_style'] = 'mixed'
        else:
            score += 5
            signals['commit_style'] = 'large_commits'
            reasons.append("Many large commits")
        
        if git_metrics.total_branches > 1:
            score += 15
            signals['branching'] = True
            reasons.append(f"Uses branches ({git_metrics.total_branches})")
        else:
            signals['branching'] = False
            reasons.append("Single branch development")
        
        score = max(0, min(score, max_score))
        percentage = score / max_score
        weighted = percentage * self.weights['git_practices'] * 100
        
        reasoning = "; ".join(reasons) if reasons else "Git practices assessed"
        
        return DimensionScore(
            name="Git Practices",
            score=score,
            max_score=max_score,
            percentage=round(percentage, 3),
            weight=self.weights['git_practices'],
            weighted_score=round(weighted, 2),
            signals=signals,
            reasoning=reasoning
        )
    
    def score_real_world_readiness(self, maturity: MaturityMetrics, 
                                   file_structure: FileStructure) -> DimensionScore:
        max_score = 100
        score = 0
        signals = {}
        reasons = []
        
        if maturity.has_package_manager:
            score += 25
            signals['package_manager'] = True
            reasons.append(f"Package manager configured ({', '.join(maturity.package_managers)})")
        else:
            signals['package_manager'] = False
            reasons.append("No package manager detected")
        
        if file_structure.key_files_present.get('gitignore', False):
            score += 10
            signals['gitignore'] = True
        else:
            signals['gitignore'] = False
            reasons.append("Missing .gitignore")
        
        if maturity.has_config_example:
            score += 15
            signals['config_example'] = True
            reasons.append("Configuration examples provided")
        else:
            signals['config_example'] = False
            reasons.append("No config examples")
        
        feature_count = sum(1 for v in maturity.real_world_features.values() if v)
        if feature_count >= 3:
            score += 25
            signals['features'] = 'production_ready'
            reasons.append(f"Production features detected ({feature_count})")
        elif feature_count >= 2:
            score += 18
            signals['features'] = 'intermediate'
            reasons.append("Some production features")
        elif feature_count >= 1:
            score += 10
            signals['features'] = 'basic'
        else:
            signals['features'] = 'minimal'
            reasons.append("Few production features")
        
        if maturity.error_handling_score >= 0.6:
            score += 15
            signals['error_handling'] = 'excellent'
            reasons.append("Strong error handling")
        elif maturity.error_handling_score >= 0.3:
            score += 10
            signals['error_handling'] = 'adequate'
        elif maturity.error_handling_score > 0:
            score += 5
            signals['error_handling'] = 'minimal'
        else:
            signals['error_handling'] = 'none'
            reasons.append("No error handling detected")
        
        if maturity.has_deployment_config:
            score += 10
            signals['deployment'] = True
            reasons.append("Deployment configuration present")
        else:
            signals['deployment'] = False
        
        score = max(0, min(score, max_score))
        percentage = score / max_score
        weighted = percentage * self.weights['real_world_readiness'] * 100
        
        reasoning = "; ".join(reasons) if reasons else "Real-world readiness assessed"
        
        return DimensionScore(
            name="Real-World Readiness",
            score=score,
            max_score=max_score,
            percentage=round(percentage, 3),
            weight=self.weights['real_world_readiness'],
            weighted_score=round(weighted, 2),
            signals=signals,
            reasoning=reasoning
        )
    
    def calculate_overall_score(self, dimension_scores: List[DimensionScore]) -> float:
        total_weighted = sum(ds.weighted_score for ds in dimension_scores)
        return round(total_weighted, 2)
    
    def determine_tier(self, score: float) -> str:
        if score >= TIER_THRESHOLDS['advanced']:
            return "Advanced"
        elif score >= TIER_THRESHOLDS['intermediate']:
            return "Intermediate"
        else:
            return "Beginner"
    
    def determine_confidence(self, total_files: int, total_commits: int) -> str:
        if (total_files >= CONFIDENCE_THRESHOLDS['high']['min_files'] and 
            total_commits >= CONFIDENCE_THRESHOLDS['high']['min_commits']):
            return "High"
        elif (total_files >= CONFIDENCE_THRESHOLDS['medium']['min_files'] and 
              total_commits >= CONFIDENCE_THRESHOLDS['medium']['min_commits']):
            return "Medium"
        else:
            return "Low"