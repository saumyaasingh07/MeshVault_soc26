# Contributing to MeshVault

This guide covers how the MeshVault team works day-to-day: branching, sprints, standups, and coding standards. If you're picking up an issue for the first time, read this first.

---

## Git Branching Strategy

Each issue gets its own branch, created off main
Branch naming pattern: issue-<number>-<short-description> (e.g. issue-27-receive-shares, issue-10-gf-arithmetic)
Once your work on an issue is complete:

    1.Push your branch to GitHub: git push origin issue-<number>-<short-description>
    2.Open a Pull Request comparing your branch against main
    3.A mentor/senior reviews the code in the PR
    4.Once approved, it gets merged into main

New issues are typically created after a review, based on progress — check the issue tracker regularly


## Sprint Structure

Development is organized into **1.5–2 week sprints** (Scrum cycles). Each sprint has its own set of issues labeled `sprint-N` in the issue tracker, grouped under larger **Epics** (e.g. `[EPIC] Transfer Layer`).

- Issues are broken down and assigned per sprint
- Work should stay scoped to the issue(s) assigned to you for that sprint
- New issues may be added mid-project as scope becomes clearer — check the issue tracker regularly

## Standup Meetings

Short, ~30-minute standup meetings are held to:
- Share progress since the last standup
- Flag blockers early
- Align on technical direction before conflicting work happens

## Issue Tracking

- All work is tracked via GitHub Issues, grouped into Epics
- **Always reference the issue number** in your commits and Pull Requests (e.g. `Implement retry logic (#28)`)
- If you're unsure who owns an issue, check its **Assignee** field before starting work on it

## Pull Requests

- **No large code dumps.** Each PR should cover a single, well-defined issue or scope — not multiple unrelated changes bundled together
- Every PR must be **reviewed by at least one other contributor or mentor** before merging
- Include a short description of what the PR does and which issue it closes

## Coding Standards

- Follow standard Python style; this project uses `black` for formatting and `flake8` for linting (see `requirements.txt`)
- Write tests for new functionality using `pytest`
- Test coverage should include edge cases relevant to the module (e.g. threshold boundaries K=N and K=1 for crypto, connection timeouts and drops for networking)

## Documentation

- Any new module should include clear docstrings explaining its purpose and usage
- Update `CHANGELOG.md` when adding a feature, fixing a bug, or making a notable refactor
- Larger architectural or mathematical write-ups (e.g. cryptographic proofs) can use LaTeX if needed; general docs stay in Markdown

## CLI Shell Integration & Auto-completion

MeshVault includes built-in shell auto-completion powered by `Typer`.

### Enabling Auto-completion

To enable tab auto-completion for `meshvault` commands and options (`--threshold`, `--shares`, `--interface`, `--secret`), generate and source the completion script for your shell:

#### **Bash**
```bash
# Generate completion script to ~/.meshvault-complete.bash
python3 -m cli completion bash > ~/.meshvault-complete.bash

# Source it in your ~/.bashrc
echo "source ~/.meshvault-complete.bash" >> ~/.bashrc
source ~/.bashrc
```

#### **Zsh**
```zsh
# Generate completion script to custom fpath directory
mkdir -p ~/.zsh/completion
python3 -m cli completion zsh > ~/.zsh/completion/_meshvault

# Add to ~/.zshrc
echo "fpath=(~/.zsh/completion \$fpath)" >> ~/.zshrc
echo "autoload -U compinit && compinit" >> ~/.zshrc
source ~/.zshrc
```

#### **Fish**
```fish
# Save Fish completion script directly
python3 -m cli completion fish > ~/.config/fish/completions/meshvault.fish
```

#### **PowerShell**
```powershell
# Output completion script and add to PowerShell profile
python -m cli completion powershell | Out-String | Invoke-Expression
```

### CLI Debugging & Traceback Formatting
By default, MeshVault catches CLI errors and displays user-friendly, formatted error messages without stack traces. To inspect full tracebacks for debugging:

```bash
python3 -m cli --debug split -k 3 -n 5
```

---

## Getting Started Checklist

1. Pick up an issue assigned to you (or ask a mentor if unassigned)
2. Create a branch for it (see [Git Branching Strategy](#git-branching-strategy) above)
3. Implement the change, with tests
4. Reference the issue number in your commits
5. Open a Pull Request and request a review
6. Update `CHANGELOG.md` if applicable