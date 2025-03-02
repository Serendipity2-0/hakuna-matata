# Coding Standards

## Introduction
This document outlines the coding standards for TradeMan projects. Following these standards ensures consistency, readability, and maintainability across all codebases.

## General Guidelines

### Naming Conventions
- Use **camelCase** for variables and functions in JavaScript
- Use **PascalCase** for class names and React components
- Use **snake_case** for Python variables and functions
- Use **UPPER_SNAKE_CASE** for constants

### Indentation and Formatting
- Use 4 spaces for indentation in Python
- Use 2 spaces for indentation in JavaScript, HTML, and CSS
- Limit line length to 80-100 characters
- Use blank lines to separate logical sections

### Comments
- Write comments that explain "why", not "what"
- Use docstrings for functions and classes
- Keep comments up-to-date with code changes

## Language-Specific Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Use f-strings for string formatting
- Use list comprehensions when they improve readability

### JavaScript
- Use ES6+ features when possible
- Prefer const over let, and let over var
- Use destructuring assignment
- Use arrow functions for callbacks

### SQL
- Use UPPERCASE for SQL keywords
- Use snake_case for table and column names
- Include comments for complex queries

## Code Review Process
All code must go through a code review process before being merged:
1. Create a pull request
2. Assign at least one reviewer
3. Address all comments and suggestions
4. Get approval before merging

## Testing Requirements
- Write unit tests for all new features
- Maintain at least 80% code coverage
- Test edge cases and error conditions

## Version Control
- Write clear, concise commit messages
- Reference issue numbers in commit messages
- Keep commits focused on a single change

## Conclusion
Following these standards will help maintain code quality and make collaboration easier for all team members.
