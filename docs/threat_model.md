# Threat Model

This document outlines the main trust boundaries, assets, and security assumptions for `ciphey`.

## System Overview

`ciphey` is a local decoding tool with a thin CLI over a library-first core. Users provide ciphertext, files, configuration, and optional model-download credentials. The search pipeline runs decoders and checkers against attacker-controlled input and stores some local state under `~/.ciphey`.

## Security Goals

- protect local secrets and sensitive user data
- avoid unsafe handling of attacker-controlled input
- preserve integrity of release artifacts and repository automation
- keep resource usage bounded enough that hostile input does not bypass expected timeout behavior

## Key Assets

- local files passed through `--file`
- `~/.ciphey/config.toml`
- `~/.ciphey/database.sqlite`
- optional model files under `~/.ciphey/models/`
- Hugging Face or other download credentials used during first-run setup
- release artifacts, workflow definitions, and dependency metadata

## Trust Boundaries

- CLI arguments, stdin, and file contents are untrusted input.
- Decoder and checker execution must treat transformed candidate strings as untrusted.
- The first-run model download flow crosses a trust boundary into third-party services.
- SQLite-backed persistence is trusted only as local state owned by the current user, not as authoritative truth from a trusted server.
- GitHub workflows, release automation, and repository settings form the supply-chain boundary for published artifacts.

## Primary Threats

### Crafted Input Causes Resource Exhaustion

Attackers can supply inputs that trigger excessive search branching, expensive checker behavior, or timeout regressions.

Mitigations:

- preserve timeout behavior as part of the public contract
- keep search and checker changes covered by targeted tests and benches
- prefer bounded or clearly costed operations when handling candidate plaintext

### Unsafe Local File Handling

The `--file` path and file contents may be attacker-controlled or unexpectedly sensitive.

Mitigations:

- keep file access explicit and local to user-requested paths
- treat parsing and decoding failures as normal input errors, not exceptional trust signals
- review changes in file-handling paths as security-sensitive

### Token Or Secret Exposure During First-Run Setup

The enhanced-detection setup flow may involve user credentials for model download.

Mitigations:

- do not log or persist tokens unnecessarily
- keep credential handling private to the minimum code path required for model download
- document the expected handling so regressions are easy to spot in review

### Local Persistence Exposure Or Poisoning

Configuration, cache, and human-review data live on disk and may influence later runs.

Mitigations:

- keep storage behavior explicit and predictable
- use test helpers instead of the real user database in tests
- review SQLite changes for injection, corruption, and privacy risks

### False Positives Reveal Sensitive Material

Plaintext-identification logic can classify secrets, credentials, or unrelated structured data as meaningful plaintext.

Mitigations:

- validate checker changes with representative encoded and plaintext examples
- bias toward explainable detection behavior over opaque heuristics when risk is unclear
- treat secret-like output as a security consideration during checker tuning

### Supply-Chain Or Automation Compromise

Compromised dependencies, workflows, or release automation can affect published artifacts and contributors.

Mitigations:

- protect the default branch
- use Dependabot, code scanning, and secret scanning
- prefer reviewed changes over direct pushes to release-critical code paths

## Assumptions And Out Of Scope

- A fully compromised user workstation is out of scope.
- Network threats are mostly limited to optional model download or dependency/release workflows.
- `ciphey` is a local analysis tool, not a sandbox for safely executing untrusted code.
