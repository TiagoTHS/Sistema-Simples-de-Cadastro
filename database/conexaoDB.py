import mysql.connector

#Banco de dados utilizado para o sistema
def ConexaoMySQL ():
    banco = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="loja_demo"
    )
    
    return banco