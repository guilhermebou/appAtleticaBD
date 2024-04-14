import psycopg2
from psycopg2 import sql
import PySimpleGUI as sg
from io import BytesIO
from PIL import Image
import datetime
import tempfile
import os
from PyPDF2 import PdfReader

def select_imagem():
    layout_select_img = [
        [sg.Text('ID da imagem de consulta:'), sg.InputText(key='id')],
        [sg.Button('SELECT'), sg.Button('Cancelar')]
    ]

    window_img = sg.Window('Consulta IMG ', layout=layout_select_img)

    while True:
        event, values = window_img.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'SELECT':
            id = values['id']
            try:
                imagem_data = retrieve_image_from_db(id)

                if imagem_data:

                    temp_image_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                    with open(temp_image_path, 'wb') as temp_image:
                        temp_image.write(imagem_data)

                    layout = [
                        [sg.Image(filename=temp_image_path)],
                        [sg.Button('Fechar')]
                    ]

                    window = sg.Window('Imagem do Banco de Dados', layout)

                    while True:
                        event, values = window.read()
                        if event == sg.WINDOW_CLOSED or event == 'Fechar':
                            window.close()
                            break
                else:
                    sg.popup('Nenhuma imagem encontrada com o ID fornecido')

            except psycopg2.Error as e:
                sg.popup(e)

    window_img.close()

def retrieve_image_from_db(image_id):
    try:
        cursor.execute("SELECT imagem FROM imagens WHERE id = %s", (image_id,))
        image_data = cursor.fetchone()
        if image_data:
            return image_data[0]
        else:
            print("Nenhuma imagem encontrada com o ID fornecido")
            return None
    except psycopg2.Error as e:
        print("Erro ao recuperar imagem:", e)
        return None

def insert_user():
    layout_insert = [
        [sg.Text('Nome:'), sg.InputText(key='nome')],
        [sg.Text("Data de Nascimento (YYYY-MM-DD):"),sg.InputText(key='dt_nasc'),],
        [sg.Text('Selecione o sexo:')],
        [sg.Radio('Masculino','SEX',key='M'), sg.Radio('Feminino','SEX',key='F')],
        [sg.Text('Insira Foto do Usuario:')],
        [sg.InputText(key='FILE'), sg.FileBrowse()],
        [sg.Button('Inserir'),sg.Button('Cancelar')]
    ]

    window_insert = sg.Window('Inserir Dados').Layout(layout_insert)

    while True:
        event, values = window_insert.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Inserir':
            nome = values['nome']
            dt_nasc = values['dt_nasc']

            imagem_path = values['FILE']

            if imagem_path == '':
                imagem_bytes = None
            else:
                with open(imagem_path, 'rb') as f:
                    imagem_bytes = psycopg2.Binary(f.read())

            if values['M']:
                sexo = 'M'
            else:
                sexo = 'F'
            try:
                cursor.execute("INSERT INTO Usuario (nome,dt_nascimento,sexo,foto_perfil) VALUES (%s,%s,%s,%s)", (nome,dt_nasc,sexo,imagem_bytes))
                connect.commit()
                sg.popup('Dados inseridos com sucesso!')
            except psycopg2.Error as e:
                connect.rollback()
                sg.popup('ERRO: ', e)
    window_insert.close()

def delete_user():
    layout_delete = [
        [sg.Text('ID do Usuario a ser deletado:'), sg.InputText(key='id')],
        [sg.Button('Deletar'), sg.Button('Cancelar')]
    ]
    window_delete = sg.Window('Deletar Dados').Layout(layout_delete)

    while True:
        event, values = window_delete.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Deletar':
            usuario_id = values['id']
            try:
                cursor.execute("DELETE FROM Usuario WHERE id = %s", (usuario_id,))
                connect.commit()
                sg.popup('Dados deletados com sucesso!')
            except psycopg2.Error as e:
                connect.rollback()
                sg.popup(e)

    window_delete.close()

def update_user():
    layout_update = [
        [sg.Text('ID do Usuario a ser atualizado:'), sg.InputText(key='id')],
        [sg.Text('Nome:'), sg.InputText(key='nome')],
        [sg.Text("Data de Nascimento (YYYY-MM-DD):"), sg.InputText(key='dt_nasc')],
        [sg.Text('Selecione o sexo:')],
        [sg.Radio('Masculino', 'SEX', key='M'), sg.Radio('Feminino', 'SEX', key='F')],
        [sg.Text('Insira Foto do Usuario:')],
        [sg.InputText(key='FILE'), sg.FileBrowse()],
        [sg.Button('Atualizar'), sg.Button('Cancelar')]
    ]
    window_update = sg.Window('Atualizar Dados').Layout(layout_update)

    while True:
        event, values = window_update.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Atualizar':
            user_id = values['id']

            update_query_parts = []
            update_values = []

            if 'nome' in values and values['nome']:
                update_query_parts.append("nome = %s")
                update_values.append(values['nome'])
            if 'dt_nasc' in values and values['dt_nasc']:
                update_query_parts.append("dt_nascimento = %s")
                update_values.append(values['dt_nasc'])
            if 'M' in values and values['M']:
                update_query_parts.append("sexo = 'M'")
            elif 'F' in values and values['F']:
                update_query_parts.append("sexo = 'F'")
            if 'FILE' in values and values['FILE']:
                imagem_path = values['FILE']
                with open(imagem_path, 'rb') as f:
                    imagem_bytes = f.read()
                update_query_parts.append("foto_perfil = %s")
                update_values.append(psycopg2.Binary(imagem_bytes))

            try:
                set_clause = ", ".join(update_query_parts)

                sql_query = f"UPDATE Usuario SET {set_clause} WHERE Usuario.id = %s"
                update_values.append(user_id)

                cursor.execute(sql_query, tuple(update_values))
                connect.commit()
                sg.popup('Dados atualizados com sucesso!')
            except psycopg2.Error as e:
                connect.rollback()
                sg.popup(e)

    window_update.close()

def resize_image(image_path, target_size=(100, 100)):
    img = Image.open(image_path)
    img.thumbnail(target_size)
    img.save(image_path)

def select_user():

    layout_user = [
        [sg.Text('ID do Usuario:'), sg.InputText(key='id_user'), sg.Button('Buscar', bind_return_key=True), sg.Button('Cancelar')],
        [sg.Column(layout=[
            [sg.Text('Nome:', size=(17, 1)), sg.Text(size=(20, 1), key='-Nome-')],
            [sg.Text('Data de Nascimento:', size=(17, 1)), sg.Text(size=(20, 1), key='-DataNascimento-')],
            [sg.Text('Sexo:', size=(17, 1)), sg.Text(size=(20, 1), key='-Sexo-')]
        ]), sg.Column(layout=[
            [sg.Image(key='-FotoPerfil-', size=(100, 100), pad=(0, 0))]
        ])]
    ]


    sg.theme('LightGrey1')
    sg.set_options(font=('Helvetica', 12), element_padding=(5, 5))


    window_select_user = sg.Window('Buscar Usuário', layout=layout_user)

    while True:
        event, values = window_select_user.read()

        if event in (sg.WINDOW_CLOSED, 'Cancelar'):
            break
        elif event == 'Buscar':
            user_id = values['id_user']
            try:
                cursor.execute("SELECT * FROM Usuario WHERE id = %s", (user_id,))
                usuario = cursor.fetchone()
                if usuario:
                    window_select_user['-Nome-'].update(usuario[1])
                    window_select_user['-DataNascimento-'].update(str(usuario[2]))
                    window_select_user['-Sexo-'].update(usuario[3])


                    foto_perfil = usuario[4]
                    if foto_perfil:

                        try:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
                                temp_image_path = temp_image.name
                                temp_image.write(foto_perfil)
                        except Exception as e:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
                                temp_image_path = temp_image.name
                                temp_image.write(foto_perfil)

                        resize_image(temp_image_path)


                        if os.path.exists(temp_image_path):
                            window_select_user['-FotoPerfil-'].update(filename=temp_image_path)
                        else:
                            window_select_user['-FotoPerfil-'].update(filename='')
                    else:
                        window_select_user['-FotoPerfil-'].update(filename='')

                else:
                    sg.popup('Nenhum usuário encontrado com o ID fornecido.')
            except psycopg2.Error as e:
                connect.rollback()
                sg.popup(e)
            except Exception as e:
                sg.popup(e)

    window_select_user.close()

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
                connect.rollback()
                sg.popup(e)

    window_create_user.close()

def menu_user():

    layout_crud_user = [
        [sg.Button('Select', size=(10, 2), button_color=('white', '#3498db'), border_width=3),
         sg.Button('Insert', size=(10, 2), button_color=('white', '#2ecc71'), border_width=3)],
        [sg.Button('Update', size=(10, 2), button_color=('white', '#f39c12'), border_width=3),
         sg.Button('Delete', size=(10, 2), button_color=('white', '#e74c3c'), border_width=3)],
        [sg.Button('Listar Todos', size=(20, 2), button_color=('white', '#9b59b6'), border_width=3)],
        [sg.Button('Sair', size=(10, 2), button_color=('white', '#95a5a6'), border_width=3)]
    ]


    sg.theme('LightGrey1')
    sg.set_options(font=('Helvetica', 12), element_padding=(5, 5))


    window_menu = sg.Window('CRUD Usuario', layout=layout_crud_user, size=(400, 300), finalize=True)

    while True:
        event, values = window_menu.read()

        if event in (None, 'Sair'):
            break
        elif event == 'Select':
            select_user()
        elif event == 'Insert':
            insert_user()
        elif event == 'Update':
            update_user()
        elif event == 'Delete':
            delete_user()
        elif event == 'Listar Todos':
            list_all_users()

    window_menu.close()

def list_all_users():
    try:
        cursor.execute("SELECT id, nome, dt_nascimento, sexo FROM Usuario")
        usuarios = cursor.fetchall()
        if usuarios:
            result_str = ''
            for usuario in usuarios:
                result_str += f'ID: {usuario[0]}, Nome: {usuario[1]}, Data Nascimento: {usuario[2]}, Sexo: {usuario[3]}\n'
            sg.popup_scrolled(result_str, title='Todos os Usuários', size=(50, 20))
        else:
            sg.popup('Nenhum usuário encontrado.')
    except psycopg2.Error as e:
        connect.rollback()
        sg.popup(e)

def view_pdf_from_bytes(pdf_bytes):
    try:

        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_pdf.write(pdf_bytes)
        temp_pdf.close()


        with open(temp_pdf.name, 'rb') as file:
            reader = PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            sg.popup_scrolled(text)


        os.unlink(temp_pdf.name)
    except Exception as e:
        sg.popup(f"Erro ao abrir o PDF: {e}")

def select_vendas():
    layout_vendas = [
        [sg.Text('ID do Usuario:'), sg.InputText(key='id_user')],
        [sg.Text('ID do Produto:'), sg.InputText(key='id_prod')],
        [sg.Button('Buscar'), sg.Button('Cancelar')]
    ]
    window_select_vendas = sg.Window('Buscar vendas').Layout(layout_vendas)

    while True:
        event, values = window_select_vendas.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Buscar':
            user_id = values['id_user']
            user_prod = values['id_prod']
            try:
                cursor.execute("""
                    SELECT U.nome, P.nome, VP.quantidade, VP.valor_total, VP.data_venda, VP.comprovante_venda
                    FROM VENDAPRODUTO VP
                    INNER JOIN USUARIO U ON VP.usuario_id = U.id
                    INNER JOIN PRODUTO P ON P.id = VP.produto_id
                    WHERE VP.usuario_id = %s AND VP.produto_id = %s
                """, (user_id, user_prod))

                vendas = cursor.fetchall()
                if vendas:
                    for venda in vendas:
                        layout_venda = [
                            [sg.Text(f'Usuário: {venda[0]}')],
                            [sg.Text(f'Produto: {venda[1]}')],
                            [sg.Text(f'Quantidade: {venda[2]}')],
                            [sg.Text(f'Valor Total: {venda[3]}')],
                            [sg.Text(f'Data: {venda[4]}')],
                            [sg.Button('Visualizar Comprovante', key=venda[5])]
                        ]
                        window_venda = sg.Window('Detalhes da Venda').Layout(layout_venda)

                        while True:
                            event, values = window_venda.read()
                            if event in (None, 'Cancelar'):
                                break
                            elif event == venda[5]:

                                try:
                                    comprovante = venda[5].tobytes()
                                    sg.popup_scrolled(comprovante.decode('utf-8'))
                                except Exception as e:
                                    comprovante_bytes = venda[5]
                                    view_pdf_from_bytes(comprovante_bytes)

                        window_venda.close()
                else:
                    sg.popup('Nenhuma venda encontrada para os IDs fornecidos.')
            except psycopg2.Error as e:
                connect.rollback()
                sg.popup(e)

    window_select_vendas.close()

def insert_vendas():
    layout_insert = [
        [sg.Text('ID do Produto:'), sg.InputText(key='id_prod')],
        [sg.Text('ID do Usuario:'), sg.InputText(key='id_user')],
        [sg.Text('Quantidade:'),sg.InputText(key='quant'),sg.Text('Valor:'),sg.InputText(key='valor')],
        [sg.Text('Insira o Comprovante da venda:')],
        [sg.InputText(key='FILE'), sg.FileBrowse()],
        [sg.Button('Inserir'),sg.Button('Cancelar')]
    ]

    window_insert = sg.Window('Inserir Dados').Layout(layout_insert)

    while True:
        event, values = window_insert.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Inserir':
            id_prod = values['id_prod']
            id_user = values['id_user']
            quant = values['quant']
            valor = values['valor']
            date = datetime.date.today()
            imagem_path = values['FILE']
            if imagem_path == '':
                imagem = None
            else:
                with open(imagem_path, 'rb') as f:
                    imagem = psycopg2.Binary(f.read())

            try:
                #INSERT INTO VendaProduto (produto_id, usuario_id, quantidade, valor_total, data_venda, comprovante_venda) VALUES (2, 2, 1, 150.00, '2024-04-12', NULL);
                cursor.execute("INSERT INTO VendaProduto (produto_id, usuario_id, quantidade, valor_total, data_venda, comprovante_venda) VALUES (%s,%s,%s,%s,%s,%s)", (id_prod,id_user,quant,valor,date,imagem))
                connect.commit()
                sg.popup('Dados inseridos com sucesso!')
            except psycopg2.Error as e:
                connect.rollback()
                sg.popup('ERRO: ', e)
    window_insert.close()

def update_vendas():
    layout_update = [
        [sg.Text('ID da VENDA:'), sg.InputText(key='id_venda')],
        [sg.Text('ID do Produto:'), sg.InputText(key='id_prod')],
        [sg.Text('ID do Usuario:'), sg.InputText(key='id_user')],
        [sg.Text('Quantidade:'),sg.InputText(key='quant'),sg.Text('Valor:'),sg.InputText(key='valor'),sg.Text('Data:'),sg.InputText(key='date')],
        [sg.Text('Insira o Comprovante da venda:')],
        [sg.InputText(key='FILE'), sg.FileBrowse()],
        [sg.Button('Atualizar'),sg.Button('Cancelar')]
    ]
    window_update = sg.Window('Atualizar Dados').Layout(layout_update)

    while True:
        event, values = window_update.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Atualizar':

            id_venda = values['id_venda']
            update_query_parts = []
            update_values = []

            if 'id_prod' in values and values['id_prod']:
                update_query_parts.append("produto_id = %s")
                update_values.append(values['id_prod'])
            if 'id_user' in values and values['id_user']:
                update_query_parts.append("usuario_id = %s")
                update_values.append(values['id_user'])
            if 'quant' in values and values['quant']:
                update_query_parts.append("quantidade = %s")
                update_values.append(values['quant'])
            if 'valor' in values and values['valor']:
                update_query_parts.append("valor_total = %s")
                update_values.append(values['valor'])
            if 'date' in values and values['date']:
                update_query_parts.append("data_venda = %s")
                update_values.append(values['date'])
            if 'FILE' in values and values['FILE']:
                imagem_path = values['FILE']
                with open(imagem_path, 'rb') as f:
                    imagem_bytes = f.read()
                update_query_parts.append("comprovante_venda = %s")
                update_values.append(psycopg2.Binary(imagem_bytes))
            try:
                set_clause = ", ".join(update_query_parts)

                sql_query = f"UPDATE VendaProduto SET {set_clause} WHERE VendaProduto.id = %s"
                update_values.append(id_venda)

                cursor.execute(sql_query, tuple(update_values))
                connect.commit()
                sg.popup('Dados atualizados com sucesso!')
            except psycopg2.Error as e:
                connect.rollback()
                sg.popup(e)

    window_update.close()

def delete_vendas():
    layout_delete = [
        [sg.Text('ID da venda a ser deletado:'), sg.InputText(key='id')],
        [sg.Button('Deletar'), sg.Button('Cancelar')]
    ]
    window_delete = sg.Window('Deletar Dados').Layout(layout_delete)

    while True:
        event, values = window_delete.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Deletar':
            venda_id = values['id']
            try:
                cursor.execute("DELETE FROM VendaProduto WHERE id = %s", (venda_id,))
                connect.commit()
                sg.popup('Dados deletados com sucesso!')
            except psycopg2.Error as e:
                connect.rollback()
                sg.popup(e)

    window_delete.close()


def menu_vendas():
    layout_crud_vendas = [
        [sg.Button('Select'),sg.Button('Insert')],
        [sg.Button('Update'),sg.Button('Delete')],
        [sg.Button('Sair')]
    ]

    window_menu = sg.Window('Menu',size=(600,200)).Layout(layout_crud_vendas)

    while True:
        event, values = window_menu.read()
        if event in (None, 'Sair'):
            break
        if event == 'Select':
            select_vendas()
        elif event == 'Insert':
            insert_vendas()
        elif event == 'Update':
            update_vendas()
        elif event == 'Delete':
            delete_vendas()

    window_menu.close()

def menu():
    layout_menu = [
        [sg.Button('CRUD Usuario', size=(20, 2), button_color=('white', '#2E86C1'), border_width=5, pad=(20, 10), key='-CRUDUsuario-'),
         sg.Button('CRUD Venda Produto', size=(20, 2), button_color=('white', '#27AE60'), border_width=5, pad=(20, 10), key='-CRUDVendaProduto-'),
         sg.Button('Criar Usuario', size=(20, 2), button_color=('white', '#F39C12'), border_width=5, pad=(20, 10), key='-CriarUsuario-')],
        [sg.Button('Sair', size=(10, 2), button_color=('white', '#C0392B'), border_width=5, pad=(20, 10), key='-Sair-')]
    ]

    sg.theme('LightGrey1')
    sg.set_options(font=('Helvetica', 12), element_padding=(5, 5))

    window_menu = sg.Window('Sistema Atlética', layout=layout_menu, size=(800, 200), finalize=True)

    while True:
        event, values = window_menu.read()

        if event in (sg.WINDOW_CLOSED, '-Sair-'):
            break
        elif event == '-CRUDUsuario-':
            menu_user()
        elif event == '-CRUDVendaProduto-':
            menu_vendas()
        elif event == '-CriarUsuario-':
            create_user()

    window_menu.close()
    cursor.close()
    connect.close()


layout_login = [
    [sg.Text('Usuario:', size=(10, 1)), sg.InputText(key='user', size=(20, 1))],
    [sg.Text('Senha:', size=(10, 1)), sg.InputText('', password_char='*', key='pw', size=(20, 1))],
    [sg.Button('Logar', size=(10, 1), button_color=('white', '#3498db'), border_width=3, pad=(10, 10)),
     sg.Button('Cancelar', size=(10, 1), button_color=('white', '#FF0000'), border_width=3, pad=(10, 10))]
]

sg.theme('LightGrey1')
sg.set_options(font=('Helvetica', 12), element_padding=(5, 5))

window_login = sg.Window('Login', layout=layout_login, size=(400, 150), finalize=True)

while True:
    try:
        event, values = window_login.read()
        if event in (sg.WINDOW_CLOSED, 'Cancelar'):
            break;

        if event == 'Logar':
            user = values['user']
            pw = values['pw']

            connect = psycopg2.connect(database="Moca",
                        host= "localhost",
                        user= user,
                        password= pw,
                        port= "5432")
            cursor = connect.cursor()
            sg.popup('Login realizado com sucesso!')
            window_login.close()
            menu()
    except psycopg2.Error as e:
        connect.rollback()
        sg.popup("Nome de usuário ou senha errados. Por favor tente outra vez.")
