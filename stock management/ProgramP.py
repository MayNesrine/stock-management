import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import mysql.connector
from datetime import datetime
from Login import LoginWindow
import socket
from socket import error as SocketError
import time 
class GestionStock:
    def __init__(self, master):
        self.master = master
        self.login_window = LoginWindow(tk.Toplevel(self.master), self)
        self.master.withdraw()  # Cache la fenêtre principale
    def show_main_window(self):
        self.master.deiconify()
        self.master.geometry("780x680")
        self.master.title("Gestion de stock")
        self.master.resizable(False, False)  # Empêche le redimensionnement de la fenêtre
        self.current_frame = None  # Pour suivre le cadre actuel
        self.create_frames()
        self.create_menu()
        self.cadre_principal()
        self.check_stock_periodically()
       
    def create_frames(self):        #créer les deux frames des bases
        self.top_frame = tk.Frame(self.master, bg="white")
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.cadre_menu = tk.Frame(self.master, bg="white")
        self.cadre_menu.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_menu(self):          #les deux boutons en menu 
        self.principal=tk.Button(self.cadre_menu,text="Screen Principal", bg="#118098", font=("Helvetica", 12, "bold"),
                                 command=self.cadre_principal)
        self.principal.grid(row=0, column=1, padx=10, pady=20)
        self.article = tk.Button(self.cadre_menu, text="Add Reference", bg="#118098", font=("Helvetica", 12, "bold"),
                                 command=self.cadre_ajout_article)
        self.article.grid(row=0, column=2, padx=10, pady=20) 
    def cadre_ajout_article(self):      #interface pour afficher l'historique et ajouter un nouveau article à la base des données 
        if self.current_frame == "article":
            return  
        self.current_frame = "article"
        self.left_frame.destroy()
        self.right_frame.destroy()
 
        self.article_frame = tk.Frame(self.top_frame, bg="#cdd2b4", width=750, height=520)
        self.article_frame.pack(fill=tk.BOTH, expand=True)
        
        self.titre = tk.Label(self.article_frame, text="BASE DES DONNEES DES ARTICLES", font=("Helvetica", 17, "bold", "underline"), fg="brown", bg="#cdd2b4")
        self.titre.pack(pady=17)
        self.AA = tk.Label(self.article_frame, text="AJOUT_ARTICLE", font=("Helvetica", 14, "bold", "underline"), fg="#118098", bg="#cdd2b4")
        self.AA.place(relx=0.15,rely=0.14)
        self.AA = tk.Label(self.article_frame, text="Historique", font=("Helvetica", 15, "bold", "underline"), fg="#118098", bg="#cdd2b4")
        self.AA.place(relx=0.7,rely=0.14)
        self.label_reference = tk.Label(self.article_frame, text="Référence:", font=("Helvetica", 12, "bold"), fg="#234349", bg="#cdd2b4")
        self.label_reference.place(relx=0.01, rely=0.25, anchor="w")
        self.champ_reference = tk.Entry(self.article_frame, width=20)
        self.champ_reference.place(relx=0.23, rely=0.25, anchor="w")

        self.label_adresse = tk.Label(self.article_frame, text="Adresse:", font=("Helvetica", 12, "bold"), fg="#234349", bg="#cdd2b4")
        self.label_adresse.place(relx=0.01, rely=0.35, anchor="w")
        self.champ_adresse = tk.Entry(self.article_frame, width=20)
        self.champ_adresse.place(relx=0.23, rely=0.35, anchor="w")

        self.label_place = tk.Label(self.article_frame, text="Place:", font=("Helvetica", 12, "bold"), fg="#234349", bg="#cdd2b4")
        self.label_place.place(relx=0.01, rely=0.45, anchor="w")
        self.champ_place = tk.Entry(self.article_frame, width=20)
        self.champ_place.place(relx=0.23, rely=0.45, anchor="w")

        self.label_quantite_tot = tk.Label(self.article_frame, text="Quantité maximale:", font=("Helvetica", 12, "bold"), fg="#234349", bg="#cdd2b4")
        self.label_quantite_tot.place(relx=0.01, rely=0.55, anchor="w")
        self.champ_quantite_tot = tk.Entry(self.article_frame, width=20)
        self.champ_quantite_tot.place(relx=0.23, rely=0.55, anchor="w")

        self.label_quantite_min = tk.Label(self.article_frame , text="Quantité minimale:", font=("Helvetica", 12, "bold"), fg="#234349", bg="#cdd2b4")
        self.label_quantite_min.place(relx=0.01, rely=0.65, anchor="w")
        self.champ_quantite_min = tk.Entry(self.article_frame , width=20)
        self.champ_quantite_min.place(relx=0.23, rely=0.65, anchor="w")

        self.bouton_ajouter = tk.Button(self.article_frame , text="Enregistrer", bg="lightgreen", font=("Helvetica", 12, "bold"),width=17, command=lambda: self.ajouter_article(self.champ_reference.get(), self.champ_adresse.get(), self.champ_place.get(), self.champ_quantite_tot.get(), self.champ_quantite_min.get()))
        self.bouton_ajouter.place(relx=0.05, rely=0.75, anchor="w")
        self.bouton_ferm= tk.Button(self.article_frame , text="fermer", bg="#FF5733", font=("Helvetica", 12, "bold"),width=17, command=self.fermer_aprés_ajout)
        self.bouton_ferm.place(relx=0.05, rely=0.83, anchor="w")
        # Créer un widget Treeview
        self.tree_historique = ttk.Treeview(self.article_frame, columns=('Nom_agent', 'Matricule','Reference', 'Qté_Sortie'))
        self.tree_historique.place(relx=0.47, rely=0.25)
        self.bouton_vider = tk.Button(self.article_frame , text="Vider historique", bg="lightgreen", font=("Helvetica", 12, "bold"),width=17,command=self.clear_history)
        self.bouton_vider.place(relx=0.57, rely=0.75, anchor="w")
        self.btn_delete_row = tk.Button(self.article_frame, text="Supprimer ligne", bg="#FF5733", font=("Helvetica", 12, "bold"),width=17,
                                        command=self.delete_selected_row)
        self.btn_delete_row.place(relx=0.57, rely=0.83, anchor="w")
        # Ajouter des en-têtes de colonne
        self.tree_historique.heading('#0', text='Date')
        self.tree_historique.heading('Nom_agent', text='Nom_agent')
        self.tree_historique.heading('Matricule', text='Matricule')
        self.tree_historique.heading('Reference', text='Reference')
        self.tree_historique.heading('Qté_Sortie', text='Qté_Sortie')

        self.tree_historique.column('#0', width=125) 
        self.tree_historique.column('Nom_agent', width=90) 
        self.tree_historique.column('Matricule', width=70) 
        self.tree_historique.column('Reference', width=60) 
        self.tree_historique.column('Qté_Sortie', width=55) 
        self.afficher_historique()

    def ajouter_article(self, reference, adresse, place, quantite_tot, quantite_min):#la fonction d'ajouter un nouveau article ou update la quantité totale d'article trouvé
        if reference and adresse and place and quantite_tot and quantite_min:
            try:
                self.connection()
                curseur = self.connexion.cursor()
                curseur.execute("SELECT Quantite_totale FROM articles WHERE reference_article = %s", (reference,))
                row = curseur.fetchone()
                if row: 
                    quantite_actuelle = row[0]
                    nouvelle_quantite = int(quantite_actuelle) +int(quantite_tot)
                    curseur.execute("UPDATE articles SET Quantite_totale = %s WHERE reference_article = %s", (nouvelle_quantite, reference))
                else:  
                    curseur.execute('INSERT INTO articles (reference_article, Adresse_article, Place_article, Quantite_totale, Quantite_min) VALUES (%s, %s, %s, %s, %s);',
                                    (reference, adresse, place, quantite_tot, quantite_min))
                self.envoyer_commande("ouvrir_tiroir",adresse)
                self.connexion.commit()
                print("Article ajouté avec succès.")
            except mysql.connector.Error as e:
                print(f"Erreur lors de l'ajout de l'article: {e}")
            self.close_connection()
    def fermer_aprés_ajout(self):
        self.envoyer_commande("fermer_tiroir",self.champ_adresse.get())
        time.sleep(0.5)
        for entry in [self.champ_reference, self.champ_adresse, self.champ_place, self.champ_quantite_tot, self.champ_quantite_min]:
            entry.delete(0, tk.END)
        
    def cadre_principal(self):
        if self.current_frame == "principal":
            return
        if self.current_frame == "article":
            self.article_frame.destroy()
            pass
        self.current_frame = "principal"
        self.left_frame = tk.Frame(self.top_frame, bg="gray", width=250, height=520)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.top_frame, bg="lightgrey", width=500, height=520)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        project_dossier = os.path.dirname(__file__)  # Répertoire du prog Python actuel
        self.image_path = os.path.join(project_dossier, "icone.png")

        self.canvas = tk.Canvas(self.left_frame, width=90, height=90, bg="gray")
        self.canvas.grid(row=0, column=0, columnspan=2, padx=50, pady=10,ipadx=2,ipady=2)
        self.circle = self.canvas.create_oval(0, 0, 100, 100, fill="gray")
        self.image = PhotoImage(file=self.image_path)
        self.canvas.create_image(50, 50, image=self.image)
        self.canvas.image = self.image
        self.label_nom_agent = tk.Label(self.left_frame, text="Nom de l'agent:", bg="grey", fg="white", font=("bold"))
        self.label_nom_agent.grid(row=1, column=0, padx=10, pady=20, sticky="w")
        self.champ_nom_agent = tk.Entry(self.left_frame)
        self.champ_nom_agent.grid(row=1, column=1, padx=10, pady=20)
        self.champ_nom_agent.bind('<KeyRelease>', self.autoriser_ecriture)

        self.label_matricule = tk.Label(self.left_frame, text="Matricule:", bg="grey", fg="white", font=("bold"))
        self.label_matricule.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.champ_matricule = tk.Entry(self.left_frame,state=tk.DISABLED)
        self.champ_matricule.grid(row=2, column=1, padx=10, pady=10)
        self.champ_matricule.bind('<KeyRelease>', self.autoriser_ecriture)

        self.title = tk.Label(self.right_frame, text="GESTION DE STOCK AUTOMATIQUE",
                              font=("Helvetica", 16, "bold", "underline"), fg="#B15201", bg="lightgray")
        self.title.grid(row=0, column=0, columnspan=2, padx=20, pady=5)

        self.label_reference_article = tk.Label(self.right_frame, text="Référence de l'article:", font="bold",
                                                fg="black", bg="lightgrey")
        self.label_reference_article.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.champ_reference_article = tk.Entry(self.right_frame,state=tk.DISABLED)
        self.champ_reference_article.grid(row=1, column=1, padx=10, pady=10)
        self.champ_reference_article.bind("<FocusOut>", lambda event: self.db_article_details())#lorsque on termine de saisir quelque chose dans le champ de référence d'article,on récupére les détails de l'article correspondant à la référence saisie

        self.label_quantite_sortie = tk.Label(self.right_frame, text="Quantité à sortir:", font="bold",
                                              fg="black", bg="lightgrey")
        self.label_quantite_sortie.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.champ_quantite_sortie = tk.Entry(self.right_frame,state=tk.DISABLED)
        self.champ_quantite_sortie.grid(row=2, column=1, padx=10, pady=10)
        self.champ_quantite_sortie.bind("<KeyRelease>", self.update_quantite_restante)#une touche est relâchée dans le champ de saisie self.champ_quantite_sortie, la fonction self.update_quantite_restante sera appelée

        self.label_AdresseIP_article = tk.Label(self.right_frame, text="AdresseIP de l'article:", font="bold",
                                                fg="black", bg="lightgrey")
        self.label_AdresseIP_article.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.champ_AdresseIP_article = tk.Entry(self.right_frame)
        self.champ_AdresseIP_article.grid(row=3, column=1, padx=10, pady=10)

        self.label_Place_article = tk.Label(self.right_frame, text="Emplacement de l'article:", font="bold",
                                            fg="black", bg="lightgrey")
        self.label_Place_article.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.champ_Place_article = tk.Entry(self.right_frame)
        self.champ_Place_article.grid(row=4, column=1, padx=10, pady=10)

        self.label_Quantité_totale = tk.Label(self.right_frame, text="Quantité Totale:", font="bold",
                                              fg="black", bg="lightgrey")
        self.label_Quantité_totale.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.champ_Quantité_totale = tk.Entry(self.right_frame)
        self.champ_Quantité_totale.grid(row=5, column=1, padx=10, pady=10)

        self.label_Quantité_restante = tk.Label(self.right_frame, text="Quantité restante:", font="bold",
                                                fg="black", bg="lightgrey")
        self.label_Quantité_restante.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.champ_Quantité_restante = tk.Label(self.right_frame, width=17,anchor="w")
        self.champ_Quantité_restante.grid(row=6, column=1, padx=10, pady=10)

        self.label_Quantité_minimale = tk.Label(self.right_frame, text="Quantité minimale:", font="bold",
                                                 fg="black", bg="lightgrey")
        self.label_Quantité_minimale.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.champ_Quantité_minimale = tk.Entry(self.right_frame)
        self.champ_Quantité_minimale.grid(row=7, column=1, padx=10, pady=10)
        self.B_ouvrir = tk.Button(self.right_frame, text="Ouvrir Tiroir", bg="#34A853", font=("bold"),command=self.enregistrer_sortie)
        self.B_ouvrir.grid(row=8, column=0, columnspan=2, padx=30, pady=20, ipadx=25, ipady=5)
        self.B_fermer = tk.Button(self.right_frame, text="Fermer Tiroir", bg="#AD452F", font=("bold"),command=self.fermer_tiroir)
        self.B_fermer.grid(row=9, column=0, columnspan=2, padx=10, pady=8, ipadx=22, ipady=5)
    
    def enregistrer_sortie(self):               #enregistrer l'historique et envoyer la commande(ouvrir le tiroir ou manque de stock)
        nom_agent = self.champ_nom_agent.get()
        matricule = self.champ_matricule.get()
        reference_article = self.champ_reference_article.get()
        quantite_sortie = self.champ_quantite_sortie.get()
        date_sortie = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if nom_agent and matricule and reference_article and quantite_sortie and date_sortie:
            try:
                self.connection()
                curseur = self.connexion.cursor()

                esp32_address = self.champ_AdresseIP_article.get()  #choisir l'adresse de la carte ESP32
                Quantité_totale = int(self.champ_Quantité_totale.get())
                quantite_min = int(self.champ_Quantité_minimale.get())
                quantite_sortie= int(self.champ_quantite_sortie.get())
                quantite_restante = Quantité_totale - quantite_sortie
                if  Quantité_totale<= quantite_min or quantite_restante<= quantite_min:
                    self.envoyer_commande("manque_de_stock", esp32_address)
                else: 
                    self.envoyer_commande("ouvrir_tiroir",esp32_address)    #commande pour ouvrir la tiroir 
                    #mettre à jour la quantité totale
                    curseur.execute('UPDATE articles SET Quantite_totale = Quantite_totale - %s WHERE reference_article = %s',
                                    (quantite_sortie, reference_article))
                    time.sleep(2)                
                    curseur.execute('INSERT INTO historique_article (DA_TE, nom_agent, matricule_agent, reference_article, quantite_sortie) VALUES (%s, %s, %s, %s, %s)',
                                (date_sortie, nom_agent, matricule, reference_article, quantite_sortie))

                self.connexion.commit()

                # Validation de la transaction
                self.connexion.commit()
                self.autoriser_ecriture()   #désactiver l'autoristion à l'écriture suivante

            except mysql.connector.Error as e:
                print(f"Erreur lors de l'enregistrement de la sortie: {e}")

            self.close_connection()

    def envoyer_commande(self,commande,esp32_address):          #envoi une commande vers le serveur ESP32 à traiter
        if esp32_address:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Créer socket TCP
                client_socket.connect((esp32_address, 8080))  # Remplacez 8080 par esp32_port # 0 représente un port aléatoire
                client_socket.sendall(commande.encode())    #envoyer la commande
                client_socket.close()
                print("Commande envoyée à l'ESP32.")
            except SocketError as e:        #Exception d'erreur par socket
                print(f"Erreur de l'envoi de la commande à l'ESP32 : {e}") 

    def fermer_tiroir(self):
        self.envoyer_commande("fermer_tiroir", self.champ_AdresseIP_article.get())
        self.champ_nom_agent.delete(0,tk.END)
        self.champ_matricule.delete(0,tk.END)
        self.champ_reference_article.delete(0,tk.END)
        self.champ_AdresseIP_article.delete(0,tk.END)
        self.champ_Place_article.delete(0,tk.END)
        self.champ_quantite_sortie.delete(0,tk.END)
        self.champ_Quantité_totale.delete(0,tk.END)
        self.champ_Quantité_totale.config(bg="white")
        self.champ_Quantité_restante.config(text="",bg="white")
        self.champ_Quantité_minimale.delete(0,tk.END)

        self.autoriser_ecriture()   #désactiver l'autoristion à l'écriture suivante
    def afficher_historique(self):          # Récupérer l'historique à partir de la base des données
        try:
            self.connection()
            curseur = self.connexion.cursor()

            curseur.execute('SELECT * FROM historique_article')
            rows = curseur.fetchall()  #récupérer tous les lignes d'historique d'une requête SELECT

            for row in rows:    #insérer les données dans l'interface 
                self.tree_historique.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4]))

        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération de l'historique: {e}")
        self.close_connection()
    def delete_selected_row(self):
        selected_row = self.tree_historique.selection()
        if selected_row:
            row_id = self.tree_historique.item(selected_row)['text']
            try:
                self.connection()
                curseur = self.connexion.cursor()

                curseur.execute("DELETE FROM historique_article WHERE DA_TE = %s", (row_id,))
                self.connexion.commit()

                self.tree_historique.delete(selected_row)
                print("Row deleted successfully.")
            except mysql.connector.Error as e:
                print(f"Error deleting row: {e}")
                self.close_connection()
        else:
            print("select a row to delete.")
    def clear_history(self):
        try:
            self.connection()
            curseur = self.connexion.cursor()
            curseur.execute('DELETE FROM historique_article')
            self.connexion.commit()
            print("History cleared successfully from the database.")
            self.tree_historique.delete(*self.tree_historique.get_children())
            print("History cleared successfully from the interface.")
        except pyodbc.Error as e:
            print(f"Error clearing history: {e}")

        self.close_connection()

    def update_quantite_restante(self, event):    # Obtenir la quantité totale et la quantité de sortie actuelles
         quantite_minimale = self.champ_Quantité_minimale.get()
         min_Qte = int(quantite_minimale)
         quantite_totale = self.champ_Quantité_totale.get()
         quantite_sortie = self.champ_quantite_sortie.get()
         total_str = int(quantite_totale)
         sortie_str = int(quantite_sortie)
         quantite_restante = total_str - sortie_str
         self.champ_Quantité_restante.config(text=str(quantite_restante))
         if  quantite_restante<= min_Qte:
             self.champ_Quantité_restante.config(bg="red")
         else:
             self.champ_Quantité_restante.config(bg="white")
        


    def db_article_details(self):               # Récupérer les détails de l'article à partir de son réference
        reference_article = self.champ_reference_article.get()
        if reference_article:
            try:
                self.connection()
                curseur = self.connexion.cursor()

                # Récupérer les détails de l'article à partir de la base de données
                requete = "SELECT Adresse_article, Place_article, Quantite_totale, Quantite_min FROM articles WHERE reference_article = %s"
                curseur.execute(requete, (reference_article,))
                details = curseur.fetchone()  # récupérer la prochaine ligne de résultat d'une requête SELECT

                # Mettre à jour les champs de texte avec les détails récupérés
                if details:
                    adresse, place, Qte_Totale, Qte_min = details
                    self.champ_AdresseIP_article.delete(0, tk.END)
                    self.champ_AdresseIP_article.insert(0, adresse)
                    self.champ_Place_article.delete(0, tk.END)
                    self.champ_Place_article.insert(0, place)
                    self.champ_Quantité_totale.delete(0, tk.END)
                    self.champ_Quantité_totale.insert(0, Qte_Totale)
                    self.champ_Quantité_minimale.delete(0, tk.END)
                    self.champ_Quantité_minimale.insert(0, Qte_min)

                    if Qte_Totale <= Qte_min:
                        self.champ_Quantité_totale.config(bg="red")
                    else:
                        self.champ_Quantité_totale.config(bg="white")

                self.close_connection()

            except mysql.connector.Error as e:
                print(f"Erreur lors de la récupération des détails de l'article: {e}")


    def autoriser_ecriture(self,event=None):    #Priorité de remplir les champs d'écriture
        if self.champ_nom_agent.get():
            self.champ_matricule.config(state=tk.NORMAL)  # Autoriser l'écriture dans le champ
            if self.champ_matricule.get():
                self.champ_reference_article.config(state=tk.NORMAL) 
                self.champ_quantite_sortie.config(state=tk.NORMAL)  
            else: 
                self.champ_reference_article.delete(0, tk.END)        
                self.champ_reference_article.config(state=tk.DISABLED)
                self.champ_quantite_sortie.delete(0, tk.END)        
                self.champ_quantite_sortie.config(state=tk.DISABLED)
        else:
            self.champ_matricule.delete(0, tk.END)        
            self.champ_matricule.config(state=tk.DISABLED) # désactiver l'écriture dans le champ
            self.champ_reference_article.delete(0, tk.END)        
            self.champ_reference_article.config(state=tk.DISABLED)
            self.champ_quantite_sortie.delete(0, tk.END)        
            self.champ_quantite_sortie.config(state=tk.DISABLED)
    
    def connection(self):           #fonction de connection avec mysql
        self.connexion = None
        try:
            self.connexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rpi",
                database="project_Omar"
            )
        except mysql.connector.Error as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")

    def close_connection(self):   #fonction déconnexion avec base des données
        if self.connexion:
            self.connexion.close()
    def check_stock_periodically(self):
        try:
            self.connection()
            curseur = self.connexion.cursor()
            curseur.execute('SELECT reference_article, Quantite_totale, Quantite_min, Adresse_article FROM articles')
            articles = curseur.fetchall()

            for reference, quantite_totale, quantite_min, esp32_address in articles:
                if quantite_totale <= quantite_min:
                    self.envoyer_commande("manque_de_stock", esp32_address)
                    print(f"Manque de stock pour la référence : {reference}")

        except pyodbc.Error as e:
            print(f"Erreur lors de la vérification du stock : {e}")
        self.close_connection()
        self.master.after(60000, self.check_stock_periodically)


if __name__ == "__main__":
    fenetre = tk.Tk()
    app = GestionStock(fenetre)
    fenetre.mainloop()
