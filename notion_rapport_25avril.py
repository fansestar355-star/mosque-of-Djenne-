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
    return {'object':'block','type':'heading_1',
            'heading_1':{'rich_text':[{'type':'text','text':{'content':text}}]}}

def h2(text):
    return {'object':'block','type':'heading_2',
            'heading_2':{'rich_text':[{'type':'text','text':{'content':text}}]}}

def p(text):
    return {'object':'block','type':'paragraph',
            'paragraph':{'rich_text':[{'type':'text','text':{'content':text}}]}}

def bullet(text):
    return {'object':'block','type':'bulleted_list_item',
            'bulleted_list_item':{'rich_text':[{'type':'text','text':{'content':text}}]}}

def todo(text, checked=False):
    return {'object':'block','type':'to_do',
            'to_do':{'rich_text':[{'type':'text','text':{'content':text}}],'checked':checked}}

def divider():
    return {'object':'block','type':'divider','divider':{}}

def callout(text, emoji):
    return {
        'object':'block','type':'callout',
        'callout':{
            'rich_text':[{'type':'text','text':{'content':text}}],
            'icon':{'type':'emoji','emoji':emoji},
            'color':'blue_background'
        }
    }

children = [
    callout('Rapport genere automatiquement par Claude Code le ' + date, '\U0001f916'),
    h1('\U0001f3db Tombeau des Askia — Session du 25 Avril 2026'),
    p('Session de developpement et de correction de bugs sur la page web interactive '
      'du Tombeau des Askia (Gao, Mali). Travail sur tombeau-3d.html : '
      'performance mobile, audio positionnel, corrections visuelles et slider custom.'),
    divider(),

    h2('\U0001f50a 1. Audio positionnel — Appel a la priere (Adhan)'),
    p('Implementation d un systeme audio positionnel 3D utilisant la Web Audio API.'),
    bullet('Remplacement de HTMLAudioElement par fetch() + ArrayBuffer + decodeAudioData'),
    bullet('URLs Wikimedia Commons (CORS garanti) avec fallback MP3'),
    bullet('AudioContext cree au clic uniquement (politique autoplay navigateur)'),
    bullet('PannerNode HRTF positionne au sommet de la tour pyramidale'),
    bullet('Pre-chargement du buffer audio au chargement du modele'),
    bullet('Correction URL Wikimedia : hash 7/7e remplace par 8/86 (ancienne URL = 404)'),
    bullet('MP3 mis en premier dans la liste (meilleure compatibilite mobile)'),
    divider(),

    h2('\U0001f4f1 2. Optimisations performance mobile'),
    p('Le modele 3D ne se chargeait pas sur mobile — nombreuses corrections apportees.'),
    bullet('Scripts Three.js charges en parallele (Promise.all) au lieu de cascade sequentielle'),
    bullet('Detection IS_MOBILE pour adapter tous les parametres de rendu'),
    bullet('Shadow map desactivee sur mobile (etait 2048x2048 — trop lourd)'),
    bullet('EffectComposer / ShaderPass non charges sur mobile'),
    bullet('Boucle de rendu : renderer.render() direct sur mobile (pas de post-processing)'),
    bullet('Pixel ratio limite a 1.5 sur mobile (au lieu de 2)'),
    bullet('DoubleSide uniquement sur la carte satellite, FrontSide pour le reste'),
    bullet('Anisotropie limitee a 2 sur mobile'),
    bullet('Bouton Mode Dessin masque sur mobile (shader non disponible)'),
    bullet('Progression % GLB visible dans le loader'),
    divider(),

    h2('\U0001f41b 3. Corrections de bugs critiques'),
    bullet('Bug THREE.Vector3 global : new THREE.Vector3() s executait avant le chargement '
           'de Three.js — script entier plantait a la ligne 947'),
    bullet('Bug TDZ _annotations : let _annotations jamais initialise car script plante avant'),
    bullet('Fix : _adhanTowerTop initialise a null, Vector3 cree dans setupAdhan()'),
    bullet('Image illustration d arbre.jpg renommee en illustration-arbre.jpg '
           '(apostrophe dans le nom = 404 sur GitHub Pages)'),
    bullet('Ajout message d erreur visible + bouton Reessayer dans le loader'),
    bullet('Timeout 45 secondes dans startExperience() avec message d erreur'),
    bullet('Decodeur DRACO pointe vers jsDelivr (meme CDN que Three.js) au lieu de gstatic'),
    bullet('Ordre de chargement des scripts post-processing corrige (dependances strictes)'),
    divider(),

    h2('\U0001f333 4. Illustrations 3D dans la scene'),
    bullet('Augmentation visibilite des arbres : taille x2, contraste x9, seuil 170'),
    bullet('Nouvelle tentative : contraste x20, seuil 150, couleur beige chaud'),
    bullet('Suppression des illustrations : lignes de vent, rose des vents, arbres'),
    bullet('Conserve uniquement : soleil et fleche Tour 17m'),
    divider(),

    h2('\U0001f3ae 5. Slider annotations — redesign complet'),
    p('Le slider vertical (cote droit) a ete entierement reecrit car input[type=range] '
      'ne se stylise pas correctement sur mobile.'),
    bullet('Suppression de input[type=range] (non stylisable sur mobile)'),
    bullet('Remplacement par div custom avec touch events natifs (touchstart, touchmove)'),
    bullet('Thumb en forme de diamant dore avec halo lumineux'),
    bullet('Rail fin 1px avec gradient dore montant/descendant en temps reel'),
    bullet('11 tirets decoratifs (5 majeurs, 5 mineurs) sur le rail'),
    bullet('Label pourcentage mis a jour en temps reel au glissement'),
    bullet('Fonctionne parfaitement sur mobile et desktop'),
    divider(),

    h2('\U00002705 Recapitulatif des commits du jour'),
    todo('fix(audio): adhan positionnel via fetch+decodeAudioData (Wikimedia Commons)', True),
    todo('perf(mobile): chargement parallele, rendu allege, pas de post-processing', True),
    todo('fix: THREE.Vector3 global causait ReferenceError + TDZ _annotations', True),
    todo('fix: URL audio Wikimedia corrigee + image arbre renommee (sans apostrophe)', True),
    todo('fix(mobile): erreurs visibles + timeout + DRACO via jsDelivr + scripts ordonnes', True),
    todo('feat: arbres 2x plus grands, contraste x9, seuil 170', True),
    todo('feat: arbres reduits a l echelle du modele, contraste x9, seuil 170', True),
    todo('feat: arbres — seuil 150, facteur x20, couleur beige chaud bien visible', True),
    todo('feat: supprime vent, rose des vents et arbres — garde soleil + fleche Tour 17m', True),
    todo('feat: slider annotations redesigne — piste fine, thumb dore, icones', True),
    todo('feat: slider entierement custom (div + touch events) — diamant dore, tirets deco', True),
    divider(),

    h2('\U0001f517 Informations projet'),
    bullet('Repository GitHub : https://github.com/fansestar355-star/tombeau-des-askia'),
    bullet('Fichier principal modifie : tombeau-3d.html'),
    bullet('Branche : master'),
    bullet('Dernier commit : 4fafe1d'),
]

page = {
    'parent': {'database_id': DATABASE_ID},
    'properties': {
        'Name': {'title': [{'text': {'content': 'Rapport Dev : Tombeau des Askia — Session 25 Avril 2026'}}]},
        'Date': {'date': {'start': date}}
    },
    'children': children
}

body = json.dumps(page).encode('utf-8')
req = urllib.request.Request(
    'https://api.notion.com/v1/pages',
    data=body, headers=headers, method='POST'
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    print('Page Notion creee :', result.get('url', 'URL inconnue'))
