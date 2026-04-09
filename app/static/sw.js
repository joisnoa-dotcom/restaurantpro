// Un Service Worker básico y seguro para RestaurantPro
// No guarda caché agresivo para evitar pedidos fantasma o desactualizados.

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

// Pasa todas las peticiones directo a la red (Network Only)
self.addEventListener('fetch', (event) => {
    event.respondWith(fetch(event.request));
});