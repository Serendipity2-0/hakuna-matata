
# Git Commit Message Guidelines for LLM

When writing commit messages, follow this structured approach to ensure clarity and consistency. The guidelines are tailored for the LLM to generate messages based on `git diff` output:

## 1. Commit Structure
Use the following format:
```
<type>(<scope>): <short summary>

[optional body]

[optional footer]
```

- **Type**: The type of change, which should be one of the following:
  - `feat`: A new feature
  - `fix`: A bug fix
  - `refactor`: Code changes that neither fix a bug nor add a feature
  - `style`: Code style improvements (formatting, whitespace, etc.) that do not affect functionality
  - `docs`: Documentation changes
  - `test`: Adding or updating tests
  - `chore`: Changes to build processes or auxiliary tools, libraries, etc.
  - `perf`: Performance improvement
  - `ci`: Continuous Integration-related changes

- **Scope**: The part of the codebase affected (e.g., `auth`, `api`, `frontend`, `build`). Leave empty if not applicable.

- **Short Summary**: A brief description of what was changed (use imperative mood, e.g., "Add", "Fix", "Update").

## 2. Message Length
- The summary should be no more than **50 characters**.
- The body, if necessary, should not exceed **72 characters per line**.

## 3. Message Body (Optional)
Provide additional context if needed:
- Explain **what** and **why** rather than **how**.
- Mention any potential impact or side effects.
- List additional information about **related tickets**, **issues**, or **motivation**.

## 4. Footer (Optional)
Include any relevant **meta information**:
- Reference related issues using `Fixes #<issue number>` if a bug is resolved.
- Note any breaking changes with `BREAKING CHANGE:` followed by details.

## Examples

1. **Adding a new feature:**
   ```
   feat(api): add user registration endpoint

   Implements the /register endpoint with validation checks for user data.
   ```

2. **Fixing a bug:**
   ```
   fix(auth): resolve token expiration bug

   Corrects the expiration time calculation to align with server settings. Fixes #42.
   ```

3. **Refactoring code:**
   ```
   refactor(frontend): optimize component rendering logic
   ```

4. **Updating documentation:**
   ```
   docs: update README with setup instructions
   ```
