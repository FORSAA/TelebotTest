from Telebot_Main.functions.Classes.Connection import *
from Telebot_Main.functions.Classes.User_Pattern import *


class UserData_repo():
    def __init__(self):
        self._connection = getConnection()
        self.cursor = self._connection.cursor()

    def SelectAll(self):
        result = self.cursor.execute('exec SelectUslessInfo').fetchall()
        return result

    def SelectUslessInfo(self):
        result = self.cursor.execute('exec SelectUslessInfo').fetchall()
        return result

    def SelectByTelegram_Id(self, User_id: int):
        result = self.cursor.execute(f"exec SelectByTelegram_Id '{User_id}'").fetchone()
        return result

    def AddUser(self, User):
        self.cursor.execute(f"exec AddUser '{User.login}', '{User.password}', {User.telegram_id}").commit()

    def DeleteUser(self, User):
        self.cursor.execute(f'exec DeleteUser {User.telegram_id}')

    def EditUser(self, User):
        self.cursor.execute(f"exec EditUser '{User.login}', '{User.password}', {User.telegram_id}").commit()
