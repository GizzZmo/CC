# GitHub CI/CD Workflows

This directory contains the comprehensive CI/CD workflow system for the Cyberchess project.

## Overview

Our CI/CD system is designed to ensure code quality, reliability, and smooth releases. All workflows are automatically triggered by relevant events (push, pull request, schedule, etc.).

## Workflows

### Core CI/CD Workflows

#### 1. CI (`ci.yml`)
**Triggers:** Push and PR to `main` and `develop` branches
**Purpose:** Main continuous integration workflow that tests the application across multiple Python versions

**What it does:**
- Tests on Python 3.7, 3.8, 3.9, 3.10, 3.11, and 3.12
- Installs dependencies from requirements.txt
- Runs the automated test suite (`test_features.py`)
- Validates all demo scripts (`demo.py`, `demo_advanced.py`)
- Verifies opening book and puzzle modules
- Uses pip caching for faster builds

**Status Badge:**
```markdown
[![CI](https://github.com/GizzZmo/CC/workflows/CI/badge.svg)](https://github.com/GizzZmo/CC/actions/workflows/ci.yml)
```

#### 2. Code Quality (`code-quality.yml`)
**Triggers:** Push and PR to `main` and `develop` branches
**Purpose:** Enforce code quality standards and detect potential issues

**What it does:**
- Runs flake8 for Python linting (syntax errors, undefined names)
- Checks code formatting with black
- Verifies import sorting with isort
- Runs security checks with bandit
- All checks are non-blocking to provide feedback without failing builds

**Status Badge:**
```markdown
[![Code Quality](https://github.com/GizzZmo/CC/workflows/Code%20Quality/badge.svg)](https://github.com/GizzZmo/CC/actions/workflows/code-quality.yml)
```

#### 3. Build (`build.yml`)
**Triggers:** Push and PR to `main` and `develop` branches
**Purpose:** Verify the build process and create distributable packages

**What it does:**
- Runs the build script (`build.py`)
- Verifies build artifacts are created correctly
- Uploads build artifacts for 30 days
- Generates build summary in GitHub Actions UI

**Status Badge:**
```markdown
[![Build](https://github.com/GizzZmo/CC/workflows/Build/badge.svg)](https://github.com/GizzZmo/CC/actions/workflows/build.yml)
```

#### 4. Matrix Tests (`matrix-tests.yml`)
**Triggers:** Push to `main`, PR to `main`, weekly schedule (Sundays at 3 AM UTC)
**Purpose:** Comprehensive testing across different operating systems and Python versions

**What it does:**
- Tests on Ubuntu, macOS, and Windows
- Tests on Python 3.8, 3.10, and 3.12
- Ensures cross-platform compatibility
- Runs weekly to catch platform-specific issues

### Release & Deployment

#### 5. Release (`release.yml`)
**Triggers:** Push of version tags (e.g., `v1.0.0`)
**Purpose:** Automate the release process

**What it does:**
- Extracts version information from tags
- Runs the build script to create release artifacts
- Generates release notes from CHANGELOG.md
- Creates a GitHub Release with artifacts
- Uploads release artifacts with 90-day retention

**How to create a release:**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Code Quality & Maintenance

#### 6. Dependency Check (`dependency-check.yml`)
**Triggers:** Weekly schedule (Mondays at 9 AM UTC), manual trigger
**Purpose:** Monitor dependencies for security vulnerabilities and updates

**What it does:**
- Checks for security vulnerabilities with pip-audit
- Lists outdated packages
- Generates dependency report
- Runs weekly to stay up-to-date with security patches

#### 7. Documentation (`documentation.yml`)
**Triggers:** Push/PR affecting `.md` files
**Purpose:** Ensure documentation quality

**What it does:**
- Lints Markdown files
- Checks for broken links
- Runs spell checking with typos
- Only runs when documentation files change

**Status Badge:**
```markdown
[![Documentation](https://github.com/GizzZmo/CC/workflows/Documentation/badge.svg)](https://github.com/GizzZmo/CC/actions/workflows/documentation.yml)
```

### Pull Request Workflows

#### 8. PR Validation (`pr-validation.yml`)
**Triggers:** Pull request events (opened, synchronized, reopened)
**Purpose:** Automated PR validation and quality checks

**What it does:**
- Validates PR title follows semantic conventions
- Detects changed Python files
- Runs tests only on changed code
- Checks code complexity with radon
- Measures test coverage
- Verifies no merge conflicts
- Generates detailed PR summary

#### 9. Auto Label (`auto-label.yml`)
**Triggers:** PRs and issues (opened, edited, synchronized)
**Purpose:** Automatically label PRs and issues based on content

**What it does:**
- Labels PRs based on changed files (uses `.github/labeler.yml`)
- Adds size labels (xs, s, m, l, xl) based on changes
- Labels issues as bug/enhancement based on content
- Helps with project organization

**Label categories:**
- `documentation` - Documentation changes
- `tests` - Test file changes
- `python` - Python code changes
- `ci` - CI/CD changes
- `dependencies` - Dependency updates
- `game-logic` - Core game files
- `features` - Feature modules
- `build` - Build script changes

### Community & Automation

#### 10. Greetings (`greetings.yml`)
**Triggers:** First-time issue or PR from a contributor
**Purpose:** Welcome new contributors

**What it does:**
- Sends welcome message to first-time issue creators
- Sends welcome message to first-time PR creators
- Provides helpful guidelines and links

#### 11. Stale (`stale.yml`)
**Triggers:** Daily schedule (1 AM UTC)
**Purpose:** Manage inactive issues and PRs

**What it does:**
- Marks issues stale after 60 days of inactivity
- Closes stale issues after 7 more days
- Marks PRs stale after 45 days of inactivity
- Closes stale PRs after 14 more days
- Exempts pinned, security, and WIP items
- Removes stale label when updated

## Configuration Files

### `.github/labeler.yml`
Configuration for automatic PR labeling based on changed files.

### `.github/markdown-link-check-config.json`
Configuration for the Markdown link checker (timeout, retries, ignored patterns).

### `.github/CODEOWNERS`
Defines code ownership for automatic reviewer assignment.

### `.github/ISSUE_TEMPLATE/`
Issue templates for:
- Bug reports
- Feature requests
- Questions

### `.github/PULL_REQUEST_TEMPLATE/`
Pull request template with checklist for contributors.

## Workflow Dependencies

Workflows use the following GitHub Actions:

- `actions/checkout@v4` - Checkout repository code
- `actions/setup-python@v5` - Set up Python environment
- `actions/upload-artifact@v4` - Upload build artifacts
- `actions/stale@v9` - Stale issue/PR management
- `actions/labeler@v5` - Auto-label PRs
- `actions/first-interaction@v1` - Greet first-time contributors
- `actions/github-script@v7` - Run custom GitHub API scripts
- `softprops/action-gh-release@v1` - Create GitHub releases
- `DavidAnson/markdownlint-cli2-action@v14` - Lint Markdown
- `gaurav-nelson/github-action-markdown-link-check@v1` - Check Markdown links
- `crate-ci/typos@master` - Spell checking
- `tj-actions/changed-files@v41` - Detect changed files
- `amannn/action-semantic-pull-request@v5` - Validate PR titles
- `codelytv/pr-size-labeler@v1` - Label PR size

## Local Testing

To test the workflows locally before pushing:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests:**
   ```bash
   python test_features.py
   ```

3. **Run demos:**
   ```bash
   python demo.py
   python demo_advanced.py
   ```

4. **Check code quality:**
   ```bash
   pip install flake8 black isort bandit
   flake8 .
   black --check .
   isort --check-only .
   bandit -r . -ll
   ```

5. **Test build:**
   ```bash
   python build.py
   ```

## Maintenance

### Adding a New Workflow

1. Create a new `.yml` file in `.github/workflows/`
2. Define triggers, jobs, and steps
3. Test the workflow by pushing to a feature branch
4. Update this README with workflow documentation

### Updating Workflows

When updating workflows:
1. Test changes on a feature branch first
2. Monitor workflow runs for any errors
3. Update documentation if behavior changes
4. Consider backward compatibility

### Monitoring

- Check the [Actions tab](https://github.com/GizzZmo/CC/actions) regularly
- Review failed workflows and fix issues promptly
- Monitor dependency check results weekly
- Review and respond to stale issue/PR notifications

## Best Practices

1. **Keep workflows focused:** Each workflow should have a single, clear purpose
2. **Use caching:** Leverage pip caching to speed up workflows
3. **Fail gracefully:** Use `continue-on-error` for non-critical checks
4. **Provide feedback:** Generate summaries and reports in `$GITHUB_STEP_SUMMARY`
5. **Be mindful of costs:** Optimize workflows to reduce unnecessary runs
6. **Version pin actions:** Use specific versions (e.g., `@v4`) for stability
7. **Test locally first:** Always test changes locally before relying on CI

## Troubleshooting

### Workflow Fails on Python Version X
- Check if dependencies support that Python version
- Review the specific error in the workflow logs
- Consider excluding unsupported Python versions

### Build Artifacts Missing
- Verify `build.py` completes successfully
- Check artifact upload step logs
- Ensure paths in `upload-artifact` are correct

### Flake8/Black Errors
- Run the tools locally to see full output
- Fix errors or update configuration
- Consider using `continue-on-error: true` for gradual adoption

### Stale Bot Too Aggressive
- Adjust `days-before-*-stale` values in `stale.yml`
- Add labels to exempt items from stale bot
- Use `pinned` label for important issues

## Contributing

When contributing to workflows:
1. Test changes thoroughly
2. Document new workflows in this README
3. Follow existing patterns and conventions
4. Consider impact on CI costs and performance

## Questions?

For questions about the CI/CD system, please:
- Check the [GitHub Actions documentation](https://docs.github.com/en/actions)
- Open an issue with the `ci` label
- Review workflow run logs for specific errors

---

*Last Updated: December 2025*
