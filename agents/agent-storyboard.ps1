# ============================================================
# Agent Storyboard v2 - Vision narrative inedite
# Mentalite : directeur artistique de musee numerique mondial
# Inspiration : Saydnaya (Amnesty), Teamlab, Google Arts & Culture
# Principe : le medium EST le message. La forme raconte le fond.
# ============================================================
param([string]$NomProjet = "La Takienta")

$NOTION_TOKEN = "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"
$DATABASE_ID  = "65073e08-97ca-4c60-9cf2-da1078736240"
$NOTION_API   = "https://api.notion.com/v1"
$headers = @{
    "Authorization"  = "Bearer $NOTION_TOKEN"
    "Notion-Version" = "2022-06-28"
    "Content-Type"   = "application/json; charset=utf-8"
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AGENT STORYBOARD v2 - $NomProjet" -ForegroundColor Cyan
Write-Host "  Vision : inedite, emotionnelle, architecturale" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$nomLower = $NomProjet.ToLower()
$date = Get-Date -Format "yyyy-MM-dd"

# ============================================================
# STORYBOARDS PAR PROJET - Chaque experience a une PHILOSOPHIE
# ============================================================
if ($nomLower -like "*takienta*") {

    $philosophie = "L'experience ne MONTRE PAS une Takienta. Elle fait VIVRE ce que c'est d'etre Batammariba. L'utilisateur traverse les epreuves de l'histoire pour comprendre pourquoi ces murs existent."

    $conceptVisuel = "Inspiration technique : Saydnaya (navigation spatiale comme narration), Teamlab (la lumiere comme matiere vivante), Google Tilt Brush (la 3D qui se dessine devant toi). Palette : noirs profonds + ocres chauds + or des rituels. Pas de boutons criards. Pas de menus. Juste l'espace et le son."

    $sequenceNarrative = @"
TITRE : 'Ils ont bati pour ne pas disparaitre'

ACTE 1 - L'OBSCURITE (0-8 secondes)
Ecran completement noir. Silence total.
Puis : un son de vent chaud. Tres loin, des voix de femmes qui chantent (enregistrement reel Batammariba).
Lentement : des particules de poussiere rouge apparaissent dans le noir.
Pas de loading bar. Pas de titre. Juste la poussiere et les voix.
L'utilisateur ne sait pas encore ou il est. C'est voulu.
Technique : noir total -> particles lentes -> fog rouge profond

ACTE 2 - LA TERRE SE SOUVIENT (8-20 secondes)
Du sol emerge une lumiere orange tres douce, comme un feu de bois.
On commence a voir : on est dans une plaine aride. Des ombres de tours au loin.
Une voix (texte flottant, pas audio) apparait dans l'espace 3D :
'Ils appelaient cet endroit Koutammakou. La terre qui se souvient.'
Puis : 'Pendant 400 ans, ils ont construit. Chaque saison. Apres chaque pluie. Apres chaque raid.'
Les mots apparaissent et disparaissent dans l'espace, animes comme des braises.
Technique : CSS2DObject animes, fog dynamique, point light orange au sol

ACTE 3 - NAISSANCE (20-45 secondes)
La tour principale emerge du sol, mais PAS comme un objet 3D qui apparait.
Elle emerge comme si de l'argile montait et prenait forme : shader de 'construction progressive'.
D'abord la base (terre sombre), puis les murs (banco clair), puis le toit (chaume dore).
Pendant la construction, des textes apparaissent sur les parties :
Sur le sol : 'Ici dorment les animaux. Ici, les morts sont proches de la terre.'
Sur les murs : 'La porte est basse. Pour entrer, tu dois t'agenouiller. Meme un ennemi arme.'
Sur le toit : 'Ici dorment les graines. Et les ancetres veillent.'
L'utilisateur peut tourner autour avec OrbitControls mais ne peut pas 'cliquer sur des boutons'.
Technique : dissolve shader (clipPlane progressif), CSS2DObject temporises

ACTE 4 - LA NUIT DU VILLAGE (45-90 secondes)
La lumiere change : coucher de soleil accelere. Le ciel passe de orange a bleu nuit.
3 tours secondaires apparaissent autour. Des feux s'allument a leurs pieds.
Des silhouettes humaines stylisees (geometrie simple, pas de visages) vaquent a leurs occupations.
Une femme repare un mur avec ses mains. Un enfant monte a l'echelle. Un vieil homme assis regarde.
Si l'utilisateur clique sur une silhouette :
  - La scene se fige. Tout devient noir et blanc sauf la silhouette.
  - Un texte apparait : son role, son nom, sa relation a la tour.
  - Puis la scene reprend, en couleur.
Technique : raycasting sur InstancedMesh, GSAP pour transitions, desaturation post-processing

ACTE 5 - L'ECHO (90 secondes - fin ouverte)
La camera monte lentement, comme un drone, en vue aerienne.
On voit le village entier. 50, 100, 200 tours. Les feux comme des lucioles.
Texte final qui flotte :
'50 000 personnes vivent encore ici. Dans ces tours de terre.'
'Ils n'ont pas preserve un monument. Ils vivent.'
Un bouton discret apparait : 'Explorer le site UNESCO'
La musique monte. Puis silence. L'ecran reste sur la vue aerienne, en boucle infinie douce.
Technique : camera tween vers le haut, InstancedMesh village, ambient occlusion
"@

    $directivesCode = @"
DIRECTIVES TECHNIQUES POUR L'AGENT CODE :

ATMOSPHERE :
- Fond de scene : JAMAIS un ciel bleu. Nuit africaine : #0a0500 avec etoiles parsemees.
- Brume chaude (fog exponentiel) : couleur #3d1500, densite 0.004
- Post-processing : FilmGrain subtil + legerement desature (pas de couleurs saturees criardes)
- Pas d'ombre portee nette. Lumiere diffuse douce comme un feu, pas un soleil de studio.

INTERACTION :
- AUCUN bouton visible au demarrage. L'interface apparait seulement quand necessaire.
- OrbitControls mais target fixe sur la tour. L'utilisateur tourne AUTOUR, ne se balade pas.
- Sur mobile : gyroscope pour regarder autour (DeviceOrientation).
- Curseur personnalise : une petite braise qui laisse une trace ephemere.

TYPOGRAPHIE ET TEXTES :
- Police : Georgia ou serif, jamais sans-serif. C'est une experience culturelle, pas une app tech.
- Textes 3D : CSS2DObject, couleur #FFE4B5 (moccasin), taille 0.85em, pas de fond
- Apparition : fade-in sur 1.5 secondes, texte qui 'brule' (letter-spacing qui se reduit)
- Les textes ne sont JAMAIS dans un panel. Ils flottent dans l'espace 3D.

AUDIO (optionnel si ressources disponibles) :
- Vent du Sahel en boucle, tres doux, vol.15
- Voix de femmes au loin, vol.08
- Craquement de bois quand on tourne la camera

MODELE 3D :
- Si GLB disponible : charger avec DRACOLoader, ombres reelles
- Si pas de GLB : placeholder architecturalement juste (cylindre + cone MAIS avec textures procedurales banco)
- La tour principale : echelle IMPOSANTE. Quand on arrive, elle doit impressionner.

LOADING :
- Pas d'ecran de chargement generique.
- Fond noir total avec juste : une particule de poussiere rouge qui tombe.
- Quand charge : cette particule grossit et explose en centaines d'autres -> transition vers la scene.
"@

} elseif ($nomLower -like "*toguna*") {

    $philosophie = "L'experience FORCE l'utilisateur dans la contrainte physique du Toguna. L'ecran RETRECIT. La camera SE BAISSE. On est oblige de se courber. On vit ce que le batiment impose."

    $conceptVisuel = "Ecran qui se retrecit progressivement (letterbox) pour simuler la hauteur basse. Palette : ocres Mali, or des ornements, noir des ombres profondes. Sons : palabres en langue Dogon, djembe distant."

    $sequenceNarrative = @"
TITRE : 'Pour parler en egal, il faut d'abord s'abaisser'
ACTE 1 : Plaine du Mali. Chaleur visible (distorsion air chaud).
ACTE 2 : L'ecran se retrecit verticalement. Letterbox de plus en plus etroit. On est force de se baisser.
ACTE 3 : Les piliers sculptes s'illuminent un par un. Chaque sculpture raconte une decision historique.
ACTE 4 : Des voix en Dogon. Textes traduits qui flottent. Le conseil parle.
ACTE 5 : L'ecran s'ouvre a nouveau. La lumiere du soir. La sagesse acquise par la contrainte.
"@

    $directivesCode = "Effet letterbox CSS progressif. Sons Dogon. Piliers interactifs. Palette chaude."

} elseif ($nomLower -like "*musgum*") {

    $philosophie = "L'experience montre que la beaute et l'ingenierie ne font qu'un. Le dome n'est pas decoratif. Il est parfait. L'utilisateur comprend la physique par la beaute."

    $conceptVisuel = "Palette : argile beige, vert Lac Tchad, ciel africain. Visualisation des forces structurelles (lignes de compression qui s'allument). Pluie qui suit les nervures."

    $sequenceNarrative = @"
TITRE : '2000 ans avant les ingenieurs modernes, ils avaient resolu le probleme'
ACTE 1 : Plaine du Cameroun. Ciel lourd avant l'orage.
ACTE 2 : La pluie commence. On voit l'eau SUIVRE les nervures du dome. Parfaitement.
ACTE 3 : Visualisation des forces : des lignes lumineuses montrent la distribution des charges.
ACTE 4 : Entrer a l'interieur. Fraicheur. Lumiere tamisee. Silence de la tempete dehors.
ACTE 5 : La comparaison : un batiment moderne cote a cote. Lequel resiste mieux ?
"@

    $directivesCode = "Simulation pluie particle. Shader forces structurelles. Split-screen final. Palette terre + vert."

} else {
    $philosophie = "L'architecture africaine comme argument. Pas comme decor."
    $conceptVisuel = "Palette sombre + lumiere chaude. Textes narratifs. Interaction par la curiosite."
    $sequenceNarrative = "ACTE 1 : Immersion. ACTE 2 : Decouverte. ACTE 3 : Comprehension. ACTE 4 : Emotion. ACTE 5 : Action."
    $directivesCode = "Three.js, OrbitControls, CSS2DRenderer, ambient occlusion, textes narratifs flottants."
}

# --- Construire la page Notion ---
$children = @()

$children += "{`"object`":`"block`",`"type`":`"callout`",`"callout`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"Storyboard v2 - Niveau professionnel. Ce document est le brief createur pour l'Agent Code. Chaque ligne compte.`"}}],`"icon`":{`"type`":`"emoji`",`"emoji`":`"\ud83c\udfa5`"},`"color`":`"purple_background`"}}"

$philosophieEscape = $philosophie -replace '"', '\"'
$conceptEscape = $conceptVisuel -replace '"', '\"'

$children += "{`"object`":`"block`",`"type`":`"heading_1`",`"heading_1`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"Brief Createur : $NomProjet`"}}]}}"
$children += "{`"object`":`"block`",`"type`":`"heading_2`",`"heading_2`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"Philosophie de l'experience`"}}]}}"
$children += "{`"object`":`"block`",`"type`":`"paragraph`",`"paragraph`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"$philosophieEscape`"},`"annotations`":{`"bold`":true}}]}}"

$children += "{`"object`":`"block`",`"type`":`"heading_2`",`"heading_2`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"Direction artistique`"}}]}}"
$children += "{`"object`":`"block`",`"type`":`"paragraph`",`"paragraph`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"$conceptEscape`"}}]}}"

$children += "{`"object`":`"block`",`"type`":`"divider`",`"divider`":{}}"
$children += "{`"object`":`"block`",`"type`":`"heading_2`",`"heading_2`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"Sequence narrative detaillee`"}}]}}"

# Decouper la sequence en paragraphes
$seqLignes = $sequenceNarrative -split "`n"
foreach ($ligne in $seqLignes) {
    $ligne = $ligne.Trim()
    if ($ligne -eq "") { continue }
    $ligneEscape = $ligne -replace '"', '\"' -replace '\\', '\\\\'
    if ($ligne -match "^(ACTE|TITRE)") {
        $children += "{`"object`":`"block`",`"type`":`"heading_3`",`"heading_3`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"$ligneEscape`"}}]}}"
    } elseif ($ligne -match "^-") {
        $ligneContent = $ligneEscape.TrimStart('-').Trim()
        $children += "{`"object`":`"block`",`"type`":`"bulleted_list_item`",`"bulleted_list_item`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"$ligneContent`"}}]}}"
    } else {
        $children += "{`"object`":`"block`",`"type`":`"paragraph`",`"paragraph`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"$ligneEscape`"}}]}}"
    }
}

$children += "{`"object`":`"block`",`"type`":`"divider`",`"divider`":{}}"
$children += "{`"object`":`"block`",`"type`":`"heading_2`",`"heading_2`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"Directives techniques pour Agent Code`"}}]}}"

$directives = $directivesCode -split "`n"
foreach ($ligne in $directives) {
    $ligne = $ligne.Trim()
    if ($ligne -eq "") { continue }
    $ligneEscape = $ligne -replace '"', '\"' -replace '\\', '\\\\'
    if ($ligne -match "^[A-Z ]+:$") {
        $children += "{`"object`":`"block`",`"type`":`"heading_3`",`"heading_3`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"$ligneEscape`"}}]}}"
    } else {
        $children += "{`"object`":`"block`",`"type`":`"bulleted_list_item`",`"bulleted_list_item`":{`"rich_text`":[{`"type`":`"text`",`"text`":{`"content`":`"$ligneEscape`"}}]}}"
    }
}

$children = $children | Select-Object -First 100
$blocsJson = $children -join ","
$titreEscape = "Brief Createur : $NomProjet (Agent v2)" -replace '"', '\"'

$body = "{
  `"parent`":{`"database_id`":`"$DATABASE_ID`"},
  `"properties`":{
    `"Name`":{`"title`":[{`"text`":{`"content`":`"$titreEscape`"}}]},
    `"Cat\u00e9gorie`":{`"select`":{`"name`":`"Planification`"}},
    `"Date`":{`"date`":{`"start`":`"$date`"}}
  },
  `"children`":[$blocsJson]
}"
$bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
try {
    $result = Invoke-RestMethod -Uri "$NOTION_API/pages" -Method POST -Headers $headers -Body $bodyBytes
    Write-Host "`n[Agent Storyboard v2] TERMINE" -ForegroundColor Green
    Write-Host "Brief createur : $($result.url)" -ForegroundColor Yellow
    return $result.url
} catch {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    Write-Host "Erreur: $($reader.ReadToEnd())" -ForegroundColor Red
    return ""
}
