

## FastMCP Example
### Why FastMCP?
The MCP protocol is powerful but implementing it involves a lot of boilerplate - server setup, protocol handlers, content types, error management. FastMCP handles all the complex protocol details and server management, so you can focus on building great tools. It’s designed to be high-level and Pythonic; in most cases, decorating a function is all you need.
FastMCP 2.0 has evolved into a comprehensive platform that goes far beyond basic protocol implementation. While 1.0 provided server-building capabilities (and is now part of the official MCP SDK), 2.0 offers a complete ecosystem including client libraries, authentication systems, deployment tools, integrations with major AI platforms, testing frameworks, and production-ready infrastructure patterns.

### What is MCP?
The Model Context Protocol lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. It is often described as “the USB-C port for AI”, providing a uniform way to connect LLMs to resources they can use. It may be easier to think of it as an API, but specifically designed for LLM interactions. MCP servers can:

* Expose data through Resources (think of these sort of like GET endpoints; they are used to load information into the LLM’s context)
* Provide functionality through Tools (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
* Define interaction patterns through Prompts (reusable templates for LLM interactions)
And more!

FastMCP provides a high-level, Pythonic interface for building, managing, and interacting with these servers.
### Using the FastMCP CLI
```bash
uv run fastmcp run server.py
```

To test the MCP:
```bash
uv run fastmcp dev server.py
```

### Deploy to GoogleRun

Configure our Google Cloud credentials:

```bash
gcloud auth login
export PROJECT_ID=<your-project-id>
gcloud config set project $PROJECT_ID
```

#### Option 1: Deploy from Source

```bash
gcloud run deploy mcp-server \
  --no-allow-unauthenticated \
  --region=us-central1 \
  --source .
```

#### Option 2: Deploy from Container Image

#### Create Artifact Registry Repository

```bash
gcloud artifacts repositories create remote-mcp-servers \
  --repository-format=docker \
  --location=us-central1 \
  --description="Repository for remote MCP servers" \
  --project=$PROJECT_ID
```

#### Build and Push Container Image

```bash
gcloud builds submit \
  --region=us-central1 \
  --tag us-central1-docker.pkg.dev/$PROJECT_ID/remote-mcp-servers/mcp-server:latest
```

#### Deploy to Cloud Run

```bash
gcloud run deploy mcp-server \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/remote-mcp-servers/mcp-server:latest \
  --region=us-central1 \
  --no-allow-unauthenticated
```

### Authentication Setup

#### Grant IAM Permissions

Ensure users have the Cloud Run Invoker role:

```bash
# For a specific user
gcloud run services add-iam-policy-binding mcp-server \
  --region=us-central1 \
  --member="user:email@example.com" \
  --role="roles/run.invoker"

# For your current account
gcloud run services add-iam-policy-binding mcp-server \
  --region=us-central1 \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/run.invoker"
```

### Start Cloud Run Proxy

Create an authenticated tunnel to your remote MCP server:

```bash
gcloud run services proxy mcp-server --region=us-central1
```

This creates a local proxy at `http://127.0.0.1:8080` that forwards authenticated requests to your Cloud Run service.

### Testing the Server

With the Cloud Run proxy running, test your MCP server:

```bash
uv run test_server.py
```

Expected output:
```
>>> Tool found: add
>>> Tool found: subtract
>>> Calling add tool for 1 + 2
<<< Result: 3
>>> Calling subtract tool for 10 - 3
<<< Result: 7
```