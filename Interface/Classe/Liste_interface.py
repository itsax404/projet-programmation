import os.path
import tkinter as tk
from tkinter import ttk, messagebox, Menu, filedialog
from .PdFviewer import Visualisation_pdf
from .Fenetre_def_modèle import Defenir_modele
class Liste_interface_c (tk.Frame):
    def __init__(self, master, main_path, database, image_processor):
        super().__init__(master)
        self.master = master
        self.pack()
        self.path = main_path
        self.database = database
        self.image_processor = image_processor


    def affichage(self):

        self.frame = tk.Frame(master=self.master, borderwidth=5, relief="ridge")
        self.frame.pack(fill=tk.BOTH)

        self.affichage_label_btn()

        self.affichage_label_list()


    def affichage_label_btn(self):
        """affichage des butons : tout selectonner, supprimer et visualiser .

            Parameters:

            Returns:
                    affichage dans la fênetre"""

        self.file_btn = tk.LabelFrame(self.frame, text="option")
        self.file_btn.pack(fill=tk.BOTH, padx=20, pady=10)

        btn_all = tk.Button(master=self.file_btn, text="Selectionner tout les fichiers", command=self.tout_select)
        btn_all.grid(row=0, column=0, padx=10, pady=10)

        btn_suppr = tk.Button(master=self.file_btn, text="Supprimer", command=self.suppr)
        btn_suppr.grid(row=0, column=1, padx=10, pady=10)

        btn_visualisation = tk.Button(master=self.file_btn, text="Visualiser fichier", command=self.visualisation)
        btn_visualisation.grid(row=0, column=2, padx=10, pady=10)

        btn_visualisation = tk.Button(master=self.file_btn, text="Definir modèle", command=self.open_fenetre_modèle)
        btn_visualisation.grid(row=0, column=3, padx=10, pady=10)

    def affichage_label_list(self):

        """
        affichage de la liste des fichiers + scrollbar pour defiler les fichiers insérés
        :return:
        """
        "frame"
        self.file_frame = tk.LabelFrame(self.frame, text="liste des fichiers")
        self.file_frame.pack(fill=tk.BOTH, padx=10)

        #liste
        self.tv = ttk.Treeview(master=self.file_frame, columns=(1, 2, 3), show='headings', height=3)
        self.tv.grid(pady=10, padx=10, row=1, column=0)

        self.tv.column(1, width=25)
        self.tv.column(2, width=575)
        self.tv.column(3, width=50)

        self.tv.heading(1, text='Type')
        self.tv.heading(2, text='Adresse du fichier')
        self.tv.heading(3, text='Modèle')

        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview")
        #

        #scrollbar
        scrollbar = tk.Scrollbar(self.file_frame)
        scrollbar.grid(row=1, column=3)

        self.tv.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tv.yview)


    def add(self, file):
        if(file!=None) :
            for newfile in file:
                self.tv.insert(parent='', index='end', values=(0, newfile, 5))


    def suppr(self):
        res = messagebox.askyesno('', 'Voulez-vous vraiment supprimer les fichers?')
        if res == True:
            for selected_item in self.tv.selection():
                self.tv.delete(selected_item)


    def tout_select(self):
        """
        TODO docstring
        :return:
        """
        for item in self.tv.get_children():
            self.tv.selection_add(item)


    def visualisation(self):
        selected_item = self.tv.selection()[0]
        data = list(self.tv.item(selected_item).get("values"))
        v_fenetre = Visualisation_pdf(self.master, data[1], self.path, self.database, self.image_processor)
        v_fenetre.affichage()


    def open_fenetre_modèle(self):
        self.fenetre_defmodele = Defenir_modele(self, self.path, self.database)
        self.fenetre_defmodele.affichage()



    def change_type_modele(self):
        selected_item = self.tv.selection()
        self.tv.item(item=selected_item, values=("test toto", "tom", "Ad"))




class Menu_p (tk.Frame):
    def __init__(self, master, list_interface):
        super().__init__(master)
        self.master = master
        self.list = list_interface
        self.pack()


    def affichage(self):
        menu = Menu(master=self.master)
        element_menu = Menu(menu)
        element_menu.add_command(label='Ouvrir fichier', command=self.Openfiles)
        menu.add_cascade(label="Menu", menu=element_menu)
        self.master.config(menu=menu)


    def Openfiles(self):
        filenames = filedialog.askopenfilenames(initialdir="/", title="Select a File",
                                                filetypes=(("pdf", "*.pdf"), ("all files", "*.*")))
        self.list.add(filenames)

