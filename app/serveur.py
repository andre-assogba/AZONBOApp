# -*- coding: utf-8 -*-
# AZONBOApp v1.3
# Andre Marc ASSOGBA

from flask import Flask, render_template, request, session, redirect, url_for
from db import initialiser, supprimer_vente, annuler_vente, get_articles_session, get_credit_session, get_produit, get_user_id, lister_produits, ajouter_produit, creer_session, ajouter_vente, lister_sessions, lister_dettes, get_dette, rechercher_dettes, enregistrer_remboursement, lister_remboursements, modifier_vente, modifier_quantites_vente, get_articles_session, verifier_utilisateur, get_resume, modifier_produit, supprimer_produit
from ventes import Vente
from validation import valider_login, valider_inscription, valider_client, valider_paiement, valider_quantite_vente, valider_remboursement, valider_modification_vente
from datetime import datetime

app = Flask(__name__)
import os
app.secret_key = os.environ.get('SECRET_KEY', 'azonbo_secret_2026')
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
    from datetime import datetime, timedelta
    erreur = None
    tentatives = session.get('tentatives', 0)
    blocage = session.get('blocage')
    if blocage:
        if datetime.now() < datetime.fromisoformat(blocage):
            erreur = 'Compte bloque 15 minutes. Reessayez plus tard.'
            return render_template('login.html', erreur=erreur)
        else:
            session.pop('tentatives', None)
            session.pop('blocage', None)
            tentatives = 0
    if request.method == 'POST':
        nom = request.form.get('nom', '')
        mdp = request.form.get('mot_de_passe', '')
        ok, msg = valider_login(nom, mdp)
        if not ok:
            return render_template('login.html', erreur=msg)
        user_id = verifier_utilisateur(nom, mdp)
        if user_id:
            session['utilisateur'] = nom
            session.pop('tentatives', None)
            session.pop('blocage', None)
            return redirect(url_for('menu'))
        else:
            tentatives += 1
            session['tentatives'] = tentatives
            if tentatives >= 5:
                session['blocage'] = (datetime.now() + timedelta(minutes=15)).isoformat()
                erreur = 'Trop de tentatives. Reessayez dans 15 minutes.'
            else:
                erreur = f'Nom ou mot de passe incorrect. Tentative {tentatives}/5.'
    return render_template('login.html', erreur=erreur)

@app.route('/offline')
def offline():
    return render_template('offline.html')

@app.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect(url_for('login'))

@app.route('/')
def menu():
    from datetime import datetime
    date = datetime.now().strftime('%d/%m/%Y')
    ventes, dettes = get_resume(uid(), date)
    ventes = (ventes[0], int(ventes[1] or 0))
    dettes = (dettes[0], int(dettes[1] or 0))
    nom = session.get('utilisateur', '')
    return render_template('menu.html', ventes=ventes, dettes=dettes, nom=nom, date=date)

@app.route('/produits')
def produits():
    p = lister_produits(uid())
    return render_template('produits.html', produits=p)

@app.route('/produits/ajouter', methods=['POST'])
def ajouter_produit_route():
    from validation import valider_produit
    ok, resultat = valider_produit(
        request.form.get('nom',''),
        request.form.get('prix',''),
        request.form.get('quantite',''),
        request.form.get('seuil','')
    )
    if not ok:
        p = lister_produits(uid())
        return render_template('produits.html', produits=p, erreur=resultat)
    ajouter_produit(uid(), resultat['nom'], resultat['prix'], resultat['qte'], resultat['seuil'])
    return redirect(url_for('produits'))

@app.route('/ventes')
def ventes():
    sessions = lister_sessions(uid())
    return render_template('ventes.html', sessions=sessions)

@app.route('/ventes/nouvelle', methods=['GET', 'POST'])
def nouvelle_vente():
    produits = lister_produits(uid())
    if request.method == 'POST':
        ok_c, client = valider_client(request.form.get('client', ''))
        if not ok_c:
            return render_template('nouvelle_vente.html', produits=produits, erreur=client)
        mode = request.form.get('paiement', 'cash')
        produits_sel = request.form.getlist('produit_id')
        quantites = request.form.getlist('quantite')
        articles_valides = []
        for pid, qte_str in zip(produits_sel, quantites):
            if not qte_str or not qte_str.strip() or int(qte_str) == 0:
                continue
            p = get_produit(int(pid))
            if p:
                ok_q, qte = valider_quantite_vente(qte_str, p[3], p[1])
                if not ok_q:
                    return render_template('nouvelle_vente.html', produits=produits, erreur=qte)
                articles_valides.append((p, qte))
        if not articles_valides:
            return render_template('nouvelle_vente.html', produits=produits, erreur='Selectionnez au moins un produit avec une quantite.')
        total_tmp = sum(p[2] * q for p, q in articles_valides)
        ok_p, avance = valider_paiement(mode, request.form.get('avance',''), total_tmp)
        if not ok_p:
            return render_template('nouvelle_vente.html', produits=produits, erreur=avance)
        v = Vente(client, mode)
        for p, qte in articles_valides:
            v.ajouter_produit(p[0], p[1], p[2], qte)
        date = datetime.now().strftime('%d/%m/%Y %H:%M')
        sid = creer_session(uid(), v.client, date, v.total, v.mode)
        for item in v.produits:
            ajouter_vente(sid, item['id'], item['quantite'], item['total'])
        if v.mode in ('credit', 'partiel'):
            from db import ajouter_dette
            avance = int(request.form.get('avance') or 0)
            reste = v.total - avance
            ajouter_dette(uid(), sid, v.client, v.total, date, reste, request.form.get('telephone', ''))
        return redirect(url_for('facture', sid=sid))
    return render_template('nouvelle_vente.html', produits=produits, erreur=None)

@app.route('/resume')
def resume():
    date = datetime.now().strftime('%d/%m/%Y')
    ventes, dettes = get_resume(uid(), date)
    ventes = (ventes[0], int(ventes[1] or 0))
    dettes = (dettes[0], int(dettes[1] or 0))
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
    recherche = False
    if request.method == 'POST':
        client = request.form.get('nom', '').strip()
        if client:
            liste = rechercher_dettes(uid(), client)
            recherche = True
        else:
            liste = lister_dettes(uid())
    else:
        liste = lister_dettes(uid())
    return render_template('dettes.html', dettes=liste, client=client, recherche=recherche)

@app.route('/dettes/<int:cid>')
def dette_detail(cid):
    d = get_dette(cid)
    r = lister_remboursements(cid)
    return render_template('dette_detail.html', dette=d, remboursements=r)

@app.route('/dettes/<int:cid>/rembourser', methods=['POST'])
def rembourser(cid):
    from db import get_dette
    d = get_dette(cid)
    if not d:
        return redirect(url_for('dettes'))
    ok, resultat = valider_remboursement(request.form.get('montant',''), d[3])
    if not ok:
        from db import lister_remboursements
        r = lister_remboursements(cid)
        return render_template('dette_detail.html', dette=d, remboursements=r, erreur=resultat)
    enregistrer_remboursement(cid, resultat)
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
    articles = get_articles_session(sid)
    if request.method == 'POST':
        ok, resultat = valider_modification_vente(
            request.form.get('client',''),
            request.form.get('paiement','')
        )
        if not ok:
            articles = get_articles_session(sid)
            s = lister_sessions(uid())
            session_data = next((x for x in s if x[0] == sid), None)
            produits = lister_produits(uid())
            quantites = {a[3]: a[1] for a in articles}
            return render_template('modifier_vente.html', sid=sid, s=session_data, produits=produits, quantites=quantites, erreur=resultat)
        client = resultat['client']
        mode = resultat['mode']
        modifier_vente(sid, client, mode)
        articles_form = [(int(k.split('_')[1]), int(v)) for k, v in request.form.items() if k.startswith('qte_') and v.strip() != '' and int(v) > 0]
        modifier_quantites_vente(sid, articles_form)
        return redirect(url_for('ventes'))
    s = lister_sessions(uid())
    session_data = next((x for x in s if x[0] == sid), None)
    produits = lister_produits(uid())
    quantites = {a[3]: a[1] for a in articles}
    return render_template('modifier_vente.html', sid=sid, s=session_data, produits=produits, quantites=quantites)


@app.route('/produits/<int:pid>/modifier', methods=['POST'])
def modifier_produit_route(pid):
    from validation import valider_produit
    prix_achat = float(request.form.get('prix_achat', 0) or 0)
    ok, resultat = valider_produit(request.form.get('nom',''), request.form.get('prix',''), request.form.get('quantite',''), request.form.get('seuil',''))
    if not ok:
        p = lister_produits(uid())
        return render_template('produits.html', produits=p, erreur=resultat)
    modifier_produit(pid, resultat['nom'], resultat['prix'], prix_achat, resultat['qte'], resultat['seuil'])
    return redirect(url_for('produits'))

@app.route('/produits/<int:pid>/supprimer', methods=['POST'])
def supprimer_produit_route(pid):
    supprimer_produit(pid, uid())
    return redirect(url_for('produits'))

@app.route('/inscription', methods=['GET','POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom', '')
        mdp = request.form.get('mot_de_passe', '')
        ok, resultat = valider_inscription(nom, mdp)
        if not ok:
            return render_template('inscription.html', erreur=resultat)
        from db import s_inscrire
        ok = s_inscrire(resultat['nom'], resultat['mdp'])
        if ok:
            return redirect('/login?inscrit=1')
        return render_template('inscription.html', erreur='Nom deja pris')
    return render_template('inscription.html')


@app.route('/historique_client', methods=['GET', 'POST'])
def historique_client_route():
    from db import historique_client
    resultats = []
    nom = ''
    if request.method == 'POST':
        nom = request.form.get('nom', '')
        if nom:
            rows = historique_client('%' + nom + '%', uid())
            ventes = {}
            vrai_nom = nom
            for r in rows:
                sid = r[0]
                if sid not in ventes:
                    ventes[sid] = {'date': r[1], 'total': r[2], 'paiement': r[3], 'articles': [], 'client': r[7] if len(r) > 7 else nom, 'statut': r[8] if len(r) > 8 else 'active'}
                ventes[sid]['articles'].append({'nom': r[4], 'qte': r[5], 'total': r[6]})
            if rows:
                nom = rows[0][7]
            resultats = ventes
    return render_template('historique_client.html', resultats=resultats, nom=nom)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/ventes/<int:sid>/supprimer', methods=['POST'])
def supprimer_vente_route(sid):
    from db import supprimer_vente
    supprimer_vente(sid, uid())
    return redirect(url_for('ventes'))

@app.route('/ventes/<int:sid>/confirmer-annulation')
def confirmer_annulation(sid):
    s = lister_sessions(uid())
    session_data = next((x for x in s if x[0] == sid), None)
    return render_template('confirmer_annulation.html', sid=sid, s=session_data)

@app.route('/ventes/<int:sid>/annuler', methods=['POST'])
def annuler_vente_route(sid):
    annuler_vente(sid, uid())
    return redirect(url_for('ventes'))
