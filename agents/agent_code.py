"""
Agent 4 : Generation du code WebAR
- Recoit le prompt detaille du storyboard
- Genere le fichier HTML complet de l'experience
- Sauvegarde dans le dossier du projet
"""

import os
from datetime import datetime

def generer_experience_takienta(nom_projet, glb_path=None):
    """
    Genere une experience WebAR complete pour La Takienta
    Concept : Voyage dans le temps - la tour se construit devant toi
    """

    nom_fichier = nom_projet.lower().replace(" ", "-")
    if not glb_path:
        glb_path = f"./assets/{nom_fichier}.glb"

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>{nom_projet} - Experience WebAR</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #0a0a0a; overflow: hidden; font-family: 'Georgia', serif; }}

    #canvas-container {{ width: 100vw; height: 100vh; position: relative; }}

    /* Overlay de chargement */
    #loading-screen {{
      position: fixed; top: 0; left: 0;
      width: 100%; height: 100%;
      background: linear-gradient(135deg, #1a0a00, #2d1200);
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      z-index: 100; color: #D2691E;
    }}
    #loading-title {{
      font-size: 2.2em; font-weight: bold;
      color: #F4A460; text-align: center;
      text-shadow: 0 0 20px #C1440E;
      margin-bottom: 20px;
      letter-spacing: 3px;
    }}
    #loading-subtitle {{
      font-size: 1em; color: #8B4513;
      margin-bottom: 40px; text-align: center;
    }}
    #progress-bar-container {{
      width: 280px; height: 4px;
      background: #3a2010; border-radius: 2px;
    }}
    #progress-bar {{
      height: 100%; width: 0%;
      background: linear-gradient(90deg, #C1440E, #F4A460);
      border-radius: 2px;
      transition: width 0.3s ease;
    }}
    #loading-percent {{
      margin-top: 10px; font-size: 0.85em; color: #8B4513;
    }}

    /* Interface principale */
    #ui-overlay {{
      position: fixed; top: 0; left: 0;
      width: 100%; height: 100%;
      pointer-events: none; z-index: 10;
    }}

    /* Panneau d'info */
    #info-panel {{
      position: fixed; bottom: 0; left: 0; right: 0;
      background: linear-gradient(0deg, rgba(10,5,0,0.95) 0%, rgba(10,5,0,0.7) 80%, transparent 100%);
      padding: 30px 24px 24px;
      transform: translateY(100%);
      transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
      color: #F4A460;
    }}
    #info-panel.visible {{ transform: translateY(0); }}
    #info-panel h2 {{
      font-size: 1.4em; color: #F4A460;
      margin-bottom: 8px; letter-spacing: 1px;
    }}
    #info-panel p {{
      font-size: 0.9em; color: #D2691E;
      line-height: 1.6; margin-bottom: 12px;
    }}
    #info-close {{
      position: absolute; top: 16px; right: 16px;
      background: none; border: 1px solid #8B4513;
      color: #F4A460; width: 32px; height: 32px;
      border-radius: 50%; cursor: pointer; font-size: 1.1em;
      pointer-events: all;
    }}

    /* Boutons de controle */
    #controls {{
      position: fixed; bottom: 30px; right: 20px;
      display: flex; flex-direction: column; gap: 12px;
      pointer-events: all;
    }}
    .ctrl-btn {{
      width: 48px; height: 48px;
      background: rgba(193, 68, 14, 0.85);
      border: none; border-radius: 50%;
      color: #FFF8DC; font-size: 1.3em;
      cursor: pointer; display: flex;
      align-items: center; justify-content: center;
      box-shadow: 0 4px 15px rgba(193, 68, 14, 0.4);
      transition: transform 0.2s, background 0.2s;
      backdrop-filter: blur(4px);
    }}
    .ctrl-btn:hover {{ transform: scale(1.1); background: rgba(244, 164, 96, 0.9); }}
    .ctrl-btn:active {{ transform: scale(0.95); }}

    /* Badge UNESCO */
    #badge-unesco {{
      position: fixed; top: 20px; left: 20px;
      background: rgba(10, 5, 0, 0.8);
      border: 1px solid #8B4513;
      border-radius: 8px; padding: 8px 14px;
      color: #F4A460; font-size: 0.75em;
      letter-spacing: 1px; text-transform: uppercase;
      backdrop-filter: blur(4px);
      opacity: 0; transition: opacity 1s ease;
      pointer-events: none;
    }}
    #badge-unesco.visible {{ opacity: 1; }}

    /* Texte de scene */
    #scene-text {{
      position: fixed; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      color: #F4A460; text-align: center;
      font-size: 1.6em; font-weight: bold;
      text-shadow: 0 0 30px #C1440E, 0 0 60px #8B4513;
      opacity: 0; transition: opacity 0.8s ease;
      pointer-events: none; letter-spacing: 2px;
      max-width: 80%;
    }}

    /* Annotation 3D */
    .annotation {{
      position: absolute;
      background: rgba(193, 68, 14, 0.85);
      color: #FFF8DC; font-size: 0.75em;
      padding: 5px 10px; border-radius: 4px;
      pointer-events: none; white-space: nowrap;
      border-left: 3px solid #F4A460;
      backdrop-filter: blur(4px);
      opacity: 0; transition: opacity 0.5s;
    }}
    .annotation.visible {{ opacity: 1; }}
    .annotation::before {{
      content: ''; position: absolute;
      left: -8px; top: 50%; transform: translateY(-50%);
      width: 0; height: 0;
      border-top: 5px solid transparent;
      border-bottom: 5px solid transparent;
      border-right: 8px solid rgba(193, 68, 14, 0.85);
    }}
  </style>
</head>
<body>

<div id="loading-screen">
  <div id="loading-title">LA TAKIENTA</div>
  <div id="loading-subtitle">Koutammakou · Patrimoine UNESCO · Togo</div>
  <div id="progress-bar-container">
    <div id="progress-bar"></div>
  </div>
  <div id="loading-percent">Chargement...</div>
</div>

<div id="canvas-container"></div>

<div id="ui-overlay">
  <div id="badge-unesco">Patrimoine UNESCO 2004</div>
  <div id="scene-text"></div>
</div>

<div id="info-panel">
  <button id="info-close" onclick="fermerInfo()">×</button>
  <h2 id="info-titre">La Takienta</h2>
  <p id="info-contenu">Architecture ancestrale du peuple Batammariba.</p>
  <p style="font-size:0.8em; color:#8B4513; margin-top:8px;">
    Le Koutammakou est inscrit au Patrimoine Mondial de l'UNESCO depuis 2004.
    Ces tours en terre crue sont a la fois habitations, greniers et lieux de culte.
  </p>
</div>

<div id="controls">
  <button class="ctrl-btn" onclick="toggleRotation()" title="Rotation auto">↻</button>
  <button class="ctrl-btn" onclick="resetCamera()" title="Reinitialiser vue">⌂</button>
  <button class="ctrl-btn" onclick="afficherInfo()" title="Informations">ℹ</button>
</div>

<!-- Three.js depuis CDN -->
<script type="importmap">
{{
  "imports": {{
    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
  }}
}}
</script>

<script type="module">
import * as THREE from 'three';
import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
import {{ GLTFLoader }} from 'three/addons/loaders/GLTFLoader.js';
import {{ DRACOLoader }} from 'three/addons/loaders/DRACOLoader.js';
import {{ Sky }} from 'three/addons/objects/Sky.js';
import {{ CSS2DRenderer, CSS2DObject }} from 'three/addons/renderers/CSS2DRenderer.js';

// ============================================================
// SCENE - Configuration principale
// ============================================================
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x1a0a00, 0.008);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(8, 4, 12);

const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.8;
document.getElementById('canvas-container').appendChild(renderer.domElement);

// Renderer CSS2D pour les annotations
const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(window.innerWidth, window.innerHeight);
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0';
labelRenderer.domElement.style.pointerEvents = 'none';
document.getElementById('canvas-container').appendChild(labelRenderer.domElement);

// ============================================================
// CONTROLES
// ============================================================
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 3;
controls.maxDistance = 30;
controls.maxPolarAngle = Math.PI * 0.85;
controls.target.set(0, 2, 0);

let autoRotate = true;
controls.autoRotate = autoRotate;
controls.autoRotateSpeed = 0.4;

// ============================================================
// CIEL - Atmosphere africaine
// ============================================================
const sky = new Sky();
sky.scale.setScalar(450000);
scene.add(sky);

const skyUniforms = sky.material.uniforms;
skyUniforms['turbidity'].value = 8;
skyUniforms['rayleigh'].value = 1.5;
skyUniforms['mieCoefficient'].value = 0.005;
skyUniforms['mieDirectionalG'].value = 0.82;

const sun = new THREE.Vector3();
const phi = THREE.MathUtils.degToRad(75);
const theta = THREE.MathUtils.degToRad(210);
sun.setFromSphericalCoords(1, phi, theta);
skyUniforms['sunPosition'].value.copy(sun);

// ============================================================
// LUMIÈRES
// ============================================================
const ambientLight = new THREE.AmbientLight(0x8B4513, 0.4);
scene.add(ambientLight);

const sunLight = new THREE.DirectionalLight(0xFFD89B, 1.2);
sunLight.position.set(10, 20, 5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 100;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
scene.add(sunLight);

// Lumiere de remplissage chaude
const fillLight = new THREE.DirectionalLight(0xFF6B35, 0.3);
fillLight.position.set(-5, 3, -5);
scene.add(fillLight);

// ============================================================
// SOL - Terre africaine
// ============================================================
const groundGeo = new THREE.PlaneGeometry(60, 60, 20, 20);
const groundMat = new THREE.MeshStandardMaterial({{
  color: 0x8B6914,
  roughness: 0.95,
  metalness: 0.0
}});
// Deformation legere du sol pour le naturalisme
const posAttr = groundGeo.attributes.position;
for (let i = 0; i < posAttr.count; i++) {{
  posAttr.setZ(i, (Math.random() - 0.5) * 0.15);
}}
groundGeo.computeVertexNormals();
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Herbes seches - instances
const grassGeo = new THREE.ConeGeometry(0.02, 0.3, 3);
const grassMat = new THREE.MeshStandardMaterial({{ color: 0x8B7355, roughness: 1 }});
const grassCount = 300;
const grassMesh = new THREE.InstancedMesh(grassGeo, grassMat, grassCount);
const dummy = new THREE.Object3D();
for (let i = 0; i < grassCount; i++) {{
  const x = (Math.random() - 0.5) * 40;
  const z = (Math.random() - 0.5) * 40;
  if (Math.abs(x) > 4 || Math.abs(z) > 4) {{
    dummy.position.set(x, 0.15, z);
    dummy.rotation.x = (Math.random() - 0.5) * 0.3;
    dummy.rotation.z = (Math.random() - 0.5) * 0.3;
    dummy.updateMatrix();
    grassMesh.setMatrixAt(i, dummy.matrix);
  }}
}}
scene.add(grassMesh);

// ============================================================
// MODELE 3D - Chargement avec DRACO
// ============================================================
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

let modele = null;
let annotationsVisibles = false;

function majChargement(pct, msg) {{
  document.getElementById('progress-bar').style.width = pct + '%';
  document.getElementById('loading-percent').textContent = msg;
}}

majChargement(10, 'Preparation de la scene...');

// Simuler un chargement progressif pendant l'init
setTimeout(() => majChargement(30, 'Chargement du terrain...'), 300);
setTimeout(() => majChargement(60, 'Chargement du modele 3D...'), 800);

gltfLoader.load(
  '{glb_path}',
  (gltf) => {{
    modele = gltf.scene;

    // Centrer et positionner le modele
    const box = new THREE.Box3().setFromObject(modele);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const scale = 5 / maxDim;

    modele.scale.setScalar(scale);
    modele.position.set(-center.x * scale, -box.min.y * scale, -center.z * scale);

    // Ombres et materiaux
    modele.traverse(child => {{
      if (child.isMesh) {{
        child.castShadow = true;
        child.receiveShadow = true;
        if (child.material) {{
          child.material.roughness = Math.max(child.material.roughness || 0.8, 0.7);
        }}
      }}
    }});

    // Animation d'apparition : le modele emerge du sol
    modele.position.y -= 8;
    scene.add(modele);

    majChargement(90, 'Finalisation...');

    // Animation d'emergence
    let emerging = true;
    let targetY = modele.position.y + 8;
    let emergenceSpeed = 0.05;

    function emergence() {{
      if (emerging) {{
        modele.position.y += emergenceSpeed;
        emergenceSpeed = Math.min(emergenceSpeed * 1.02, 0.15);
        if (modele.position.y >= targetY) {{
          modele.position.y = targetY;
          emerging = false;
          afficherSceneTexte("Koutammakou", 3000);
          setTimeout(() => {{
            document.getElementById('badge-unesco').classList.add('visible');
            creerAnnotations();
          }}, 4000);
        }}
        requestAnimationFrame(emergence);
      }}
    }}

    setTimeout(() => {{
      majChargement(100, 'Pret !');
      masquerEcranChargement();
      emergence();
    }}, 500);
  }},
  (xhr) => {{
    if (xhr.total > 0) {{
      const pct = 60 + (xhr.loaded / xhr.total) * 30;
      majChargement(Math.round(pct), `Modele : ${{Math.round(pct - 60) * 3}}%`);
    }}
  }},
  (error) => {{
    console.warn('Modele GLB non trouve - affichage placeholder');
    majChargement(100, 'Pret !');
    masquerEcranChargement();
    creerPlaceholder();
    setTimeout(() => {{
      afficherSceneTexte("Koutammakou", 3000);
      document.getElementById('badge-unesco').classList.add('visible');
      creerAnnotations();
    }}, 2000);
  }}
);

// ============================================================
// PLACEHOLDER - Si pas de modele GLB disponible
// ============================================================
function creerPlaceholder() {{
  const group = new THREE.Group();

  // Base cylindrique (mur de la tour)
  const murGeo = new THREE.CylinderGeometry(1.2, 1.4, 4, 16);
  const murMat = new THREE.MeshStandardMaterial({{
    color: 0xC1440E, roughness: 0.9, metalness: 0
  }});
  const mur = new THREE.Mesh(murGeo, murMat);
  mur.position.y = 2;
  mur.castShadow = true;
  group.add(mur);

  // Toit conique en chaume
  const toitGeo = new THREE.ConeGeometry(1.6, 2, 16);
  const toitMat = new THREE.MeshStandardMaterial({{
    color: 0x8B7355, roughness: 1
  }});
  const toit = new THREE.Mesh(toitGeo, toitMat);
  toit.position.y = 5;
  toit.castShadow = true;
  group.add(toit);

  // Porte
  const porteGeo = new THREE.BoxGeometry(0.4, 0.8, 0.1);
  const porteMat = new THREE.MeshStandardMaterial({{ color: 0x3D1C02 }});
  const porte = new THREE.Mesh(porteGeo, porteMat);
  porte.position.set(0, 0.4, 1.35);
  group.add(porte);

  // Tours secondaires
  for (let i = 0; i < 3; i++) {{
    const angle = (i / 3) * Math.PI * 2 + Math.PI / 6;
    const dist = 4.5;
    const tg = new THREE.Group();

    const m = new THREE.Mesh(
      new THREE.CylinderGeometry(0.7, 0.85, 3, 12),
      murMat
    );
    m.position.y = 1.5;
    m.castShadow = true;
    tg.add(m);

    const t = new THREE.Mesh(
      new THREE.ConeGeometry(0.95, 1.5, 12),
      toitMat
    );
    t.position.y = 3.75;
    t.castShadow = true;
    tg.add(t);

    tg.position.set(Math.cos(angle) * dist, 0, Math.sin(angle) * dist);
    group.add(tg);
  }}

  modele = group;
  scene.add(group);
}}

// ============================================================
// ANNOTATIONS
// ============================================================
const annotationsData = [
  {{ nom: "Grenier", pos: new THREE.Vector3(0, 4.5, 0), info: "Stockage du mil et des semences. Protege par les ancetres." }},
  {{ nom: "Autel", pos: new THREE.Vector3(1.3, 0.8, 0), info: "Lieu de communication avec les esprits ancestraux." }},
  {{ nom: "Terrasse", pos: new THREE.Vector3(0, 3.2, 1.5), info: "Espace de vie et de surveillance. Vue a 360 degres." }},
  {{ nom: "Tour principale", pos: new THREE.Vector3(0, 6, 0), info: "Toit conique en chaume. Renouvelé tous les 3 ans en communauté." }}
];

function creerAnnotations() {{
  annotationsData.forEach(data => {{
    const div = document.createElement('div');
    div.className = 'annotation';
    div.textContent = data.nom;
    div.addEventListener('pointerdown', () => {{
      document.getElementById('info-titre').textContent = data.nom;
      document.getElementById('info-contenu').textContent = data.info;
      document.getElementById('info-panel').classList.add('visible');
    }});

    const label = new CSS2DObject(div);
    label.position.copy(data.pos);
    scene.add(label);

    setTimeout(() => div.classList.add('visible'), 500);
  }});
  annotationsVisibles = true;
}}

// ============================================================
// PARTICULES - Poussiere du Sahel
// ============================================================
const particleGeo = new THREE.BufferGeometry();
const particleCount = 500;
const positions = new Float32Array(particleCount * 3);
for (let i = 0; i < particleCount; i++) {{
  positions[i * 3] = (Math.random() - 0.5) * 30;
  positions[i * 3 + 1] = Math.random() * 10;
  positions[i * 3 + 2] = (Math.random() - 0.5) * 30;
}}
particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
const particleMat = new THREE.PointsMaterial({{
  color: 0xD2691E, size: 0.06, transparent: true, opacity: 0.4
}});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);

// ============================================================
// ANIMATION PRINCIPALE
// ============================================================
const clock = new THREE.Clock();

function animate() {{
  requestAnimationFrame(animate);
  const elapsed = clock.getElapsedTime();

  controls.update();

  // Animation des particules (vent)
  const pPos = particles.geometry.attributes.position;
  for (let i = 0; i < particleCount; i++) {{
    pPos.setX(i, pPos.getX(i) + 0.003);
    pPos.setY(i, pPos.getY(i) + Math.sin(elapsed + i) * 0.001);
    if (pPos.getX(i) > 15) pPos.setX(i, -15);
  }}
  pPos.needsUpdate = true;

  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);
}}

animate();

// ============================================================
// FONCTIONS UI
// ============================================================
window.toggleRotation = function() {{
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
}};

window.resetCamera = function() {{
  camera.position.set(8, 4, 12);
  controls.target.set(0, 2, 0);
  controls.update();
}};

window.afficherInfo = function() {{
  document.getElementById('info-titre').textContent = 'La Takienta';
  document.getElementById('info-contenu').textContent = 'Les tours Takienta sont les maisons-fortresses du peuple Batammariba au nord-est du Togo. Chaque tour symbolise l\'univers : le niveau bas pour les animaux, le niveau moyen pour les vivants, le toit pour les ancetres.';
  document.getElementById('info-panel').classList.add('visible');
}};

window.fermerInfo = function() {{
  document.getElementById('info-panel').classList.remove('visible');
}};

function afficherSceneTexte(texte, duree) {{
  const el = document.getElementById('scene-text');
  el.textContent = texte;
  el.style.opacity = '1';
  setTimeout(() => {{ el.style.opacity = '0'; }}, duree);
}}

function masquerEcranChargement() {{
  const screen = document.getElementById('loading-screen');
  screen.style.transition = 'opacity 1s ease';
  screen.style.opacity = '0';
  setTimeout(() => {{ screen.style.display = 'none'; }}, 1000);
}}

// ============================================================
// RESPONSIVE
// ============================================================
window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  labelRenderer.setSize(window.innerWidth, window.innerHeight);
}});

</script>
</body>
</html>"""

    return html

def run(nom_projet, prompt_storyboard=None, glb_path=None):
    """Point d'entree principal de l'agent"""
    print(f"\n{'='*50}")
    print(f"AGENT CODE - Projet : {nom_projet}")
    print(f"{'='*50}")

    nom_fichier = nom_projet.lower().replace(" ", "-")
    dossier_sortie = os.path.join(
        "C:/Users/Kabakoo Apprenant.e/Desktop/MES PROJETS",
        "projets-generes",
        nom_fichier
    )
    os.makedirs(dossier_sortie, exist_ok=True)
    os.makedirs(os.path.join(dossier_sortie, "assets"), exist_ok=True)

    # Generer le HTML
    html = generer_experience_takienta(nom_projet, glb_path)
    chemin_html = os.path.join(dossier_sortie, "index.html")

    with open(chemin_html, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n[Agent Code] TERMINE")
    print(f"Fichier HTML genere : {chemin_html}")
    print(f"Taille : {len(html)} caracteres")
    print(f"\n[INSTRUCTION] Pour tester localement :")
    print(f"  Ouvre le fichier dans un navigateur ou lance un serveur local")
    print(f"  Depose ton fichier GLB dans : {dossier_sortie}/assets/{nom_fichier}.glb")

    return {
        "status": "ok",
        "chemin_html": chemin_html,
        "dossier": dossier_sortie
    }

if __name__ == "__main__":
    run("La Takienta")
