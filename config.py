import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

SCORING_WEIGHTS = {
    'code_quality': 0.30,
    'structure_modularity': 0.20,
    'documentation': 0.15,
    'testing_maintainability': 0.15,
    'git_practices': 0.10,
    'real_world_readiness': 0.10
}

KEY_FILES = {
    'readme': ['README.md', 'readme.md', 'README.rst', 'README.txt'],
    'license': ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'COPYING'],
    'gitignore': ['.gitignore'],
    'contributing': ['CONTRIBUTING.md', 'CONTRIBUTING.rst'],
    'changelog': ['CHANGELOG.md', 'CHANGELOG.rst', 'HISTORY.md'],
    'code_of_conduct': ['CODE_OF_CONDUCT.md']
}

TEST_INDICATORS = [
    'test', 'tests', '__tests__', 'spec', 'specs',
    'test_', '_test', '.test.', '.spec.'
]

PACKAGE_MANAGERS = {
    'python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', 'poetry.lock'],
    'javascript': ['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'],
    'ruby': ['Gemfile', 'Gemfile.lock'],
    'java': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
    'go': ['go.mod', 'go.sum'],
    'rust': ['Cargo.toml', 'Cargo.lock'],
    'php': ['composer.json', 'composer.lock']
}

LINTER_CONFIGS = {
    'python': ['.pylintrc', 'pylint.rc', '.flake8', 'setup.cfg', 'tox.ini', '.ruff.toml'],
    'javascript': ['.eslintrc', '.eslintrc.js', '.eslintrc.json', '.eslintrc.yml', 'eslint.config.js'],
    'typescript': ['tsconfig.json', 'tslint.json'],
    'ruby': ['.rubocop.yml'],
    'go': ['.golangci.yml', '.golangci.yaml']
}

CONFIG_FILES = [
    '.env.example', '.env.sample', '.env.template',
    'config.example.js', 'config.example.json',
    'config.sample.js', 'config.sample.json'
]

REAL_WORLD_INDICATORS = {
    'api': ['api', 'routes', 'controllers', 'endpoints', 'rest', 'graphql'],
    'database': ['models', 'migrations', 'schema', 'database', 'db'],
    'auth': ['auth', 'authentication', 'authorization', 'login', 'jwt', 'oauth'],
    'deployment': ['Dockerfile', 'docker-compose.yml', '.dockerignore', 'k8s', 'kubernetes'],
    'ci_cd': ['.github/workflows', '.gitlab-ci.yml', '.travis.yml', 'Jenkinsfile', '.circleci']
}

TIER_THRESHOLDS = {
    'advanced': 80,
    'intermediate': 60,
    'beginner': 0
}

CONFIDENCE_THRESHOLDS = {
    'high': {'min_files': 10, 'min_commits': 5},
    'medium': {'min_files': 3, 'min_commits': 2},
    'low': {'min_files': 0, 'min_commits': 0}
}

EXCLUDED_DIRS = [
    '.git', 'node_modules', '__pycache__', '.pytest_cache',
    'venv', 'env', '.venv', 'virtualenv',
    'dist', 'build', 'target', 'out',
    '.idea', '.vscode', '.DS_Store',
    'coverage', '.nyc_output', 'vendor'
]

EXCLUDED_EXTENSIONS = [
    '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
    '.exe', '.bin', '.dat', '.db', '.sqlite',
    '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
    '.pdf', '.zip', '.tar', '.gz', '.rar',
    '.lock', '.log', '.tmp', '.cache'
]

CODE_EXTENSIONS = {
    'python': ['.py'],
    'javascript': ['.js', '.jsx', '.mjs', '.cjs'],
    'typescript': ['.ts', '.tsx'],
    'java': ['.java'],
    'cpp': ['.cpp', '.cc', '.cxx', '.h', '.hpp'],
    'c': ['.c', '.h'],
    'csharp': ['.cs'],
    'go': ['.go'],
    'rust': ['.rs'],
    'ruby': ['.rb'],
    'php': ['.php'],
    'swift': ['.swift'],
    'kotlin': ['.kt', '.kts']
}