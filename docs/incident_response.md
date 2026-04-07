# Incident Response Plan

This document defines the maintainer workflow for handling a suspected security incident or vulnerability in `ciphey`.

## Scope

This plan covers:

- vulnerabilities reported through email or GitHub private vulnerability reporting
- security incidents affecting released code, release artifacts, workflows, or repository secrets
- security regressions in local file handling, token handling, SQLite persistence, plaintext detection, and decoder execution

## Severity Levels

- `SEV-1`: active exploitation, credential compromise, release compromise, or a vulnerability that can expose sensitive data or execute code without a reasonable workaround
- `SEV-2`: denial of service, significant local data exposure, or a vulnerability with meaningful impact but limited exploitability
- `SEV-3`: defense-in-depth gaps, low-impact leaks, or issues that need a fix but do not create immediate user risk

## Response Targets

- Acknowledge a private report within 72 hours.
- Classify initial severity as soon as the report is reproducible or well-supported.
- For `SEV-1`, provide reporter updates at least every 24 hours while containment or a fix is in progress.
- For `SEV-2` and `SEV-3`, provide reporter updates when triage or remediation status materially changes.

## Workflow

### 1. Intake

- Keep reports private.
- Capture the affected version, commit, impact, and reproduction details.
- Avoid requesting real secrets unless they are necessary to validate the issue.

### 2. Triage

- Confirm whether the issue is in scope.
- Reproduce with the smallest local test case possible.
- Identify whether the issue affects released artifacts, only `master`, or only unreleased changes.

### 3. Containment

Use the smallest effective containment step first:

- pause or restrict vulnerable release activity
- disable or patch a vulnerable workflow
- revoke and rotate exposed credentials or tokens
- publish a temporary mitigation note when a fix will take longer than expected

### 4. Remediation

- land the smallest safe fix that closes the issue without silently extending timeout or trust boundaries
- add focused regression coverage near the affected component
- update `SECURITY.md` when reporting behavior or supported channels change

### 5. Release And Disclosure

- prepare a release or other user-facing remediation path
- coordinate disclosure timing with the reporter when possible
- use a GitHub security advisory or other private coordination channel until a fix is ready
- publish clear upgrade or mitigation guidance once disclosure is appropriate

### 6. Post-Incident Review

After remediation:

- document root cause and trigger conditions
- record what detection or review step failed to catch the issue earlier
- decide whether tests, benchmarks, review checklists, or release controls need to change

## Evidence Handling

- Keep proof-of-concept material private until disclosure.
- Redact secrets, tokens, local file contents, and personal data from shared logs.
- Prefer minimal reproductions over full user datasets.
