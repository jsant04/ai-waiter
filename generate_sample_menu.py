"""
Generate a sample restaurant Excel menu for testing AI Waiter uploads.
Run: python generate_sample_menu.py
"""
import os

try:
    import pandas as pd
except ImportError:
    print("pandas not installed. Run: pip install pandas openpyxl")
    raise

MENU_DATA = [
    # ── Starters ─────────────────────────────────────────
    {
        "Name": "Bruschetta al Pomodoro",
        "Category": "Starters",
        "Price": 8.50,
        "Description": "Toasted sourdough rubbed with garlic, topped with fresh tomatoes, basil, and a drizzle of extra-virgin olive oil.",
        "Allergens": "Gluten",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 220,
    },
    {
        "Name": "Crispy Calamari",
        "Category": "Starters",
        "Price": 12.99,
        "Description": "Lightly battered squid rings fried golden, served with lemon aioli and a side of marinara sauce.",
        "Allergens": "Gluten, Eggs, Shellfish",
        "Spicy Level": "None",
        "Vegetarian": "No",
        "Vegan": "No",
        "Calories": 380,
    },
    {
        "Name": "Spicy Chicken Wings",
        "Category": "Starters",
        "Price": 13.99,
        "Description": "12 crispy chicken wings tossed in our signature hot sauce. Served with blue cheese dip and celery sticks.",
        "Allergens": "Dairy",
        "Spicy Level": "High",
        "Vegetarian": "No",
        "Vegan": "No",
        "Calories": 520,
    },
    {
        "Name": "Burrata & Heirloom Tomatoes",
        "Category": "Starters",
        "Price": 14.50,
        "Description": "Fresh burrata cheese over a bed of heirloom tomatoes, drizzled with aged balsamic and fresh basil.",
        "Allergens": "Dairy",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "No",
        "Calories": 310,
    },
    # ── Salads ──────────────────────────────────────────
    {
        "Name": "Classic Caesar Salad",
        "Category": "Salads",
        "Price": 11.99,
        "Description": "Crisp romaine lettuce, house-made Caesar dressing, shaved Parmesan, and garlic croutons.",
        "Allergens": "Gluten, Dairy, Eggs, Fish",
        "Spicy Level": "None",
        "Vegetarian": "No",
        "Vegan": "No",
        "Calories": 340,
    },
    {
        "Name": "Quinoa & Roasted Veggie Bowl",
        "Category": "Salads",
        "Price": 13.50,
        "Description": "Tri-color quinoa with roasted seasonal vegetables, chickpeas, and lemon-tahini dressing.",
        "Allergens": "Sesame",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 420,
    },
    # ── Pasta ───────────────────────────────────────────
    {
        "Name": "Spaghetti Carbonara",
        "Category": "Pasta",
        "Price": 16.99,
        "Description": "Classic Roman pasta with crispy guanciale, egg yolk, Pecorino Romano, and freshly cracked black pepper.",
        "Allergens": "Gluten, Eggs, Dairy",
        "Spicy Level": "None",
        "Vegetarian": "No",
        "Vegan": "No",
        "Calories": 620,
    },
    {
        "Name": "Penne Arrabbiata",
        "Category": "Pasta",
        "Price": 14.50,
        "Description": "Penne in a bold, spicy San Marzano tomato sauce with garlic, chili flakes, and fresh parsley.",
        "Allergens": "Gluten",
        "Spicy Level": "Medium",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 480,
    },
    {
        "Name": "Truffle Tagliatelle",
        "Category": "Pasta",
        "Price": 22.00,
        "Description": "Fresh egg tagliatelle with black truffle, wild mushrooms, shaved Parmesan, and truffle oil.",
        "Allergens": "Gluten, Eggs, Dairy",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "No",
        "Calories": 570,
    },
    # ── Mains ───────────────────────────────────────────
    {
        "Name": "Grilled Salmon Fillet",
        "Category": "Mains",
        "Price": 24.99,
        "Description": "Atlantic salmon fillet grilled to perfection, served with lemon butter sauce, asparagus, and roasted potatoes.",
        "Allergens": "Fish, Dairy",
        "Spicy Level": "None",
        "Vegetarian": "No",
        "Vegan": "No",
        "Calories": 520,
    },
    {
        "Name": "8oz Ribeye Steak",
        "Category": "Mains",
        "Price": 34.99,
        "Description": "USDA prime ribeye cooked to your preference, served with house fries, grilled tomato, and peppercorn sauce.",
        "Allergens": "Dairy",
        "Spicy Level": "None",
        "Vegetarian": "No",
        "Vegan": "No",
        "Calories": 720,
    },
    {
        "Name": "Margherita Pizza",
        "Category": "Mains",
        "Price": 14.99,
        "Description": "12-inch Neapolitan-style pizza with San Marzano tomato sauce, fresh mozzarella, and fresh basil.",
        "Allergens": "Gluten, Dairy",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "No",
        "Calories": 680,
    },
    {
        "Name": "Spicy Diavola Pizza",
        "Category": "Mains",
        "Price": 16.99,
        "Description": "Spicy salami, nduja, jalapeños, mozzarella, and chili oil on a crispy Neapolitan base.",
        "Allergens": "Gluten, Dairy",
        "Spicy Level": "High",
        "Vegetarian": "No",
        "Vegan": "No",
        "Calories": 780,
    },
    {
        "Name": "Mushroom & Spinach Risotto",
        "Category": "Mains",
        "Price": 17.99,
        "Description": "Creamy Arborio risotto with wild mushrooms, baby spinach, white wine, and Parmesan.",
        "Allergens": "Dairy",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "No",
        "Calories": 490,
    },
    {
        "Name": "Vegan Buddha Bowl",
        "Category": "Mains",
        "Price": 15.99,
        "Description": "Brown rice, roasted sweet potato, edamame, avocado, cucumber, and miso-ginger dressing.",
        "Allergens": "Sesame, Soy",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 450,
    },
    # ── Desserts ────────────────────────────────────────
    {
        "Name": "Tiramisu",
        "Category": "Desserts",
        "Price": 8.99,
        "Description": "Classic Italian tiramisu with mascarpone, espresso-soaked ladyfingers, and cocoa dusting.",
        "Allergens": "Gluten, Eggs, Dairy",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "No",
        "Calories": 380,
    },
    {
        "Name": "Chocolate Fondant",
        "Category": "Desserts",
        "Price": 9.99,
        "Description": "Warm dark chocolate fondant with a molten center, served with vanilla bean ice cream.",
        "Allergens": "Gluten, Eggs, Dairy",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "No",
        "Calories": 480,
    },
    {
        "Name": "Vegan Mango Sorbet",
        "Category": "Desserts",
        "Price": 6.99,
        "Description": "Three scoops of refreshing mango sorbet made with real Alphonso mangoes. Naturally vegan.",
        "Allergens": "None",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 160,
    },
    # ── Drinks ──────────────────────────────────────────
    {
        "Name": "Fresh Orange Juice",
        "Category": "Drinks",
        "Price": 4.50,
        "Description": "Freshly squeezed orange juice, served chilled.",
        "Allergens": "None",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 110,
    },
    {
        "Name": "Sparkling Water (500ml)",
        "Category": "Drinks",
        "Price": 2.99,
        "Description": "Premium Italian sparkling mineral water.",
        "Allergens": "None",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 0,
    },
    {
        "Name": "House Red Wine (Glass)",
        "Category": "Drinks",
        "Price": 7.50,
        "Description": "Smooth Montepulciano d'Abruzzo, full-bodied with notes of cherry and spice.",
        "Allergens": "Sulphites",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 125,
    },
    {
        "Name": "Aperol Spritz",
        "Category": "Drinks",
        "Price": 9.99,
        "Description": "Classic Italian aperitivo: Aperol, Prosecco, soda water, and a slice of orange.",
        "Allergens": "Sulphites",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 158,
    },
    {
        "Name": "Espresso",
        "Category": "Drinks",
        "Price": 2.99,
        "Description": "Single shot of our house-blend espresso, rich and aromatic.",
        "Allergens": "None",
        "Spicy Level": "None",
        "Vegetarian": "Yes",
        "Vegan": "Yes",
        "Calories": 5,
    },
]


def generate():
    df = pd.DataFrame(MENU_DATA)

    # Save in the project root
    output_path = os.path.join(os.path.dirname(__file__), "sample_menu.xlsx")
    df.to_excel(output_path, index=False, engine="openpyxl")

    print(f"✅ Sample menu saved to: {output_path}")
    print(f"   {len(df)} items across {df['Category'].nunique()} categories:")
    for cat, count in df.groupby("Category").size().items():
        print(f"   • {cat}: {count} items")


if __name__ == "__main__":
    generate()
