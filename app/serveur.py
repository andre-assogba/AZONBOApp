# -*- coding: utf-8 -*-
# AZONBOApp v1.3
# Andre Marc ASSOGBA

from flask import Flask, render_template, request, session, redirect, url_for
from db import initialiser, get_articles_session, get_credit_session, get_produit, get_user_id, lister_produits, ajouter_produit, creer_session, ajouter_vente, lister_sessions, lister_dettes, get_dette, rechercher_dettes, enregistrer_remboursement, modifier_vente, verifier_utilisateur, get_resume
from ventes import Vente
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'azonbo_secret_2026'
initialiser()

def uid():
    return get_user_id(session['utilisateur'])

@app.before_request
def verifier_connexion():
    routes_libres = ['login', 'static', 'inscription']
    if 'utilisateur' not in session and request.endpoint not in routes_libres:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    erreur = None
    if request.method == 'POST':
        nom = request.form['nom']
        mdp = request.form['mot_de_passe']
        user_id = verifier_utilisateur(nom, mdp)
        if user_id:
            session['utilisateur'] = nom
            return redirect(url_for('menu'))
        else:
            erreur = 'Nom ou mot de passe incorrect.'
    return render_template('login.html', erreur=erreur)

@app.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect(url_for('login'))

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/produits')
def produits():
    p = lister_produits(uid())
    return render_template('produits.html', produits=p)

@app.route('/produits/ajouter', methods=['POST'])
def ajouter_produit_route():
    nom = request.form['nom']
    prix = float(request.form['prix'])
    qte = int(request.form['quantite'])
    seuil = int(request.form['seuil'])
    ajouter_produit(uid(), nom, prix, qte, seuil)
    return redirect(url_for('produits'))

@app.route('/ventes')
def ventes():
    sessions = lister_sessions(uid())
    return render_template('ventes.html', sessions=sessions)

@app.route('/ventes/nouvelle', methods=['GET', 'POST'])
def nouvelle_vente():
    produits = lister_produits(uid())
    if request.method == 'POST':
        client = request.form.get('client', 'Client')
        mode = request.form.get('paiement', 'cash')
        produits_sel = request.form.getlist('produit_id')
        quantites = request.form.getlist('quantite')
        if not produits_sel:
            return render_template('nouvelle_vente.html', produits=produits, erreur='Aucun produit selectionne.')
        v = Vente(client, mode)
        for pid, qte in zip(produits_sel, quantites):
            p = get_produit(int(pid))
            if p:
                v.ajouter_produit(p[0], p[1], p[2], int(qte))
        date = datetime.now().strftime('%d/%m/%Y %H:%M')
        sid = creer_session(uid(), v.client, date, v.total, v.mode)
        for item in v.produits:
            ajouter_vente(sid, item['id'], item['quantite'], item['total'])
        if v.mode in ('credit', 'partiel'):
            from db import ajouter_dette
            avance = int(request.form.get('avance', 0))
            reste = v.total - avance
            ajouter_dette(uid(), sid, v.client, v.total, date, reste)
        return redirect(url_for('facture', sid=sid))
    return render_template('nouvelle_vente.html', produits=produits, erreur=None)

@app.route('/resume')
def resume():
    date = datetime.now().strftime('%d/%m/%Y')
    ventes, dettes = get_resume(uid(), date)
    return render_template('resume.html', date=date, ventes=ventes, dettes=dettes)

@app.route('/historique', methods=['GET', 'POST'])
def historique():
    resultats = []
    client = ''
    if request.method == 'POST':
        client = request.form.get('client', '')
        resultats = rechercher_dettes(uid(), client)
    return render_template('historique.html', resultats=resultats, client=client)

@app.route('/dettes', methods=['GET', 'POST'])
def dettes():
    client = ''
    if request.method == 'POST':
        client = request.form.get('client', '')
        liste = rechercher_dettes(uid(), client)
    else:
        liste = lister_dettes(uid())
    return render_template('dettes.html', dettes=liste, client=client)

@app.route('/dettes/<int:cid>')
def dette_detail(cid):
    d = get_dette(cid)
    return render_template('dette_detail.html', dette=d)

@app.route('/dettes/<int:cid>/rembourser', methods=['POST'])
def rembourser(cid):
    montant = float(request.form['montant'])
    enregistrer_remboursement(cid, montant)
    return redirect(url_for('dettes'))

@app.route('/facture/<int:sid>')
def facture(sid):
    s = lister_sessions(uid())
    session_data = next((x for x in s if x[0] == sid), None)
    articles = get_articles_session(sid)
    credit = get_credit_session(sid)
    return render_template('facture.html', s=session_data, sid=sid, articles=articles, credit=credit)

@app.route('/ventes/<int:sid>/modifier', methods=['GET', 'POST'])
def modifier_vente_route(sid):
    if request.method == 'POST':
        client = request.form['client']
        mode = request.form['paiement']
        modifier_vente(sid, client, mode)
        return redirect(url_for('ventes'))
    s = lister_sessions(uid())
    session_data = next((x for x in s if x[0] == sid), None)
    return render_template('modifier_vente.html', sid=sid, s=session_data)


@app.route('/inscription', methods=['GET','POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        mdp = request.form.get('mot_de_passe')
        if not nom or not mdp:
            return render_template('inscription.html', erreur='Remplissez tous les champs')
        from db import s_inscrire
        ok = s_inscrire(nom, mdp)
        if ok:
            return redirect('/login')
        return render_template('inscription.html', erreur='Nom deja pris')
    return render_template('inscription.html')

if __name__ == '__main__':
    app.run(debug=True)
