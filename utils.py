import json
from pathlib import Path
from typing import Dict, Any
from config import DATA_FILE

def load_stats() -> Dict[str, Any]:
    p = Path(DATA_FILE)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_stats(stats: Dict[str, Any]):
    p = Path(DATA_FILE)
    p.write_text(json.dumps(stats, ensure_ascii=False, indent=4), encoding="utf-8")
