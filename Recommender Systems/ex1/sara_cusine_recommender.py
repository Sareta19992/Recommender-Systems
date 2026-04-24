import json
from collections import Counter
from apyori import apriori

# -----------------------------
# Load dataset
# -----------------------------
with open("recipies.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

# -----------------------------
# Basic data analysis
# -----------------------------
total_recipes = len(recipes)
cuisine_counts = Counter(recipe["cuisine"] for recipe in recipes)
all_cuisines = sorted(cuisine_counts.keys())

print("=== BASIC DATA ANALYSIS ===")
print(f"Total number of recipes: {total_recipes}")
print(f"Number of cuisines available: {len(all_cuisines)}")
print("\nCuisine type and number of recipes:")
for cuisine, count in sorted(cuisine_counts.items()):
    print(f"{cuisine}: {count}")


# -----------------------------
# Recommendation function
# -----------------------------
def recommend_ingredients(cuisine_type):
    selected_recipes = [
        recipe for recipe in recipes
        if recipe["cuisine"].lower() == cuisine_type.lower()
    ]

    if not selected_recipes:
        print(f"\nWe don't have recommendations for {cuisine_type}")
        return

    transactions = [recipe["ingredients"] for recipe in selected_recipes]

    # Assignment says:
    # support = 100 / total number of recipes for selected cuisine
    # Apriori expects support as a fraction between 0 and 1,
    # so we convert it safely.
    min_support_value = min(100 / len(selected_recipes), 1.0)

    results = list(apriori(
        transactions,
        min_support=min_support_value,
        min_confidence=0.5,
        min_lift=1,
        min_length=2
    ))

    print(f"\n=== RECOMMENDATIONS FOR {cuisine_type.upper()} ===")

    if not results:
        print("No association rules were found for this cuisine.")
        return

    # Top group of ingredients = first relation record
    first_record = results[0]
    top_ingredients = list(first_record.items)

    print("\nTop group of ingredients:")
    print(top_ingredients)

    print("\nRules with lift greater than 2:")
    found_rule = False

    for record in results:
        for stat in record.ordered_statistics:
            if stat.lift > 2:
                found_rule = True
                left_side = list(stat.items_base)
                right_side = list(stat.items_add)
                print(
                    f"{left_side} -> {right_side} | "
                    f"Confidence: {stat.confidence:.2f} | "
                    f"Lift: {stat.lift:.2f}"
                )

    if not found_rule:
        print("No rules found with lift greater than 2.")


# -----------------------------
# User input loop
# -----------------------------
while True:
    user_input = input("\nEnter a cuisine type (or type 'exit' to quit): ").strip()

    if user_input.lower() == "exit":
        print("Program ended.")
        break

    recommend_ingredients(user_input)