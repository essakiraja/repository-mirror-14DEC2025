import sys
from datetime import datetime
from github_client import GitHubClient
from repo_cloner import RepositoryCloner
from structure_analyzer import StructureAnalyzer
from code_analyzer import CodeAnalyzer
from git_analyzer import GitAnalyzer
from testing_maturity_analyzer import TestingMaturityAnalyzer
from scoring_engine import ScoringEngine
from insight_generator import InsightGenerator
from models import AnalysisResult

class RepositoryMirror:
    def __init__(self, github_token: str = None):
        self.github_client = GitHubClient(github_token)
        self.scoring_engine = ScoringEngine()
        self.insight_generator = InsightGenerator()
    
    def analyze(self, repo_url: str) -> AnalysisResult:
        print(f"Analyzing repository: {repo_url}")
        
        owner, repo_name = self.github_client.parse_repo_url(repo_url)
        print(f"  Owner: {owner}, Repository: {repo_name}")
        
        print("Fetching repository metadata...")
        repo_metadata = self.github_client.get_repository_metadata(owner, repo_name)
        
        with RepositoryCloner() as cloner:
            print("Cloning repository...")
            repo_path = cloner.clone(repo_url)
            git_repo = cloner.get_git_repo()
            
            print("Analyzing file structure...")
            structure_analyzer = StructureAnalyzer(repo_path)
            file_structure = structure_analyzer.analyze()
            
            print("Analyzing code metrics...")
            code_analyzer = CodeAnalyzer(repo_path, repo_metadata.primary_language)
            code_metrics = code_analyzer.analyze()
            
            print("Analyzing git history...")
            git_analyzer = GitAnalyzer(git_repo)
            git_metrics = git_analyzer.analyze()
            
            print("Analyzing testing and maturity...")
            test_maturity_analyzer = TestingMaturityAnalyzer(
                repo_path, 
                repo_metadata.primary_language
            )
            testing_metrics = test_maturity_analyzer.analyze_testing()
            maturity_metrics = test_maturity_analyzer.analyze_maturity()
        
        print("Calculating scores...")
        dimension_scores = []
        
        code_quality_score = self.scoring_engine.score_code_quality(code_metrics)
        dimension_scores.append(code_quality_score)
        
        structure_score = self.scoring_engine.score_structure_modularity(file_structure)
        dimension_scores.append(structure_score)
        
        doc_score = self.scoring_engine.score_documentation(file_structure)
        dimension_scores.append(doc_score)
        
        testing_score = self.scoring_engine.score_testing_maintainability(
            testing_metrics, code_metrics
        )
        dimension_scores.append(testing_score)
        
        git_score = self.scoring_engine.score_git_practices(git_metrics)
        dimension_scores.append(git_score)
        
        readiness_score = self.scoring_engine.score_real_world_readiness(
            maturity_metrics, file_structure
        )
        dimension_scores.append(readiness_score)
        
        overall_score = self.scoring_engine.calculate_overall_score(dimension_scores)
        tier = self.scoring_engine.determine_tier(overall_score)
        confidence = self.scoring_engine.determine_confidence(
            file_structure.total_files,
            git_metrics.total_commits
        )
        
        print("Generating insights...")
        analysis = AnalysisResult(
            repository=repo_metadata,
            file_structure=file_structure,
            code_metrics=code_metrics,
            git_metrics=git_metrics,
            testing_metrics=testing_metrics,
            maturity_metrics=maturity_metrics,
            dimension_scores=dimension_scores,
            overall_score=overall_score,
            tier=tier,
            confidence=confidence,
            strengths=[],
            weaknesses=[]
        )
        
        analysis.strengths = self.insight_generator.generate_strengths(analysis)
        analysis.weaknesses = self.insight_generator.generate_weaknesses(analysis)
        
        print("Analysis complete!")
        return analysis
    
    def generate_output(self, analysis: AnalysisResult) -> dict:
        summary = self.insight_generator.generate_summary(analysis)
        roadmap_items = self.insight_generator.generate_roadmap(analysis)
        
        roadmap = [
            {
                "priority": item.priority,
                "action": item.action,
                "effort": item.effort,
                "impact": item.impact,
                "rationale": item.rationale
            }
            for item in roadmap_items
        ]
        
        dimension_details = {}
        for dim in analysis.dimension_scores:
            dimension_details[dim.name] = {
                "score": dim.score,
                "max_score": dim.max_score,
                "percentage": dim.percentage,
                "weight": dim.weight,
                "weighted_score": dim.weighted_score,
                "reasoning": dim.reasoning,
                "signals": dim.signals
            }
        
        return {
            "score": analysis.overall_score,
            "tier": analysis.tier,
            "confidence": analysis.confidence,
            "summary": summary,
            "strengths": analysis.strengths,
            "weaknesses": analysis.weaknesses,
            "roadmap": roadmap,
            "metadata": {
                "repository": {
                    "name": analysis.repository.name,
                    "owner": analysis.repository.owner,
                    "url": analysis.repository.url,
                    "primary_language": analysis.repository.primary_language,
                    "stars": analysis.repository.stars,
                    "forks": analysis.repository.forks
                },
                "metrics": {
                    "total_files": analysis.file_structure.total_files,
                    "code_files": analysis.file_structure.total_code_files,
                    "total_commits": analysis.git_metrics.total_commits,
                    "total_lines": analysis.code_metrics.total_lines,
                    "functions": analysis.code_metrics.functions_count,
                    "avg_complexity": analysis.code_metrics.avg_complexity
                },
                "dimensions": dimension_details,
                "analyzed_at": analysis.timestamp.isoformat()
            }
        }