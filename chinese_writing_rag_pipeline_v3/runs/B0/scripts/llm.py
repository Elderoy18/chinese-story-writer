"""Shared LLM helper: one structured-output call to OpenAI, cached on disk.

    rec, from_cache = cached_json_call(cache_dir, model, effort, system, schema, schema_name, user, salt="")

The cache key covers the model, reasoning effort, system prompt, schema, user
message and an optional salt (e.g. a run number, so repeated runs of the same
input are separate calls). Re-running costs nothing unless one of those changes.

Needs OPENAI_API_KEY: from the environment, or from .env in this pipeline's
folder (one line, OPENAI_API_KEY=...; git-ignored). Standard library only.
"""
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
_KEY = None


def api_key():
    global _KEY
    if _KEY:
        return _KEY
    if os.environ.get("OPENAI_API_KEY"):
        _KEY = os.environ["OPENAI_API_KEY"]
    elif ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("OPENAI_API_KEY="):
                _KEY = line.split("=", 1)[1].strip().strip('"')
    if not _KEY:
        sys.exit(f"OPENAI_API_KEY not set (environment or {ENV_FILE})")
    return _KEY


def prompt_version(system, schema):
    return hashlib.sha1((system + json.dumps(schema)).encode()).hexdigest()[:10]


def call_json(model, effort, system, schema, schema_name, user):
    """One chat completion with a strict JSON schema -> (parsed output, usage, model)."""
    body = json.dumps({
        "model": model, "reasoning_effort": effort,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "response_format": {"type": "json_schema", "json_schema": {"name": schema_name, "strict": True, "schema": schema}},
    }).encode()
    for attempt in range(6):
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body,
                                     headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                res = json.load(r)
            return json.loads(res["choices"][0]["message"]["content"]), res.get("usage", {}), res.get("model", model)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 5:
                time.sleep(3 * 2 ** attempt)
                continue
            raise RuntimeError(f"OpenAI {e.code}: {e.read().decode()[:300]}")
        except (urllib.error.URLError, TimeoutError):
            if attempt < 5:
                time.sleep(3 * 2 ** attempt)
                continue
            raise


EMBED_MODEL = "text-embedding-3-small"


def embed(texts, cache_dir, model=EMBED_MODEL):
    """Embedding vectors for texts, cached one file per model (text -> vector)."""
    path = Path(cache_dir) / f"embeddings_{model}.jsonl"
    cache = {}
    if path.exists():
        for line in open(path, encoding="utf-8"):
            r = json.loads(line)
            cache[r["text"]] = r["vector"]
    todo = sorted({t for t in texts if t not in cache})
    path.parent.mkdir(parents=True, exist_ok=True)
    for i in range(0, len(todo), 256):
        chunk = todo[i:i + 256]
        body = json.dumps({"model": model, "input": chunk}).encode()
        for attempt in range(6):
            req = urllib.request.Request("https://api.openai.com/v1/embeddings", data=body,
                                         headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    data = json.load(r)["data"]
                break
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
                if attempt == 5:
                    raise
                time.sleep(3 * 2 ** attempt)
        with open(path, "a", encoding="utf-8") as fh:
            for t, d in zip(chunk, data):
                cache[t] = d["embedding"]
                fh.write(json.dumps({"text": t, "vector": d["embedding"]}, ensure_ascii=False) + "\n")
    return [cache[t] for t in texts]


def cached_json_call(cache_dir, model, effort, system, schema, schema_name, user, salt=""):
    version = prompt_version(system, schema)
    key = f"{model}|{effort}|{version}|{user}" + (f"|{salt}" if salt else "")
    path = Path(cache_dir) / f"{hashlib.sha1(key.encode()).hexdigest()[:16]}.json"
    if path.exists():
        return json.load(open(path, encoding="utf-8")), True
    out, usage, served = call_json(model, effort, system, schema, schema_name, user)
    rec = {"input": user, "salt": salt, "output": out, "usage": usage, "model": served, "prompt_version": version}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec, False
