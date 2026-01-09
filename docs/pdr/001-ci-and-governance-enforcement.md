# PDR-001: CI and Governance Enforcement

## Status

Accepted

## Context

This repository is used as a public portfolio to demonstrate real-world Platform / DevOps practices. The goal is to enforce production-grade governance on changes merged into the `main` branch, even in a single-maintainer setup.

The platform includes:

* Mandatory CI pipelines
* Branch protection using GitHub Rulesets
* Code ownership enforcement
* Separation between authoring and approval of changes

A key requirement is to ensure that no non-compliant or unreviewed change can reach `main`, regardless of PR approvals.

## Decision

The following governance mechanisms were implemented:

1. **GitHub Rulesets for `main`**

   * Require pull requests before merge
   * Block force pushes
   * Require at least one approving review
   * Require status checks to pass

2. **Required CI Checks**

   * The primary CI pipeline (`ci`) is configured as a required status check
   * Additional quality gates may exist as non-required or required depending on risk

3. **Intentional CI Failure Scenarios**

   * A controlled CI workflow was added to intentionally fail
   * Used to validate that branch protection blocks merges under failure conditions

4. **CODEOWNERS Enforcement**

   * Platform-critical paths (`.github/workflows`, `platform/`, `docs/`) require Code Owner review
   * Self-approval is not permitted, even for the repository owner

## Consequences

* Pull requests are blocked if required CI checks fail
* Pull requests authored by the Code Owner cannot be self-approved
* Governance remains enforced even in a single-maintainer repository
* Some PRs are intentionally left unmerged to demonstrate enforcement behavior

## Rationale

In production environments, governance failures are more costly than delayed merges. Enforcing CI, reviews, and ownership rules reduces the risk of regressions and unauthorized changes.

This setup mirrors enterprise platform teams where:

* CI acts as a quality gate
* Human review is mandatory
* Ownership boundaries are respected

## Notes

This decision prioritizes correctness and auditability over convenience. In a real team, additional reviewers would be required to complete the workflow.


## Evidence

- Pull Request #16: Governance and CI enforcement validation  
  (PR intentionally closed without merge to demonstrate enforcement behavior)
