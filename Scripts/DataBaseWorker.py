import sqlite3

class DataWorker:
    def __init__(self):
        self.DataBase = sqlite3.connect(r"C:\Панель Инстрементов\Python progects\WildPickles_DiscordBot\Resources\DataBase.db")
        self.Cursor = self.DataBase.cursor()
    
    def MakeRequest(self, request):
        self.Cursor.execute(request)
        return self.Cursor.fetchall()