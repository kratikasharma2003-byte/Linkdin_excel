import time
import json
import os
import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from config import (
    INPUT_FILE,
    OUTPUT_FILE,
    ERROR_FILE,
    URL_COLUMN,
    BATCH_SIZE,
    LIMIT
)

from app.excel_reader import read_linkedin_urls
from app.extractor import ProfileExtractor, extract_profile
from app.processor import save_json
from app.reporter import generate_report

app = FastAPI(
    title="LinkedIn Data Extractor API",
    description="API for reading LinkedIn URLs from Excel and extracting profile data.",
    version="1.0.0"
)

# In-memory status tracking
extraction_state = {
    "is_running": False,
    "last_report": None
}


def run_extraction():
    """Runs the complete profile extraction pipeline."""
    if extraction_state["is_running"]:
        raise RuntimeError("An extraction is already in progress.")

    extraction_state["is_running"] = True
    start_time = time.time()

    try:
        print("Starting LinkedIn Data Extraction...")

        # Step 1: Read Excel
        urls, invalid_urls = read_linkedin_urls(
            INPUT_FILE,
            URL_COLUMN or None
        )

        print("Valid URLs:", len(urls))
        print("Invalid URLs:", len(invalid_urls))

        if LIMIT and LIMIT > 0:
            urls = urls[:LIMIT]
            print(f"Limiting execution to first {LIMIT} URLs.")

        # Step 2: Connect authorized provider
        extractor = ProfileExtractor()

        records = []

        # Step 3: Process URLs in batches
        for start in range(0, len(urls), BATCH_SIZE):
            batch = urls[start:start + BATCH_SIZE]
            batch_num = start // BATCH_SIZE + 1
            total_batches = (len(urls) + BATCH_SIZE - 1) // BATCH_SIZE
            print(f"\nProcessing batch {batch_num}/{total_batches} ({len(batch)} items)")

            for index, url in enumerate(batch, start=1):
                if index % 100 == 0 or index == len(batch):
                    print(f"Progress: {start + index}/{len(urls)}")
                record = extract_profile(url, extractor)
                records.append(record)

            # Step 4: Save checkpoint after each batch
            save_json(records, OUTPUT_FILE)
            print("Batch completed and checkpoint saved.")

        # Step 5: Final output
        elapsed = time.time() - start_time
        save_json(records, OUTPUT_FILE)

        report = generate_report(records, invalid_urls, elapsed)

        os.makedirs(os.path.dirname(ERROR_FILE), exist_ok=True)
        with open(ERROR_FILE, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "invalid_urls": invalid_urls,
                    "failed_profiles": report["errors"],
                    "performance": report
                },
                file,
                indent=4
            )

        extraction_state["last_report"] = report

        print("\n===== FINAL REPORT =====")
        print(json.dumps(report, indent=4))
        print("\nOutput:", OUTPUT_FILE)
        print("Errors:", ERROR_FILE)

        return report

    finally:
        extraction_state["is_running"] = False


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "LinkedIn Data Extractor",
        "docs_url": "/docs",
        "endpoints": {
            "extract_sync": "POST /extract",
            "extract_background": "POST /extract/background",
            "status": "GET /status",
            "records": "GET /records",
            "errors": "GET /errors"
        }
    }


@app.post("/extract")
def trigger_extraction_sync():
    """Run extraction synchronously and return the final report."""
    if extraction_state["is_running"]:
        raise HTTPException(status_code=409, detail="Extraction is already running")
    try:
        report = run_extraction()
        return {"status": "completed", "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract/background")
def trigger_extraction_async(background_tasks: BackgroundTasks):
    """Run extraction in the background."""
    if extraction_state["is_running"]:
        raise HTTPException(status_code=409, detail="Extraction is already running")
    background_tasks.add_task(run_extraction)
    return {"status": "started", "message": "Extraction launched in background"}


@app.get("/status")
def get_status():
    """Get current extraction status and the latest report."""
    return {
        "is_running": extraction_state["is_running"],
        "last_report": extraction_state["last_report"]
    }


@app.get("/records")
def get_records():
    """Retrieve extracted records from data/output.json."""
    if not os.path.exists(OUTPUT_FILE):
        return []
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/errors")
def get_errors():
    """Retrieve error logs from data/errors.json."""
    if not os.path.exists(ERROR_FILE):
        return {}
    with open(ERROR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    import sys
    if "--cli" in sys.argv:
        run_extraction()
    else:
        port = int(os.getenv("PORT", "8001"))
        print(f"Starting Uvicorn server on http://127.0.0.1:{port}...")
        uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
