## MCP Server on Google Cloud Run

Deploy your Model Context Protocol (MCP) server on Google Cloud Run for scalable, secure, and centralized AI context management.

### Overview

The Model Context Protocol (MCP) standardizes how applications provide context to Large Language Models (LLMs). This guide demonstrates how to deploy an MCP server on Google Cloud Run, enabling remote access and scalable infrastructure for your AI applications.

### Benefits of Remote MCP Servers

- **Scalability**: Automatic scaling based on demand
- **Centralized Access**: Share servers with team members through IAM
- **Security**: Enforce authenticated requests to prevent unauthorized access
- **Maintenance**: Centralized updates benefit all team members

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (package and project management)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (gcloud CLI)
- Google Cloud Project with billing enabled

### Project Setup

#### 1. Create Project Structure

```bash
mkdir mcp-on-cloudrun
cd mcp-on-cloudrun

# Initialize uv project
uv init --name "mcp-on-cloudrun" --description "Example of deploying a MCP server on Cloud Run" --bare --python 3.10

# Create additional files
touch server.py test_server.py Dockerfile
```

#### 2. Configure Google Cloud

```bash
# Set your project ID
export PROJECT_ID=<your-project-id>

# Authenticate with Google Cloud
gcloud auth login

# Set the active project
gcloud config set project $PROJECT_ID
```

#### 3. Add Dependencies

```bash
uv add fastmcp==2.6.1 --no-sync
```

### Deployment Options

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

### MCP Transport Options

This example uses **streamable-http** transport (recommended for remote servers). The MCP endpoint will be available at:
- Streamable HTTP: `http://localhost:8080/mcp`
- SSE (deprecated but supported): `http://localhost:8080/sse`

### File Structure

```
mcp-on-cloudrun/
├── pyproject.toml       # Project configuration and dependencies
├── server.py           # MCP server implementation
├── test_server.py      # Test client for the MCP server
└── Dockerfile         # Container configuration for Cloud Run
```

### Security Considerations

- **Always use `--no-allow-unauthenticated`** when deploying to prevent unauthorized access
- Use IAM roles to control access to your MCP server
- The Cloud Run proxy ensures secure, authenticated connections
- Monitor your Cloud Run logs for unexpected usage patterns

### Next Steps

- Extend your MCP server with additional tools and resources
- Set up monitoring and alerting for your Cloud Run service
- Implement custom authentication if needed
- Scale your MCP server based on usage patterns

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Cloud Run MCP Server Guide](https://cloud.google.com/run/docs/tutorials/ai-model-context-protocol)