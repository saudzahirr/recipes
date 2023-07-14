#!/usr/bin/env python
# coding: utf-8

from recipes import *
from display import *


file_path = "Recipes/recipes_data.txt"


def main():
    recipes = Recipes(
        file_path, output_file_path = "Recipes/",
        serial_title = "Combinations", column_separator = "|",
        separator = "-", text_position = "center", left_padding = 0,
        right_padding = 0, column_width = 0
    )
    recipes.get_recipe_names()
    recipes.get_ingredients()
    recipes.get_recipes()
    recipes.try_recipe()
    
    display()





if __name__ == "__main__":
    main()