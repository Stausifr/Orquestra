// ui/dashboard/next.config.js
const backend = process.env.ORCHESTRATOR_URL || 'http://orchestrator:8000';

/** @type {import('next').NextConfig} */
module.exports = {
  async rewrites() {
    return [
      { source: '/api/agents', destination: `${backend}/agents` },
      { source: '/api/approvals', destination: `${backend}/approvals/pending` },
      // optional health probe:
      { source: '/api/healthz', destination: `${backend}/agents` },
    ];
  },
};
