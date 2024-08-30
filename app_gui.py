import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import sys
from modelos.restaurante import Restaurante
from modelos.avaliacao import Avaliacao

class RestauranteApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gerenciamento de Restaurantes")
        self.geometry("800x600")

        # Definir o ícone da janela
        if os.path.exists("restaurante.ico"):
            self.iconbitmap("restaurante.ico")
        else:
            print("Arquivo de ícone 'restaurante.ico' não encontrado.")

        # Configuração do estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Lista de restaurantes
        self.tree = ttk.Treeview(self.main_frame, columns=("Nome", "Categoria", "Avaliação", "Status"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Avaliação", text="Avaliação")
        self.tree.heading("Status", text="Status")
        
        # Configuração das colunas para centralizar os dados
        self.tree.column("Nome", anchor="w", width=200)
        self.tree.column("Categoria", anchor="center", width=150)
        self.tree.column("Avaliação", anchor="center", width=100)
        self.tree.column("Status", anchor="center", width=100)
        
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Frame para botões
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        # Botões
        ttk.Button(self.button_frame, text="Cadastrar Restaurante", command=self.cadastrar_restaurante).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Habilitar/Desabilitar", command=self.habilitar_restaurante).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="Avaliar Restaurante", command=self.avaliar_restaurante).grid(row=0, column=2, padx=5)
        ttk.Button(self.button_frame, text="Alterar Restaurante", command=self.alterar_restaurante).grid(row=0, column=3, padx=5)
        ttk.Button(self.button_frame, text="Excluir Restaurante", command=self.excluir_restaurante).grid(row=0, column=4, padx=5)

        # Carregar dados iniciais
        self.carregar_dados()
        self.atualizar_lista_restaurantes()

    def get_data_dir(self):
        """
        Retorna o diretório onde os dados serão salvos.
        Se o programa for um executável, usa o diretório do executável.
        Caso contrário, usa o diretório do script.
        """
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def carregar_dados(self):
        """
        Carrega os dados dos restaurantes a partir do arquivo JSON.
        Se o arquivo não existir, cria um novo arquivo vazio.
        """
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
            messagebox.showinfo("Informação", f"Arquivo de dados não encontrado. Criando um novo arquivo em {ARQUIVO_DADOS}")
            self.salvar_dados()

    def salvar_dados(self):
        """
        Salva os dados dos restaurantes no arquivo JSON.
        """
        ARQUIVO_DADOS = os.path.join(self.get_data_dir(), 'dados_restaurantes.json')
        dados = []
        for restaurante in Restaurante.restaurantes:
            dados.append({
                'nome': restaurante._nome,
                'categoria': restaurante._categoria,
                'ativo': restaurante._ativo,
                'avaliacao': [avaliacao.__dict__() for avaliacao in restaurante._avaliacao]
            })
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def atualizar_lista_restaurantes(self):
        """
        Atualiza a lista de restaurantes exibida na interface gráfica.
        """
        for i in self.tree.get_children():
            self.tree.delete(i)
        for restaurante in Restaurante.restaurantes:
            self.tree.insert("", "end", values=(restaurante._nome, restaurante._categoria, restaurante.media_avaliacoes, restaurante.ativo))

    def cadastrar_restaurante(self):
        """
        Abre uma janela para cadastrar um novo restaurante.
        """
        def salvar():
            nome = nome_entry.get()
            categoria = categoria_entry.get()
            if nome and categoria:
                novo_restaurante = Restaurante(nome, categoria)
                self.salvar_dados()
                self.atualizar_lista_restaurantes()
                top.destroy()
                messagebox.showinfo("Sucesso", f"Restaurante {nome} cadastrado com sucesso!")
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

        top = tk.Toplevel(self)
        top.title("Cadastrar Restaurante")
        top.geometry("300x200")
        if os.path.exists("restaurante.ico"):
            top.iconbitmap("restaurante.ico")
            
        ttk.Label(top, text="Nome:").pack(pady=5)
        nome_entry = ttk.Entry(top)
        nome_entry.pack(pady=5)

        ttk.Label(top, text="Categoria:").pack(pady=5)
        categoria_entry = ttk.Entry(top)
        categoria_entry.pack(pady=5)

        ttk.Button(top, text="Salvar", command=salvar).pack(pady=10)

    def habilitar_restaurante(self):
        """
        Habilita ou desabilita o restaurante selecionado.
        """
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado)
            nome_restaurante = item['values'][0]
            for restaurante in Restaurante.restaurantes:
                if restaurante._nome == nome_restaurante:
                    restaurante.alternar_estado()
                    self.salvar_dados()
                    self.atualizar_lista_restaurantes()
                    messagebox.showinfo("Sucesso", f"Estado do restaurante {restaurante._nome} alterado para {restaurante.ativo}")
                    return
        else:
            messagebox.showerror("Erro", "Por favor, selecione um restaurante.")

    def avaliar_restaurante(self):
        """
        Abre uma janela para avaliar o restaurante selecionado.
        """
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado)
            nome_restaurante = item['values'][0]
            
            def salvar_avaliacao():
                cliente = cliente_entry.get()
                nota = nota_entry.get()
                if cliente and nota:
                    try:
                        nota = float(nota)
                        if 0 <= nota <= 10:
                            for restaurante in Restaurante.restaurantes:
                                if restaurante._nome == nome_restaurante:
                                    restaurante.receber_avaliacao(cliente, nota)
                                    self.salvar_dados()
                                    self.atualizar_lista_restaurantes()
                                    top.destroy()
                                    messagebox.showinfo("Sucesso", "Avaliação registrada com sucesso!")
                                    return
                        else:
                            messagebox.showerror("Erro", "A nota deve estar entre 0 e 10.")
                    except ValueError:
                        messagebox.showerror("Erro", "Por favor, digite um número válido para a nota.")
                else:
                    messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

            top = tk.Toplevel(self)
            top.title(f"Avaliar Restaurante: {nome_restaurante}")
            top.geometry("300x200")
            if os.path.exists("restaurante.ico"):
                top.iconbitmap("restaurante.ico")

            ttk.Label(top, text="Nome do Cliente:").pack(pady=5)
            cliente_entry = ttk.Entry(top)
            cliente_entry.pack(pady=5)

            ttk.Label(top, text="Nota (0-10):").pack(pady=5)
            nota_entry = ttk.Entry(top)
            nota_entry.pack(pady=5)

            ttk.Button(top, text="Salvar Avaliação", command=salvar_avaliacao).pack(pady=10)
        else:
            messagebox.showerror("Erro", "Por favor, selecione um restaurante.")

    def alterar_restaurante(self):
        """
        Abre uma janela para alterar as informações do restaurante selecionado.
        """
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado)
            nome_restaurante = item['values'][0]
            
            def salvar_alteracoes():
                novo_nome = novo_nome_entry.get()
                nova_categoria = nova_categoria_entry.get()
                if novo_nome or nova_categoria:
                    for restaurante in Restaurante.restaurantes:
                        if restaurante._nome == nome_restaurante:
                            if novo_nome:
                                restaurante._nome = novo_nome.title()
                            if nova_categoria:
                                restaurante._categoria = nova_categoria.upper()
                            self.salvar_dados()
                            self.atualizar_lista_restaurantes()
                            top.destroy()
                            messagebox.showinfo("Sucesso", f"Restaurante alterado com sucesso para: {restaurante}")
                            return
                else:
                    messagebox.showerror("Erro", "Por favor, preencha pelo menos um campo para alterar.")

            top = tk.Toplevel(self)
            top.title(f"Alterar Restaurante: {nome_restaurante}")
            top.geometry("300x200")
            if os.path.exists("restaurante.ico"):
                top.iconbitmap("restaurante.ico")

            ttk.Label(top, text="Novo Nome:").pack(pady=5)
            novo_nome_entry = ttk.Entry(top)
            novo_nome_entry.pack(pady=5)

            ttk.Label(top, text="Nova Categoria:").pack(pady=5)
            nova_categoria_entry = ttk.Entry(top)
            nova_categoria_entry.pack(pady=5)

            ttk.Button(top, text="Salvar Alterações", command=salvar_alteracoes).pack(pady=10)
        else:
            messagebox.showerror("Erro", "Por favor, selecione um restaurante.")

    def excluir_restaurante(self):
        """
        Exclui o restaurante selecionado após confirmação do usuário.
        """
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado)
            nome_restaurante = item['values'][0]
            confirmacao = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o restaurante '{nome_restaurante}'?")
            if confirmacao:
                for restaurante in Restaurante.restaurantes:
                    if restaurante._nome == nome_restaurante:
                        Restaurante.restaurantes.remove(restaurante)
                        self.salvar_dados()
                        self.atualizar_lista_restaurantes()
                        messagebox.showinfo("Sucesso", f"Restaurante '{nome_restaurante}' excluído com sucesso.")
                        return
        else:
            messagebox.showerror("Erro", "Por favor, selecione um restaurante.")

if __name__ == '__main__':
    app = RestauranteApp()
    app.mainloop()