# LightGuard-Agent 🛡️

# MCP Arabic Toolkit 🌍

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/Model%20Context%20Protocol-Compatible-purple.svg)](https://modelcontextprotocol.io/)

**A high-performance Model Context Protocol (MCP) server providing Arabic Natural Language Processing (NLP), text normalization, diacritics stripping, dialect detection, and token efficiency analysis for AI agents.**

Developed by **Tarek Mohamed** ([@seotarek](https://github.com/seotarek))

---

## ✨ Features

- ⚡ **Model Context Protocol (MCP) Compatible:** Plug directly into Claude Desktop, Cursor, and any MCP client.
- 🧹 **Advanced Arabic Normalization:** Unify complex Alef variants, Hamza, Yaa, Taa Marbuta, and strip Tatweel.
- 🎯 **Tashkeel Stripping:** Remove diacritics (Harakat) accurately with zero distortion to core roots.
- 🗣️ **Arabic Dialect Classification:** Heuristic and marker-based identification across **Egyptian (EGY)**, **Levantine (LEV)**, **Gulf (GLF)**, **Maghrebi (MAG)**, and **Modern Standard Arabic (MSA)**.
- 📊 **Token & Prompt Efficiency Metrics:** Calculate character-to-word and token compression statistics to optimize LLM prompt budgets for Arabic workloads.

---

## 🛠️ MCP Tools Exposed

| Tool Name | Description |
| :--- | :--- |
| `arabic_normalize_text` | Normalizes Arabic letters, unifies orthographic variants, and strips elongation. |
| `arabic_strip_diacritics` | Strips all Tashkeel / Harakat from the input text. |
| `arabic_detect_dialect` | Identifies regional dialect with confidence scores. |
| `arabic_token_metrics` | Measures Arabic prompt density, word counts, and estimated token ratios. |

---

## 🚀 Quickstart & Installation

### 1. Clone & Run
```bash
git clone https://github.com/seotarek/mcp-arabic-toolkit.git
cd mcp-arabic-toolkit
```

### 2. Configure with Claude Desktop or Cursor
Add the server configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arabic-toolkit": {
      "command": "python",
      "args": ["-m", "mcp_arabic.server"],
      "cwd": "/path/to/mcp-arabic-toolkit"
    }
  }
}
```

---

## 🧪 Testing

Run the automated test suite:
```bash
python -m unittest discover tests
```

---

## 📜 License
This project is open source and available under the [MIT License](LICENSE).
