import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
import logfire

# Environment variables for configuration
MCP_SERVER_URL = os.getenv('MCP_SERVER_URL')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
LOGFIRE_TOKEN = os.getenv('LOGFIRE_TOKEN')

# Validate environment variables
if not MCP_SERVER_URL:
    raise ValueError("MCP_SERVER_URL environment variable is required")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")
if not LOGFIRE_TOKEN:
    raise ValueError("LOGFIRE_TOKEN environment variable is required")

# Configure logfire
logfire.configure(
    token=LOGFIRE_TOKEN,
    service_name='client-mcp',
    environment='test'
)
logfire.instrument_pydantic_ai()

# Initialize MCP server connection
server = MCPServerStreamableHTTP(MCP_SERVER_URL)

# Initialize Google provider and model
provider = GoogleProvider(api_key=GEMINI_API_KEY)
model = GoogleModel('gemini-2.5-flash', provider=provider)  # Updated to valid model name

# Create agent with model and MCP server toolsets
agent = Agent(model, toolsets=[server])

async def main():
    """
    Main async function that demonstrates using Pydantic AI agent
    with MCP server integration to perform date calculations.
    """
    try:
        # Use async context manager for proper resource management
        async with agent:  
            result = await agent.run('What is the result of subtracting 30504 from 244403?')
        
        # Print the result
        print(result.output)
        # Expected output: 213899
        
    except Exception as e:
        print(f"Error occurred: {e}")
        logfire.error(f"Error occurred: {e}")
        raise

    logfire.info("Pydantic AI agent completed successfully")

if __name__ == "__main__":
    # Properly run the async main function
    asyncio.run(main())