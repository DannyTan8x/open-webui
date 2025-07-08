import logging
from typing import Optional
import aiohttp

from open_webui.retrieval.n8n.main import Searchn8nResult, get_filtered_results
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])

async def search_n8n_webhook(
    n8n_webhook_url: str,
    query: str,
    count: int,
    filter_list: Optional[list[str]] = None,
) -> list[Searchn8nResult]:
    all_results = []
    question = query["messages"][-1]["content"]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            n8n_webhook_url,
            json={"question": question, "form_data": query}
        ) as resp:
            if resp.status != 200:
                raise Exception(f"n8n RAG failed, status={resp.status}")
            response = await resp.json()
            
            if response and "data" in response:
                all_results.extend(response["data"])
            elif response:
                all_results.extend(response)

    if filter_list:
        all_results = get_filtered_results(all_results, filter_list)

    # Limit results to count
    all_results = all_results[:count]

    return [
        Searchn8nResult(
            link=result.get("link", ""),
            title=result.get("title", ""),
            snippet=result.get("snippet", ""),
        )
        for result in all_results
    ]

