# GitHub Copilot Commit Message Instructions

Follow the Conventional Commits specification when creating commit messages:

1. Format: `<type>[optional scope]: <description>`
   - Types: fix, feat, docs, style, refactor, perf, test, build, ci, chore
   - Scope: Component or area of codebase in parentheses (optional)
   - Description: Short, imperative summary of changes

2. Breaking changes:
   - Add ! after type/scope: `feat!: drop support for Node 8`
   - OR add footer: `BREAKING CHANGE: use JavaScript features not available in Node 8`

3. Keep the subject line under 72 characters and use imperative mood

4. For complex changes, add a body separated by a blank line from the subject:
   ```
   fix(parser): prevent racing of requests

   Introduce a request id and a reference to latest request.
   Dismiss incoming responses other than from latest request.
   ```

5. Reference issues in footer using: `Refs: #123` or `Fixes: #123`
