
from datetime import datetime, timezone
import json
import os


def create_empty_profile(url):

    return {
        "profile_url": url,
        "extraction_status": "failed",
        "extracted_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "profile": {
            "name": None,
            "profile_photo_url": None,
            "headline": None,
            "followers_count": None,
            "connections_count": None,
            "premium_status": None,
            "about": None
        },

        "account_history": {
            "joined_linkedin": {
                "month": None,
                "year": None,
                "display_text": None
            },
            "contact_info_last_updated": {
                "display_text": None
            },
            "profile_photo_last_updated": {
                "display_text": None
            },
            "identity_verification": {
                "verified": None,
                "method": None,
                "month": None,
                "year": None,
                "display_text": None
            }
        },

        "contact_info": {
            "linkedin_url": url,
            "websites": [],
            "email": None,
            "phone": None,
            "other_links": []
        },

        "activities": [],
        "experience": [],
        "education": [],
        "skills": [],
        "recommendations": [],
        "certifications": [],
        "courses": [],
        "languages": [],
        "errors": []
    }


def save_json(data, file_path):

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    with open(file_path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )
