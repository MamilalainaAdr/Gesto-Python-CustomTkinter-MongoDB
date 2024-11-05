from tkinter import *
import tkinter as tk
import customtkinter as ctk
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pymongo
from pymongo import *

#----DB CONNECTION----#
client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client["GesToPyVF"]
mycol1 = mydb['Produits']
mycol2 = mydb['Stock']
mycol3 = mydb['Commandes']
mycol4 = mydb['Historique']

#----APPEARANCE & MAIN WINDOW----#
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
root = ctk.CTk()
root.title('Gestion de stock')
root.geometry('720x500')
root.resizable(False, False)

#----CREATING TABVIEW & TABS----#
mytab = ctk.CTkTabview(root, width=680, height=480)
mytab.pack()
tab1 = mytab.add('Produits')
tab2 = mytab.add('Stockage')
tab3 = mytab.add('Commandes')
tab4 = mytab.add('Historique')

#----COMMANDS IN TAB1----#
#crud
def create_crud1(idG):
    def crud(value):
        #----EDIT----#
        if value == 'Modifier':
            def editProduct(idG):
                document1 = mycol1.find_one({'_id': idG})
                document2 = mycol2.find_one({'nom': document1['nom']})

                window2 = ctk.CTkToplevel(tab1)
                window2.title('Modifier le produit')
                window2.geometry('180x240')
                window2.resizable(False, False)

                def butcheck(value):
                    if value == 'Modifier':
                        #checking empty data            
                        if ((prod.get() == '') or (ref.get() == '') or (pu.get() == '')):
                            status.configure(text='Veuillez compléter\n tous les champs')
                        else:
                            prodU = prod.get()
                            refU = ref.get()
                            puU = pu.get()

                            #Construct the updated document data
                            updated_document1 = {
                                'nom': prodU, 
                                'reference': refU, 
                                'prix_unitaire': puU, 
                            }
                            updated_document2 = {
                                'nom': prodU, 
                                'reference': refU, 
                                'prix_unitaire': puU,
                                'qte_en_stock': document2['qte_en_stock']
                            }
                            # Update the document in the MongoDB collection
                            mycol1.update_one({"_id": idG}, {"$set": updated_document1})
                            mycol2.update_one({"nom": document1['nom']}, {"$set": updated_document2})
                            status.configure(text='')
                            window2.destroy()
                            #Update the list
                            for widget in myframe1.winfo_children():
                                widget.destroy()
                            listing1()
                            for widget in myframe2.winfo_children():
                                widget.destroy()
                            listing2()
                    else:
                        window2.destroy()
                        

                prod = ctk.CTkEntry(window2, placeholder_text=document1['nom'])
                prod.pack_configure(pady=10)
                ref = ctk.CTkEntry(window2, placeholder_text=document1['reference'])
                ref.pack_configure(pady=10)
                pu = ctk.CTkEntry(window2, placeholder_text=document1['prix_unitaire'])
                pu.pack_configure(pady=10)
                status = ctk.CTkLabel(window2, text='')
                status.pack()
                buttons = ctk.CTkSegmentedButton(window2, values=['Annuler', 'Modifier'], command=butcheck)
                buttons.pack_configure(side='bottom', fill='both')
            editProduct(idG)
                    
        #----DELETE----#
        elif value == 'Supprimer':
            def deleteProduct(idG):
                window3 = ctk.CTkToplevel(tab1)
                window3.title('Supprimer le produit')
                window3.geometry('180x80')
                window3.resizable(False, False)

                def butcheck(value):
                    if value == 'Supprimer':
                        #delete the document
                        doc1 = mycol1.find_one({'_id': idG})
                        mycol1.find_one_and_delete({'_id': idG})
                        mycol2.find_one_and_delete({'nom': doc1['nom']})
                        window3.destroy()
                        #Update the list
                        for widget in myframe1.winfo_children():
                            widget.destroy()
                        listing1()
                        for widget in myframe2.winfo_children():
                            widget.destroy()
                        listing2()
                    else:
                        window3.destroy()

                label = ctk.CTkLabel(window3, text='Supprimer ce produit?')
                label.pack_configure(pady=10)
                buttons = ctk.CTkSegmentedButton(window3, values=['Annuler', 'Supprimer'], command=butcheck)
                buttons.pack_configure(side='bottom', fill='both')

            deleteProduct(idG)

    return crud

#get a list of all products
def listing1():
    documents = mycol1.find()
    for document in documents:
        prodG = document['nom']
        refG = document['reference']
        puG = document['prix_unitaire']
        idG = document['_id']

        crud_function = create_crud1(idG)

        listing = ctk.CTkFrame(myframe1, width=580, height=40)
        listing.pack()
        mylabel1 = ctk.CTkLabel(listing, text=('Nom_du_Produit:', prodG), width=560, anchor='w')
        mylabel1.pack()
        mylabel2 = ctk.CTkLabel(listing, text=('Reference:', refG), width=560, anchor='w')
        mylabel2.pack()
        mylabel3 = ctk.CTkLabel(listing, text=('Prix_Unitaire:', puG), width=560, anchor='w')
        mylabel3.pack()

        model = ctk.CTkSegmentedButton(listing, values=['Modifier', 'Supprimer'], command=crud_function)
        model.pack_configure(side='bottom', fill='both')

#adding new product
def ajouter1():
    def butcheck(value):
        if value == 'Ajouter':
            #checking for empty data            
            if ((prod.get() == '') or (ref.get() == '') or (pu.get() == '')):
                status.configure(text='Veuillez compléter\n tous les champs')
            else:
                prodG = prod.get()
                refG = ref.get()
                puG = pu.get()
                status.configure(text='')
                #insert data into collection 1 and 2
                data1 = {'nom': prodG, 'reference': refG, 'prix_unitaire': puG}
                mycol1.insert_one(data1)
                data2 = {'nom': prodG, 'reference': refG, 'prix_unitaire': puG, 'qte_en_stock': 0}
                mycol2.insert_one(data2)
                # updating the list 1 and 2
                window1.destroy()
                for widget in myframe1.winfo_children():
                    widget.destroy()
                listing1()
                for widget in myframe2.winfo_children():
                    widget.destroy()
                listing2()

            
        else:
            window1.destroy()

    window1 = ctk.CTkToplevel(tab1)
    window1.title('Ajouter un nouveau produit')
    window1.geometry('180x240')
    window1.resizable(False, False)
    prod = ctk.CTkEntry(window1, placeholder_text='Nom du produit')
    prod.pack_configure(pady=10)
    ref = ctk.CTkEntry(window1, placeholder_text='Reference')
    ref.pack_configure(pady=10)
    pu = ctk.CTkEntry(window1, placeholder_text='Prix unitaire')
    pu.pack_configure(pady=10)
    status = ctk.CTkLabel(window1, text='')
    status.pack()
    buttons = ctk.CTkSegmentedButton(window1, values=['Annuler', 'Ajouter'], command=butcheck)
    buttons.pack_configure(side='bottom', fill='both')

#searchbar in myframe1
def sb1(event=None):
    recherche = myentry1.get().lower()
    if recherche == '':
        for widget in myframe1.winfo_children():
            widget.destroy()
        listing1()
    else:
        for widget in myframe1.winfo_children():
            widget.destroy()

        for document in mycol1.find():
            if recherche in document['nom'].lower():
                prodG = document['nom']
                refG = document['reference']
                puG = document['prix_unitaire']
                idG = document['_id']
                crud_function = create_crud1(idG)
                listing = ctk.CTkFrame(myframe1, width=580, height=40)
                listing.pack()
                mylabel1 = ctk.CTkLabel(listing, text=('Nom_du_Produit:', prodG), width=560, anchor='w')
                mylabel1.pack()
                mylabel2 = ctk.CTkLabel(listing, text=('Reference:', refG), width=560, anchor='w')
                mylabel2.pack()
                mylabel3 = ctk.CTkLabel(listing, text=('Prix_Unitaire:', puG), width=560, anchor='w')
                mylabel3.pack()
                model = ctk.CTkSegmentedButton(listing, values=['Modifier', 'Supprimer'], command=crud_function)
                model.pack_configure(side='bottom', fill='both')

#----COMMANDS IN TAB2----#
#crud
def create_crud2(ieG):
    def crud(value):
        #----EDIT----#
        if value == 'Ajouter':
            def addStk(ieG):
                document = mycol2.find_one({'_id': ieG})

                window2 = ctk.CTkToplevel(tab2)
                window2.title('Ajouter au stock')
                window2.geometry('180x220')
                window2.resizable(False, False)

                def butcheck(value):
                    if value == 'Ajouter':
                        #checking empty data            
                        if ((qes.get() == '') or (date.get() == '')):
                            status.configure(text='Veuillez compléter\n tous les champs')
                            return
                        else:
                            tsyintqefasU = document['qte_en_stock']
                            qefasU = int(tsyintqefasU)
                            tsyintqesU = qes.get()
                            qesU = int(tsyintqesU)
                            dateU = date.get()
                            #Construct the updated document data
                            updated_document1 = {
                                'nom': document['nom'], 
                                'reference': document['reference'], 
                                'prix_unitaire': document['prix_unitaire'], 
                                'qte_en_stock': qefasU + qesU
                            }
                            document4 = {
                                'action': "A ajouté "+str(qesU)+" nouveau(x) produit(s): "+document['nom'],
                                'date': dateU
                            }

                            # Update the document in the MongoDB collection
                            mycol2.update_one({"_id": ieG}, {"$set": updated_document1})
                            mycol4.insert_one(document4)
                            status.configure(text='')
                            window2.destroy()
                            #Update the list
                            for widget in myframe2.winfo_children():
                                widget.destroy()
                            listing2()
                            for widget in myframe4.winfo_children():
                                widget.destroy()
                            listing4()                            
                    else:
                        window2.destroy()

                qes = ctk.CTkEntry(window2, placeholder_text='Quantité')
                qes.pack_configure(pady=10)
                date = ctk.CTkEntry(window2, placeholder_text="Date d'ajout")
                date.pack_configure(pady=10)
                status = ctk.CTkLabel(window2, text='')
                status.pack()
                buttons = ctk.CTkSegmentedButton(window2, values=['Annuler', 'Ajouter'], command=butcheck)
                buttons.pack_configure(side='bottom', fill='both')
            addStk(ieG)

    return crud

#get a list of all products
def listing2():
    documents = mycol2.find()
    for document in documents:
        prodG = document['nom']
        refG = document['reference']
        puG = document['prix_unitaire']
        qesG = document['qte_en_stock']
        ieG = document['_id']

        crud_function = create_crud2(ieG)

        listing = ctk.CTkFrame(myframe2, width=580, height=40)
        listing.pack()
        mylabel1 = ctk.CTkLabel(listing, text=('Nom_du_produit:', prodG), width=560, anchor='w')
        mylabel1.pack()
        mylabel2 = ctk.CTkLabel(listing, text=('Reference:', refG), width=560, anchor='w')
        mylabel2.pack()
        mylabel3 = ctk.CTkLabel(listing, text=('Prix_unitaire:', puG), width=560, anchor='w')
        mylabel3.pack()
        mylabel4 = ctk.CTkLabel(listing, text=('Quantite_en_stock:', qesG), width=560, anchor='w')
        mylabel4.pack()

        model = ctk.CTkSegmentedButton(listing, values=['Ajouter'], command=crud_function)
        model.pack_configure(side='bottom', fill='both')

#searchbar in myframe2
def sb2(event=None):
    recherche = myentry2.get().lower()
    if recherche == '':
        for widget in myframe2.winfo_children():
            widget.destroy()
        listing2()
    else:
        for widget in myframe2.winfo_children():
            widget.destroy()

        for document in mycol2.find():
            if recherche in document['nom'].lower():
                prodG = document['nom']
                refG = document['reference']
                puG = document['prix_unitaire']
                qesG = document['qte_en_stock']
                ieG = document['_id']
                crud_function = create_crud2(ieG)
                listing = ctk.CTkFrame(myframe2, width=580, height=40)
                listing.pack()
                mylabel1 = ctk.CTkLabel(listing, text=('Nom_du_produit:', prodG), width=560, anchor='w')
                mylabel1.pack()
                mylabel2 = ctk.CTkLabel(listing, text=('Reference:', refG), width=560, anchor='w')
                mylabel2.pack()
                mylabel3 = ctk.CTkLabel(listing, text=('Prix_unitaire:', puG), width=560, anchor='w')
                mylabel3.pack()
                mylabel4 = ctk.CTkLabel(listing, text=('Quantite_en_stock', qesG), width=560, anchor='w')
                mylabel4.pack()
                model = ctk.CTkSegmentedButton(listing, values=['Ajouter'], command=crud_function)
                model.pack_configure(side='bottom', fill='both')

#----COMMANDS IN TAB3----#
#crud
def create_crud3(ifG):
    def crud(value):
        #----CANCEL----#
        if value == 'Annuler':
            def cancCom(ifG):
                window3 = ctk.CTkToplevel(tab3)
                window3.title('Annuler la commande')
                window3.geometry('180x80')
                window3.resizable(False, False)

                def butcheck(value):
                    if value == 'OK':
                        doc3 = mycol3.find_one({'_id': ifG})
                        doc2 = mycol2.find_one({'nom': doc3['produit']})
                        doc4 = mycol4.find_one({'date': doc3['date_commande']})

                        tsyintqte3 = doc3['qte_commande']
                        qte3 = int(tsyintqte3)
                        tsyintqes2 = doc2['qte_en_stock']
                        qes2 = int(tsyintqes2)
                        qtes = qte3 + qes2
                        data2 = {'nom': doc2['nom'], 'reference': doc2['reference'],
                                 'prix_unitaire': doc2['prix_unitaire'], 'qte_en_stock': qtes}
                        
                        mycol2.update_one({'nom': doc3['produit']}, {'$set': data2})
                        mycol4.find_one_and_delete({'date': doc3['date_commande']})
                        #delete the document
                        mycol3.find_one_and_delete({'_id': ifG})
                        window3.destroy()
                        #Update the list
                        for widget in myframe3.winfo_children():
                            widget.destroy()
                        listing3()
                        for widget in myframe2.winfo_children():
                            widget.destroy()
                        listing2()
                        for widget in myframe4.winfo_children():
                            widget.destroy()
                        listing4()
                    
                    else:
                        window3.destroy()

                label = ctk.CTkLabel(window3, text='Annuler cette commande?')
                label.pack_configure(pady=10)
                buttons = ctk.CTkSegmentedButton(window3, values=['Retour', 'OK'], command=butcheck)
                buttons.pack_configure(side='bottom', fill='both')

            cancCom(ifG)

        #----VALIDER----#
        else:
            def validCom(ifG):
                window4 = ctk.CTkToplevel(tab3)
                window4.title('Commande terminée')
                window4.geometry('180x150')
                window4.resizable(False, False)

                def butcheck(value):
                    if value == 'Terminer':
                        if (entryF.get() == ''):
                            status.configure(text='Veuillez completer\n tous les champs')
                        else:
                            #storing values in mycol4
                            doc3 = mycol3.find_one({'_id': ifG})
                            data4 = {
                                'action': 'Commande terminée: '+str(doc3['qte_commande'])+(' * ')+str(doc3['produit'])+' du '+str(doc3['date_commande']),
                                'date': entryF.get()
                            }
                            mycol4.insert_one(data4)

                            #pdf
                            document = mycol3.find({'_id': ifG})
                            compteur = 0
                            dossier = './../rapports/'
                            while compteur<1000:
                                nom_fichier = os.path.join(dossier, f'rapport_{compteur}.pdf')
                                try:
                                    with open(nom_fichier, 'r'):
                                        compteur += 1
                                except FileNotFoundError:
                                    break
                            c = canvas.Canvas(nom_fichier, pagesize=letter)
                            c.setFont('Helvetica-Bold', 16)
                            y_position = 750
                            for ligne in document:
                                c.drawString(100, y_position, f"-------------------------RAPPORT DE VENTE-------------------------")
                                c.drawString(100, y_position - 20, f" ")
                                c.drawString(100, y_position - 40, f"Produit: {ligne['produit']}")
                                c.drawString(100, y_position - 60, f"Quantité commandée: {ligne['qte_commande']}")
                                c.drawString(100, y_position - 80, f"Prix total: {ligne['prix_total']} MGA")
                                c.drawString(100, y_position - 100, f"Date de commande: {ligne['date_commande']}")
                                c.drawString(100, y_position - 120, f"Date de réception: {entryF.get()}")
                                y_position -= 140
                            c.save()
                            print(f'Rapport generé avec succes: {nom_fichier}')
                            
                            #delete command from myframe3
                            mycol3.find_one_and_delete({'_id': ifG})
                            window4.destroy()
                            #updating myframes
                            for widget in myframe4.winfo_children():
                                widget.destroy()
                            listing4()
                            for widget in myframe3.winfo_children():
                                widget.destroy()
                            listing3()

                    else:
                        window4.destroy()

                label = ctk.CTkLabel(window4, text='Terminer la commande et\nimporter au format pdf:')
                label.pack_configure(pady=10)
                entryF = ctk.CTkEntry(window4, placeholder_text='Date de validation')
                entryF.pack()
                status = ctk.CTkLabel(window4, text='')
                status.pack()
                buttons = ctk.CTkSegmentedButton(window4, values=['Annuler', 'Terminer'], command=butcheck)
                buttons.pack_configure(side='bottom', fill='both')
            
            validCom(ifG)

    return crud

#get a list of all commands
def listing3():
    documents = mycol3.find()
    for document in documents:
        prodG = document['produit']
        qteG = document['qte_commande']
        ptG = document['prix_total']
        dateG = document['date_commande']
        ifG = document['_id']

        crud_function = create_crud3(ifG)

        listing = ctk.CTkFrame(myframe3, width=580, height=40)
        listing.pack()
        mylabel1 = ctk.CTkLabel(listing, text=('Produit_commandé:', prodG), width=560, anchor='w')
        mylabel1.pack()
        mylabel3 = ctk.CTkLabel(listing, text=('Quantité_commandée:', qteG), width=560, anchor='w')
        mylabel3.pack()
        mylabel4 = ctk.CTkLabel(listing, text=('Prix_total:', ptG), width=560, anchor='w')
        mylabel4.pack()
        mylabel5 = ctk.CTkLabel(listing, text=('Date_commande:', dateG), width=560, anchor='w')
        mylabel5.pack()

        model = ctk.CTkSegmentedButton(listing, values=['Terminer', 'Annuler'], command=crud_function)
        model.pack_configure(side='bottom', fill='both')

#adding new command
def ajouter3():
    #loops for getting values in the db
    documents = mycol2.find()
    prodOpt = list()
    for document in documents:
        prodOpt.append(document['nom'])
    #window
    def butcheck(value):
        if value == 'Ajouter':
            tsyintqteG = qte.get()
            qteG = int(tsyintqteG)
            prodc = mycol2.find_one({'nom': prod.get()})
            tsyintmax = prodc['qte_en_stock']
            intmax = int(tsyintmax)

            #checking for empty data            
            if (qte.get() == '' or date.get() == ''):
                status.configure(text='Veuillez compléter\n tous les champs')
            elif (intmax < qteG):
                status.configure(text=('Quantité maximum: ', intmax))
            else:
                prodG = prod.get()
                # tsyintqteG = qte.get()
                # qteG = int(tsyintqteG)
                dateG = date.get()
                status.configure(text='')

                produit = mycol2.find_one({'nom': prodG})
                tsyintpu = produit['prix_unitaire']
                pu = int(tsyintpu)
                ptG = qteG*pu


                #insert data into collection
                data3 = {'produit': prodG, 'qte_commande': qteG, 'prix_total': ptG, 'date_commande': dateG}
                mycol3.insert_one(data3)

                tsyintqes = produit['qte_en_stock']
                qes = int(tsyintqes)
                qesR = qes - qteG
                data2 = {'nom': produit['nom'], 'reference': produit['reference'],
                         'prix_unitaire': produit['prix_unitaire'], 'qte_en_stock': qesR}
                mycol2.update_one({'nom': prodG}, {'$set': data2})

                data4 = {
                    'action': "A commandé "+str(qteG)+" produit(s): "+str(prodG),
                    'date': dateG
                    }
                mycol4.insert_one(data4)
                # updating the list
                window1.destroy()
                for widget in myframe3.winfo_children():
                    widget.destroy()
                listing3()
                for widget in myframe2.winfo_children():
                    widget.destroy()
                listing2()
                for widget in myframe4.winfo_children():
                    widget.destroy()
                listing4()
            
        else:
            window1.destroy()

    window1 = ctk.CTkToplevel(tab3)
    window1.title('Passer une commande')
    window1.geometry('180x260')
    window1.resizable(False, False)
    prod = ctk.CTkOptionMenu(window1, values=prodOpt)
    prod.pack(pady=10)
    qte = ctk.CTkEntry(window1, placeholder_text='Quantité commandée')
    qte.pack_configure(pady=10)
    date = ctk.CTkEntry(window1, placeholder_text='Date de la commande')
    date.pack_configure(pady=10)
    status = ctk.CTkLabel(window1, text='')
    status.pack()
    buttons = ctk.CTkSegmentedButton(window1, values=['Annuler', 'Ajouter'], command=butcheck)
    buttons.pack_configure(side='bottom', fill='both')

#----COMMANDS IN TAB4----#
#crud
def create_crud4(igG):
    def hisdel(value):
        #---Delete----#
        if value == 'Supprimer':
            def deleteCom(igG):
                window3 = ctk.CTkToplevel(tab4)
                window3.title('Suppression')
                window3.geometry('180x80')
                window3.resizable(False, False)

                def butcheck(value):
                    if value == 'Supprimer':
                        #delete the document
                        mycol4.find_one_and_delete({'_id': igG})
                        window3.destroy()
                        #Update the list
                        for widget in myframe4.winfo_children():
                            widget.destroy()
                        listing4()
                    
                    else:
                        window3.destroy()

                label = ctk.CTkLabel(window3, text='Supprimer de\n l\'historique?')
                label.pack_configure(pady=10)
                buttons = ctk.CTkSegmentedButton(window3, values=['Annuler', 'Supprimer'], command=butcheck)
                buttons.pack_configure(side='bottom', fill='both')

            deleteCom(igG)
    return hisdel

#get the history
def listing4():
    documents = mycol4.find()
    for document in documents:
        actionG = document['action']
        dateG = document['date']
        igG = document['_id']

        crud_function = create_crud4(igG)

        listing = ctk.CTkFrame(myframe4, width=580, height=20, border_width=10)
        listing.pack()
        mylabel1 = ctk.CTkLabel(listing, text=('Action:', actionG), width=560, anchor='w')
        mylabel1.pack()
        mylabel2 = ctk.CTkLabel(listing, text=('Date:', dateG), width=560, anchor='w')
        mylabel2.pack()
        model = ctk.CTkSegmentedButton(listing, values=['Supprimer'], command=crud_function)
        model.pack_configure(side='bottom', fill='both')
        
#----TAB1----#
myentry1 = ctk.CTkEntry(tab1, placeholder_text='Trouver un produit ...', width=580)
myentry1.pack_configure(side='top')
myentry1.bind('<KeyRelease>', sb1)
myframe1 = ctk.CTkScrollableFrame(tab1, width=600, height=320, border_width=3)
listing1()
myframe1.pack(pady=10)
mybutton1 = ctk.CTkButton(tab1, text='+ Nouveau', command=ajouter1)
mybutton1.pack()

#----TAB2----#
myentry2 = ctk.CTkEntry(tab2, placeholder_text='Rechercher dans le stock ...', width=580)
myentry2.pack_configure(side='top')
myentry2.bind('<KeyRelease>', sb2)
myframe2 = ctk.CTkScrollableFrame(tab2, width=600, height=352, border_width=3)
listing2()
myframe2.pack(pady=10)

#----TAB3----#
myframe3 = ctk.CTkScrollableFrame(tab3, width=600, height=348, border_width=3)
listing3()
myframe3.pack(pady=10)
mybutton3 = ctk.CTkButton(tab3, text='+ Commander', command=ajouter3)
mybutton3.pack()

#----TAB4----#
myframe4 = ctk.CTkScrollableFrame(tab4, width=600, height=380, border_width=3)
listing4()
myframe4.pack(pady=10)


root.mainloop()
