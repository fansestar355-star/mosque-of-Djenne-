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
            'color': 'yellow_background'
        }
    }

children = [
    callout('Rapport genere automatiquement par Claude Code via Blender MCP le ' + date, '\U0001f916'),
    h1('\U0001f3db Tombeau des Askia - Gao, Mali'),
    p('Le Tombeau des Askia est un monument historique classe au Patrimoine mondial de lUNESCO. '
      'Il est le lieu de sepulture d Askia Mohammad I, l un des empereurs les plus importants de '
      'l Empire Songhoi (XVe-XVIe siecle). La structure en banco (terre crue) est caracteristique '
      'de l architecture soudano-sahelienne.'),
    divider(),

    h2('\U0001f4cd 1. Localisation GPS'),
    bullet('Latitude  : 16.2872 N'),
    bullet('Longitude : -0.0400 E  (0 deg 02 24 W)'),
    bullet('Ville     : Gao, Mali - Region de Gao'),
    bullet('Elevation : 256 m (SRTM 90m)'),
    bullet('Source    : latitude.to / OpenTopoData NASA SRTM'),
    divider(),

    h2('\U0001f5fa 2. Topographie SRTM generee dans Blender'),
    p('Une topographie numerique a ete generee dans Blender a partir des donnees d elevation SRTM '
      '(Shuttle Radar Topography Mission) de la NASA via l API OpenTopoData.'),
    bullet('Grille : 10 x 10 points d elevation (100 points SRTM 90m de resolution)'),
    bullet('Zone couverte : environ 10 km x 5.5 km autour du tombeau'),
    bullet('Elevation reelle : 245 m - 261 m (relief de 16 m, terrain plat typique du Sahel)'),
    bullet('Amplification du relief : x1.5 pour la visibilite dans Blender'),
    bullet('Objet Blender cree : Topographie_Askia (22 x 12 unites Blender)'),
    bullet('Materiau terre applique sur le terrain (couleur sable sahelien)'),
    bullet('Modele 3D positionne au point exact GPS du tombeau sur le terrain'),
    divider(),

    h2('\U0001f9f9 3. Nettoyage geometrique du modele 3D'),
    p('Le modele Mesh_0 (fichier Askia.blend) a ete nettoye de ses artefacts geometriques '
      'directement dans Blender via la connexion MCP :'),
    bullet('726 fragments parasites supprimes (micro-islands de 3 a 47 vertices)'),
    bullet('4 152 vertices parasites elimines'),
    bullet('Mesh principal conserve intact : 92 563 vertices | 184 244 faces'),
    bullet('15 518 aretes non-manifold identifiees et traitees'),
    divider(),

    h2('\U0001f3a8 4. Correction de texture'),
    bullet('Texture Image_0 (2048x2048 px) : zones bleues et cyan remplacees par couleur terre'),
    bullet('Couleur terre echantillonnee directement depuis le modele : R=0.644 G=0.520 B=0.337'),
    bullet('Methode : propagation iterative par voisinage pour integration harmonieuse'),
    bullet('Plus de 280 000 pixels corriges au total (plusieurs passes successives)'),
    bullet('Vegetation verte (arbres) conservee intacte'),
    bullet('Noeud Metallic deconnecte : Image_1.Blue -> Metallic causait des reflets bleus'),
    bullet('Metallic mis a 0 pour supprimer les reflets metalliques indesires'),
    divider(),

    h2('\U0001f4bb 5. Outils et methodes utilises'),
    bullet('Connexion : Blender MCP (port 9876) - controle Python en temps reel'),
    bullet('Elevation : API OpenTopoData (dataset SRTM 90m NASA)'),
    bullet('Coordonnees : latitude.to / UNESCO World Heritage data'),
    bullet('Manipulation image : NumPy (manipulation pixel par pixel)'),
    bullet('Geometrie : BMesh API Blender pour nettoyage des fragments'),
    divider(),

    h2('✅ Recapitulatif des taches'),
    todo('Coordonnees GPS du Tombeau des Askia trouvees (16.2872N, -0.0400E)', True),
    todo('100 points SRTM telecharges via OpenTopoData API', True),
    todo('Topographie 3D creee dans Blender (objet Topographie_Askia)', True),
    todo('Modele 3D positionne sur la topographie au point exact du tombeau', True),
    todo('726 fragments geometriques supprimes du modele', True),
    todo('Texture bleue corrigee par echantillonnage des couleurs voisines', True),
    todo('Noeud Metallic deconnecte pour supprimer les reflets bleus', True),
    todo('Sauvegarder le fichier Askia.blend', False),
    todo('Exporter le modele en GLB pour usage web ou AR', False),
    todo('Appliquer une texture satellite sur la topographie', False),
]

page = {
    'parent': {'database_id': DATABASE_ID},
    'properties': {
        'Name': {'title': [{'text': {'content': 'Rapport 3D : Tombeau des Askia - Topographie & Nettoyage'}}]},
        'Date': {'date': {'start': date}}
    },
    'children': children
}

body = json.dumps(page).encode('utf-8')
req = urllib.request.Request('https://api.notion.com/v1/pages', data=body, headers=headers, method='POST')
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    print('Page Notion creee :', result.get('url', 'URL inconnue'))
