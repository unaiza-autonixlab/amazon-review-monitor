import requests
import hashlib

APIFY_BASE = "https://api.apify.com/v2"
ACTOR_ID = "junglee~amazon-reviews-scraper"


def fetch_recent_reviews(asin: str, api_token: str, max_reviews: int = 20) -> list[dict]:
    """
    Fetch the most recent reviews for a given ASIN via Apify.
    Requires a free Apify account token — sign up at apify.com.
    """
    url = (
        f"{APIFY_BASE}/acts/{ACTOR_ID}/run-sync-get-dataset-items"
        f"?token={api_token}&timeout=120"
    )

    payload = {
        "productUrls": [{"url": f"https://www.amazon.com/dp/{asin}"}],
        "maxReviews": max_reviews,
        "sort": "recent",
    }

    try:
        response = requests.post(url, json=payload, timeout=130)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"  [!] Apify timed out for {asin}. Try again or increase timeout.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"  [!] Apify error for {asin}: {e.response.status_code} — {e.response.text[:200]}")
        return []
    except requests.RequestException as e:
        print(f"  [!] Request failed for {asin}: {e}")
        return []

    raw_items = response.json()
    if not isinstance(raw_items, list):
        print(f"  [!] Unexpected Apify response for {asin}: {str(raw_items)[:200]}")
        return []

    return [_normalize(item, asin) for item in raw_items]


def _normalize(item: dict, asin: str) -> dict:
    title = item.get("reviewTitle", "")
    date = item.get("reviewedIn", "")
    rating_raw = item.get("ratingScore", 0)

    try:
        rating = int(float(str(rating_raw)))
    except (ValueError, TypeError):
        rating = 0

    # Stable unique ID from content since Apify doesn't return review IDs
    unique_str = f"{asin}:{title}:{date}"
    review_id = hashlib.md5(unique_str.encode()).hexdigest()

    return {
        "id": review_id,
        "asin": asin,
        "rating": rating,
        "title": title,
        "body": item.get("reviewDescription", ""),
        "date": date,
        "author": item.get("reviewerName", "Verified Buyer"),
        "verified": item.get("isVerified", False),
        "url": f"https://www.amazon.com/product-reviews/{asin}",
    }
