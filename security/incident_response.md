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

### Rust-Specific Response

When the incident involves Rust code or Rust dependencies, maintainers should answer these questions early:

- Is the issue in `ciphey` code, a direct dependency, or a transitive dependency?
- Is it reachable in normal builds, or only behind specific Cargo features, targets, or optional workflows?
- Does it affect memory safety, undefined behavior, local file access, token handling, SQLite persistence, or only a low-risk development path?

### Rust Triage

- Check the affected crate version in `Cargo.toml` and `Cargo.lock`.
- Use `cargo tree -i <crate>` to find why the vulnerable crate is present and whether it is runtime, test-only, bench-only, or release-only.
- Confirm whether the affected code path is actually compiled for `ciphey`'s supported targets and enabled features.
- If the report involves unsafe Rust, FFI, or C bindings, isolate the exact boundary where safety assumptions fail.

### Rust Containment

- Prefer the smallest containment step that removes the vulnerable code path from normal use.
- If the issue is in a dependency and no patch is available yet, disable the affected feature, decoder, or workflow if possible.
- If the issue is in first-run setup, file handling, or SQLite persistence, consider shipping a temporary mitigation note before a full fix is ready.
- Avoid broad dependency churn during incident response; keep the containment diff easy to review.

### Rust Remediation

- For dependency incidents, prefer a narrow update such as `cargo update -p <crate>` or a targeted version bump before considering larger upgrades.
- Review the resulting `Cargo.lock` diff carefully so unrelated crate movement does not get bundled into the security fix.
- For crate-code incidents, land the smallest fix that restores safety or correct bounds checking, especially around `unsafe`, regex handling, file reads, token flow, and SQLite boundaries.
- Add a regression test that reproduces the vulnerable condition when practical. If a full regression test is not possible, document why.

### Rust Validation

After the fix:

- run `cargo check`
- run the smallest relevant `cargo test` surface first, then broader coverage as needed
- run `cargo clippy` if the change touches logic where lints may expose related issues
- verify that timeout behavior and plaintext-detection behavior were not unintentionally changed by the patch

If the incident is tied to a RustSec, GHSA, or crates.io advisory, record the advisory identifier in the incident notes and in the user-facing disclosure.

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
