"""
Agent 2 : Recherche d'images et generation 3D via Meshy.ai
- Trouve les images de reference (4 vues du modele)
- Envoie a Meshy.ai pour generation du modele 3D
- Notifie quand le modele est pret
"""

import urllib.request
import urllib.parse
import json
import time
from datetime import datetime

MESHY_API_KEY = "msy_IBtfNbiumEPkQtOtnXNfc1SHalcUtPBRAbYC"
NOTION_TOKEN  = "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"
DATABASE_ID   = "65073e08-97ca-4c60-9cf2-da1078736240"

# Images de reference par projet (URLs Wikipedia Commons - libres de droits)
IMAGES_REFERENCE = {
    "takienta": {
        "description": "Tour Takienta du peuple Batammariba au Togo",
        "vues": [
            {
                "vue": "Face principale",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Koutammakou_Togo.jpg/800px-Koutammakou_Togo.jpg",
                "description": "Vue frontale d'une tour Takienta typique avec son toit conique en chaume"
            },
            {
                "vue": "Vue d'ensemble du village",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Tamberma_house.jpg/800px-Tamberma_house.jpg",
                "description": "Ensemble de tours Takienta dans leur environnement naturel"
            },
            {
                "vue": "Detail architectural",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Koutammakou.jpg/800px-Koutammakou.jpg",
                "description": "Detail de la base cylindrique et des ouvertures"
            }
        ],
        "prompt_meshy": "Traditional Batammariba Takienta tower from Togo, West Africa. Cylindrical mud brick tower with conical thatched roof, small rectangular doorway at base, defensive architecture, 2-3 stories tall, natural earth tones (ochre, brown, beige), surrounded by dry savanna landscape. Architectural 3D model, clean topology, game-ready, 4 views: front, back, left, right side views on white background."
    },
    "toguna": {
        "description": "Toguna des Dogons du Mali",
        "vues": [
            {
                "vue": "Vue de face",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Dogon_Toguna.jpg/800px-Dogon_Toguna.jpg",
                "description": "Vue frontale d'un Toguna avec ses piliers de bois sculptes"
            }
        ],
        "prompt_meshy": "Dogon Toguna meeting house from Mali, West Africa. Low-ceiling communal structure with thick millet stalk roof, carved wooden pillars, open sides, very low roof (forces seated position). Architectural 3D model, earthy colors, traditional African architecture, 4 views on white background."
    },
    "musgum": {
        "description": "Case Musgum du Cameroun",
        "vues": [
            {
                "vue": "Vue principale",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Musgum_mud_huts.jpg/800px-Musgum_mud_huts.jpg",
                "description": "Vue d'une case Musgum avec ses nervures decoratives et sa forme conique"
            }
        ],
        "prompt_meshy": "Musgum mud hut from Cameroon, Central Africa. Organic egg-shaped dome structure made of mud, decorative vertical ribbing on exterior for drainage, single small doorway, natural clay colors. Architectural 3D model, smooth organic form, bioclimatic architecture, 4 views on white background."
    }
}

def meshy_headers():
    return {
        "Authorization": f"Bearer {MESHY_API_KEY}",
        "Content-Type": "application/json"
    }

def meshy_request(endpoint, method="GET", data=None):
    url = f"https://api.meshy.ai/v2{endpoint}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=meshy_headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"  [Erreur Meshy] {e.code} : {error_body}")
        return None

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

def lancer_generation_meshy(nom_projet):
    """Lance la generation du modele 3D sur Meshy.ai via Image-to-3D avec textures"""

    nom_lower = nom_projet.lower()
    config = None
    for k, v in IMAGES_REFERENCE.items():
        if k in nom_lower:
            config = v
            break

    if not config:
        config = {
            "description": nom_projet,
            "prompt_meshy": f"Traditional African architecture: {nom_projet}. Detailed 3D architectural model, earthy natural materials.",
            "vues": []
        }

    # Choisir l'image de reference (premiere vue disponible)
    vues = config.get("vues", [])
    image_url = vues[0]["url"] if vues else None

    if not image_url:
        print(f"  [Avertissement] Aucune image de reference trouvee pour '{nom_projet}', utilisation text-to-3D")
        data = {
            "mode": "preview",
            "prompt": config["prompt_meshy"],
            "art_style": "realistic",
            "negative_prompt": "low quality, blurry, cartoon, anime, people, humans, animals"
        }
        result = meshy_request("/text-to-3d", method="POST", data=data)
        endpoint_statut = "/text-to-3d"
    else:
        print(f"[Agent Image/3D] Lancement Image-to-3D Meshy.ai pour : {nom_projet}")
        print(f"  Image source : {image_url[:80]}...")
        # Appel API Meshy.ai - Image to 3D avec textures PBR activees
        data = {
            "image_url": image_url,
            "enable_pbr": True,
            "should_remesh": True
        }
        result = meshy_request("/image-to-3d", method="POST", data=data)
        endpoint_statut = "/image-to-3d"

    config["_endpoint_statut"] = endpoint_statut

    if result and "result" in result:
        task_id = result["result"]
        print(f"  [OK] Task ID Meshy : {task_id}")
        return task_id, config
    else:
        print(f"  [Erreur] Impossible de lancer la generation")
        return None, config

def verifier_statut_meshy(task_id, config=None):
    """Verifie le statut d'une generation Meshy.ai"""
    endpoint = "/image-to-3d"
    if config and config.get("_endpoint_statut"):
        endpoint = config["_endpoint_statut"]
    result = meshy_request(f"{endpoint}/{task_id}")
    if result:
        status = result.get("status", "unknown")
        progress = result.get("progress", 0)
        return status, progress, result
    return "error", 0, None

def creer_page_notion_images(nom_projet, config, task_id, statut_initial):
    """Cree la page de suivi dans Notion"""

    date = datetime.now().strftime("%Y-%m-%d")
    vues = config.get("vues", [])

    children = [
        {
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": f"Generation 3D lancee le {date} via Meshy.ai. Task ID: {task_id}. Statut: {statut_initial}"}}],
                "icon": {"type": "emoji", "emoji": "\U0001f3a8"},
                "color": "yellow_background"
            }
        },
        {
            "object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": f"Images de reference : {nom_projet}"}}]}
        }
    ]

    # Ajouter les vues de reference
    if vues:
        children.append({
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Vues de reference utilisees"}}]}
        })
        for vue in vues:
            children.append({
                "object": "block", "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"{vue['vue']} : {vue['description']}"}}]}
            })
            # Ajouter le lien image
            children.append({
                "object": "block", "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"URL : {vue['url']}", "link": {"url": vue['url']}}}]}
            })

    children.append({"object": "block", "type": "divider", "divider": {}})

    # Section generation Meshy
    children.append({
        "object": "block", "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Generation Meshy.ai"}}]}
    })
    children.append({
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Task ID : {task_id}"}}]}
    })
    children.append({
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Statut : {statut_initial}"}}]}
    })
    vues = config.get("vues", [])
    mode_label = f"Image-to-3D (PBR textures activees) - source : {vues[0]['url'][:80]}..." if vues else f"Text-to-3D - prompt : {config['prompt_meshy'][:300]}"
    children.append({
        "object": "block", "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Mode : {mode_label}"}, "annotations": {"italic": True, "color": "gray"}}]}
    })
    children.append({"object": "block", "type": "divider", "divider": {}})

    # Instructions pour la suite
    children.append({
        "object": "block", "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Etapes suivantes (a faire manuellement)"}}]}
    })
    etapes = [
        "Aller sur meshy.ai pour voir le modele genere",
        "Evaluer la qualite du modele (forme, proportions, details)",
        "Si OK : telecharger en format GLB",
        "Ouvrir dans Blender pour optimisation (reduire polygones, bake textures)",
        "Exporter en GLB optimise (< 5MB de preference)",
        "Deposer le fichier GLB dans le dossier du projet",
        "Revenir ici et lancer l'Agent Hebergement GitHub"
    ]
    for e in etapes:
        children.append({
            "object": "block", "type": "to_do",
            "to_do": {"rich_text": [{"type": "text", "text": {"content": e}}], "checked": False}
        })

    page_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": f"Images 3D : {nom_projet} (Agent Auto)"}}]},
            "Cat\u00e9gorie": {"select": {"name": "Avancée"}},
            "Date": {"date": {"start": date}}
        },
        "children": children
    }

    result = notion_request("/pages", method="POST", data=page_data)
    return result.get("url", "")

def run(nom_projet):
    """Point d'entree principal de l'agent"""
    print(f"\n{'='*50}")
    print(f"AGENT IMAGE/3D - Projet : {nom_projet}")
    print(f"{'='*50}")

    # Lancer la generation
    task_id, config = lancer_generation_meshy(nom_projet)

    statut_initial = "en_attente"
    if task_id:
        # Verifier statut initial
        statut, progress, _ = verifier_statut_meshy(task_id, config)
        statut_initial = f"{statut} ({progress}%)"
        print(f"  Statut initial : {statut_initial}")

    # Creer la page Notion
    url_notion = creer_page_notion_images(nom_projet, config, task_id or "erreur_lancement", statut_initial)

    print(f"\n[Agent Image/3D] TERMINE")
    print(f"Page Notion creee : {url_notion}")

    if task_id:
        print(f"\n[NOTIFICATION] La generation Meshy.ai est lancee !")
        print(f"  Task ID : {task_id}")
        print(f"  Va sur https://www.meshy.ai pour voir ton modele.")
        print(f"  Quand c'est pret, telecharge le GLB et depose-le dans le dossier du projet.")

    return {
        "status": "ok",
        "task_id": task_id,
        "url_notion": url_notion,
        "config": config
    }

if __name__ == "__main__":
    run("La Takienta")
