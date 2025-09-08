# Connectors

Connectors implement a common interface with `list_agents()` and provider-specific actions.

To add a provider:
1. Implement a subclass of `BaseConnector`.
2. Provide discovery and action methods.
3. Register with worker discovery logic.
