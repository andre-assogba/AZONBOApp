const CACHE = 'azonbo-v1';
const URLS = ['/'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(URLS)));
});

self.addEventListener('fetch', e => {
  if (e.request.mode === 'navigate') return;
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});