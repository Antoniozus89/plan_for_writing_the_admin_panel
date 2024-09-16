import sqlite3

def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            image_url TEXT NOT NULL  
            
        )
    ''')
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, description, price, image_url FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products

def populate_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    products = [
        {"title": "Продукт 1", "description": "Описание продукта 1", "price": 100,
         "image_url":
             "https://balthazar.club/uploads/posts/2022-10/1666112821_37-balthazar-club-p-tort-kusok-sala-pinterest-40.png"},
        {"title": "Продукт 2", "description": "Описание продукта 2", "price": 200,
         "image_url":
             "https://derevenskie-produkty-v-saratove.ru/f/store/item/82/00000282/cover/fullsize.jpg"},
        {"title": "Продукт 3", "description": "Описание продукта 3", "price": 300,
         "image_url":
             "https://i.pinimg.com/736x/d6/b2/e5/d6b2e57136c343f0d0ca4d6e9eb03813.jpg"},
        {"title": "Продукт 4", "description": "Описание продукта 4", "price": 400,
         "image_url":
             "https://klike.net/uploads/posts/2023-02/1675231900_4-122.jpg"}
    ]

    cursor.executemany('INSERT INTO Products (title, description, price, image_url) VALUES (:title, :description, :price, :image_url)', products)
    conn.commit()
    conn.close()
    print("Таблица Products успешно заполнена.")

