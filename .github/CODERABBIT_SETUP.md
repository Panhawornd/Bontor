# CodeRabbit Setup Guide

This guide will help you set up CodeRabbit for automated security-focused code reviews in your repository.

## Prerequisites

1. GitHub account with admin access to this repository
2. Repository is already pushed to GitHub

## Setup Steps

### 1. Install CodeRabbit GitHub App

1. Go to [CodeRabbit GitHub App](https://github.com/apps/coderabbitai)
2. Click "Install" or "Configure"
3. Select your organization or personal account
4. Choose the repositories where you want CodeRabbit to run:
   - Select "Only select repositories"
   - Choose `Capstone-Grade-Analyze`
5. Click "Install" or "Save"

### 2. Grant Permissions

CodeRabbit will request the following permissions:
- **Read**: Repository metadata, pull requests, code
- **Write**: Pull request comments, status checks (optional)

Grant these permissions to enable code reviews.

### 3. Verify Configuration

The repository already includes:
- `.coderabbit.yaml` - Main configuration file with security-focused rules
- `.github/workflows/coderabbit.yml` - GitHub Actions workflow (optional, for enhanced features)

### 4. Test the Integration

1. Create a test branch:
   ```bash
   git checkout -b test/coderabbit-integration
   ```

2. Make a small change and commit:
   ```bash
   git add .
   git commit -m "test: CodeRabbit integration"
   git push origin test/coderabbit-integration
   ```

3. Create a Pull Request on GitHub

4. CodeRabbit should automatically:
   - Review the code changes
   - Post comments on security issues
   - Provide suggestions for improvements

## Configuration Files

### `.coderabbit.yaml`

This file contains security-focused review settings:
- **Security Rules**: SQL injection, XSS, authentication checks
- **Performance Checks**: Database queries, API endpoints
- **Best Practices**: Code style, type safety, documentation

### `.github/workflows/coderabbit.yml`

GitHub Actions workflow that triggers CodeRabbit reviews on:
- Pull request events (opened, synchronized, reopened)
- Push to main/develop branches

## Security Focus Areas

CodeRabbit is configured to check for:

### Critical Security Issues
- Hardcoded secrets (passwords, API keys, tokens)
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Authentication/authorization flaws
- CORS misconfigurations

### Code Quality
- Input validation
- Error handling
- Type safety
- Dependency vulnerabilities

## Customization

### Adjust Review Strictness

Edit `.coderabbit.yaml`:
- `min_confidence`: Lower for more reviews, higher for fewer
- `block_on_critical`: Set to `true` to block PRs with critical issues
- `min_severity`: Adjust minimum severity for comments

### Add Custom Rules

Add security rules to `.coderabbit.yaml` under `security_rules`:
```yaml
security_rules:
  - name: "Custom rule name"
    pattern: "regex_pattern"
    severity: high|medium|low
    message: "Custom message"
```

## Troubleshooting

### CodeRabbit Not Reviewing PRs

1. Check if the GitHub App is installed:
   - Go to repository Settings → Integrations → Installed GitHub Apps
   - Verify "CodeRabbit" is listed

2. Check App permissions:
   - Ensure it has read/write access to pull requests

3. Review workflow logs:
   - Go to Actions tab → CodeRabbit Review workflow

### False Positives

If CodeRabbit flags legitimate code:
- You can dismiss comments on GitHub
- Adjust patterns in `.coderabbit.yaml`
- Add file patterns to `ignore` section

## Best Practices

1. **Review CodeRabbit Comments**: Don't ignore security warnings
2. **Fix Critical Issues**: Address high-severity security issues before merging
3. **Update Rules**: Periodically review and update security rules
4. **Monitor Dependencies**: Keep dependencies updated to avoid vulnerabilities

## Resources

- [CodeRabbit Documentation](https://docs.coderabbit.ai)
- [CodeRabbit GitHub App](https://github.com/apps/coderabbitai)
- [Security Best Practices](https://docs.coderabbit.ai/security)

## Support

If you encounter issues:
1. Check the [CodeRabbit documentation](https://docs.coderabbit.ai)
2. Review GitHub Actions logs
3. Check CodeRabbit's status page

