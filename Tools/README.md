# Tools

Script e automazioni locali per il Brain.

## brain_rag/

RAG (Retrieval-Augmented Generation) locale per il Brain. Indicizza tutti i file `.md` in un vector store ChromaDB con embedding `multilingual-e5-base` via sentence-transformers. Tutto gira in locale, nessun dato esce dalla macchina.

### Setup

```bash
cd Tools/brain_rag
pip install -r requirements.txt
```

### Uso

```bash
# Prima indicizzazione (scarica modello ~1GB la prima volta)
python indexer.py --full

# Aggiornamento incrementale (solo file modificati)
python indexer.py

# Query
python query.py "come funziona il modulo tea_quotations"

# Query con più risultati
python query.py "fatturazione" --top 10

# Query filtrata per sezione
python query.py "odoo 19" --filter section=Learning

# Output formattato per iniezione in prompt LLM
python query.py "dealer website piaggio" --context
```
