import urllib.request, json
from datetime import datetime

TOKEN = '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'
DATABASE_ID = '65073e08-97ca-4c60-9cf2-da1078736240'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

date = datetime.now().strftime('%Y-%m-%d')

def h1(text):
    return {'object':'block','type':'heading_1','heading_1':{'rich_text':[{'type':'text','text':{'content':text}}]}}
def h2(text):
    return {'object':'block','type':'heading_2','heading_2':{'rich_text':[{'type':'text','text':{'content':text}}]}}
def p(text):
    return {'object':'block','type':'paragraph','paragraph':{'rich_text':[{'type':'text','text':{'content':text}}]}}
def bullet(text):
    return {'object':'block','type':'bulleted_list_item','bulleted_list_item':{'rich_text':[{'type':'text','text':{'content':text}}]}}
def todo(text, checked=False):
    return {'object':'block','type':'to_do','to_do':{'rich_text':[{'type':'text','text':{'content':text}}],'checked':checked}}
def divider():
    return {'object':'block','type':'divider','divider':{}}
def callout(text, emoji):
    return {'object':'block','type':'callout','callout':{'rich_text':[{'type':'text','text':{'content':text}}],'icon':{'type':'emoji','emoji':emoji},'color':'purple_background'}}

children = [
    callout('Rapport genere automatiquement par Claude Code le ' + date, '\U0001f916'),
    p('Site : https://fansestar355-star.github.io/tombeau-des-askia/'),
    divider(),

    h1('\U0001f4f1 1. Positionnement modele 3D sur mobile'),
    p('Correction du bug camera-target et ajustement de la position du modele sur petit ecran.'),
    bullet('Correction bug inversion : camera-target Y positif = descend, negatif = monte'),
    bullet('Valeur finale camera-target : 0m 0m 0m (origine du modele)'),
    bullet('Suppression offset X qui empechait la rotation naturelle entre chapitres'),
    bullet('Le modele tourne desormais sur son propre axe comme sur desktop'),
    divider(),

    h1('\U0001f4cf 2. Taille et zoom du modele mobile'),
    bullet('Reduction du multiplicateur de zoom de x2.8 a x2.0 -> modele plus grand a lecran'),
    bullet('Meme parametres appliques aux deux modeles (real et draw)'),
    divider(),

    h1('\U0001f3a8 3. Harmonisation modele Draw avec modele Real'),
    h2('Redimensionnement GLB dans Blender'),
    bullet('Dimensions originales Askia_Mohamed_draw.glb : 3.40 x 2.59 x 3.86 m'),
    bullet('Centre original decale a Z=1.90m (hors origine)'),
    bullet('Dimensions finales apres mise a echelle : 1.69 x 1.29 x 1.92 m'),
    bullet('Recentre a lorigine (0, 0, 0) et re-exporte en GLB'),
    h2('Camera et exposition'),
    bullet('switchModel() corrige : camera du chapitre actuel restauree au changement de modele'),
    bullet('Exposition differenciee : 0.65 draw (blanc/esquisse), 1.0 real (colore)'),
    divider(),

    h1('\U0001f4f2 4. Ameliorations experience mobile'),
    bullet('Direction scroll inversee : swipe vers le haut = chapitre suivant'),
    bullet('Suppression du bouton Enquete historique sur tous les ecrans'),
    divider(),

    h1('\U0001f4ca 5. Indicateur Swipe — 3 iterations'),
    h2('v1 : Chevrons simples — abandonne'),
    bullet('Deux chevrons animes, trop basique'),
    h2('v2 : Icone souris + doigt — abandonne'),
    bullet('Souris animee desktop, main mobile, pas assez attractif'),
    h2('v3 : Barre de progression droite (version finale)'),
    bullet('Barre verticale sur le bord droit, toujours visible'),
    bullet('3 chevrons ^ en cascade -> direction swipe vers le haut'),
    bullet('Progression chapitres : 33% -> 66% -> 100% avec transition fluide'),
    bullet('Dot lumineux violet avec effet glow qui glisse le long de la barre'),
    bullet('Chevrons seteignent au dernier chapitre'),
    divider(),

    h1('✅ Recapitulatif des taches'),
    todo('Bug camera-target mobile corrige', True),
    todo('Modele draw redimensionne (Blender) aux dimensions du real', True),
    todo('Modele draw recentre a lorigine (0,0,0)', True),
    todo('switchModel() corrige pour camera et exposition', True),
    todo('Direction scroll mobile inversee', True),
    todo('Bouton Enquete historique supprime', True),
    todo('Indicateur swipe redesigne (barre + chevrons)', True),
    todo('Indicateur visible jusqu a la fin de lexperience', True),
    todo('11 commits deployes sur GitHub Pages', True),
    divider(),

    h1('\U0001f527 Outils utilises'),
    bullet('Claude Code (IA) + Blender MCP'),
    bullet('@google/model-viewer : camera-orbit, camera-target, exposure'),
    bullet('GSAP 3.12.2 : animations transitions chapitres'),
    bullet('Blender Python API : redimensionnement et recentrage GLB'),
    bullet('CSS keyframes : animations chevrons, dot glow, barre progression'),
    bullet('GitHub Pages : deploiement continu (master branch)'),
    divider(),

    h2('\U0001f517 Commits GitHub'),
    bullet('11 commits cette session : 403d353 -> 88c49cd'),
    bullet('Fichiers : index.html, assets/3d/Askia_Mohamed_draw.glb'),
]

page = {
    'parent': {'database_id': DATABASE_ID},
    'properties': {
        'Name': {'title': [{'text': {'content': 'Session 23/04 - Tombeau des Askia : Mobile & Indicateur Swipe'}}]},
        'Date': {'date': {'start': date}}
    },
    'children': children
}

body = json.dumps(page).encode('utf-8')
req = urllib.request.Request('https://api.notion.com/v1/pages', data=body, headers=headers, method='POST')
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    print('Page creee :', result.get('url', 'URL inconnue'))
