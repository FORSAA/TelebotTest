import pyodbc

class ConnectionOption:
    def __init__(self):
        self.connection_string = 'DRIVER={SQL Server};SERVER=.;DATABASE=telebot_db;TRUSTED_CONNECTION=TRUE;'

def getConnection():
    Option = ConnectionOption()
    connection = pyodbc.connect(Option.connection_string, timeout=100)
    return connection