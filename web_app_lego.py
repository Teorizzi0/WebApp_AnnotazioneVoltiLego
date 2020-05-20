'''
    File name: web_app_lego.py
    Author: Matteo Rizzi
    Date created: 10/04/2017
    Date last modified: 29/06/2017
    Python Version: 3.6

'''

import os

import sqlite3

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from werkzeug import secure_filename
from random import randint

app = Flask(__name__)
app.secret_key = 'samcpacpa,sqp,cpsac-aawsaqw192311ì'    #secret key necessaria per garantire sicurezza delle sessioni

#Questo è il Path in cui verranno salvate le immagini caricate in modalità amministratore. Devono andare in static
#all'interno della directory del progetto cosi da poter essere visualizzate.
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\matte\\Documents\\Unimib\\Stage\\AnnotazioniVolti\\DBLego\\static'

#Il Path deve essere modificato in base alla posizione in cui verrà messo il file.db collegato all'applicazione.
global dbannotazioni
dbannotazioni = 'C:\\Users\\matte\\Documents\\Unimib\\Stage\\AnnotazioniVolti\\DBLego\\dbannotazioni.db'

free = None  #lista di immagini da valutare

#Funzione che controlla se un valore posizioanto all'indice 'random' di una lista è presente in un'altra lista
def check_list(list1, list2):
    #random = randint(0,2)  #questo per testare il programma con 3 immagini in una cartella temporanea
    random = randint(0, 999)  #questo per intero dataset di 1000 immagini
    while list1[random] in list2:
        #random = randint(0,2)
        random = randint(0,999)
    session['name_u'] = list1[random]
    return None


#La lista free è l'elenco di tutte le immagini disponibili per essere valutate. Il path varia a seconda delle necessità.
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST' or request.method == 'GET':
        if 'username' in session:
            username = session['username']
            with sqlite3.connect(dbannotazioni) as ann:
                cur4 = ann.cursor()
                cur4.execute('SELECT "volto_umano" FROM Annotazione WHERE Annotazione.Id_session = ?', [username])
                global imm_valutate
                imm_valutate = list(cur4.fetchall())
                imm_valutate = ([('{} '*len(t)).format(*t).strip() for t in imm_valutate])
                global numero_valutate
                numero_valutate = len(imm_valutate)  #contatore di immagini già fatte
                ann.commit()
                global free
                #nella cartella 'temporanea' ho usato poche immagini per far si che si possa testare ogni aspetto.
                free = os.listdir('C:\\Users\\matte\\Documents\\Unimib\\Stage\\AnnotazioniVolti\\DBLego\\Volti_umani')
                #free = os.listdir('C:\\Users\\matte\\Documents\\Unimib\\Stage\\AnnotazioniVolti\\DBLego\\temporanea')
                global numero_rimanenti
                numero_rimanenti = len(free)
                #se le liste delle immagini valutate e quelle disponibili coincidono allora l'annotazione è finita
                if all(value in imm_valutate for value in free):
                    return redirect(url_for('fine'), code=307)
                else:
                    check_list(free, imm_valutate)
                    return render_template('apphome.html', namehtml = username)
        return render_template('applogin.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('methodnotallowed.html')
    else:
        session['username'] = request.form['username']
        if session['username'] == 'admin':
            global error1
            error1 = None
            return render_template('gotoadmin.html', error_h = error1, namehtml = session['username'])
        else:
            with sqlite3.connect(dbannotazioni) as con:
                cur1 = con.cursor()
                cur1.execute('SELECT * FROM Utente WHERE username = ?', [session['username']])
                if cur1.fetchone() is not None:
                    return redirect(url_for('index'))  #se l'utente è gia registrato voglio che abbia lista imm valutate
                else:
                    cur1.execute('INSERT INTO Utente (username) VALUES (?)',[session['username']])
                    con.commit()
                    imm_valutate = []  #se non è registrato gli associo lista vuota che riempirà ad ogni valutazione
                    return redirect(url_for('index'))


@app.route('/annotazionivolti', methods = ['GET', 'POST'])
def rico():
    if request.method == 'GET':
        return render_template('methodnotallowed.html')
    else:
        if 'username' in session:
            username = session['username']
            name_u = session['name_u']
            return render_template('appvolti2.html', namehtml = username, name_u_h = name_u, numero_fatte = numero_valutate, numero_html = numero_rimanenti)


#Questa funzione di routing '/filter' è molto lunga e poco portabile, però non ho trovato un'alternativa poichè ogni
#query doveva prendere attributi diversi dal database e fare una funzione per la query non era funzionale in quanto
#il cursore cur non riusciva a rispettare le sessioni.
@app.route('/filter', methods=['GET', 'POST'])
def viewdb():
    if request.method == 'GET':
        return render_template('methodnotallowed.html')
    else:
        global occh, lent, sopra, cica, ross, neo, rughe, fascia, pizz, baffi, barba, capello, lingua, elmo
        global benda, trucco, maschera
        global list1, list2, list3, list4, list5, list6, list7, list8, list9, list10, list11, list12, list13
        global list14, list15, list16, list17
        global list_pronta
        global genere
        global bool_occhiali, bool_lentiggini, bool_sopracciglia, bool_cicatrice, bool_rossetto, bool_neo
        global bool_rughe, bool_fascia, bool_trucco, bool_maschera, bool_elmo
        global bool_pizzetto, bool_barba, bool_baffi, bool_capello, bool_lingua, bool_benda

        with sqlite3.connect(dbannotazioni) as conlego:
            cur3 = conlego.cursor()
            # query che mi restituisce tutto il db cosi poi posso fare intersezioni.
            cur3.execute('SELECT "Nome file" FROM VoltoLego')
            # lista di tuple risultanti
            list_pronta = list(cur3.fetchall())
            # trasformo lista di tuple in lista di stringhe
            list_pronta = ([('{} ' * len(t)).format(*t).strip() for t in list_pronta])

            bool_occhiali = request.form.get('occhiali')
            if bool_occhiali:
                occh = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Occhiali = ?', [occh])
                list1 = list(cur3.fetchall())
                # trasformo lista di tuple in lista di stringhe a cui poi aggiungerò il .jpg
                list1 = ([('{} ' * len(t)).format(*t).strip() for t in list1])
                # faccio intersezione per vedere se ho risultati in comune
                list_pronta = list(set(list_pronta) & set(list1))
            else:
                list1 = []

            bool_lentiggini = request.form.get('lent')
            if bool_lentiggini:
                lent = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Lentiggini = ?', [lent])
                list2 = list(cur3.fetchall())
                list2 = ([('{} ' * len(t)).format(*t).strip() for t in list2])
                list_pronta = list(set(list_pronta) & set(list2))
            else:
                list2 = []

            bool_sopracciglia = request.form.get('sopra')
            if bool_sopracciglia:
                sopra = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Sopracciglia = ?', [sopra])
                list3 = list(cur3.fetchall())
                list3 = ([('{} ' * len(t)).format(*t).strip() for t in list3])
                list_pronta = list(set(list_pronta) & set(list3))
            else:
                list3 = []

            bool_cicatrice = request.form.get('cica')
            if bool_cicatrice:
                cica = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Cicatrice = ?', [cica])
                list4 = list(cur3.fetchall())
                list4 = ([('{} ' * len(t)).format(*t).strip() for t in list4])
                list_pronta = list(set(list_pronta) & set(list4))
            else:
                list4 = []

            bool_rossetto = request.form.get('ross')
            if bool_rossetto:
                ross = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Rossetto = ?', [ross])
                list5 = list(cur3.fetchall())
                list5 = ([('{} ' * len(t)).format(*t).strip() for t in list5])
                list_pronta = list(set(list_pronta) & set(list5))
            else:
                list5 = []

            bool_neo = request.form.get('neo')
            if bool_neo:
                neo = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Neo = ?', [neo])
                list6 = list(cur3.fetchall())
                list6 = ([('{} ' * len(t)).format(*t).strip() for t in list6])
                list_pronta = list(set(list_pronta) & set(list6))
            else:
                list6 = []

            bool_rughe = request.form.get('rughe')
            if bool_rughe:
                rughe = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Rughe = ?', [rughe])
                list7 = list(cur3.fetchall())
                list7 = ([('{} ' * len(t)).format(*t).strip() for t in list7])
                list_pronta = list(set(list_pronta) & set(list7))
            else:
                list7 = []

            bool_fascia = request.form.get('fascia')
            if bool_fascia:
                fascia = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Fascia = ?', [fascia])
                list8 = list(cur3.fetchall())
                list8 = ([('{} ' * len(t)).format(*t).strip() for t in list8])
                list_pronta = list(set(list_pronta) & set(list8))
            else:
                list8 = []

            bool_pizzetto = request.form.get('pizz')
            if bool_pizzetto:
                pizz = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Pizzetto = ?', [pizz])
                list9 = list(cur3.fetchall())
                list9 = ([('{} ' * len(t)).format(*t).strip() for t in list9])
                list_pronta = list(set(list_pronta) & set(list9))
            else:
                list9 = []

            bool_baffi = request.form.get('baffi')
            if bool_baffi:
                baffi = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Baffi = ?', [baffi])
                list10 = list(cur3.fetchall())
                list10 = ([('{} ' * len(t)).format(*t).strip() for t in list10])
                list_pronta = list(set(list_pronta) & set(list10))
            else:
                list10 = []

            bool_barba = request.form.get('barba')
            if bool_barba:
                barba = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Barba = ?', [barba])
                list11 = list(cur3.fetchall())
                list11 = ([('{} ' * len(t)).format(*t).strip() for t in list11])
                list_pronta = list(set(list_pronta) & set(list11))
            else:
                list11 = []

            bool_capello = request.form.get('cap')
            if bool_capello:
                capello = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Capelli = ?', [capello])
                list12 = list(cur3.fetchall())
                list12 = ([('{} ' * len(t)).format(*t).strip() for t in list12])
                list_pronta = list(set(list_pronta) & set(list12))
            else:
                list12 = []

            bool_lingua = request.form.get('lingua')
            if bool_lingua:
                lingua = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Lingua = ?', [lingua])
                list13 = list(cur3.fetchall())
                list13 = ([('{} ' * len(t)).format(*t).strip() for t in list13])
                list_pronta = list(set(list_pronta) & set(list13))
            else:
                list13 = []

            bool_elmo = request.form.get('elmo')
            if bool_elmo:
                elmo = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Cappellielmo = ?', [elmo])
                list14 = list(cur3.fetchall())
                list14 = ([('{} ' * len(t)).format(*t).strip() for t in list14])
                list_pronta = list(set(list_pronta) & set(list14))
            else:
                list14 = []

            bool_benda = request.form.get('benda')
            if bool_benda:
                benda = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.BendaOcchio = ?', [benda])
                list15 = list(cur3.fetchall())
                list15 = ([('{} ' * len(t)).format(*t).strip() for t in list15])
                list_pronta = list(set(list_pronta) & set(list15))
            else:
                list15 = []

            bool_trucco = request.form.get('trucco')
            if bool_trucco:
                trucco = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Trucco = ?', [trucco])
                list16 = list(cur3.fetchall())
                list16 = ([('{} ' * len(t)).format(*t).strip() for t in list16])
                list_pronta = list(set(list_pronta) & set(list16))
            else:
                list16 = []

            bool_maschera = request.form.get('maschera')
            if bool_maschera:
                maschera = 1
                cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Maschera = ?', [maschera])
                list17 = list(cur3.fetchall())
                list17 = ([('{} ' * len(t)).format(*t).strip() for t in list17])
                list_pronta = list(set(list_pronta) & set(list17))
            else:
                list17 = []

                # Per i radiobutton faccio prima un controllo se sono segnati o no, e poi se sono maschio e femmina.
            if request.form.get('genere'):
                genere = request.form['genere']
                if genere == "M":
                    cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Genere = "M"')
                    list18 = list(cur3.fetchall())
                    list18 = ([('{} ' * len(t)).format(*t).strip() for t in list18])
                    list_pronta = list(set(list_pronta) & set(list18))
                elif genere == "F":
                    cur3.execute('SELECT "Nome file" FROM VoltoLego WHERE VoltoLego.Genere = "F"')
                    list18 = list(cur3.fetchall())
                    list18 = ([('{} ' * len(t)).format(*t).strip() for t in list18])
                    list_pronta = list(set(list_pronta) & set(list18))
            else:
                genere = False

    #Per aggiungere o cambiare delle carattaristiche bisognarà aggiungere lo stesso blocco di codice per la nuova
    #caratteristica.
    return checkbox()


@app.route('/checkbox', methods= ['GET', 'POST'])
def checkbox():
    if request.method == 'GET':
        return render_template('methodnotallowed.html')
    else:
        if 'username' in session:
            username = session['username']
            name_u = session['name_u']
            list_images = []
            #faccio un ciclo for per aggiungere il .jpg ad ogni immagine
            for i in list_pronta:
                list_images.append(i+ ".jpg")
            return render_template('appvolti1.html', listaimmagini = list_images, name_u_h = name_u,namehtml = username, numero_fatte = numero_valutate, numero_html = numero_rimanenti)


#Anche in questo caso la funzione di routing è molto estesa e ripetitiva ma in questo modo garantisco di poter aggiungere
#al database annotazione ogni valore che è stato inserito dall'utente nell'annotazione appena conclusa.
@app.route('/addindb', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('methodnotallowed.html')
    else:
        if 'username' in session:
            username = session['username']
            name_u = session['name_u']
            lego_name = request.form['chosen']
            lego_name = lego_name.replace(".jpg", "")  #serve per avere solo il nome dell'immagine lego senza .jpg
            with sqlite3.connect(dbannotazioni) as conann:
                cur2 = conann.cursor()
                cur2.execute('INSERT INTO Annotazione (Id_session, volto_umano,volto_lego) VALUES (?,?,?)',
                             [username, name_u, lego_name])
                if bool_occhiali:
                    cur2.execute('UPDATE Annotazione SET Occhiali = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_lentiggini:
                    cur2.execute('UPDATE Annotazione SET Lentiggini = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_sopracciglia:
                    cur2.execute('UPDATE Annotazione SET Sopracciglia = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_cicatrice:
                    cur2.execute('UPDATE Annotazione SET Cicatrice = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_rossetto:
                    cur2.execute('UPDATE Annotazione SET Rossetto = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_neo:
                    cur2.execute('UPDATE Annotazione SET Neo = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_rughe:
                    cur2.execute('UPDATE Annotazione SET Rughe = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_fascia:
                    cur2.execute('UPDATE Annotazione SET Fascia = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_pizzetto:
                    cur2.execute('UPDATE Annotazione SET Pizzetto = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_barba:
                    cur2.execute('UPDATE Annotazione SET Barba = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_baffi:
                    cur2.execute('UPDATE Annotazione SET Baffi = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_capello:
                    cur2.execute('UPDATE Annotazione SET Capelli = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_lingua:
                    cur2.execute('UPDATE Annotazione SET Lingua = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_benda:
                    cur2.execute('UPDATE Annotazione SET BendaOcchio = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_elmo:
                    cur2.execute('UPDATE Annotazione SET Cappellielmo = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_trucco:
                    cur2.execute('UPDATE Annotazione SET Trucco = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if bool_maschera:
                    cur2.execute('UPDATE Annotazione SET Maschera = 1 WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if genere == "M":
                    cur2.execute('UPDATE Annotazione SET Genere = "M" WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])
                if genere == "F":
                    cur2.execute('UPDATE Annotazione SET Genere = "F" WHERE Id_session = ? AND volto_umano = ?',
                                 [username, name_u])

                # Qua estraggo tutte le immagini già valutate e lo faccio tutte le volte che aggiorno il db annotazione
                cur2.execute('SELECT "volto_umano" FROM Annotazione WHERE Annotazione.Id_session = ?', [username])
                imm_valutate = list(cur2.fetchall())
                imm_valutate = ([('{} ' * len(t)).format(*t).strip() for t in imm_valutate])
                global numero_valutate
                numero_valutate = len(imm_valutate)
                conann.commit()
            # se gli elementi di free e imm_valutate sono gli stessi allora ho finito
            if set(free) == set(imm_valutate):
                return redirect(url_for('fine'))
            else:
                check_list(free, imm_valutate)

                return rico()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.clear()
    return redirect(url_for('index'))


@app.route("/fine", methods=['GET', 'POST'])
def fine():
        session.pop('username', None)
        session.clear()
        # session.pop()? dipende da cookies
        return render_template('fine.html')



#-------------------------------------Admin Extension--------------------
@app.route('/admin', methods= ['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('methodnotallowed.html')
    else:
        username = session['username']
        passnow = request.form['password']
        with sqlite3.connect(dbannotazioni) as conadmin:
            cur5 = conadmin.cursor()
            cur5.execute('SELECT "password" FROM Utente WHERE username = ?', [username])
            passdb = str(cur5.fetchone()[0])  #metodo per avere stringa come risultato
            if passnow == passdb :
                global error2
                error2 = None
                return adminuploadpage()  #cosi chiamo metodo post e non get
               #return redirect(url_for('adminuploadpage'))

            else:
                global error1
                error1 = "Password errata"
                return render_template('gotoadmin.html', error_h = error1, namehtml = username)

@app.route('/adminuploadpage', methods= ['GET', 'POST'])
def adminuploadpage():
    if request.method == 'GET':
        return render_template('methodnotallowed.html')
    else:
        session['username'] = "admin"
        return render_template('upload.html', namehtml = session['username'], error = error2)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        global filename
        file = request.files['file']
        filename = secure_filename(file.filename)
        with sqlite3.connect(dbannotazioni) as conadd:
            cur3 = conadd.cursor()
            #Rimuovo il formato prima di aggiungere immagine al db

            filename = filename.replace(".jpg", "")
            filename = filename.replace(".png", "")
            filename = filename.replace(".gif", "")

            # Controllo se nel database c'è già immagine
            cur3.execute('SELECT "Nome file" FROM VoltoLego')
            list_voltilego = list(cur3.fetchall())
            list_voltilego = ([('{} ' * len(t)).format(*t).strip() for t in list_voltilego])

            if filename in list_voltilego:
                global error2
                error2 = "Impossibile completare il caricamento. L'immagine è già presente nel database."
                conadd.commit()
                return adminuploadpage()
            else:
                #f.save(secure_filename(f.filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template('adminrecordindb.html',namehtml="admin", volto_name = filename)


@app.route('/addnewrecord', methods = ['GET', 'POST'])
def adminrecord():
    if request.method == 'GET':
        return render_template('methodnotallowed.html')
    else:
        global occh, lent, sopra, cica, ross, neo, rughe, fascia, pizz, baffi, barba, capello, lingua, elmo
        global benda, trucco, maschera
        global bool_occhiali, bool_lentiggini, bool_sopracciglia, bool_cicatrice, bool_rossetto, bool_neo
        global bool_rughe, bool_fascia, bool_trucco, bool_maschera, bool_elmo
        global bool_pizzetto, bool_barba, bool_baffi, bool_capello, bool_lingua, bool_benda

        with sqlite3.connect(dbannotazioni) as conadd:
            cur3 = conadd.cursor()
            bool_occhiali = request.form.get('occhiali')
            if bool_occhiali:
                occh = 1
            else:
                occh = 0

            bool_lentiggini = request.form.get('lent')
            if bool_lentiggini:
                lent = 1
            else:
                lent = 0

            bool_sopracciglia = request.form.get('sopra')
            if bool_sopracciglia:
                sopra = 1
            else:
                sopra = 0

            bool_cicatrice = request.form.get('cica')
            if bool_cicatrice:
                cica = 1
            else:
                cica = 0

            bool_rossetto = request.form.get('ross')
            if bool_rossetto:
                ross = 1
            else:
                ross = 0

            bool_neo = request.form.get('neo')
            if bool_neo:
                neo = 1
            else:
                neo = 0

            bool_rughe = request.form.get('rughe')
            if bool_rughe:
                rughe = 1
            else:
                rughe = 0

            bool_fascia = request.form.get('fascia')
            if bool_fascia:
                fascia = 1
            else:
                fascia = 0

            bool_pizzetto = request.form.get('pizz')
            if bool_pizzetto:
                pizz = 1
            else:
                pizz = 0

            bool_baffi = request.form.get('baffi')
            if bool_baffi:
                baffi = 1
            else:
                baffi = 0

            bool_barba = request.form.get('barba')
            if bool_barba:
                barba = 1
            else:
                barba = 0

            bool_capello = request.form.get('cap')
            if bool_capello:
                capello = 1
            else:
                capello = 0

            bool_lingua = request.form.get('lingua')
            if bool_lingua:
                lingua = 1
            else:
                lingua = 0

            bool_elmo = request.form.get('elmo')
            if bool_elmo:
                elmo = 1
            else:
                elmo = 0

            bool_benda = request.form.get('benda')
            if bool_benda:
                benda = 1
            else:
                benda = 0

            bool_trucco = request.form.get('trucco')
            if bool_trucco:
                trucco = 1
            else:
                trucco = 0

            bool_maschera = request.form.get('maschera')
            if bool_maschera:
                maschera = 1
            else:
                maschera = 0

            if request.form.get('genere'):
                genere = request.form['genere']
            else:
                genere = None

            error2 = None
            cur3.execute('INSERT INTO VoltoLego ("Nome File", Occhiali, Lentiggini, Sopracciglia, Cicatrice, Rossetto,'
                             ' Neo, Rughe, Fascia, Pizzetto, Baffi, Barba, Capelli, Lingua, Genere, Cappellielmo,'
                             ' BendaOcchio, Trucco, Maschera) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                             [filename, occh, lent, sopra, cica, ross, neo, rughe, fascia, pizz, baffi, barba, capello,
                              lingua, genere, elmo, benda, trucco, maschera])

            conadd.commit()
            return adminuploadpage()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False) #Per raggiungere la pagina web, ogni dispositivo connnesso alla stessa
                                                  #rete del server, dovrà collegarsi all'URL: 'indirizzo ip server:'
