import os
import shutil
import tempfile
from pathlib import Path
from git import Repo, GitCommandError

class RepositoryCloner:
    def __init__(self, clone_dir: str = None):
        self.clone_dir = clone_dir or tempfile.mkdtemp(prefix='repo_mirror_')
        self.repo_path = None
        self.git_repo = None
    
    def clone(self, url: str, depth: int = 1) -> str:
        try:
            repo_name = url.rstrip('/').split('/')[-1].replace('.git', '')
            self.repo_path = os.path.join(self.clone_dir, repo_name)
            
            if os.path.exists(self.repo_path):
                shutil.rmtree(self.repo_path)
            
            self.git_repo = Repo.clone_from(
                url,
                self.repo_path,
                depth=None
            )
            
            return self.repo_path
        except GitCommandError as e:
            raise Exception(f"Failed to clone repository: {str(e)}")
    
    def get_repo_path(self) -> str:
        return self.repo_path
    
    def get_git_repo(self) -> Repo:
        return self.git_repo
    
    def cleanup(self):
        if self.repo_path and os.path.exists(self.repo_path):
            try:
                shutil.rmtree(self.repo_path)
            except Exception as e:
                print(f"Warning: Failed to cleanup directory {self.repo_path}: {e}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()