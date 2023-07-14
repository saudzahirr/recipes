#!/usr/bin/env python
# coding: utf-8

import re



class Recipes:
    def __init__(self, recipes_file_name, output_file_path = "Recipes/", serial_title = "Combinations", column_separator = "|", separator = "-",
                 text_position = "center", left_padding = 0, right_padding = 0, column_width = 0):
        self.recipes_file_name = recipes_file_name
        self.output_file_path = output_file_path
        self.serial_title = serial_title
        self.column_separator = column_separator
        self.separator = separator
        self.text_position = text_position
        self.left_padding = left_padding
        self.right_padding = right_padding
        self.column_width = column_width


    def get_recipe_names(self):
        """
        This function returns a
        list of names of the dishes.
        """
        
        with open(self.recipes_file_name, 'r') as f:
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



                
    def get_aligned_text(self, text, spacing):
        """
        This function sets the alignment
        of the text and returns aligned text.
        """

        text_position = self.text_position
        l = self.left_padding
        r = self.right_padding
        
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




    def get_separators(self, max_cell_lengths, number_of_cells, add_column_separation = True):
        """
        This function returns a separator line
        (a separation between headers and table).
        """

        column_width = self.column_width
        column_separator = self.column_separator
        separator = self.separator
        
        max_cell_lengths = [column_width] * number_of_cells if column_width != 0 else max_cell_lengths
        
        if add_column_separation:
            separator_line = column_separator
            for i in range(number_of_cells):
                separator_line += separator * max_cell_lengths[i] + column_separator
                
        else:
            # Endline.
            separator_line = separator
            for i in range(number_of_cells):
                separator_line += separator * (max_cell_lengths[i] + 1)

        return separator_line




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




    def write_combinations(self, file, headers, ingredients):
        """
        This function writes the different
        possible combinations of ingredients
        for each recipe.
        """
        
        column_separator = self.column_separator
        separator = self.separator
        text_position = self.text_position
        left_padding = self.left_padding
        right_padding = self.right_padding
        column_width = self.column_width

        number_of_cells = len(headers)
        
        combinations = self.get_combinations(ingredients, len(headers))
        
        # Adding serial number to each combination.
        for n, combination in enumerate(combinations, start = 1):
            combination.insert(0, str(n))
        
        l = left_padding
        r = right_padding

        # Maximum cell length of each column.
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
                    combination_text += column_separator + self.get_aligned_text(string, spacing) + column_separator
                else:
                    combination_text += self.get_aligned_text(string, spacing) + column_separator

            # Condition for adding a newline untill the last entry.
            if int(combination[0]) < N:
                combination_text += "\n"
                
                
        file.write(self.get_separators(max_cell_lengths, number_of_cells, add_column_separation = False))
        file.write("\n")
        
        for a in range(len(headers)):
            header = headers[a]
            
            # Number of white spaces in a cell.
            max_cell_length = column_width if column_width != 0 else max_cell_lengths[a]
            spacing = max_cell_length - len(header)
            
            if a == 0:
                # Filling the first cell.
                title = column_separator + self.get_aligned_text(header, spacing) + column_separator
                file.write(title)
                
            else:
                title = self.get_aligned_text(header, spacing) + column_separator
                file.write(title)
        
        file.write("\n")
        file.write(self.get_separators(max_cell_lengths, number_of_cells))
        file.write("\n")
        
        file.write(combination_text)
        
        # Writing ending line of table.
        file.write("\n")
        file.write(self.get_separators(max_cell_lengths, number_of_cells, add_column_separation = False))
        
        
        
    
    def get_recipes(self):
        """
        This function writes seperate files of recipes
        and their respective possible combination of ingredients.
        """

        serial_title = self.serial_title
        
        path = self.output_file_path
        for name in self.names:
            file_name = path + name + str("_recipes.txt")
            ingredients = self.ingredients[name]
            with open(file_name, 'w') as f:
                headers = [serial_title]
                for ingredient_names in ingredients.keys():
                    headers.append(ingredient_names)
                
                title = name + " Recipes."
                f.write(f"{title: ^{len(title)}}" + "\n\n")
                self.write_combinations(f, headers, ingredients)




    def try_recipe(self):
        """
        This function is used to
        create a chef scorecard for
        each and every recipe. It is
        upto user that he wants to
        check each and every recipe.
        """

        recipe_name = input("Enter recipe name: ")
        
        if recipe_name not in self.names:
            raise Exception("Recipe not found.")
        
        path = self.output_file_path
        file_name = path + recipe_name + str("_recipes.txt")
        
        with open(file_name, 'r') as f:
            lines = f.readlines()
        
        scorecard = [[" ", " ", " ", " "]] * (len(lines) - 6)
        index = 5
        while index < len(lines) - 1:
            line = lines[index]
            quantities = line.strip("|").split("|")
            quantities = [re.sub("(^\s*|\s*$)", "", a) for a in quantities]
            
            quantities.insert(0, "Combination")
            quantities.insert(2, ":")
            quantities = " ".join(quantities)
            print(quantities)
            
            taste = int(input("Taste of this combination (/15): "))
            if taste < 0 or taste > 15:
                raise ValueError("Taste should be between 0 and 15.")
            
            texture = int(input("Texture of this combination (/10): "))
            if texture < 0 or texture > 10:
                raise ValueError("Texture should be between 0 and 10.")
            
            looks = int(input("Looks of this combination (/5): "))
            if looks < 0 or looks > 5:
                raise ValueError("Looks should be between 0 and 5.")
            
            
            total = taste + texture + looks

            print("Total rating (/30): ", total)
            print("\n")

            taste = str(taste) + "/15"
            texture = str(texture) + "/10"
            looks = str(looks) + "/5"
            total = str(total) + "/30"
            scorecard[index - 5] = [taste, texture, looks, total]

            enter = input("Press enter key to continue.")

            if enter == "":
                index += 1
            else:
                break
            
            print("\n")

        headers = ["Taste", "Texture", "Looks", "Total Rating"]

        column_separator = self.column_separator
        l = self.left_padding
        r = self.right_padding
        column_width = self.column_width
        max_cell_lengths = [max([len(h), len(c)]) + l + r for h, c in zip(headers, scorecard[:][-1])]
        
        for max_cell_length in max_cell_lengths:
            if column_width != 0 and column_width < max_cell_length:
                raise Exception("Column width should be greater than or equal to the maximum cell")

        
        scorecard_file = path + str("chef_scorecard.txt")
        self.scorecard_file = scorecard_file
        with open(scorecard_file, 'w') as f:
            for line in lines[:2]:
                f.write(line)
            
            f.write(re.sub("\n", "", lines[2]))
            f.write(self.get_separators(max_cell_lengths, len(headers), add_column_separation = False)[1:])
            f.write("\n")
            f.write(re.sub("\n", "", lines[3]))
            
            cursor_position = f.tell()
            f.seek(cursor_position)
            
            for a in range(len(headers)):
                header = headers[a]

                # Number of white spaces in a cell.
                max_cell_length = column_width if column_width != 0 else max_cell_lengths[a]
                spacing = max_cell_length - len(header)

                title = self.get_aligned_text(header, spacing) + column_separator
                f.write(title)
            
            f.write("\n")
            f.write(re.sub("\n", "", lines[4]))
            
            cursor_position = f.tell()
            f.seek(cursor_position)

            f.write(self.get_separators(max_cell_lengths, len(headers))[1:])
            f.write("\n")

            for line, score  in zip(lines[5:], scorecard):
                line = re.sub("\n", "", line)
                f.write(line)

                # To avoid overwriting the
                # text we set the cursor on
                # the last cursor position.
                cursor_position = f.tell()
                f.seek(cursor_position)

                extension = ""
                for i in range(len(score)):
                    string = score[i]
                    max_cell_length = column_width if column_width != 0 else max_cell_lengths[i]
                    spacing = max_cell_length - len(string)
                    extension += self.get_aligned_text(string, spacing) + column_separator
                    
                f.write(extension)
                f.write("\n")
            
            f.write(re.sub("\n", "", lines[2]))
            f.write(self.get_separators(max_cell_lengths, len(headers), add_column_separation = False)[1:])
            