# Review instructions

## Passes

Run three passes and tag each finding with its pass:

- **Bugs:** <logic errors that would break this product's promise>
- **Security:** secrets, API keys, or key material in the repo, unexpected network or dependency surface, unsafe file or path handling
- **Compliance:** the change matches `intent/<change>/spec.md` and `plan.md`, and the conventions in `AGENTS.md`. A departure from the plan that is not written back into `plan.md` in the same change is a compliance finding.

## Builder writing

Tag these under **Compliance** unless they would break the product; then use **Important** under Bugs.

- **Self-reference:** prose about this repo hardcodes its owner, name, or URL instead of saying "this repo". Distribution entry points may hardcode a canonical location—a curl-to-sh one-liner, an installer's default source URL, or another repo's dependency that pulls these skills—with an optional override such as `LOCAL_SKILLS_REPO_URL` for forks. References to other repos are fine. Never derive this repo's identity from `GITHUB_REPOSITORY` in code other repos' CI may run.
- **Variable config:** docs, tests, or workflows embed a literal value where the design names a setting (env var, secret, or config key).
- **Obvious notes (human-facing docs only):** in README, user docs, or setup docs, parentheticals or asides that restate what the reader already knows (for example that a successful command exits zero). Do not flag explicit expectations in agent-facing files (`AGENTS.md`, `REVIEW.md`, skills, intents for agents); those notes stay.

## What Important means here

Reserve Important for findings that <break the product's promise, leak data, or ship a change the spec forbids>. Style and naming are nits.

## Cap the nits

Report at most five nits per review; summarize the rest as a count.

## Do not report

Formatting the CI already enforces, generated files the repo ignores, and wording inside the verbatim prompt block of any `intent.md`.
