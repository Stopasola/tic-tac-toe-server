from tkinter import *
from datetime import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
import threading
from tkinter import messagebox
from client import *
import time

global CabecalhoLista, tree, ValoresLista
global Input_Nome, Input_Porta, Input_IP, player_ocupy
player_ocupy = False
tree = None
count = 0

horario_e_data_atual = datetime.now()
data = horario_e_data_atual.strftime("%d/%m/%Y")
horario = horario_e_data_atual.strftime("%H:%M")


def refresh(ValoresLista):
    global count

    x = tree.get_children()
    for item in x:
        tree.delete(item)
    count = 0

    setup_widgets(ValoresLista)


def next_id():
    global count
    count += 1
    return "%.4d" % count


def setup_widgets(ValoresLista):
    for item in ValoresLista:
        tree.insert('', 'end', id=next_id(), values=item)
        for ix, val in enumerate(item):
            col_w = tkFont.Font().measure(val)
            if tree.column(CabecalhoLista[ix], width=None) < col_w:
                tree.column(CabecalhoLista[ix], width=col_w)


def onselect(evt):
    global tree, Input_Nome, Input_Porta, Input_IP, player_ocupy
    selected = []
    selected = evt.widget.selection()

    for idx in selected:
        selected_user = tree.item(idx)['values']

    print(selected_user)
    user_option = messagebox.askyesno('Solicitação de Jogo',
                                      'Você deseja se conectar com o usuário: ' + str(selected_user[0]))

    if user_option and player_ocupy == False:
        #comunication_server(Input_IP.get(), int(Input_Porta.get()), 'EXIT')  # saio servidor UDP
        player_ocupy = True
        if not connection_client_TCP(Input_Nome.get(), str(selected_user[1]),
                                     selected_user[2]):  # Func de inicialização TCP
            messagebox.showinfo('Problemas ao Logar', 'O usuário não quis logar!!')

    if player_ocupy:
        messagebox.showinfo('Jogador Ocupado', 'O jogador já está em uma partida!!')


def Func_Lista_Clientes():
    global CabecalhoLista, tree

    style = ttk.Style()
    column_size = 60
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, rowheight=30,
                    font=('Calibri', 11))  # fonte ValoresLista
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 20, 'bold'))  # fonte CabecalhoLista
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

    List_Widget = Frame(janela)

    CabecalhoLista = ['  Nome  ', '  IP  ', '  Porta  ']

    lbListaClientes = Label(List_Widget, text="Lista Clientes:", font=FonteTitulo)
    lbListaClientes.grid(row=0, column=0, padx=1, pady=0, sticky=W)

    List_Widget.grid(row=0, column=1, padx=100, pady=0)  # Ajustar a posição do meu Container

    tree = ttk.Treeview(columns=CabecalhoLista, show="headings", style='mystyle.Treeview')
    vsb = ttk.Scrollbar(orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.grid(column=0, row=1, sticky='nsew', in_=List_Widget)
    vsb.grid(column=1, row=1, sticky='ns', in_=List_Widget)
    List_Widget.grid_columnconfigure(0, weight=1)
    List_Widget.grid_rowconfigure(0, weight=1)

    for col in CabecalhoLista:
        tree.heading(col, text=col.title())
        # adjust the column's width to the header string
        tree.column(col, width=(tkFont.Font().measure(col.title())) + column_size, anchor="center")

    tree.bind('<<TreeviewSelect>>', onselect)


def List_Players_On(UDP_IP_ADDRESS, UDP_PORT_NO):
    # A cada 5 segundos atualizo a lista caso a mesma tenha mudado
    List_Values = list()
    now = int(time.time())
    future = now

    while int(time.time()) <= future:

        if int(time.time()) == future:
            # envia comando list para o server, e recebe uma lista com os usuarios
            server_list = comunication_server(UDP_IP_ADDRESS, UDP_PORT_NO, 'LIST')

            for i in range(1, len(server_list)):
                info = str(server_list[i])
                info = info.split(':')
                List_Values.append(info[:])

            print('List_Values', List_Values)
            refresh(List_Values)
            List_Values.clear()
            future = int(time.time()) + 5


def Connect_User(Input_Nome, Input_Porta, Input_IP):
    pass_login = login_server(Input_IP.get(), int(Input_Porta.get()), Input_Nome.get())

    if pass_login == False:
        messagebox.showinfo('Problemas ao Logar', 'A Porta ou IP informados estão incorretos')
        Input_IP.delete(0, END)
        Input_Porta.delete(0, END)
        Input_Nome.delete(0, END)
    else:  # Caso o usuario consiga logar com sucesso, é exibida a lista de usuarios onlines no server
        Func_Lista_Clientes()

        thread = threading.Thread(target=List_Players_On, args=(Input_IP.get(), int(Input_Porta.get())))
        thread.start()

        thread1 = threading.Thread(target=listen_client_TCP_connection)  # escuta conexões tcp
        thread1.start()


def Info_Player():
    global Input_Nome, Input_Porta, Input_IP

    Player = Frame(janela, highlightbackground="black", highlightcolor="black", highlightthickness=3)
    lbNome = Label(Player, text="Nome:", font=FonteTitulo)
    Input_Nome = ttk.Entry(Player)
    lbAddPorta = Label(Player, text="Porta:", font=FonteTitulo)
    Input_Porta = ttk.Entry(Player)
    lbAdd_IP = Label(Player, text="IP:", font=FonteTitulo)
    Input_IP = ttk.Entry(Player)
    btn_Insere_Info = ttk.Button(Player, text="Inserir",
                                 command=lambda: Connect_User(Input_Nome, Input_Porta, Input_IP))

    lbNome.grid(row=0, column=0, padx=10, pady=10, sticky=W)
    Input_Nome.grid(row=0, column=1, padx=25, pady=25, sticky=W)
    lbAddPorta.grid(row=1, column=0, padx=10, pady=10, sticky=W)
    Input_Porta.grid(row=1, column=1, padx=25, pady=25, sticky=W)
    lbAdd_IP.grid(row=2, column=0, padx=10, pady=10, sticky=W)
    Input_IP.grid(row=2, column=1, padx=25, pady=25, sticky=W)
    btn_Insere_Info.grid(row=3, column=0, padx=10, pady=10, sticky=W)

    Player.grid(row=0, column=0, padx=10, pady=10, sticky=NW)  # Pos Container


"""##################################### Configurações Iniciais ########################################"""

janela = Tk()

janela.title("Tela Inicial")
FonteTitulo = ("Verdana", "17")
FonteTexto = ("Verdana", "8")

""" Funções """

Info_Player()

janela.geometry("800x600")
janela.mainloop()
