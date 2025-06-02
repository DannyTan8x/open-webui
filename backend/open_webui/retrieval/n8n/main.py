import validators

from typing import  Optional,  Dict, Any
from urllib.parse import urlparse

from pydantic import BaseModel


def get_filtered_results(results: list, filter_list: list[str]) -> list:
    if not filter_list:
        return results

    filtered_results = []
    for result in results:
        if any(domain in result.get("link", "") for domain in filter_list):
            filtered_results.append(result)
    return filtered_results


class Searchn8nResult(BaseModel):
    id: Optional[int] = None
    link: Optional[str] = None  # 可對應 file 或 link
    title: Optional[str] = None
    snippet: Optional[str] = None
    content: Optional[str] = None
    file: Optional[str] = None
    additional_fields: Optional[Dict[str, Any]] = None