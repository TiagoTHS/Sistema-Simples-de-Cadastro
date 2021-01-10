from PyQt5 import uic,QtWidgets
import mysql.connector

#Banco de dados utilizado para o sistema
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

#Função para o botão 'Enviar', que guarda os dados recebidos do formulario em um banco de dados
def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    categoria = ""

    if formulario.radioButton.isChecked() :
        categoria = "Informatica"
        formulario.radioButton.setCheckable(False)
    elif formulario.radioButton_2.isChecked() :
        categoria = "Alimentos"
        formulario.radioButton_2.setCheckable(False)
    elif formulario.radioButton_3.isChecked() :
        formulario.radioButton_3.setCheckable(False)
        categoria = "Eletronicos"
    else:
        categoria = "Nao Especificada"

    cursor = banco.cursor()
    comando_SQL = "insert into produtos (codigo, descricao, preco, categoria) values (%s, %s, %s, %s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()

    print("Codigo: ", linha1)
    print("Descricao: ", linha2)
    print("Preco: ", linha3)
    print(f"Categoria {categoria} Selecionada")

    #Limpa o que esta escrito no formulario para um novo cadastro
    formulario.lineEdit.clear()
    formulario.lineEdit_2.clear()
    formulario.lineEdit_3.clear()

#Função para o botão 'Listar', que abre uma nova janela com a listagem dos produtos
def funcao_listar():
    listagem.show()
        
#carrega os arquivos de interface do sistema
app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
listagem=uic.loadUi("listagem.ui")
#chama a funçao para o botão 'Enviar'
formulario.pushButton.clicked.connect(funcao_principal)

#chama a funçao para o botão 'Listar'
formulario.pushButton_2.clicked.connect(funcao_listar)

formulario.show()
app.exec()