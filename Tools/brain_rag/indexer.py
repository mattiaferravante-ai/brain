"""
Indicizza i file .md del Brain in un vector store ChromaDB locale.
Supporta indicizzazione completa e incrementale (solo file modificati).
"""

import hashlib
import json
import re
import sys
import time
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from config import (
    BRAIN_ROOT,
    CHROMA_DIR,
    CHUNK_MAX_TOKENS,
    CHUNK_OVERLAP_TOKENS,
    COLLECTION_NAME,
    DATA_DIR,
    EMBEDDING_MODEL,
    EXCLUDE_DIRS,
    STATE_FILE,
)


def should_exclude(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.relative_to(BRAIN_ROOT).parts)


def collect_md_files() -> list[Path]:
    return sorted(
        p for p in BRAIN_ROOT.rglob("*.md")
        if not should_exclude(p)
    )


def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def extract_metadata(path: Path, content: str) -> dict:
    rel = path.relative_to(BRAIN_ROOT).as_posix()
    parts = rel.split("/")

    meta = {
        "source": rel,
        "filename": path.stem,
    }

    if len(parts) > 1:
        meta["section"] = parts[0]
    if len(parts) > 2:
        meta["subsection"] = "/".join(parts[1:-1])

    tags = re.findall(r"#(\w[\w/-]*)", content)
    if tags:
        meta["tags"] = ",".join(tags[:10])

    wikilinks = re.findall(r"\[\[([^\]]+)\]\]", content)
    if wikilinks:
        meta["wikilinks"] = ",".join(wikilinks[:20])

    return meta


def strip_frontmatter(content: str) -> str:
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].strip()
    return content


def chunk_by_headings(content: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    content = strip_frontmatter(content)
    sections = re.split(r"(?=^#{1,3}\s)", content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]

    chunks = []
    for section in sections:
        words = section.split()
        if len(words) <= max_tokens:
            chunks.append(section)
        else:
            start = 0
            while start < len(words):
                end = start + max_tokens
                chunk_text = " ".join(words[start:end])
                chunks.append(chunk_text)
                start = end - overlap_tokens

    return chunks if chunks else [content.strip()] if content.strip() else []


def build_documents(files: list[Path]) -> tuple[list[str], list[str], list[dict]]:
    ids, documents, metadatas = [], [], []

    for path in files:
        content = path.read_text(encoding="utf-8", errors="replace")
        meta = extract_metadata(path, content)
        chunks = chunk_by_headings(content, CHUNK_MAX_TOKENS, CHUNK_OVERLAP_TOKENS)

        for i, chunk in enumerate(chunks):
            doc_id = f"{meta['source']}::chunk_{i}"
            prefix = "passage: "
            ids.append(doc_id)
            documents.append(prefix + chunk)
            metadatas.append({**meta, "chunk_index": i, "total_chunks": len(chunks)})

    return ids, documents, metadatas


def index(full: bool = False):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Modello embedding: {EMBEDDING_MODEL}")
    print("Caricamento modello (prima volta scarica ~1GB)...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if full:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
        state = {}
        print("Indicizzazione completa...")
    else:
        state = load_state()
        print("Indicizzazione incrementale...")

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    all_files = collect_md_files()
    print(f"File .md trovati: {len(all_files)}")

    current_hashes = {}
    to_index = []
    for f in all_files:
        h = file_hash(f)
        rel = f.relative_to(BRAIN_ROOT).as_posix()
        current_hashes[rel] = h
        if state.get(rel) != h:
            to_index.append(f)

    deleted = [rel for rel in state if rel not in current_hashes]
    if deleted:
        del_ids = [
            eid for eid in collection.get()["ids"]
            if any(eid.startswith(rel + "::") for rel in deleted)
        ]
        if del_ids:
            collection.delete(ids=del_ids)
            print(f"Rimossi {len(del_ids)} chunk da {len(deleted)} file eliminati")

    if not to_index:
        print("Nessun file modificato, indice aggiornato.")
        save_state(current_hashes)
        return

    print(f"File da (re)indicizzare: {len(to_index)}")

    for f in to_index:
        rel = f.relative_to(BRAIN_ROOT).as_posix()
        old_ids = [
            eid for eid in collection.get()["ids"]
            if eid.startswith(rel + "::")
        ]
        if old_ids:
            collection.delete(ids=old_ids)

    ids, documents, metadatas = build_documents(to_index)
    print(f"Chunk totali da indicizzare: {len(ids)}")

    t0 = time.time()
    raw_texts = [d for d in documents]
    embeddings = model.encode(raw_texts, show_progress_bar=True, normalize_embeddings=True)
    elapsed = time.time() - t0
    print(f"Embedding generati in {elapsed:.1f}s")

    batch_size = 100
    for i in range(0, len(ids), batch_size):
        collection.upsert(
            ids=ids[i:i + batch_size],
            documents=documents[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
            embeddings=embeddings[i:i + batch_size].tolist(),
        )

    save_state(current_hashes)
    total = collection.count()
    print(f"Indicizzazione completata. Chunk totali nel DB: {total}")


if __name__ == "__main__":
    full = "--full" in sys.argv
    index(full=full)
