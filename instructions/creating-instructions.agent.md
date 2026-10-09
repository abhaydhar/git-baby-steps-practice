# Create Project Instructions

- Keep instruction files in `./instructions/` as platform-agnostic Markdown documents.
- Name each instruction using `[verb]-[topic].agent.md` with hyphen-separated words.
- Keep each instruction focused on one workflow or responsibility; do not mix unrelated tasks.
- Use short bullet points, sub-bullets with `+`, and practical action steps rather than long explanations.
- Put the instruction catalog in `./instructions/main.agent.md` and keep it as the project entry point.
- Add each new instruction to the catalog with a one-line description and relevant keywords.
- When a user asks for an instruction or workflow, follow the catalog first, then open the relevant instruction file.
- Treat the catalog as the routing layer; keep the instruction files themselves as operational guidance.
- Follow the same structure across instruction files: action, scope, constraints, and exceptions when needed.
- Prefer reusable instructions over monolithic prompts; split large workflows into smaller files when the logic grows.
- Use `main.agent.md` as the source of truth for what exists and when to use it.
- Create entry-point wrappers for the selected IDE:
  + VS Code + Copilot: `.github/copilot-instructions.md` referencing `./instructions/main.agent.md`
  + Cursor: `.cursor/rules/*.mdc` referencing the instruction catalog
  + Claude Code: `.claude/CLAUDE.md` or command files referencing the project instructions
- If no IDE folder is present, ask the user which environment they are using, then create the matching scaffolding.
- For VS Code, enable instruction-file loading in `.vscode/settings.json` with `github.copilot.chat.codeGeneration.useInstructionFiles` set to `true`.
- Keep `.github/copilot-instructions.md` and `AGENTS.md` simple: state that the project should always follow `./instructions/main.agent.md` on each prompt.
- When updating an instruction file, read it first, preserve useful content, and add the new guidance in place rather than rewriting the whole file.
- Add `Keywords`, `Target`, and `Exceptions` metadata to catalog entries when useful for routing.
- Use `AGENTS.md` as a universal fallback entry point when IDE-specific wrappers are not committed.
- Keep instruction content in English unless the user explicitly asks for another language.
- Prefer concise, concrete wording over fluff, background, or rationale.
- When the project is empty, install the instruction structure from scratch and verify the entry point references the catalog correctly.
- After creating or changing the instruction setup, check that the entry point file, catalog file, and relevant wrappers exist and are aligned.
- If a skill is needed for an executable workflow, place it under `./instructions/[name]/SKILL.md` and link it from the root catalog in the same style as an instruction.
- Store instruction files under `./instructions/`, not inside arbitrary subfolders unless the team intentionally organizes them by domain.
- Maintain the catalog as a living index that points to the actual instruction files and remains easy to scan.
- Use this file as the reference for creating new project instruction assets, then update the catalog when the instruction tree expands.
