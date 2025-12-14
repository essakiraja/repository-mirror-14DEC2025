from typing import List, Tuple
from models import AnalysisResult, RoadmapItem

class InsightGenerator:
    def __init__(self):
        pass
    
    def generate_strengths(self, analysis: AnalysisResult) -> List[str]:
        strengths = []
        
        for dimension in analysis.dimension_scores:
            if dimension.percentage >= 0.8:
                strengths.append(f"{dimension.name}: {dimension.reasoning}")
        
        if analysis.code_metrics.comment_ratio >= 0.15:
            strengths.append(f"Well-documented code with {analysis.code_metrics.comment_ratio:.1%} comment ratio")
        
        if analysis.code_metrics.avg_complexity <= 5:
            strengths.append(f"Low cyclomatic complexity (avg {analysis.code_metrics.avg_complexity:.1f})")
        
        if analysis.git_metrics.total_commits >= 20:
            strengths.append(f"Substantial development history with {analysis.git_metrics.total_commits} commits")
        
        if analysis.testing_metrics.has_ci_cd:
            tools = ", ".join(analysis.testing_metrics.ci_cd_tools)
            strengths.append(f"Automated testing with {tools}")
        
        if analysis.maturity_metrics.error_handling_score >= 0.6:
            strengths.append(f"Strong error handling practices ({analysis.maturity_metrics.error_handling_score:.0%} of files)")
        
        feature_count = sum(1 for v in analysis.maturity_metrics.real_world_features.values() if v)
        if feature_count >= 3:
            features = [k for k, v in analysis.maturity_metrics.real_world_features.items() if v]
            strengths.append(f"Production-ready features: {', '.join(features)}")
        
        if not strengths:
            strengths.append("Repository structure is present")
        
        return strengths[:5]
    
    def generate_weaknesses(self, analysis: AnalysisResult) -> List[str]:
        weaknesses = []
        
        for dimension in analysis.dimension_scores:
            if dimension.percentage < 0.5:
                weaknesses.append(f"{dimension.name}: {dimension.reasoning}")
        
        if not analysis.file_structure.key_files_present.get('readme', False):
            weaknesses.append("Missing README.md - critical for project documentation")
        
        if not analysis.file_structure.key_files_present.get('license', False):
            weaknesses.append("Missing LICENSE - unclear legal status")
        
        if analysis.code_metrics.comment_ratio < 0.05:
            weaknesses.append(f"Very low comment ratio ({analysis.code_metrics.comment_ratio:.1%}) - code may be hard to understand")
        
        if analysis.code_metrics.avg_complexity > 15:
            weaknesses.append(f"High average complexity ({analysis.code_metrics.avg_complexity:.1f}) - refactoring recommended")
        
        if not analysis.testing_metrics.has_test_directory:
            weaknesses.append("No tests detected - code quality and reliability uncertain")
        
        if not analysis.testing_metrics.has_ci_cd:
            weaknesses.append("No CI/CD configuration - manual testing and deployment")
        
        if not analysis.maturity_metrics.has_package_manager:
            weaknesses.append("No package manager detected - dependency management unclear")
        
        if analysis.git_metrics.total_commits < 5:
            weaknesses.append(f"Limited commit history ({analysis.git_metrics.total_commits} commits) - maturity uncertain")
        
        good_msg_ratio = (analysis.git_metrics.good_commit_messages / 
                         max(analysis.git_metrics.total_commits, 1))
        if good_msg_ratio < 0.3:
            weaknesses.append(f"Poor commit message quality ({good_msg_ratio:.0%} are descriptive)")
        
        if analysis.maturity_metrics.error_handling_score < 0.2:
            weaknesses.append("Minimal error handling - production readiness concern")
        
        if not weaknesses:
            weaknesses.append("Minor improvements possible in some areas")
        
        return weaknesses[:6]
    
    def generate_roadmap(self, analysis: AnalysisResult) -> List[RoadmapItem]:
        roadmap = []
        priority = 1
        
        if not analysis.file_structure.key_files_present.get('readme', False):
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Create a comprehensive README.md with project overview, installation instructions, and usage examples",
                effort="Low",
                impact="High",
                rationale="README is the first thing users see and is critical for adoption"
            ))
            priority += 1
        
        if not analysis.testing_metrics.has_test_directory:
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Set up a testing framework and write unit tests for core functionality",
                effort="Medium",
                impact="High",
                rationale="Tests ensure code reliability and facilitate refactoring"
            ))
            priority += 1
        
        if not analysis.testing_metrics.has_ci_cd:
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Configure CI/CD pipeline (GitHub Actions, GitLab CI, or similar) to automate testing",
                effort="Low",
                impact="High",
                rationale="Automated testing prevents regressions and improves code quality"
            ))
            priority += 1
        
        if analysis.code_metrics.comment_ratio < 0.08:
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Add inline comments and docstrings to complex functions and classes",
                effort="Medium",
                impact="Medium",
                rationale="Documentation helps other developers understand and maintain the code"
            ))
            priority += 1
        
        if not analysis.file_structure.key_files_present.get('license', False):
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Add a LICENSE file to clarify usage rights (MIT, Apache 2.0, GPL, etc.)",
                effort="Low",
                impact="Medium",
                rationale="License is essential for open source projects and legal clarity"
            ))
            priority += 1
        
        if analysis.code_metrics.avg_complexity > 15:
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Refactor high-complexity functions into smaller, single-purpose functions",
                effort="High",
                impact="High",
                rationale=f"Average complexity of {analysis.code_metrics.avg_complexity:.1f} indicates maintainability issues"
            ))
            priority += 1
        
        if not analysis.testing_metrics.has_linter_config:
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Add linter configuration (ESLint, Pylint, etc.) to enforce code style",
                effort="Low",
                impact="Medium",
                rationale="Linters catch bugs early and maintain consistent code style"
            ))
            priority += 1
        
        if not analysis.maturity_metrics.has_config_example:
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Create .env.example or config.example files to document required configuration",
                effort="Low",
                impact="Medium",
                rationale="Configuration examples make local setup easier for contributors"
            ))
            priority += 1
        
        good_msg_ratio = (analysis.git_metrics.good_commit_messages / 
                         max(analysis.git_metrics.total_commits, 1))
        if good_msg_ratio < 0.5:
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Adopt conventional commits or a commit message standard (feat:, fix:, docs:, etc.)",
                effort="Low",
                impact="Low",
                rationale="Clear commit messages improve project history and collaboration"
            ))
            priority += 1
        
        if analysis.maturity_metrics.error_handling_score < 0.3:
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Add try-catch blocks and error handling to critical code paths",
                effort="Medium",
                impact="High",
                rationale="Proper error handling prevents crashes and improves user experience"
            ))
            priority += 1
        
        if analysis.file_structure.max_depth > 8:
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Flatten deeply nested directory structure to improve code navigation",
                effort="Medium",
                impact="Low",
                rationale=f"Current depth of {analysis.file_structure.max_depth} levels makes navigation difficult"
            ))
            priority += 1
        
        if not analysis.file_structure.key_files_present.get('contributing', False):
            roadmap.append(RoadmapItem(
                priority=priority,
                action="Add CONTRIBUTING.md to guide new contributors",
                effort="Low",
                impact="Low",
                rationale="Contribution guidelines lower the barrier for external contributions"
            ))
            priority += 1
        
        return roadmap[:8]
    
    def generate_summary(self, analysis: AnalysisResult) -> str:
        tier = analysis.tier
        score = analysis.overall_score
        lang = analysis.repository.primary_language or "multiple languages"
        
        summary_parts = []
        
        summary_parts.append(
            f"This {lang} repository scores {score}/100, placing it in the {tier} tier."
        )
        
        top_dimension = max(analysis.dimension_scores, key=lambda d: d.percentage)
        bottom_dimension = min(analysis.dimension_scores, key=lambda d: d.percentage)
        
        summary_parts.append(
            f"Strongest area is {top_dimension.name} ({top_dimension.percentage:.0%}), "
            f"while {bottom_dimension.name} needs improvement ({bottom_dimension.percentage:.0%})."
        )
        
        if analysis.code_metrics.files_analyzed > 0:
            summary_parts.append(
                f"Code analysis covered {analysis.code_metrics.files_analyzed} files "
                f"with {analysis.code_metrics.total_lines:,} lines of code."
            )
        
        if analysis.testing_metrics.has_test_directory:
            summary_parts.append(
                f"Testing practices are established with {analysis.testing_metrics.test_files_count} test files."
            )
        else:
            summary_parts.append("No testing infrastructure detected.")
        
        if analysis.git_metrics.total_commits >= 10:
            summary_parts.append(
                f"Development history shows {analysis.git_metrics.total_commits} commits "
                f"with {analysis.git_metrics.commit_frequency_trend} recent activity."
            )
        
        feature_count = sum(1 for v in analysis.maturity_metrics.real_world_features.values() if v)
        if feature_count >= 2:
            summary_parts.append(
                f"Project demonstrates {feature_count} production-ready features."
            )
        
        return " ".join(summary_parts)