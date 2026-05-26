# ============================================================
# Agent Image/3D - Meshy.ai + telechargement auto + images Notion
# ============================================================
param([string]$NomProjet = "La Takienta")

$MESHY_API_KEY = "msy_IBtfNbiumEPkQtOtnXNfc1SHalcUtPBRAbYC"
$NOTION_TOKEN  = "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"
$DATABASE_ID   = "65073e08-97ca-4c60-9cf2-da1078736240"
$NOTION_API    = "https://api.notion.com/v1"
$MESHY_API     = "https://api.meshy.ai/v2"

$notionHeaders = @{
    "Authorization"  = "Bearer $NOTION_TOKEN"
    "Notion-Version" = "2022-06-28"
    "Content-Type"   = "application/json; charset=utf-8"
}
$meshyHeaders = @{
    "Authorization" = "Bearer $MESHY_API_KEY"
    "Content-Type"  = "application/json"
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AGENT IMAGE/3D - $NomProjet" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$nomLower    = $NomProjet.ToLower()
$nomFichier  = $NomProjet.ToLower() -replace " ", "-"
$dossierOut  = "C:\Users\Kabakoo Apprenant.e\Desktop\MES PROJETS\projets-generes\$nomFichier"
$dossierAssets = "$dossierOut\assets"
if (-not (Test-Path $dossierAssets)) { New-Item -ItemType Directory -Path $dossierAssets -Force | Out-Null }

# ---- CONFIG PAR PROJET ----
if ($nomLower -like "*takienta*") {
    $promptMeshy = "Traditional Batammariba Takienta tower from Togo West Africa. Cylindrical mud brick tower with conical thatched roof, small low rectangular doorway at base, defensive architecture 2-3 stories tall, natural earth tones ochre brown beige, dry savanna landscape. Architectural 3D model clean topology game-ready. Four views: front back left right."
    $description = "Tour Takienta - Koutammakou, Togo (UNESCO)"
    $vues = @(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Koutammakou_Togo.jpg/800px-Koutammakou_Togo.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Tamberma_house.jpg/800px-Tamberma_house.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Koutammakou.jpg/800px-Koutammakou.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Togo_Koutammakou_01.jpg/800px-Togo_Koutammakou_01.jpg"
    )
    $vueTitres = @("Vue frontale - Tour principale", "Ensemble de tours dans leur paysage", "Detail architectural - base cylindrique", "Vue aerienne du village")
    $githubGlb = "https://raw.githubusercontent.com/fansestar355-star/Toguna-Assets/main/La_Takienta.glb"
} elseif ($nomLower -like "*toguna*") {
    $promptMeshy = "Dogon Toguna meeting house from Mali West Africa. Low-ceiling communal structure with thick millet stalk roof, carved wooden pillars, open sides, very low roof forces seated position. Traditional African architecture. Four views on white background."
    $description = "Toguna des Dogons - Mali"
    $vues = @("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Dogon_Toguna.jpg/800px-Dogon_Toguna.jpg")
    $vueTitres = @("Toguna avec piliers sculptes")
    $githubGlb = ""
} elseif ($nomLower -like "*musgum*") {
    $promptMeshy = "Musgum mud hut from Cameroon. Organic egg-shaped dome made of mud, decorative vertical ribbing for drainage, single small doorway, natural clay colors. Four views on white background."
    $description = "Case Musgum - Cameroun"
    $vues = @("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Musgum_mud_huts.jpg/800px-Musgum_mud_huts.jpg")
    $vueTitres = @("Case Musgum - nervures decoratives")
    $githubGlb = ""
} else {
    $promptMeshy = "Traditional African architectural structure: $NomProjet. Detailed 3D model, natural materials, earthy colors. Four views front back left right."
    $description = $NomProjet
    $vues = @()
    $vueTitres = @()
    $githubGlb = ""
}

# ---- VERIFIER SI GLB GITHUB EXISTE ----
if ($githubGlb) {
    Write-Host "  Verification modele GitHub..." -ForegroundColor Gray
    try {
        $headResp = Invoke-WebRequest -Uri $githubGlb -Method HEAD -TimeoutSec 5 -ErrorAction Stop
        Write-Host "  [OK] Modele GitHub disponible : $githubGlb" -ForegroundColor Green
        # Telecharger le GLB depuis GitHub
        $glbDest = "$dossierAssets\$nomFichier.glb"
        if (-not (Test-Path $glbDest)) {
            Write-Host "  Telechargement du modele GitHub..." -ForegroundColor Yellow
            Invoke-WebRequest -Uri $githubGlb -OutFile $glbDest -TimeoutSec 60
            Write-Host "  [OK] GLB telecharge : $glbDest" -ForegroundColor Green
        } else {
            Write-Host "  GLB deja present localement." -ForegroundColor Gray
        }
    } catch {
        Write-Host "  [Info] Modele GitHub non accessible, Meshy.ai sera utilise." -ForegroundColor Yellow
    }
}

# ---- LANCER MESHY.AI ----
Write-Host "`n  Lancement generation Meshy.ai..." -ForegroundColor Yellow
$meshyBody = @{
    mode             = "preview"
    prompt           = $promptMeshy
    art_style        = "realistic"
    negative_prompt  = "low quality blurry cartoon people humans animals"
} | ConvertTo-Json -Compress
$meshyBytes = [System.Text.Encoding]::UTF8.GetBytes($meshyBody)

$taskId = ""
try {
    $meshyResult = Invoke-RestMethod -Uri "$MESHY_API/text-to-3d" -Method POST -Headers $meshyHeaders -Body $meshyBytes
    $taskId = $meshyResult.result
    Write-Host "  [OK] Meshy.ai Task ID : $taskId" -ForegroundColor Green
} catch {
    Write-Host "  [Info] Meshy.ai : $($_.Exception.Message)" -ForegroundColor Yellow
}

# ---- POLLING MESHY.AI (attente automatique) ----
if ($taskId) {
    Write-Host ""
    Write-Host "  Attente de la generation 3D (max 10 min)..." -ForegroundColor Yellow
    Write-Host "  Tu peux continuer a travailler, je surveille automatiquement." -ForegroundColor Gray

    $maxAttempts = 20
    $attempt = 0
    $glbUrl = ""

    while ($attempt -lt $maxAttempts) {
        Start-Sleep -Seconds 30
        $attempt++
        try {
            $status = Invoke-RestMethod -Uri "$MESHY_API/text-to-3d/$taskId" -Method GET -Headers $meshyHeaders
            $pct = if ($status.progress) { "$($status.progress)%" } else { "..." }
            Write-Host "  [$attempt/20] Statut : $($status.status) $pct" -ForegroundColor Gray

            if ($status.status -eq "SUCCEEDED") {
                $glbUrl = $status.model_urls.glb
                Write-Host "  [OK] Generation terminee !" -ForegroundColor Green
                Write-Host "  GLB URL : $glbUrl" -ForegroundColor Yellow
                break
            } elseif ($status.status -eq "FAILED" -or $status.status -eq "EXPIRED") {
                Write-Host "  [Erreur] Generation Meshy echouee : $($status.status)" -ForegroundColor Red
                break
            }
        } catch {
            Write-Host "  [Retry] Verification status..." -ForegroundColor Gray
        }
    }

    # Telecharger le GLB Meshy si pas deja de modele GitHub
    if ($glbUrl) {
        $glbDest = "$dossierAssets\$nomFichier-meshy.glb"
        Write-Host "  Telechargement du modele Meshy.ai..." -ForegroundColor Yellow
        try {
            Invoke-WebRequest -Uri $glbUrl -OutFile $glbDest -TimeoutSec 120
            Write-Host "  [OK] GLB Meshy sauvegarde : $glbDest" -ForegroundColor Green
            Write-Host ""
            Write-Host "  *** MODELE 3D DISPONIBLE ***" -ForegroundColor Magenta
            Write-Host "  Fichier : $glbDest" -ForegroundColor Magenta
            Write-Host "  Verifie le modele - optimise dans Blender si besoin." -ForegroundColor Cyan
        } catch {
            Write-Host "  [Erreur] Telechargement GLB : $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# ---- CREER PAGE NOTION AVEC VRAIES IMAGES ----
$date = Get-Date -Format "yyyy-MM-dd"
$taskDisplay = if ($taskId) { $taskId } else { "non-lance" }

# Construire les blocs image
$imageBlocks = @()
for ($i = 0; $i -lt $vues.Count; $i++) {
    $imageBlocks += @{
        object = "block"
        type   = "image"
        image  = @{
            type     = "external"
            external = @{ url = $vues[$i] }
            caption  = @(@{ type="text"; text=@{content=$vueTitres[$i]} })
        }
    }
}

# Blocs etapes
$etapes = @(
    "Verifier le modele Meshy.ai sur meshy.ai (Task: $taskDisplay)",
    "GLB telecharge automatiquement dans assets/ si generation OK",
    "Si besoin : optimiser dans Blender (reduire polygones < 50k)",
    "Relancer agent-github.ps1 pour mettre en ligne avec le nouveau modele"
)
$etapeBlocks = $etapes | ForEach-Object {
    @{ object="block"; type="to_do"; to_do=@{ rich_text=@(@{type="text";text=@{content=$_}}); checked=$false } }
}

$page = @{
    parent     = @{ database_id = $DATABASE_ID }
    properties = @{
        Name = @{ title = @(@{ text = @{ content = "Images 3D : $NomProjet" } }) }
        "Categorie" = @{ select = @{ name = "3D" } }
        Date = @{ date = @{ start = $date } }
    }
    children = @(
        @{ object="block"; type="callout"; callout=@{
            rich_text=@(@{type="text";text=@{content="Generation Meshy.ai : $taskDisplay | $(if($githubGlb){"Modele GitHub disponible"}else{"Pas de modele GitHub"})"}})
            icon=@{type="emoji";emoji=[char]0x1F3A8}; color="yellow_background"
        }}
        @{ object="block"; type="heading_1"; heading_1=@{ rich_text=@(@{type="text";text=@{content=$description}}) } }
        @{ object="block"; type="heading_2"; heading_2=@{ rich_text=@(@{type="text";text=@{content="References visuelles - La Takienta"}}) } }
    ) + $imageBlocks + @(
        @{ object="block"; type="divider"; divider=@{} }
        @{ object="block"; type="heading_2"; heading_2=@{ rich_text=@(@{type="text";text=@{content="Prompt Meshy.ai utilise"}}) } }
        @{ object="block"; type="quote"; quote=@{ rich_text=@(@{type="text";text=@{content=$promptMeshy};annotations=@{italic=$true;color="gray"}}) } }
        @{ object="block"; type="divider"; divider=@{} }
        @{ object="block"; type="heading_2"; heading_2=@{ rich_text=@(@{type="text";text=@{content="Etapes suivantes"}}) } }
    ) + $etapeBlocks
}

$bodyJson = $page | ConvertTo-Json -Depth 20 -Compress
$bodyJson = $bodyJson -replace '"Categorie"', '"Cat\u00e9gorie"'
$bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($bodyJson)

try {
    $result = Invoke-RestMethod -Uri "$NOTION_API/pages" -Method POST -Headers $notionHeaders -Body $bodyBytes
    Write-Host "`n[Agent Image/3D] TERMINE" -ForegroundColor Green
    Write-Host "Page Notion : $($result.url)" -ForegroundColor Yellow
    return $result.url
} catch {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    Write-Host "Erreur Notion: $($reader.ReadToEnd())" -ForegroundColor Red
    return ""
}
