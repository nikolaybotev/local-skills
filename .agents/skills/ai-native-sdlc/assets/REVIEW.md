# Review instructions

## Passes

Run three passes and tag each finding with its pass:

- **Bugs:** <logic errors that would break this product's promise>
- **Security:** secrets or personal data in the repo, unexpected network or dependency surface, unsafe file or path handling
- **Compliance:** the change matches `intent/<change>/spec.md` and `plan.md`, and the conventions in `AGENTS.md`. A departure from the plan that is not written back into `plan.md` in the same change is a compliance finding.

## What Important means here

Reserve Important for findings that <break the product's promise, leak data, or ship a change the spec forbids>. Style and naming are nits.

## Cap the nits

Report at most five nits per review; summarize the rest as a count.

## Do not report

Formatting the CI already enforces, generated files the repo ignores, and wording inside the verbatim prompt block of any `intent.md`.
