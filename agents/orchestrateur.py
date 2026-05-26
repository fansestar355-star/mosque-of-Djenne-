"""
ORCHESTRATEUR - Chef des agents
Tu tapes le nom d'un projet, il gere tout automatiquement :
  1. Agent Recherche -> rapport Notion
  2. Agent Image/3D -> generation Meshy.ai + page Notion
  3. Agent Storyboard -> plan WebAR + prompt pour Agent Code
  4. Agent Code -> genere le HTML de l'experience
  5. Agent GitHub -> met en ligne sur GitHub Pages

USAGE :
  python orchestrateur.py "La Takienta"
  python orchestrateur.py "Toguna"
  python orchestrateur.py "Dome Musgum"
"""

import sys
import os
import threading
import time
from datetime import datetime

# Fix encodage terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ajouter le dossier agents au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import agent_recherche
import agent_image_3d
import agent_storyboard
import agent_code
import agent_github

def separateur():
    print("\n" + "="*60)

def notifier(message, emoji=""):
    print(f"\n{'*'*60}")
    print(f"  {emoji} NOTIFICATION : {message}")
    print(f"{'*'*60}\n")

def attendre_validation(message):
    """Attend que l'utilisateur appuie sur Entree pour continuer"""
    print(f"\n{'>'*60}")
    print(f"  ACTION REQUISE : {message}")
    print(f"  Appuie sur ENTREE quand tu es pret...")
    print(f"{'>'*60}")
    input()

def run_agent_en_parallele(agents_et_args):
    """Lance plusieurs agents en parallele et attend qu'ils finissent"""
    resultats = {}
    threads = []
    erreurs = []

    def runner(nom, fn, args, kwargs):
        try:
            resultats[nom] = fn(*args, **kwargs)
        except Exception as e:
            erreurs.append(f"{nom}: {e}")
            resultats[nom] = {"status": "error", "message": str(e)}

    for nom, fn, args, kwargs in agents_et_args:
        t = threading.Thread(target=runner, args=(nom, fn, args, kwargs))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if erreurs:
        print(f"\n  [Avertissement] Erreurs non bloquantes : {erreurs}")

    return resultats

def pipeline(nom_projet):
    """Pipeline complet pour un projet"""

    debut = datetime.now()
    separateur()
    print(f"  ORCHESTRATEUR - Lancement du pipeline")
    print(f"  Projet : {nom_projet.upper()}")
    print(f"  Heure  : {debut.strftime('%H:%M:%S')}")
    separateur()

    # ====================================================
    # PHASE 1 : Recherche + Images en PARALLELE
    # ====================================================
    print("\n[Phase 1/4] Lancement Recherche + Images en parallele...")
    print("  Tu peux aller faire autre chose, je te notifie quand c'est pret.")

    resultats_phase1 = run_agent_en_parallele([
        ("recherche", agent_recherche.run, [nom_projet], {}),
        ("image_3d", agent_image_3d.run, [nom_projet], {}),
    ])

    res_recherche = resultats_phase1.get("recherche", {})
    res_image = resultats_phase1.get("image_3d", {})

    notifier(f"Phase 1 terminee pour '{nom_projet}' !", "✓")
    print(f"  Rapport Notion : {res_recherche.get('url', 'N/A')}")
    print(f"  Images/3D Notion : {res_image.get('url_notion', 'N/A')}")

    # Notifier sur Meshy.ai
    if res_image.get("task_id"):
        task_id = res_image["task_id"]
        notifier(f"Generation 3D lancee sur Meshy.ai ! Task: {task_id}", "🎨")
        print(f"  Va sur https://www.meshy.ai pour voir ton modele.")
        print(f"  Quand le modele est pret :")
        print(f"  1. Telecharge le fichier GLB")
        print(f"  2. Ouvre Blender pour optimiser (facultatif)")
        print(f"  3. Depose le GLB dans le bon dossier")
        print(f"  4. Reviens ici et appuie sur ENTREE")
        attendre_validation("Depose le fichier GLB et appuie sur ENTREE pour continuer")

    # ====================================================
    # PHASE 2 : Storyboard
    # ====================================================
    print("\n[Phase 2/4] Creation du storyboard WebAR...")

    rapport_recherche = res_recherche.get("rapport", None)
    res_storyboard = agent_storyboard.run(nom_projet, rapport_recherche)

    notifier(f"Storyboard cree pour '{nom_projet}' !", "📋")
    print(f"  Storyboard Notion : {res_storyboard.get('url_notion', 'N/A')}")
    print(f"\n  Consulte le storyboard dans Notion.")
    print(f"  Si tu veux modifier quelque chose, fais-le maintenant.")
    attendre_validation("Valide le storyboard et appuie sur ENTREE pour generer le code")

    # ====================================================
    # PHASE 3 : Generation du code
    # ====================================================
    print("\n[Phase 3/4] Generation de l'experience WebAR...")

    # Chercher si un GLB a ete depose
    nom_fichier = nom_projet.lower().replace(" ", "-")
    dossier_projet = f"C:/Users/Kabakoo Apprenant.e/Desktop/MES PROJETS/projets-generes/{nom_fichier}"
    glb_path = None

    # Chercher un GLB dans le dossier projet ou le dossier principal
    for dossier_cherche in [
        f"C:/Users/Kabakoo Apprenant.e/Desktop/MES PROJETS/projets-generes/{nom_fichier}/assets",
        "C:/Users/Kabakoo Apprenant.e/Desktop/MES PROJETS",
        "C:/Users/Kabakoo Apprenant.e/Desktop"
    ]:
        if os.path.exists(dossier_cherche):
            for f in os.listdir(dossier_cherche):
                if f.lower().endswith(".glb") and nom_fichier.replace("-", "") in f.lower().replace("-", "").replace(" ", ""):
                    glb_path = f"./assets/{f}"
                    print(f"  [OK] Modele GLB trouve : {f}")
                    break

    res_code = agent_code.run(
        nom_projet,
        prompt_storyboard=res_storyboard.get("prompt_code"),
        glb_path=glb_path
    )

    notifier(f"Code WebAR genere pour '{nom_projet}' !", "💻")
    print(f"  Fichier : {res_code.get('chemin_html', 'N/A')}")

    # ====================================================
    # PHASE 4 : Mise en ligne GitHub
    # ====================================================
    print("\n[Phase 4/4] Mise en ligne sur GitHub Pages...")
    attendre_validation("Pret pour la mise en ligne ? Appuie sur ENTREE")

    res_github = agent_github.run(nom_projet, dossier_source=res_code.get("dossier"))

    # ====================================================
    # BILAN FINAL
    # ====================================================
    duree = (datetime.now() - debut).seconds
    separateur()
    notifier(f"Pipeline complet termine pour '{nom_projet}' !", "🚀")
    print(f"  Duree totale : {duree} secondes")
    print(f"\n  RESULTATS :")
    print(f"  • Recherche Notion  : {res_recherche.get('url', 'N/A')}")
    print(f"  • Images/3D Notion  : {res_image.get('url_notion', 'N/A')}")
    print(f"  • Storyboard Notion : {res_storyboard.get('url_notion', 'N/A')}")
    print(f"  • Fichier HTML      : {res_code.get('chemin_html', 'N/A')}")
    print(f"  • URL publique      : {res_github.get('url', 'N/A')}")
    separateur()

    return {
        "recherche": res_recherche,
        "image_3d": res_image,
        "storyboard": res_storyboard,
        "code": res_code,
        "github": res_github
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nom = " ".join(sys.argv[1:])
    else:
        print("Projets disponibles : La Takienta, Toguna, Dome Musgum")
        print("Ou tape le nom d'un nouveau projet")
        nom = input("\nNom du projet : ").strip()
        if not nom:
            nom = "La Takienta"

    pipeline(nom)
