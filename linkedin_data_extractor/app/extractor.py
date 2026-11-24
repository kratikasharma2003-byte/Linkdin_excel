
import requests
import time

from app.processor import create_empty_profile
from config import (
    API_URL,
    API_KEY,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    REQUEST_DELAY
)


def merge_dict(base, incoming):
    """Merge nested dictionaries without losing default fields."""

    for key, value in incoming.items():

        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            merge_dict(base[key], value)

        elif key in base:
            base[key] = value

    return base


class ProfileExtractor:

    def __init__(self):

        self.mock_mode = False
        if not API_URL or not API_KEY or "your-api-endpoint.com" in API_URL:
            print("[INFO] No external API configured in .env. Running in Mock/Demo extraction mode...")
            self.mock_mode = True
            return

        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def fetch_profile(self, url):

        if self.mock_mode:
            slug = url.rstrip("/").split("/")[-1].replace("-", " ").title()
            return {
                "profile": {
                    "name": slug,
                    "headline": f"Professional Profile ({slug})",
                    "followers_count": 500,
                    "connections_count": 500,
                    "premium_status": False,
                    "about": f"Simulated profile data for {url}"
                }
            }

        for attempt in range(MAX_RETRIES):

            try:

                response = self.session.post(
                    API_URL,
                    json={"profile_url": url},
                    timeout=REQUEST_TIMEOUT
                )

                if response.status_code == 429:
                    wait = int(
                        response.headers.get("Retry-After", 10)
                    )
                    time.sleep(min(wait, 120))
                    continue

                if response.status_code in (401, 403):
                    raise PermissionError(
                        "API authentication or access denied"
                    )

                if response.status_code >= 500:
                    response.raise_for_status()

                response.raise_for_status()

                payload = response.json()

                # Provider must return normalized profile data
                if "data" in payload:
                    payload = payload["data"]

                if not isinstance(payload, dict):
                    raise ValueError("Invalid API response format")

                return payload

            except PermissionError:
                raise

            except requests.RequestException:

                if attempt == MAX_RETRIES - 1:
                    raise

                time.sleep(2 ** attempt)

            except ValueError:
                raise

        raise RuntimeError("Maximum API retries exceeded")


def extract_profile(url, extractor):

    result = create_empty_profile(url)

    try:

        data = extractor.fetch_profile(url)

        result = merge_dict(result, data)

        result["profile_url"] = url
        result["contact_info"]["linkedin_url"] = url

        result["extraction_status"] = (
            "success"
            if result["profile"]["name"]
            else "partial"
        )

    except Exception as error:

        result["extraction_status"] = "failed"

        result["errors"].append({
            "message": str(error)
        })

    time.sleep(REQUEST_DELAY)

    return result
