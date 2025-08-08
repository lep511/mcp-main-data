import os
import asyncio
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from html2text import html2text
import mcp.types as types
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
import logging
from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("mcp-wiki-demo")

@mcp.tool
def extract_wikipedia_article(url: str) -> str:
    """
    Retrieves and processes a Wikipedia article from the given URL, extracting
    the main content and converting it to Markdown format.
        
    Args:
        url (str): The complete Wikipedia article URL. Must start with 'http' 
                  or 'https'. Example: "https://en.wikipedia.org/wiki/Python"
    
    Returns:
        str: The main article content converted to Markdown format, including
             text, headers, links, and basic formatting.
    """
    try:
        # Validate URL format - must include protocol
        if not url.startswith("http"):
            raise ValueError("URL must begin with http or https protocol.")

        # Make HTTP request with timeout to prevent hanging
        response = requests.get(url, timeout=8)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Unable to access the article. Server returned status: {response.status_code}"
                )
            )
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Locate the main Wikipedia content container
        # This div contains the actual article text, excluding navigation, sidebar, etc.
        content_div = soup.find("div", {"id": "mw-content-text"})
        
        # Ensure we found the expected Wikipedia page structure
        if not content_div:
            raise McpError(
                ErrorData(
                    code=INVALID_PARAMS,
                    message="The main article content section was not found at the specified Wikipedia URL."
                )
            )
        
        # Convert the HTML content to Markdown format
        # This preserves formatting like headers, links, lists, etc.
        markdown_text = html2text(str(content_div))
        
        return markdown_text

    except Exception as e:
        # Catch any unexpected errors and wrap them in MCP-compliant error format
        # The 'from e' preserves the original exception chain for debugging
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR, 
                message=f"An unexpected error occurred: {str(e)}"
            )
        ) from e

@mcp.tool
async def list_tools() -> list[types.Tool]:
    """
    Return a list of available tools for the MCP server.
        
    Returns:
        list[types.Tool]: A list of Tool objects, each containing:
            - name: Unique identifier for the tool
            - description: Human-readable description of what the tool does
            - inputSchema: JSON Schema defining the required and optional parameters

    """
    return [
        # Define the Wikipedia article extraction tool
        types.Tool(
            name="extract-wikipedia-article",
            description=("Extracts the main content of a Wikipedia article"),
            inputSchema={
                "type": "object",
                "required": ["url"],  # URL parameter is mandatory
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the Wikipedia article to extract",
                    },
                },
            },
        )
    ]


if __name__ == "__main__":
    logger.info(f" MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_async(
            transport="streamable-http", 
            host="0.0.0.0", 
            port=os.getenv("PORT", 8080),
        )
    )