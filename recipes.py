#!/usr/bin/env python
# coding: utf-8

import re


file_path = "Recipes/recipes_data.txt"



class Recipes:
    def __init__(self, recipes):
        self.recipes = recipes

    def get_recipe_names(self):
        """
        This function returns a
        list of names of the dishes.
        """
        
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
        """
        This function returns a dictionary with
        names of dishes as keys and a subdictionary
        with its keys as ingredient names and its
        value as a list of possible weights.
        """
        
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



    def get_recipes(self, serial_title = "Combinations", column_separator = "|", separator = "-",
                      text_position = "center", left_padding = 0, right_padding = 0, column_width = 0):
        
        path = "Recipes/"
        for name in self.names:
            file_name = path + name + str("_recipes.txt")
            ingredients = self.ingredients[name]
            with open(file_name, 'w') as f:
                headers = [serial_title]
                for ingredient_names in ingredients.keys():
                    headers.append(ingredient_names)
                
                title = name + " Recipes."
                f.write(f"{title: ^{len(title)}}" + "\n")
                self.write_combinations(f, headers, ingredients, column_separator, separator, text_position, left_padding, right_padding, column_width)



                
    def get_combinations(self, ingredients, number_of_cells):
        """
        This function returns the different
        possible combinations of ingredients
        for each recipe.
        """
        keys = list(ingredients.keys())

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
        
        # Breaking a combinations list into chunks of size n.
        n = number_of_cells - 1
        combinations = [combinations[i * n:(i + 1) * n] for i in range((len(combinations) + n - 1) // n )]

        return combinations




    def write_combinations(self, file, headers, ingredients, column_separator, separator, text_position, left_padding, right_padding, column_width):
        """
        This function writes the different
        possible combinations of ingredients
        for each recipe.
        """
        
        number_of_cells = len(headers)
        
        combinations = self.get_combinations(ingredients, len(headers))
        
        for n, combination in enumerate(combinations, start = 1):
            combination.insert(0, str(n))
        
        l = left_padding
        r = right_padding
        max_cell_lengths = [max([len(h), len(c)]) + l + r for h, c in zip(headers, combinations[:][-1])]
        
        for max_cell_length in max_cell_lengths:
            if column_width != 0 and column_width < max_cell_length:
                raise Exception("Column width should be greater than or equal to the maximum cell")

        
        # Calculating the number of rows (or number of possible combinations).
        N = 1
        for key in list(ingredients.keys()):
            N *= len(ingredients[key])
            
        combination_text = ""
        
        for combination in combinations:
            for i in range(len(combination)):
                string = combination[i]
                
                max_cell_length = column_width if column_width != 0 else max_cell_lengths[i]
                spacing = max_cell_length - len(string)
                
                if i == 0:
                    # Filling the first cell.
                    combination_text += column_separator + self.get_aligned_text(string, spacing, text_position, l, r) + column_separator
                else:
                    combination_text += self.get_aligned_text(string, spacing, text_position, l, r) + column_separator

            # Condition for adding a newline untill the last entry.
            if int(combination[0]) < N:
                combination_text += "\n"
                
                
        file.write(self.get_separators(max_cell_lengths, number_of_cells, column_width, column_separator, separator, add_column_separation = False))
        file.write("\n")
        
        for a in range(len(headers)):
            header = headers[a]
            
            # Number of white spaces in a cell.
            max_cell_length = column_width if column_width != 0 else max_cell_lengths[a]
            spacing = max_cell_length - len(header)
            
            # print(f"{header}, {len(header)}, {max_cell_length}, {spacing}")
            
            if a == 0:
                # Filling the first cell.
                title = column_separator + self.get_aligned_text(header, spacing, text_position, l, r) + column_separator
                file.write(title)
                
            else:
                title = self.get_aligned_text(header, spacing, text_position, l, r) + column_separator
                file.write(title)
        
        file.write("\n")
        file.write(self.get_separators(max_cell_lengths, number_of_cells, column_width, column_separator, separator))
        file.write("\n")
        
        file.write(combination_text)
        
        # Writing ending line of table.
        file.write("\n")
        file.write(self.get_separators(max_cell_lengths, number_of_cells, column_width, column_separator, separator, add_column_separation = False))
        
        
        
    
    def check_recipes(self):
        pass
    
    
    
    
    def get_aligned_text(self, text, spacing, text_position = "center", l = 0, r = 0):
        """
        This function sets the alignment
        of the text and returns aligned text.
        """
        
        if text_position == "left":
            spacing = spacing - l - r if l or r != 0 else spacing
            d = spacing + len(text)
            aligned_text = " " * l + f"{text : <{d}}" + " " * r
            
        elif text_position == "center":
            spacing = spacing - l - r if l or r != 0 else spacing
            d = spacing + len(text)
            aligned_text = " " * l + f"{text : ^{d}}" + " " * r
            
        elif text_position == "right":        
            spacing = spacing - l - r if l or r != 0 else spacing
            d = spacing + len(text)
            aligned_text = " " * l + f"{text : >{d}}" + " " * r
            
        else:
            raise ValueError("Enter the correct alignment. The correct alignments are left, center and right.")

        return aligned_text




    def get_separators(self, max_cell_lengths, number_of_cells, column_width, column_separator, separator = "-", add_column_separation = True):
        """
        This function returns a separator line
        (a separation between headers and table).
        """
        
        max_cell_lengths = [column_width] * number_of_cells if column_width != 0 else max_cell_lengths
        
        if add_column_separation:
            separator_line = column_separator
            for i in range(number_of_cells):
                separator_line += separator * max_cell_lengths[i] + column_separator
                
        else:
            # Endline.
            separator_line = "-"
            for i in range(number_of_cells):
                separator_line += separator * (max_cell_lengths[i] + 1)

        return separator_line




def main():
    recipes = Recipes(file_path)
    recipes.get_recipe_names()
    recipes.get_ingredients()
    
    recipes.get_recipes(serial_title = "Combinations", column_separator = "|", separator = "-",
                      text_position = "center", left_padding = 0, right_padding = 2, column_width = 0)

if __name__ == "__main__":
    main()
