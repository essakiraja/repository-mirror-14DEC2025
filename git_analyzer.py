import re
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List
from git import Repo
from models import GitMetrics

class GitAnalyzer:
    def __init__(self, git_repo: Repo):
        self.repo = git_repo
    
    def analyze_commit_message(self, message: str) -> bool:
        message = message.strip()
        
        if len(message) < 10:
            return False
        
        poor_patterns = [
            r'^(fix|update|change|add|remove|modify)$',
            r'^(wip|temp|tmp|test)$',
            r'^\.',
            r'^[0-9]+$',
            r'^(asdf|qwer|aaa|bbb)$'
        ]
        
        for pattern in poor_patterns:
            if re.match(pattern, message.lower()):
                return False
        
        good_indicators = [
            r'^(feat|fix|docs|style|refactor|test|chore|perf)(\(.+\))?:',
            len(message.split()) >= 3,
            ':' in message[:50],
        ]
        
        return any(good_indicators)
    
    def calculate_commit_size(self, commit) -> int:
        try:
            stats = commit.stats.total
            return stats['insertions'] + stats['deletions']
        except:
            return 0
    
    def analyze(self) -> GitMetrics:
        commits = list(self.repo.iter_commits())
        total_commits = len(commits)
        
        if total_commits == 0:
            return GitMetrics(
                total_commits=0,
                unique_authors=0,
                avg_commits_per_week=0,
                commit_frequency_trend='unknown',
                avg_commit_message_length=0,
                good_commit_messages=0,
                poor_commit_messages=0,
                total_branches=len(list(self.repo.branches)),
                total_prs=0,
                merge_pr_ratio=0,
                large_commits=0,
                incremental_commits=0
            )
        
        authors = set()
        commit_dates = []
        message_lengths = []
        good_messages = 0
        poor_messages = 0
        large_commits = 0
        incremental_commits = 0
        
        for commit in commits:
            authors.add(commit.author.email)
            commit_dates.append(commit.committed_datetime)
            
            message = commit.message.split('\n')[0]
            message_lengths.append(len(message))
            
            if self.analyze_commit_message(message):
                good_messages += 1
            else:
                poor_messages += 1
            
            commit_size = self.calculate_commit_size(commit)
            if commit_size > 500:
                large_commits += 1
            elif commit_size > 0:
                incremental_commits += 1
        
        commit_dates.sort()
        
        if len(commit_dates) >= 2:
            date_range = (commit_dates[-1] - commit_dates[0]).total_seconds()
            weeks = max(date_range / (7 * 24 * 3600), 1)
            avg_commits_per_week = total_commits / weeks
        else:
            avg_commits_per_week = 0
        
        trend = 'unknown'
        if len(commit_dates) >= 10:
            recent_cutoff = datetime.now() - timedelta(days=30)
            recent_commits = sum(1 for d in commit_dates if d.replace(tzinfo=None) > recent_cutoff)
            
            if recent_commits > total_commits * 0.3:
                trend = 'active'
            elif recent_commits > 0:
                trend = 'moderate'
            else:
                trend = 'inactive'
        
        avg_message_length = sum(message_lengths) / len(message_lengths) if message_lengths else 0
        
        total_branches = len(list(self.repo.branches))
        
        return GitMetrics(
            total_commits=total_commits,
            unique_authors=len(authors),
            avg_commits_per_week=round(avg_commits_per_week, 2),
            commit_frequency_trend=trend,
            avg_commit_message_length=round(avg_message_length, 2),
            good_commit_messages=good_messages,
            poor_commit_messages=poor_messages,
            total_branches=total_branches,
            total_prs=0,
            merge_pr_ratio=0,
            large_commits=large_commits,
            incremental_commits=incremental_commits
        )