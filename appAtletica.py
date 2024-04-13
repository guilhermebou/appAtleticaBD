import psycopg2
from psycopg2 import sql
import PySimpleGUI as sg


def insert_data():
    layout_insert = [
        [sg.Text('Nome:'), sg.InputText(key='nome')],
        [sg.Button('Inserir'), sg.Button('Cancelar')]
    ]
    window_insert = sg.Window('Inserir Dados').Layout(layout_insert)

    while True:
        event, values = window_insert.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Inserir':
            nome = values['nome']
            try:
                cursor.execute("INSERT INTO Funcionario (nome) VALUES (%s)", (nome,))
                connect.commit()
                sg.popup('Dados inseridos com sucesso!')
            except psycopg2.Error as e:
                sg.popup(e)

    window_insert.close()

def delete_data():
    layout_delete = [
        [sg.Text('ID do Funcionario a ser deletado:'), sg.InputText(key='id')],
        [sg.Button('Deletar'), sg.Button('Cancelar')]
    ]
    window_delete = sg.Window('Deletar Dados').Layout(layout_delete)

    while True:
        event, values = window_delete.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Deletar':
            funcionario_id = values['id']
            try:
                cursor.execute("DELETE FROM Funcionario WHERE id = %s", (funcionario_id,))
                connect.commit()
                sg.popup('Dados deletados com sucesso!')
            except psycopg2.Error as e:
                sg.popup(e)

    window_delete.close()

def update_data():
    layout_update = [
        [sg.Text('ID do jogador a ser atualizado:'), sg.InputText(key='id')],
        [sg.Text('Atualizar o Nome do jogador para:'), sg.InputText(key='nome')],
        [sg.Button('Atualizar'), sg.Button('Cancelar')]
    ]
    window_update = sg.Window('Atualizar Dados').Layout(layout_update)

    while True:
        event, values = window_update.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Atualizar':
            funcionario_id = values['id']
            nome = values['nome']
            try:
                cursor.execute("UPDATE funcionario SET nome = %s WHERE funcionario.id = %s", (nome, funcionario_id))
                connect.commit()
                sg.popup('Dados atualizados com sucesso!')
            except psycopg2.Error as e:
                sg.popup(e)

    window_update.close()

def retrieve_data():
    try:
        cursor.execute("SELECT * FROM Funcionario")
    except psycopg2.ProgrammingError as e:
            sg.popup('Você não tem permissão para consultar.')

    funcionarios = cursor.fetchall()
    layout_retrieve = [
        [sg.Text('Funcionario cadastrados:')],
        [sg.Output(size=(30,20))]
    ]

    sg.popup(funcionarios)

def create_user():
    layout_create = [
        [sg.Text('Usuario:'),sg.InputText(key='user')],
        [sg.Text('Senha:'),sg.InputText('', password_char='*',key='pw')],
        [sg.Checkbox('SELECT',key= 'select'),sg.Checkbox('INSERT',key= 'insert'),sg.Checkbox('UPDATE',key= 'update'),sg.Checkbox('DELETE',key= 'delete')],
        [sg.Button('Criar'),sg.Button('Cancelar')],
    ]
    window_create_user = sg.Window('Criação Usuario').Layout(layout_create)

    while True:
        event, values = window_create_user.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Criar':
            user = values['user']
            pw = values['pw']
            create_user_query = sql.SQL("CREATE ROLE {} LOGIN PASSWORD %s;").format(sql.Identifier(user))
            try:
                cursor.execute(create_user_query, (pw,))
                #connect.commit()

                perm_select = values['select']
                perm_insert = values['insert']
                perm_update = values['update']
                perm_delete = values['delete']

                if not (perm_select or perm_insert or perm_update or perm_delete):
                    sg.popup('Pelo menos uma permissão deve ser dada!')
                    continue

                perms = []

                if perm_select:
                    perms.append("SELECT")
                if perm_insert:
                    perms.append("INSERT")
                if perm_update:
                    perms.append("UPDATE")
                if perm_delete:
                    perms.append("DELETE")

                #GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO seu_usuario;
                if perms:

                    grant_permissions_query = f"GRANT {', '.join(perms)} ON ALL TABLES IN SCHEMA public TO {user};"
                    cursor.execute(grant_permissions_query)

                    grant_permissions_query = f"GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO {user};"
                    cursor.execute(grant_permissions_query)
                    connect.commit()
                sg.popup('Usuario criado com sucesso!')
            except psycopg2.Error as e:
                sg.popup(e)

    window_create_user.close()

def menu():
    layout_menu = [
        [sg.Button('Inserir')],
        [sg.Button('Deletar')],
        [sg.Button('Atualizar')],
        [sg.Button('Consultar')],
        [sg.Button('Criar Usuario')],
        [sg.Button('Sair')]
    ]

    window_menu = sg.Window('Menu',size=(600,200)).Layout(layout_menu)

    while True:
        event, values = window_menu.read()
        if event in (None, 'Sair'):
            break
        if event == 'Inserir':
            insert_data()
        elif event == 'Deletar':
            delete_data()
        elif event == 'Atualizar':
            update_data()
        elif event == 'Consultar':
            retrieve_data()
        elif event == 'Criar Usuario':
            create_user()

    window_menu.close()
    cursor.close()
    connect.close()


layout_login = [
    [sg.Text('Usuario:'),sg.InputText(key='user')],
    [sg.Text('Senha:'),sg.InputText('', password_char='*',key='pw')],
    [sg.Button('Logar')]
]

window_login = sg.Window('Login',size=(600,200)).Layout(layout_login)

while True:
    try:
        event, values = window_login.read()
        if event == 'Logar':
            user = values['user']
            pw = values['pw']

            connect = psycopg2.connect(database="pythonTest",
                        host= "localhost",
                        user= user,
                        password= pw,
                        port= "5432")
            cursor = connect.cursor()
            sg.popup('Login realizado com sucesso!')
            window_login.close()
            menu()
    except psycopg2.Error as e:
        sg.popup("Nome de usuário ou senha errados. Por favor tente outra vez.")


