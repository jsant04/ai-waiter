"""
Upload Router
-------------
POST /api/upload-menu
  Accepts an Excel (.xlsx / .xls) menu file, parses it into
  LangChain Documents, embeds them with OpenAI, and stores
  them in Supabase pgvector for later retrieval.
"""

import logging
import os
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from models.schemas import UploadResponse
from services.menu_parser import parse_excel_menu
from services.vector_store import store_documents

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_EXTENSIONS = {".xlsx", ".xls"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post(
    "/upload-menu",
    response_model=UploadResponse,
    summary="Upload restaurant menu (Excel)",
    description=(
        "Upload a .xlsx or .xls file containing the restaurant menu. "
        "Each row is parsed into an embedding and stored in Supabase. "
        "Existing embeddings for the restaurant are replaced on every upload."
    ),
)
async def upload_menu(
    file: UploadFile = File(..., description="Excel file (.xlsx or .xls)"),
    restaurant_id: str = Form(
        default="default",
        description="Restaurant identifier for multi-tenant support",
    ),
) -> UploadResponse:
    """Parse and embed a restaurant menu from an Excel file."""

    # ── Validate file extension ──
    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # ── Read file bytes ──
    raw = await file.read()
    if len(raw) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(raw) // 1024} KB). Maximum allowed is 10 MB.",
        )

    if len(raw) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    tmp_path: str | None = None

    try:
        # ── Write to a temp file for pandas ──
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp.write(raw)
            tmp_path = tmp.name

        logger.info(
            "Processing menu upload | restaurant=%s | file=%s | size=%d bytes",
            restaurant_id,
            filename,
            len(raw),
        )

        # ── Parse ──
        documents = parse_excel_menu(tmp_path, restaurant_id)

        if not documents:
            raise HTTPException(
                status_code=422,
                detail=(
                    "No valid menu items found in the file. "
                    "Please ensure the file has a 'Name' column and at least one data row."
                ),
            )

        # ── Embed + store ──
        items_count = store_documents(documents, restaurant_id)

        logger.info(
            "Menu upload complete | restaurant=%s | items=%d",
            restaurant_id,
            items_count,
        )

        return UploadResponse(
            message=f"✅ Menu uploaded successfully! {items_count} items are now ready.",
            items_processed=items_count,
            restaurant_id=restaurant_id,
            status="success",
        )

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    except Exception as exc:
        logger.error("Menu upload error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process the menu file. Please check the format and try again.",
        ) from exc

    finally:
        # Always clean up temp file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
