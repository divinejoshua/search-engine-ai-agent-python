# serp.py
import asyncio
import aiohttp
from typing import List

async def search_duckduckgo(query: str) -> List[str]:
    """Search the web using DuckDuckGo's HTML API.
    
    Args:
        query: The search query string
        
    Returns:
        List of formatted search results as strings
    """
    try:
        async with aiohttp.ClientSession() as session:
            # Using DuckDuckGo's HTML API
            url = "https://html.duckduckgo.com/html/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = f'q={query.replace(" ", "+")}'
            
            async with session.post(url, headers=headers, data=data) as response:
                if response.status != 200:
                    return [f"Error: Received status code {response.status}"]
                    
                html = await response.text()
                
                # Simple HTML parsing to extract results
                results = []
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find all search result items
                for result in soup.select('.result'):
                    title_elem = result.select_one('h2 a')
                    snippet_elem = result.select_one('.result__snippet')
                    
                    if title_elem and snippet_elem:
                        title = title_elem.get_text(strip=True)
                        snippet = snippet_elem.get_text(strip=True)
                        link = title_elem.get('href', '')
                        
                        # Clean up the link
                        if link.startswith('//'):
                            link = 'https:' + link
                        elif link.startswith('/'):
                            link = 'https://duckduckgo.com' + link
                            
                        results.append(f"{title}\n{snippet}\n{link}")
                
                return results if results else ["No results found."]
                
    except Exception as e:
        return [f"Error performing search: {str(e)}"]
