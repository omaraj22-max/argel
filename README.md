# Argel · Catálogo digital para dentistas

Sitio estático de **Argel — Odontología profesional**. Catálogo clínico con flujo de
requisición (sin precios: el distribuidor cotiza) y landing de captación de distribuidores.

## Páginas

| Archivo | Descripción |
|---|---|
| [`index.html`](index.html) | Catálogo SPA: filtros por categoría + búsqueda, ficha de producto, requisición, selección de distribuidor por geolocalización y captura de lead. |
| [`distribuidores.html`](distribuidores.html) | Landing "Soy distribuidor": propuesta de valor, pilares, cómo funciona y formulario de alta. |
| [`products.js`](products.js) | 112 productos generados desde el catálogo (no editar a mano). |
| [`build_products.py`](build_products.py) | Convierte `Catalogo_ARGEL.csv` → `products.js`. |

## Regenerar el catálogo

Coloca `Catalogo_ARGEL.csv` en `~/Desktop/Argel/` y ejecuta:

```bash
python3 build_products.py
```

Columnas esperadas: `#, Producto, Categoria, Precio_MXN, Descripcion, URL_producto, URL_imagen`.
Los precios **no** se muestran en el sitio (modelo "tu distribuidor cotiza").

## Desarrollo local

```bash
python3 -m http.server 4185
# abre http://localhost:4185
```

## Puesta en producción (leads)

Las funciones `submitReq()` (index) y `submitDist()` (distribuidores) ya construyen el
`payload` del lead y lo imprimen en consola. Para enviarlo a Google Sheets, descomenta el
bloque `fetch(...)` y reemplaza la URL del Web App de Apps Script.

## Stack

HTML + CSS + JS vanilla. Sin build. Tipografías Montserrat + Inter (Google Fonts).
Paleta de marca: navy `#072B5B`, sky `#28B7E8`.
