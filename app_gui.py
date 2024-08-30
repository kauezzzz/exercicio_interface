# import tkinter as tk
# from tkinter import ttk, messagebox
# import os
# import json
# import sys
# from modelos.restaurante import Restaurante
# from modelos.avaliacao import Avaliacao

# class RestauranteApp(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title("Sistema de Gerenciamento de Restaurantes")
#         self.geometry("800x600")

#         # Definir o ícone da janela
#         if os.path.exists("restaurante.ico"):
#             self.iconbitmap("restaurante.ico")
#         else:
#             print("Arquivo de ícone 'restaurante.ico' não encontrado.")

#         # Configuração do estilo
#         self.style = ttk.Style()
#         self.style.theme_use("clam")

#         # Frame principal
#         self.main_frame = ttk.Frame(self)
#         self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

#         # Lista de restaurantes
#         self.tree = ttk.Treeview(self.main_frame, columns=("Nome", "Categoria", "Avaliação", "Status"), show="headings")
#         self.tree.heading("Nome", text="Nome")
#         self.tree.heading("Categoria", text="Categoria")
#         self.tree.heading("Avaliação", text="Avaliação")
#         self.tree.heading("Status", text="Status")
        
#         # Configuração das colunas para centralizar os dados
#         self.tree.column("Nome", anchor="w", width=200)
#         self.tree.column("Categoria", anchor="center", width=150)
#         self.tree.column("Avaliação", anchor="center", width=100)
#         self.tree.column("Status", anchor="center", width=100)
        
#         self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

#         # Frame para botões
#         self.button_frame = ttk.Frame(self.main_frame)
#         self.button_frame.pack(pady=10)

#         # Botões
#         ttk.Button(self.button_frame, text="Cadastrar Restaurante", command=self.cadastrar_restaurante).grid(row=0, column=0, padx=5)
#         ttk.Button(self.button_frame, text="Habilitar/Desabilitar", command=self.habilitar_restaurante).grid(row=0, column=1, padx=5)
#         ttk.Button(self.button_frame, text="Avaliar Restaurante", command=self.avaliar_restaurante).grid(row=0, column=2, padx=5)
#         ttk.Button(self.button_frame, text="Alterar Restaurante", command=self.alterar_restaurante).grid(row=0, column=3, padx=5)
#         ttk.Button(self.button_frame, text="Excluir Restaurante", command=self.excluir_restaurante).grid(row=0, column=4, padx=5)

#         # Carregar dados iniciais
#         self.carregar_dados()
#         self.atualizar_lista_restaurantes()

#     def get_data_dir(self):
#         """
#         Retorna o diretório onde os dados serão salvos.
#         Se o programa for um executável, usa o diretório do executável.
#         Caso contrário, usa o diretório do script.
#         """
#         if getattr(sys, 'frozen', False):
#             return os.path.dirname(sys.executable)
#         else:
#             return os.path.dirname(os.path.abspath(__file__))

#     def carregar_dados(self):
#         """
#         Carrega os dados dos restaurantes a partir do arquivo JSON.
#         Se o arquivo não existir, cria um novo arquivo vazio.
#         """
#         ARQUIVO_DADOS = os.path.join(self.get_data_dir(), 'dados_restaurantes.json')
#         try:
#             with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
#                 dados = json.load(arquivo)
#                 Restaurante.restaurantes.clear()
#                 for restaurante_dados in dados:
#                     restaurante = Restaurante(
#                         restaurante_dados['nome'],
#                         restaurante_dados['categoria']
#                     )
#                     restaurante._ativo = restaurante_dados['ativo']
#                     restaurante._avaliacao = [Avaliacao(**avaliacao) for avaliacao in restaurante_dados['avaliacao']]
#         except FileNotFoundError:
#             messagebox.showinfo("Informação", f"Arquivo de dados não encontrado. Criando um novo arquivo em {ARQUIVO_DADOS}")
#             self.salvar_dados()

#     def salvar_dados(self):
#         """
#         Salva os dados dos restaurantes no arquivo JSON.
#         """
#         ARQUIVO_DADOS = os.path.join(self.get_data_dir(), 'dados_restaurantes.json')
#         dados = []
#         for restaurante in Restaurante.restaurantes:
#             dados.append({
#                 'nome': restaurante._nome,
#                 'categoria': restaurante._categoria,
#                 'ativo': restaurante._ativo,
#                 'avaliacao': [avaliacao.__dict__() for avaliacao in restaurante._avaliacao]
#             })
#         with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
#             json.dump(dados, arquivo, indent=4, ensure_ascii=False)

#     def atualizar_lista_restaurantes(self):
#         """
#         Atualiza a lista de restaurantes exibida na interface gráfica.
#         """
#         for i in self.tree.get_children():
#             self.tree.delete(i)
#         for restaurante in Restaurante.restaurantes:
#             self.tree.insert("", "end", values=(restaurante._nome, restaurante._categoria, restaurante.media_avaliacoes, restaurante.ativo))

#     def cadastrar_restaurante(self):
#         """
#         Abre uma janela para cadastrar um novo restaurante.
#         """
#         def salvar():
#             nome = nome_entry.get()
#             categoria = categoria_entry.get()
#             if nome and categoria:
#                 novo_restaurante = Restaurante(nome, categoria)
#                 self.salvar_dados()
#                 self.atualizar_lista_restaurantes()
#                 top.destroy()
#                 messagebox.showinfo("Sucesso", f"Restaurante {nome} cadastrado com sucesso!")
#             else:
#                 messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

#         top = tk.Toplevel(self)
#         top.title("Cadastrar Restaurante")
#         top.geometry("300x200")
#         if os.path.exists("restaurante.ico"):
#             top.iconbitmap("restaurante.ico")
            
#         ttk.Label(top, text="Nome:").pack(pady=5)
#         nome_entry = ttk.Entry(top)
#         nome_entry.pack(pady=5)

#         ttk.Label(top, text="Categoria:").pack(pady=5)
#         categoria_entry = ttk.Entry(top)
#         categoria_entry.pack(pady=5)

#         ttk.Button(top, text="Salvar", command=salvar).pack(pady=10)

#     def habilitar_restaurante(self):
#         """
#         Habilita ou desabilita o restaurante selecionado.
#         """
#         selecionado = self.tree.selection()
#         if selecionado:
#             item = self.tree.item(selecionado)
#             nome_restaurante = item['values'][0]
#             for restaurante in Restaurante.restaurantes:
#                 if restaurante._nome == nome_restaurante:
#                     restaurante.alternar_estado()
#                     self.salvar_dados()
#                     self.atualizar_lista_restaurantes()
#                     messagebox.showinfo("Sucesso", f"Estado do restaurante {restaurante._nome} alterado para {restaurante.ativo}")
#                     return
#         else:
#             messagebox.showerror("Erro", "Por favor, selecione um restaurante.")

#     def avaliar_restaurante(self):
#         """
#         Abre uma janela para avaliar o restaurante selecionado.
#         """
#         selecionado = self.tree.selection()
#         if selecionado:
#             item = self.tree.item(selecionado)
#             nome_restaurante = item['values'][0]
            
#             def salvar_avaliacao():
#                 cliente = cliente_entry.get()
#                 nota = nota_entry.get()
#                 if cliente and nota:
#                     try:
#                         nota = float(nota)
#                         if 0 <= nota <= 10:
#                             for restaurante in Restaurante.restaurantes:
#                                 if restaurante._nome == nome_restaurante:
#                                     restaurante.receber_avaliacao(cliente, nota)
#                                     self.salvar_dados()
#                                     self.atualizar_lista_restaurantes()
#                                     top.destroy()
#                                     messagebox.showinfo("Sucesso", "Avaliação registrada com sucesso!")
#                                     return
#                         else:
#                             messagebox.showerror("Erro", "A nota deve estar entre 0 e 10.")
#                     except ValueError:
#                         messagebox.showerror("Erro", "Por favor, digite um número válido para a nota.")
#                 else:
#                     messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

#             top = tk.Toplevel(self)
#             top.title(f"Avaliar Restaurante: {nome_restaurante}")
#             top.geometry("300x200")
#             if os.path.exists("restaurante.ico"):
#                 top.iconbitmap("restaurante.ico")

#             ttk.Label(top, text="Nome do Cliente:").pack(pady=5)
#             cliente_entry = ttk.Entry(top)
#             cliente_entry.pack(pady=5)

#             ttk.Label(top, text="Nota (0-10):").pack(pady=5)
#             nota_entry = ttk.Entry(top)
#             nota_entry.pack(pady=5)

#             ttk.Button(top, text="Salvar Avaliação", command=salvar_avaliacao).pack(pady=10)
#         else:
#             messagebox.showerror("Erro", "Por favor, selecione um restaurante.")

#     def alterar_restaurante(self):
#         """
#         Abre uma janela para alterar as informações do restaurante selecionado.
#         """
#         selecionado = self.tree.selection()
#         if selecionado:
#             item = self.tree.item(selecionado)
#             nome_restaurante = item['values'][0]
            
#             def salvar_alteracoes():
#                 novo_nome = novo_nome_entry.get()
#                 nova_categoria = nova_categoria_entry.get()
#                 if novo_nome or nova_categoria:
#                     for restaurante in Restaurante.restaurantes:
#                         if restaurante._nome == nome_restaurante:
#                             if novo_nome:
#                                 restaurante._nome = novo_nome.title()
#                             if nova_categoria:
#                                 restaurante._categoria = nova_categoria.upper()
#                             self.salvar_dados()
#                             self.atualizar_lista_restaurantes()
#                             top.destroy()
#                             messagebox.showinfo("Sucesso", f"Restaurante alterado com sucesso para: {restaurante}")
#                             return
#                 else:
#                     messagebox.showerror("Erro", "Por favor, preencha pelo menos um campo para alterar.")

#             top = tk.Toplevel(self)
#             top.title(f"Alterar Restaurante: {nome_restaurante}")
#             top.geometry("300x200")
#             if os.path.exists("restaurante.ico"):
#                 top.iconbitmap("restaurante.ico")

#             ttk.Label(top, text="Novo Nome:").pack(pady=5)
#             novo_nome_entry = ttk.Entry(top)
#             novo_nome_entry.pack(pady=5)

#             ttk.Label(top, text="Nova Categoria:").pack(pady=5)
#             nova_categoria_entry = ttk.Entry(top)
#             nova_categoria_entry.pack(pady=5)

#             ttk.Button(top, text="Salvar Alterações", command=salvar_alteracoes).pack(pady=10)
#         else:
#             messagebox.showerror("Erro", "Por favor, selecione um restaurante.")

#     def excluir_restaurante(self):
#         """
#         Exclui o restaurante selecionado após confirmação do usuário.
#         """
#         selecionado = self.tree.selection()
#         if selecionado:
#             item = self.tree.item(selecionado)
#             nome_restaurante = item['values'][0]
#             confirmacao = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o restaurante '{nome_restaurante}'?")
#             if confirmacao:
#                 for restaurante in Restaurante.restaurantes:
#                     if restaurante._nome == nome_restaurante:
#                         Restaurante.restaurantes.remove(restaurante)
#                         self.salvar_dados()
#                         self.atualizar_lista_restaurantes()
#                         messagebox.showinfo("Sucesso", f"Restaurante '{nome_restaurante}' excluído com sucesso.")
#                         return
#         else:
#             messagebox.showerror("Erro", "Por favor, selecione um restaurante.")

# if __name__ == '__main__':
#     app = RestauranteApp()
#     app.mainloop()

import customtkinter as ctk
import os
import json
import sys
from modelos.restaurante import Restaurante
from modelos.avaliacao import Avaliacao
from customtkinter import CTkMessagebox

class RestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.title("Sistema de Gerenciamento de Restaurantes")
        self.geometry("800x600")
        ctk.set_appearance_mode("light")  # Modo claro conforme solicitado
        ctk.set_default_color_theme("green")

        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Frame para botões de ação
        self.action_frame = ctk.CTkFrame(self.main_frame)
        self.action_frame.pack(pady=10, fill="x")

        # Botões de ação
        actions = [
            ("Cadastrar", self.cadastrar_restaurante),
            ("Habilitar/Desabilitar", self.habilitar_restaurante),
            ("Avaliar", self.avaliar_restaurante),
            ("Alterar", self.alterar_restaurante),
            ("Excluir", self.excluir_restaurante)
        ]

        for text, command in actions:
            ctk.CTkButton(self.action_frame, text=text, command=command, width=150).pack(side="left", padx=5)

        # Frame rolável para lista de restaurantes
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.pack(pady=10, fill="both", expand=True)

        # Cabeçalho da lista
        self.header_frame = ctk.CTkFrame(self.scrollable_frame)
        self.header_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(self.header_frame, text="Nome", width=250).pack(side="left", padx=5)
        ctk.CTkLabel(self.header_frame, text="Categoria", width=200).pack(side="left", padx=5)
        ctk.CTkLabel(self.header_frame, text="Avaliação", width=100).pack(side="left", padx=5)
        ctk.CTkLabel(self.header_frame, text="Status", width=100).pack(side="left", padx=5)

        # Lista de restaurantes
        self.restaurant_list = []

        # Carregar dados iniciais
        self.carregar_dados()
        self.atualizar_lista_restaurantes()

    def get_data_dir(self):
        """Retorna o diretório onde os dados serão salvos."""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def carregar_dados(self):
        """Carrega os dados dos restaurantes do arquivo JSON."""
        ARQUIVO_DADOS = os.path.join(self.get_data_dir(), 'dados_restaurantes.json')
        try:
            with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                Restaurante.restaurantes.clear()
                for restaurante_dados in dados:
                    restaurante = Restaurante(
                        restaurante_dados['nome'],
                        restaurante_dados['categoria']
                    )
                    restaurante._ativo = restaurante_dados['ativo']
                    restaurante._avaliacao = [Avaliacao(**avaliacao) for avaliacao in restaurante_dados['avaliacao']]
        except FileNotFoundError:
            CTkMessagebox(title="Informação", message=f"Arquivo de dados não encontrado. Criando um novo arquivo em {ARQUIVO_DADOS}")
            self.salvar_dados()

    def salvar_dados(self):
        """Salva os dados dos restaurantes no arquivo JSON."""
        ARQUIVO_DADOS = os.path.join(self.get_data_dir(), 'dados_restaurantes.json')
        dados = [restaurante.to_dict() for restaurante in Restaurante.restaurantes]
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def atualizar_lista_restaurantes(self):
        """Atualiza a lista de restaurantes exibida na interface."""
        # Limpar a lista atual
        for widget in self.restaurant_list:
            widget.destroy()
        self.restaurant_list.clear()
        
        # Adicionar restaurantes à lista
        for restaurante in Restaurante.restaurantes:
            frame = ctk.CTkFrame(self.scrollable_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(frame, text=restaurante._nome, width=250).pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=restaurante._categoria, width=200).pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=str(restaurante.media_avaliacoes), width=100).pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=restaurante.ativo, width=100).pack(side="left", padx=5)
            
            frame.bind("<Double-1>", lambda e, r=restaurante: self.mostrar_opcoes_restaurante(r._nome))
            self.restaurant_list.append(frame)

    def mostrar_opcoes_restaurante(self, nome_restaurante):
        """Mostra uma janela com opções para o restaurante selecionado."""
        opcoes_window = ctk.CTkToplevel(self)
        opcoes_window.title(f"Opções para {nome_restaurante}")
        opcoes_window.geometry("300x200")

        ctk.CTkButton(opcoes_window, text="Habilitar/Desabilitar", command=lambda: self.habilitar_restaurante(nome_restaurante)).pack(pady=10)
        ctk.CTkButton(opcoes_window, text="Avaliar", command=lambda: self.avaliar_restaurante(nome_restaurante)).pack(pady=10)
        ctk.CTkButton(opcoes_window, text="Alterar", command=lambda: self.alterar_restaurante(nome_restaurante)).pack(pady=10)
        ctk.CTkButton(opcoes_window, text="Excluir", command=lambda: self.excluir_restaurante(nome_restaurante)).pack(pady=10)

    def cadastrar_restaurante(self):
        """Abre uma janela para cadastrar um novo restaurante."""
        dialog = ctk.CTkInputDialog(text="Nome do Restaurante:", title="Cadastrar Restaurante")
        nome = dialog.get_input()
        if nome:
            dialog = ctk.CTkInputDialog(text="Categoria do Restaurante:", title="Cadastrar Restaurante")
            categoria = dialog.get_input()
            if categoria:
                novo_restaurante = Restaurante(nome, categoria)
                self.salvar_dados()
                self.atualizar_lista_restaurantes()
                CTkMessagebox(title="Sucesso", message=f"Restaurante {nome} cadastrado com sucesso!")
            else:
                CTkMessagebox(title="Erro", message="Categoria não fornecida.")
        else:
            CTkMessagebox(title="Erro", message="Nome não fornecido.")

    def habilitar_restaurante(self, nome_restaurante=None):
        """Habilita ou desabilita o restaurante selecionado."""
        if nome_restaurante is None:
            dialog = ctk.CTkInputDialog(text="Nome do Restaurante:", title="Habilitar/Desabilitar Restaurante")
            nome_restaurante = dialog.get_input()
        if nome_restaurante:
            for restaurante in Restaurante.restaurantes:
                if restaurante._nome.lower() == nome_restaurante.lower():
                    restaurante.alternar_estado()
                    self.salvar_dados()
                    self.atualizar_lista_restaurantes()
                    CTkMessagebox(title="Sucesso", message=f"Estado do restaurante {restaurante._nome} alterado para {restaurante.ativo}")
                    return
            CTkMessagebox(title="Erro", message="Restaurante não encontrado.")
        else:
            CTkMessagebox(title="Erro", message="Nome não fornecido.")

    def avaliar_restaurante(self, nome_restaurante=None):
        """Abre uma janela para avaliar o restaurante selecionado."""
        if nome_restaurante is None:
            dialog = ctk.CTkInputDialog(text="Nome do Restaurante:", title="Avaliar Restaurante")
            nome_restaurante = dialog.get_input()
        if nome_restaurante:
            restaurante = next((r for r in Restaurante.restaurantes if r._nome.lower() == nome_restaurante.lower()), None)
            if restaurante:
                dialog = ctk.CTkInputDialog(text="Nome do Cliente:", title="Avaliar Restaurante")
                cliente = dialog.get_input()
                if cliente:
                    dialog = ctk.CTkInputDialog(text="Nota (0-10):", title="Avaliar Restaurante")
                    nota = dialog.get_input()
                    if nota:
                        try:
                            nota = float(nota)
                            if 0 <= nota <= 10:
                                restaurante.receber_avaliacao(cliente, nota)
                                self.salvar_dados()
                                self.atualizar_lista_restaurantes()
                                CTkMessagebox(title="Sucesso", message="Avaliação registrada com sucesso!")
                            else:
                                CTkMessagebox(title="Erro", message="A nota deve estar entre 0 e 10.")
                        except ValueError:
                            CTkMessagebox(title="Erro", message="Por favor, digite um número válido para a nota.")
                    else:
                        CTkMessagebox(title="Erro", message="Nota não fornecida.")
                else:
                    CTkMessagebox(title="Erro", message="Nome do cliente não fornecido.")
            else:
                CTkMessagebox(title="Erro", message="Restaurante não encontrado.")
        else:
            CTkMessagebox(title="Erro", message="Nome do restaurante não fornecido.")

    def alterar_restaurante(self, nome_restaurante=None):
        """Abre uma janela para alterar as informações do restaurante selecionado."""
        if nome_restaurante is None:
            dialog = ctk.CTkInputDialog(text="Nome do Restaurante:", title="Alterar Restaurante")
            nome_restaurante = dialog.get_input()
        if nome_restaurante:
            restaurante = next((r for r in Restaurante.restaurantes if r._nome.lower() == nome_restaurante.lower()), None)
            if restaurante:
                dialog = ctk.CTkInputDialog(text="Novo Nome (deixe em branco para não alterar):", title="Alterar Restaurante")
                novo_nome = dialog.get_input()
                dialog = ctk.CTkInputDialog(text="Nova Categoria (deixe em branco para não alterar):", title="Alterar Restaurante")
                nova_categoria = dialog.get_input()
                if novo_nome or nova_categoria:
                    if novo_nome:
                        restaurante._nome = novo_nome.title()
                    if nova_categoria:
                        restaurante._categoria = nova_categoria.upper()
                    self.salvar_dados()
                    self.atualizar_lista_restaurantes()
                    CTkMessagebox(title="Sucesso", message=f"Restaurante alterado com sucesso para: {restaurante}")
                else:
                    CTkMessagebox(title="Erro", message="Nenhuma alteração fornecida.")
            else:
                CTkMessagebox(title="Erro", message="Restaurante não encontrado.")
        else:
            CTkMessagebox(title="Erro", message="Nome do restaurante não fornecido.")

    def excluir_restaurante(self, nome_restaurante=None):
        """Exclui o restaurante selecionado após confirmação do usuário."""
        if nome_restaurante is None:
            dialog = ctk.CTkInputDialog(text="Nome do Restaurante:", title="Excluir Restaurante")
            nome_restaurante = dialog.get_input()
        if nome_restaurante:
            restaurante = next((r for r in Restaurante.restaurantes if r._nome.lower() == nome_restaurante.lower()), None)
            if restaurante:
                confirmacao = CTkMessagebox(title="Confirmar Exclusão", 
                                            message=f"Tem certeza que deseja excluir o restaurante '{restaurante._nome}'?",
                                            icon="question", option_1="Sim", option_2="Não")
                if confirmacao.get() == "Sim":
                    Restaurante.restaurantes.remove(restaurante)
                    self.salvar_dados()
                    self.atualizar_lista_restaurantes()
                    CTkMessagebox(title="Sucesso", message=f"Restaurante '{restaurante._nome}' excluído com sucesso.")
            else:
                CTkMessagebox(title="Erro", message="Restaurante não encontrado.")
        else:
            CTkMessagebox(title="Erro", message="Nome do restaurante não fornecido.")

if __name__ == '__main__':
    app = RestauranteApp()
    app.mainloop()