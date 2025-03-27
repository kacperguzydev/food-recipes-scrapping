import sqlite3

def create():
    with sqlite3.connect('recipes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT,
            image TEXT,
            name TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            ingredient TEXT,
            FOREIGN KEY (recipe_id) REFERENCES Recipes(id) ON DELETE CASCADE
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Directions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            direction TEXT,
            FOREIGN KEY (recipe_id) REFERENCES Recipes(id) ON DELETE CASCADE
        )
        ''')
        conn.commit()

def insert(food_recipes):
    with sqlite3.connect('recipes.db') as conn:
        cursor = conn.cursor()
        for recipe in food_recipes:
            cursor.execute('SELECT * FROM Recipes WHERE name = ?', (recipe['name'],))
            if cursor.fetchone():
                print(f"Recipe '{recipe['name']}' already exists. Skipping insertion.")
                continue

            cursor.execute('''
            INSERT INTO Recipes (link, image, name) VALUES (?, ?, ?)
            ''', (recipe['link'], recipe['image'], recipe['name']))

            recipe_id = cursor.lastrowid
            insert_ingredients(cursor, recipe_id, recipe['ingredients'])
            insert_directions(cursor, recipe_id, recipe['directions'])

        conn.commit()

def insert_ingredients(cursor, recipe_id, ingredients):
    for ingredient in ingredients:
        cursor.execute('''
        INSERT INTO Ingredients (recipe_id, ingredient) VALUES (?, ?)
        ''', (recipe_id, ingredient.strip()))

def insert_directions(cursor, recipe_id, directions):
    for direction in directions:
        cursor.execute('''
        INSERT INTO Directions (recipe_id, direction) VALUES (?, ?)
        ''', (recipe_id, direction.strip()))

def print_recipes():
    with sqlite3.connect('recipes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Recipes')
        recipes = cursor.fetchall()

        for recipe in recipes:
            recipe_id, link, image, name = recipe
            print(f"Recipe ID: {recipe_id}\nName: {name}\nLink: {link}\nImage: {image}\nIngredients:")
            cursor.execute('SELECT ingredient FROM Ingredients WHERE recipe_id = ?', (recipe_id,))
            ingredients = cursor.fetchall()
            for ingredient in ingredients:
                print(f" - {ingredient[0].strip()}")
            print("Directions:")
            cursor.execute('SELECT direction FROM Directions WHERE recipe_id = ?', (recipe_id,))
            directions = cursor.fetchall()
            for direction in directions:
                print(f" - {direction[0].strip()}")
            print("\n" + "-" * 40 + "\n")

def delete_all_records():
    with sqlite3.connect('recipes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Directions')
        cursor.execute('DELETE FROM Ingredients')
        cursor.execute('DELETE FROM Recipes')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="Recipes"')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="Ingredients"')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="Directions"')
        conn.commit()