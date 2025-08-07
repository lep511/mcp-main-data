## MCP server Wiki extractor

Integrating context from tools and data sources into LLMs can be challenging, which impacts ease-of-use in the development of AI agents. To address this challenge, Anthropic introduced the Model Context Protocol (MCP), which standardizes how applications provide context to LLMs. Imagine you want to build an MCP server for your API to make it available to fellow developers so they can use it as context in their own AI applications

### A quick refresher

* **SSE** enables servers to push data to clients over a persistent HTTP connection. In a typical setup for MCP, this involved using two distinct endpoints: one for the client to send requests to the server (usually via HTTP POST) and a separate endpoint where the client would establish an SSE connection (HTTP GET) to receive streaming responses and server-initiated messages.

* **MCP** is an open standard designed to standardize how Large Language Models (LLMs) interact with external data sources, APIs and resources as agent tools, MCP aims to replace the current landscape of fragmented, custom integrations with a universal, standardized framework.

* **Streamable HTTP** utilizes a single HTTP endpoint for both sending requests from the client to the server, and receiving responses and notifications from the server to the client.

MCP has evolved and now supports remote access transports: streamable-http and sse. Server-Sent Events (SSE) has been deprecated in favor of Streamable HTTP in the latest MCP specification but is still supported for backwards compatibility. Both of these two transports allow for running MCP servers remotely.

With Streamable HTTP, the server operates as an independent process that can handle multiple client connections. This transport uses HTTP POST and GET requests.

The server MUST provide a single HTTP endpoint path (hereafter referred to as the MCP endpoint) that supports both POST and GET methods. For example, this could be a URL like https://example.com/mcp.

To start the server, you can run the command:

```bash
uv run server_sse.py
```

To debug the server using MCP Inspector, execute the command:

```bash
uv run mcp dev server_sse.py
```

### Deploy MCP in Google Run


### Test with ADK agents

```bash
uv run adk web
```



