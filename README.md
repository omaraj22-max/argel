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

## Leads → Google Sheets

Los formularios ya envían el lead mediante `sendLead()` ([`config.js`](config.js)).
Mientras `LEAD_ENDPOINT` esté vacío, el sitio corre en **modo demo** (el lead solo se
imprime en consola; nada se rompe). Para conectarlo a una hoja de cálculo:

1. Crea una Google Sheet nueva.
2. **Extensiones → Apps Script**, borra todo y pega [`apps-script/Codigo.gs`](apps-script/Codigo.gs). Guarda.
3. **Implementar → Nueva implementación → Aplicación web**
   - Ejecutar como: **Yo**
   - Quién tiene acceso: **Cualquier usuario**
4. Copia la URL que termina en `/exec` y pégala en [`config.js`](config.js):
   ```js
   const LEAD_ENDPOINT = "https://script.google.com/macros/s/XXXXX/exec";
   ```
5. Listo. Las requisiciones del catálogo caen en la pestaña **Requisiciones** (con
   distribuidor, teléfono, dirección, productos y unidades) y las altas de la landing
   en **Distribuidores-Leads**. Las pestañas y encabezados se crean solos.

Para actualizar el código del script después: **Administrar implementaciones → editar →
Versión: Nueva → Implementar** (la URL `/exec` no cambia).

## Stack

HTML + CSS + JS vanilla. Sin build. Tipografías Montserrat + Inter (Google Fonts).
Paleta de marca: navy `#072B5B`, sky `#28B7E8`.
