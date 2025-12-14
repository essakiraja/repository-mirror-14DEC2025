from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class RepositoryMetadata:
    name: str
    owner: str
    url: str
    default_branch: str
    created_at: datetime
    updated_at: datetime
    stars: int
    forks: int
    open_issues: int
    size_kb: int
    primary_language: Optional[str]
    languages: Dict[str, int]
    has_wiki: bool
    has_issues: bool
    has_projects: bool
    archived: bool

@dataclass
class FileStructure:
    total_files: int
    total_code_files: int
    max_depth: int
    avg_depth: float
    directories: int
    key_files_present: Dict[str, bool]
    file_types: Dict[str, int]
    largest_files: List[tuple]

@dataclass
class CodeMetrics:
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    avg_file_length: float
    avg_function_length: float
    comment_ratio: float
    files_analyzed: int
    functions_count: int
    classes_count: int
    avg_complexity: float
    max_complexity: int
    complexity_distribution: Dict[str, int]

@dataclass
class GitMetrics:
    total_commits: int
    unique_authors: int
    avg_commits_per_week: float
    commit_frequency_trend: str
    avg_commit_message_length: float
    good_commit_messages: int
    poor_commit_messages: int
    total_branches: int
    total_prs: int
    merge_pr_ratio: float
    large_commits: int
    incremental_commits: int

@dataclass
class TestingMetrics:
    has_test_directory: bool
    test_files_count: int
    test_to_code_ratio: float
    has_ci_cd: bool
    ci_cd_tools: List[str]
    has_linter_config: bool
    linter_tools: List[str]

@dataclass
class MaturityMetrics:
    has_package_manager: bool
    package_managers: List[str]
    has_config_example: bool
    has_deployment_config: bool
    deployment_tools: List[str]
    real_world_features: Dict[str, bool]
    error_handling_score: float

@dataclass
class DimensionScore:
    name: str
    score: float
    max_score: float
    percentage: float
    weight: float
    weighted_score: float
    signals: Dict[str, any]
    reasoning: str

@dataclass
class AnalysisResult:
    repository: RepositoryMetadata
    file_structure: FileStructure
    code_metrics: CodeMetrics
    git_metrics: GitMetrics
    testing_metrics: TestingMetrics
    maturity_metrics: MaturityMetrics
    dimension_scores: List[DimensionScore]
    overall_score: float
    tier: str
    confidence: str
    strengths: List[str]
    weaknesses: List[str]
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class RoadmapItem:
    priority: int
    action: str
    effort: str
    impact: str
    rationale: str

@dataclass
class FinalOutput:
    score: float
    tier: str
    confidence: str
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    roadmap: List[Dict[str, any]]
    metadata: Dict[str, any]