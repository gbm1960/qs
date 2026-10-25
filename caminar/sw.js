/**
 * Service Worker para "El Poder de Caminar" PWA
 * Proporciona soporte offline completo, sincronización y caché inteligente
 */

const CACHE_NAME = 'caminar-pwa-v1.1';
const DYNAMIC_CACHE = 'caminar-dynamic-v1.1';

// Recursos críticos locales para funcionamiento offline
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icons/favicon.svg',
  './icons/favicon-32x32.png',
  './icons/favicon-16x16.png',
  './icons/icon-192x192.png',
  './icons/icon-512x512.png',
  './icons/icon-maskable-192x192.png',
  './icons/icon-maskable-512x512.png',
  './icons/apple-touch-icon-180x180.png',
  './icons/apple-touch-icon.png',
  './screenshots/desktop.png',
  './screenshots/mobile.png'
];

// Librerías externas CDN necesarias para la app
const CDN_ASSETS = [
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/lucide@latest',
  'https://cdn.jsdelivr.net/gh/gitbrent/pptxgenjs@3.12.0/dist/pptxgen.bundle.js',
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap'
];

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      
      // 1. Guardar recursos estáticos locales
      await cache.addAll(STATIC_ASSETS);

      // 2. Guardar CDNs de forma segura (sin que un fallo en un CDN bloquee el install)
      await Promise.allSettled(
        CDN_ASSETS.map(async (url) => {
          try {
            const response = await fetch(url, { mode: 'cors' });
            if (response && response.status === 200) {
              await cache.put(url, response);
            }
          } catch (err) {
            console.warn(`[PWA SW] Pre-caching CDN falló silenciosamente para: ${url}`, err);
          }
        })
      );

      return self.skipWaiting();
    })()
  );
});

// Activación y limpieza de versiones obsoletas
self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const cacheNames = await caches.keys();
      await Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME && name !== DYNAMIC_CACHE) {
            console.log(`[PWA SW] Eliminando caché obsoleta: ${name}`);
            return caches.delete(name);
          }
        })
      );
      return self.clients.claim();
    })()
  );
});

// Interceptor de peticiones HTTP (Fetch)
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Evitar interceptar esquemas no soportados (ej. chrome-extension:)
  if (!url.protocol.startsWith('http')) return;

  // 1. Estrategia para navegación de páginas (HTML): Network-First con Fallback a Caché
  if (request.mode === 'navigate') {
    event.respondWith(
      (async () => {
        try {
          const networkResponse = await fetch(request);
          if (networkResponse && networkResponse.status === 200) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
            return networkResponse;
          }
          throw new Error('Network response not ok');
        } catch (error) {
          console.log('[PWA SW] Offline detectado para navegación, sirviendo desde caché');
          const cachedResponse = await caches.match(request);
          if (cachedResponse) return cachedResponse;
          
          const indexResponse = await caches.match('./index.html');
          if (indexResponse) return indexResponse;

          return caches.match('./');
        }
      })()
    );
    return;
  }

  // 2. Estrategia para fuentes de Google (fonts.gstatic.com) y CDNs: Cache-First con Network Fallback
  if (url.origin.includes('fonts.gstatic.com') ||
      url.origin.includes('fonts.googleapis.com') ||
      url.origin.includes('tailwindcss.com') ||
      url.origin.includes('unpkg.com') ||
      url.origin.includes('jsdelivr.net')) {
    event.respondWith(
      (async () => {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
          // Revalidación en segundo plano (Stale-While-Revalidate)
          fetch(request).then(async (networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              const dynamicCache = await caches.open(DYNAMIC_CACHE);
              dynamicCache.put(request, networkResponse);
            }
          }).catch(() => {/* modo offline, ignorar */});
          return cachedResponse;
        }

        try {
          const networkResponse = await fetch(request);
          if (networkResponse && networkResponse.status === 200) {
            const dynamicCache = await caches.open(DYNAMIC_CACHE);
            dynamicCache.put(request, networkResponse.clone());
          }
          return networkResponse;
        } catch (err) {
          // Si está offline y no está en caché
          return new Response('', { status: 408, statusText: 'Offline Fallback' });
        }
      })()
    );
    return;
  }

  // 3. Estrategia por defecto para imágenes, iconos y recursos locales: Cache-First
  event.respondWith(
    (async () => {
      const cachedResponse = await caches.match(request);
      if (cachedResponse) return cachedResponse;

      try {
        const networkResponse = await fetch(request);
        if (networkResponse && networkResponse.status === 200) {
          const dynamicCache = await caches.open(DYNAMIC_CACHE);
          dynamicCache.put(request, networkResponse.clone());
        }
        return networkResponse;
      } catch (err) {
        // En caso de fallo offline para imágenes, podemos devolver fallback si fuera necesario
        return cachedResponse || new Response('Recurso no disponible offline', { status: 503 });
      }
    })()
  );
});

// Notificaciones y mensajes internos
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
