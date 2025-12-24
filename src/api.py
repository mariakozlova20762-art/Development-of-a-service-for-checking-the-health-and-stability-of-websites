# src/api.py
from fastapi import APIRouter, HTTPException
from src.checker import check_website, check_multiple_websites
from typing import List

router = APIRouter(prefix="/api/v1")


@router.get("/health")
async def get_health():
    return {"status": "ok"}


@router.get("/check/{url:path}")
async def check_single_website(url: str):
    """
    Проверить один веб-сайт
    """
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    
    result = await check_website(url)
    return result


@router.post("/check/multiple")
async def check_multiple(urls: List[str]):
    """
    Проверить несколько веб-сайтов
    """
    if not urls:
        raise HTTPException(status_code=400, detail="URLs list is empty")
    
    # Добавляем https:// если нет протокола
    formatted_urls = []
    for url in urls:
        url = str(url).strip()
        if not url:
            continue
        if not url.startswith(("http://", "https://")):
            formatted_urls.append(f"https://{url}")
        else:
            formatted_urls.append(url)
    
    if not formatted_urls:
        raise HTTPException(status_code=400, detail="No valid URLs provided")
    
    results = await check_multiple_websites(formatted_urls)
    return {"results": results}