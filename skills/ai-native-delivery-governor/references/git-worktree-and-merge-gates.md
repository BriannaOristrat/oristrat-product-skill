# Git Worktree And Merge Gates

Use before pull, merge, rebase, conflict resolution, or restoring temporary preservation state.

## Preflight

1. Record current branch, HEAD, upstream, target ref, and commit graph divergence.
2. Inspect staged, unstaged, untracked, unmerged, and feature-relevant ignored files.
3. Classify every dirty path as current delivery, another local round, local environment, generated output, or unrelated user work.
4. Do not run `git pull` on a dirty worktree until every relevant path has a preservation plan.
5. Prefer `git fetch` plus an explicit merge/rebase decision over an opaque pull when conflicts are likely.

## Preservation

- Create a backup branch before integrating a remote/release branch when local commits are at risk.
- Preserve exact paths and record stash commit hashes and messages. Do not rely only on changing `stash@{n}` positions.
- `git stash -u` does not preserve ignored files. Find relevant ignored files explicitly and choose a narrow preservation method.
- Do not use `git stash --all` across a large workspace without auditing the included paths.

## Conflict Ownership

For each conflict, classify the desired result:

- keep target branch behavior;
- keep current local behavior;
- combine both because they affect the same contract;
- leave a release-owned defect untouched.

If the user says not to fix release problems, do not refactor, reformat, or lint-fix release-owned code while resolving conflicts. Compare the resolved file against both parents and ensure only the intended semantic combination remains.

## Restore And Cleanup

After the merge commit when authorized:

1. Restore local rounds by recorded stash hash or exact preservation source.
2. Check for conflict markers, duplicate i18n namespaces/registrations, staged files, and hidden ignored files.
3. Re-run target validation affected by the restore.
4. Report temporary backup branches and stashes.
5. Drop temporary recovery assets only after explicit cleanup approval or when their removal was included in the approved plan.
