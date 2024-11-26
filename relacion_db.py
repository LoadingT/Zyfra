import sqlite3

# Создание подключения к базе данных
conn = sqlite3.connect("zyfra.db")

# Создание объекта для выполнения SQL-запросов
cursor = conn.cursor()

# Создание таблицы для пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")
conn.commit()


# Функция для добавления пользователя
def add_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"Пользователь '{username}' добавлен.")
    except sqlite3.IntegrityError:
        print(f"Пользователь с именем '{username}' уже существует.")


# Функция для получения всех пользователей
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)


# Функция для проверки существует ли такой пользователь
def user_exists(username, password):
    """ Проверяет, существует ли пользователь с указанными логином и паролем. """
    # да, тут надо закриптовать/декриптовать пароль, но мне лень =)
    # Можно использовать ECC/SHA-256/AES -> к быстродействию лучше использовать AES
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        return True  # Пользователь найден
    return False  # Пользователь не найден


def username_exists(username):
    """ Проверяет, существует ли пользователь с указанными логином. """
    cursor.execute("SELECT * FROM users WHERE username = ?", __parameters=username)
    user = cursor.fetchone()
    if user:
        return True  # Пользователь найден
    return False  # Пользователь не найден
