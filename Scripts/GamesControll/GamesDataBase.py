import sqlite3
from os import path
from GamesControll.GamesData import GameData


class DataWorker:
    def __init__(self):
        parent_dir = path.dirname(path.abspath(__file__))
        data_base_path = "/".join(parent_dir.split('\\')[:-2]) + "/Resources/DataBase.db"

        self.DataBase = sqlite3.connect(data_base_path)
        self.Cursor = self.DataBase.cursor()
    
    def SetInfo(self, name, role_id, category_id):
        self.Cursor.execute("INSERT INTO GAMES VALUES (?, ?, ?)", (name, role_id, category_id))
        self.DataBase.commit()
    
    def GetInfo(self, name):
        game_info = self.Cursor.execute("SELECT * FROM GAMES WHERE NAME=?",
          (name,)).fetchone()

        self.DataBase.commit()
        return GameData(game_info[0], game_info[1], game_info[2])
    
    def DeleteInfo(self, name):
        self.Cursor.execute("DELETE FROM GAMES WHERE NAME=?", (name,))
        self.DataBase.commit()