// ui/dashboard/server.js
const express = require('express');
const path = require('path');
const fs = require('fs');

const ORCH_URL = process.env.ORCHESTRATOR_URL || 'http://orchestrator:8000';
const app = express();

// Serve static files from either ./public or the repo root of the UI
const publicDir = fs.existsSync(path.join(__dirname, 'public'))
  ? path.join(__dirname, 'public')
  : __dirname;

app.use(express.static(publicDir));

// Small fetch forwarder (Node 18+ has global fetch)
async function forward(res, url) {
  try {
    const r = await fetch(url);
    const body = await r.text();
    res
      .status(r.status)
      .type(r.headers.get('content-type') || 'application/json')
      .send(body);
  } catch (err) {
    res.status(500).json({ error: String(err), target: url });
  }
}

// API proxies used by the dashboard
app.get('/api/agents', (_req, res) => forward(res, `${ORCH_URL}/agents`));
app.get('/api/approvals', (_req, res) => forward(res, `${ORCH_URL}/approvals/pending`));
app.get('/api/healthz', (_req, res) => res.json({ ok: true, orchestrator: ORCH_URL }));

// Fallback to index.html so the root loads
app.get('*', (_req, res) => {
  const idxPublic = path.join(publicDir, 'index.html');
  const idxLocal = path.join(__dirname, 'index.html');
  const file = fs.existsSync(idxPublic) ? idxPublic : idxLocal;
  res.sendFile(file);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`UI listening on ${port}, proxying to ${ORCH_URL}`);
});
