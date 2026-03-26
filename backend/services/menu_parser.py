"""
Menu Parser Service
-------------------
Parses Excel (.xlsx / .xls) menus into LangChain Documents
ready for embedding and vector storage.

Supported column names (case-insensitive, flexible aliases):
  name, category, price, description, allergens,
  spicy_level, vegetarian, vegan, calories
"""

import logging
from typing import List

import pandas as pd
from langchain.schema import Document

logger = logging.getLogger(__name__)

# ── Flexible column name aliases ──────────────────────────
COLUMN_ALIASES: dict[str, list[str]] = {
    "name": [
        "name", "item", "item name", "dish", "dish name",
        "menu item", "food name", "product",
    ],
    "category": [
        "category", "type", "section", "course",
        "menu section", "group", "department",
    ],
    "price": ["price", "cost", "amount", "rate", "usd", "eur"],
    "description": [
        "description", "desc", "details", "about", "info",
        "ingredients", "notes",
    ],
    "allergens": [
        "allergens", "allergy", "allergen info", "contains",
        "allergen", "allergy info",
    ],
    "spicy_level": [
        "spicy", "spicy level", "heat", "spice level",
        "spice", "hot level",
    ],
    "is_vegetarian": ["vegetarian", "veg", "is vegetarian", "is_vegetarian"],
    "is_vegan": ["vegan", "is vegan", "is_vegan"],
    "calories": ["calories", "cal", "kcal", "energy"],
}


def _normalize_column(col: str) -> str:
    """Map a raw column header to a canonical key."""
    col_lower = col.lower().strip()
    for key, aliases in COLUMN_ALIASES.items():
        if col_lower in aliases:
            return key
    return col_lower


def _build_content(row: pd.Series) -> str:
    """Build a rich text representation of one menu item."""
    parts: list[str] = []

    name = str(row.get("name", "")).strip()
    parts.append(f"Menu Item: {name or 'Unknown Item'}")

    if category := str(row.get("category", "")).strip():
        parts.append(f"Category: {category}")

    if price := str(row.get("price", "")).strip():
        # Format price nicely
        try:
            parts.append(f"Price: ${float(price):.2f}")
        except ValueError:
            parts.append(f"Price: {price}")

    if description := str(row.get("description", "")).strip():
        parts.append(f"Description: {description}")

    if allergens := str(row.get("allergens", "")).strip():
        parts.append(f"Allergens: {allergens}")

    if spicy := str(row.get("spicy_level", "")).strip():
        parts.append(f"Spicy Level: {spicy}")

    if veg := str(row.get("is_vegetarian", "")).strip():
        if veg.lower() in ("yes", "true", "1", "y"):
            parts.append("Vegetarian: Yes 🌱")

    if vegan := str(row.get("is_vegan", "")).strip():
        if vegan.lower() in ("yes", "true", "1", "y"):
            parts.append("Vegan: Yes 🌿")

    if cals := str(row.get("calories", "")).strip():
        parts.append(f"Calories: {cals} kcal")

    return "\n".join(parts)


def parse_excel_menu(file_path: str, restaurant_id: str) -> List[Document]:
    """
    Parse an Excel menu file and return a list of LangChain Documents.

    Args:
        file_path:     Absolute path to the .xlsx / .xls file.
        restaurant_id: Identifier for the owning restaurant.

    Returns:
        List of Documents ready to embed and store.
    """
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except Exception as exc:
        raise ValueError(f"Could not open Excel file: {exc}") from exc

    if df.empty:
        raise ValueError("The uploaded Excel file contains no data rows.")

    # Normalise column headers
    df.columns = [_normalize_column(col) for col in df.columns]

    # Drop fully empty rows; fill remaining NaN with empty string
    df.dropna(how="all", inplace=True)
    df = df.astype(object).fillna("")

    documents: List[Document] = []

    for _, row in df.iterrows():
        name = str(row.get("name", "")).strip()
        if not name:
            # Skip rows with no item name
            continue

        content = _build_content(row)

        metadata = {
            "name": name,
            "category": str(row.get("category", "General")).strip(),
            "price": str(row.get("price", "")).strip(),
            "allergens": str(row.get("allergens", "")).strip(),
            "is_vegetarian": str(row.get("is_vegetarian", "")).strip().lower()
            in ("yes", "true", "1", "y"),
            "is_vegan": str(row.get("is_vegan", "")).strip().lower()
            in ("yes", "true", "1", "y"),
            "restaurant_id": restaurant_id,
        }

        documents.append(Document(page_content=content, metadata=metadata))

    logger.info(
        "Parsed %d menu items from '%s' for restaurant '%s'",
        len(documents),
        file_path,
        restaurant_id,
    )
    return documents
