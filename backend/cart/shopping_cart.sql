SELECT recipes_ingredient.name, SUM(amount)
FROM recipes_recipeingredients
    JOIN recipes_ingredient
        ON recipes_recipeingredients.ingredient_id=recipes_ingredient.id
    JOIN recipes_recipe
        ON recipes_recipe.id=recipes_recipeingredients.recipe_id
WHERE recipe_id IN (SELECT recipe_id FROM cart_cart WHERE cart_cart.user_id=1)
GROUP BY recipes_ingredient.name;
-- https://stackoverflow.com/questions/13092268/how-do-you-join-two-tables-on-a-foreign-key-field-using-django-orm
/*
 1

In Django 3.2, the framework automatically follows relationships when using method QuerySet.filter()

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
>>> Choice.objects.filter(question__pub_date__year=current_year)
This compiles to the following SQL query:

SELECT
    "polls_choice"."id",
    "polls_choice"."question_id",
    "polls_choice"."choice_text",
    "polls_choice"."votes"
FROM
    "polls_choice"
INNER JOIN "polls_question" ON
    ("polls_choice"."question_id" = "polls_question"."id")
WHERE
    "polls_question"."pub_date" BETWEEN 2020-12-31 23:00:00 AND 2021-12-31 22:59:59.999999
 */