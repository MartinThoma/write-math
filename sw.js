// Offline-first service worker.
// Every asset is served from the cache first and refreshed in the background
// (stale-while-revalidate). The weights file name contains a content hash, so
// model.json and the weights it references can never get out of sync.

const CACHE = "write-math-830ab150986c";
const SHELL = [
  "./",
  "index.html",
  "css/style.css",
  "js/app.js",
  "js/nn.js",
  "js/raster.js",
  "js/worker.js",
  "manifest.webmanifest",
  "icon.svg",
  "model/model.json",
];

async function cacheModel(cache, response) {
  const spec = await response.clone().json();
  const weightsUrl = new URL(`model/${spec.weights}`, self.registration.scope).href;
  if (!(await cache.match(weightsUrl))) await cache.add(weightsUrl);
  // Drop weights of older models.
  for (const req of await cache.keys()) {
    if (/\/model\/weights-[^/]+\.bin$/.test(req.url) && req.url !== weightsUrl) {
      await cache.delete(req);
    }
  }
}

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.addAll(SHELL);
    await cacheModel(cache, await cache.match("model/model.json"));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) if (key !== CACHE) await caches.delete(key);
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;

  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const cached = await cache.match(req, { ignoreSearch: true });
    const refresh = fetch(req).then(async (res) => {
      if (res.ok) {
        await cache.put(req, res.clone());
        if (req.url.endsWith("/model/model.json")) await cacheModel(cache, res);
      }
      return res;
    });
    if (cached) {
      event.waitUntil(refresh.catch(() => {}));
      return cached;
    }
    return refresh;
  })());
});
