import tkinter as tk

from tkinter import Label,PhotoImage, Entry,Button,ttk

from tkinter.ttk import Treeview
import RPi.GPIO as GPIO

import os

from tkinter import simpledialog

import time

from database import DataBase

from tkinter import messagebox
case1=17

case2=15

led1=23

led2=22
ledstock1=27
ledstock2=8
GPIO.setmode(GPIO.BCM)

GPIO.setup(case1, GPIO.OUT)

GPIO.setup(case2, GPIO.OUT)

GPIO.setup(led1, GPIO.OUT)

GPIO.setup(led2, GPIO.OUT)
GPIO.setup(ledstock1, GPIO.OUT)

GPIO.setup(ledstock2, GPIO.OUT)


casier={"casier1":case1,"casier2":case2}

leds=[led1,led2]
ledstock=[ledstock1,ledstock2]
GPIO.output(case1, False)

GPIO.output(case2, False)
style="Helvetica 9 bold"

white="white"

lightgrey="lightgrey"

gray="gray"

menuButtonColor="#118098"

x=75

colorButton="#118098"

articleBackground="#D0D0D0"

textcolor="#26518A"

bleu="#26518A"

reference,date,designation,emplacement,quantiteMax,quantiteMin,quantiteT,prixUnitaire ,prixTotale,fournisseur_ref,nom_fournisseur,qte_R="ref","date","desig","place","Qte_Max","Qte_Min","Qte_T","PU","PT","ref_F","nom_F","qte_R"

db=DataBase()

class GestionStock(tk.Tk):

    def __init__(self):

        super().__init__()

        

        self.geometry("900x580")

        self.resizable(False,False)

        self.title("Gestion de stock")

        self.p=Principale(self)

        

        

        self.p.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.cadre_menu=Cadre_menu(self)

        self.cadre_menu.pack(side=tk.BOTTOM, fill=tk.X)

        

        self.principal=tk.Button(self.cadre_menu,text="Principal", bg=menuButtonColor, font=style,

                                state="disabled",command=self.showPrincipale)

        self.principal.grid(row=0, column=1, padx=10, pady=20)

        self.article = tk.Button(self.cadre_menu, text="Reference", bg=menuButtonColor, font=style,

                                 command=self.showArtcicle)

        self.article.grid(row=0, column=2, padx=10, pady=20)   

        self.boutton_fourniseur = Button(self.cadre_menu, text="Fourniseur", bg=menuButtonColor, font=style,

                               command=self.showFournisseur )

        self.boutton_fourniseur.grid(row=0, column=3, padx=10, pady=20)

        self.boutton_historique = Button(self.cadre_menu, text="Historique", bg=menuButtonColor, font=style,

                               command=self.showHistorique )

        self.boutton_historique.grid(row=0, column=5, padx=10, pady=20)

        self.boutton_agent = Button(self.cadre_menu, text="Agent", bg=menuButtonColor, font=style,

                               command=self.showAgent )

        self.boutton_agent.grid(row=0, column=4, padx=10, pady=20)

        self.article_frame=Article(self)

        self.fourniseur_frame=Fournisseur(self)

        self.historique_frame=Historique(self)

        self.agent_frame=Agent(self)

        

            



    def showArtcicle(self):
        try:
            _username,_password=self.login_dialog()
            row=db.login(username=_username,password=_password)
            print(row)
            if _username==row[0] and _password==row[1]:
                

                self.p.forget()

                self.fourniseur_frame.forget()

                self.article_frame.pack(fill=tk.BOTH, expand=True)

                self.historique_frame.forget()

                self.agent_frame.forget()

                self.boutton_agent.configure(state="active")

                self.principal.configure(state="active")

                self.article.config(state="disabled")

                self.boutton_fourniseur.config(state="active")

                self.boutton_historique.config(state="active")

                self.article_frame.actualiser_liste()
            else :
                self.showPrincipale()
        except Exception as e:
            print("erreur")
    def showPrincipale(self):

        self.article_frame.forget()

        self.p.pack(fill=tk.BOTH, expand=True)

        self.fourniseur_frame.forget()

        self.agent_frame.forget()

        self.boutton_agent.configure(state="active")

        self.article.configure(state="active")

        self.principal.config(state="disabled")

        self.boutton_historique.config(state="active")

        self.historique_frame.forget()
    def login_dialog(self):
        _username = simpledialog.askstring("Login", "Enter your username:", parent=self)
        if _username:
            _password = simpledialog.askstring("Password", "Enter your password:", parent=self, show='*')
            if _password:
                # Here you can perform your authentication logic
                print("Username:", _username)
                print("Password:", _password)
            else:
                print("Password not provided.")
        else:
            print("Username not provided.")
        return _username,_password
       


        

    def showFournisseur(self):
        try:
            _username,_password=self.login_dialog()
            row=db.login(username=_username,password=_password)
            print(row)
            if _username==row[0] and _password==row[1]:
                

                self.article_frame.forget()

                self.p.forget()

                self.historique_frame.forget()

                self.fourniseur_frame.pack(fill=tk.BOTH, expand=True)

                self.agent_frame.forget()

                self.boutton_agent.configure(state="active")

            

                self.article.configure(state="active")

                self.principal.config(state="active")

                self.boutton_fourniseur.configure(state="disabled")

                self.boutton_historique.config(state="active")
                self.fourniseur_frame.actualiser_liste()
            else :
                self.showPrincipale()
        except Exception as e:
            print("erreur")


    def showHistorique(self):
        try:
            _username,_password=self.login_dialog()
            row=db.login(username=_username,password=_password)
            print(row)
            if _username==row[0] and _password==row[1]:
                
                self.article_frame.forget()

                self.p.forget()

                self.fourniseur_frame.forget()

                self.historique_frame.pack(fill=tk.BOTH, expand=True)

                self.agent_frame.forget()

                self.boutton_agent.configure(state="active")

            

                self.article.configure(state="active")

                self.principal.config(state="active")

                self.boutton_fourniseur.configure(state="active")

                self.boutton_historique.configure(state="disabled")
                self.historique_frame.actualiser_liste()
            else :
                self.showPrincipale()
        except Exception as e:
            print("erreur")

    def showAgent(self):
        try:
            _username,_password=self.login_dialog()
            row=db.login(username=_username,password=_password)
            print(row)
            self.fourniseur_frame.actualiser_liste()
            if _username==row[0] and _password==row[1]:
                
                self.article_frame.forget()

                self.p.forget()

                self.fourniseur_frame.forget()

                self.historique_frame.forget()

                self.agent_frame.pack(fill=tk.BOTH, expand=True)

            

                self.article.configure(state="active")

                self.principal.config(state="active")

                self.boutton_fourniseur.configure(state="active")

                self.boutton_agent.configure(state="disabled")

                self.boutton_historique.configure(state="active")
                self.agent_frame.actualiser_liste()
            else :
                self.showPrincipale()
        except Exception as e:
            print("erreur")

class Principale (tk.Frame):

    def __init__(self, parent,):

        super().__init__(parent, height=480,width=900,)

        self.left_frame = tk.Frame(self, bg=gray, width=200, height=480)

        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self, bg=lightgrey, width=500, height=550)

        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        

        project_dossier = os.path.dirname(__file__)  

        self.image_path = os.path.join(project_dossier, "icone.png")

        self.canvas = tk.Canvas(self.left_frame, width=90, height=90, bg="gray")

        self.canvas.grid(row=0, column=0, columnspan=2, padx=50, pady=10,ipadx=2,ipady=2)

        self.circle = self.canvas.create_oval(0, 0, 100, 100, fill="gray")

        self.image = PhotoImage(file=self.image_path)

        self.canvas.create_image(50, 50, image=self.image)

        self.canvas.image = self.image



        self.label_nom_agent = Label(self.left_frame, text="Nom de l'agent:", bg="grey", fg="white", font=style)

        self.label_nom_agent.grid(row=1, column=0, padx=10, pady=20, sticky="w")

        self.champ_nom_agent = Entry(self.left_frame,font=style)

        self.champ_nom_agent.grid(row=1, column=1, padx=10, pady=20)



        self.label_matricule = Label(self.left_frame, text="Matricule:", bg="grey", fg="white", font=style)

        self.label_matricule.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.champ_matricule = Entry(self.left_frame,font=style)

        self.champ_matricule.grid(row=2, column=1, padx=10, pady=10)

        self.label_password = Label(self.left_frame, text="Mot de passe", bg="grey", fg="white", font=style)

        self.label_password.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.champ_password = Entry(self.left_frame,show=".",font=style)

        self.champ_password.grid(row=3, column=1, padx=10, pady=10)

        self.B_valider= tk.Button(self.left_frame, text="Valider", bg="#26518A", font=("bold"), fg="white",command=self.loginAgent)

        self.B_valider.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.img = PhotoImage(file='logo.png')



        self.logo_label = Label(self.right_frame,image=self.img  )

        self.logo_label.grid(row=0, column=3, columnspan=4, padx=130, pady=5)





        self.title = Label(self.right_frame, text="OUVERTURE AUTOMATIQUE",

                              font=("Helvetica", 16, "bold", "underline"), fg=textcolor, bg="lightgray")

        self.title.grid(row=0, column=0, columnspan=2, padx=20, pady=5)



        self.label_reference_article = Label(self.right_frame, text="Référence de l'article:", font=style,

                                                fg="black", bg="lightgrey")

        self.label_reference_article.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.champ_reference_article = Entry(self.right_frame)

        self.champ_reference_article.grid(row=1, column=1, padx=10, pady=10)

        

        self.label_quantite_sortie= Label(self.right_frame, text="Quantité à sortir:", font=style,

                                                fg="black", bg="lightgrey")

        self.label_quantite_sortie.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.champ_quantite_sortie= Entry(self.right_frame)

        self.champ_quantite_sortie.grid(row=2, column=1, padx=10, pady=10)



        self.label_Designation = Label(self.right_frame, text="Désignation:", font=style,

                                              fg="black", bg="lightgrey")

        self.label_Designation.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.champl_Designation =Label(self.right_frame, width=18,bg=articleBackground, borderwidth=1, relief="solid")

        self.champl_Designation.grid(row=3, column=1, padx=10, pady=10)



        self.label_Place_article = Label(self.right_frame, text="Emplacement de l'article:", font=style,

                                                fg="black", bg="lightgrey")

        self.label_Place_article.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.champ_Place_article =Label(self.right_frame, width=18,bg=articleBackground, borderwidth=1, relief="solid")

        self.champ_Place_article.grid(row=4, column=1, padx=10, pady=10)



        self.label_quantite_totale = Label(self.right_frame, text="Quantité Totale:", font=style,

                                              fg="black", bg="lightgrey")

        self.label_quantite_totale.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.champ_quantite_totale = Label(self.right_frame, width=18,bg=articleBackground, borderwidth=1, relief="solid")

        self.champ_quantite_totale.grid(row=5, column=1, padx=10, pady=10)



        self.label_quantite_minimale = Label(self.right_frame, text="Quantité minimale:", font=style,

                                                 fg="black", bg="lightgrey")

        self.label_quantite_minimale.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.champ_quantite_minimale =Label(self.right_frame, width=18,bg=articleBackground, borderwidth=1, relief="solid")

        self.champ_quantite_minimale.grid(row=6, column=1, padx=10, pady=10)



        self.label_quantite_restante = Label(self.right_frame, text="Quantité restante:", font=style,

                                                fg="black", bg="lightgrey")

        self.label_quantite_restante .grid(row=7, column=0, padx=10, pady=10, sticky="w",)

        self.champ_quantite_restante  = Label(self.right_frame, width=18, borderwidth=1, relief="solid",bg="lightgrey")

        self.champ_quantite_restante.grid(row=7, column=1, padx=10, pady=10)

        self.champ_reference_article.bind("<FocusOut>", lambda event: self.db_article_details())







        self.B_ouvrir = tk.Button(self.right_frame, state='disabled',text="Ouvrir Tiroir", bg=bleu, font=("bold"),command=self.enregistrer_sortie)

        self.B_ouvrir.grid(row=8, column=0, columnspan=2, padx=30, pady=20, ipadx=25, ipady=5)



        self.annuler_ouvrir = tk.Button(self.right_frame, text="Annuler", bg=textcolor, font=("bold"),command=self.annuler)

        self.annuler_ouvrir.grid(row=8, column=2, columnspan=2, padx=30, pady=20, ipadx=25, ipady=5)
        





    def enregistrer_sortie(self):              
        nom_agent = self.champ_nom_agent.get()

        matricule = self.champ_matricule.get()

        reference_article = self.champ_reference_article.get()

        quantite_sortie = self.champ_quantite_sortie.get()

        try:
            place=self.champ_Place_article.cget("text")
            if db.chek_manque(reference=reference_article,qt_r=int(quantite_sortie))==False:


                db.retirer_article(id_article=reference_article, id_agent=matricule , quantite_sortir=quantite_sortie)

                

                qte=db.recuper_qte_restante(ref=reference_article)

                nv_qte=qte-int(quantite_sortie)

                db.update_qte_restante(ref=reference_article,qte=str(nv_qte))
                

                self.ouvrir(str(place))
                db.historique()
                self.supInfoAgent()
            else :
                self.champ_quantite_restante.config(bg="red")
                
                self.blink(str(place))
                messagebox.showerror(title="failed",message=" insufficient stock")
                

            self.champ_matricule.config(state="normal")
            self.champ_password.config(state="normal")
            self.champ_nom_agent.config(state="normal")
            self.annuler()
            self.B_ouvrir.config(state='disabled')

        except():

            print("erreur")

            self.supInfoAgent()

    def db_article_details(self):

        reference_article = self.champ_reference_article.get()

        details=db.db_article_details(reference_article)

        if details:

                    adresse, place ,Qte_max, Qte_min,Qte_Totale,quantiteRestante = details
                    

                    """self.champ_AdresseIP_article.delete(0, tk.END)

                    self.champ_AdresseIP_article.insert(0, adresse)"""
                    if (Qte_min >quantiteRestante):
                        
                        self.champ_quantite_restante.config(bg="red")
                        
                    else :
                        self.champ_quantite_restante.config(bg="green")
                    self.update()  
                    print(type(str(Qte_max)))

                    self.champ_Place_article.config(text="",)

                    self.champ_Place_article.config(text=place)

                    self.champ_quantite_totale.config(text="",)

                    self.champ_quantite_totale.config(text=f"{Qte_Totale}")

                    self.champ_quantite_minimale.config(text="",)

                    self.champ_quantite_minimale.config(text= f"{Qte_min}")

                    self.champl_Designation.config(text="")

                    self.champl_Designation.config(text=adresse)

                    self.champ_quantite_minimale.config(text="")

                    self.champ_quantite_minimale.config(text=f'{Qte_min}')

                    self.champ_quantite_restante.config(text="")

                    self.champ_quantite_restante.config(text=f'{quantiteRestante}')

                    #if Qte_min

                    

    def annuler(self):

       self.champ_Place_article.config(text="",)

       self.champ_quantite_totale.config(text="",)

       self.champ_quantite_minimale.config(text="",)

       self.champl_Designation.config(text="")

       self.champ_quantite_minimale.config(text="")
       self.champ_quantite_restante.config(bg=lightgrey)
       self.champ_quantite_restante.config(text="")

       self.champ_nom_agent.delete(0,tk.END)

       self.champ_matricule.delete(0,tk.END)

       self.champ_password.delete(0,tk.END)

       self.champ_quantite_sortie.delete(0,tk.END)

       self.champ_reference_article.delete(0,tk.END)
       self.B_ouvrir.config(state='disabled')
       self.supInfoAgent()

    def supInfoAgent(self):

       self.champ_nom_agent.delete(0,tk.END)

       self.champ_matricule.delete(0,tk.END)

       self.champ_password.delete(0,tk.END)

        

    def getinfoAgent(self):

        n=self.champ_nom_agent.get()

        m=self.champ_matricule.get()

        mot=self.champ_password.get()

        return (m,n,mot)

    

    def loginAgent(self):

        try :

            print(self.getinfoAgent())

            print(db.chercheUnAgent(self.champ_matricule.get()))

            if self.getinfoAgent()==db.chercheUnAgent(self.champ_matricule.get()):

                print("ok")

                self.B_ouvrir.configure(state='active')
                self.champ_matricule.config(state="disabled")
                self.champ_password.config(state="disabled")
                self.champ_nom_agent.config(state="disabled")



            else:

                

                self.B_ouvrir.configure(state='disabled')

                self.supInfoAgent()

                messagebox.showerror("Agent non authorisé")

            

            

        except():

            messagebox.showerror("erreur")
    def blink(self,case):
      for i ,j ,z in zip (casier.keys(), casier.values(), ledstock) :

              print(i)
              if i==case:

                      

                      GPIO.output(z, True)
                      

                      print("blink")

                      print(z)
                      print(" no blink")
                      time.sleep(4)
                      GPIO.output(z, False)
                      

                      break
    
    def ouvrir(self,case):
      print("cc")
      for i ,j ,z in zip (casier.keys(), casier.values(), leds) :
              print(i)

              if i==case:

                      GPIO.output(j, True)

                      GPIO.output(z, True)

                      print("ouvrir")

                      print(z)

                      time.sleep(10)

                      GPIO.output(j, False)

                      GPIO.output(z, False)

                      break


  

class Cadre_menu(tk.Frame):

    def __init__(self, parent,):

        super().__init__(parent,bg=white,height=100,width=900,)





class Fournisseur(tk.Frame):

    def __init__(self, parent,):

        super().__init__(parent,height=480,width=900, bg=articleBackground)

       

        self.titre = Label(self, text="BASE DES DONNEES DES FOURNISEURS", font=("Helvetica", 17, "bold", "underline"), fg="brown", bg=articleBackground).pack(pady=17)

        """self.AA = Label(self, text="AJOUT_FOURNISEURS", font=("Helvetica", 14, "bold", "underline"), fg=colorButton, bg=articleBackground)

        self.AA.place(relx=0.15,rely=0.14)"""

        self.AA = Label(self, text="Liste des fournisseurs", font=("Helvetica", 15, "bold", "underline"), fg=colorButton, bg=articleBackground).place (relx=0.55,rely=0.14)

        self.label_nom = Label(self, text="Nom:", font=style, fg="#234349", bg=articleBackground)

        self.label_nom.place(relx=0.01, rely=0.35, anchor="w")

        self.champ_nom= Entry(self, width=20)

        self.champ_nom.place(relx=0.23, rely=0.35, anchor="w")



        self.label_ref = Label(self, text="Reférence:", font=style, fg="#234349", bg=articleBackground)

        self.label_ref.place(relx=0.01, rely=0.25, anchor="w")

        self.champ_ref = Entry(self, width=20)

        self.champ_ref.place(relx=0.23, rely=0.25, anchor="w")



        self.label_adresse = Label(self, text="Adresse:", font=style, fg="#234349", bg=articleBackground)

        self.label_adresse.place(relx=0.01, rely=0.45, anchor="w")

        self.champ_adresse = Entry(self, width=20)

        self.champ_adresse.place(relx=0.23, rely=0.45, anchor="w")



        self.label_telephone = Label(self, text="Téléphone:", font=style, fg="#234349", bg=articleBackground)

        self.label_telephone.place(relx=0.01, rely=0.55, anchor="w")

        self.champ_telephone = Entry(self, width=20)

        self.champ_telephone.place(relx=0.23, rely=0.55, anchor="w")

        

        self.bouton_ajouter = tk.Button(self , text="Enregistrer", bg=colorButton, font=style,width=17,command=self.ajouter_fourni)

        self.bouton_ajouter.place(relx=0.02, rely=0.68, anchor="w")

        

        self.bouton_supprimer = tk.Button(self , text="Supprimer", bg=colorButton, font=style,width=17)

        self.bouton_supprimer.place(relx=0.19, rely=0.68, anchor="w")

        

        self.bouton_modifier = tk.Button(self , text="Modifier", bg=colorButton, font=style,width=17)

        self.bouton_modifier.place(relx=0.19, rely=0.78, anchor="w")

        

        self.bouton_chercher = tk.Button(self , text="Chercher", bg=colorButton, font=style,width=17)

        self.bouton_chercher.place(relx=0.02, rely=0.78, anchor="w")

        ref, nom, adresse, tel = 'Référence', 'Nom', 'Adresse', 'Téléphone'



        self.tree_fournisseur = Treeview(self, columns=(ref,nom, adresse, tel), height=15)



        self.tree_fournisseur.place(relx=0.42, rely=0.23)



        self.tree_fournisseur.heading('#0', text='')

        self.tree_fournisseur.heading(ref, text=ref)



        self.tree_fournisseur.heading(nom, text=nom)



        self.tree_fournisseur.heading(adresse, text=adresse)



        self.tree_fournisseur.heading(tel, text=tel)

        

        x=130

        self.tree_fournisseur.column('#0', width=25)

        self.tree_fournisseur.column(ref, width=x)

        self.tree_fournisseur.column(nom, width=x) 

        self.tree_fournisseur.column(adresse, width=x) 

        self.tree_fournisseur.column(tel, width=x)

        self.actualiser_liste()  

    def getFournisseur(self):

        nom=self.champ_nom.get()

        ref=self.champ_ref.get()

        adr=self.champ_adresse.get()

        tel=self.champ_telephone.get()

        return nom, ref,adr,tel

    def ajouter_fourni(self):

        try:

            nom,ref,adr,tel=self.getFournisseur()

            db.ajouter_fournisseur(reference=ref,nom=nom,adresse=adr,telephone=tel)

            self.vide_champ()

            self.actualiser_liste()

        except():

            print("erreur")

            self.vide_champ

    def vide_champ(self):

        self.champ_nom.delete(0,tk.END)

        self.champ_ref.delete(0,tk.END)

        self.champ_adresse.delete(0,tk.END)

        self.champ_telephone.delete(0,tk.END)

    def actualiser_liste(self):

        children = self.tree_fournisseur.get_children()

        for child in children:

            self.tree_fournisseur.delete(child)

        fournisseur = db.list_fournisseur()

        print(fournisseur)

        for fr in fournisseur:

            self.tree_fournisseur.insert("", "end", values=fr)





class Agent(tk.Frame):

    def __init__(self, parent,):

        super().__init__(parent,height=480,width=900, bg=articleBackground)

       

        self.titre = Label(self, text="BASE DES DONNEES DES AGENTS", font=("Helvetica", 17, "bold", "underline"), fg="brown", bg=articleBackground).pack(pady=17)

        """self.AA = Label(self, text="AJOUT_Agent", font=("Helvetica", 14, "bold", "underline"), fg=colorButton, bg=articleBackground)

        self.AA.place(relx=0.15,rely=0.14)"""

        self.AA = Label(self, text="Liste des agents", font=("Helvetica", 15, "bold", "underline"), fg=colorButton, bg=articleBackground).place (relx=0.55,rely=0.14)

        self.label_nom = Label(self, text="Nom:", font=style, fg="#234349", bg=articleBackground)

        self.label_nom.place(relx=0.01, rely=0.25, anchor="w")

        self.champ_nom= Entry(self, width=20)

        self.champ_nom.place(relx=0.23, rely=0.25, anchor="w")



        self.label_Matricule = Label(self, text="Matricule:", font=style, fg="#234349", bg=articleBackground)

        self.label_Matricule.place(relx=0.01, rely=0.35, anchor="w")

        self.champ_Matricule = Entry(self, width=20)

        self.champ_Matricule.place(relx=0.23, rely=0.35, anchor="w")



        self.label_mot_de_passe = Label(self, text="mot de passe :", font=style, fg="#234349", bg=articleBackground)

        self.label_mot_de_passe.place(relx=0.01, rely=0.45, anchor="w")

        self.champ_mot_de_passe = Entry(self, width=20)

        self.champ_mot_de_passe.place(relx=0.23, rely=0.45, anchor="w")



        self.label_confirme = Label(self, text="confirme mot de passe :", font=style, fg="#234349", bg=articleBackground)

        self.label_confirme.place(relx=0.01, rely=0.55, anchor="w")

        self.champ_confirme = Entry(self, width=20)

        self.champ_confirme.place(relx=0.23, rely=0.55, anchor="w")

        

        self.bouton_ajouter = tk.Button(self , text="Enregistrer", bg=colorButton, font=style,width=17,command=self.ajout_agent)

        self.bouton_ajouter.place(relx=0.02, rely=0.68, anchor="w")

        

        self.bouton_supprimer = tk.Button(self , text="Supprimer", bg=colorButton, font=style,width=17)

        self.bouton_supprimer.place(relx=0.19, rely=0.68, anchor="w")

        

        self.bouton_modifier = tk.Button(self , text="Modifier", bg=colorButton, font=style,width=17)

        self.bouton_modifier.place(relx=0.19, rely=0.78, anchor="w")

        matricule,nom,mots_pass='Matricule','Nom','Motde pass'

        self.bouton_chercher = tk.Button(self , text="Chercher", bg=colorButton, font=style,width=17)

        self.bouton_chercher.place(relx=0.02, rely=0.78, anchor="w")

                

        self.tree_agent = ttk.Treeview(self, columns=(matricule,nom, mots_pass))

        self.tree_agent.place(relx=0.42, rely=0.23)

        xa=150

        self.tree_agent.heading('#0', text="")
        self.tree_agent.heading(matricule, text=matricule)

        self.tree_agent.heading(nom, text=nom)

        self.tree_agent.heading(mots_pass, text=mots_pass)



        

        self.tree_agent.column('#0', width=0)

        self.tree_agent.column(nom, width=xa)

        self.tree_agent.column(mots_pass, width=xa)
        self.actualiser_liste()

    def vider(self):                    

        self.champ_nom.config(text="",)

        self.champ_mot_de_passe.config(text="")

        self.champ_confirme.config(text="",)

        self.champ_Matricule.config(text="",)



    def get_req(self):

        n=self.champ_nom.get()

        m=self.champ_Matricule.get()

        mo=self.champ_mot_de_passe.get()

        return n,m,mo

    def ajout_agent(self):

        n,m,mo=self.get_req()

        confirm=self.champ_confirme.get()

        try:

            if confirm==mo:

                db.ajouter_agent(m,n,mo)

                self.vider()
                self.actualiser_liste()



            else :

                messagebox.showerror("mot de pass invalide ")

                self.vider()



        except():

            print("erreur")

    def actualiser_liste(self):
       
        for i in self.tree_agent.get_children():
            self.tree_agent.delete(i)

        agents = db.list_agent()
        for agent in agents:
             self.tree_agent.insert("", "end", values=agent)


    def sup_agent(self):

        pass

    def cherch_agent(self):

        pass

    def edit_agent(self):

        pass



class Article(tk.Frame):

    def __init__(self, parent,):

        super().__init__(parent,height=480,width=900, bg=articleBackground)

        self.titre = Label(self, text="BASE DES DONNEES DES ARTICLES", font=("Helvetica", 17, "bold", "underline"), fg="brown", bg=articleBackground)

        self.titre.pack(pady=17)

        self.AA = Label(self, text="AJOUT_ARTICLE", font=("Helvetica", 14, "bold", "underline"), fg=colorButton, bg=articleBackground)

        self.AA.place(relx=0.15,rely=0.14)

        self.AA = Label(self, text="Liste des articles ", font=("Helvetica", 15, "bold", "underline"), fg=colorButton, bg=articleBackground).place(relx=0.6,rely=0.14)

        self.label_reference = Label(self, text="Référence:", font=style, fg="#234349", bg=articleBackground)

        self.label_reference.place(relx=0.01, rely=0.25, anchor="w")

        self.champ_reference = Entry(self, width=20)

        self.champ_reference.place(relx=0.23, rely=0.25, anchor="w")



        self.label_designation = Label(self, text="Désignation:", font=style, fg="#234349", bg=articleBackground)

        self.label_designation.place(relx=0.01, rely=0.32, anchor="w")

        self.champ_designation =  Entry(self, width=20)

        self.champ_designation.place(relx=0.23, rely=0.32, anchor="w")

        self.label_place = Label(self, text="Place:", font=style, fg="#234349", bg=articleBackground)

        self.label_place.place(relx=0.01, rely=0.39, anchor="w")

        self.champ_place = ttk.Combobox(

        self,

        state="readonly",
 
        width=20,

        values=['casier1','casier2'])

        self.champ_place.place(relx=0.23, rely=0.39, anchor="w")
        self.champ_place.bind("<<ComboboxSelected>>", self.getSelectedItem)

        self.label_quantite_tot = Label(self, text="Quantité maximale:", font=style, fg="#234349", bg=articleBackground)

        self.label_quantite_tot.place(relx=0.01, rely=0.46, anchor="w")

        self.champ_quantite_tot = Entry(self, width=20)

        self.champ_quantite_tot.place(relx=0.23, rely=0.46, anchor="w")

        self.label_quantite_min = Label(self , text="Quantité minimale:", font=style, fg="#234349", bg=articleBackground)

        self.label_quantite_min.place(relx=0.01, rely=0.53, anchor="w")

        self.champ_quantite_min = Entry(self , width=20)

        self.champ_quantite_min.place(relx=0.23, rely=0.53, anchor="w")


        self.label_prix_unitaire = Label(self , text="Prix Unitaire:", font=style, fg="#234349", bg=articleBackground)

        self.label_prix_unitaire.place(relx=0.01, rely=0.67, anchor="w")       

        self.champ_prix_unitaire = Entry(self , width=20)

        self.champ_prix_unitaire.place(relx=0.23, rely=0.67, anchor="w")       

        

        self.label_prix_totale = Label(self , text="Prix Totale:", font=style, fg="#234349", bg=articleBackground)

        self.label_prix_totale.place(relx=0.01, rely=0.74, anchor="w")       

        self.champ_prix_totale = Label(self, width=18,bg=articleBackground, borderwidth=1, relief="solid")

        self.champ_prix_totale.place(relx=0.23, rely=0.74, anchor="w")         



        self.label_fournisseur = Label(self , text="Fournisseur:", font=style, fg="#234349", bg=articleBackground)

        self.label_fournisseur .place(relx=0.01, rely=0.83, anchor="w")

        self.data=db.recupere_fournisseur()
        
        print("***********")

        self.champ_fournisseur = ttk.Combobox(

        self,

        state="readonly",
 
        width=20,

        values=list(self.data.values()))
      

        
        self.champ_fournisseur .bind("<<ComboboxSelected>>", self.getSelectedItem)



        self.champ_fournisseur .place(relx=0.23, rely=0.83, anchor="w")         

        self.bouton_ajouter = tk.Button(self , text="Ajouter", bg=colorButton, font=style,width=10,command=self.ajouter_article)

        self.bouton_ajouter.place(relx=0.48, rely=0.75, anchor="w")





        self.bouton_suprimer = tk.Button(self , text="Supprimer", bg=colorButton, font=style,width=10)

        self.bouton_suprimer.place(relx=0.58, rely=0.75, anchor="w")

        

        self.bouton_chercher = tk.Button(self , text="Chercher", bg=colorButton, font=style,width=10)

        self.bouton_chercher.place(relx=0.68, rely=0.75, anchor="w")

        

        self.bouton_modifier = tk.Button(self , text="Modifier", bg=colorButton, font=style,width=10)

        self.bouton_modifier.place(relx=0.78, rely=0.75, anchor="w")

        self.tree_article = ttk.Treeview(self, columns=(reference,date,designation,emplacement,quantiteMax,quantiteMin,quantiteT,prixUnitaire ,prixTotale,fournisseur_ref,nom_fournisseur,qte_R))

        self.tree_article.place(relx=0.42, rely=0.23)

        

        self.tree_article.heading('#0', text="")

        self.tree_article.heading(reference, text=reference)

        self.tree_article.heading(date, text=date)

        self.tree_article.heading(designation, text=designation)

        self.tree_article.heading(emplacement, text=emplacement)

        self.tree_article.heading(quantiteMax, text=quantiteMax)

        self.tree_article.heading(quantiteMin, text=quantiteMin)

        self.tree_article.heading(quantiteT, text=quantiteT)

        self.tree_article.heading(prixUnitaire , text=prixUnitaire )

        self.tree_article.heading(prixTotale, text=prixTotale)

        self.tree_article.heading(fournisseur_ref, text=fournisseur_ref)

        self.tree_article.heading(nom_fournisseur, text=nom_fournisseur)

        

        self.tree_article.heading(qte_R, text=qte_R)

        x=50

        y=20

        self.tree_article.column('#0', width=0, )

        self.tree_article.column(reference, width=x, )

        self.tree_article.column(date, width=x+10, ) 

        self.tree_article.column(designation, width=x,)

        self.tree_article.column(emplacement, width=x) 

        self.tree_article.column(quantiteMax, width=x-y) 

        self.tree_article.column(quantiteMin, width=x-y)

        self.tree_article.column(quantiteT, width=x-y) 

        self.tree_article.column(prixUnitaire, width=x-y)

        self.tree_article.column(prixTotale, width=x-y)

        self.tree_article.column(fournisseur_ref, width=x) 

        self.tree_article.column(nom_fournisseur, width=x)

        self.tree_article.column(qte_R, width=x)

        self.actualiser_liste()
    def ouvrir(self,case):
      print("cc")
      for i ,j ,z in zip (casier.keys(), casier.values(), leds) :
              print(i)

              if i==case:

                      GPIO.output(j, True)

                      GPIO.output(z, True)

                      print("ouvrir")

                      print(z)

                      time.sleep(10)

                      GPIO.output(j, False)

                      GPIO.output(z, False)

                      break



         

    def ajouter_article(self):
        try:
            referenceArticle = self.champ_reference.get()

            designation = self.champ_designation.get()

            place = self.champ_place.get()

            qte_max = int(self.champ_quantite_tot.get())  # Convert to int or float

            qte_min = int(self.champ_quantite_min.get())  # Convert to int or float

            qte_total = int(self.champ_quantite_tot.get())  # Convert to int or float

            prix_unitaire = int(self.champ_prix_unitaire.get())  # Convert to float

            prix_total = qte_total * prix_unitaire  # Calculate without eval

            print(prix_total)

            self.champ_prix_totale.config(text=f'{prix_total}')

            fournisseur=self.champ_fournisseur.get()

            db.ajouter_nouveau_article(reference=referenceArticle,designation=designation,emplacement=place,quantiteMax=str(qte_max),quantiteMin=str(qte_min),quantiteT=str(qte_total),prixUnitaire=str(prix_unitaire),fournisseur_ref=fournisseur)

            self.actualiser_liste()
            self.ouvrir(place)
            self.vide_champ()
        except Exception as e:
            print(f"erreur : {e}")
    def getSelectedItem(self, eventObject):
        pass
        """selected_name = self.champ_fournisseur.get() 
        selected_identifier = self.data 
        print("Selected Name:", selected_name)
        print("Selected Identifier:", selected_identifier)
"""
    def vide_champ(self):
        self.champ_reference.delete(0,tk.END)
        self.champ_designation.delete(0,tk.END)
        self.champ_place.delete(0,tk.END)
        self.champ_quantite_tot.delete(0,tk.END)
        self.champ_prix_unitaire.delete(0,tk.END)
        self.champ_prix_totale.config(text='')
        self.champ_fournisseur.delete(0,tk.END)
    def actualiser_liste(self):

        children = self.tree_article.get_children()

        for child in children:

            self.tree_article.delete(child)

        articles_disponible = db.listeArticle()

        for article in articles_disponible:

            self.tree_article.insert("", "end", values=article)

class Historique(tk.Frame):

    def __init__(self, parent,):

        super().__init__(parent, height=480,width=900,bg=articleBackground)
        Nom_agent,Matricule,Reference,Qte_Sortie='Nom_agent', 'Matricule','Reference', 'Qte_Sortie'

        self.AA = tk.Label(self ,text="Historique", font=("Helvetica", 25, "bold", "underline"), fg=colorButton, bg=lightgrey).place(relx=0.4,rely=0.01)

        self.tree_historique =Treeview(self, columns=('id','Nom_agent', 'Matricule','Reference', 'Date','Qté_Sortie'),height=18)

        self.tree_historique.place(relx=0.17, rely=0.12)

        self.bouton_vider = Button(self , text="Vider historique", bg=colorButton, font=("Helvetica", 12, "bold"),width=17,command=self.sup_historique )

        self.bouton_vider.place(relx=0.4, rely=0.94, anchor="w")

        self.tree_historique.heading('#0', text='')

        self.tree_historique.heading('Nom_agent', text='Nom_agent')

        self.tree_historique.heading('Matricule', text='Matricule')

        self.tree_historique.heading('Reference', text='Reference')
        self.tree_historique.heading('Date', text='Date')

        self.tree_historique.heading('Qté_Sortie', text='Qté_Sortie')

        x=125

        self.tree_historique.column('#0', width=0) 
        self.tree_historique.column('id', width=20) 
        self.tree_historique.column('Nom_agent', width=x) 

        self.tree_historique.column('Matricule', width=x)
        self.tree_historique.column('Date', width=x) 

        self.tree_historique.column('Reference', width=x) 
        self.tree_historique.column('Date', width=x) 

        self.tree_historique.column('Qté_Sortie', width=x)

        self.actualiser_liste()

    

    def actualiser_liste(self):

        children = self.tree_historique.get_children()

        for child in children:

            self.tree_historique.delete(child)

        liste_hitorique = db.historique()
        print("liste_hitorique")
        print(liste_hitorique)

        for historique in liste_hitorique :

            self.tree_historique.insert("", "end", values=historique)
    def sup_historique (self):
        db.vide_historique()
        self.actualiser_liste()
if __name__=="__main__":

    app=GestionStock()

    app.mainloop()

