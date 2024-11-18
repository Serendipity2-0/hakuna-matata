# Git Branching Workflow Documentation

## Overview

This document outlines our Git branching strategy, which follows a hierarchical structure to manage feature development, integration, and release processes.

## Branch Hierarchy

Our workflow consists of the following branches, in order of stability:

1. `main`: Production-ready code
2. `dev`: Integration branch for features
3. `phase1`: Grouping of related features phase by phase
4. `feature/auction`: Individual feature branch

## Workflow

### 1. Feature Development

- **Branch name format**: `feature/<feature-name>`
- **Base branch**: `phase1`

Developers work on individual features in dedicated feature branches. For example, `feature/auction`.

#### Commands:

```bash
# Switch to phase1 branch
git checkout phase1

# Create a new feature branch
git checkout -b feature/auction

# Work on the feature
git checkout feature/auction

# Push changes to feature/auction
git push origin feature/auction
```

### 2. Phase Integration

- **Branch name**: `phase1`
- **Base branch**: `dev`

The `phase1` branch groups related features together. Once all features for this phase are complete and merged.

### 3. Development Integration

- **Branch name**: `dev`
- **Base branch**: `main`

The `dev` branch integrates all completed phases and features. It's used for testing the entire system together.

### 4. Production Release

- **Branch name**: `main`

The `main` branch always contains production-ready code. Once `dev` is thoroughly tested and approved:

```bash
# Release process - Merge the pull request from dev to main
git checkout main
git pull origin main
git tag v1.x.x
git push origin v1.x.x
```

### Best Practices

1. Always create pull requests for code reviews before merging.
2. Keep commits small and focused.
3. Write clear commit messages.
4. Regularly sync your feature branch with its base branch to minimize merge conflicts.
5. Delete feature branches after they're merged.

### Commands Cheat Sheet

```bash
# Create a new feature branch
git checkout phase1
git checkout -b feature/new-feature

# Push changes to remote
git push origin feature/new-feature

# Update your branch with changes from base branch
git checkout feature/new-feature
git pull origin phase1

# Merge a branch (after pull request is approved)
git checkout phase1
git merge feature/new-feature

# Delete a branch locally
git branch -d feature/new-feature

# Delete a branch remotely
git push origin --delete feature/new-feature
```