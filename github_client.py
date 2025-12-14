import re
from typing import Optional, Tuple
from github import Github, GithubException
from models import RepositoryMetadata
from config import GITHUB_TOKEN

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or GITHUB_TOKEN
        self.client = Github(self.token) if self.token else Github()
    
    def parse_repo_url(self, url: str) -> Tuple[str, str]:
        patterns = [
            r'github\.com[:/]([^/]+)/([^/\.]+)',
            r'^([^/]+)/([^/]+)$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1), match.group(2)
        
        raise ValueError(f"Invalid GitHub repository URL: {url}")
    
    def get_repository_metadata(self, owner: str, repo_name: str) -> RepositoryMetadata:
        try:
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            
            languages = repo.get_languages()
            
            return RepositoryMetadata(
                name=repo.name,
                owner=repo.owner.login,
                url=repo.html_url,
                default_branch=repo.default_branch,
                created_at=repo.created_at,
                updated_at=repo.updated_at,
                stars=repo.stargazers_count,
                forks=repo.forks_count,
                open_issues=repo.open_issues_count,
                size_kb=repo.size,
                primary_language=repo.language,
                languages=languages,
                has_wiki=repo.has_wiki,
                has_issues=repo.has_issues,
                has_projects=repo.has_projects,
                archived=repo.archived
            )
        except GithubException as e:
            raise Exception(f"Failed to fetch repository metadata: {str(e)}")
    
    def get_commit_count(self, owner: str, repo_name: str) -> int:
        try:
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            commits = repo.get_commits()
            return commits.totalCount
        except:
            return 0
    
    def get_branch_count(self, owner: str, repo_name: str) -> int:
        try:
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            branches = repo.get_branches()
            return branches.totalCount
        except:
            return 0
    
    def get_pr_count(self, owner: str, repo_name: str) -> Tuple[int, int]:
        try:
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            open_prs = repo.get_pulls(state='open').totalCount
            closed_prs = repo.get_pulls(state='closed').totalCount
            return open_prs, closed_prs
        except:
            return 0, 0
    
    def check_rate_limit(self) -> dict:
        rate_limit = self.client.get_rate_limit()
        return {
            'core': {
                'remaining': rate_limit.core.remaining,
                'limit': rate_limit.core.limit,
                'reset': rate_limit.core.reset
            }
        }