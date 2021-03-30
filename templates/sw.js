/*
// Cache name
const CACHE_NAME = 'pwa-django-recipe';
// Cache targets
const urlsToCache = [
   'static/css/custom.css',
   'static/js/javascript.js',
   'media/',
];
self.addEventListener('install', (event) => {
 event.waitUntil(
   caches
     .open(CACHE_NAME)
     .then((cache) => {
       return cache.addAll(urlsToCache);
     })
 );
 
});
*/
self.addEventListener('fetch', (event) => {
  /*
 event.respondWith(
   caches
     .match(event.request)
     .then((response) => {
       return response ? response : fetch(event.request);
     })
     
 );
 */
});