# Git Setup Guide

## ✅ `.gitignore` Created

A comprehensive `.gitignore` file has been added to protect sensitive information and keep your repository clean.

## 🔒 What's Protected

### Critical (Security)
- ✅ `.env` - **Contains your API keys** (never committed)
- ✅ `app.log` - May contain sensitive data
- ✅ `uploads/` - User-uploaded images
- ✅ `results/` - Test results

### Build Artifacts
- ✅ `venv/` - Python virtual environment
- ✅ `node_modules/` - Node dependencies
- ✅ `__pycache__/` - Python bytecode
- ✅ `*.pyc`, `*.pyo` - Compiled Python files

### IDE & OS Files
- ✅ `.vscode/`, `.idea/` - IDE settings
- ✅ `.DS_Store` - macOS metadata
- ✅ `Thumbs.db` - Windows thumbnails

## 📝 What's Safe to Commit

### Source Code
- ✅ All `.py` files
- ✅ All `.jsx`, `.css` files
- ✅ `requirements.txt`
- ✅ `package.json`

### Configuration (Safe)
- ✅ `.env.example` - Template with placeholders
- ✅ `.gitignore` - This file
- ✅ `vite.config.js`

### Documentation
- ✅ All `.md` files
- ✅ `README.md`
- ✅ `TROUBLESHOOTING.md`, etc.

### Directory Structure
- ✅ `.gitkeep` files in `uploads/` and `results/`

## 🚀 Initialize Git Repository

```bash
# Initialize repository
git init

# Check what will be committed
git status

# Stage all files
git add .

# First commit
git commit -m "Initial commit: Image Testing System with React UI"
```

## ⚠️ Important Security Check

Before pushing to GitHub/GitLab:

```bash
# Verify .env is ignored
git status | grep .env
# Should show nothing (or only .env.example)

# Double check .env is in .gitignore
cat .gitignore | grep "^\.env$"
# Should show: .env
```

## 🔑 API Keys Safety

### ❌ NEVER Commit
```bash
# These files contain secrets
.env
app.log (may contain API keys in error messages)
```

### ✅ Safe to Share
```bash
# These are templates
.env.example
```

## 📦 Setting Up for Others

When someone clones your repository:

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd image_test_automation

# 2. Copy the example env file
cp .env.example .env

# 3. Edit .env with their API keys
nano .env

# 4. Install dependencies
pip install -r requirements.txt
cd frontend && npm install

# 5. Build React app
npm run build

# 6. Run application
cd ..
python app.py
```

## 🔄 Common Git Commands

```bash
# Check status
git status

# Add specific files
git add app.py frontend/src/

# Add all changes
git add .

# Commit with message
git commit -m "Add new feature"

# Push to remote
git push origin main

# Pull latest changes
git pull origin main

# View commit history
git log --oneline

# View what's ignored
git status --ignored
```

## 🌿 Recommended Branch Strategy

```bash
# Create feature branch
git checkout -b feature/add-new-api-provider

# Make changes and commit
git add .
git commit -m "Add support for Google Cloud Vision"

# Push feature branch
git push origin feature/add-new-api-provider

# Merge to main (on GitHub/GitLab via Pull Request)
# Or locally:
git checkout main
git merge feature/add-new-api-provider
```

## 📋 Pre-Commit Checklist

Before committing:
- [ ] `.env` is NOT staged
- [ ] No API keys in code
- [ ] No `app.log` staged
- [ ] Code is tested locally
- [ ] Documentation is updated

```bash
# Check what will be committed
git diff --cached

# Unstage a file if needed
git reset HEAD <file>
```

## 🚨 Emergency: Accidentally Committed Secrets

If you accidentally committed `.env` or API keys:

```bash
# Remove from last commit (if not pushed)
git reset --soft HEAD~1
git reset HEAD .env
git commit -m "Your commit message"

# Remove from history (if already pushed) - USE WITH CAUTION
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (warns collaborators)
git push origin --force --all
```

**Important**: After removing leaked secrets, **rotate your API keys immediately**!

## 📚 Files Overview

| File | Git Status | Purpose |
|------|-----------|---------|
| `.env` | ❌ Ignored | Your actual API keys |
| `.env.example` | ✅ Committed | Template for others |
| `.gitignore` | ✅ Committed | Ignore rules |
| `app.log` | ❌ Ignored | Application logs |
| `venv/` | ❌ Ignored | Python packages |
| `node_modules/` | ❌ Ignored | Node packages |
| `uploads/` | ❌ Ignored | User images |
| `results/` | ❌ Ignored | Test results |
| `static/` | ✅ Committed | React build |
| `app.py` | ✅ Committed | Source code |
| `*.md` | ✅ Committed | Documentation |

## 🔗 Connect to GitHub

```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/yourusername/image-test-automation.git
git branch -M main
git push -u origin main
```

## 🛡️ GitHub Repository Settings

After pushing:
1. Go to Settings → Secrets and variables → Actions
2. Add these secrets:
   - `OPENAI_API_KEY` (if using OpenAI)
   - `AZURE_VISION_KEY` (if using Azure)
   - `AZURE_VISION_ENDPOINT` (if using Azure)

This allows CI/CD to run without exposing keys in code.

---

**Remember**: Your `.env` file is your most important secret. Never commit it! 🔐
