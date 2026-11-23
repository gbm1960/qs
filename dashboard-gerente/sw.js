/**
 * Service Worker para "Dashboard Gerente | Quadratic Solutions" PWA
 * Proporciona soporte offline, sincronización y caché inteligente
 */

const CACHE_NAME = 'dashboard-gerente-v1.1';
const DYNAMIC_CACHE = 'dashboard-gerente-dynamic-v1.1';

const ALLOWED_CDN_HOSTS = new Set([
  'fonts.gstatic.com',
  'fonts.googleapis.com',
  'cdn.tailwindcss.com',
  'cdnjs.cloudflare.com'
]);

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
  './icons/apple-touch-icon.png'
];

const CDN_ASSETS = [
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Urbanist:wght@400;600;700&display=swap'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);

      await Promise.allSettled(
        STATIC_ASSETS.map(async (assetUrl) => {
          try {
            const res = await fetch(assetUrl, { cache: 'reload' });
            if (res && res.status === 200) {
              await cache.put(assetUrl, res);
            }
          } catch (e) {
            console.warn('[PWA SW] Fallo al cachear recurso local:', assetUrl, e);
          }
        })
      );

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

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const cacheNames = await caches.keys();
      await Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME && name !== DYNAMIC_CACHE) {
            return caches.delete(name);
          }
        })
      );
      return self.clients.claim();
    })()
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (!url.protocol.startsWith('http')) return;

  if (request.mode === 'navigate') {
    event.respondWith(
      (async () => {
        try {
          const networkResponse = await fetch(request, { cache: 'no-cache' });
          if (networkResponse && networkResponse.status === 200) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
            return networkResponse;
          }
          throw new Error('Network response not ok');
        } catch (error) {
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

  if (request.method === 'GET' && ALLOWED_CDN_HOSTS.has(url.hostname)) {
    event.respondWith(
      (async () => {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
          fetch(request).then(async (networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              const dynamicCache = await caches.open(DYNAMIC_CACHE);
              dynamicCache.put(request, networkResponse);
            }
          }).catch(() => {});
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
          return new Response('', { status: 408, statusText: 'Offline Fallback' });
        }
      })()
    );
    return;
  }

  if (request.method !== 'GET' || url.origin !== self.location.origin) {
    return;
  }

  event.respondWith(
    (async () => {
      const cachedResponse = await caches.match(request);
      if (cachedResponse) return cachedResponse;

      try {
        const networkResponse = await fetch(request);
        if (networkResponse && networkResponse.status === 200 && request.method === 'GET' && url.origin === self.location.origin) {
          const dynamicCache = await caches.open(DYNAMIC_CACHE);
          dynamicCache.put(request, networkResponse.clone());
        }
        return networkResponse;
      } catch (err) {
        return cachedResponse || new Response('Recurso no disponible offline', { status: 503 });
      }
    })()
  );
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
