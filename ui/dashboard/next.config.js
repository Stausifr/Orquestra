// ui/dashboard/next.config.js
const backend = process.env.ORCHESTRATOR_URL || 'http://orchestrator:8000';

/** @type {import('next').NextConfig} */
module.exports = {
  async rewrites() {
    return [
      // agents & approvals
      { source: '/api/agents', destination: `${backend}/agents` },
      { source: '/api/approvals', destination: `${backend}/approvals/pending` },
      { source: '/api/approvals/:id/:action', destination: `${backend}/approvals/:id/:action` },

      // policies
      { source: '/api/policies', destination: `${backend}/policies` },
      { source: '/api/policies/load', destination: `${backend}/policies/load` },

      // workflows & audit
      { source: '/api/workflows/:run_id', destination: `${backend}/workflows/:run_id` },
      { source: '/api/audit/:run_id.json', destination: `${backend}/audit/:run_id.json` },
      { source: '/api/audit/:run_id.pdf', destination: `${backend}/audit/:run_id.pdf` },

      // incident simulate (if you trigger from UI)
      { source: '/api/incidents/simulate', destination: `${backend}/incidents/simulate` },

      // optional health
      { source: '/api/healthz', destination: `${backend}/agents` },
    ];
  },
};
