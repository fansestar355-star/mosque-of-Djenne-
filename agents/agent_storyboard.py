"""
Agent 3 : Storyboard et Storytelling WebAR
- Analyse les recherches faites par Agent 1
- Connait les projets existants pour creer quelque chose de MIEUX
- Cree un storyboard detaille dans Notion
- Genere un prompt precis pour Agent Code
"""

import urllib.request
import json
from datetime import datetime

NOTION_TOKEN = "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"
DATABASE_ID  = "65073e08-97ca-4c60-9cf2-da1078736240"

# References WebAR de classe mondiale pour s'inspirer (sans copier)
REFERENCES_WEBAR = [
    {
        "nom": "Google Arts & Culture - Art Selfie AR",
        "concept": "L'utilisateur se prend en photo et se voit transforme en oeuvre d'art historique",
        "lecon": "Le selfie comme porte d'entree vers la culture - rend l'histoire personnelle"
    },
    {
        "nom": "Musee du Louvre - WebAR Nuit des Musees",
        "concept": "Pointer vers une oeuvre = voir son histoire animee en overlay AR",
        "lecon": "L'objet reel devient declencheur de narration"
    },
    {
        "nom": "8th Wall - Monument Valley AR",
        "concept": "Architecture impossible qui se deroule dans l'espace reel autour de toi",
        "lecon": "L'architecture peut defier la physique pour creer de la magie"
    },
    {
        "nom": "Niantic Lightship - Experiences de lieu",
        "concept": "Un lieu reel devient un monde enrichi : des entites vivent dans ton environnement",
        "lecon": "Ancrer l'experience dans le lieu reel cree une connexion emotionnelle forte"
    }
]

# Templates de storyboard par type d'architecture
TEMPLATES_STORYBOARD = {
    "tombeau": {
        "concept_central": "LE RÉVEIL DE L'EMPIRE — Le Tombeau des Askia te convoque à travers les siècles pour témoigner de la grandeur de l'Empire Songhaï. Un voyage de 120 secondes qui grave l'histoire dans ta mémoire.",
        "arc_emotionnel": "Mystère → Révélation → Émerveillement → Fierté → Appartenance",
        "scenes": [
            {
                "num": 1,
                "titre": "L'Appel du Sahel — Le désert parle",
                "duree": "0-8 secondes",
                "description": "Écran noir total. Silence. Puis, une voix de griot en langue songhaï murmure une incantation (sous-titrée). Des particules de sable ocre et rouge émergent du néant, tourbillonnant en spirale. Elles dessinent progressivement la silhouette de la pyramide de 17 mètres. La lumière chaude du soleil sahélien perce l'obscurité. L'utilisateur réalise qu'il est à Gao, en 1495.",
                "emotion": "Mystère, curiosité, hypnose",
                "interaction": "Aucune — scène cinématique d'ouverture. L'utilisateur est spectateur.",
                "techno": "Three.js BufferGeometry particles (50 000 points), custom vertex shader sand-storm, AudioContext griot voice, GSAP timeline, fog shader",
                "details_visuels": "Fond #050505 (noir total identité Takienta/Toguna). Particules sable : #D2691E (terre banco) virant vers #f9d58b (or ambre). Silhouette pyramidale en pointillés #f9d58b pulsant sur fond #0d0810.",
                "details_sonores": "Voix griot songhaï + vent Sahel (basse fréquence) + silence progressif vers une note de kora"
            },
            {
                "num": 2,
                "titre": "La Matière Vivante — Le banco se souvient",
                "duree": "8-25 secondes",
                "description": "La pyramide complète se matérialise, grain par grain, comme si la terre se souvenait de sa propre forme. La texture banco est ultra-réaliste : argile, paille, empreintes de mains. Les torons de bois de rônier scintillent légèrement. Des annotations lumineuses flottent autour : '1495', 'Askia Mohamed', 'Empire Songhaï'. L'utilisateur peut pincer pour zoomer et voir les détails de la construction.",
                "emotion": "Émerveillement, respect, stupéfaction architecturale",
                "interaction": "Pinch to zoom, drag to rotate (OrbitControls). Taper sur le monument déclenche un vibration haptique + son de terre battue.",
                "techno": "GLTFLoader + DRACOLoader, MeshStandardMaterial avec normalMap banco, CSS2DRenderer pour annotations, morphTargets pour apparition progressive, EnvironmentMap sahélien",
                "details_visuels": "Fond scène #0d0810 (identité partagée). Matériau banco : #D2691E roughness 0.9, normalMap haute densité. Annotations flottantes : texte #f9d58b sur fond #55415d semi-transparent. Lumière soleil #f9d58b (angle 35°). Torons bois : #8B6914.",
                "details_sonores": "Son sourd de terre battue au tap. Vent doux du désert en fond."
            },
            {
                "num": 3,
                "titre": "Les Mains des Bâtisseurs — 1495",
                "duree": "25-50 secondes",
                "description": "Des mains semi-transparentes et dorées apparaissent sur le monument — les mains des artisans de 1495. Elles appliquent le banco, posent les briques, lissent les surfaces. Chaque zone touchée par les mains s'illumine brièvement. En parallèle, une barre de progression subtile indique 'Construction : 1495'. Au bout de quelques secondes, un groupe de silhouettes stylisées (maçons, femmes portant l'eau, enfants) entoure le chantier. Askia Mohamed lui-même apparaît en silhouette dorée lumineuse au premier plan, regardant son œuvre.",
                "emotion": "Connexion humaine, fierté ancestrale, gratitude",
                "interaction": "Toucher les zones illuminées = voir une micro-animation de construction et entendre une phrase du griot. 3 zones : la base, le corps pyramidal, le sommet.",
                "techno": "SkinnedMesh pour les mains animées, InstancedMesh pour les silhouettes de foule, raycasting zones interactives, ParticleSystem dorée au contact, Timeline GSAP synchronisée",
                "details_visuels": "Mains : MeshBasicMaterial #f9d58b semi-transparent (opacity 0.6) — même couleur accent que Takienta/Toguna. Silhouettes foule : #2b2b3b avec outline #f9d58b. Askia Mohamed : silhouette #f9d58b lumineux avec halo #55415d. Zones interactives : bordure #f9d58b pulsante.",
                "details_sonores": "Sons de construction banco : frottement terre, claquements de mains, voix collectives. Griot récite 3 phrases historiques au tap."
            },
            {
                "num": 4,
                "titre": "L'Empire à Son Apogée — Gao Médiévale",
                "duree": "50-80 secondes",
                "description": "Transition épique : la caméra s'élève lentement. La ville de Gao médiévale se déploie autour du tombeau — mosquée adjacente, palais royal, marché trans-saharien, caravanes de chameaux chargés d'or et de sel. Des routes lumineuses partent dans toutes les directions (routes caravanières vers Tombouctou, l'Egypte, le Maroc). Le ciel vire au coucher de soleil intense. Des particules d'or flottent dans l'air. La musique atteint son apogée : kora + ngoni + percussions djembé.",
                "emotion": "Grandeur, fierté, émerveillement civilisationnel",
                "interaction": "Swipe horizontal pour explorer la ville médiévale. Cliquer sur les caravanes = voir les marchandises (or, sel, manuscrits). Cliquer sur les routes = voir la destination.",
                "techno": "Three.js scene dynamique avec LOD (Level of Detail), InstancedMesh pour caravanes et personnages, LineSegments pour les routes lumineuses, ShaderMaterial sunset sky, GSAP camera dolly up, PostProcessing bloom sur les particules d'or",
                "details_visuels": "Ciel sunset : gradient #D2691E (banco) vers #55415d (violet identité) vers #050505. Particules d'or : PointsMaterial #f9d58b additive blending (cohérence Takienta). Routes caravanières : LineDashedMaterial #f9d58b pulsant. Bloom PostProcessing sur #f9d58b uniquement.",
                "details_sonores": "Apogée musicale : kora (mélodie) + ngoni (basse) + djembé (rythme). Volume progressif vers le pic émotionnel."
            },
            {
                "num": 5,
                "titre": "Le Passage du Temps — Ce qui résiste",
                "duree": "80-100 secondes",
                "description": "L'empire s'efface progressivement — les bâtiments disparaissent, le sable reprend ses droits, le ciel s'assombrit. Mais le tombeau, LUI, reste. Immuable. Des tempêtes de sable l'assaillent visuellement, des pluies AR tombent, les conflits de 2012 apparaissent en éclairs rouges... Le tombeau résiste. Puis, les mains des restaurateurs de 2026 apparaissent, appliquant le nuevo banco. Le monument reprend sa couleur d'origine. Message animé lettre par lettre : 'Certaines choses sont trop précieuses pour disparaître.'",
                "emotion": "Tension, résilience, espoir, émotion profonde",
                "interaction": "L'utilisateur peut souffler dans le micro (Web Speech API détection son) pour disperser les particules de sable. Sinon, tap pour avancer.",
                "techno": "Displace shader pour effet tempête sable, Rain system (ligne de particules), Red lightning shader pour conflits, MorphTarget pour dégradation/restauration du modèle, TextGeometry animée lettre par lettre, Web Speech API microphone",
                "details_visuels": "Tempête : désaturation vers #2b2b3b (gris identité). Éclairs de conflit : #55415d intense pulsant. Restauration 2026 : retour progressif vers #D2691E (banco) puis #f9d58b (lumière espoir). Message texte : #fff8e7 sur fond #0d0810 — cohérence UI Takienta/Toguna.",
                "details_sonores": "Tempête + tonnerre + silence pesant → puis marteau des restaurateurs → puis retour doux de la kora"
            },
            {
                "num": 6,
                "titre": "Ton Héritage — La Connexion",
                "duree": "100-120 secondes",
                "description": "Plan final. Le tombeau brille doucement sous un ciel étoilé du Sahel. Un arc de lumière dorée part de l'écran de l'utilisateur, traverse la carte de l'Afrique de l'Ouest stylisée, et rejoint Gao. La carte s'illumine : Mali, Niger, Burkina, Sénégal, Côte d'Ivoire — toutes les terres de l'ancien empire. Texte final : 'L'Empire Songhaï a construit ce monde. Tu en portes l'héritage.' Deux boutons apparaissent : 'En savoir plus' (lien UNESCO) et 'Partager' (Web Share API).",
                "emotion": "Appartenance, fierté identitaire, désir de transmettre",
                "interaction": "Bouton 'Partager' → Web Share API (photo du monument + texte prédéfini). Bouton 'En savoir plus' → lien UNESCO. Gyroscope : incliner le téléphone pour voir les étoiles bouger.",
                "techno": "Globe Three.js simplifié avec TorusGeometry continents, TubeGeometry pour l'arc lumineux, DeviceOrientationControls pour gyroscope, Web Share API, TextGeometry finale, StarField shader nuit sahélienne",
                "details_visuels": "Ciel nocturne #050505 : 5000 étoiles PointsMaterial #fff8e7 (size 0.5). Arc patrimoine : TubeGeometry emissive #f9d58b pulsant (signature visuelle identité). Carte Afrique : outline #f9d58b doux. Boutons UI : fond #55415d + texte #f9d58b — IDENTIQUE aux boutons Takienta et Toguna.",
                "details_sonores": "Musique finale douce et épique. Voix griot : dernière phrase en songhaï sous-titrée. Fade out progressif."
            }
        ],
        "palette_couleurs": ["#f9d58b", "#55415d", "#050505", "#0d0810", "#D2691E", "#fff8e7", "#2b2b3b", "#8B6914"],
        "palette_description": "IDENTITÉ VISUELLE PARTAGÉE avec La Takienta et Le Toguna — #f9d58b (or/ambre, accent principal), #55415d (violet profond, fond/contraste), #050505 (noir scène Three.js), #0d0810 (noir-violet radial), #D2691E (terre cuite banco, accent site spécifique), #fff8e7 (crème, textes), #2b2b3b (gris sombre, éléments secondaires), #8B6914 (or sombre, profondeur)",
        "ambiance_sonore": "Voix griot songhaï + Kora malienne + Ngoni + Djembé + sons naturels Sahel (vent, sable, oiseaux nocturnes)",
        "emotion_cible": "Mystère → Émerveillement → Fierté ancestrale → Appartenance culturelle — une expérience qui grave l'Empire Songhaï dans la mémoire",
        "specifications_techniques": {
            "framework": "Three.js r170+",
            "format_modele": "GLB compressé Draco (max 5MB)",
            "rendu": "WebGL2 avec antialiasing MSAA x4",
            "postprocessing": "UnrealBloom pour les particules d'or, FXAA",
            "audio": "Web Audio API avec AudioContext, AudioWorklet pour effets",
            "mobile": "Portrait + paysage, touch events optimisés, 60fps target",
            "accessibilite": "Sous-titres pour toutes les voix, mode faible mouvement"
        }
    },
    "takienta": {
        "concept_central": "Voyage dans le temps : voir la Takienta se construire devant toi",
        "scenes": [
            {
                "num": 1,
                "titre": "L'Eveil - La terre parle",
                "duree": "0-5 secondes",
                "description": "L'ecran s'ouvre sur une terre aride. Des particules de poussiere rouge s'elevent du sol. La camera pivote lentement vers le ciel. Son : vent du Sahel, voix ancestrale en langue Ditammari.",
                "interaction": "Aucune - scene cinematique d'introduction",
                "techno": "Three.js particles, AudioContext, fog shader"
            },
            {
                "num": 2,
                "titre": "La Fondation - Les mains batissent",
                "duree": "5-15 secondes",
                "description": "Des mains en AR semi-transparentes posent les premieres briques d'argile. La base circulaire de la tour se dessine progressivement. Chaque brique deposee declenche un son de terre battue.",
                "interaction": "Tap sur l'ecran pour accelerer la construction",
                "techno": "GLTF animation, morphTargets, sound triggers"
            },
            {
                "num": 3,
                "titre": "La Montee - La tour s'eleve",
                "duree": "15-30 secondes",
                "description": "La tour complete emerge du sol en 3D. Elle grandit lentement, etage par etage. Des annotations lumineuses apparaissent sur chaque element : Grenier (stockage du mil), Autel (connexion aux ancetres), Terrasse (observation).",
                "interaction": "Pinch pour zoomer, swipe pour tourner autour",
                "techno": "OrbitControls, CSS2DRenderer, GSAP animations"
            },
            {
                "num": 4,
                "titre": "La Vie - Le village s'anime",
                "duree": "30-60 secondes",
                "description": "Autour de la tour principale, d'autres tours apparaissent. Des silhouettes stylisees des Batammariba vaquent a leurs occupations. La nuit tombe : des feux s'allument. L'utilisateur peut pointer vers chaque activite pour en savoir plus.",
                "interaction": "Cliquer sur les silhouettes = voir leur role dans la communaute",
                "techno": "InstancedMesh pour les personnages, jour/nuit shader, raycasting"
            },
            {
                "num": 5,
                "titre": "Le Patrimoine - Ton lien avec l'histoire",
                "duree": "60-90 secondes",
                "description": "La camera s'eloigne pour montrer le Koutammakou depuis le ciel (satellite view). Un arc lumineux relie l'utilisateur a ce lieu au Togo. Texte final : 'La Takienta est inscrite au Patrimoine Mondial de l'UNESCO depuis 2004.'",
                "interaction": "Bouton 'En savoir plus' qui ouvre une page web",
                "techno": "Tween.js camera animation, globe Three.js simplifie, lien externe"
            }
        ],
        "palette_couleurs": ["#C1440E", "#8B4513", "#D2691E", "#F4A460", "#2F4F2F", "#FFF8DC"],
        "ambiance_sonore": "Flute africaine, percussions douces, voix ancestrales",
        "emotion_cible": "Fierté, connexion aux racines, émerveillement architectural"
    }
}

def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

def notion_request(endpoint, method="GET", data=None):
    url = f"https://api.notion.com/v1{endpoint}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=notion_headers(), method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def generer_prompt_agent_code(nom_projet, template):
    """Genere le prompt detaille pour l'Agent Code"""

    scenes_txt = ""
    for s in template["scenes"]:
        visuels = s.get("details_visuels", "")
        sonores = s.get("details_sonores", "")
        emotion = s.get("emotion", "")
        scenes_txt += (
            f"Scene {s['num']} - {s['titre']} ({s['duree']}) : {s['description']} "
            f"Emotion: {emotion}. Interaction: {s['interaction']}. "
            f"Technologies: {s['techno']}. "
            f"Visuels: {visuels}. Sons: {sonores}. "
        )

    prompt = f"""
PROJET WEBAR : {nom_projet}
CONCEPT : {template['concept_central']}

STORYBOARD COMPLET :
{scenes_txt}

SPECIFICATIONS TECHNIQUES :
- Framework : Three.js r160+
- Format modele : GLB (charge via GLTFLoader + DRACOLoader)
- Rendu : WebGL avec antialiasing
- Responsive : mobile first (portrait et paysage)
- Performance : max 60fps sur mobile recent

PALETTE COULEURS : {', '.join(template['palette_couleurs'])}
AMBIANCE : {template['ambiance_sonore']}
EMOTION CIBLE : {template['emotion_cible']}

CONTRAINTES :
- Pas de framework externe sauf Three.js et ses modules
- Tout en un seul fichier HTML (self-contained)
- Commentaires en francais dans le code
- Le modele GLB sera charge depuis './assets/{nom_projet.lower().replace(' ', '-')}.glb'
- Interface minimaliste : bouton plein ecran, bouton info, progress bar de chargement

INSPIRATION SANS COPIE :
- Google Arts & Culture : rendre l'histoire personnelle via l'ecran
- 8th Wall : l'architecture peut etre magique et defier la gravite
- Louvre AR : l'objet reel comme declencheur de narration
"""
    return prompt.strip()

def creer_storyboard_notion(nom_projet, rapport_recherche=None):
    """Cree le storyboard complet dans Notion"""

    date = datetime.now().strftime("%Y-%m-%d")
    nom_lower = nom_projet.lower()

    # Choisir le template
    template = None
    for k, v in TEMPLATES_STORYBOARD.items():
        if k in nom_lower or any(mot in nom_lower for mot in ["askia", "gao", "tombeau", "songhai"]):
            if k == "tombeau" and any(mot in nom_lower for mot in ["tombeau", "askia", "gao", "songhai"]):
                template = v
                break
            elif k != "tombeau" and k in nom_lower:
                template = v
                break

    if not template:
        # Template generique
        template = {
            "concept_central": f"Immersion dans l'architecture de {nom_projet}",
            "scenes": [
                {"num": 1, "titre": "Introduction", "duree": "0-5s", "description": "Scene d'ouverture cinematique", "interaction": "Aucune", "techno": "Three.js, particles"},
                {"num": 2, "titre": "Decouverte", "duree": "5-30s", "description": "Le modele apparait progressivement avec animations", "interaction": "Rotation, zoom", "techno": "GLTF, OrbitControls"},
                {"num": 3, "titre": "Exploration", "duree": "30-60s", "description": "Annotations interactives sur chaque element", "interaction": "Clic sur elements", "techno": "Raycasting, CSS2DRenderer"},
                {"num": 4, "titre": "Conclusion", "duree": "60-90s", "description": "Message culturel final, lien vers ressources", "interaction": "Bouton en savoir plus", "techno": "Tween, liens externes"},
            ],
            "palette_couleurs": ["#8B4513", "#D2691E", "#F4A460", "#2F4F4F"],
            "ambiance_sonore": "Musique traditionnelle africaine, sons naturels",
            "emotion_cible": "Émerveillement, fierté culturelle, curiosité"
        }

    prompt_code = generer_prompt_agent_code(nom_projet, template)

    children = [
        {
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": f"Storyboard genere le {date} par Agent Storyboard. Ce document sert de brief pour l'Agent Code."}}],
                "icon": {"type": "emoji", "emoji": "\U0001f3ac"},
                "color": "purple_background"
            }
        },
        {
            "object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": f"Storyboard WebAR : {nom_projet}"}}]}
        },
        {
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": f"Concept Central"}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": template["concept_central"]}, "annotations": {"bold": True}}]}
        },
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Inspirations WebAR de reference"}}]}
        }
    ]

    for ref in REFERENCES_WEBAR:
        children.append({
            "object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"{ref['nom']} → Lecon : {ref['lecon']}"}}]}
        })

    children.append({"object": "block", "type": "divider", "divider": {}})
    children.append({
        "object": "block", "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Storyboard Scene par Scene"}}]}
    })

    for scene in template["scenes"]:
        children.append({
            "object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": f"Scene {scene['num']} : {scene['titre']} ({scene['duree']})"}}]}
        })
        children.append({
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": scene["description"]}}]}
        })
        children.append({
            "object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Interaction : {scene['interaction']}"}, "annotations": {"color": "blue"}}]}
        })
        children.append({
            "object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Technologies : {scene['techno']}"}, "annotations": {"italic": True, "color": "gray"}}]}
        })

    children.append({"object": "block", "type": "divider", "divider": {}})
    children.append({
        "object": "block", "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Design"}}]}
    })
    children.append({
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Palette couleurs : {', '.join(template['palette_couleurs'])}"}}]}
    })
    children.append({
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Ambiance sonore : {template['ambiance_sonore']}"}}]}
    })
    children.append({
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Emotion cible : {template['emotion_cible']}"}}]}
    })

    children.append({"object": "block", "type": "divider", "divider": {}})
    children.append({
        "object": "block", "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Prompt pour Agent Code"}}]}
    })

    # Decouper le prompt en morceaux de 1900 chars
    prompt_restant = prompt_code
    while len(prompt_restant) > 0:
        morceau = prompt_restant[:1900]
        prompt_restant = prompt_restant[1900:]
        children.append({
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": morceau}, "annotations": {"code": False, "color": "gray"}}]}
        })

    page_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": f"Storyboard WebAR : {nom_projet} (Agent Auto)"}}]},
            "Cat\u00e9gorie": {"select": {"name": "Planification"}},
            "Date": {"date": {"start": date}}
        },
        "children": children[:100]
    }

    result = notion_request("/pages", method="POST", data=page_data)
    return result.get("url", ""), prompt_code, template

def run(nom_projet, rapport_recherche=None):
    """Point d'entree principal de l'agent"""
    print(f"\n{'='*50}")
    print(f"AGENT STORYBOARD - Projet : {nom_projet}")
    print(f"{'='*50}")

    url, prompt_code, template = creer_storyboard_notion(nom_projet, rapport_recherche)

    print(f"\n[Agent Storyboard] TERMINE")
    print(f"Storyboard cree dans Notion : {url}")
    print(f"\n[Agent Storyboard] Prompt pret pour Agent Code ({len(prompt_code)} caracteres)")

    return {
        "status": "ok",
        "url_notion": url,
        "prompt_code": prompt_code,
        "template": template
    }

if __name__ == "__main__":
    run("La Takienta")
