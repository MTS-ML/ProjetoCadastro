import tkinter as tk
from tkinter import font
import re
import sqlite3


def criando_banco():
    # CRIANDO O BANCO DE DADOS (usei somente na primeira vez para criar).
    # OBS: SELECIONAR O QUE QUISER E 'ctrl + /' comenta tudo)
    conexao_bd = sqlite3.connect(
        'banco_clientes.db')  # PARA CONECTAR AO BANCO DE DADOS, SE NÃO EXISTIR, ELE CRIA E CONECTA.
    cursor = conexao_bd.cursor()  # CRIA O CURSOR, CHAMADO TAMBÉM DE MENSAGEIRO, PARA FAZER DETERMINADA AÇÃO.

    #  CRIANDO A TABELA NO BANCO DE DADOS
    # OBS: NÃO PODE USAR '-', SE NÃO DA ERRO
    cursor.execute('''CREATE TABLE clientes (
        Nome text,
        CPF text,
        Email text,
        Senha text
        )
    ''')

    # COMO SE FOSSE UM "TEM CERTEZA?" É O COMMIT.
    conexao_bd.commit()
    conexao_bd.close()
# criando_banco()  # EXECUTAR SOMENTE 1 VEZ PARA CRIAR O BANCO


def cadastrar_cliente(entry_nome, entry_cpf, entry_email, entry_senha, ):
    conexao_bd = sqlite3.connect('banco_clientes.db')
    try:
        cursor = conexao_bd.cursor()

        # CRIANDO A TABELA NO BANCO DE DADOS
        cursor.execute("INSERT INTO clientes VALUES (?, ?, ?, ?)",  # ESSES ':' SIGNIFICA CRIAÇÃO DE VARIÁVEL TEMPORÁRIA
                       (  # ISSO É UM DICIONÁRIO
                           entry_nome.get(),
                           entry_cpf.get(),
                           entry_email.get(),
                           entry_senha.get()
                       )
                       )
        #  COMO SE FOSSE UM "TEM CERTEZA?" É O COMMIT.
        conexao_bd.commit()
    finally:
        conexao_bd.close()

        # PARA APAGAR OS VALORES APÓS CADASTRAR O CLIENTE
        entry_nome.delete(0, 'end')
        entry_cpf.delete(0, 'end')
        entry_email.delete(0, 'end')
        entry_senha.delete(0, 'end')


def menu():
    # CRIANDO INTERFACE
    janela = tk.Tk()
    janela.title('MENU')

    largura_janela = 250
    altura_janela = 250
    janela.geometry(f"{largura_janela}x{altura_janela}")

    # Frame para centralizar os elementos // USA O FRAME E O PACK AO INVÉS DO 'janela' E GRID
    janela_principal = tk.Frame(janela)
    janela_principal.pack(expand=True)

    # LABEL
    fonte = font.Font(weight='bold', underline=True)
    titulo2_label = tk.Label(janela_principal, text='MENU', font=fonte)
    titulo2_label.pack(pady=10)

    # BOTÕES DO MENU
    botao_cadastrar = tk.Button(janela_principal, text='CADASTRAR USUÁRIO', command=interface_cadastro)
    botao_cadastrar.pack(pady=10)  # MEXE NO EIXO Y (VERTICALMENTE)

    botao_login = tk.Button(janela_principal, text='LOGIN', command=interface_login)
    botao_login.pack(pady=10)

    botao_sair = tk.Button(janela_principal, text='SAIR', command=janela.destroy)
    botao_sair.pack(pady=10)

    janela.mainloop()


def campo_nome(janela_cadastro):
    label_nome = tk.Label(janela_cadastro, text='Nome completo:')  # janela_cadastro é o nome da nova janela criada
    label_nome.pack(pady=5)
    entry_nome = tk.Entry(janela_cadastro, width=40)
    entry_nome.pack(pady=(0, 5))
    erro_nome = tk.Label(janela_cadastro, text='', fg='red')
    erro_nome.pack(pady=5)
    return entry_nome, erro_nome


#   VALIDAÇÃO DO NOME
def validar_nome(entry_nome, erro_nome):
    nome = entry_nome.get().strip()
    padrao = r'^[A-Z][a-z]*([ ][A-Z][a-z]*)+$'
    if re.match(padrao, nome):
        erro_nome.config(text='Nome válido', fg='green')  # Se passar a validação, remove a mensagem de erro
        return True
    else:
        erro_nome.config(text='Digite seu nome completo.', fg='red')  # Se não passar validação, exibe mensagem de erro
        return False


def campo_cpf(janela_cadastro):
    label_cpf = tk.Label(janela_cadastro, text='CPF: ')
    label_cpf.pack(pady=5)
    entry_cpf = tk.Entry(janela_cadastro, width=40)
    entry_cpf.pack(pady=2)
    erro_cpf = tk.Label(janela_cadastro, text='', fg='red')
    erro_cpf.pack(pady=2)
    return entry_cpf, erro_cpf


#                                   VALIDAÇÃO DO CPF
def validar_cpf(entry_cpf, erro_cpf):
    cpf = entry_cpf.get().replace('-', '').replace('.', '').strip()

    conexao_bd = sqlite3.connect('banco_clientes.db')
    cursor = conexao_bd.cursor()

    cursor.execute("SELECT COUNT(*) FROM clientes WHERE CPF = ?", (cpf,))
    resultado = cursor.fetchone()
    quantidade_cpf = resultado[0]

    if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0] * 11:  # ÚLTIMA VERIFICAÇÃO É PARA NÃO TER NÚMEROS IGUAIS APENAS
        erro_cpf.config(text='Digite os 11 números do seu CPF.', fg='red')
        return False
    elif quantidade_cpf != 0:
        erro_cpf.config(text='CPF já cadastrado', fg='red')
        return False
    elif validar_digitos_cpf(cpf):
        erro_cpf.config(text='CPF válido', fg='green')
        return True
    else:
        erro_cpf.config(text='Número de CPF inválido', fg='red')
        return False


def validar_digitos_cpf(cpf):
    # Verifica o primeiro dígito verificador
    seq = 10
    total = 0
    for num in cpf[:9]:
        total += int(num) * seq
        seq -= 1
    resto = total % 11
    digito_verificador_1 = 0 if resto < 2 else 11 - resto

    # Verifica o segundo dígito verificador
    seq = 11
    total = 0
    for num in cpf[:10]:
        total += int(num) * seq
        seq -= 1
    resto = total % 11
    digito_verificador_2 = 0 if resto < 2 else 11 - resto

    # Verifica se os dígitos verificadores estão corretos
    if digito_verificador_1 == int(cpf[9]) and digito_verificador_2 == int(cpf[10]):
        return True
    else:
        return False


def campo_email(janela_cadastro):
    label_email = tk.Label(janela_cadastro, text='E-mail: ')
    label_email.pack(pady=5)
    entry_email = tk.Entry(janela_cadastro, width=40)
    entry_email.pack(pady=5)
    erro_email = tk.Label(janela_cadastro, text='', fg='red')
    erro_email.pack(pady=5)
    return entry_email, erro_email


def validar_email(entry_email, erro_email):
    email = entry_email.get().strip().lower()
    if email == '':
        erro_email.config(text='E-mail não pode ficar em branco', fg='red')
        return True
    if '@' not in email or not email.endswith('.com'):
        erro_email.config(text='Endereço de e-mail não é válido', fg='red')
        return False
    else:
        erro_email.config(text='Endereço de e-mail válido!', fg='green')
        return True


def campo_senha(janela_cadastro):
    label_senha = tk.Label(janela_cadastro, text='Senha: ')
    label_senha.pack(pady=5)
    entry_senha = tk.Entry(janela_cadastro, width=40)
    entry_senha.pack(pady=5)
    erro_senha = tk.Label(janela_cadastro, text='', fg='red')
    erro_senha.pack(pady=5)
    return entry_senha, erro_senha


def validar_senha(entry_senha, erro_senha, entry_cpf):
    senha = entry_senha.get().strip()
    if senha == '':
        erro_senha.config(text='Senha não pode ficar em branco', fg='red')
        return False
    if senha == entry_cpf.get():  # DEMOREI BASTANTE PARA DESCOBRIR ESSE, ESTAVA COLOCANDO TUDO MENOS 'entry_login.GET()'.
        erro_senha.config(text='CPF e senha não podem ser iguais', fg='red')
        return False
    if not any(char.isupper() for char in senha):
        erro_senha.config(text='Necessário 1 letra maiúscula', fg='red')
        return False
    if not any(char.isdigit() for char in senha):
        erro_senha.config(text='Necessário 1 número', fg='red')
        return False
    if ' ' in senha:
        erro_senha.config(text='Não é permitido espaços', fg='red')
        return False
    else:
        erro_senha.config(text='Senha válida', fg='green')
        return True


def validar_campos(entry_nome, erro_nome, entry_cpf, erro_cpf,
                   entry_email, erro_email, entry_senha, erro_senha,
                   label_botao_cadastrar, segunda_janela):
    nome_valido = validar_nome(entry_nome, erro_nome)
    cpf_valido = validar_cpf(entry_cpf, erro_cpf)
    email_valido = validar_email(entry_email, erro_email)
    senha_valida = validar_senha(entry_senha, erro_senha, entry_cpf)

    # VALIDAÇÕES
    if nome_valido and cpf_valido and email_valido and senha_valida:
        label_botao_cadastrar.config(text='Cadastro realizado com sucesso!', fg='green')
        cadastrar_cliente(entry_nome, entry_cpf, entry_email, entry_senha)
        segunda_janela.after(2000, segunda_janela.destroy)
    else:
        label_botao_cadastrar.config(text='Preencha os campos corretamente', fg='red')


def criar_botao_cadastrar(janela_cadastro, entry_nome, erro_nome, entry_cpf, erro_cpf,
                          entry_email, erro_email, entry_senha, erro_senha, label_botao_cadastrar, segunda_janela):

    # Botão para confirmar o cadastro
    # Lambda funciona como uma função anônima. Não poderia colocar somente a função validar_campos e passar os parametros no command,
    # seria necessário criar outra função separada e passar ela sem parametros, nessa função separada, estaria a função
    # validar_campos com seus parametros. Então, usando o lambda funciona como um atalho, podendo chamar a função diretamente.
    botao_cadastrar = tk.Button(janela_cadastro, text='Cadastrar', command=lambda: validar_campos(
        entry_nome, erro_nome, entry_cpf, erro_cpf, entry_email, erro_email, entry_senha, erro_senha, label_botao_cadastrar, segunda_janela))
    botao_cadastrar.pack(pady=5)


def interface_cadastro():
    # Função para a interface de cadastro
    segunda_janela = tk.Toplevel()  # Cria uma nova janela para o cadastro
    segunda_janela.title('CADASTRO DE USUÁRIO')

    largura_janela = 350
    altura_janela = 450
    segunda_janela.geometry(f"{largura_janela}x{altura_janela}")

    #     Frame para organizar os elementos
    janela_cadastro = tk.Frame(segunda_janela)
    janela_cadastro.pack(expand=True)

    # ORDEM DE EXIBIÇÃO NA TELA
    entry_nome, erro_nome = campo_nome(janela_cadastro)
    entry_cpf, erro_cpf = campo_cpf(janela_cadastro)
    entry_email, erro_email = campo_email(janela_cadastro)
    entry_senha, erro_senha = campo_senha(janela_cadastro)

    label_botao_cadastrar = tk.Label(janela_cadastro, text='', fg='red')
    criar_botao_cadastrar(janela_cadastro, entry_nome, erro_nome, entry_cpf, erro_cpf,
                          entry_email, erro_email, entry_senha, erro_senha, label_botao_cadastrar, segunda_janela)
    label_botao_cadastrar.pack(pady=5)


#                     JANELA DO LOGIN
def campo_login(janela_login):
    label_login = tk.Label(janela_login, text='Login: (CPF ou Email)')
    label_login.pack(pady=5)
    entry_login = tk.Entry(janela_login, width=40)
    entry_login.pack(pady=5)

    erro_login = tk.Label(janela_login, text='', fg='red')
    erro_login.pack(pady=5)
    return entry_login, erro_login


def senha_para_login(janela_login):
    label_senha = tk.Label(janela_login, text='Senha: ')
    label_senha.pack(pady=5)
    entry_senha = tk.Entry(janela_login, width=40)
    entry_senha.pack(pady=5)
    erro_senha = tk.Label(janela_login, text='', fg='red')
    erro_senha.pack(pady=5)
    return entry_senha, erro_senha


# VERIFICA SE O LOGIN E SENHA ESTÃO CADASTRADOS NO BD
def validar_login_senha(entry_login, erro_login, entry_senha, erro_senha, janela_login, terceira_janela):
    login = entry_login.get().strip()
    senha = entry_senha.get().strip()

    if login == '':
        erro_login.config(text='Login está em branco', fg='red')
    if senha == '':
        erro_senha.config(text='Senha está em branco', fg='red')

    conexao_bd = sqlite3.connect('banco_clientes.db')
    cursor = conexao_bd.cursor()

    # Verifica se o login (CPF ou email) está cadastrado na tabela de clientes
    cursor.execute("SELECT CPF, Email, Senha FROM clientes WHERE CPF = ? OR Email = ?", (login, login))
    resultado = cursor.fetchone()  # Retorna a primeira linha encontrada com CPF ou Email

    if resultado:
        cpf_cliente, email_cliente, senha_cliente = resultado

        if (login == cpf_cliente or login == email_cliente) and senha == senha_cliente:
            label_realizar_login = tk.Label(janela_login, text='Login realizado com sucesso', fg='green')
            label_realizar_login.pack(pady=5)
            terceira_janela.after(2000, terceira_janela.destroy)

        if login == cpf_cliente or login == email_cliente:
            erro_login.config(text='Login válido', fg='green')

            if senha == '':
                erro_senha.config(text='Senha está em branco!', fg='red')
            elif senha != senha_cliente:
                erro_senha.config(text='Senha incorreta!', fg='red')
            else:
                erro_senha.config(text='Senha válida!', fg='green')
    else:
        erro_login.config(text='Login não cadastrado', fg='red')
        entry_login.delete(0, 'end')  # Limpa o campo de login
        entry_senha.delete(0, 'end')  # Limpa o campo de senha

    conexao_bd.close()


def criar_botao_login(janela_login, entry_login, erro_login, entry_senha, erro_senha, terceira_janela):
    botao_login = tk.Button(janela_login, text='Relizar Login', command=lambda: validar_login_senha(
        entry_login, erro_login, entry_senha, erro_senha, janela_login, terceira_janela))
    botao_login.pack(pady=5)


def interface_login():
    terceira_janela = tk.Toplevel()
    terceira_janela.title('LOGIN')

    largura_janela = 300
    altura_janela = 285
    terceira_janela.geometry(f'{largura_janela}x{altura_janela}')

    janela_login = tk.Frame(terceira_janela)
    janela_login.pack(expand=True)

    # ORDEM DE EXIBIÇÃO NA TELA
    entry_login, erro_login = campo_login(janela_login)
    entry_senha, erro_senha = senha_para_login(janela_login)

    criar_botao_login(janela_login, entry_login, erro_login, entry_senha, erro_senha, terceira_janela)
    label_criar_login = tk.Label(janela_login, text='', fg='green')
    label_criar_login.pack(pady=5)


# Chamar a função principal para iniciar a interface
menu()
