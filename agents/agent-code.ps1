# ============================================================
# Agent Code v2 - Experience WebAR haute qualite
# Mentalite : studio de creation numerique, pas un dev generique
# ============================================================
param([string]$NomProjet = "La Takienta")

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AGENT CODE v2 - $NomProjet" -ForegroundColor Cyan
Write-Host "  Niveau : experience immersive professionnelle" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$nomFichier = $NomProjet.ToLower() -replace " ", "-"
$dossierSortie = "C:\Users\Kabakoo Apprenant.e\Desktop\MES PROJETS\projets-generes\$nomFichier"
$dossierAssets = "$dossierSortie\assets"
if (-not (Test-Path $dossierSortie)) { New-Item -ItemType Directory -Path $dossierSortie -Force | Out-Null }
if (-not (Test-Path $dossierAssets)) { New-Item -ItemType Directory -Path $dossierAssets -Force | Out-Null }

$glbPath = "./assets/$nomFichier.glb"
$glbTrouve = Get-ChildItem -Path $dossierAssets -Filter "*.glb" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($glbTrouve) { $glbPath = "./assets/$($glbTrouve.Name)"; Write-Host "  GLB: $($glbTrouve.Name)" -ForegroundColor Green }
else { Write-Host "  Placeholder 3D procedral (banco shader)" -ForegroundColor Yellow }

Write-Host "  Generation de l'experience..." -ForegroundColor Yellow

$htmlContent = @'
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>La Takienta — Koutammakou</title>
<style>
  *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:100%; height:100%; background:#000; overflow:hidden; }
  canvas { display:block; }

  /* ── LOADING ── */
  #boot {
    position:fixed; inset:0; background:#000;
    display:flex; align-items:center; justify-content:center;
    z-index:200; transition:opacity 1.8s ease;
  }
  #boot-particle {
    width:4px; height:4px; border-radius:50%;
    background:#c1440e; box-shadow:0 0 12px 4px #c1440e88;
    animation:fall 2s ease-in infinite;
  }
  @keyframes fall { 0%{transform:translateY(-60px);opacity:0} 60%{opacity:1} 100%{transform:translateY(60px);opacity:0} }

  /* ── CANVAS CONTAINER ── */
  #app { position:fixed; inset:0; }

  /* ── TEXTES NARRATIFS CSS ── */
  #narrative {
    position:fixed; inset:0; pointer-events:none; z-index:10;
    display:flex; align-items:center; justify-content:center;
  }
  .n-text {
    font-family:'Georgia',serif; color:#ffe4b5; text-align:center;
    font-size:clamp(1rem,2.5vw,1.4rem); line-height:1.8;
    max-width:640px; padding:0 24px;
    opacity:0; transform:translateY(8px);
    transition:opacity 1.4s ease, transform 1.4s ease;
    text-shadow:0 2px 20px rgba(0,0,0,.9), 0 0 40px rgba(193,68,14,.3);
  }
  .n-text.show { opacity:1; transform:translateY(0); }
  .n-text em { font-style:italic; color:#f4a460; }

  /* ── SOUS-TITRE LOCATIF ── */
  #locator {
    position:fixed; top:24px; left:50%; transform:translateX(-50%);
    color:#8b4513; font-family:Georgia,serif; font-size:.75rem;
    letter-spacing:.2em; text-transform:uppercase;
    opacity:0; transition:opacity 2s;
    pointer-events:none;
  }

  /* ── ANNOTATIONS 3D ── */
  .ann {
    font-family:Georgia,serif; font-size:.78rem;
    color:#ffe4b5; pointer-events:all; cursor:pointer;
    border-left:2px solid #c1440e; padding:4px 10px;
    background:rgba(10,5,0,.75); backdrop-filter:blur(6px);
    opacity:0; transition:opacity .8s; white-space:nowrap;
    max-width:220px; white-space:normal; line-height:1.4;
  }
  .ann.show { opacity:1; }
  .ann:hover { color:#f4a460; border-color:#f4a460; }

  /* ── PANEL DETAIL ── */
  #detail {
    position:fixed; bottom:0; left:0; right:0; z-index:20;
    background:linear-gradient(0deg,rgba(5,2,0,.97) 0%,rgba(5,2,0,.8) 70%,transparent);
    padding:36px 28px 28px; color:#ffe4b5;
    font-family:Georgia,serif;
    transform:translateY(100%); transition:transform .55s cubic-bezier(.4,0,.2,1);
  }
  #detail.open { transform:translateY(0); }
  #detail h3 { font-size:1.15rem; margin-bottom:10px; color:#f4a460; letter-spacing:.05em; }
  #detail p  { font-size:.88rem; line-height:1.75; color:#d2b48c; max-width:600px; }
  #detail-close {
    position:absolute; top:14px; right:18px;
    background:none; border:1px solid #5a3010; color:#ffe4b5;
    width:30px; height:30px; border-radius:50%; cursor:pointer;
    font-size:.85rem; display:flex; align-items:center; justify-content:center;
  }

  /* ── CONTROLS ── */
  #ctrl {
    position:fixed; bottom:28px; right:20px;
    display:flex; flex-direction:column; gap:10px; z-index:15;
  }
  .cb {
    width:44px; height:44px; border-radius:50%; border:none; cursor:pointer;
    background:rgba(193,68,14,.8); color:#ffe8cc;
    font-size:1.1rem; display:flex; align-items:center; justify-content:center;
    backdrop-filter:blur(6px); box-shadow:0 4px 16px rgba(193,68,14,.35);
    transition:transform .2s, background .2s; opacity:0; pointer-events:none;
  }
  .cb.ready { opacity:1; pointer-events:all; }
  .cb:hover { transform:scale(1.1); background:rgba(244,164,96,.85); }

  /* ── BADGE UNESCO ── */
  #badge {
    position:fixed; top:20px; left:20px; z-index:15;
    background:rgba(5,2,0,.82); border:1px solid #5a3010; border-radius:6px;
    padding:7px 14px; color:#f4a460; font-family:Georgia,serif;
    font-size:.7rem; letter-spacing:.12em; text-transform:uppercase;
    opacity:0; transition:opacity 1.5s; pointer-events:none;
    backdrop-filter:blur(6px);
  }

  /* ── CURSEUR BRAISE ── */
  #cursor {
    position:fixed; width:8px; height:8px; border-radius:50%;
    background:#c1440e; box-shadow:0 0 10px 3px #c1440e88;
    pointer-events:none; z-index:999; transform:translate(-50%,-50%);
    transition:width .15s, height .15s, opacity .3s; opacity:0;
  }
  body:hover #cursor { opacity:1; }
</style>
</head>
<body>

<div id="boot"><div id="boot-particle"></div></div>
<div id="app"></div>
<div id="badge">Koutammakou &mdash; UNESCO 2004</div>
<div id="locator">Koutammakou &bull; Nord-Est Togo</div>
<div id="narrative"><p class="n-text" id="nt"></p></div>

<div id="detail">
  <button id="detail-close" onclick="closeDetail()">&#215;</button>
  <h3 id="d-title"></h3>
  <p id="d-body"></p>
</div>

<div id="ctrl">
  <button class="cb" id="btn-rot" title="Rotation auto">&#8635;</button>
  <button class="cb" id="btn-reset" title="Vue initiale">&#8962;</button>
  <button class="cb" id="btn-info" title="A propos">&#9432;</button>
</div>

<div id="cursor"></div>

<script type="importmap">
{"imports":{
  "three":"https://unpkg.com/three@0.160.0/build/three.module.js",
  "three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"
}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls }    from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader }       from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader }      from 'three/addons/loaders/DRACOLoader.js';
import { Sky }              from 'three/addons/objects/Sky.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

// ─────────────────────────────────────────────
// CURSEUR PERSONNALISE
// ─────────────────────────────────────────────
const cur = document.getElementById('cursor');
document.addEventListener('mousemove', e => {
  cur.style.left = e.clientX + 'px';
  cur.style.top  = e.clientY + 'px';
});
document.body.style.cursor = 'none';

// ─────────────────────────────────────────────
// SCENE
// ─────────────────────────────────────────────
const W = innerWidth, H = innerHeight;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(W, H);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.6;  // Sombre et chaleureux
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.getElementById('app').appendChild(renderer.domElement);

const labelRdr = new CSS2DRenderer();
labelRdr.setSize(W, H);
Object.assign(labelRdr.domElement.style, { position:'absolute', top:'0', pointerEvents:'none' });
document.getElementById('app').appendChild(labelRdr.domElement);

const scene = new THREE.Scene();
// Brume chaude epaisse : on emerge de la chaleur
scene.fog = new THREE.FogExp2(0x1a0800, 0.006);
scene.background = new THREE.Color(0x050200);

const camera = new THREE.PerspectiveCamera(55, W/H, 0.1, 600);
camera.position.set(12, 5, 16);

// ─────────────────────────────────────────────
// CONTROLES — rotation douce autour de la tour
// ─────────────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.04;
controls.minDistance  = 4;
controls.maxDistance  = 35;
controls.maxPolarAngle = Math.PI * 0.82;
controls.target.set(0, 3, 0);
controls.autoRotate = true;
controls.autoRotateSpeed = 0.25;

// ─────────────────────────────────────────────
// CIEL NUIT AFRICAINE
// ─────────────────────────────────────────────
// Etoiles
const starGeo = new THREE.BufferGeometry();
const starPos = new Float32Array(4000 * 3);
for (let i = 0; i < 4000; i++) {
  const r = 280;
  const theta = Math.random() * Math.PI * 2;
  const phi   = Math.acos(2 * Math.random() - 1);
  starPos[i*3]   = r * Math.sin(phi) * Math.cos(theta);
  starPos[i*3+1] = r * Math.abs(Math.sin(phi));   // hemisphere haut
  starPos[i*3+2] = r * Math.sin(phi) * Math.sin(theta);
}
starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color:0xffeedd, size:0.35, transparent:true, opacity:.6 })));

// Horizon rougeoyant (coucher de soleil lointain)
const skyGeo = new THREE.SphereGeometry(280, 32, 16);
const skyMat = new THREE.ShaderMaterial({
  side: THREE.BackSide,
  uniforms: { uTime: { value:0 } },
  vertexShader: `
    varying vec3 vPos;
    void main(){ vPos=position; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }
  `,
  fragmentShader: `
    varying vec3 vPos;
    void main(){
      float h = normalize(vPos).y;
      vec3 night  = vec3(0.01,0.005,0.0);
      vec3 horizon= vec3(0.25,0.06,0.01);
      vec3 col = mix(horizon, night, smoothstep(-0.05,0.35,h));
      gl_FragColor = vec4(col,1.);
    }
  `
});
scene.add(new THREE.Mesh(skyGeo, skyMat));

// ─────────────────────────────────────────────
// LUMIERES — ambiance feu de bois la nuit
// ─────────────────────────────────────────────
scene.add(new THREE.AmbientLight(0x1a0800, 0.35));

// Lumiere principale : comme une torche
const fireLight = new THREE.PointLight(0xff6b20, 3.0, 30);
fireLight.position.set(0, 0.6, 3);
fireLight.castShadow = true;
fireLight.shadow.mapSize.set(1024, 1024);
scene.add(fireLight);

// Lumiere de remplissage tres douce
const rimLight = new THREE.DirectionalLight(0x3d1500, 0.4);
rimLight.position.set(-8, 12, -6);
scene.add(rimLight);

// ─────────────────────────────────────────────
// SOL — terre ocre africaine
// ─────────────────────────────────────────────
const groundGeo = new THREE.PlaneGeometry(80, 80, 40, 40);
// Legere ondulation du terrain
const gPos = groundGeo.attributes.position;
for (let i = 0; i < gPos.count; i++) {
  gPos.setZ(i, (Math.random()-0.5) * 0.18 + Math.sin(gPos.getX(i)*0.3)*0.08);
}
groundGeo.computeVertexNormals();
const groundMat = new THREE.MeshStandardMaterial({
  color: 0x6b3a10, roughness: 1, metalness: 0,
});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI/2;
ground.receiveShadow = true;
scene.add(ground);

// Rochers/pierres disperses
const rockMat = new THREE.MeshStandardMaterial({ color:0x4a2d0d, roughness:0.95 });
for (let i = 0; i < 18; i++) {
  const r = 2 + Math.random() * 0.8;
  const geo = new THREE.DodecahedronGeometry(r * (0.08 + Math.random()*0.15), 0);
  const rock = new THREE.Mesh(geo, rockMat);
  const angle = Math.random() * Math.PI * 2;
  const dist  = 8 + Math.random() * 22;
  rock.position.set(Math.cos(angle)*dist, 0, Math.sin(angle)*dist);
  rock.rotation.set(Math.random()*2, Math.random()*2, Math.random()*2);
  rock.castShadow = true;
  scene.add(rock);
}

// ─────────────────────────────────────────────
// PARTICULES — poussiere du Sahel + braises
// ─────────────────────────────────────────────
const dustCount = 800;
const dustPos = new Float32Array(dustCount * 3);
const dustVel = new Float32Array(dustCount * 3);
for (let i = 0; i < dustCount; i++) {
  dustPos[i*3]   = (Math.random()-0.5)*50;
  dustPos[i*3+1] = Math.random()*12;
  dustPos[i*3+2] = (Math.random()-0.5)*50;
  dustVel[i*3]   = (Math.random()-0.5)*0.008;
  dustVel[i*3+1] = (Math.random()-0.5)*0.003;
  dustVel[i*3+2] = (Math.random()-0.5)*0.006;
}
const dustGeo = new THREE.BufferGeometry();
dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({
  color:0xc1440e, size:0.07, transparent:true, opacity:0.35, depthWrite:false
}));
scene.add(dust);

// Braises montantes autour du feu
const emberCount = 120;
const emberPos = new Float32Array(emberCount * 3);
const emberVel = new Float32Array(emberCount * 3);
for (let i = 0; i < emberCount; i++) {
  emberPos[i*3]   = (Math.random()-0.5)*1.5;
  emberPos[i*3+1] = Math.random()*0.5;
  emberPos[i*3+2] = 2.5 + (Math.random()-0.5)*1.5;
  emberVel[i*3]   = (Math.random()-0.5)*0.02;
  emberVel[i*3+1] = 0.015 + Math.random()*0.025;
  emberVel[i*3+2] = (Math.random()-0.5)*0.01;
}
const emberGeo = new THREE.BufferGeometry();
emberGeo.setAttribute('position', new THREE.BufferAttribute(emberPos, 3));
const embers = new THREE.Points(emberGeo, new THREE.PointsMaterial({
  color:0xff8c00, size:0.12, transparent:true, opacity:0.85, depthWrite:false
}));
scene.add(embers);

// ─────────────────────────────────────────────
// FEU DE CAMP — geometrie simple
// ─────────────────────────────────────────────
const logMat = new THREE.MeshStandardMaterial({ color:0x2a1005, roughness:1 });
for (let i = 0; i < 4; i++) {
  const log = new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.08,0.9,6), logMat);
  const a = (i/4)*Math.PI*2;
  log.position.set(Math.cos(a)*0.4, 0, 2.5+Math.sin(a)*0.25);
  log.rotation.z = Math.PI/2;
  log.rotation.y = a;
  scene.add(log);
}

// ─────────────────────────────────────────────
// MODELE 3D — Takienta
// ─────────────────────────────────────────────
let mainTower = null;
let annotationsCreated = false;

// Shader banco (argile) procedural
const bancoMat = new THREE.MeshStandardMaterial({
  color: 0xb5601a,
  roughness: 0.92,
  metalness: 0.0,
});
const roofMat = new THREE.MeshStandardMaterial({
  color: 0x7a6030,
  roughness: 1.0,
  metalness: 0.0,
});
const doorMat = new THREE.MeshStandardMaterial({
  color: 0x1a0800,
  roughness: 0.8,
});

function buildPlaceholder() {
  const g = new THREE.Group();

  // Tour principale
  const mainGrp = new THREE.Group();

  // Mur cylindrique 3 niveaux
  const base = new THREE.Mesh(new THREE.CylinderGeometry(1.35,1.55,1.4,20), bancoMat);
  base.position.y = 0.7; base.castShadow = true; base.receiveShadow = true;
  mainGrp.add(base);

  const mid = new THREE.Mesh(new THREE.CylinderGeometry(1.25,1.38,1.6,20), bancoMat);
  mid.position.y = 2.2; mid.castShadow = true; mid.receiveShadow = true;
  mainGrp.add(mid);

  const top = new THREE.Mesh(new THREE.CylinderGeometry(1.0,1.28,1.2,20), bancoMat);
  top.position.y = 3.7; top.castShadow = true; top.receiveShadow = true;
  mainGrp.add(top);

  // Terrasse / rebord avant le toit
  const terr = new THREE.Mesh(new THREE.CylinderGeometry(1.1,1.05,0.25,20), bancoMat);
  terr.position.y = 4.42; terr.castShadow = true;
  mainGrp.add(terr);

  // Toit conique
  const roof = new THREE.Mesh(new THREE.ConeGeometry(1.55,2.2,20), roofMat);
  roof.position.y = 5.65; roof.castShadow = true;
  mainGrp.add(roof);

  // Petite porte basse (entree qui oblige a se baisser)
  const door = new THREE.Mesh(new THREE.BoxGeometry(0.38,0.68,0.12), doorMat);
  door.position.set(0,0.34,1.35);
  mainGrp.add(door);

  // Petite fenetre sur le flanc
  const win = new THREE.Mesh(new THREE.BoxGeometry(0.18,0.18,0.12), doorMat);
  win.position.set(1.3,2.5,0);
  mainGrp.add(win);

  mainTower = mainGrp;
  g.add(mainGrp);

  // Tours secondaires (2 + 1 grenier)
  const secondaryData = [
    { x:-4.5, z:-2, scale:0.72, h:3.8 },
    { x: 4.2, z:-2.5, scale:0.65, h:3.4 },
    { x: 1.5, z:-5, scale:0.5, h:2.8 },
  ];
  secondaryData.forEach(d => {
    const sg = new THREE.Group();
    const sw = new THREE.Mesh(new THREE.CylinderGeometry(d.scale,d.scale*1.1,d.h,16), bancoMat);
    sw.position.y = d.h/2; sw.castShadow = true; sg.add(sw);
    const sr = new THREE.Mesh(new THREE.ConeGeometry(d.scale*1.15,d.h*0.4,16), roofMat);
    sr.position.y = d.h*1.18; sr.castShadow = true; sg.add(sr);
    sg.position.set(d.x,0,d.z);
    g.add(sg);
  });

  // Feux secondaires
  const secFirePositions = [[-4.5,0,-2],[4.2,0,-2.5]];
  secFirePositions.forEach(p => {
    const fl = new THREE.PointLight(0xff5500, 1.2, 8);
    fl.position.set(p[0]+0.5, 0.5, p[2]+0.8);
    scene.add(fl);
  });

  scene.add(g);
  return g;
}

// Charger GLB ou placeholder
const dracoLdr = new DRACOLoader();
dracoLdr.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
const gltfLdr = new GLTFLoader();
gltfLdr.setDRACOLoader(dracoLdr);

gltfLdr.load('GLB_PATH_PLACEHOLDER',
  gltf => {
    const m = gltf.scene;
    const box = new THREE.Box3().setFromObject(m);
    const s = 5.5 / Math.max(...box.getSize(new THREE.Vector3()).toArray());
    m.scale.setScalar(s);
    const c = box.getCenter(new THREE.Vector3());
    m.position.set(-c.x*s, -box.min.y*s, -c.z*s);
    m.traverse(ch => { if(ch.isMesh){ ch.castShadow=true; ch.receiveShadow=true; } });
    mainTower = m;
    scene.add(m);
    finishLoading();
  },
  null,
  () => { buildPlaceholder(); finishLoading(); }
);

// ─────────────────────────────────────────────
// SEQUENCE NARRATIVE
// ─────────────────────────────────────────────
const nt = document.getElementById('nt');
function showText(html, duration) {
  return new Promise(resolve => {
    nt.innerHTML = html;
    nt.classList.add('show');
    setTimeout(() => {
      nt.classList.remove('show');
      setTimeout(resolve, 1400);
    }, duration);
  });
}

async function runNarrative() {
  await delay(800);
  await showText("Ils appelaient cet endroit <em>Koutammakou</em>.", 3200);
  await delay(400);
  await showText("La terre qui se souvient.", 2800);
  await delay(300);
  await showText("Pendant 400 ans, ils ont construit.<br>Après chaque saison de pluie. Après chaque raid.", 4000);
  await delay(400);
  await showText("Ils n'ont pas bâti un monument.<br>Ils ont répondu à la violence par l'architecture.", 4200);
  await delay(600);
  // Afficher les annotations
  createAnnotations();
  document.getElementById('badge').style.opacity = '1';
  document.getElementById('locator').style.opacity = '1';
  document.querySelectorAll('.cb').forEach(b => b.classList.add('ready'));
}

function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

// ─────────────────────────────────────────────
// ANNOTATIONS — données culturelles réelles
// ─────────────────────────────────────────────
const ANNOTATIONS = [
  {
    pos: new THREE.Vector3(0, 6.8, 0),
    label: "Grenier sacré",
    title: "Le grenier — Espace des ancêtres",
    body: "Au sommet de la Takienta, les semences de mil sont gardées dans le grenier. Mais c'est aussi le lieu de communication avec les ancêtres. Les esprits montent par la tour comme une antenne vers le ciel. Monter dans la Takienta, c'est se rapprocher du sacré."
  },
  {
    pos: new THREE.Vector3(1.6, 0.3, 0),
    label: "La porte basse",
    title: "La porte — Acte d'humilité forcée",
    body: "Cette porte est si petite qu'on doit s'agenouiller pour entrer. Ce n'est pas un hasard. Pendant des siècles de raids esclavagistes, un ennemi armé ne pouvait pas entrer l'arme levée. La contrainte physique est une stratégie de survie. L'architecture comme résistance."
  },
  {
    pos: new THREE.Vector3(-1.4, 2.5, 0.5),
    label: "Murs en banco",
    title: "Les murs — Architecture féminine",
    body: "40 cm d'épaisseur d'argile, de paille et de bouse de vache. Ce sont les femmes Batammariba qui construisent et réparent ces murs avec leurs mains. La Takienta est un bâtiment féminin. Sa solidité vient de leur savoir transmis de mère en fille depuis des générations."
  },
  {
    pos: new THREE.Vector3(0, 4.5, 1.5),
    label: "Terrasse de vie",
    title: "La terrasse — Entre ciel et terre",
    body: "La terrasse est le niveau des vivants : on y dort, on y cuisine, on observe le territoire à 360 degrés. C'est aussi un poste de surveillance. Dans la cosmologie Batammariba, ce niveau intermédiaire est celui des humains — entre les animaux (bas) et les ancêtres (haut)."
  },
];

function createAnnotations() {
  if (annotationsCreated) return;
  annotationsCreated = true;
  ANNOTATIONS.forEach(data => {
    const div = document.createElement('div');
    div.className = 'ann';
    div.textContent = data.label;
    div.addEventListener('pointerdown', () => openDetail(data.title, data.body));
    const obj = new CSS2DObject(div);
    obj.position.copy(data.pos);
    scene.add(obj);
    setTimeout(() => div.classList.add('show'), 500 + Math.random()*1200);
  });
}

function openDetail(title, body) {
  document.getElementById('d-title').textContent = title;
  document.getElementById('d-body').textContent = body;
  document.getElementById('detail').classList.add('open');
}
window.closeDetail = () => document.getElementById('detail').classList.remove('open');

// ─────────────────────────────────────────────
// BOOT → SCENE
// ─────────────────────────────────────────────
function finishLoading() {
  const boot = document.getElementById('boot');
  // Explosion de la particule
  boot.style.opacity = '0';
  setTimeout(() => { boot.style.display = 'none'; runNarrative(); }, 1800);
}

// ─────────────────────────────────────────────
// BOUTONS
// ─────────────────────────────────────────────
let autoRot = true;
document.getElementById('btn-rot').addEventListener('click', () => {
  autoRot = !autoRot;
  controls.autoRotate = autoRot;
});
document.getElementById('btn-reset').addEventListener('click', () => {
  camera.position.set(12, 5, 16);
  controls.target.set(0, 3, 0);
  controls.update();
});
document.getElementById('btn-info').addEventListener('click', () => {
  openDetail(
    'La Takienta — Koutammakou',
    'Les tours Takienta sont les maisons-fortresses du peuple Batammariba au nord-est du Togo. Inscrites au Patrimoine Mondial de l\'UNESCO en 2004, elles abritent encore 50 000 personnes aujourd\'hui. Ce ne sont pas des ruines. C\'est une civilisation vivante.'
  );
});

// ─────────────────────────────────────────────
// BOUCLE D'ANIMATION
// ─────────────────────────────────────────────
const clock = new THREE.Clock();
let frame = 0;

function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();
  frame++;

  controls.update();

  // Scintillement du feu
  fireLight.intensity = 2.8 + Math.sin(t * 7.3) * 0.6 + Math.sin(t * 13.1) * 0.3;
  fireLight.position.x = Math.sin(t * 2.1) * 0.08;
  fireLight.position.z = 3 + Math.sin(t * 3.4) * 0.06;

  // Gradient ciel dynamique (coucher de soleil tres lent)
  skyMat.uniforms.uTime.value = t;

  // Poussiere (vent)
  if (frame % 2 === 0) {
    const dp = dustGeo.attributes.position;
    for (let i = 0; i < dustCount; i++) {
      dp.setX(i, dp.getX(i) + dustVel[i*3]   + 0.005);
      dp.setY(i, dp.getY(i) + dustVel[i*3+1] + Math.sin(t*0.5+i)*0.001);
      dp.setZ(i, dp.getZ(i) + dustVel[i*3+2]);
      if (dp.getX(i) > 25) dp.setX(i, -25);
      if (dp.getY(i) > 14) dp.setY(i, 0.2);
    }
    dp.needsUpdate = true;
  }

  // Braises montantes
  const ep = emberGeo.attributes.position;
  for (let i = 0; i < emberCount; i++) {
    ep.setX(i, ep.getX(i) + emberVel[i*3]   + Math.sin(t*3+i)*0.002);
    ep.setY(i, ep.getY(i) + emberVel[i*3+1]);
    ep.setZ(i, ep.getZ(i) + emberVel[i*3+2]);
    if (ep.getY(i) > 6) { // Recycler la braise
      ep.setX(i, (Math.random()-0.5)*1.2);
      ep.setY(i, 0.1);
      ep.setZ(i, 2.5 + (Math.random()-0.5)*1.2);
    }
  }
  ep.needsUpdate = true;

  renderer.render(scene, camera);
  labelRdr.render(scene, camera);
}
animate();

// ─────────────────────────────────────────────
// RESPONSIVE
// ─────────────────────────────────────────────
window.addEventListener('resize', () => {
  const w = innerWidth, h = innerHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  labelRdr.setSize(w, h);
});

// Gyroscope mobile
if (window.DeviceOrientationEvent) {
  window.addEventListener('deviceorientation', e => {
    if (!e.beta) return;
    const b = THREE.MathUtils.degToRad(e.beta  - 45);
    const g = THREE.MathUtils.degToRad(e.gamma);
    camera.position.x += g * 0.02;
    camera.position.y = Math.max(2, Math.min(20, 5 + b * 3));
    controls.update();
  });
}
</script>
</body>
</html>
'@

# Injecter le bon chemin GLB
$htmlContent = $htmlContent -replace "GLB_PATH_PLACEHOLDER", $glbPath

$cheminHTML = "$dossierSortie\index.html"
[System.IO.File]::WriteAllText($cheminHTML, $htmlContent, [System.Text.Encoding]::UTF8)

Write-Host "`n[Agent Code v2] TERMINE" -ForegroundColor Green
Write-Host "Fichier : $cheminHTML" -ForegroundColor Yellow
Write-Host "Taille  : $([Math]::Round($htmlContent.Length/1024, 1)) KB" -ForegroundColor Gray
Write-Host "`nPour tester : ouvrir dans Chrome (serveur local recommande)" -ForegroundColor Cyan
return $cheminHTML
