// ============================================================
//  CONFIGURACIÓN DE LEADS — ARGEL
//  Pega aquí la URL del Web App de Apps Script (termina en /exec).
//  Mientras esté vacío, el sitio funciona en "modo demo": los leads
//  solo se imprimen en la consola del navegador (no se pierde nada).
//  Pasos de despliegue: ver apps-script/Codigo.gs y el README.
// ============================================================
const LEAD_ENDPOINT = "https://script.google.com/macros/s/AKfycbz6g9FHy3r3ooAo1fsk732WLcMp5w-H8BDv5gch5uE_ZWZA3NsJITJx-rx7JBhAJt85XA/exec";

/**
 * Envía el lead a la hoja de cálculo. Es "fire-and-forget": no bloquea la UI
 * y nunca rompe el flujo aunque la red falle (los leads no deben perderse de
 * vista del usuario). Usa text/plain para evitar el preflight CORS de Apps Script.
 */
function sendLead(payload) {
  if (!LEAD_ENDPOINT) {
    console.log('[ARGEL · modo demo] Lead capturado (configura LEAD_ENDPOINT para enviarlo a Sheets):', payload);
    return Promise.resolve({ demo: true });
  }
  return fetch(LEAD_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify(payload)
  }).catch(function (err) {
    console.error('No se pudo enviar el lead:', err);
  });
}
