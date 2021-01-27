from PyQt5 import QtWidgets
from reportlab.pdfgen import canvas
from database.conexaoDB import ConexaoMySQL

banco = ConexaoMySQL()

# Função para o botão 'Login'
# Como parametros, a propria tela de login para salvar informações digitadas, e também a proxima tela que deve aparecer
def funcao_login(tela, proxTela):
    user = str(tela.lineEdit.text())
    senha = str(tela.lineEdit_2.text())

    if user == 'Tiago' and senha == '123':
        proxTela.show()
        tela.close()
    else:
        tela.label_4.setText("Usuário ou senha incorretos!")



# Função para o botão 'Enviar', que guarda os dados recebidos do formulario em um banco de dados
# Como parametro, a propria tela de cadastro para salvar informações digitadas
def funcao_enviar(tela):
    linha1 = tela.lineEdit.text()
    linha2 = tela.lineEdit_2.text()
    linha3 = tela.lineEdit_3.text()
    linha4 = tela.lineEdit_4.text()
    categoria = ""

    if tela.radioButton.isChecked() :
        categoria = "Informatica"
    elif tela.radioButton_2.isChecked() :
        categoria = "Alimentos"
    elif tela.radioButton_3.isChecked() :
        categoria = "Eletronicos"
    else:
        categoria = "Nao Especificada"

    if linha1 and linha2 and linha3 and linha4:
        try :
            cursor = banco.cursor()
            comando_SQL = "insert into produtos (codigo, descricao, preco, quantidade, categoria) values (%s, %s, %s, %s, %s)"
            dados = (str(linha1), str(linha2), str(linha3), str(linha4), categoria)
            cursor.execute(comando_SQL, dados)
            banco.commit()

            print("Codigo: ", linha1)
            print("Descricao: ", linha2)
            print("Preco: ", linha3)
            print("Quantidade: ", linha4)
            print(f"Categoria {categoria} Selecionada")
        except :
            print("Erro ao cadastrar o produto / Ja ha um produto com esse codigo")
    else:
        print("Adicione infos!")

    #Limpa o que esta escrito no formulario para um novo cadastro
    tela.lineEdit.setText("")
    tela.lineEdit_2.setText("")
    tela.lineEdit_3.setText("")
    tela.lineEdit_4.setText("")



# Função para o botão 'Atualizar', que atualiza os dados recebidos do formulario no banco de dados
# Como parametro, a propria tela de atualização para salvar informações digitadas
def funcao_att(tela):
    cod = tela.lineEdit.text()
    desc = tela.lineEdit_2.text()
    preco = tela.lineEdit_3.text()
    quant = tela.lineEdit_4.text()

    cursor = banco.cursor()
    if desc:
        cursor.execute("update produtos set descricao = '{}' where codigo = '{}'".format(desc, cod))
    if preco:
        cursor.execute("update produtos set preco = '{}' where codigo = '{}'".format(preco, cod))
    if quant:
        cursor.execute("update produtos set quantidade = '{}' where codigo = '{}'".format(quant, cod))

    banco.commit()



# Função para o botão 'Listar Produtos', que abre uma nova janela com a listagem dos produtos
# Como parametro, a tela de listagem a ser mostrada
def funcao_listarProd(proxTela):

    proxTela.show()

    try:
        cursor = banco.cursor()
        comando_SQL = "select * from produtos"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()

        d = lambda dado: dado[2]
        dados_lidos.sort(key=d)

        proxTela.tableWidget.setRowCount(len(dados_lidos))
        proxTela.tableWidget.setColumnCount(5)

        # proxTela.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Código"))
        # proxTela.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Descrição"))
        # proxTela.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Preço"))
        # proxTela.tableWidget.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Categoria"))

        for i in range(0, len(dados_lidos)):
            proxTela.tableWidget.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(str(dados_lidos[i][0])))
            for j in range(0, 5):
                proxTela.tableWidget.setItem(i, j ,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j+1])))
    except:
        print("Erro ao listar os produtos / Nao ha produtos a serem listados")



# Função para o botão 'Listar Vendas', que abre uma nova janela com a listagem das Vendas
# Como parametro, a tela de listagem a ser mostrada
def funcao_listarVenda(proxTela):

    proxTela.show()

    try:
        cursor = banco.cursor()
        comando_SQL = "select * from vendas"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()

        proxTela.tableWidget.setRowCount(len(dados_lidos))
        proxTela.tableWidget.setColumnCount(5)

        # proxTela.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Código"))
        # proxTela.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Descrição"))
        # proxTela.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Preço"))
        # proxTela.tableWidget.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Categoria"))

        for i in range(0, len(dados_lidos)):
            proxTela.tableWidget.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(str(dados_lidos[i][0])))
            for j in range(0, 5):
                proxTela.tableWidget.setItem(i, j ,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j+1])))
    except:
        print("Erro ao listar as vendas / Nao ha vendas a serem listadas")



# Função que gera um pdf com os valores contidos no banco de dados
# Unico parametro é a tela de aviso apos a criação o PDF
def funcao_pdf (aviso):
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
    aviso.show()
    print("PDF salvo com sucesso")



# Função para o botão 'Excluir linha selecionada'
# Como parametro, a tela de listagem para receber as informações para excluir
def funcao_excluir_dado(tela) :
    linha_selecionada = tela.tableWidget.currentRow()
    tela.tableWidget.removeRow(linha_selecionada)

    cursor = banco.cursor()
    cursor.execute("select id from produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha_selecionada][0] 
    cursor.execute("delete from produtos where id ="+ str(valor_id))
    banco.close()



# Função para o botão 'Vender'
# Como parametro a tela de venda a ser mostrada
# Criação de um completer para auxiliar na escrita da descrição
def funcao_vender(proxTela):
    
    proxTela.lineEdit.setText("")
    proxTela.lineEdit_2.setText("")
    proxTela.lineEdit_3.setText("")
    proxTela.lineEdit_4.setText("")
    proxTela.lineEdit_5.setText("")
    
    proxTela.show()

    cursor = banco.cursor()
    cursor.execute("select descricao from produtos")
    desc = cursor.fetchall()
    lista_desc = []
    for i in range(len(desc)):
        lista_desc.append(desc[i][0])

    completer = QtWidgets.QCompleter(lista_desc)
    proxTela.lineEdit_4.setCompleter(completer)



# Função para o botão 'Completar'
# Como parametro a tela de venda para ser completada com demais infos
def funcao_completar(tela):

    cursor = banco.cursor()
    
    cod = tela.lineEdit_2.text()
    descri = str(tela.lineEdit_4.text())
    quant = tela.lineEdit_3.text()

    if descri :
        tela.lineEdit_2.setText("")
        cursor.execute("select codigo from produtos where descricao ='{}'".format(descri))
        codig = cursor.fetchall()
        tela.lineEdit_2.setText(str(codig[0][0]))
        if quant :
            cursor.execute("select preco from produtos where descricao ='{}'".format(descri))
            valor_un = cursor.fetchall()
            valor_total = ((valor_un[0][0]) * float(quant))
            tela.lineEdit_5.setText(str(valor_total))
    elif cod :
        cursor.execute("select descricao from produtos where codigo ="+ str(cod))
        desc = cursor.fetchall()
        tela.lineEdit_4.setText(str(desc[0][0]))
        if quant :
            cursor.execute("select preco from produtos where codigo ="+ str(cod))
            valor_un = cursor.fetchall()
            valor_total = ((valor_un[0][0]) * float(quant))
            tela.lineEdit_5.setText(str(valor_total))



# Função para o botão 'Finalizar'
# Como parametro a tela de venda para salvar informações, e a tela de pós venda
def funcao_finalizar(tela, proxTela):

    nome = tela.lineEdit.text()
    cod = tela.lineEdit_2.text()
    desc = tela.lineEdit_4.text()
    quant = float(tela.lineEdit_3.text())
    total = tela.lineEdit_5.text()

    cursor = banco.cursor()
    cursor.execute("select quantidade from produtos where codigo = '{}'".format(cod))
    quant_inicial = cursor.fetchall()
    quant_final = quant_inicial[0][0] - quant
    cursor.execute("update produtos set quantidade = {} where codigo = '{}'".format(quant_final, cod))
    
    comando_SQL = "insert into vendas (cliente, codigo, descricao, quantidade, valortotal) values (%s, %s, %s, %s, %s)"
    dados = (str(nome), str(cod), str(desc), str(quant), str(total))
    cursor.execute(comando_SQL, dados)
    banco.commit()

    proxTela.show()