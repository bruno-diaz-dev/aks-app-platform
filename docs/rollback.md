# Rollback Procedure

## Context
This repository follows a GitOps deployment model where Git is the single source
of truth for the desired state of the cluster.

Application deployments are driven by image version updates committed to this
repository and reconciled automatically by the GitOps controller.

## Rollback strategy
Rollback is performed by reverting the Git commit that introduced the faulty
image version.

No direct changes are applied to the cluster.

## Rollback steps
1. Identify the commit that updated the application image to the faulty version.
2. Revert the commit:
   ```bash
   git revert <commit-sha>
   git push
   ```
3. The GitOps controller detects the change and reconciles the cluster back to
the previous stable version.

Benefits

- Full auditability through Git history

- Deterministic and reproducible rollbacks

- No manual intervention on the cluster

- Consistent with GitOps principles

## Non-goals

- Automatic rollbacks based on health checks

- Imperative rollback commands (kubectl rollout undo)

- Out-of-band cluster changes