import sys
import json
from typing import Dict, Any, List
from .normalizer import ArabicNormalizer
from .dialect_detector import ArabicDialectDetector

TOOLS = [
    {
        "name": "arabic_normalize_text",
        "description": "Normalizes Arabic text by unifying character variants (Alef, Yaa), removing Tatweel, and stripping diacritics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The raw Arabic text to normalize."},
                "unify_alef": {"type": "boolean", "default": True, "description": "Unify all Alef variants (أ, إ, آ, ٱ) into ا."},
                "unify_yaa": {"type": "boolean", "default": True, "description": "Unify final Yaa (ى) into ي."},
                "unify_taa": {"type": "boolean", "default": False, "description": "Unify Taa Marbuta (ة) into ه."}
            },
            "required": ["text"]
        }
    },
    {
        "name": "arabic_strip_diacritics",
        "description": "Removes all vowel marks (Tashkeel/Harakat) and elongation (Tatweel) from Arabic text.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The Arabic text with diacritics."}
            },
            "required": ["text"]
        }
    },
    {
        "name": "arabic_detect_dialect",
        "description": "Classifies Arabic text into Modern Standard Arabic (MSA), Egyptian, Levantine, Gulf, or Maghrebi.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The Arabic text to analyze."}
            },
            "required": ["text"]
        }
    },
    {
        "name": "arabic_token_metrics",
        "description": "Computes token-to-word ratio, character count, and compression statistics for Arabic prompts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The Arabic text to evaluate."}
            },
            "required": ["text"]
        }
    }
]

def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    text = arguments.get("text", "")
    if name == "arabic_normalize_text":
        res = ArabicNormalizer.normalize(
            text,
            unify_alef=arguments.get("unify_alef", True),
            unify_yaa=arguments.get("unify_yaa", True),
            unify_taa=arguments.get("unify_taa", False)
        )
        return {"normalized_text": res}
    elif name == "arabic_strip_diacritics":
        res = ArabicNormalizer.strip_diacritics(text)
        return {"stripped_text": res}
    elif name == "arabic_detect_dialect":
        res = ArabicDialectDetector.detect(text)
        return res
    elif name == "arabic_token_metrics":
        words = len(text.split())
        chars = len(text)
        diacritics_count = len(text) - len(ArabicNormalizer.strip_diacritics(text))
        return {
            "word_count": words,
            "character_count": chars,
            "diacritics_count": diacritics_count,
            "estimated_token_ratio": round(chars / max(words, 1), 2)
        }
    else:
        raise ValueError(f"Unknown tool: {name}")

def run_stdio_server():
    """Standard Model Context Protocol (MCP) JSON-RPC loop over stdio."""
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "mcp-arabic-toolkit", "version": "0.1.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                tool_res = handle_call_tool(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(tool_res, ensure_ascii=False, indent=2)}]
                    }
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method '{method}' not found"}
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": req.get("id") if 'req' in locals() else None,
                "error": {"code": -32000, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run_stdio_server()
