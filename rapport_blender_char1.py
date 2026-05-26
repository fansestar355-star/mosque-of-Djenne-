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
            'color': 'blue_background'
        }
    }

def quote(text):
    return {'object': 'block', 'type': 'quote',
            'quote': {'rich_text': [{'type': 'text', 'text': {'content': text}}]}}

children = [
    callout('Rapport genere automatiquement par Claude Code via Blender MCP le ' + date, '\U0001f916'),

    h1('\U0001f9cd Rigging & Weight Painting - Personnage char1 (Boubou)'),
    p('Session de travail sur le personnage "char1" equipe de l\'armature "Meshy_Walking_Armature". '
      'Le personnage est un homme age portant un boubou bleu traditionnel avec une animation de marche (walking_man). '
      'La session a porte sur le diagnostic complet, la correction de l\'armature et la redistribution des poids.'),
    divider(),

    h2('\U0001f50d 1. Diagnostic initial de la scene'),
    p('Etat de la scene au debut de la session :'),
    bullet('2 objets : Meshy_Walking_Armature (ARMATURE) + char1 (MESH) - tous deux a l\'origine (0,0,0)'),
    bullet('3 materiaux appliques sur le personnage'),
    bullet('Mesh : 39 155 vertices | 97 846 aretes | 59 390 polygones'),
    bullet('24 os dans l\'armature | 24 groupes de sommets correspondants'),
    bullet('0 vertex non assigne - couverture complete'),
    bullet('Animation NLA : "Armature|walking_man|baselayer" - 1 a 25.8 frames'),
    divider(),

    h2('⚠️ 2. Probleme critique detecte : Echelle de l\'armature'),
    p('Probleme identifie lors du diagnostic :'),
    bullet('Echelle armature : 0.01 (non appliquee) - les os etaient 100x trop petits'),
    bullet('Echelle mesh : 1.0 (correcte)'),
    bullet('Consequence : deformations incorrectes lors de la lecture de l\'animation'),
    bullet('Correction : application de l\'echelle via bpy.ops.object.transform_apply(scale=True)'),
    bullet('Resultat : echelle armature passee de 0.01 a 1.0'),
    quote('Tous les vertices etaient correctement assignes (0 vertex orphelin, poids normalises a 1.0). Le probleme etait uniquement l\'echelle non appliquee de l\'armature.'),
    divider(),

    h2('\U0001f9f5 3. Correction de la repartition des poids - Robe (Boubou)'),
    p('Apres correction de l\'echelle, analyse de la repartition des poids sur la robe :'),

    h3('Probleme identifie :'),
    bullet('LeftLeg (tibia gauche) : 18 122 vertices influences | poids moyen 0.372'),
    bullet('RightLeg (tibia droit) : 16 112 vertices influences | poids moyen 0.394'),
    bullet('Hips (bassin) : 9 141 vertices | poids moyen 0.342 - insuffisant pour une robe longue'),
    bullet('Consequence : la robe suivait les jambes individuellement au lieu de flotter naturellement'),

    h3('Methode de correction :'),
    bullet('Identification des vertices "robe" par distance aux os tibias (seuil > 0.08 m)'),
    bullet('10 892 vertices robe identifies | 4 316 vertices peau/corps preserves'),
    bullet('Reduction progressive des tibias selon hauteur Z :'),
    bullet('  Z < 0.30 m (cheville/sol) : reduction 85% de l\'influence tibia'),
    bullet('  Z 0.30-0.50 m (mollet)    : reduction 70%'),
    bullet('  Z 0.50-0.65 m (genou)     : reduction 55%'),
    bullet('  Z 0.65-0.85 m (cuisse)    : reduction 35%'),
    bullet('Redistribution vers : 60% Hips | 25% UpLeg ipsilateral | 15% UpLeg contralateral'),
    bullet('12 044 vertices traites | 302 renormalises en passe finale | 0 vertex mal normalise'),

    h3('Resultats apres correction :'),
    bullet('LeftLeg  : poids moyen 0.205 (-45%)'),
    bullet('RightLeg : poids moyen 0.190 (-52%)'),
    bullet('Hips     : 20 927 vertices influences | poids moyen 0.276 (+128%)'),
    bullet('LeftUpLeg  : 19 683 vertices | poids moyen 0.340'),
    bullet('RightUpLeg : 19 454 vertices | poids moyen 0.335'),
    divider(),

    h2('\U0001f45f 4. Correction des poids - Zone pieds / bas de robe'),
    p('Probleme residuel identifie sur le bas de la robe (Z < 0.20 m) :'),

    h3('Probleme identifie :'),
    bullet('845 vertices du bas de la robe avec influence tibia > 0.5 (tibia dominant)'),
    bullet('Le tissu au sol suivait les chevilles individuelles au lieu du bassin'),
    bullet('Deformations visibles lors des foulees (etirement anguleux en bas de robe)'),

    h3('Methode de correction :'),
    bullet('Distinction robe/sandale par double seuil : dist pied > 0.06 m ET dist tibia > 0.05 m'),
    bullet('Reduction 80% de l\'influence tibia sur les vertices tissu identifies'),
    bullet('Redistribution vers : 55% Hips | 20% UpLegs | 25% Foot gauche+droit'),
    bullet('Ancrage partiel aux os de pied preserve pour un mouvement naturel au sol'),
    bullet('1 000 vertices bas de robe corriges | 0 vertex mal normalise'),

    h3('Resultats apres correction :'),
    bullet('La robe coule comme un boubou traditionnel - unie dans le bas'),
    bullet('Bassin comme conducteur principal du mouvement de la robe'),
    bullet('Balancement naturel aux pieds grace a l\'ancrage partiel Foot'),
    divider(),

    h2('\U0001f4ca 5. Bilan global des corrections'),
    bullet('Total vertices traites (robe + pieds) : ~13 044 vertices'),
    bullet('Tous les poids renormalises : somme = 1.0 pour chaque vertex'),
    bullet('Vertices peau/corps non modifies : preserved avec leurs poids d\'origine'),
    bullet('Methode API utilisee : vertex_group.add([v.index], weight, "REPLACE") - seule methode fiable'),
    divider(),

    h2('\U0001f4bb 6. Outils et methodes utilises'),
    bullet('Connexion : Blender MCP (BlenderMCP panel) - controle Python en temps reel'),
    bullet('API Blender : bpy, bmesh, mathutils.Vector'),
    bullet('Diagnostic : bpy.data.objects, vertex.groups, vertex_group.index'),
    bullet('Distance os : projection point sur segment (parametre t clampe [0,1])'),
    bullet('Ecriture poids : vertex_group.add([idx], weight, "REPLACE") - API officielle'),
    bullet('Verification : somme des poids par vertex pour validation normalisation'),
    divider(),

    h2('✅ Recapitulatif des taches'),
    todo('Diagnostic complet de la scene (objets, os, groupes, poids)', True),
    todo('Detection du probleme d\'echelle armature (0.01 vs 1.0)', True),
    todo('Application de l\'echelle armature via transform_apply', True),
    todo('Analyse de la distribution des poids par os', True),
    todo('Identification des vertices robe par distance aux os', True),
    todo('Redistribution des poids tibias vers Hips/UpLegs (zone robe)', True),
    todo('Correction des poids bas de robe zone pieds', True),
    todo('Renormalisation complete de tous les poids (0 erreur)', True),
    todo('Verification visuelle sur plusieurs frames de l\'animation', True),
    todo('Centrer le modele a l\'origine de la scene', False),
    todo('Configurer la boucle d\'animation correctement', False),
    todo('Exporter le modele corrige en FBX ou GLB', False),
]

page = {
    'parent': {'database_id': DATABASE_ID},
    'properties': {
        'Name': {'title': [{'text': {'content': 'Rapport Blender : Rigging & Weight Painting - char1 Boubou (' + date + ')'}}]},
        'Date': {'date': {'start': date}}
    },
    'children': children
}

body = json.dumps(page).encode('utf-8')
req = urllib.request.Request('https://api.notion.com/v1/pages', data=body, headers=headers, method='POST')
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    print('Page Notion creee :', result.get('url', 'URL inconnue'))
