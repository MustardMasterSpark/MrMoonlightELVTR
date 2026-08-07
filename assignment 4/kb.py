"""
Knowledge base and retrieval for the Mr. Moonlight content pipeline.

No model is called anywhere in this file, and nothing is imported beyond the
standard library.

RETRIEVAL CHOICE. This uses BM25 sparse retrieval rather than dense vector
embeddings. That is a deliberate decision, not a shortcut:

  1. Anthropic does not serve an embeddings endpoint, so a dense pipeline would
     need a second vendor and a second API key. This runs on one credential.
  2. BM25 is deterministic. The same query returns the same chunks every time,
     which is what makes the retrieval trace in output/06_rag_trace.md
     reproducible and auditable rather than a snapshot.
  3. The corpus is two documents totalling roughly 97 KB. Dense retrieval earns
     its complexity on large heterogeneous corpora; on a corpus this size with
     a shared, highly specific vocabulary — Tracey, Rylee, Furman, Aanniarvik,
     the Glade — lexical overlap is a strong signal.

The tradeoff is real and worth stating: BM25 matches words, not meaning. A query
for "fear" will not retrieve a chunk that only says "dread". Queries are
therefore built from the script's own vocabulary, which is where the surrounding
pipeline gets its accuracy.
"""

import json
import math
import re
from pathlib import Path

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "do", "for",
    "from", "has", "have", "he", "her", "his", "i", "if", "in", "into", "is",
    "it", "its", "of", "on", "or", "she", "that", "the", "their", "them",
    "there", "they", "this", "to", "was", "were", "what", "when", "which",
    "who", "will", "with", "you", "your",
}

TOKEN_RE = re.compile(r"[a-z0-9']+")


def tokenize(text):
    return [t for t in TOKEN_RE.findall(text.lower())
            if t not in STOPWORDS and len(t) > 1]


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def chunk_gdd(text, max_chars=1400):
    """Split the GDD on its bold section headings, then on paragraphs if a
    section runs long. Section titles are kept on the chunk because they carry
    most of the retrievable signal."""
    chunks = []
    current_title, buffer = "Front matter", []

    def flush():
        body = "\n".join(buffer).strip()
        if not body:
            return
        if len(body) <= max_chars:
            chunks.append((current_title, body))
            return
        piece = []
        size = 0
        for paragraph in body.split("\n"):
            if size + len(paragraph) > max_chars and piece:
                chunks.append((current_title, "\n".join(piece).strip()))
                piece, size = [], 0
            piece.append(paragraph)
            size += len(paragraph)
        if piece:
            chunks.append((current_title, "\n".join(piece).strip()))

    # pdftotext output: headings are short ALL-CAPS lines. Page furniture from
    # the PDF header and footer is dropped so it cannot pollute retrieval.
    heading_re = re.compile(r"^([A-Z][A-Z0-9 ,.·—\'&()\-]{5,60})$")
    noise_re = re.compile(r"(MR\. MOONLIGHT \(MVP\)|GAME DESIGN DOCUMENT\s+·|^\s*\d{1,3}\s*$|^\x0c)")

    for raw in text.splitlines():
        line = raw.replace("\x0c", "").rstrip()
        if noise_re.search(line):
            continue
        stripped = line.strip()
        heading = heading_re.match(stripped)
        if heading and len(stripped.split()) <= 9:
            flush()
            current_title = re.sub(r"\s+", " ", heading.group(1)).strip(": ")
            buffer = []
            continue
        buffer.append(line)
    flush()

    return [
        {"id": f"GDD#{i:03d}", "source": "GDD", "section": title, "text": body}
        for i, (title, body) in enumerate(chunks)
    ]


def chunk_script(text):
    """One chunk per scene. Scene boundaries live in HTML comments, so they are
    read here before comments are stripped for any other purpose."""
    chunks = []
    scene_no, scene_title, buffer = 0, "Front matter", []

    def flush():
        body = "\n".join(buffer).strip()
        if body:
            chunks.append((scene_no, scene_title, body))

    for line in text.splitlines():
        banner = re.search(r"SCENE\s+(\d+)\s+—\s+(.+?)\s*$", line)
        if banner:
            flush()
            scene_no = int(banner.group(1))
            scene_title = banner.group(2).replace("[OUTLINE]", "").strip()
            buffer = []
            continue
        if line.strip().startswith("<!--") or line.strip().startswith("-->"):
            continue
        buffer.append(line)
    flush()

    return [
        {"id": f"L01#S{no:02d}", "source": "L01", "section": f"Scene {no:02d} — {title}",
         "text": body}
        for no, title, body in chunks
    ]


# ---------------------------------------------------------------------------
# BM25
# ---------------------------------------------------------------------------

class BM25:
    def __init__(self, chunks, k1=1.5, b=0.75):
        self.chunks = chunks
        self.k1, self.b = k1, b
        self.docs = [tokenize(c["section"] + " " + c["text"]) for c in chunks]
        self.lengths = [len(d) for d in self.docs]
        self.avg_len = (sum(self.lengths) / len(self.lengths)) if self.lengths else 0.0

        self.freqs = []
        document_freq = {}
        for doc in self.docs:
            counts = {}
            for token in doc:
                counts[token] = counts.get(token, 0) + 1
            self.freqs.append(counts)
            for token in counts:
                document_freq[token] = document_freq.get(token, 0) + 1

        total = len(self.docs)
        self.idf = {
            token: math.log(1 + (total - freq + 0.5) / (freq + 0.5))
            for token, freq in document_freq.items()
        }

    def search(self, query, top_k=4):
        terms = tokenize(query)
        scored = []
        for index, counts in enumerate(self.freqs):
            score = 0.0
            matched = []
            for term in terms:
                if term not in counts:
                    continue
                freq = counts[term]
                norm = 1 - self.b + self.b * (self.lengths[index] / (self.avg_len or 1))
                score += self.idf.get(term, 0.0) * (freq * (self.k1 + 1)) / (
                    freq + self.k1 * norm)
                matched.append(term)
            if score > 0:
                scored.append((score, index, sorted(set(matched))))
        scored.sort(key=lambda s: -s[0])

        results = []
        for score, index, matched in scored[:top_k]:
            chunk = dict(self.chunks[index])
            chunk["score"] = round(score, 3)
            chunk["matched_terms"] = matched
            results.append(chunk)
        return results


# ---------------------------------------------------------------------------
# Public surface
# ---------------------------------------------------------------------------

class KnowledgeBase:
    def __init__(self, knowledge_dir):
        directory = Path(knowledge_dir)
        gdd = (directory / "GDD.md").read_text(encoding="utf-8")
        script = (directory / "L01.txt").read_text(encoding="utf-8")

        self.chunks = chunk_gdd(gdd) + chunk_script(script)
        self.index = BM25(self.chunks)
        self.trace = []

    def stats(self):
        gdd = sum(1 for c in self.chunks if c["source"] == "GDD")
        script = len(self.chunks) - gdd
        return {"total_chunks": len(self.chunks), "gdd_chunks": gdd,
                "script_chunks": script,
                "avg_chunk_chars": round(
                    sum(len(c["text"]) for c in self.chunks) / len(self.chunks))}

    def retrieve(self, query, top_k=4, purpose=""):
        """Retrieve and record. Every retrieval is logged so the trace document
        can show query, chunk and output side by side."""
        results = self.index.search(query, top_k=top_k)
        self.trace.append({
            "purpose": purpose,
            "query": query,
            "retrieved": [
                {"id": r["id"], "section": r["section"], "score": r["score"],
                 "matched_terms": r["matched_terms"],
                 "excerpt": r["text"][:600]}
                for r in results
            ],
        })
        return results

    def as_context(self, results, max_chars=5000):
        parts, size = [], 0
        for r in results:
            block = f"[{r['id']} — {r['section']}]\n{r['text']}"
            if size + len(block) > max_chars:
                block = block[:max_chars - size]
                parts.append(block)
                break
            parts.append(block)
            size += len(block)
        return "\n\n".join(parts)

    def attach_output(self, purpose, output_excerpt):
        """Bind a generated excerpt to the retrieval that produced it."""
        for entry in reversed(self.trace):
            if entry["purpose"] == purpose and "output" not in entry:
                entry["output"] = output_excerpt
                return

    def dump_trace(self, path):
        Path(path).write_text(json.dumps(self.trace, indent=2), encoding="utf-8")


if __name__ == "__main__":
    kb = KnowledgeBase(Path(__file__).parent / "knowledge")
    print(json.dumps(kb.stats(), indent=2))
    for query in ["Tracey personality addict grumpy",
                  "wolves pack attack behaviour",
                  "art style low poly textures palette"]:
        print(f"\nQUERY: {query}")
        for r in kb.retrieve(query, top_k=3):
            print(f"  {r['id']:12} {r['score']:6.2f}  {r['section'][:50]}")
