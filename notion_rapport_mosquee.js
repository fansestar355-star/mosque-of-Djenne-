// Rapport Notion — Mosquée de Djenné (session complète)
// Envoie le rapport dans la base "Journal de bord : 3 prochains mois"

const TOKEN = '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';
const DATABASE_ID = '65073e08-97ca-4c60-9cf2-da1078736240';

const today = new Date().toISOString().slice(0, 10);

// Helpers
const rt = (text, opts = {}) => ({
  type: 'text',
  text: { content: text },
  annotations: opts,
});
const h1 = (t) => ({ object: 'block', type: 'heading_1', heading_1: { rich_text: [rt(t)] } });
const h2 = (t) => ({ object: 'block', type: 'heading_2', heading_2: { rich_text: [rt(t)] } });
const h3 = (t) => ({ object: 'block', type: 'heading_3', heading_3: { rich_text: [rt(t)] } });
const p = (t) => ({ object: 'block', type: 'paragraph', paragraph: { rich_text: typeof t === 'string' ? [rt(t)] : t } });
const bullet = (t) => ({ object: 'block', type: 'bulleted_list_item', bulleted_list_item: { rich_text: typeof t === 'string' ? [rt(t)] : t } });
const todo = (t, done = false) => ({ object: 'block', type: 'to_do', to_do: { rich_text: [rt(t)], checked: done } });
const code = (t, lang = 'plain text') => ({ object: 'block', type: 'code', code: { rich_text: [rt(t)], language: lang } });
const divider = () => ({ object: 'block', type: 'divider', divider: {} });
const callout = (t, emoji, color = 'blue_background') => ({
  object: 'block', type: 'callout',
  callout: { rich_text: [rt(t)], icon: { type: 'emoji', emoji }, color },
});
const quote = (t) => ({ object: 'block', type: 'quote', quote: { rich_text: [rt(t)] } });

const blocks = [
  callout('Rapport généré automatiquement par Claude Code le ' + today, '🤖'),

  h1('🕌 Mosquée de Djenné — Rapport de session'),
  p([
    rt('Expérience immersive 3D Three.js style ', { italic: false }),
    rt('Call of Duty', { italic: true }),
    rt(' : accueil → vidéo intro → vue 3D extérieure → transition porte → mode FPS intérieur.'),
  ]),
  p([
    rt('Style futuriste, palette ', {}),
    rt('#55415d', { code: true }), rt(' (accent) + ', {}),
    rt('#f9d58b', { code: true }), rt(' (or).', {}),
  ]),
  divider(),

  h2('🏗️ Architecture mise en place'),
  bullet('Renderer + canvas + boucle d\'animation partagés (un seul WebGLRenderer)'),
  bullet('Machine à états : welcome → video → exterior → transition → interior'),
  bullet('5 états : welcome-state, video-state, exterior-state, transition-state, interior-state'),
  bullet('Modules monde : mosque-parts.js, sky-clouds.js, djenne-houses.js'),
  bullet('UI : gear-menu (engrenage hexagonal), camera-tween (zoom doux)'),
  bullet('Contrôles : fps-controller (WASD/ZQSD + souris + joystick), mesh-collider (raycast capsule)'),
  bullet('Utils : responsive.js (mobile detection via matchMedia)'),
  divider(),

  h2('🎨 Design tableau d\'accueil — 7 itérations'),
  bullet('1. Carte glassmorphism simple'),
  bullet('2. Holographique plein écran (particules 3D + halo violet + grille Tron)'),
  bullet('3. Navy + Gold (Cinzel, icônes SVG, keycaps relief)'),
  bullet('4. Palette violet #55415D'),
  bullet('5. Cards éditoriales (médaillons circulaires, halos radial)'),
  bullet('6. Carrousel pleine largeur (auto-rotate, swipe, dots)'),
  bullet('7. Prisme 3D rotatif (triangulaire CSS, runes sélectrices, animation float) — version actuelle'),
  divider(),

  h2('🤖 Connexion Blender MCP'),
  bullet('Installation de l\'addon officiel ahujasid/blender-mcp'),
  bullet('Pont socket sur port 9876 — Blender ↔ Claude bidirectionnel'),
  bullet('Outils MCP natifs : get_scene_info, execute_blender_code, get_viewport_screenshot, etc.'),
  bullet('Mémoire sauvegardée : toujours utiliser le script officiel, jamais une version custom'),
  divider(),

  h2('🕌 Optimisation modèle mosquée'),
  h3('Avant → Après'),
  bullet('Taille GLB : 127 MB → 14.09 MB (-89%)'),
  bullet('Polygones : 2.4 M → 1.49 M (-38%)'),
  bullet('Textures : toutes réduites à 512²'),
  h3('Actions'),
  bullet('Analyse polys : Porte_Cour (1.1M) + Portes_Exterieures (762K) = 78% du modèle'),
  bullet('Test Collapse 10% → cassait visuel (transparence, traits étirés)'),
  bullet('Test Collapse 40% → mieux mais artefacts'),
  bullet('Planar 8° → préserve angles, -49% chacune sans casser'),
  bullet('17 meshes renommés en PascalCase (Mosquee_Base, Minarets, Porte_Cour, etc.)'),
  bullet('3 caméras placées dans Blender : Camera_Exterieur, Camera_Exterieur_Target, Camera_Interieur'),
  bullet('Export GLB : Draco niveau 6 + JPEG + caméras incluses'),
  divider(),

  h2('🚁 Drone (autre projet ajouté)'),
  bullet('Modèle Meshy.ai quadricoptère (3175 verts / 6351 polys)'),
  bullet('4 hélices Helice_FR/FL/BL/BR séparées'),
  bullet('Animation rotation Z : 6 tours/sec (360 RPM), interpolation linéaire, boucle parfaite'),
  bullet('Textures réduites de 16.91 MB → 4.92 MB → 1.35 MB (2048² → 1024² → 512²)'),
  bullet('Export GLB final : 0.20 MB (200 KB)'),
  bullet('✅ Hébergé sur GitHub'),
  bullet('⏳ Intégration Three.js en cours (interrompue)'),
  divider(),

  h2('☁️ Hébergement GitHub'),
  p([
    rt('Repo public : '),
    { type: 'text', text: { content: 'github.com/fansestar355-star/mosquee-djenne', link: { url: 'https://github.com/fansestar355-star/mosquee-djenne' } } },
  ]),
  p([
    rt('GitHub Pages : '),
    { type: 'text', text: { content: 'fansestar355-star.github.io/mosquee-djenne', link: { url: 'https://fansestar355-star.github.io/mosquee-djenne/' } } },
  ]),
  h3('Commits réalisés'),
  bullet('Initial commit (code + assets)'),
  bullet('Fix overlay loader qui bloquait le clic "Commencer"'),
  bullet('Refonte holographique welcome'),
  bullet('GLB optimisé 14 MB'),
  bullet('Drone GLB animé'),
  divider(),

  h2('🛠️ Outils créés (locaux, dans tools/)'),
  bullet('blender_mcp_addon.py — addon officiel Ahuja'),
  bullet('blender_cli.js, run_in_blender.js — clients socket'),
  bullet('30+ scripts Python d\'analyse / optimisation'),
  bullet('Captures viewport pour validation visuelle'),
  divider(),

  h2('⏭️ État actuel — à reprendre'),
  todo('Mosquée GLB optimisée 14 MB hébergée', true),
  todo('Drone GLB animé 0.2 MB hébergé', true),
  todo('Welcome panel design prism 3D', true),
  todo('Intégration drone dans Three.js (interrompue)'),
  todo('Adapter Three.js pour lire les caméras du GLB'),
  todo("Utiliser getObjectByName('Minarets') etc. dans mosque-parts.js"),
  todo('Tester l\'expérience complète (vidéo, transition, FPS) avec le nouveau GLB'),
  divider(),

  h2('🧠 Mémoires persistantes sauvegardées'),
  bullet('Projet mosquee-djenne — repo, palette, style futuriste'),
  bullet('Addon Blender MCP — utiliser exclusivement la version ahujasid'),
];

async function main() {
  const body = {
    parent: { database_id: DATABASE_ID },
    properties: {
      Name: { title: [rt('Rapport Mosquée de Djenné — ' + today)] },
      Date: { date: { start: today } },
    },
    children: blocks,
  };

  console.log(`Envoi de ${blocks.length} blocks...`);

  const res = await fetch('https://api.notion.com/v1/pages', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      'Notion-Version': '2022-06-28',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) {
    console.error('ERREUR Notion :', JSON.stringify(data, null, 2));
    process.exit(1);
  }
  console.log('✅ Page créée :', data.url);
}

main().catch((e) => { console.error(e); process.exit(1); });
