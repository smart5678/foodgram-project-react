.mode csv
.import ../data/ingredients.csv temp
INSERT INTO recipes_ingredient (name, measurement_unit) SELECT * FROM temp;
