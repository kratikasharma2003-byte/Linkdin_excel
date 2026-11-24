
import pandas as pd
from urllib.parse import urlparse


def is_valid_linkedin_url(url):
    try:
        parsed = urlparse(url.strip())

        return (
            parsed.scheme in ("http", "https")
            and parsed.netloc.lower() in (
                "linkedin.com",
                "www.linkedin.com"
            )
            and parsed.path.startswith("/in/")
        )
    except Exception:
        return False


def read_linkedin_urls(file_path, url_column=None):

    df = pd.read_excel(file_path)

    if url_column and url_column in df.columns:
        column = url_column
    else:
        candidates = [
            col for col in df.columns
            if any(
                word in str(col).lower()
                for word in ["linkedin", "profile", "url"]
            )
        ]

        if not candidates:
            raise ValueError(
                "LinkedIn URL column not found in Excel"
            )

        column = candidates[0]

    urls = []
    invalid = []
    seen = set()

    for value in df[column].dropna():

        url = str(value).strip()

        if url.lower() in seen:
            continue

        seen.add(url.lower())

        if is_valid_linkedin_url(url):
            urls.append(url)
        else:
            invalid.append({
                "url": url,
                "error": "Invalid LinkedIn profile URL"
            })

    return urls, invalid
