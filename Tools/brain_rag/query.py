"""
CLI per interrogare il Brain via ricerca semantica.

Uso:
    python query.py "la mia domanda"
    python query.py "la mia domanda" --top 10
    python query.py "la mia domanda" --filter section=Work
"""

import argparse
import sys

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K


def query(text: str, top_k: int = TOP_K, where: dict | None = None) -> list[dict]:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    model = SentenceTransformer(EMBEDDING_MODEL)
    embedding = model.encode(["query: " + text], normalize_embeddings=True)

    params = {
        "query_embeddings": embedding.tolist(),
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        params["where"] = where

    results = collection.query(**params)

    output = []
    for i in range(len(results["ids"][0])):
        doc = results["documents"][0][i]
        if doc.startswith("passage: "):
            doc = doc[9:]

        output.append({
            "id": results["ids"][0][i],
            "source": results["metadatas"][0][i].get("source", ""),
            "score": 1 - results["distances"][0][i],
            "metadata": results["metadatas"][0][i],
            "content": doc,
        })

    return output


def parse_filter(filter_str: str) -> dict:
    key, value = filter_str.split("=", 1)
    return {key.strip(): value.strip()}


def main():
    parser = argparse.ArgumentParser(description="Query the Brain RAG")
    parser.add_argument("question", help="Domanda da cercare")
    parser.add_argument("--top", type=int, default=TOP_K, help=f"Numero di risultati (default: {TOP_K})")
    parser.add_argument("--filter", type=str, help="Filtro metadata key=value (es. section=Work)")
    parser.add_argument("--context", action="store_true", help="Output formattato per iniezione in prompt LLM")
    args = parser.parse_args()

    where = parse_filter(args.filter) if args.filter else None
    results = query(args.question, top_k=args.top, where=where)

    if not results:
        print("Nessun risultato trovato.")
        sys.exit(0)

    if args.context:
        print("--- CONTESTO RAG ---")
        for r in results:
            print(f"\n[{r['source']}] (score: {r['score']:.3f})")
            print(r["content"])
        print("\n--- FINE CONTESTO ---")
    else:
        for i, r in enumerate(results, 1):
            print(f"\n{'='*60}")
            print(f"#{i}  {r['source']}  (score: {r['score']:.3f})")
            tags = r["metadata"].get("tags", "")
            if tags:
                print(f"     tags: {tags}")
            print(f"{'-'*60}")
            print(r["content"][:500])
            if len(r["content"]) > 500:
                print("...")


if __name__ == "__main__":
    main()
