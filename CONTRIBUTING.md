# Contributing

## Adding a Connector
1. Create a new module in `pkg/connectors` implementing `BaseConnector`.
2. Add discovery and action methods.
3. Register it in `services/worker/discovery_refresher.py`.

## Adding a Policy Pack
1. Place JSON file in `policies/examples`.
2. Ensure it matches `policies/schema.json`.
3. Add unit tests for new rules.
