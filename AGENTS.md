# AGENTS.md

This repository holds the default provider and model catalog for [Crystal Code](https://github.com/YELANDAOKONG/CrystalCode). It contains data only. [README.md](README.md) documents the file format, the catalog table, and the build step.

## Source of truth

- Edit `providers/<id>.json`. The file name without `.json` is the provider id. A file is one provider entry, or an array of entries when one service exposes several protocols.
- `providers.json` is generated. Never edit it by hand. Regenerate it with `python3 build_providers.py` after every change under `providers/`, and keep both in the same change.
- Keep the existing key order and two-space indentation. `build_providers.py` keeps provider order stable; a new provider file is appended alphabetically.

## Where model data comes from

models.dev does not contain everything the catalog needs. It is a starting point for ids and rough limits, and it must not be treated as complete or authoritative. It does not describe:

- Context window tiers that depend on the billing plan or the request, for example a standard window and a larger paid window. These go in `contextWindows`, with `contextWindow` as the upper bound.
- Whether a model supports speed selection. These go in `speeds`.
- Which service tiers a model accepts. These go in `serviceTiers`.
- Provider-specific thinking effort tokens, and whether thinking can be disabled.

Take these values from the provider's official documentation, pricing page, or API reference, and check the model id against the live model list when the provider exposes one. When the official source does not state a value, omit the field. Do not copy it from a similar model or from an aggregator, and do not guess.

## Rules

- A model that the provider has retired or that is not available through that endpoint must not be listed. Models that cannot be selected are removed, not marked.
- Router providers (`openrouter`, `openrouter-free`, `requesty`, `vercel`, and similar) use that router's own model ids and limits, which can differ from the first-party provider's.
- Secrets must never appear in this repository. Use `apiKeyEnvironment` to name an environment variable; do not write `apiKey` literals.
- The `README.md` catalog table and provider notes must match `providers/`. Update them when a provider is added or removed.
- Do not commit, amend, or push unless the user asks. When asked, use Conventional Commits with a lowercase type, as in `feat: add mercury-3 to inception`. `commit.sh` documents the allowed types.

## Verify

There is no test suite. Before handoff:

```bash
python3 build_providers.py
git status --short providers.json providers/
```

The build must succeed, and `providers.json` must change only in the entries you edited. Review `git diff providers.json` for unrelated churn.
