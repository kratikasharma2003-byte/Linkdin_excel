
def generate_report(records, invalid_urls, elapsed):

    successful = sum(
        r["extraction_status"] == "success"
        for r in records
    )

    failed = sum(
        r["extraction_status"] == "failed"
        for r in records
    )

    partial = sum(
        r["extraction_status"] == "partial"
        for r in records
    )

    total = len(records)

    report = {
        "profiles_processed": total,
        "successful_records": successful,
        "partial_records": partial,
        "failed_records": failed,
        "invalid_urls": len(invalid_urls),
        "execution_time_seconds": round(elapsed, 2),
        "average_processing_time_seconds": round(
            elapsed / total, 2
        ) if total else 0,
        "errors": [
            {
                "profile_url": r["profile_url"],
                "errors": r["errors"]
            }
            for r in records
            if r["errors"]
        ],
        "scalability": (
            "Batch processing, controlled concurrency, "
            "provider rate limits and checkpointing recommended."
        )
    }

    return report
