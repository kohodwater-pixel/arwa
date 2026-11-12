# Figma and Canva

## Which tool

| Use **Figma** when the work needs precise control | Use **Canva** when the work needs speed |
|---|---|
| Logo and identity files, components, variants | Social media posts and ad sets |
| Design systems, variables and design tokens | Company profiles the client will edit themselves |
| Website, app and dashboard UI | Presentations and proposals in Canva |
| Reading colours, fonts and components from an existing design | Resizing one design to many formats |
| Identity applications built from components | Template-based marketing output, checking against a Brand Kit |

When neither fits or neither is available, build in HTML/SVG/PPTX inside the client folder. Local files are always an acceptable deliverable; a tool is a means, not the product.

## Figma workflow

1. `whoami` once per session if access is in doubt.
2. Extract `fileKey` and `nodeId` from the URL (convert `-` to `:` in the node id).
3. `create_session` with the file key before any other file tool; reuse the returned session id.
4. Reading: `get_design_context` (after loading the `figma-design-to-code` skill), `get_variable_defs` for tokens, `get_metadata` for structure, `get_screenshot` to see it.
5. Writing: `create_new_file` if needed, then `use_figma` only after loading the `figma-use` skill (from the Figma plugin, or `get_figma_skill` / `skill://figma/figma-use/SKILL.md`).
6. After writing, take a `get_screenshot` of what you made and look at it.

## Canva workflow

1. `list-brand-kits` to see whether a Brand Kit exists. If it does not, brand compliance is checked manually against the client's `brand-context.md`, and you say so.
2. Create with `generate-design` (then `create-design-from-candidate`), or from a Brand Template when one exists.
3. Edit with `edit-design`; resize with `resize-design`; export with `export-design`.
4. After any change, `read-design` or export and view the result.

## Verification — no unverified claims

- An operation counts as done only when the tool call returned success **and** you looked at the result (screenshot, read-back or export).
- Record each operation in the handoff with the URL or file it produced.
- If a tool is missing, access is denied, a seat is view-only, or a rate limit is hit: stop, report exactly what failed, and continue with a local file instead. Do not retry in a loop and do not describe the work as done.
- Arabic text placed in Figma or Canva is checked visually like any other export.

## Client data

- A Figma or Canva file belongs to one client. Name it `<client-slug> — <deliverable>` and record its URL in the client's `brand-context.md`.
- Never copy assets between clients' files.
- Client text, images and video are never sent to any third-party cloud service other than the connected Figma and Canva accounts, unless the user explicitly approves that service for that client.
