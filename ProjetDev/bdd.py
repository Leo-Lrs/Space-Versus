import sqlite3

from pygame.cursors import Cursor

class Bdd():
    def __init__(self):
        self.connexion = sqlite3.connect("basededonnees.db")
        with self.connexion:
            curseur = self.connexion.cursor()

            curseur.execute('''CREATE TABLE IF NOT EXISTS scores(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                Pseudo TEXT,
                Valeur INTEGER
            )''')

            curseur.execute('''CREATE TABLE IF NOT EXISTS player1(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                Pseudo TEXT,
                Velocity FLOAT,
                Angle_speed FLOAT,
                Attack FLOAT,
                Health INT

            )''')

            curseur.execute('''CREATE TABLE IF NOT EXISTS player2(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                Pseudo TEXT,
                Velocity FLOAT,
                Angle_speed FLOAT,
                Attack FLOAT,
                Health INT

            )''')
            self.connexion.commit()
            curseur.close()

    def fake_info(self):
        with self.connexion:
            curseur = self.connexion.cursor()
            try:
                curseur.executescript("""    
                    INSERT INTO scores(Pseudo, Valeur) VALUES ("toto", 1000);
                    INSERT INTO scores(Pseudo, Valeur) VALUES ("tata", 750);
                    INSERT INTO scores(Pseudo, Valeur) VALUES ("titi", 500)
                """)
                self.connexion.commit()
                curseur.close()
            except sqlite3.Error as e:
                print (e)

    def hall_of_fame(self, max):
        with self.connexion:
            curseur = self.connexion.cursor()
            req = curseur.execute(f"""
                SELECT Pseudo, Valeur FROM scores
                ORDER BY valeur DESC
                LIMIT {max};        
            """)
            req = curseur.fetchall()
            self.connexion.commit()
            curseur.close()
            return req
    
    def insert_data_player(self, table, player):
        try:
            with self.connexion:
                curseur = self.connexion.cursor()
                curseur.execute(f"""
                    INSERT INTO {table}(id, Pseudo, Velocity, Angle_speed, Attack, Health) 
                    VALUES ("1", "{player.pseudo}", {player.velocity}, {player.angle_speed}, {player.attack}, {player.health})
                
                """)
                self.connexion.commit()
                curseur.close()
        except sqlite3.Error as e:
            print ("Déjà créé", e)

    def select_data_player(self, table, data):
        with self.connexion:
            curseur = self.connexion.cursor()
            req = curseur.execute(f"""
                SELECT {data} FROM {table}
            """)
            req = curseur.fetchone()
            curseur.close()
            return req

    def select_update_data_player(self, table, case):
        with self.connexion:
            curseur = self.connexion.cursor()
            case_origin = self.connexion.execute(f"""
                SELECT {case} 
                FROM {table};
            """)
            selected_value = case_origin.fetchone()
            selected_value = selected_value[0]
            self.connexion.commit()
            curseur.close()
            return selected_value
    
    def update_data_player(self, table, case, valeur):
        with self.connexion:
            curseur = self.connexion.cursor()
            updated_value = self.select_update_data_player(table, case) + valeur
            self.connexion.execute(f"""            
                UPDATE {table}
                SET {case} = {updated_value}
                WHERE id = 1
            """)
            self.connexion.commit()
            curseur.close()

    def update_name_player(self, table, valeur):
        with self.connexion:
            curseur = self.connexion.cursor()
            self.connexion.execute(f"""            
                UPDATE {table}
                SET Pseudo = "{valeur}"
                WHERE id = 1
            """)
            self.connexion.commit()
            curseur.close()

    def update_score(self, winner, score):
        with self.connexion:
            curseur = self.connexion.cursor()
            curseur.execute(f"""    
                    INSERT INTO scores(Pseudo, Valeur) VALUES ("{winner}", {score})
                """)
            self.connexion.commit()
            curseur.close()

