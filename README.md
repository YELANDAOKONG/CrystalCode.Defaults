# Crystal Code Defaults

**Default provider and model definitions for [Crystal Code](https://github.com/YELANDAOKONG/CrystalCode).**

This repository holds the reference `providers.json` catalog: named endpoints, protocols, model ids, and per-model metadata such as context windows, output limits, thinking efforts, and image input. Copy it into your Crystal home to extend the small starter set built into Crystal Code with the full catalog.

[![Crystal Code](https://img.shields.io/badge/Crystal%20Code-YELANDAOKONG%2FCrystalCode-512BD4.svg)](https://github.com/YELANDAOKONG/CrystalCode)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[Get started](#get-started) · [Catalog](#catalog) · [How the file is used](#how-the-file-is-used) · [File format](#file-format) · [Maintenance](#maintenance)

## 📦 What's in this repository

| File | Purpose |
| :--- | :--- |
| `providers.json` | The default provider and model catalog |

<a name="get-started"></a>

## 🚀 Get started

### 📥 1. Download the catalog

Crystal Code reads `providers.json` from its home directory: `~/.crystal/providers.json`, or the directory named by `CRYSTAL_HOME` when that variable is set. On Windows the default home is `%USERPROFILE%\.crystal`.

**Linux or macOS**

```bash
mkdir -p ~/.crystal
curl --fail --location --show-error \
  https://raw.githubusercontent.com/YELANDAOKONG/CrystalCode.Defaults/master/providers.json \
  --output ~/.crystal/providers.json
```

**Windows PowerShell**

```powershell
$crystalHome = "$env:USERPROFILE\.crystal"
New-Item -ItemType Directory -Force $crystalHome | Out-Null
Invoke-WebRequest `
  -Uri https://raw.githubusercontent.com/YELANDAOKONG/CrystalCode.Defaults/master/providers.json `
  -OutFile "$crystalHome\providers.json"
```

The download replaces an existing `providers.json`. Back up or merge a file you already customized before you overwrite it.

### 🔑 2. Set provider keys

Keys never belong in this file. Write each one in `~/.crystal/credentials.json` under the provider name, or set `<PROVIDER>_API_KEY` for the process that starts the app. A provider entry can also name an environment variable with `apiKeyEnvironment`, as `bigmodel` does with `ZHIPU_API_KEY`. See [Credentials](https://github.com/YELANDAOKONG/CrystalCode/blob/master/docs/user-guide.md#credentials) in the user guide for the full lookup order.

### 🏁 3. Restart Crystal Code

Provider definitions are read at startup. Restart the app after the file changes, then select a model with `/model`, or start with `--provider` and `--model`.

<a name="catalog"></a>

## 🗂️ Catalog

| Provider | Protocols | Base URI |
| :--- | :--- | :--- |
| `deepseek` | `deepseek` | `https://api.deepseek.com/` |
| `openai` | `openai` | `https://api.openai.com/v1/` |
| `anthropic` | `anthropic` | `https://api.anthropic.com/v1/` |
| `gemini` | `gemini` | `https://generativelanguage.googleapis.com/v1beta/` |
| `moonshot` | `openai` | `https://api.moonshot.cn/v1/` |
| `siliconflow` | `openai` | `https://api.siliconflow.cn/v1/` |
| `bigmodel` | `openai` | `https://open.bigmodel.cn/api/paas/v4/` |
| `openrouter` | `openai` | `https://openrouter.ai/api/v1/` |
| `requesty` | `openai` | `https://router.requesty.ai/v1/` |
| `opencode-zen` | `responses`, `anthropic`, `gemini`, `openai` | `https://opencode.ai/zen/v1/` |
| `opencode-go` | `responses`, `anthropic`, `openai` | `https://opencode.ai/zen/go/v1/` |
| `commandcode` | `openai`, `anthropic` | `https://api.commandcode.ai/provider/v1/` |

A provider name can map to an array of entries when one service exposes several protocols or endpoints; `opencode-zen`, `opencode-go`, and `commandcode` use this form, and each model is routed to the protocol that owns it.

`openai` means OpenAI-compatible Chat Completions and `responses` is the OpenAI Responses API. `deepseek`, `anthropic`, `gemini`, and `ollama` are native protocols.

<a name="how-the-file-is-used"></a>

## ⚙️ How the file is used

- Without this file, Crystal Code falls back to a small starter catalog: `deepseek`, `openai`, `gemini`, and `ollama`. The `anthropic` protocol is built in, but has no starter entry.
- A `providers.json` in the Crystal home supplies the operator catalog and overlays the built-in one.
- Models that are not listed in the effective catalog cannot be selected. There is no global context window.
- A model may declare selectable context budgets with `contextWindows`; `/context` cycles them, and compaction and the status bar use the selected budget.
- When `providers.json` exists, the legacy `providers` object in `config.json` is ignored.

<a name="file-format"></a>

## 📄 File format

Top-level keys are provider names. Each value is one provider entry or an array of entries, in the same shape Crystal Code reads and writes.

Provider fields:

| Field | Meaning |
| :--- | :--- |
| `protocol` | `deepseek`, `openai`, `responses`, `anthropic`, `gemini`, or `ollama` |
| `baseUri` | Absolute API base URI; the adapter appends the protocol's chat path |
| `models` | Table of selectable model ids |
| `replayReasoningContent` | Replay provider reasoning content (DeepSeek always does this) |
| `tokenLimit` | Chat Completions output field: `max_tokens` or `max_completion_tokens` |
| `options` | Optional object of protocol-specific settings; unknown names, or names that do not apply to the protocol, fail loading. `temperature`, `topP`, and `maxTokens` stay on the model |
| `apiKeyEnvironment` | Environment variable name checked first for this provider |
| `apiKey` | Literal, `{env:NAME}`, or `{file:path}`. Keep secrets out of this file |
| `requiresApiKey` | Whether a missing key is an error (default `true`, except `ollama`) |
| `organization` / `project` | Optional OpenAI organization and project |

Model fields:

| Field | Meaning |
| :--- | :--- |
| `contextWindow` | Required. Positive maximum token window; upper bound for selectable budgets, and the sole budget when `contextWindows` is omitted |
| `contextWindows` | Optional distinct positive token budgets no greater than `contextWindow`, for example `[272000, 1000000]`. `/context` cycles them; the lowest is the initial budget, and compaction and the status bar use the selected budget |
| `maxTokens` | Optional positive output-token cap |
| `thinking` | Whether the model accepts reasoning hints |
| `thinkingEfforts` | Portable names `minimal`, `low`, `medium`, `high`, and `maximum` (`max` is stored as `maximum`), or another effort token the endpoint accepts. A token starts with a letter and then uses only letters, digits, and hyphens |
| `thinkingCanDisable` | Whether `/thinking off` is accepted (default `true`). Models that always reason, such as Gemini 3, set this to `false` |
| `imageInput` | Whether the model may receive images (default `false`) |
| `audioInput` | Declared audio input (default `false`). Stored and visible to plugins; the host does not accept or send audio |
| `videoInput` | Declared video input (default `false`). Stored and visible to plugins; the host does not accept or send video |
| `temperature` | Optional, 0 to 2 |
| `topP` | Optional, 0 to 1 |

The [user guide](https://github.com/YELANDAOKONG/CrystalCode/blob/master/docs/user-guide.md#configuration) covers protocols, examples, and credentials in full.

## 🤝 Maintenance

Maintainers can write a commit message and commit the current change with [`commit.sh`](commit.sh). It runs `crystal run` in this repository. Extra arguments are appended to the task. The run skips external tools and the directory trust check, and it does not record the directory as trusted.

Update `providers.json` by hand when a provider adds, retires, or changes models or model metadata. Crystal Code does not rewrite this file.

## 📄 License

[MIT](LICENSE)
