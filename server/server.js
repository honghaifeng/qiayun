const crypto = require('crypto');
const fs = require('fs/promises');
const http = require('http');
const path = require('path');
const { URL } = require('url');

const rootDir = path.resolve(__dirname, '..');
const publicDir = path.join(rootDir, 'website');
const dataDir = process.env.QIAYUN_DATA_DIR || path.join(rootDir, 'data');
const inquiriesFile = path.join(dataDir, 'inquiries.json');
const port = Number(process.env.PORT || 3000);
const adminPassword = process.env.ADMIN_PASSWORD || 'qiayun-admin';
const sessionSecret = process.env.SESSION_SECRET || crypto.randomBytes(32).toString('hex');
const maxBodySize = 64 * 1024;
const sessions = new Map();

const contentTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml; charset=utf-8',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8'
};

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  });
  res.end(JSON.stringify(payload));
}

function sendText(res, statusCode, text) {
  res.writeHead(statusCode, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end(text);
}

function parseCookies(req) {
  return Object.fromEntries((req.headers.cookie || '').split(';').map(item => {
    const index = item.indexOf('=');
    if (index === -1) return null;
    return [item.slice(0, index).trim(), decodeURIComponent(item.slice(index + 1))];
  }).filter(Boolean));
}

function sign(value) {
  return crypto.createHmac('sha256', sessionSecret).update(value).digest('hex');
}

function createSession() {
  const id = crypto.randomUUID();
  const expiresAt = Date.now() + 7 * 24 * 60 * 60 * 1000;
  sessions.set(id, expiresAt);
  return `${id}.${sign(id)}`;
}

function isAuthenticated(req) {
  const token = parseCookies(req).qy_admin;
  if (!token) return false;
  const [id, signature] = token.split('.');
  if (!id || signature !== sign(id)) return false;
  const expiresAt = sessions.get(id);
  if (!expiresAt || expiresAt < Date.now()) {
    sessions.delete(id);
    return false;
  }
  return true;
}

function safeEqual(left, right) {
  const leftBuffer = Buffer.from(left);
  const rightBuffer = Buffer.from(right);
  return leftBuffer.length === rightBuffer.length && crypto.timingSafeEqual(leftBuffer, rightBuffer);
}

async function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.setEncoding('utf8');
    req.on('data', chunk => {
      body += chunk;
      if (Buffer.byteLength(body) > maxBodySize) {
        reject(new Error('REQUEST_TOO_LARGE'));
        req.destroy();
      }
    });
    req.on('end', () => resolve(body));
    req.on('error', reject);
  });
}

function cleanText(value, maxLength) {
  return String(value || '').replace(/\s+/g, ' ').trim().slice(0, maxLength);
}

function cleanMessage(value) {
  return String(value || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim().slice(0, 3000);
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

async function loadInquiries() {
  try {
    const text = await fs.readFile(inquiriesFile, 'utf8');
    const data = JSON.parse(text);
    return Array.isArray(data) ? data : [];
  } catch (error) {
    if (error.code === 'ENOENT') return [];
    throw error;
  }
}

async function saveInquiries(inquiries) {
  await fs.mkdir(dataDir, { recursive: true });
  await fs.writeFile(inquiriesFile, JSON.stringify(inquiries, null, 2));
}

async function handleInquiry(req, res) {
  try {
    const rawBody = await readBody(req);
    const payload = JSON.parse(rawBody || '{}');
    const inquiry = {
      id: crypto.randomUUID(),
      name: cleanText(payload.name, 120),
      email: cleanText(payload.email, 160),
      phone: cleanText(payload.phone, 80),
      company: cleanText(payload.company, 160),
      message: cleanMessage(payload.message),
      lang: cleanText(payload.lang, 20),
      page: cleanText(payload.page, 300),
      userAgent: cleanText(req.headers['user-agent'], 300),
      ip: cleanText(req.headers['x-forwarded-for'] || req.socket.remoteAddress, 120),
      createdAt: new Date().toISOString()
    };

    if (!inquiry.name) return sendJson(res, 400, { ok: false, message: 'Name is required.' });
    if (!isValidEmail(inquiry.email)) return sendJson(res, 400, { ok: false, message: 'A valid email is required.' });

    const inquiries = await loadInquiries();
    inquiries.unshift(inquiry);
    await saveInquiries(inquiries.slice(0, 1000));
    sendJson(res, 201, { ok: true, id: inquiry.id });
  } catch (error) {
    if (error.message === 'REQUEST_TOO_LARGE') return sendJson(res, 413, { ok: false, message: 'Request is too large.' });
    if (error instanceof SyntaxError) return sendJson(res, 400, { ok: false, message: 'Invalid JSON.' });
    console.error(error);
    sendJson(res, 500, { ok: false, message: 'Server error.' });
  }
}

async function handleAdminLogin(req, res) {
  try {
    const payload = JSON.parse(await readBody(req) || '{}');
    if (!safeEqual(String(payload.password || ''), adminPassword)) {
      return sendJson(res, 401, { ok: false, message: 'Invalid password.' });
    }
    const token = createSession();
    res.writeHead(200, {
      'Content-Type': 'application/json; charset=utf-8',
      'Set-Cookie': `qy_admin=${encodeURIComponent(token)}; HttpOnly; SameSite=Lax; Path=/; Max-Age=604800`,
      'Cache-Control': 'no-store'
    });
    res.end(JSON.stringify({ ok: true }));
  } catch (error) {
    sendJson(res, 400, { ok: false, message: 'Invalid login request.' });
  }
}

async function handleAdminLogout(req, res) {
  const token = parseCookies(req).qy_admin;
  if (token) sessions.delete(token.split('.')[0]);
  res.writeHead(200, {
    'Content-Type': 'application/json; charset=utf-8',
    'Set-Cookie': 'qy_admin=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0',
    'Cache-Control': 'no-store'
  });
  res.end(JSON.stringify({ ok: true }));
}

async function handleAdminInquiries(req, res) {
  if (!isAuthenticated(req)) return sendJson(res, 401, { ok: false, message: 'Unauthorized.' });
  const inquiries = await loadInquiries();
  sendJson(res, 200, { ok: true, inquiries });
}

async function serveStatic(req, res, pathname) {
  let relativePath = decodeURIComponent(pathname);
  if (relativePath === '/') relativePath = '/index.html';
  if (relativePath === '/admin') relativePath = '/admin/index.html';
  const filePath = path.normalize(path.join(publicDir, relativePath));
  if (!filePath.startsWith(publicDir)) return sendText(res, 403, 'Forbidden');

  try {
    const stat = await fs.stat(filePath);
    if (stat.isDirectory()) return serveStatic(req, res, path.join(pathname, 'index.html'));
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, {
      'Content-Type': contentTypes[ext] || 'application/octet-stream',
      'Cache-Control': ext === '.html' ? 'no-cache' : 'public, max-age=3600'
    });
    const buffer = await fs.readFile(filePath);
    res.end(buffer);
  } catch (error) {
    if (error.code === 'ENOENT') return sendText(res, 404, 'Not Found');
    console.error(error);
    sendText(res, 500, 'Server error');
  }
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === 'POST' && url.pathname === '/api/inquiries') return handleInquiry(req, res);
  if (req.method === 'POST' && url.pathname === '/api/admin/login') return handleAdminLogin(req, res);
  if (req.method === 'POST' && url.pathname === '/api/admin/logout') return handleAdminLogout(req, res);
  if (req.method === 'GET' && url.pathname === '/api/admin/inquiries') return handleAdminInquiries(req, res);
  if (!['GET', 'HEAD'].includes(req.method)) return sendText(res, 405, 'Method Not Allowed');

  return serveStatic(req, res, url.pathname);
});

server.listen(port, () => {
  console.log(`QiaYun website running at http://localhost:${port}`);
  console.log(`Admin panel: http://localhost:${port}/admin`);
});
