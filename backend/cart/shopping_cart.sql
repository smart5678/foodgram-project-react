SELECT recipes_ingredient.name, SUM(amount)
FROM recipes_recipeingredients
    JOIN recipes_ingredient
        ON recipes_recipeingredients.ingredient_id=recipes_ingredient.id
    JOIN recipes_recipe
        ON recipes_recipe.id=recipes_recipeingredients.recipe_id
WHERE recipe_id IN (SELECT recipe_id FROM cart_cart WHERE cart_cart.user_id=1)
GROUP BY recipes_ingredient.name;
-- https://stackoverflow.com/questions/13092268/how-do-you-join-two-tables-on-a-foreign-key-field-using-django-orm