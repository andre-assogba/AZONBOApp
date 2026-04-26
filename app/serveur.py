# -*- coding: utf-8 -*-
# AZONBOApp v1.2 - Interface Flask
# Andre Marc ASSOGBA

from flask import Flask, render_template, request, session, redirect, url_for
from db import initialiser, lister_produits, ajouter_produit, verifier_utilisateur, creer_utilisateur, lister_sessions, lister_dettes, get_resume, get_dette, rechercher_dettes, enregistrer_remboursement, modifier_vente
from ventes import Vente
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'azonbo_secret_2026'
initialiser()

@app.route('/')
def menu():
    return render_template('menu.html')


@app.route('/produits')
def produits():
    p = lister_produits()
    return render_template('produits.html', produits=p)

@app.route('/produits/ajouter', methods=['POST'])
def ajouter():
    nom = request.form['nom']
    prix = float(request.form['prix'])
    qte = int(request.form['qte'])
    seuil = int(request.form['seuil'])
    ajouter_produit(nom, prix, qte, seuil)
    return redirect(url_for('produits'))

@app.route('/historique', methods=['GET', 'POST'])
def historique():
    try:
        resultats = []
        nom = ''
        if request.method == 'POST':
            nom = request.form['nom']
            conn = __import__('db').connecter()
            c = conn.cursor()
            c.execute('SELECT id, client, date, total, paiement FROM sessions WHERE client LIKE ? ORDER BY date DESC', ('%' + nom + '%',))
            resultats = c.fetchall()
            conn.close()
        return render_template('historique.html', resultats=resultats, nom=nom)
    except Exception as e:
        return render_template('erreur.html', msg=str(e))

@app.route('/resume')
def resume():
    try:
        r = get_resume()
        return render_template('resume.html', r=r)
    except Exception as e:
        return render_template('erreur.html', msg=str(e))

@app.route('/dettes', methods=['GET', 'POST'])
def dettes():
    nom = ""
    if request.method == "POST":
        nom = request.form.get("nom", "").strip()
        d = rechercher_dettes(nom)
    else:
        d = lister_dettes()
    try:
        return render_template('dettes.html', dettes=d)
    except Exception as e:
        return render_template('erreur.html', msg=str(e))

@app.route('/ventes/nouvelle', methods=['GET', 'POST'])
def nouvelle_vente():
    try:
        produits = lister_produits()
        if request.method == 'POST':
            client = request.form['client'].strip()
            mode = request.form['mode']
            avance = float(request.form.get('avance') or 0)
            articles = []
            for p in produits:
                qte = int(request.form.get('qte_' + str(p[0]), 0))
                if qte > 0:
                    articles.append((p[1], qte, qte * p[2], p[0]))
            if not articles:
                return render_template('nouvelle_vente.html', produits=produits, erreur='Aucun produit selectionne.')
            total = sum(a[2] for a in articles)
            if mode == 'cash':
                avance = total
            from datetime import datetime
            date = datetime.now().strftime('%d/%m/%Y %H:%M')
            v = Vente(client, date, articles, total, mode, avance)
            sid = v.sauvegarder()
            return redirect('/facture/' + str(sid))
        return render_template('nouvelle_vente.html', produits=produits, erreur=None)
    except Exception as e:
        return render_template('erreur.html', msg=str(e))

@app.route('/ventes')
def ventes():
    try:
        sessions = lister_sessions()
        return render_template('ventes.html', sessions=sessions)
    except Exception as e:
        return render_template('erreur.html', msg=str(e))


@app.route('/facture/<int:sid>')
def facture(sid):
    try:
        import db
        conn = db.connecter()
        c = conn.cursor()
        c.execute('SELECT client, date, total, paiement FROM sessions WHERE id=?', (sid,))
        s = c.fetchone()
        c.execute('SELECT p.nom, v.quantite, v.total FROM ventes v JOIN produits p ON v.produit_id=p.id WHERE v.session_id=?', (sid,))
        articles = c.fetchall()
        c.execute('SELECT montant_restant FROM credits WHERE session_id=?', (sid,))
        credit = c.fetchone()
        avance = round(s[2] - credit[0]) if credit else s[2]
        reste = round(credit[0]) if credit else 0
        conn.close()
        return render_template('facture.html', sid=sid, s=s, articles=articles, avance=avance, reste=reste)
    except Exception as e:
        return render_template('erreur.html', msg=str(e))




@app.route('/dettes/<int:cid>')
def dette_detail(cid):
    try:
        dette, remboursements = get_dette(cid)
        return render_template('dette_detail.html', dette=dette, remboursements=remboursements)
    except Exception as e:
        return render_template('erreur.html', msg=str(e))

@app.route('/dettes/<int:cid>/rembourser', methods=['POST'])
def rembourser(cid):
    try:
        montant = float(request.form['montant'])
        enregistrer_remboursement(cid, montant)
        return redirect('/dettes/' + str(cid))
    except Exception as e:
        return render_template('erreur.html', msg=str(e))

@app.route('/ventes/<int:sid>/modifier', methods=['GET', 'POST'])
def modifier_vente_route(sid):
    try:
        import db
        conn = db.connecter()
        c = conn.cursor()
        c.execute('SELECT client, paiement FROM sessions WHERE id=?', (sid,))
        s = c.fetchone()
        conn.close()
        if request.method == 'POST':
            client = request.form['client'].strip()
            mode = request.form['mode']
            modifier_vente(sid, client, mode)
            return redirect('/ventes')
        return render_template('modifier_vente.html', sid=sid, s=s)
    except Exception as e:
        return render_template('erreur.html', msg=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    erreur = None
    if request.method == 'POST':
        nom = request.form['nom']
        mdp = request.form['mot_de_passe']
        if verifier_utilisateur(nom, mdp):
            session['utilisateur'] = nom
            return redirect(url_for('menu'))
        else:
            erreur = 'Nom ou mot de passe incorrect.'
    return render_template('login.html', erreur=erreur)

@app.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect(url_for('login'))

@app.before_request
def verifier_connexion():
    routes_libres = ['login', 'static']
    if 'utilisateur' not in session and request.endpoint not in routes_libres:
        return redirect(url_for('login'))
