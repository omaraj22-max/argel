/**
 * ARGEL · Receptor de leads (Google Apps Script · Web App)
 * --------------------------------------------------------
 * Recibe los formularios del catálogo (requisiciones) y de la landing de
 * distribuidores, y los escribe en dos pestañas de esta hoja de cálculo.
 *
 * Despliegue (una sola vez):
 *  1. Crea una Google Sheet nueva.
 *  2. Extensiones → Apps Script. Borra el contenido y pega ESTE archivo.
 *  3. Guarda. Implementar → Nueva implementación → tipo "Aplicación web".
 *       - Ejecutar como: Yo
 *       - Quién tiene acceso: Cualquier usuario
 *  4. Copia la URL que termina en /exec y pégala en config.js (LEAD_ENDPOINT).
 *
 * Para actualizar el código luego: Implementar → Administrar implementaciones →
 * editar (lápiz) → Versión: Nueva → Implementar. La URL /exec se mantiene.
 */

var TAB_REQUISICIONES = 'Requisiciones';
var TAB_DISTRIBUIDORES = 'Distribuidores-Leads';

var HEADERS_REQ = [
  'Fecha', 'Nombre', 'WhatsApp', 'Email', 'Tipo (estudiante/ejerce)',
  'Universidad/Clínica', 'Ciudad', 'Distribuidor', 'Tel. distribuidor',
  'Dirección distribuidor', 'Nota', 'Productos', '# Productos', 'Unidades'
];
var HEADERS_DIST = [
  'Fecha', 'Razón social', 'Contacto', 'WhatsApp', 'Email', 'Ciudad', '¿Ya distribuye?'
];

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    if (data.tipo_lead === 'distribuidor') {
      guardarDistribuidor(data);
    } else {
      guardarRequisicion(data);
    }
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json({ ok: true, service: 'ARGEL leads', ts: new Date().toISOString() });
}

function guardarRequisicion(d) {
  var sheet = hoja(TAB_REQUISICIONES, HEADERS_REQ);
  var productos = (d.productos || [])
    .map(function (p) { return p.cantidad + '× ' + p.nombre; })
    .join('\n');
  var unidades = (d.productos || []).reduce(function (a, p) { return a + (Number(p.cantidad) || 0); }, 0);
  sheet.appendRow([
    d.fecha || new Date().toISOString(),
    d.nombre || '', d.whatsapp || '', d.email || '', d.tipo || '',
    d.organizacion || '', d.ciudad || '', d.distribuidor || '',
    d.distribuidor_telefono || '', d.distribuidor_direccion || '',
    d.nota || '', productos, (d.productos || []).length, unidades
  ]);
}

function guardarDistribuidor(d) {
  var sheet = hoja(TAB_DISTRIBUIDORES, HEADERS_DIST);
  sheet.appendRow([
    d.fecha || new Date().toISOString(),
    d.razon_social || '', d.contacto || '', d.whatsapp || '',
    d.email || '', d.ciudad || '', d.ya_distribuye || ''
  ]);
}

/** Devuelve la pestaña creándola con encabezados si no existe. */
function hoja(nombre, headers) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(nombre);
  if (!sheet) {
    sheet = ss.insertSheet(nombre);
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
