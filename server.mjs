import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sirv from 'sirv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 8080;

const serve = sirv(path.join(__dirname, 'dist'), {
  dev: false,
  etag: true,
  maxAge: 60,
  immutable: false,
  gzip: true,
});

// The site is static and its only third party is Google Fonts. Everything else
// is same-origin, so the policy can be tight: no framing, no plugins, no forms,
// scripts only from this origin. Inline styles are allowed because the page sets
// style attributes; the hub-data block is JSON, not script, so it is unaffected.
const CSP = [
  "default-src 'self'",
  "script-src 'self'",
  "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
  "font-src https://fonts.gstatic.com",
  "img-src 'self' data:",
  "connect-src 'self'",
  "object-src 'none'",
  "base-uri 'none'",
  "form-action 'none'",
  "frame-ancestors 'none'",
].join('; ');

const SECURITY_HEADERS = {
  'content-security-policy': CSP,
  'x-content-type-options': 'nosniff',
  'referrer-policy': 'strict-origin-when-cross-origin',
  'permissions-policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=()',
  'cross-origin-opener-policy': 'same-origin',
  'strict-transport-security': 'max-age=15552000',
};

const server = http.createServer((req, res) => {
  for (const [k, v] of Object.entries(SECURITY_HEADERS)) res.setHeader(k, v);

  // Read-only site: nothing here accepts a body.
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { allow: 'GET, HEAD', 'content-type': 'text/plain' });
    res.end('method not allowed');
    return;
  }
  if (req.url === '/healthz') {
    res.writeHead(200, { 'content-type': 'text/plain', 'cache-control': 'no-store' });
    res.end('ok');
    return;
  }
  serve(req, res, () => {
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end('not found');
  });
});

// Drop slow or oversized requests instead of holding sockets open.
server.headersTimeout = 15_000;
server.requestTimeout = 30_000;
server.maxHeadersCount = 50;

server.listen(PORT, () => {
  console.log(`[hub] listening on :${PORT}`);
});
