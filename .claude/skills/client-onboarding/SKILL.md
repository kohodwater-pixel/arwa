---
name: client-onboarding
description: Onboard a new agency client - create their project folder from the template, run the discovery questionnaire, and write the brief and brand-context file. Use when the user says 'new client', 'onboard', 'start a project', 'client brief', or names a client that has no folder under clients/.
---

# Client onboarding

## Steps

1. **Create the workspace.** Copy `clients/CLIENT_TEMPLATE/` to `clients/<client-slug>/` (lowercase, hyphenated, Latin characters). Never edit the template itself.
2. **Collect what exists.** Ask for, or gather from the client's website and social accounts: current logo and brand files, existing profile or deck, competitors they name, and any brand guidelines. Save them untouched in `_originals/` and log them in `_originals/README.md`; put working copies in `01-brief/assets-received/`.
3. **Run discovery.** Use `01-brief/discovery-questionnaire.md`. Ask only the questions you cannot answer from material already supplied, in small batches. Ask in the client's language.
4. **Write the brief.** Fill all eleven fields of `01-brief/brief.md`: company name, business activity, country and target market, services and products, target audience, competitors, project objectives, required languages, existing files and logos, required deliverables, deadline — plus the list of verified facts the client allows to be published.
5. **Fill `brand-context.md`** with everything confirmed so far. Mark gaps as `TBC` and assumptions as assumptions.
6. **Confirm scope.** Summarise the deliverables and the stages they map to (see `CLAUDE.md`) and get the user's confirmation before research starts.

## Done when

- The client folder exists with a completed brief
- `brand-context.md` has no empty mandatory fields (only filled or `TBC`)
- Scope, languages and approver are confirmed
