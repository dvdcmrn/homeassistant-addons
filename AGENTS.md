# Agents

This repository has **no local AI toolkit** (no `.cursor/` agent trees, no `.claude/`, no `CLAUDE.md`).

Use the Cursor MCP knowledge tools (`valhal-knowledge-*`) and **`gungnir`** / **`valhal-odin`** for homelab ops (same GungnirMCP gateway).

## Knowledge (MCP)

| Tool | Purpose |
|------|---------|
| `valhal-knowledge-search_kbase` | Search |
| `valhal-knowledge-read_kbase_doc` | Read a doc |
| `valhal-knowledge-write_kbase_doc` | Write/update a doc |
| `valhal-knowledge-kbase_manifest` | List bases / files |

Useful paths inside the knowledge base:

- `homelab/` — LAN hosts and network
- `mjolnir/project.md` — workstation defaults
- `projects/<repo>/project.md` — per-repo ship/deploy notes

## Skills / rules

Workflow skills live in Cursor via GungnirMCP Library export (`~/.cursor/skills`), not in this repo.
