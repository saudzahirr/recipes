# Recipes

 Imagine you have a unique cookbook with different recipes. Each recipe comes with its own unique name and a list of ingredients, each with its own specific quantity. Now, let's embark on an imaginative journey to discover all the possibilities of ingredient combinations for each recipe, aiming to unearth the most tantalizing and delightful taste experiences.
This code is designed to assist in organizing and generating recipe files. It provides a convenient way to extract dish names and ingredients from a recipe data file and create individual recipe files for each dish. The script utilizes regular expressions to parse the recipe data, allowing for flexibility in handling different file formats. With customizable formatting options, users can specify the title, separators, and text alignment for the generated recipe files. It includes functionality to extract recipe names and ingredients from a text file, and also to generate recipe files with different combinations of ingredients.


## Features

- Extract names of dishes from a recipes data file.
- Extract ingredients and their weights for each dish.
- Generate recipe files with different combinations of ingredients.

## Usage

1. Ensure you have a recipes data file in the specified format.
   
   ```
   [Recipe Name]:
   ----------------------------------------------------------------
   [Ingredient 1] = [Quantity 1], [Quantity 2], [Quantity 3], ...
   [Ingredient 2] = [Quantity 1], [Quantity 2], [Quantity 3], ...
   [Ingredient 3] = [Quantity 1], [Quantity 2], [Quantity 3], ...
   .
   .
   .
   ----------------------------------------------------------------
   ...
   ```
2. Update the `file_path` variable in the code with the correct path to your recipes data file.
3. Create an instance of the `Recipes` class with the file path:

   ```python
   recipes = Recipes(file_path)
   ```
4. Call the `get_recipe_names()` method to extract the names of the dishes:

   ```python
   recipe_names = recipes.get_recipe_names()
   ```
5. Call the `get_ingredients()` method to extract the ingredients for each dish:

   ```python
   ingredients = recipes.get_ingredients()
   ```
6. Optionally, modify the parameters for the `write_recipes()` method to customize the generated recipe files. By default, the method generates files with a serial title of 
   "Combinations", a separator of "-", and centers the text:

   ```python
   recipes.write_recipes(serial_title="Combinations", separator="-", text_position="center")
   ```
7. By default, the output format is as:

   ```
   |  Combinations  |     [Ingredient 1]      |      [Ingredient 2]      |     [Ingredient 3]      | ...
   |----------------|-------------------------|--------------------------|-------------------------| ...
   |       1        |      [Quantity 1]       |       [Quantity 1]       |      [Quantity 1]       | ...
   |       2        |      [Quantity 1]       |       [Quantity 1]       |      [Quantity 2]       | ...
   |       3        |      [Quantity 1]       |       [Quantity 2]       |      [Quantity 3]       | ...
   |       4        |      [Quantity 1]       |       [Quantity 2]       |      [Quantity 4]       | ...
   .
   .
   .
   ---------------------------------------------------------------------
   ```
## Methods
1. `get_recipe_names()`
   This method returns a list of names of the dishes extracted from the recipes data file.

2. `get_ingredients()`
   This method returns a dictionary with names of dishes as keys and a subdictionary with ingredient names as keys and a list of possible weights as values.

3. `write_recipes(serial_title="Combinations", separator="-", text_position="center")`
   This method generates recipe files with different combinations of ingredients. It accepts the following optional parameters:
   - serial_title: The title for the serial number column in the generated files. Defaults to "Combinations".
   - separator: The character used for separating cells in the generated files. Defaults to "-".
   - text_position: The alignment of the text in each cell. Can be "left", "center", or "right". Defaults to "center".

## Requirements
The "re" module, which stands for regular expressions, is part of the standard library in Python. It is available by default when you install Python, and you do not need to install any additional packages or libraries to use it.

To use the "re" module in your Python code, you can simply import it at the beginning of your script or interactive session like this:
```python
import re
```
`Python 3.11.3`

## Learn More
To learn more about regular expression, take a look at the following resources:
- [Python Regular Expression](https://docs.python.org/3/library/re.html)
- [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html)
