# Instructions for Removing Sensitive Data

To completely remove the sensitive API key from your Git history, follow these steps:

## Option 1: Using git filter-branch (built-in)

```bash
# Create a backup of your repository first
git clone --mirror https://github.com/yagupta77/screenshot-analysis.git screenshot-analysis-backup

# Run this command to remove the sensitive data from all branches
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch .env" --prune-empty --tag-name-filter cat -- --all

# Force push the changes to GitHub
git push --force origin main
```

## Option 2: Using BFG Repo-Cleaner (recommended)

1. Download BFG Repo-Cleaner from https://rtyley.github.io/bfg-repo-cleaner/
2. Run these commands:

```bash
# Create a file with the sensitive data to be removed
echo "OPENAI_API_KEY=[REDACTED]" > sensitive-data.txt

# Run BFG to remove the sensitive data
java -jar bfg.jar --replace-text sensitive-data.txt screenshot-analysis.git

# Clean up the repository
cd screenshot-analysis.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push the changes
git push --force
```

## Alternative: Create a New Repository

The simplest solution might be to:

1. Create a new repository on GitHub
2. Make sure `.env` is in your `.gitignore` file
3. Initialize a new Git repository locally
4. Add and commit your files (without the sensitive data)
5. Push to the new repository

This way, you start with a clean history without any sensitive data.
