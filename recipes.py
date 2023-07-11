# -*- coding: utf-8 -*-
"""PythonTest2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1psr1SX8TLbmgGERXFosk0Ke3H17HK1x0
"""

from google.colab import drive
drive.mount('/content/drive')

import re

file_path = "/content/recipes_data.txt"

class Recipes:
    def __init__(self, recipes):
        self.recipes = recipes

    def get_recipe_names(self):
        with open(self.recipes, 'r') as f:
             content = f.read()

        self.content = content
        names = []
        for name in re.findall(r"\w+\s*\w+:", content):
            name = re.sub(":", "", name)
            names.append(name)

        self.names = names
        return  self.names



    def get_ingredients(self):
        ingredients = {}
        for name in self.names:
            ingredients[name] = {}
            pattern = re.compile(f"{name}:\n[-]+\n(.*?)\n[-]+", re.DOTALL)
            for text in re.findall(pattern, self.content):
                for string in re.findall(r"^(?!-).*$", text, re.MULTILINE):
                    for ingredient in re.findall(r"(.*?)\s*=", string, re.DOTALL):
                        ingredients[name][ingredient] = re.findall(r"\d+%*.*?\s*\w*.*?", string, re.DOTALL)

        self.ingredients = ingredients
        return self.ingredients



    def write_recipes(self, separator = "-", text_position = "center"):
        path = "/content/"
        for name in self.names:
            file_name = path + name + str("_recipes.txt")
            ingredients = self.ingredients[name]
            with open(file_name, 'w') as f:
                 headers = ["Combinations"]
                 for ingredient in ingredients.keys():
                     headers.append(ingredient)

                 max_cell_length = len(headers[0]) + 4
                 number_of_cells = len(headers)

                 for a in range(len(headers)):
                     header = headers[a]
                     spacing = max_cell_length - len(header)

                     if a == 0:
                        title = "|" + self.get_aligned_text(header, spacing, text_position) + "|"
                        f.write(title)
                     else:
                        title = self.get_aligned_text(header, spacing, text_position) + "|"
                        f.write(title)

                 f.write("\n")
                 f.write(self.get_separators(max_cell_length, number_of_cells, separator))
                 f.write("\n")
                 f.write(self.get_combination(ingredients, max_cell_length, number_of_cells, text_position))
                 f.write("\n")
                 f.write(self.get_separators(max_cell_length, number_of_cells, separator, add_bar = False))



    def get_combination(self, ingredients, max_cell_length, number_of_cells, text_position):
        keys = list(ingredients.keys())

        N = 1
        for key in keys:
            N *= len(ingredients[key])

        options = [ingredients[k] for k in keys]
        k = len(keys)
        indices = [0] * k
        combinations = []

        while True:
          for i in range(k):
              ingredient = keys[i]
              option_index = indices[i]
              combinations.append(options[i][option_index])


          j = k - 1
          while j >= 0:
            indices[j] += 1
            if indices[j] == len(options[j]):
              indices[j] = 0
              j -= 1
            else:
              break

          if j < 0:
            break

        n = number_of_cells - 1
        combinations = [combinations[i * n:(i + 1) * n] for i in range((len(combinations) + n - 1) // n )]


        combination_text = ""

        for n, combination in enumerate(combinations, start = 1):
            combination.insert(0, str(n))
            for i in range(len(combination)):
                string = combination[i]
                spacing = max_cell_length - len(string)

                if i == 0:
                   combination_text += "|" + self.get_aligned_text(string, spacing, text_position) + "|"
                else:
                  combination_text += self.get_aligned_text(string, spacing, text_position) + "|"

            if int(n) < N:
               combination_text += "\n"

        # combination_text = ""
        # separator_line = "|"
        # for n in range(1, N + 1):
        #     n = str(n)
        #     spacing = max_cell_length - len(n)
        #     combination_text += separator_line + self.get_aligned_text(n, spacing, text_position) + "|"
        #     if int(n) < N:
        #        combination_text += "\n"

        return combination_text




    def get_aligned_text(self, text, spacing, text_position = "center"):
        if text_position == "left":
           aligned_text = text + " " * spacing
        elif text_position == "center":
             d = spacing + len(text)
             # aligned_text = " " * int(spacing/2) + text + " " * int(spacing/2)
             aligned_text = f"{text : ^{d}}"
        elif text_position == "right":
           aligned_text = " " * spacing + text
        else:
           print("Enter the correct alignment.")

        return aligned_text




    def get_separators(self, max_cell_length, number_of_cells, separator = "-", add_bar = True):
        if add_bar:
           separator_line = "|"
           separators = separator * max_cell_length
           for i in range(number_of_cells):
               separator_line += separators + "|"
        else:
          separator_line = separator * (max_cell_length + 2) * (number_of_cells - 1)

        return separator_line

recipes = Recipes(file_path)

recipes.get_recipe_names()
recipes.get_ingredients()["Chocolate"]

recipes.write_recipes(separator = "-", text_position = "center")