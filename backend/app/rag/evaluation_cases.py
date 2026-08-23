"""Small, manually labeled search set for retrieval evaluation.

These labels are a starting point, not an exhaustive list of every relevant
recipe in the dataset. Add or remove recipes as you inspect search results.
"""


EVALUATION_CASES = [
    {
        "query": "chicken curry recipes",
        "relevant_recipes": {
            32: "Dad’s Curried Chicken",
            330: "Green Curry Vinegar Chicken",
            405: "Malaysian Chicken Curry with Buttermilk Beer Beignets",
            1650: "Curried Chicken Drumsticks",
            1685: "Fragrant Green Chicken Curry",
            1901: "3-Ingredient Curry Grilled Chicken Wings",
            2260: "22-Minute Coconut Chicken Curry",
            2949: "Easy Green Curry with Chicken, Bell Pepper, and Sugar Snap Peas",
        },
    },
    {
        "query": "rich chocolate cake",
        "relevant_recipes": {
            577: "Killer Chocolate Cake",
            711: "Chocolatey Chocolate Cake",
            908: "Crunchy Chocolate Caramel Layer Cake",
            1313: "BA's Best Chocolate Macaroon Cake",
            1578: "Double Chocolate Cake with Peppermint-Chocolate Frosting",
            1802: "Chocolate Spoonful Cake",
            1958: "Chocolate and Passionfruit Layer Cake",
            2468: "Hershey's \"Perfectly Chocolate\" Chocolate Cake",
        },
    },
    {
        "query": "homemade apple pie",
        "relevant_recipes": {
            1068: "Bacon-Latticed Apple Pie",
            1585: "Our Favorite Apple Pie",
            1588: "BA's Best Deep-Dish Apple Pie",
            1615: "Salted Apple Pretzel Pie",
            2492: "Classic Apple Pie",
            3337: "Layered Apple Pie With Phyllo Crust",
            5726: "Tiny Fried Apple Pies",
            5926: "Rum Raisin Apple Pie",
        },
    },
    {
        "query": "grilled salmon dinner",
        "relevant_recipes": {
            1163: "Grilled Salmon Steaks with Cilantro-Garlic Yogurt Sauce",
            1217: "Grilled Salmon with Meyer Lemons and Creamy Cucumber Salad",
            1892: "Grilled Salmon Collars",
            2016: "Whole Grilled Salmon with Chanterelles",
            2996: "Grilled Wild Salmon with Garlic Scape Pesto and Summer Squash",
            5538: "Grilled Salmon with Orzo, Feta, and Red Wine Vinaigrette",
            7218: "Herb-Grilled Salmon with Fresh Tomato-Orange Chutney",
            7662: "Grilled Salmon with Quick Blueberry Pan Sauce",
        },
    },
    {
        "query": "hearty beef stew",
        "relevant_recipes": {
            1926: "Somali Beef Stew with Spiced Rice (Bariis Maraq)",
            4067: "Beef Stew in the Crock Pot",
            4898: "Thai Beef Stew with Lemongrass and Noodles",
            6568: "Curried Beef Stew",
            7171: "Red Wine Beef Stew",
            7877: "Beef Stew",
            8128: "Beef Stew with Leeks",
            9307: "Beef Stew with Potatoes and Carrots",
        },
    },
    {
        "query": "sweet breakfast pancakes with fruit",
        "relevant_recipes": {
            844: "Almond Butter and Banana Pancakes",
            949: "Sheet-Pan Cider-Ricotta Pancakes with Pear Compote",
            1299: "Whole Grain Pancakes with Blackberries",
            1671: "Gluten-Free Blueberry Pancakes with Caramelized Bananas",
            2434: "Oat and Apple Pancakes with Yogurt",
            3796: "Fresh Raspberry-Quinoa Pancakes",
            3828: "Buttermilk Pancakes with Roasted Strawberries",
            4015: "Gluten-Free Banana-Almond Pancakes with Date Caramel",
        },
    },
    {
        "query": "shrimp pasta with tomato sauce",
        "relevant_recipes": {
            1485: "Greek-Style Shrimp Pasta with Kale",
            2031: "One-Pot Pasta Primavera with Shrimp",
            2070: "Pasta with Shrimp in Tomato Cream",
            2518: "Rock Shrimp Pasta with Spicy Tomato Sauce",
            3044: "Pasta with Rock Shrimp, Chile, and Lemon",
            4009: "Squid Ink Pasta with Shrimp, Nduja, and Tomato",
            11978: "Shrimp Scampi Pasta",
        },
    },
    {
        "query": "warm lentil soup",
        "relevant_recipes": {
            329: "Chicken-Lentil Soup With Jammy Onions",
            839: "Lentil Soup with Wheat Berries and Kale",
            1401: "Lentil and Chicken Soup with Sweet Potatoes and Escarole",
            1524: "Curried Lentil, Tomato, and Coconut Soup",
            3853: "Four Corners Lentil Soup",
            7451: "Curried Lentil Soup",
            9134: "Curried-Squash and Red-Lentil Soup",
        },
    },
    {
        "query": "roast turkey for thanksgiving",
        "relevant_recipes": {
            485: "Expertly Spiced and Glazed Roast Turkey",
            937: "Dry-Rubbed Roast Turkey",
            1006: "The Simplest Roast Turkey",
            1604: "Very Classic Dry-Brined Roast Turkey",
            2445: "Easy Roast Turkey With No-Roux Gravy",
            3311: "Garlic-Aioli Roasted Turkey with Lemon-Parsley Pan Sauce",
            3339: "Roasted Turkey Legs With Ghee",
            3352: "Porchetta-Style Roast Turkey Breast",
        },
    },
    {
        "query": "creamy mushroom risotto",
        "relevant_recipes": {
            334: "Risotto With Mushrooms and Thyme",
            884: "Oven Risotto with Crispy Roasted Mushrooms",
            1199: "Instant Pot Mushroom Risotto",
            5985: "Turkey and Mushroom Risotto",
            7542: "Wild Mushroom Risotto",
            10656: "Risotto with Leeks, Shiitake Mushrooms, and Truffles",
            12663: "Mushroom Risotto",
            13125: "Wild Mushroom Risotto",
        },
    },
]
