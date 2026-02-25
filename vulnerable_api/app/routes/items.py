from fastapi import APIRouter, Request

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/search")
async def search_items(body: dict, request: Request):
    """
    Intentionally insecure:
    - No input validation (accepts anything)
    - Simulates "dangerous" query construction with string formatting
    - Returns internal details for demo
    """
    query = body.get("query", "")
    limit = body.get("limit", 10)

    # Insecure: pretend this is a SQL query built from user input
    fake_sql = f"SELECT * FROM items WHERE name LIKE '%{query}%' LIMIT {limit};"

    # Insecure: leaks internal query details
    return {
        "message": "Search executed (simulated).",
        "constructed_query": fake_sql,
        "note": "This endpoint is intentionally vulnerable for demonstration.",
    }


@router.post("/feedback")
async def submit_feedback(body: dict, request: Request):
    """
    Intentionally insecure:
    - No validation or length limits
    - No anti-spam / abuse protections
    - Reflects user input back (bad practice)
    """
    feedback = body.get("feedback", "")
    email = body.get("email", "")

    # Insecure: reflect input
    return {
        "status": "received",
        "email": email,
        "feedback": feedback,
        "note": "This endpoint is intentionally vulnerable for demonstration.",
    }