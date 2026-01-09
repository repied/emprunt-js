# Testing the Web Application

When asked to test the application or verify changes, follow this procedure:

1.  **Environment Setup**:
    *   The application is a static site served via **Live Server** vscode extension.
    *   It runs on the host machine but is accessed via the Dev Container forwarding on port **5500**.
    *   Browser automation is handled by a **Docker MCP server** (Playwright) running on the host.

2.  **Navigation URL**:
    *   **Crucial**: Always access the site using `http://host.docker.internal:5500/`.
    *   Do *not* use `localhost` or `127.0.0.1` as the MCP container cannot see the Dev Container's localhost directly.

3.  **Testing Workflow**:
    *   Start Live Server if it is not running and retry the navigation step.
    *   Use the `mcp_mcp_docker_browser_navigate` tool to open `http://host.docker.internal:5500/`.
    *   Use `mcp_mcp_docker_browser_fill_form`, `mcp_mcp_docker_browser_click`, and `mcp_mcp_docker_browser_snapshot` to interact with the page.
    *   Check for console errors using `mcp_mcp_docker_browser_console_messages`.

4.  **Troubleshooting**:
    *   If the connection fails, verify that Live Server is running (usually started via VS Code status bar or command palette).
