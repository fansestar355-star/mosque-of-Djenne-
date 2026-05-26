# ============================================================
# Agent Recherche v2 - Recherche PROFONDE culturelle + architecturale
# ============================================================
param([string]$NomProjet = "La Takienta")

$NOTION_TOKEN = "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"
$DATABASE_ID  = "65073e08-97ca-4c60-9cf2-da1078736240"
$NOTION_API   = "https://api.notion.com/v1"
$notionHdrs = @{
    "Authorization"  = "Bearer $NOTION_TOKEN"
    "Notion-Version" = "2022-06-28"
    "Content-Type"   = "application/json; charset=utf-8"
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AGENT RECHERCHE v2 - $NomProjet" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

function Fetch-Wiki($terme) {
    $enc = [Uri]::EscapeDataString($terme)
    foreach ($lang in @("fr","en")) {
        try {
            $r = Invoke-RestMethod -Uri "https://$lang.wikipedia.org/api/rest_v1/page/summary/$enc" `
                -Headers @{"User-Agent"="LaTakienta/2.0"} -TimeoutSec 8
            if ($r.extract -and $r.extract.Length -gt 80) { return $r.extract }
        } catch {}
    }
    return ""
}

# Helper pour creer un bloc paragraph Notion
function New-ParagraphBlock($text, $color="default") {
    return @{
        object = "block"; type = "paragraph"
        paragraph = @{ rich_text = @(@{ type="text"; text=@{content=$text}; annotations=@{color=$color} }) }
    }
}
function New-HeadingBlock($text, $level=2) {
    $t = "heading_$level"
    return @{ object="block"; type=$t; $t=@{ rich_text=@(@{type="text";text=@{content=$text}}) } }
}
function New-BulletBlock($text) {
    return @{ object="block"; type="bulleted_list_item"; bulleted_list_item=@{ rich_text=@(@{type="text";text=@{content=$text}}) } }
}
function New-CalloutBlock($text, $emoji, $color) {
    return @{ object="block"; type="callout"; callout=@{ rich_text=@(@{type="text";text=@{content=$text}}); icon=@{type="emoji";emoji=[char]0x1F4DA}; color=$color } }
}
function New-DividerBlock() { return @{ object="block"; type="divider"; divider=@{} } }

$nomLower = $NomProjet.ToLower()
$date = Get-Date -Format "yyyy-MM-dd"

# ── BASE DE CONNAISSANCE PROFONDE ──────────────────────────
if ($nomLower -like "*takienta*") {
    $savoir = [ordered]@{
        "Cosmologie - La signification cachee" = "LA TAKIENTA EST UN COSMOS EN REDUCTION. Le peuple Batammariba (litteralement : les vrais batisseurs en terre) ne construit pas une maison. Il construit un univers en trois etages. Niveau 0 : espace des animaux et des morts. Niveau 1 : espace des vivants. Niveau 2 (terrasse/grenier) : espace des ancetres et des dieux. Cette verticalite n'est pas fonctionnelle. Elle est metaphysique. Monter dans la Takienta, c'est monter vers le sacre."
        "Les materiaux - Une architecture feminine" = "Les murs sont en banco (terre + paille + eau + bouse de vache). Mais ce n'est pas juste de l'argile. Chaque nouvelle couche est un acte de memoire. Les femmes Batammariba sont les architectes. Ce sont elles qui badigeonnent, qui lissent, qui donnent la forme. La Takienta est un batiment feminin. Sa solidite vient des mains des femmes. Les murs font 40cm d'epaisseur : frais le jour, chauds la nuit. 2000 ans d'ingenierie thermique avant la climatisation."
        "La memoire de la resistance" = "Les Batammariba ont subi des siecles de raids esclavagistes (Bariba, Tyokossi, puis colonisateurs). La Takienta est une reponse architecturale a la violence. La porte unique est si petite qu'on doit s'agenouiller pour entrer : impossible de rentrer l'arme levee. Les toits plats permettent la surveillance a 360 degres. Les greniers en hauteur protegeaient les reserves. Chaque element architectural est une cicatrice de l'histoire et une lecon de survie."
        "Rituels - L'architecture qui parle aux morts" = "A la mort du chef de famille, sa depouille est posee sur le toit pendant les rituels. L'idee : son esprit monte vers les ancetres par la tour comme une antenne. Les autels interieurs (kuye) recoivent des offrandes. La forgerie est sacree : le forgeron est artisan et pretre. Les portes sont sculptees de motifs genealogiques. Chaque tour a un nom. Elle est membre de la famille."
        "Aujourd'hui - Entre disparition et renaissance" = "50 000 personnes vivent encore dans des Takienta au nord-est du Togo. Le Koutammakou couvre 50 000 hectares. UNESCO depuis 2004. Les tours font 5 a 8 metres. Construction : 3 a 6 mois de travail collectif. La tradition a plus de 400 ans. Des architectes africains etudient la Takienta pour reinventer l'habitat bioclimatique urbain. La Takienta n'est pas un musee. C'est un manifeste architectural vivant."
    }
    $angles = @(
        "ANGLE RESISTANCE : L'architecture comme reponse a l'esclavage et au colonialisme. L'espace physique comme acte politique.",
        "ANGLE COSMIQUE : La tour comme corps humain/univers. Descendre = mort. Monter = transcendance.",
        "ANGLE FEMININ : Les architectes oubliees. Les femmes Batammariba qui batissent avec leurs mains depuis 400 ans.",
        "ANGLE PROCESSUS : La Takienta meurt et renait chaque annee. Ce n'est pas un batiment fige. C'est un acte continu.",
        "ANGLE VIVANT : 50 000 personnes y vivent aujourd'hui. Comment habite-t-on une Takienta en 2026 ?"
    )
    $recherches = @("Koutammakou UNESCO Togo","Batammariba people Togo","Tamberma house Togo")
} else {
    $savoir = [ordered]@{ "Contexte" = "Etude de $NomProjet, patrimoine architectural africain." }
    $angles = @("L'ingenierie africaine comme solution universelle.","La memoire du corps : habiter un espace c'est l'incorporer.")
    $recherches = @($NomProjet, "architecture africaine $NomProjet")
}

# ── RECHERCHES WIKIPEDIA ───────────────────────────────────
$resultatsWiki = @()
foreach ($terme in $recherches) {
    Write-Host "  Recherche : $terme..." -ForegroundColor Gray
    $texte = Fetch-Wiki $terme
    if ($texte) {
        $resultatsWiki += @{terme=$terme; contenu=$texte}
        Write-Host "  [OK] $terme" -ForegroundColor Green
    }
}

# ── CONSTRUIRE LES BLOCS ───────────────────────────────────
$blocks = @()
$blocks += New-CalloutBlock "Recherche approfondie Agent v2 : culture + architecture + rituels. Source : Wikipedia + base de connaissance anthropologique." "?" "blue_background"
$blocks += New-HeadingBlock "Etude approfondie : $NomProjet" 1

foreach ($key in $savoir.Keys) {
    $blocks += New-HeadingBlock $key 2
    # Decouper en morceaux de 1900 chars
    $texte = $savoir[$key]
    $pos = 0
    while ($pos -lt $texte.Length) {
        $morceau = $texte.Substring($pos, [Math]::Min(1900, $texte.Length - $pos))
        $pos += 1900
        $blocks += New-ParagraphBlock $morceau
    }
    $blocks += New-DividerBlock
}

if ($resultatsWiki.Count -gt 0) {
    $blocks += New-HeadingBlock "Sources Wikipedia" 2
    foreach ($r in $resultatsWiki) {
        $blocks += New-HeadingBlock $r.terme 3
        $texte = $r.contenu; $pos = 0
        while ($pos -lt $texte.Length) {
            $morceau = $texte.Substring($pos, [Math]::Min(1900, $texte.Length - $pos))
            $pos += 1900
            $blocks += New-ParagraphBlock $morceau "gray"
        }
    }
    $blocks += New-DividerBlock
}

$blocks += New-HeadingBlock "Angles narratifs pour l'experience WebAR" 2
foreach ($a in $angles) { $blocks += New-BulletBlock $a }

# Limiter a 100 blocs (limite Notion)
$blocks = $blocks | Select-Object -First 100

# ── CREER LA PAGE NOTION ──────────────────────────────────
$page = @{
    parent = @{ database_id = $DATABASE_ID }
    properties = @{
        Name = @{ title = @(@{ text = @{ content = "Etude profonde : $NomProjet (Agent v2)" } }) }
        "Categorie" = @{ select = @{ name = "Recherche" } }
        Date = @{ date = @{ start = $date } }
    }
    children = $blocks
}

# Serialiser proprement avec ConvertTo-Json
$bodyJson = $page | ConvertTo-Json -Depth 20 -Compress
# Corriger la cle Categorie avec accent
$bodyJson = $bodyJson -replace '"Categorie"', '"Cat\u00e9gorie"'
$bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($bodyJson)

try {
    $result = Invoke-RestMethod -Uri "$NOTION_API/pages" -Method POST -Headers $notionHdrs -Body $bodyBytes
    Write-Host "`n[Agent Recherche v2] TERMINE" -ForegroundColor Green
    Write-Host "Etude : $($result.url)" -ForegroundColor Yellow
    return $result.url
} catch {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $errDetail = $reader.ReadToEnd()
    Write-Host "Erreur Notion: $errDetail" -ForegroundColor Red
    return ""
}
