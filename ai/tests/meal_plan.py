from ai.models.meal_plan import MealPlan

meal_plan_json = '''{
  "title": "Weekly Plan with Asian Dinners",
  "notes": "Includes repeated breakfast, lunch, snack; varied Asian-inspired medium-complexity dinners; includes high-protein elements and healthy fats.",
  "plan": [
    {
      "meal_day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
      "meal_time": ["Breakfast"],
      "recipe": {
        "title": "Breakfast Burrito",
        "dietary_preferences": [],
        "description": "Hearty burrito with eggs, beans, avocado.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 650.0, "protein": 32.0, "fat": 28.0, "carbohydrates": 55.0},
        "complexity": "Easy",
        "ingredients": [
          {"name": "tortilla", "quantity": 1.0, "unit": "units", "description": "large flour"},
          {"name": "egg", "quantity": 2.0, "unit": "units", "description": "scrambled"},
          {"name": "black beans", "quantity": 80.0, "unit": "grams", "description": "heated"},
          {"name": "avocado", "quantity": 50.0, "unit": "grams", "description": "sliced"},
          {"name": "olive oil", "quantity": 10.0, "unit": "ml", "description": "for cooking"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Scramble eggs in olive oil."},
          {"step_number": 2, "description": "Warm tortilla."},
          {"step_number": 3, "description": "Fill with eggs, beans, avocado and wrap."}
        ]
      }
    },
    {
      "meal_day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
      "meal_time": ["Lunch"],
      "recipe": {
        "title": "Chicken Caesar Wrap",
        "dietary_preferences": [],
        "description": "High‑protein chicken Caesar wrap.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 700.0, "protein": 55.0, "fat": 28.0, "carbohydrates": 60.0},
        "complexity": "Easy",
        "ingredients": [
          {"name": "tortilla", "quantity": 1.0, "unit": "units", "description": "large"},
          {"name": "chicken breast", "quantity": 150.0, "unit": "grams", "description": "cooked, sliced"},
          {"name": "romaine lettuce", "quantity": 60.0, "unit": "grams", "description": "chopped"},
          {"name": "Caesar dressing", "quantity": 30.0, "unit": "ml", "description": "creamy"},
          {"name": "olive oil", "quantity": 5.0, "unit": "ml", "description": "drizzle"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Mix lettuce with dressing."},
          {"step_number": 2, "description": "Add chicken and toss."},
          {"step_number": 3, "description": "Place mix in tortilla, drizzle oil, wrap."}
        ]
      }
    },
    {
      "meal_day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
      "meal_time": ["Snack"],
      "recipe": {
        "title": "Protein Smoothie",
        "dietary_preferences": [],
        "description": "High‑protein smoothie with fruit.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 450.0, "protein": 40.0, "fat": 10.0, "carbohydrates": 45.0},
        "complexity": "Easy",
        "ingredients": [
          {"name": "protein powder", "quantity": 1.0, "unit": "units", "description": "scoop"},
          {"name": "banana", "quantity": 1.0, "unit": "units", "description": "ripe"},
          {"name": "almond milk", "quantity": 250.0, "unit": "ml", "description": "unsweetened"},
          {"name": "peanut butter", "quantity": 20.0, "unit": "grams", "description": "creamy"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Combine all ingredients."},
          {"step_number": 2, "description": "Blend until smooth."}
        ]
      }
    },
    {
      "meal_day": ["Monday"],
      "meal_time": ["Dinner"],
      "recipe": {
        "title": "Teriyaki Tofu Stir Fry",
        "dietary_preferences": [],
        "description": "Tofu stir fry with vegetables and teriyaki sauce.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 600.0, "protein": 35.0, "fat": 20.0, "carbohydrates": 70.0},
        "complexity": "Medium",
        "ingredients": [
          {"name": "tofu", "quantity": 150.0, "unit": "grams", "description": "firm, cubed"},
          {"name": "broccoli", "quantity": 100.0, "unit": "grams", "description": "florets"},
          {"name": "bell pepper", "quantity": 1.0, "unit": "units", "description": "sliced"},
          {"name": "teriyaki sauce", "quantity": 60.0, "unit": "ml", "description": "bottled"},
          {"name": "olive oil", "quantity": 10.0, "unit": "ml", "description": "for cooking"},
          {"name": "rice", "quantity": 150.0, "unit": "grams", "description": "cooked"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Pan‑fry tofu in oil."},
          {"step_number": 2, "description": "Add vegetables and cook."},
          {"step_number": 3, "description": "Stir in teriyaki and serve over rice."}
        ]
      }
    },
    {
      "meal_day": ["Tuesday"],
      "meal_time": ["Dinner"],
      "recipe": {
        "title": "Sesame Chicken Bowl",
        "dietary_preferences": [],
        "description": "Chicken with sesame sauce over rice.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 650.0, "protein": 45.0, "fat": 22.0, "carbohydrates": 75.0},
        "complexity": "Medium",
        "ingredients": [
          {"name": "chicken breast", "quantity": 150.0, "unit": "grams", "description": "cubed"},
          {"name": "soy sauce", "quantity": 30.0, "unit": "ml", "description": "for sauce"},
          {"name": "sesame oil", "quantity": 10.0, "unit": "ml", "description": "aromatic"},
          {"name": "honey", "quantity": 15.0, "unit": "grams", "description": "for sauce"},
          {"name": "broccoli", "quantity": 100.0, "unit": "grams", "description": "florets"},
          {"name": "rice", "quantity": 150.0, "unit": "grams", "description": "cooked"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Cook chicken in pan."},
          {"step_number": 2, "description": "Add sauce ingredients."},
          {"step_number": 3, "description": "Add broccoli and simmer."},
          {"step_number": 4, "description": "Serve over rice."}
        ]
      }
    },
    {
      "meal_day": ["Wednesday"],
      "meal_time": ["Dinner"],
      "recipe": {
        "title": "Beef Bulgogi Plate",
        "dietary_preferences": [],
        "description": "Korean‑style bulgogi beef with rice.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 700.0, "protein": 40.0, "fat": 25.0, "carbohydrates": 80.0},
        "complexity": "Medium",
        "ingredients": [
          {"name": "beef slices", "quantity": 150.0, "unit": "grams", "description": "thin"},
          {"name": "soy sauce", "quantity": 30.0, "unit": "ml", "description": "marinade"},
          {"name": "garlic", "quantity": 2.0, "unit": "units", "description": "minced"},
          {"name": "sugar", "quantity": 10.0, "unit": "grams", "description": "for marinade"},
          {"name": "sesame oil", "quantity": 10.0, "unit": "ml", "description": "for flavor"},
          {"name": "rice", "quantity": 150.0, "unit": "grams", "description": "cooked"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Marinate beef."},
          {"step_number": 2, "description": "Stir fry on high heat."},
          {"step_number": 3, "description": "Serve over rice."}
        ]
      }
    },
    {
      "meal_day": ["Thursday"],
      "meal_time": ["Dinner"],
      "recipe": {
        "title": "Spicy Thai Basil Chicken",
        "dietary_preferences": [],
        "description": "Ground chicken stir fry with basil and chili.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 640.0, "protein": 45.0, "fat": 20.0, "carbohydrates": 75.0},
        "complexity": "Medium",
        "ingredients": [
          {"name": "ground chicken", "quantity": 150.0, "unit": "grams", "description": "fresh"},
          {"name": "garlic", "quantity": 2.0, "unit": "units", "description": "minced"},
          {"name": "soy sauce", "quantity": 20.0, "unit": "ml", "description": "for seasoning"},
          {"name": "chili paste", "quantity": 15.0, "unit": "grams", "description": "spicy"},
          {"name": "basil", "quantity": 20.0, "unit": "grams", "description": "fresh leaves"},
          {"name": "rice", "quantity": 150.0, "unit": "grams", "description": "cooked"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Cook chicken with garlic."},
          {"step_number": 2, "description": "Add sauce and chili."},
          {"step_number": 3, "description": "Stir in basil and serve over rice."}
        ]
      }
    },
    {
      "meal_day": ["Friday"],
      "meal_time": ["Dinner"],
      "recipe": {
        "title": "Salmon Miso Bowl",
        "dietary_preferences": [],
        "description": "Baked salmon with miso glaze and rice.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 720.0, "protein": 48.0, "fat": 28.0, "carbohydrates": 70.0},
        "complexity": "Medium",
        "ingredients": [
          {"name": "salmon", "quantity": 150.0, "unit": "grams", "description": "filet"},
          {"name": "miso paste", "quantity": 20.0, "unit": "grams", "description": "for glaze"},
          {"name": "soy sauce", "quantity": 15.0, "unit": "ml", "description": "for glaze"},
          {"name": "honey", "quantity": 10.0, "unit": "grams", "description": "for glaze"},
          {"name": "rice", "quantity": 150.0, "unit": "grams", "description": "cooked"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Mix glaze ingredients."},
          {"step_number": 2, "description": "Brush on salmon and bake at 400F for 12 minutes."},
          {"step_number": 3, "description": "Serve over rice."}
        ]
      }
    },
    {
      "meal_day": ["Saturday"],
      "meal_time": ["Dinner"],
      "recipe": {
        "title": "Shrimp Pad Thai",
        "dietary_preferences": [],
        "description": "Classic pad Thai with shrimp.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 680.0, "protein": 38.0, "fat": 18.0, "carbohydrates": 90.0},
        "complexity": "Medium",
        "ingredients": [
          {"name": "shrimp", "quantity": 150.0, "unit": "grams", "description": "peeled"},
          {"name": "rice noodles", "quantity": 120.0, "unit": "grams", "description": "dry"},
          {"name": "soy sauce", "quantity": 20.0, "unit": "ml", "description": "for sauce"},
          {"name": "lime", "quantity": 1.0, "unit": "units", "description": "juiced"},
          {"name": "peanuts", "quantity": 20.0, "unit": "grams", "description": "crushed"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Cook noodles."},
          {"step_number": 2, "description": "Stir fry shrimp."},
          {"step_number": 3, "description": "Add noodles, sauce, peanuts, and lime."}
        ]
      }
    },
    {
      "meal_day": ["Sunday"],
      "meal_time": ["Dinner"],
      "recipe": {
        "title": "Vegetable Ramen Bowl",
        "dietary_preferences": [],
        "description": "Hearty Asian ramen with veggies.",
        "comments": "",
        "number_of_servings": 1,
        "nutritional_info": {"calories": 650.0, "protein": 28.0, "fat": 18.0, "carbohydrates": 90.0},
        "complexity": "Medium",
        "ingredients": [
          {"name": "ramen noodles", "quantity": 1.0, "unit": "units", "description": "packet"},
          {"name": "vegetable broth", "quantity": 350.0, "unit": "ml", "description": "hot"},
          {"name": "mushrooms", "quantity": 80.0, "unit": "grams", "description": "sliced"},
          {"name": "bok choy", "quantity": 80.0, "unit": "grams", "description": "chopped"},
          {"name": "soy sauce", "quantity": 15.0, "unit": "ml", "description": "for seasoning"}
        ],
        "instructions": [
          {"step_number": 1, "description": "Simmer broth with mushrooms."},
          {"step_number": 2, "description": "Add bok choy."},
          {"step_number": 3, "description": "Cook noodles and combine."}
        ]
      }
    }
  ]
}'''

meal_plan = MealPlan.model_validate_json(meal_plan_json)
print(meal_plan.to_summary())
print(meal_plan)