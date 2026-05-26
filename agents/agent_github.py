"""
Agent 5 : Hebergement sur GitHub Pages
- Prend le dossier genere par Agent Code
- Pousse sur le bon repo GitHub
- Retourne l'URL publique
"""

import urllib.request
import json
import base64
import os
from datetime import datetime

GITHUB_TOKEN = "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"
GITHUB_USER  = "fansestar355-star"

# Mapping projet -> repo GitHub
REPOS = {
    "takienta": "La-Takienta",
    "toguna": "Toguna-Experience",
    "musgum": "Dome-Musgum",
}

def github_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "LaTakienta-Agent"
    }

def github_request(endpoint, method="GET", data=None):
    url = f"https://api.github.com{endpoint}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=github_headers(), method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"  [GitHub Error {e.code}] {error_body[:200]}")
        return None

def get_file_sha(repo, chemin):
    """Recupere le SHA d'un fichier existant (requis pour mise a jour)"""
    result = github_request(f"/repos/{GITHUB_USER}/{repo}/contents/{chemin}")
    if result and "sha" in result:
        return result["sha"]
    return None

def pousser_fichier(repo, chemin_local, chemin_github, message_commit):
    """Pousse un fichier sur GitHub"""
    if not os.path.exists(chemin_local):
        print(f"  [Erreur] Fichier non trouve : {chemin_local}")
        return False

    with open(chemin_local, "rb") as f:
        contenu = f.read()

    contenu_b64 = base64.b64encode(contenu).decode("utf-8")
    sha = get_file_sha(repo, chemin_github)

    data = {
        "message": message_commit,
        "content": contenu_b64,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha

    result = github_request(
        f"/repos/{GITHUB_USER}/{repo}/contents/{chemin_github}",
        method="PUT",
        data=data
    )

    if result and "content" in result:
        print(f"  [OK] {chemin_github} pousse sur GitHub")
        return True
    else:
        print(f"  [Erreur] Impossible de pousser {chemin_github}")
        return False

def activer_github_pages(repo):
    """Active GitHub Pages sur la branche main"""
    data = {
        "source": {"branch": "main", "path": "/"}
    }
    # Essayer d'abord POST (creation)
    result = github_request(f"/repos/{GITHUB_USER}/{repo}/pages", method="POST", data=data)
    if not result:
        # Si deja active, PUT (mise a jour)
        github_request(f"/repos/{GITHUB_USER}/{repo}/pages", method="PUT", data=data)

def run(nom_projet, dossier_source=None):
    """Point d'entree principal de l'agent"""
    print(f"\n{'='*50}")
    print(f"AGENT GITHUB - Projet : {nom_projet}")
    print(f"{'='*50}")

    nom_lower = nom_projet.lower()
    repo = None
    for k, v in REPOS.items():
        if k in nom_lower:
            repo = v
            break

    if not repo:
        repo = nom_projet.replace(" ", "-").title()
        print(f"  Repo : {repo} (nouveau)")

    # Dossier source par defaut
    if not dossier_source:
        nom_fichier = nom_projet.lower().replace(" ", "-")
        dossier_source = f"C:/Users/Kabakoo Apprenant.e/Desktop/MES PROJETS/projets-generes/{nom_fichier}"

    index_path = os.path.join(dossier_source, "index.html")

    if not os.path.exists(index_path):
        print(f"  [Erreur] index.html non trouve dans {dossier_source}")
        print(f"  Lance d'abord l'Agent Code.")
        return {"status": "error", "message": "index.html manquant"}

    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"Experience WebAR {nom_projet} - Agent Auto - {date}"

    # Pousser index.html
    succes = pousser_fichier(repo, index_path, "index.html", message)

    # Pousser les assets GLB si presents
    assets_dir = os.path.join(dossier_source, "assets")
    if os.path.exists(assets_dir):
        for fichier in os.listdir(assets_dir):
            if fichier.endswith(".glb") or fichier.endswith(".gltf"):
                pousser_fichier(
                    repo,
                    os.path.join(assets_dir, fichier),
                    f"assets/{fichier}",
                    f"Ajout modele 3D : {fichier}"
                )

    # Activer GitHub Pages
    activer_github_pages(repo)

    url_pages = f"https://{GITHUB_USER}.github.io/{repo}/"

    print(f"\n[Agent GitHub] TERMINE")
    if succes:
        print(f"URL publique : {url_pages}")
        print(f"[NOTIFICATION] Ton experience est en ligne !")
        print(f"  Attends 1-2 minutes que GitHub Pages se deploie.")
    else:
        print(f"  Verifier les permissions du token GitHub.")

    return {
        "status": "ok" if succes else "error",
        "url": url_pages,
        "repo": repo
    }

if __name__ == "__main__":
    run("La Takienta")
