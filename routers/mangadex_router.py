from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/mangadex", tags=["Mangadex Proxy"])
API_BASE_URL = "https://api.mangadex.org"


async def fetch_from_mangadex(url: str):
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 1. Home manga
@router.get("/home")
async def fetch_home_manga():
    url = (
        f"{API_BASE_URL}/manga?limit=16&includedTagsMode=AND&excludedTagsMode=OR&"
        "contentRating%5B%5D=safe&contentRating%5B%5D=suggestive&contentRating%5B%5D=erotica&"
        "order%5BlatestUploadedChapter%5D=desc"
    )
    return await fetch_from_mangadex(url)


# 2. Manga details
@router.get("/manga/{manga_id}")
async def fetch_manga_details(manga_id: str):
    url = f"{API_BASE_URL}/manga/{manga_id}"
    return await fetch_from_mangadex(url)


# 3. Manga author
@router.get("/author/{author_id}")
async def fetch_manga_author(author_id: str):
    url = f"{API_BASE_URL}/author/{author_id}"
    return await fetch_from_mangadex(url)


# 4. Manga chapters aggregate
@router.get("/manga/{manga_id}/aggregate")
async def fetch_manga_chapters(manga_id: str):
    url = f"{API_BASE_URL}/manga/{manga_id}/aggregate"
    return await fetch_from_mangadex(url)


# 5. Chapter raw (image server)
@router.get("/chapter/{chapter_id}/raw")
async def fetch_chapter_raw(chapter_id: str):
    url = f"{API_BASE_URL}/at-home/server/{chapter_id}"
    return await fetch_from_mangadex(url)


# 6. Chapter info (metadata)
@router.get("/chapter/{chapter_id}")
async def fetch_chapter(chapter_id: str):
    url = f"{API_BASE_URL}/chapter/{chapter_id}"
    return await fetch_from_mangadex(url)


# 7. Cover (dùng khi lấy ảnh bìa)
@router.get("/cover")
async def fetch_cover(manga_id: str):
    """
    Proxy endpoint cho cover. Truyền ?manga_id=xxx
    """
    url = f"{API_BASE_URL}/cover?manga[]={manga_id}"
    return await fetch_from_mangadex(url)
