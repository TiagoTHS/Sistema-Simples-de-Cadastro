from PyQt5 import uic,QtWidgets
from funcoes import botoes
import mysql.connector


#carrega os arquivos de interface do sistema
app=QtWidgets.QApplication([])


''' Tela de Cadastro

    Nesta tela é exibido um formulário que, se preenchido corretamente, ao clicar em Enviar
    é feita uma conexão com o banco de dados e inserida as informações do formulario na table 'produtos'.

    - Carrega a UI desta tela com 'loadUi'
    - Realiza a conexão de funções para os botões presentes nesta tela
    
 '''
tela_cadastro=uic.loadUi(r"ui\cadastro.ui")
#chama a funçao para o botão 'Enviar'
tela_cadastro.pushButton.clicked.connect(lambda : botoes.funcao_enviar(tela_cadastro))
#chama a funçao para o botão 'Voltar'
tela_cadastro.pushButton_2.clicked.connect(lambda : tela_cadastro.close())



''' Tela de Listagem

    Nesta tela é feita uma busca no banco de dados, na table 'produtos', para que seja apresentado ao usuário
    os produtos já cadastrados.

    É oferecido ao Usuário as opções de criar um pdf com os dados, 
    e também de excluir algum produto ao selecionar a linha desejada.

    - Carrega a UI desta tela com 'loadUi'
    - Realiza a conexão de funções para os botões presentes nesta tela
    
 '''
listagem=uic.loadUi(r"ui\listagem.ui")
#chama a funçao para o botão 'PDF'
listagem.pushButton.clicked.connect(lambda : botoes.funcao_pdf(aviso_pdf))
#chama a funçao para o botão 'Excluir'
listagem.pushButton_2.clicked.connect(lambda : botoes.funcao_excluir_dado(listagem))
#chama a funçao para o botão 'Voltar'
listagem.pushButton_3.clicked.connect(lambda : listagem.close())



''' Tela de Menu

    É a principal tela que leva para as demais opções disponíveis no sistema (Vender, Cadastrar, Listar).

    - Carrega a UI desta tela com 'loadUi'
    - Realiza a conexão de funções para os botões presentes nesta tela
    
 '''
menu=uic.loadUi(r"ui\segunda_tela.ui")
#chama a funçao para o botão 'Cadastrar'
menu.pushButton.clicked.connect(lambda : tela_cadastro.show())
#chama a funçao para o botão 'Listar'
menu.pushButton_2.clicked.connect(lambda : botoes.funcao_listar(listagem))
#chama a funçao para o botão 'Vender'
menu.pushButton_3.clicked.connect(lambda : botoes.funcao_vender(tela_venda))
#chama a funçao para o botão 'Sair'
menu.pushButton_4.clicked.connect(lambda : menu.close())



''' Tela de Login

    Tela clássica de Login para o usuário.

    - Carrega a UI desta tela com 'loadUi'
    - Realiza a conexão de funções para os botões presentes nesta tela
    
 '''
tela_login=uic.loadUi(r"ui\login.ui")
#chama a funçao para o botão 'Login' 
tela_login.pushButton.clicked.connect(lambda : botoes.funcao_login(tela_login, menu))



''' Tela de Venda

    Nesta tela é exibido um formulário que, se preenchido corretamente, ao clicar em Finalizar
    é feita uma conexão com o banco de dados e inserida as informações do formulario na table 'vendas'.
    
    Para ajudar na hora de completar os dados, há um botão Completar que com a entrada de apenas
    (Descrição e Quantidade) ou (Código e Quantidade), os espaços (Código/Descrição) e Valor Total são completados automaticamente,
    além de uma ajuda com 'autocomplete' ao se optar por digitar a Descrição.

    - Carrega a UI desta tela com 'loadUi'
    - Realiza a conexão de funções para os botões presentes nesta tela
    
 '''
tela_venda=uic.loadUi(r"ui\window_venda.ui")
#chama a funçao para o botão 'Completar'
tela_venda.pushButton.clicked.connect(lambda : botoes.funcao_completar(tela_venda))
#chama a funçao para o botão 'Finalizar'
tela_venda.pushButton_2.clicked.connect(lambda : botoes.funcao_finalizar(tela_venda, pos_venda))



aviso_pdf=uic.loadUi(r"ui\warning_pdf.ui")
pos_venda=uic.loadUi(r"ui\pos_venda.ui")


tela_login.show()
app.exec()