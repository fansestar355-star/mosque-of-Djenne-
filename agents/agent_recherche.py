"""
Agent 1 : Recherche sur le patrimoine architectural africain
- Recherche web sur le projet
- Ecrit un rapport detaille dans Notion
"""

import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

NOTION_TOKEN = "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"
DATABASE_ID  = "65073e08-97ca-4c60-9cf2-da1078736240"

# Base de connaissances sur les projets deja realises (pour ne pas repeter)
PROJETS_EXISTANTS = {
    "toguna": {
        "approche": "Experience AR avec suivi facial MediaPipe, acces a un espace communautaire virtuel",
        "technos": "ZapWorks, MindAR, MediaPipe face tracking",
        "points_forts": "Interaction corporelle, immersion sonore, detection visage"
    },
    "musgum": {
        "approche": "Experience immersive du dome bioclimatique, navigation 3D autour de la structure",
        "technos": "Three.js, GLTFLoader, OrbitControls",
        "points_forts": "Architecture organique, textures terre, lumiere naturelle"
    },
    "takienta": {
        "approche": "Globe -> zoom Togo -> paysage avec modele Takienta annote",
        "technos": "Three.js, Sky, CSS2DRenderer, annotations flottantes",
        "points_forts": "Storytelling geographique, annotations educatives, transition globe/local"
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

def recherche_wikipedia(terme):
    """Recherche sur Wikipedia via l'API publique"""
    terme_encode = urllib.parse.quote(terme)
    url = f"https://fr.wikipedia.org/api/rest_v1/page/summary/{terme_encode}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LaTakienta/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("extract", "")
    except:
        # Essayer en anglais
        try:
            url_en = f"https://en.wikipedia.org/api/rest_v1/page/summary/{terme_encode}"
            req = urllib.request.Request(url_en, headers={"User-Agent": "LaTakienta/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("extract", "")
        except:
            return ""

def generer_rapport_recherche(nom_projet):
    """
    Genere un rapport de recherche complet sur le projet
    Retourne un dict avec toutes les informations trouvees
    """
    print(f"[Agent Recherche] Recherche sur : {nom_projet}")

    rapport = {
        "nom": nom_projet,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sections": {}
    }

    # Adapter les termes de recherche selon le projet
    termes = {
        "takienta": ["Takienta Togo", "Tour Takienta Koutammakou", "Batammariba architecture"],
        "toguna": ["Toguna Mali Dogon", "Toguna case palabre", "architecture Dogon"],
        "musgum": ["Case Musgum Cameroun", "architecture Mousgoum", "dome bioclimatique africain"],
    }

    nom_lower = nom_projet.lower()
    mots_cles = []
    for k, v in termes.items():
        if k in nom_lower:
            mots_cles = v
            break
    if not mots_cles:
        mots_cles = [nom_projet, f"architecture africaine {nom_projet}", f"{nom_projet} patrimoine"]

    # Recherches Wikipedia
    resultats = []
    for terme in mots_cles[:3]:
        texte = recherche_wikipedia(terme)
        if texte and len(texte) > 100:
            resultats.append({"terme": terme, "contenu": texte})
            print(f"  [OK] {terme} : {len(texte)} caracteres")

    rapport["sections"]["recherche"] = resultats

    # Identifier ce qui a deja ete fait pour proposer du neuf
    projet_existant = None
    for k in PROJETS_EXISTANTS:
        if k in nom_lower:
            projet_existant = PROJETS_EXISTANTS[k]
            break

    rapport["sections"]["existant"] = projet_existant
    return rapport

def creer_page_notion(rapport):
    """Cree la page de recherche dans Notion"""

    nom = rapport["nom"]
    date = rapport["date"]
    resultats = rapport["sections"]["recherche"]
    existant = rapport["sections"]["existant"]

    # Construire les blocs de contenu
    children = []

    # Callout intro
    children.append({
        "object": "block", "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": f"Rapport genere automatiquement par Agent Recherche le {date}. Base sur Wikipedia et sources documentaires."}}],
            "icon": {"type": "emoji", "emoji": "\U0001f50d"},
            "color": "blue_background"
        }
    })

    # Section : Ce qui a deja ete fait
    if existant:
        children.append({
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Ce qui existe deja - A DEPASSER"}}]}
        })
        children.append({
            "object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Approche precedente : {existant['approche']}"}}]}
        })
        children.append({
            "object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Technologies utilisees : {existant['technos']}"}}]}
        })
        children.append({
            "object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Points forts actuels : {existant['points_forts']}"}}]}
        })
        children.append({"object": "block", "type": "divider", "divider": {}})

    # Section : Recherche documentaire
    children.append({
        "object": "block", "type": "heading_1",
        "heading_1": {"rich_text": [{"type": "text", "text": {"content": f"Recherche documentaire : {nom}"}}]}
    })

    for r in resultats:
        children.append({
            "object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": r["terme"]}}]}
        })
        # Decouper le texte en paragraphes de max 2000 chars
        texte = r["contenu"]
        while len(texte) > 0:
            morceau = texte[:1900]
            texte = texte[1900:]
            children.append({
                "object": "block", "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": morceau}}]}
            })

    children.append({"object": "block", "type": "divider", "divider": {}})

    # Section : Pistes pour aller plus loin
    children.append({
        "object": "block", "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Pistes pour une experience WebAR superieure"}}]}
    })

    pistes = generer_pistes_innovation(nom, existant)
    for p in pistes:
        children.append({
            "object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": p}}]}
        })

    # Creer la page
    page_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": f"Recherche : {nom} (Agent Auto)"}}]},
            "Cat\u00e9gorie": {"select": {"name": "Recherche"}},
            "Date": {"date": {"start": date}}
        },
        "children": children[:100]  # Notion limite a 100 blocs par requete
    }

    result = notion_request("/pages", method="POST", data=page_data)
    return result.get("url", "")

def generer_pistes_innovation(nom, existant):
    """Genere des pistes pour creer quelque chose de mieux que l'existant"""

    pistes_base = [
        "Integrer une narration audio reactive (voix qui explique quand on s'approche d'un element)",
        "Utiliser la geolocalisation pour contextualiser l'experience selon ou est l'utilisateur",
        "Ajouter des animations de construction du batiment (voir comment il a ete bati)",
        "Integrer des temoignages video de communautes locales en overlay AR",
        "Creer une experience multi-utilisateurs synchronisee (plusieurs personnes visitent en meme temps)",
        "Ajouter un mode nuit/jour avec changement d'ambiance lumineuse en temps reel",
        "Integrer des elements interactifs : cliquer sur une partie = histoire de cette partie",
        "Utiliser le gyroscope pour naviguer autour du modele en bougeant le telephone",
    ]

    nom_lower = nom.lower()
    if "takienta" in nom_lower:
        pistes_base.insert(0, "Creer un portail AR : pointer vers le sol = la Takienta emerge du sol devant toi")
        pistes_base.insert(1, "Ajouter les 4 tours avec animations de fumee (rituel de communication)")
        pistes_base.insert(2, "Mode exploration : entrer virtuellement a l'interieur de la tour")

    return pistes_base[:6]

def run(nom_projet):
    """Point d'entree principal de l'agent"""
    print(f"\n{'='*50}")
    print(f"AGENT RECHERCHE - Projet : {nom_projet}")
    print(f"{'='*50}")

    rapport = generer_rapport_recherche(nom_projet)
    url = creer_page_notion(rapport)

    print(f"\n[Agent Recherche] TERMINE")
    print(f"Rapport cree dans Notion : {url}")
    return {"status": "ok", "url": url, "rapport": rapport}

if __name__ == "__main__":
    run("La Takienta")
