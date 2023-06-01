from typing import (
    Optional,
    Union
)
from pathlib import Path
from urllib import parse

def urljoin(base_url: str, path: Union[Optional[str], Path] = None):
    if path is None or path == "": return base_url
    path = path if path.startswith("/") else f"/{path}"
    base_url = base_url if base_url.endswith("/") else f"{base_url}/"
    return parse.urljoin(base_url, str(path))