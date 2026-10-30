"""Importe les questions CSS de freeCodeCamp/developer_quiz_site (licence BSD-3-Clause)
dans public/data/qcm-css.json, avec attribution (champs `source` et `license`).

Usage : python3 scripts/import_fcc_css.py <chemin/vers/css-quiz.ts>
Le fichier source est traité comme de la donnée : il est analysé par expressions
régulières, jamais exécuté. L'import est idempotent (les anciennes entrées importées
sont remplacées). Exécuter build_qcm_other.py avant pour repartir des questions originales.
"""
import json, pathlib, random, re, sys

SOURCE = "freeCodeCamp/developer_quiz_site (src/data/css-quiz.ts)"
LICENSE = "BSD-3-Clause"
target = pathlib.Path(__file__).resolve().parent.parent / "public/data/qcm-css.json"
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")

field = re.compile(r'(\w+):\s*"((?:[^"\\]|\\.)*)"', re.S)
blocks = re.findall(r"\{(.*?)\n  \}", text, re.S)
rng = random.Random(42)  # ordre des options reproductible

imported = []
for block in blocks:
    f = {k: json.loads(f'"{v}"') for k, v in field.findall(block)}
    if not all(k in f for k in ("Question", "Answer", "Distractor1", "Distractor2", "Distractor3")):
        continue
    options = [f["Answer"], f["Distractor1"], f["Distractor2"], f["Distractor3"]]
    order = list(range(4)); rng.shuffle(order)
    shuffled = [options[i] for i in order]
    imported.append({
        "id": f"css-fcc-{len(imported) + 1:03d}",
        "category": "css",
        "difficulty": "easy",
        "question": " ".join(f["Question"].split()),
        "options": shuffled,
        "answer": [order.index(0)],
        "explanation": " ".join(f.get("Explanation", "").split()) or f"Bonne réponse : {f['Answer']}.",
        "source": SOURCE,
        "license": LICENSE,
    })

existing = [q for q in json.loads(target.read_text(encoding="utf-8")) if "source" not in q]
target.write_text(json.dumps(existing + imported, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(existing)} originales + {len(imported)} importées")
