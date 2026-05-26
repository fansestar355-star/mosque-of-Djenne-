# ============================================================
# Agent GitHub - Pousse l'experience sur GitHub Pages
# ============================================================
param([string]$NomProjet = "La Takienta")

$GITHUB_TOKEN = "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"
$GITHUB_USER  = "fansestar355-star"
$GITHUB_API   = "https://api.github.com"

$headers = @{
    "Authorization" = "token $GITHUB_TOKEN"
    "Accept"        = "application/vnd.github.v3+json"
    "Content-Type"  = "application/json"
    "User-Agent"    = "LaTakienta-Agent"
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AGENT GITHUB - Projet : $NomProjet" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Mapping projet -> repo
$nomLower = $NomProjet.ToLower()
if ($nomLower -like "*takienta*") { $repo = "La-Takienta" }
elseif ($nomLower -like "*toguna*") { $repo = "Toguna-Experience" }
elseif ($nomLower -like "*musgum*") { $repo = "Dome-Musgum" }
else { $repo = $NomProjet -replace " ", "-" }

$nomFichier = $NomProjet.ToLower() -replace " ", "-"
$dossierSource = "C:\Users\Kabakoo Apprenant.e\Desktop\MES PROJETS\projets-generes\$nomFichier"
$indexPath = "$dossierSource\index.html"

if (-not (Test-Path $indexPath)) {
    Write-Host "  [Erreur] index.html non trouve dans $dossierSource" -ForegroundColor Red
    Write-Host "  Lance d'abord agent-code.ps1" -ForegroundColor Yellow
    exit 1
}

function Get-FileSha($repoName, $chemin) {
    try {
        $r = Invoke-RestMethod -Uri "$GITHUB_API/repos/$GITHUB_USER/$repoName/contents/$chemin" -Method GET -Headers $headers
        return $r.sha
    } catch { return $null }
}

function Push-File($repoName, $cheminLocal, $cheminGithub, $message) {
    $contenu = [System.IO.File]::ReadAllBytes($cheminLocal)
    $contenuB64 = [Convert]::ToBase64String($contenu)
    $sha = Get-FileSha $repoName $cheminGithub

    $data = @{ message = $message; content = $contenuB64; branch = "main" }
    if ($sha) { $data.sha = $sha }

    $body = $data | ConvertTo-Json -Depth 3
    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)

    try {
        $r = Invoke-RestMethod -Uri "$GITHUB_API/repos/$GITHUB_USER/$repoName/contents/$cheminGithub" -Method PUT -Headers $headers -Body $bodyBytes
        Write-Host "  [OK] $cheminGithub" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "  [Erreur] $cheminGithub : $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Pousser index.html
$dateCommit = Get-Date -Format "yyyy-MM-dd HH:mm"
$succes = Push-File $repo $indexPath "index.html" "Experience WebAR $NomProjet - Agent Auto - $dateCommit"

# Pousser les GLB si presents
$assetsDir = "$dossierSource\assets"
if (Test-Path $assetsDir) {
    Get-ChildItem -Path $assetsDir -Include "*.glb","*.gltf" -Recurse | ForEach-Object {
        Push-File $repo $_.FullName "assets/$($_.Name)" "Modele 3D : $($_.Name)"
    }
}

# Activer GitHub Pages
$pagesData = @{ source = @{ branch = "main"; path = "/" } }
$pagesBody = ($pagesData | ConvertTo-Json)
$pagesBytesArr = [System.Text.Encoding]::UTF8.GetBytes($pagesBody)
try {
    Invoke-RestMethod -Uri "$GITHUB_API/repos/$GITHUB_USER/$repo/pages" -Method POST -Headers $headers -Body $pagesBytesArr | Out-Null
} catch {
    try {
        Invoke-RestMethod -Uri "$GITHUB_API/repos/$GITHUB_USER/$repo/pages" -Method PUT -Headers $headers -Body $pagesBytesArr | Out-Null
    } catch { }
}

$urlPublique = "https://$GITHUB_USER.github.io/$repo/"

Write-Host "`n[Agent GitHub] TERMINE" -ForegroundColor Green
Write-Host "URL publique : $urlPublique" -ForegroundColor Yellow
Write-Host "(Attendre 1-2 minutes pour le deploiement GitHub Pages)" -ForegroundColor Gray
return $urlPublique
