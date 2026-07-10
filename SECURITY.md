# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in Creator Toolbox, please **do not**
open a public issue. Instead, please report it responsibly by emailing the
maintainers directly.

## Security Principles

### No Secrets in the Repository

- API keys, tokens, and credentials must never be committed.
- Use environment variables for sensitive configuration.
- `.env` files are gitignored.

### IP Safety

- The orchestrator enforces IP-safety rules configured per game.
- Do not incorporate leaked, rumored, or unverified game mechanics.
- Always validate against official documentation before referencing game
  features.

### Dependency Security

- Dependencies are kept minimal and vetted.
- Use `dependabot` for automated security updates.
- Review dependency licenses and vulnerability reports regularly.

### Code Review

- All contributions must go through pull request review.
- Security-sensitive changes require explicit sign-off.

## Compliance

Creator Toolbox is designed to comply with:

- Rockstar's Terms of Service and creator policies
- Copyright and intellectual property law
- Platform-specific moderation and content policies

Always review the game-specific `ip_safety` rules in `config/games/` before
deploying.
