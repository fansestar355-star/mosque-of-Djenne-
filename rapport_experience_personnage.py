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
    return {'object': 'block', 'type': 'heading_1',
            'heading_1': {'rich_text': [{'type': 'text', 'text': {'content': text}}]}}

def h2(text):
    return {'object': 'block', 'type': 'heading_2',
            'heading_2': {'rich_text': [{'type': 'text', 'text': {'content': text}}]}}

def h3(text):
    return {'object': 'block', 'type': 'heading_3',
            'heading_3': {'rich_text': [{'type': 'text', 'text': {'content': text}}]}}

def p(text):
    return {'object': 'block', 'type': 'paragraph',
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content': text}}]}}

def bullet(text):
    return {'object': 'block', 'type': 'bulleted_list_item',
            'bulleted_list_item': {'rich_text': [{'type': 'text', 'text': {'content': text}}]}}

def todo(text, checked=False):
    return {'object': 'block', 'type': 'to_do',
            'to_do': {'rich_text': [{'type': 'text', 'text': {'content': text}}], 'checked': checked}}

def divider():
    return {'object': 'block', 'type': 'divider', 'divider': {}}

def callout(text, emoji):
    return {
        'object': 'block', 'type': 'callout',
        'callout': {
            'rich_text': [{'type': 'text', 'text': {'content': text}}],
            'icon': {'type': 'emoji', 'emoji': emoji},
            'color': 'orange_background'
        }
    }

def quote(text):
    return {'object': 'block', 'type': 'quote',
            'quote': {'rich_text': [{'type': 'text', 'text': {'content': text}}]}}

children = [
    callout('Rapport genere automatiquement par Claude Code le ' + date, '\U0001f916'),

    h1('\U0001f3dc Experience Personnage — Environnement Desertique Askia Mohamed'),
    p('Session de travail sur experience-personnage.html : correction des bugs de deplacement '
      'et d\'orientation du personnage, ajout d\'effets atmospheriques de vent de sable '
      'en 3 couches avec brouillard exponentiel dynamique et voile CSS.'),
    divider(),

    h2('\U0001f41e 1. Corrections de bugs — Deplacement et orientation'),
    p('Le personnage reculait en marchant et etait mal oriente par rapport a la camera.'),

    h3('Bug 1 : personnage qui marche a reculons'),
    bullet('Cause : signes inverses dans le calcul du deplacement (position -= sin/cos au lieu de +=)'),
    bullet('Fix : position.x += Math.sin(rotation.y) * WALK_SPEED * dt pour "avancer"'),
    bullet('Fix : position.x -= Math.sin(rotation.y) * WALK_SPEED * dt pour "reculer"'),
    quote('Le modele char1_walking.glb fait face au +Z local (export Blender standard) : '
          'avancer = se deplacer dans la direction (sin, cos) du rotation.y courant.'),

    h3('Bug 2 : camera qui voit la face du personnage (3eme personne incorrecte)'),
    bullet('Cause : le personnage charge avec rotation.y = 0, donc face vers +Z = vers la camera (z=5)'),
    bullet('Fix : character.rotation.y = Math.PI apres scene.add(character)'),
    bullet('Effet : personnage face vers -Z, camera voit le dos (vue 3eme personne standard)'),
    bullet('Consequence : les controles gauche/droite sont maintenant coherents depuis la camera'),
    quote('Avec rotation.y = PI : "gauche" (rotation.y +=) tourne vers la gauche de la camera, '
          '"avancer" eloigne le personnage de la camera. Tout est cohérent.'),
    divider(),

    h2('\U0001f32a 2. Effets de vent de sable — Systeme 3 couches (version finale)'),
    p('Refonte complete du systeme de particules pour simuler un desert saharien avec '
      'vent dynamique, brouillard exponentiel et voile atmospherique.'),

    h3('Texture des grains (canvas procedural) :'),
    bullet('Fonction mkSandTex(sz) : canvas HTML avec gradient radial doux'),
    bullet('texSmall (32x32 px) : grains fins pour les couches sol et mi-hauteur'),
    bullet('texLarge (64x64 px) : taches douces pour la brume haute'),
    bullet('Gradient : blanc chaud centre (255,218,118) -> ocre (205,140,45) -> transparent'),
    bullet('THREE.CanvasTexture convertit le canvas en texture GPU'),

    h3('Couche 1 — Sable ras du sol (2 200 particules) :'),
    bullet('Hauteur : 0 a 0.55 m (ras du sol, simule le sable qui file)'),
    bullet('Vitesse : wx (vent principal) + turbulence individuelle 1.3 * sin(t + phase[i])'),
    bullet('PointsMaterial : size 0.055, opacity 0.70, alphaTest 0.01, depthWrite false'),
    bullet('Recyclage : les particules qui sortent de 45 m autour de la camera re-entrent de l\'autre cote'),

    h3('Couche 2 — Tourbillons mi-hauteur (900 particules) :'),
    bullet('Hauteur : 0.4 a 6.5 m (poussiere soulevee par le vent)'),
    bullet('Vitesse : wx * 0.55 + turbulence 0.9 * sin(t * 0.65 + phase[i])'),
    bullet('Oscillation verticale : 0.15 * sin(t * 0.85 + phase[i]) — mouvement en vague'),
    bullet('PointsMaterial : size 0.14, opacity 0.28'),

    h3('Couche 3 — Brume de poussiere haute (400 particules) :'),
    bullet('Hauteur : 5 a 26 m (haze doree qui flotte dans le ciel)'),
    bullet('Vitesse tres lente : wx * 0.22 — particules quasi-statiques'),
    bullet('PointsMaterial : size 0.65, opacity 0.10, alphaTest 0.005'),
    bullet('Zone de recyclage : 100 m autour de la camera'),

    h3('Vent dynamique — fonctions organiques :'),
    bullet('getWx(t) = 5.5 + 2.4*sin(t*0.07) + 1.1*sin(t*0.18) + 0.5*sin(t*0.41)'),
    bullet('getWz(t) = 1.1*sin(t*0.11) + 0.6*sin(t*0.29)'),
    bullet('Chaque particule a une phase individuelle gPh[i] stockee en Float32Array'),
    bullet('Turbulence par couche : amplitude et frequence differentes pour chaque layer'),
    quote('Le vent n\'est pas constant : les rafales s\'accelerent et ralentissent de facon '
          'organique, differente par couche. Les particules ne bougent pas toutes ensemble.'),
    divider(),

    h2('\U0001f32b 3. Brouillard exponentiel dynamique (FogExp2)'),
    p('Remplacement du THREE.Fog lineaire par THREE.FogExp2 pour un rendu plus naturel.'),

    bullet('Ancienne configuration : THREE.Fog(0xd4b87a, near=120, far=380) — lineaire'),
    bullet('Nouvelle configuration : THREE.FogExp2(0xc8a068, density=0.005) — exponentiel'),
    bullet('Formule : opacity = e^(-density * distance) — plus naturel que lineaire'),
    bullet('A 100 m : ~60% visible | A 200 m : ~37% visible | A 300 m : ~22% visible'),

    h3('Pulsation des rafales :'),
    bullet('gust = 0.5 + 0.38*sin(t*0.08) + 0.14*sin(t*0.23) — oscillation double'),
    bullet('scene.fog.density = 0.0025 + gust * 0.006 — varie entre 0.0025 et 0.0085'),
    bullet('Periode principale ~78 s, periode secondaire ~27 s — rythme non repetitif'),
    quote('Le brouillard s\'epaissit lors des rafales et se dissipe dans les accalmies.'),
    divider(),

    h2('\U0001f3a8 4. Voile de sable — Overlay CSS'),
    p('Un div fixe avec gradient dore en bas d\'ecran dont l\'opacite suit les rafales.'),

    bullet('Gradient : rgba(190,128,40) en bas -> transparent a 55% de hauteur'),
    bullet('Transition CSS 0.8s ease pour un fondu naturel entre les valeurs'),
    bullet('Opacite calculee : 0.25 + gust * 0.55 — varie entre 0.25 et 0.80'),
    bullet('z-index 6 (au-dessus de la scene, en-dessous du HUD)'),
    quote('Le voile s\'intensifie lors des bourrasques, simulant le sable qui remonte depuis le sol.'),
    divider(),

    h2('\U0001f50a 5. Sons de pas — Ajoutes puis supprimes'),
    p('Synthese Web Audio API en 3 couches ajoutee puis retiree a la demande.'),

    bullet('Implementation : oscillateur sinus grave + bruit bandpass + queue haute frequence'),
    bullet('Alternance L/R via StereoPannerNode (pan +-0.14) pour simuler gauche/droite'),
    bullet('Decision finale : sons supprimes (non conserves dans la version finale)'),
    divider(),

    h2('\U0001f4bb 6. Outils et methodes utilises'),
    bullet('THREE.FogExp2 : brouillard exponentiel (remplace THREE.Fog lineaire)'),
    bullet('THREE.CanvasTexture : textures procedurales pour les grains de sable'),
    bullet('THREE.PointsMaterial : map + alphaTest + depthWrite:false pour sprites transparents'),
    bullet('Float32Array par-particule : positions + phases individuelles de turbulence'),
    bullet('CSS overlay dynamique : gradient dore en bas, opacite pilotee par JS'),
    bullet('Fonctions sin multi-frequences : vent organique non periodique'),
    divider(),

    h2('✅ Recapitulatif des taches — Session 2026-04-25'),
    todo('Fix : personnage marchait a reculons (signes += / -= inverses)', True),
    todo('Fix : personnage faisait face a la camera (rotation.y = Math.PI)', True),
    todo('Fix : controles gauche/droite coherents apres correction orientation', True),
    todo('Effets de vent de sable v1 (2 couches simples)', True),
    todo('Sons de pas dans le sable (Web Audio API 3 couches)', True),
    todo('Suppression des sons de pas (decision utilisateur)', True),
    todo('Refonte complete vent de sable : 3 couches + textures canvas', True),
    todo('Vent dynamique multi-frequences avec phase individuelle par particule', True),
    todo('Brouillard lineaire -> FogExp2 avec pulsation de densite', True),
    todo('Voile CSS dore en bas d\'ecran, opacite pilotee par les rafales', True),
    todo('Ajouter une musique d\'ambiance desertique (vent, dunes)', False),
    todo('Ajouter panneau d\'information sur le Tombeau des Askia', False),
    todo('Appliquer une texture satellite sur le sol de la ville', False),
]

page = {
    'parent': {'database_id': DATABASE_ID},
    'properties': {
        'Name': {'title': [{'text': {'content': 'Rapport Three.js : Environnement Desertique & Bugs (' + date + ')'}}]},
        'Date': {'date': {'start': date}}
    },
    'children': children
}

body = json.dumps(page).encode('utf-8')
req = urllib.request.Request('https://api.notion.com/v1/pages', data=body, headers=headers, method='POST')
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    print('Page Notion creee :', result.get('url', 'URL inconnue'))
