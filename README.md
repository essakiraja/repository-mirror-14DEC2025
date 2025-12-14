# Repository Mirror - MVP

A deterministic-first, AI-assisted repository analysis system that scores GitHub repositories on a 0-100 scale with actionable improvement roadmaps.

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                  Repository Mirror                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Data Collection Layer                    │  │
│  │  - GitHub API Client (metadata, stats)           │  │
│  │  - Repository Cloner (git operations)            │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                               │
│                         ▼                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Analysis Engines (Deterministic)         │  │
│  │  - Structure Analyzer (files, depth, org)        │  │
│  │  - Code Analyzer (metrics, complexity)           │  │
│  │  - Git Analyzer (commits, messages)              │  │
│  │  - Testing/Maturity Analyzer                     │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                               │
│                         ▼                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Scoring Engine (Rule-Based)              │  │
│  │  - Weighted dimension scoring                    │  │
│  │  - Threshold-based evaluation                    │  │
│  │  - Signal aggregation                            │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                               │
│                         ▼                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Insight Generator                        │  │
│  │  - Strengths/Weaknesses extraction               │  │
│  │  - Roadmap generation                            │  │
│  │  - Summary synthesis                             │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Module Structure

```
repository-mirror/
├── config.py                      # Constants, weights, thresholds
├── models.py                      # Data classes for all entities
├── github_client.py               # GitHub API interactions
├── repo_cloner.py                 # Git clone operations
├── structure_analyzer.py          # File structure analysis
├── code_analyzer.py               # Code metrics (complexity, lines)
├── git_analyzer.py                # Git history analysis
├── testing_maturity_analyzer.py   # Testing & maturity signals
├── scoring_engine.py              # Deterministic scoring logic
├── insight_generator.py           # Strengths, weaknesses, roadmap
├── repository_mirror.py           # Main orchestrator
├── main.py                        # CLI interface
└── requirements.txt               # Dependencies
```

## Installation

### Prerequisites

- Python 3.8+
- Git installed and accessible in PATH
- GitHub personal access token (optional, for higher rate limits)

### Setup

```bash
# Clone or create project directory
mkdir repository-mirror
cd repository-mirror

# Install dependencies
pip install -r requirements.txt

# Optional: Set GitHub token for higher API rate limits
export GITHUB_TOKEN="your_github_token_here"
```

## Usage

### Basic Usage

```bash
python main.py https://github.com/user/repository
```

### Save Results to File

```bash
python main.py https://github.com/user/repository --output results.json
```

### Quiet Mode (No Console Output)

```bash
python main.py https://github.com/user/repository --quiet --output results.json
```

### With GitHub Token

```bash
python main.py https://github.com/user/repository --token YOUR_TOKEN
```

## Scoring Rubric

### Dimension Weights

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Code Quality | 30% | Comment ratio, complexity, file/function length |
| Structure & Modularity | 20% | File organization, depth, modularity |
| Documentation | 15% | README, LICENSE, CONTRIBUTING, other docs |
| Testing & Maintainability | 15% | Tests, CI/CD, linters |
| Git Practices | 10% | Commit history, message quality, branching |
| Real-World Readiness | 10% | Package managers, config, deployment, features |

### Code Quality (30%)

**Signals:**
- Comment-to-code ratio (15-25 points)
  - Excellent: ≥15% → 25 points
  - Adequate: ≥8% → 15 points
  - Poor: <8% → 5 points
- Average cyclomatic complexity (20-30 points)
  - Low: ≤5 → 30 points
  - Moderate: ≤10 → 20 points
  - High: >10 → 10 points
- Average file length (12-20 points)
  - Optimal: ≤300 lines → 20 points
  - Acceptable: ≤500 lines → 12 points
  - Long: >500 lines → 5 points
- Average function length (10-15 points)
  - Optimal: ≤30 lines → 15 points
  - Acceptable: ≤50 lines → 10 points
  - Long: >50 lines → 3 points

**Penalties:**
- Max complexity >20: -10 points
- >20% functions with high complexity: -5 points

### Structure & Modularity (20%)

**Signals:**
- File count (15-25 points)
  - Optimal: 5-50 files → 25 points
  - Good: 51-100 files → 20 points
  - Large: >200 files → 10 points
- Directory depth (15-25 points)
  - Optimal: 2-5 levels → 25 points
  - Acceptable: 6-7 levels → 18 points
  - Too deep: >10 levels → 8 points
- Code file ratio (8-20 points)
  - High: ≥60% → 20 points
  - Moderate: ≥30% → 15 points
  - Low: <30% → 8 points
- Organization (3-15 points)
  - Multiple directories: 15 points
  - Some directories: 10 points
  - Flat structure: 3 points
- Extension diversity (5-15 points)
  - High: ≥5 types → 15 points
  - Moderate: ≥3 types → 10 points
  - Low: <3 types → 5 points

### Documentation (15%)

**Signals:**
- README.md: 40 points (critical)
- LICENSE: 20 points
- CONTRIBUTING.md: 15 points
- CHANGELOG: 10 points
- CODE_OF_CONDUCT: 10 points
- Additional docs: 3-5 points

### Testing & Maintainability (15%)

**Signals:**
- Test directory exists: 25 points
- Test-to-code ratio (8-25 points)
  - Excellent: ≥30% → 25 points
  - Good: ≥15% → 15 points
  - Low: >0% → 8 points
  - None: 0 points
- CI/CD configured: 20 points
- Linter configured: 15 points
- Low complexity bonus: 5-15 points

### Git Practices (10%)

**Signals:**
- Commit count (5-20 points)
  - High: ≥20 commits → 20 points
  - Moderate: ≥10 commits → 15 points
  - Low: ≥5 commits → 10 points
  - Very low: <5 commits → 5 points
- Commit message quality (5-25 points)
  - Excellent: ≥70% good → 25 points
  - Good: ≥50% good → 18 points
  - Moderate: ≥30% good → 10 points
  - Poor: <30% good → 5 points
- Activity trend (5-20 points)
  - Active: 20 points
  - Moderate: 12 points
  - Inactive: 5 points
- Incremental development (5-20 points)
  - High incremental: 20 points
  - Mixed: 12 points
  - Large commits: 5 points
- Branching: 15 points (if >1 branch)

### Real-World Readiness (10%)

**Signals:**
- Package manager configured: 25 points
- .gitignore present: 10 points
- Config examples (.env.example): 15 points
- Production features (10-25 points)
  - ≥3 features: 25 points
  - ≥2 features: 18 points
  - ≥1 feature: 10 points
  - Features: API, database, auth, deployment, CI/CD
- Error handling (5-15 points)
  - Excellent: ≥60% files → 15 points
  - Adequate: ≥30% files → 10 points
  - Minimal: >0% → 5 points
- Deployment config: 10 points

### Tier Classification

| Score | Tier | Characteristics |
|-------|------|-----------------|
| 80-100 | Advanced | Production-ready, comprehensive testing, excellent practices |
| 60-79 | Intermediate | Solid foundation, some gaps, actively maintained |
| 0-59 | Beginner | Learning project, missing fundamentals, needs improvement |

### Confidence Levels

| Level | Criteria |
|-------|----------|
| High | ≥10 files AND ≥5 commits |
| Medium | ≥3 files AND ≥2 commits |
| Low | <3 files OR <2 commits |

## Output Format

### JSON Structure

```json
{
  "score": 78,
  "tier": "Intermediate",
  "confidence": "High",
  "summary": "Specific evaluation based on actual metrics",
  "strengths": [
    "Dimension-specific strengths with evidence"
  ],
  "weaknesses": [
    "Concrete areas needing improvement"
  ],
  "roadmap": [
    {
      "priority": 1,
      "action": "Specific, actionable improvement step",
      "effort": "Low | Medium | High",
      "impact": "Low | Medium | High",
      "rationale": "Why this matters and what it addresses"
    }
  ],
  "metadata": {
    "repository": { "name": "...", "owner": "...", "..." },
    "metrics": { "total_files": 0, "..." },
    "dimensions": { "Code Quality": { "score": 0, "..." } },
    "analyzed_at": "2025-01-15T12:00:00"
  }
}
```

### Console Output

The CLI provides a formatted summary including:
- Overall score, tier, and confidence
- Dimension breakdown with visual bars
- Top strengths (up to 5)
- Key weaknesses (up to 6)
- Prioritized improvement roadmap (top 5)

## Example Run

### Command

```bash
python main.py https://github.com/expressjs/express --output express_analysis.json
```

### Expected Output

```
╔══════════════════════════════════════════════════════════╗
║              REPOSITORY MIRROR - MVP v1.0                ║
║     Deterministic Repository Analysis & Scoring System   ║
╚══════════════════════════════════════════════════════════╝

Analyzing repository: https://github.com/expressjs/express
  Owner: expressjs, Repository: express
Fetching repository metadata...
Cloning repository...
Analyzing file structure...
Analyzing code metrics...
Analyzing git history...
Analyzing testing and maturity...
Calculating scores...
Generating insights...
Analysis complete!

======================================================================
ANALYSIS RESULTS
======================================================================

Repository: express
Owner: expressjs
Language: JavaScript

──────────────────────────────────────────────────────────────────────
OVERALL SCORE: 85/100
TIER: Advanced
CONFIDENCE: High
──────────────────────────────────────────────────────────────────────

This JavaScript repository scores 85/100, placing it in the Advanced tier...

──────────────────────────────────────────────────────────────────────
DIMENSION SCORES:
──────────────────────────────────────────────────────────────────────
  Code Quality                   [████████████████████████░░░░░░] 82% (24.6/100)
  Structure & Modularity         [███████████████████████████░░░] 91% (18.2/100)
  Documentation                  [██████████████████████████████] 100% (15.0/100)
  Testing & Maintainability      [██████████████████████░░░░░░░░] 75% (11.3/100)
  Git Practices                  [███████████████████████████░░░] 88% (8.8/100)
  Real-World Readiness           [████████████████████████████░░] 95% (9.5/100)

...
```

## Language Support

### Currently Supported

- **Python** (.py)
  - Metrics: Complexity, functions, lines
  - Linters: pylint, flake8, ruff
  - Package managers: pip, poetry, pipenv
  
- **JavaScript/TypeScript** (.js, .jsx, .ts, .tsx)
  - Metrics: Complexity, functions, lines
  - Linters: ESLint, TSLint
  - Package managers: npm, yarn, pnpm

### Adding New Languages

To extend support for additional languages:

1. **Update `config.py`:**
   ```python
   CODE_EXTENSIONS = {
       'your_language': ['.ext1', '.ext2'],
       ...
   }
   
   LINTER_CONFIGS = {
       'your_language': ['linter_config_file'],
       ...
   }
   
   PACKAGE_MANAGERS = {
       'your_language': ['package_file1', 'package_file2'],
       ...
   }
   ```

2. **Test with sample repositories** to validate metrics extraction

3. **Adjust scoring thresholds** if language-specific patterns differ significantly

## Known Limitations

### Current Limitations

1. **Shallow Analysis:**
   - Complexity metrics are approximations (lizard tool limitations)
   - No semantic code analysis
   - Cannot detect code smells or anti-patterns
   
2. **Language Coverage:**
   - Deep analysis only for Python/JavaScript
   - Other languages have basic metrics only
   - No language-specific best practices

3. **Test Coverage:**
   - Cannot measure actual test coverage percentage
   - Only detects presence of test files
   - Cannot determine test quality

4. **Git Analysis:**
   - No PR analysis (requires authenticated API calls)
   - Cannot determine code review practices
   - Limited branch analysis

5. **Documentation Quality:**
   - Only checks presence, not content quality
   - Cannot assess README completeness
   - No analysis of code comments content

6. **Performance:**
   - Clones entire repository (can be slow for large repos)
   - No caching mechanism
   - Single-threaded analysis

### Future Improvements

**Phase 2 - Enhanced Analysis:**
- Add AST-based semantic analysis
- Implement code smell detection
- Add dependency analysis (security, outdated)
- Support for monorepos

**Phase 3 - AI Integration:**
- LLM-based code quality assessment
- Intelligent roadmap prioritization
- Natural language summaries
- Comparative analysis against similar projects

**Phase 4 - Advanced Features:**
- Real test coverage measurement
- Performance benchmarking
- Security vulnerability scanning
- Technical debt estimation
- Historical trend analysis

**Phase 5 - Platform:**
- Web interface
- Batch analysis
- Repository comparison
- Team/organization analytics
- API endpoint

## Technical Decisions

### Why Deterministic-First?

1. **Reproducibility:** Same repository always produces same score
2. **Explainability:** Every point is traceable to specific metrics
3. **Trust:** No black-box AI scoring
4. **Debugging:** Easy to identify why scores change
5. **Cost:** No API costs for core functionality

### Why These Weights?

- **Code Quality (30%):** Most impactful for maintainability
- **Structure (20%):** Critical for scalability
- **Documentation (15%):** Essential for adoption
- **Testing (15%):** Ensures reliability
- **Git (10%):** Reflects development discipline
- **Real-World (10%):** Indicates practical maturity

### Why Lizard for Complexity?

- Language-agnostic
- No compilation required
- Fast analysis
- Reasonable accuracy for MVP

### Scoring Methodology

All scores use **additive point systems** with:
- Clear thresholds based on industry standards
- Penalties for anti-patterns
- Bonuses for excellence
- Normalization to 0-100 scale

## Contributing

Areas for contribution:
- Additional language support
- Enhanced complexity metrics
- Better commit message analysis
- Documentation quality scoring
- Test quality metrics

## License

MIT License - See LICENSE file for details

## Authors

Repository Mirror MVP - Built as a production-grade evaluation system
