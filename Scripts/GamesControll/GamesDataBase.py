import sqlite3
from GamesControll.GamesData import GameData

class DataWorker:
    def __init__(self):
        self.DataBase = sqlite3.connect(r"C:\Панель Инструментов\Python\WildPickles_DiscordBot\Resources\DataBase.db")
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