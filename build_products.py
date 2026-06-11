#!/usr/bin/env python3
"""Convierte Catalogo_ARGEL.csv -> products.js (const PRODUCTS = [...])."""
import csv, json, re, os, unicodedata

CSV_PATH = os.path.expanduser("~/Desktop/Argel/Catalogo_ARGEL.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "products.js")


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:48] or "producto"


SMALL = {"de", "para", "con", "y", "o", "la", "el", "los", "las", "del", "en", "a"}
# Acrónimos / códigos sin dígitos que deben conservarse en mayúsculas.
KEEP = {"ARGEL", "HQ", "XCP", "FG", "UV", "USB", "LED", "OLED", "BPA", "MDP", "PVC", "XS"}


def title_case(name):
    """Suaviza nombres en MAYÚSCULAS a tipo título, preservando acrónimos y códigos."""
    alpha = [c for c in name if c.isalpha()]
    upper_ratio = (sum(1 for c in alpha if c.isupper()) / len(alpha)) if alpha else 0
    if upper_ratio < 0.6:
        return name  # ya viene en mezcla de mayúsculas/minúsculas: respétalo
    out = []
    for i, w in enumerate(name.split()):
        core = re.sub(r"[^A-Za-zÁÉÍÓÚÑáéíóúñ]", "", w)
        if re.search(r"\d", w) or w.upper() in KEEP or core.upper() in KEEP:
            out.append(w)                       # códigos: C/12, UNC-15, PPR3, 360°, HQ, XCP…
        else:
            lw = w.lower()
            if i != 0 and lw in SMALL:
                out.append(lw)
            else:
                m = re.search(r"[a-zñáéíóú]", lw)  # primera letra real (ignora "(", "¿", etc.)
                out.append(lw[:m.start()] + lw[m.start()].upper() + lw[m.start()+1:] if m else lw)
    name = " ".join(out)
    return re.sub(r"\bargel\b", "ARGEL", name, flags=re.I)


products = []
cats_order = []
with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        num = (row.get("#") or "").strip()
        if not num:
            continue
        name = title_case((row.get("Producto") or "").strip())
        cat = (row.get("Categoria") or "").strip()
        desc = (row.get("Descripcion") or "").strip()
        url = (row.get("URL_producto") or "").strip()
        img = (row.get("URL_imagen") or "").strip()
        if cat and cat not in cats_order:
            cats_order.append(cat)
        products.append({
            "id": f"p{num}-{slugify(row.get('Producto') or num)}",
            "n": int(num),
            "name": name,
            "cat": cat,
            "desc": desc,
            "url": url,
            "img": img,
        })

js = (
    "// Generado automáticamente desde Catalogo_ARGEL.csv — no editar a mano.\n"
    "const PRODUCTS = " + json.dumps(products, ensure_ascii=False, indent=0) + ";\n"
    "const CATEGORIES = " + json.dumps(cats_order, ensure_ascii=False) + ";\n"
)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(js)

print(f"{len(products)} productos, {len(cats_order)} categorías -> {OUT_PATH}")
print("Categorías:", cats_order)
