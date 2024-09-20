import mysql.connector

class DataBase:



    def __init__(self):

        self.conn = mysql.connector.connect(

            host="127.0.0.1",  # Adresse de votre serveur MySQL

            user="root",  # Nom d'utilisateur MySQL

            password="",  # Mot de passe MySQL

            database="data2"  # Nom de la base de données

        )

        self.cursor = self.conn.cursor()

        self.cursor.execute("""

           CREATE TABLE IF NOT EXISTS admin(

               username VARCHAR(255) UNIQUE,


               password VARCHAR(255)
           )

        """)
        

        self.cursor.execute("""

           CREATE TABLE IF NOT EXISTS fournisseurs(

               fournisseur_ref VARCHAR(255) PRIMARY KEY,

               nom TEXT,

               adresse VARCHAR(255),

               telephone VARCHAR(20)

           )

        """)

        self.cursor.execute("""

           CREATE TABLE IF NOT EXISTS agents (

               matricule VARCHAR(255) PRIMARY KEY,

                nom VARCHAR(255),

                mot_de_pass VARCHAR(255)

           )

        """)
        

        self.cursor.execute("""

                CREATE TABLE IF NOT EXISTS articles (

                    reference VARCHAR(255) PRIMARY KEY,

                    date DATE,

                    designation TEXT,

                    emplacement TEXT,

                    quantiteMin INT,

                    quantiteMax INT,

                    quantiteT INT,

                    prixUnitaire INT,

                    prixTotale INT, 

                    fournisseur_ref VARCHAR(255),

                    nom_fournisseur VARCHAR(255),

                    quantiteRestante INT,

                    FOREIGN KEY (fournisseur_ref) REFERENCES fournisseurs (fournisseur_ref)

                )

        """)

        self.cursor.execute("""

           CREATE TABLE IF NOT EXISTS historique (

               id INT PRIMARY KEY AUTO_INCREMENT,

               nomAgent VARCHAR(255),

              

               idArticle VARCHAR(255),

               idAgent VARCHAR(255),

               datetimeEvent DATETIME,

               quantiteSortir INT,

               FOREIGN KEY (idArticle) REFERENCES articles(reference),

               FOREIGN KEY (idAgent) REFERENCES agents(matricule)

           )

        """)



    def retirer_article(self, id_article, id_agent, quantite_sortir):

        try:

            self.cursor.execute("SELECT nom, matricule FROM agents WHERE matricule = %s", (id_agent,))

            agent_info = self.cursor.fetchone()

            nom_agent, id_agent= agent_info if agent_info else (None, None)

            



            

            self.cursor.execute("""

                INSERT INTO historique (idArticle, idAgent, nomAgent, datetimeEvent, quantiteSortir)

                VALUES (%s, %s, %s, NOW(), %s)""", (id_article, id_agent, nom_agent, quantite_sortir))



            self.conn.commit()

        except Exception as e:

           

            print(f"Erreur lors de la retrait du produit  : {e}")

            self.conn.rollback()

    



    def recuper_qte_restante(self, ref):

        try:

            

            requete = "SELECT quantiteRestante FROM articles WHERE reference = %s"

            

           

            self.cursor.execute(requete, (ref,))

            

          

            qte = self.cursor.fetchone()

            

            if qte:

                qte_restante = qte[0]

                print(f"Quantité restante pour la référence {ref}: {qte_restante}")

                return qte_restante

            else:

                print(f"Aucune quantité restante trouvée pour la référence {ref}")

                return None

                

        except Exception as e:

          

            print(f"Erreur lors de la récupération de la quantité restante : {e}")

            return None



    def update_qte_restante(self, qte, ref):

        try:

           

            requete = "UPDATE articles SET quantiteRestante=%s WHERE reference=%s"

            

           

            self.cursor.execute(requete, (qte, ref))

            

            self.conn.commit()

            print("Mise à jour de la quantité restante réussie.")

            

        except Exception as e:

           

            print(f"Erreur lors de la mise à jour de la quantité restante : {e}")

            self.conn.rollback() 

            

        



    def ajouter_article(self, reference,designation,emplacement,quantiteMax,quantiteMin,quantiteT,prixUnitaire,fournisseur_ref):

        try:

            self.cursor.execute("SELECT nom,fournisseur_ref FROM fournisseurs WHERE fournisseur_ref = %s", (fournisseur_ref,))

            fournisseur_info = self.cursor.fetchone()

            nom_fournisseur, fournisseur_ref = fournisseur_info if fournisseur_info else (None, None)

            prixTotale=int(prixUnitaire)*int(quantiteT)

            

            self.cursor.execute("""INSERT INTO articles (reference,date,designation,emplacement,quantiteMax,quantiteMin,quantiteT,prixUnitaire ,prixTotale,fournisseur_ref,nom_fournisseur)

                VALUES (%s,CURDATE(),%s,%s,%s,%s,%s, %s,%s,%s,%s)

                """,(reference,designation,emplacement,quantiteMax,quantiteMin,quantiteT,prixUnitaire,prixTotale,fournisseur_ref,nom_fournisseur))

            self.conn.commit() 

        except Exception as e:

            print("erreur")



    def ajouter_nouveau_article(self, reference,designation,emplacement,quantiteMax,quantiteMin,quantiteT,prixUnitaire,fournisseur_ref):

        try:

            self.cursor.execute("SELECT nom,fournisseur_ref FROM fournisseurs WHERE fournisseur_ref = %s", (fournisseur_ref,))

            fournisseur_info = self.cursor.fetchone()

            nom_fournisseur, fournisseur_ref = fournisseur_info if fournisseur_info else (None, None)

            prixTotale=str(int(prixUnitaire)*int(quantiteT))

            

            self.cursor.execute("""INSERT INTO articles (reference,date,designation,emplacement,quantiteMax,quantiteMin,quantiteT,prixUnitaire ,prixTotale,fournisseur_ref,nom_fournisseur,quantiteRestante)

                VALUES (%s,CURDATE(),%s,%s,%s,%s,%s, %s,%s,%s,%s,%s)

                """,(reference,designation,emplacement,quantiteMax,quantiteMin,quantiteT,prixUnitaire,prixTotale,fournisseur_ref,nom_fournisseur,quantiteMax))



            self.conn.commit() 

        except Exception as e:

            print(f"erreur{e}")

            

    def modifier_article(self, reference, designation, emplacement, quantiteMax, quantiteMin, quantiteT, prixUnitaire, fournisseur_ref):



        self.cursor.execute("SELECT nom, fournisseur_ref FROM fournisseurs WHERE fournisseur_ref = %s", (fournisseur_ref,))

        fournisseur_info = self.cursor.fetchone()

        nom_fournisseur, fournisseur_ref = fournisseur_info if fournisseur_info else (None, None)



        if nom_fournisseur is None:

            print(f"Fournisseur with ref {fournisseur_ref} not found.")

            return  

        prixTotale = int(prixUnitaire) * int(quantiteT)



        

        self.cursor.execute("""

            UPDATE articles

            SET designation = %s, emplacement = %s, quantiteMax = %s, quantiteMin = %s, quantiteT = %s,

                prixUnitaire = %s, prixTotale = %s, fournisseur_ref = %s, nom_fournisseur = %s

            WHERE reference = %s

        """, (designation, emplacement, quantiteMax, quantiteMin, quantiteT, prixUnitaire, prixTotale, fournisseur_ref, nom_fournisseur, reference))



        self.conn.commit()  

    

    def listeArticle(self):

        try:

            self.cursor.execute("SELECT * FROM articles")

            return self.cursor.fetchall()

        except():

            print("erreur")

    

    def db_article_details(self,reference_article):            

            try:

                

                requete = "SELECT designation,emplacement,quantiteMax,quantiteMin,quantiteT,quantiteRestante FROM articles WHERE reference = %s"

                self.cursor.execute(requete, (reference_article,))

                details = self.cursor.fetchone()  

                return details

            except mysql.connector.Error as e:

                print(f"Erreur lors de la récupération des détails de l'article: {e}")

   

    def supprimer_article(self, reference):

        try:

            self.cursor.execute("DELETE FROM articles WHERE articles.reference = %s",(reference,))

            self.conn.commit() 

        except():

            print(" arcticle non supprimé ")



   

    def ajouter_agent(self,matricule,nom,cle):

        try:

            self.cursor.execute("""INSERT INTO agents (matricule,nom,mot_de_pass)

                VALUES (%s,%s,%s)

                """,(matricule,nom,cle))



            self.conn.commit() 

        except Exception as e:

            print(f"erreur{e}")

    

    def supprimer_fournisseur(self, reference):

        try:

            self.cursor.execute("DELETE FROM fournisseurs WHERE fournisseur_ref= %s",(reference,))

            self.conn.commit() 

        except():

            print(" arcticle non supprimé ")

    

    def modifier_fournisseur(self, reference, nom, adresse, telephone):

        try:

            self.cursor.execute("""

                UPDATE fournisseurs

                SET nom = %s, adresse = %s, telephone = %s

                WHERE fournisseur_ref = %s

            """, (nom, adresse, telephone, reference))



            self.conn.commit()

        except Exception as e:

            print("An error occurred while modifying the supplier:", e)

    def ajouter_fournisseur(self, reference,nom,adresse,telephone):

        try:

            self.cursor.execute("""

                INSERT INTO fournisseurs (fournisseur_ref,nom,adresse,telephone)

                VALUES ( %s, %s, %s,%s)""", (reference,nom,adresse,telephone))



            self.conn.commit() 

        except Exception as e:

            print("fournisseur ajouté")

    def recupere_fournisseur(self):

        requete = "SELECT nom, fournisseur_ref FROM fournisseurs"

        try:

            self.cursor.execute(requete)

            fournisseurs = self.cursor.fetchall()

            

            dict_fournisseurs = {}  # Initialise un dictionnaire pour stocker les fournisseurs

            

            for fournisseur in fournisseurs:

                nom, ref = fournisseur

                dict_fournisseurs[nom] = ref  # Ajoute le nom du fournisseur comme clé et la référence comme valeur

            

            if dict_fournisseurs:

                print("Liste des fournisseurs récupérée avec succès.")

                return dict_fournisseurs

            else:

                print("Aucun fournisseur trouvé dans la base de données.")

                return {"": ""}

                    

        except Exception as e:

            print(f"Erreur lors de la récupération de la liste des fournisseurs : {e}")

            return {"": ""}





    def historique(self):

        try:



            self.cursor.execute("SELECT * FROM historique")

            return self.cursor.fetchall()

        except():

            print("non valide ")


    def chercheUnAgent(self,matricule):

        try:

            self.cursor.execute("SELECT matricule,nom,mot_de_pass FROM agents where agents.matricule=%s ",(matricule,))

            return self.cursor.fetchone()

        except():

            print("erreur")

    def list_fournisseur(self):

        requete = "SELECT * FROM fournisseurs"

        try:

            self.cursor.execute(requete)

            fournisseurs = self.cursor.fetchall()

            print("Liste des fournisseurs récupérée avec succès.")

            return fournisseurs

            

                    

        except Exception as e:

            print(f"Erreur lors de la récupération de la liste des fournisseurs : {e}")

            return  []


    def list_agent(self):

        requete = "SELECT * FROM agents"

        try:

            self.cursor.execute(requete)

            fournisseurs = self.cursor.fetchall()

            print("Liste des agents récupérée avec succès.")

            return fournisseurs

            

                

        except Exception as e:

            print(f"Erreur lors de la récupération de la liste des agent: {e}")

            return  []
    def vide_historique(self):

        requete = "DELETE FROM `historique` WHERE 1 "

        try:

            self.cursor.execute(requete)

           

            print(" succès.")

            return []


        except Exception as e:

            print(f"Erreur : {e}")

            return  []

    def login(self,username, password):

        try:
            self.cursor.execute("SELECT * FROM admin WHERE Username=%s AND Password=%s", (username, password))
            row = self.cursor.fetchone()
            if row:
                return row
            else:
                return ['','']
        except Exception as e:
            print(f"erreur{e}")
            return ['','']
        

    def chek_manque(self,reference,qt_r):

        try:

            self.cursor.execute("SELECT quantiteRestante,quantiteMin FROM articles where articles.reference=%s ",(reference,))
            liste=self.cursor.fetchone()

            print(liste)
            if (liste[0] -qt_r)<=liste[1]:
                print("blink led")
                return True
            else : 

                print("low led")

                return False 
        except():

            print("erreur")
    def check_stock_periodically(self):
        try:
           
            self.cursor.execute("SELECT `emplacement`, `quantiteMin`, `quantiteRestante` FROM `articles` WHERE 1")
            articles = self.cursor.fetchall()
            print(articles)
            

        except Exception as e:
            print(f"Erreur lors de la vérification du stock : {e}")
        
        #self.master.after(60000, self.check_stock_periodically)02

db=DataBase()
db.chek_manque(reference="r002",qt_r=44) 
print (db.db_article_details("r002"))
db.check_stock_periodically()
#db.retirer_article("r002","amri",10)
"""
#db.ajouter_voiture("201248 tunisie 1013","BMW")

db.supprimer_voitures("bayouma14")

l=db.recuperer_voitures()

print(l)"""

"""UPDATE `voitures` SET `nom` = '14245 tunisie 7840' WHERE `voitures`.`matricule` = 'isszu';

UPDATE `voitures` SET `matricule` = '7841 ' WHERE `voitures`.`matricule` = '7841 tunisie';

UPDATE `voitures` SET `matricule` = '781 ', `nom` = 'Jep' WHERE `voitures`.`matricule` = '7841 ';"""



""""db=DataBase()

db.supprimer_fournisseur('ref2')

db.modifier_fournisseur(reference='ref7', nom='New Name', adresse='New Address', telephone='New Telephone')

db.ajouter_agent(matricule="78407",nom="saida",cle="1247")

db.retirer_article(id_article="pop",id_agent="14249737", quantite_sortir=5)

db.ajouter_article("pop","designation","emplacement","784","14","24","45","ref8")

db.modifier_article("artbbb","designation","maria","72","14","24","45","ref8")

db.supprimer_article("bebe")

"""



"""SELECT * FROM `fournisseurs` ORDER BY `fournisseur_ref` ASC"""






#db.ajouter_nouveau_article('reference','designation','emplacement','10',"50","10",'50','ref0')
#db.login('leoni','123')