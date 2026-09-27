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

const server = http.createServer((req, res) => {
  if (req.url === '/healthz') {
    res.writeHead(200, { 'content-type': 'text/plain' });
    res.end('ok');
    return;
  }
  serve(req, res, () => {
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end('not found');
  });
});

server.listen(PORT, () => {
  console.log(`[hub] listening on :${PORT}`);
});
