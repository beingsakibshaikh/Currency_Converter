const CACHE_NAME = 'currencypro-v1';
const urlsToCache = [
  '/',
  '/static/converter/css/styles.css',
  '/static/converter/js/main.js',
  '/static/converter/icons/icon-192.png',
  '/static/converter/icons/icon-512.png',
  // add any routes or assets you want to cache
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
