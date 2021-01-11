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



#Função para o botão 'Enviar', que guarda os dados recebidos do formulario em um banco de dados
def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    categoria = ""

    if formulario.radioButton.isChecked() :
        categoria = "Informatica"
    elif formulario.radioButton_2.isChecked() :
        categoria = "Alimentos"
    elif formulario.radioButton_3.isChecked() :
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
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")



#Função para o botão 'Listar', que abre uma nova janela com a listagem dos produtos
def funcao_listar():
    listagem.show()

    cursor = banco.cursor()
    comando_SQL = "select * from produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

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


#carrega os arquivos de interface do sistema
app=QtWidgets.QApplication([])
formulario=uic.loadUi("ui\principal.ui")
listagem=uic.loadUi("ui\listagem.ui")
aviso_pdf=uic.loadUi("ui\warning_pdf.ui")

#chama a funçao para o botão 'Enviar'
formulario.pushButton.clicked.connect(funcao_principal)

#chama a funçao para o botão 'Listar'
formulario.pushButton_2.clicked.connect(funcao_listar)

#chama a funçao para o botão 'PDF'
listagem.pushButton.clicked.connect(funcao_pdf)

#chama a funçao para o botão 'Excluir'
listagem.pushButton_2.clicked.connect(funcao_excluir_dado)

formulario.show()
app.exec()