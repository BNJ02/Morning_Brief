# init_db.py
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sqlite.db')
SQL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'init_db.sql')

def initialize_database(sql_file):
    try:
        # Connexion à la base de données (elle sera créée si elle n'existe pas)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Lire le fichier SQL
        with open(sql_file, 'r') as f:
            sql_script = f.read()

        # Exécuter le script SQL
        cursor.executescript(sql_script)

        # Sauvegarder les modifications et fermer la connexion
        conn.commit()
        conn.close()
        print(f"Database initialized successfully using {sql_file}")

    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    # Initialiser la base de données en exécutant le fichier SQL
    initialize_database(SQL_PATH)
