# src/checker.py
import httpx
import asyncio
from datetime import datetime
from typing import Dict, Optional, List


async def check_website(url: str, timeout: int = 10, follow_redirects: bool = True) -> Dict[str, any]:
    """
    Проверяет доступность веб-сайта с опцией следования за перенаправлениями
    """
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=follow_redirects
        ) as client:
            response = await client.get(url)
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000
            
            # Получаем итоговый URL после всех перенаправлений
            final_url = str(response.url)
            
            return {
                "url": url,
                "final_url": final_url if final_url != url else None,
                "status_code": response.status_code,
                "status": "up" if response.status_code < 400 else "down",
                "response_time_ms": round(response_time, 2),
                "timestamp": end_time.isoformat(),
                "error": None,
                "redirected": len(response.history) > 0,
                "redirect_count": len(response.history)
            }
    except httpx.TimeoutException:
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        return {
            "url": url,
            "final_url": None,
            "status_code": None,
            "status": "timeout",
            "response_time_ms": round(response_time, 2),
            "timestamp": end_time.isoformat(),
            "error": f"Timeout after {timeout} seconds",
            "redirected": False,
            "redirect_count": 0
        }
    except httpx.RequestError as e:
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        return {
            "url": url,
            "final_url": None,
            "status_code": None,
            "status": "error",
            "response_time_ms": round(response_time, 2),
            "timestamp": end_time.isoformat(),
            "error": str(e),
            "redirected": False,
            "redirect_count": 0
        }


async def check_multiple_websites(urls: list[str], timeout: int = 10) -> list[Dict[str, any]]:
    """
    Проверяет несколько веб-сайтов одновременно
    """
    tasks = [check_website(url, timeout) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


# Синхронная версия для простых случаев
def check_website_sync(url: str, timeout: int = 10) -> Dict[str, any]:
    """
    Синхронная версия проверки веб-сайта
    """
    start_time = datetime.now()
    
    try:
        response = httpx.get(url, timeout=timeout)
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        
        return {
            "url": url,
            "status_code": response.status_code,
            "status": "up" if response.status_code < 400 else "down",
            "response_time_ms": round(response_time, 2),
            "timestamp": end_time.isoformat(),
            "error": None
        }
    except httpx.TimeoutException:
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        return {
            "url": url,
            "status_code": None,
            "status": "timeout",
            "response_time_ms": round(response_time, 2),
            "timestamp": end_time.isoformat(),
            "error": f"Timeout after {timeout} seconds"
        }
    except httpx.RequestError as e:
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        return {
            "url": url,
            "status_code": None,
            "status": "error",
            "response_time_ms": round(response_time, 2),
            "timestamp": end_time.isoformat(),
            "error": str(e)
        }