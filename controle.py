from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

#Banco de dados utilizado para o sistema
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

def funcao_login():
    user = str(tela_login.lineEdit.text())
    senha = str(tela_login.lineEdit_2.text())

    if user == 'Tiago' and senha == '123':
        menu.show()
        tela_login.close()
    else:
        tela_login.label_4.setText("Usuário ou senha incorretos!")

def funcao_cadastro():
    tela_cadastro.show()

def funcao_sair():
    menu.close()

def funcao_voltar():
    tela_cadastro.close()
    listagem.close()

#Função para o botão 'Enviar', que guarda os dados recebidos do formulario em um banco de dados
def funcao_enviar():
    linha1 = tela_cadastro.lineEdit.text()
    linha2 = tela_cadastro.lineEdit_2.text()
    linha3 = tela_cadastro.lineEdit_3.text()
    categoria = ""

    if tela_cadastro.radioButton.isChecked() :
        categoria = "Informatica"
    elif tela_cadastro.radioButton_2.isChecked() :
        categoria = "Alimentos"
    elif tela_cadastro.radioButton_3.isChecked() :
        categoria = "Eletronicos"
    else:
        categoria = "Nao Especificada"

    cursor = banco.cursor()
    comando_SQL = "insert into produtos (codigo, descricao, preco, categoria) values (%s, %s, %s, %s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()
    banco.close()

    print("Codigo: ", linha1)
    print("Descricao: ", linha2)
    print("Preco: ", linha3)
    print(f"Categoria {categoria} Selecionada")

    #Limpa o que esta escrito no formulario para um novo cadastro
    tela_cadastro.lineEdit.setText("")
    tela_cadastro.lineEdit_2.setText("")
    tela_cadastro.lineEdit_3.setText("")



#Função para o botão 'Listar', que abre uma nova janela com a listagem dos produtos
def funcao_listar():
    listagem.show()

    cursor = banco.cursor()
    comando_SQL = "select * from produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    banco.close()

    listagem.tableWidget.setRowCount(len(dados_lidos))
    listagem.tableWidget.setColumnCount(4)

    # listagem.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Código"))
    # listagem.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Descrição"))
    # listagem.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Preço"))
    # listagem.tableWidget.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Categoria"))

    for i in range(0, len(dados_lidos)):
        listagem.tableWidget.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(str(dados_lidos[i][0])))
        for j in range(0, 4):
            listagem.tableWidget.setItem(i, j ,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j+1])))
    

# Função que gera um pdf com os valores contidos no banco de dados
def funcao_pdf ():
    cursor = banco.cursor()
    comando_SQL = "select * from produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    banco.close()
    y = 0
    pdf = canvas.Canvas("produtos-cadastrados.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos Cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CODIGO")
    pdf.drawString(210, 750, "DESCRICAO")
    pdf.drawString(330, 750, "PRECO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range (0, len(dados_lidos)):
        y += 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(330, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

    pdf.save()
    aviso_pdf.show()
    print("PDF salvo com sucesso")



def funcao_excluir_dado() :
    linha_selecionada = listagem.tableWidget.currentRow()
    listagem.tableWidget.removeRow(linha_selecionada)

    cursor = banco.cursor()
    cursor.execute("select id from produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha_selecionada][0] 
    cursor.execute("delete from produtos where id ="+ str(valor_id))
    banco.close()

def funcao_vender():

    tela_venda.lineEdit.setText("")
    tela_venda.lineEdit_2.setText("")
    tela_venda.lineEdit_3.setText("")
    tela_venda.lineEdit_4.setText("")
    tela_venda.lineEdit_5.setText("")

    tela_venda.show()

    cursor = banco.cursor()
    cursor.execute("select descricao from produtos")
    desc = cursor.fetchall()
    lista_desc = []
    for i in range(len(desc)):
        lista_desc.append(desc[i][0])

    completer = QtWidgets.QCompleter(lista_desc)
    tela_venda.lineEdit_4.setCompleter(completer)

def funcao_completar():

    cursor = banco.cursor()
    
    cod = tela_venda.lineEdit_2.text()
    descri = str(tela_venda.lineEdit_4.text())
    quant = tela_venda.lineEdit_3.text()

    if descri :
        tela_venda.lineEdit_2.setText("")
        cursor.execute("select codigo from produtos where descricao ='{}'".format(descri))
        codig = cursor.fetchall()
        tela_venda.lineEdit_2.setText(str(codig[0][0]))
        if quant :
            cursor.execute("select preco from produtos where descricao ='{}'".format(descri))
            valor_un = cursor.fetchall()
            valor_total = ((valor_un[0][0]) * float(quant))
            tela_venda.lineEdit_5.setText(str(valor_total))
    elif cod :
        cursor.execute("select descricao from produtos where codigo ="+ str(cod))
        desc = cursor.fetchall()
        tela_venda.lineEdit_4.setText(str(desc[0][0]))
        if quant :
            cursor.execute("select preco from produtos where codigo ="+ str(cod))
            valor_un = cursor.fetchall()
            valor_total = ((valor_un[0][0]) * float(quant))
            tela_venda.lineEdit_5.setText(str(valor_total))

#carrega os arquivos de interface do sistema
app=QtWidgets.QApplication([])
tela_cadastro=uic.loadUi("ui\cadastro.ui")
listagem=uic.loadUi("ui\listagem.ui")
aviso_pdf=uic.loadUi("ui\warning_pdf.ui")
tela_login=uic.loadUi("ui\login.ui")
menu=uic.loadUi("ui\segunda_tela.ui")
tela_venda=uic.loadUi("ui\window_venda.ui")

#chama a funçao para o botão 'Login' 
tela_login.pushButton.clicked.connect(funcao_login)

#chama a funçao para o botão 'Enviar'
tela_cadastro.pushButton.clicked.connect(funcao_enviar)

#chama a funçao para o botão 'Voltar'
tela_cadastro.pushButton_2.clicked.connect(funcao_voltar)

#chama a funçao para o botão 'Cadastrar'
menu.pushButton.clicked.connect(funcao_cadastro)

#chama a funçao para o botão 'Listar'
menu.pushButton_2.clicked.connect(funcao_listar)

#chama a funçao para o botão 'Vender'
menu.pushButton_3.clicked.connect(funcao_vender)

#chama a funçao para o botão 'Sair'
menu.pushButton_4.clicked.connect(funcao_sair)

#chama a funçao para o botão 'PDF'
listagem.pushButton.clicked.connect(funcao_pdf)

#chama a funçao para o botão 'Excluir'
listagem.pushButton_2.clicked.connect(funcao_excluir_dado)

#chama a funçao para o botão 'Voltar'
listagem.pushButton_3.clicked.connect(funcao_voltar)

#chama a funçao para o botão 'Completar'
tela_venda.pushButton.clicked.connect(funcao_completar)

tela_login.show()
app.exec()