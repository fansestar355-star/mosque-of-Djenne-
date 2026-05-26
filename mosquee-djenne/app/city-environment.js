import * as THREE from 'three';

// ─────────────────────────────────────────────────────────────
//  DJENNÉ HOLOGRAPHIC CITY MAQUETTE
//  Dense organic adobe city on a circular platform
//  Built around the existing mosque GLB.
// ─────────────────────────────────────────────────────────────

let _s = 42;
function rng() { _s = (_s * 16807) % 2147483647; return (_s - 1) / 2147483646; }

// ── Earth colour palette ─────────────────────────────────────
const C = [
  0xb86f2a, 0xa05c1e, 0xc47d35, 0x8c4e15, 0xbf7530,
  0x9e6025, 0xd08840, 0x7a4010, 0xb0692a, 0xc98038,
  0x6e3a0e, 0xa86825, 0xc08050, 0x945520, 0xb87838,
];

function pickColor() { return C[Math.floor(rng() * C.length)]; }

function mat(hex) {
  return new THREE.MeshLambertMaterial({ color: hex, flatShading: false });
}

// ─────────────────────────────────────────────────────────────
//  BUILDING FACTORY
// ─────────────────────────────────────────────────────────────
function makeBuilding(w, h, d, color, detailed) {
  const g = new THREE.Group();

  // main body
  const geo = new THREE.BoxGeometry(w, h, d);
  // organic vertex jitter on top edges
  if (detailed) {
    const p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) {
      if (p.getY(i) > 0) {
        p.setX(i, p.getX(i) + (rng() - 0.5) * w * 0.08);
        p.setZ(i, p.getZ(i) + (rng() - 0.5) * d * 0.08);
        p.setY(i, p.getY(i) + (rng() - 0.5) * h * 0.06);
      }
    }
    p.needsUpdate = true;
    geo.computeVertexNormals();
  }

  const darkC = new THREE.Color(color).multiplyScalar(0.85 + rng() * 0.2);
  const body = new THREE.Mesh(geo, mat(darkC.getHex()));
  body.position.y = h * 0.5;
  body.castShadow = true;
  body.receiveShadow = true;
  g.add(body);

  // parapet rim (random)
  if (detailed && rng() > 0.5) {
    const rimH = h * 0.08;
    const rimGeo = new THREE.BoxGeometry(w * 1.04, rimH, d * 1.04);
    const rc = new THREE.Color(color).multiplyScalar(0.75);
    const rim = new THREE.Mesh(rimGeo, mat(rc.getHex()));
    rim.position.y = h + rimH * 0.5;
    rim.castShadow = true;
    g.add(rim);
  }

  // toron poles
  if (detailed && rng() > 0.65) {
    const tMat = mat(0x5a3510);
    const count = 2 + Math.floor(rng() * 3);
    for (let k = 0; k < count; k++) {
      const tLen = w * 0.2;
      const tg = new THREE.CylinderGeometry(0.02, 0.015, tLen, 3);
      const tm = new THREE.Mesh(tg, tMat);
      const s = rng() > 0.5 ? 1 : -1;
      tm.position.set(s * (w * 0.5 + tLen * 0.3), h * (0.3 + rng() * 0.4), (rng() - 0.5) * d * 0.5);
      tm.rotation.z = Math.PI * 0.5;
      tm.castShadow = true;
      g.add(tm);
    }
  }

  // annex
  if (detailed && rng() > 0.7) {
    const aw = w * (0.3 + rng() * 0.35);
    const ah = h * (0.35 + rng() * 0.4);
    const ad = d * (0.3 + rng() * 0.4);
    const ac = new THREE.Color(color).multiplyScalar(0.9 + rng() * 0.15);
    const am = new THREE.Mesh(new THREE.BoxGeometry(aw, ah, ad), mat(ac.getHex()));
    am.position.set((rng() > 0.5 ? 1 : -1) * (w * 0.5 + aw * 0.4), ah * 0.5, (rng() - 0.5) * d * 0.3);
    am.castShadow = true;
    am.receiveShadow = true;
    g.add(am);
  }

  return g;
}

// ─────────────────────────────────────────────────────────────
//  TREE — small low-poly sahelian tree
// ─────────────────────────────────────────────────────────────
function makeTree(scale) {
  const g = new THREE.Group();
  const trunkH = 0.3 * scale;
  const trunk = new THREE.Mesh(
    new THREE.CylinderGeometry(0.03 * scale, 0.04 * scale, trunkH, 4),
    mat(0x6b4420)
  );
  trunk.position.y = trunkH * 0.5;
  trunk.castShadow = true;
  g.add(trunk);

  // foliage — irregular spheroid
  const foliage = new THREE.Mesh(
    new THREE.IcosahedronGeometry(0.2 * scale, 0),
    new THREE.MeshLambertMaterial({ color: 0x4a7a28, flatShading: true })
  );
  foliage.position.y = trunkH + 0.12 * scale;
  foliage.scale.set(1 + rng() * 0.3, 0.7 + rng() * 0.3, 1 + rng() * 0.3);
  foliage.castShadow = true;
  g.add(foliage);
  return g;
}

// ─────────────────────────────────────────────────────────────
//  ORGANIC STREET MASK — determines where streets go
//  Returns a function: isStreet(x, z) → boolean
// ─────────────────────────────────────────────────────────────
function buildStreetMask(platformR) {
  // Build organic winding street paths as polylines
  const streets = [];
  const branchCount = 7;

  // Main radial arteries
  for (let i = 0; i < branchCount; i++) {
    const baseAngle = (i / branchCount) * Math.PI * 2 + (rng() - 0.5) * 0.4;
    const points = [];
    let angle = baseAngle;
    let r = platformR * 0.05;
    while (r < platformR * 0.92) {
      points.push({ x: Math.cos(angle) * r, z: Math.sin(angle) * r });
      angle += (rng() - 0.48) * 0.3;
      r += platformR * 0.06 + rng() * platformR * 0.04;
    }
    streets.push({ points, width: platformR * 0.045 });
  }

  // Secondary ring connections
  for (let ring = 0; ring < 3; ring++) {
    const ringR = platformR * (0.25 + ring * 0.22);
    const pts = [];
    for (let a = 0; a < Math.PI * 2; a += 0.15 + rng() * 0.1) {
      const ja = a + (rng() - 0.5) * 0.08;
      const jr = ringR + (rng() - 0.5) * platformR * 0.08;
      pts.push({ x: Math.cos(ja) * jr, z: Math.sin(ja) * jr });
    }
    streets.push({ points: pts, width: platformR * 0.03 });
  }

  // Test if a point is near any street
  return function isStreet(px, pz) {
    for (const st of streets) {
      for (let i = 0; i < st.points.length - 1; i++) {
        const a = st.points[i], b = st.points[i + 1];
        // distance from point to segment
        const dx = b.x - a.x, dz = b.z - a.z;
        const len2 = dx * dx + dz * dz;
        if (len2 < 0.001) continue;
        let t = ((px - a.x) * dx + (pz - a.z) * dz) / len2;
        t = Math.max(0, Math.min(1, t));
        const cx = a.x + t * dx, cz = a.z + t * dz;
        const dist = Math.sqrt((px - cx) ** 2 + (pz - cz) ** 2);
        if (dist < st.width) return true;
      }
    }
    return false;
  };
}

// ─────────────────────────────────────────────────────────────
//  HOLOGRAPHIC PLATFORM — circular disc with glow edge
// ─────────────────────────────────────────────────────────────
function makePlatform(radius) {
  const g = new THREE.Group();
  g.name = 'HoloPlatform';

  // main disc — dark sandy earth
  const discGeo = new THREE.CylinderGeometry(radius, radius * 1.02, 0.15, 96);
  const discMat = new THREE.MeshStandardMaterial({
    color: 0xc49a5a,
    roughness: 0.95,
    metalness: 0,
    flatShading: false,
  });
  const disc = new THREE.Mesh(discGeo, discMat);
  disc.position.y = -0.075;
  disc.receiveShadow = true;
  g.add(disc);

  // edge glow ring
  const edgeGeo = new THREE.TorusGeometry(radius, 0.05, 8, 128);
  const edgeMat = new THREE.MeshBasicMaterial({
    color: 0x55ccee,
    transparent: true,
    opacity: 0.35,
  });
  const edge = new THREE.Mesh(edgeGeo, edgeMat);
  edge.rotation.x = Math.PI * 0.5;
  edge.position.y = 0.0;
  edge.name = 'PlatformEdge';
  g.add(edge);

  // outer glow ring
  const outerGeo = new THREE.TorusGeometry(radius * 1.03, 0.03, 8, 128);
  const outerMat = new THREE.MeshBasicMaterial({
    color: 0x55ccee,
    transparent: true,
    opacity: 0.15,
  });
  const outer = new THREE.Mesh(outerGeo, outerMat);
  outer.rotation.x = Math.PI * 0.5;
  outer.position.y = 0.0;
  g.add(outer);

  // scan rings at zone boundaries
  [0.3, 0.55, 0.8].forEach((frac, i) => {
    const rr = radius * frac;
    const ringGeo = new THREE.TorusGeometry(rr, 0.02, 6, 96);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0xf9d58b,
      transparent: true,
      opacity: 0.08 - i * 0.02,
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = Math.PI * 0.5;
    ring.position.y = 0.02;
    ring.name = `ScanRing_${i}`;
    g.add(ring);
  });

  return g;
}

// ─────────────────────────────────────────────────────────────
//  DUST PARTICLES
// ─────────────────────────────────────────────────────────────
function addDust(parent, spread, maxH) {
  const N = 400;
  const pos = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    const a = rng() * Math.PI * 2;
    const r = rng() * spread;
    pos[i * 3]     = Math.cos(a) * r;
    pos[i * 3 + 1] = rng() * maxH * 2;
    pos[i * 3 + 2] = Math.sin(a) * r;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  parent.add(new THREE.Points(geo, new THREE.PointsMaterial({
    color: 0xd4aa70, size: 0.08, transparent: true,
    opacity: 0.2, sizeAttenuation: true, depthWrite: false,
  })));
  parent.userData._dustGeo = geo;
  parent.userData._dustN = N;
  parent.userData._dustH = maxH;
}

// ─────────────────────────────────────────────────────────────
//  MAIN EXPORT
// ─────────────────────────────────────────────────────────────
export function buildCityEnvironment(scene, mosqueSize) {
  _s = 42;

  const city = new THREE.Group();
  city.name = 'DjenneCity';

  const mW = mosqueSize.x;
  const mD = mosqueSize.z;
  const mH = mosqueSize.y;
  const mR = Math.max(mW, mD) * 0.5;

  // Platform radius — mosque takes up the center ~25% area
  const platformR = mR * 4.5;

  // ── Holographic platform ──────────────────────────────────
  const platform = makePlatform(platformR);
  city.add(platform);

  // ── Street mask ───────────────────────────────────────────
  const isStreet = buildStreetMask(platformR);

  // ── Dense building grid with organic jitter ───────────────
  // Cell size — buildings are packed tight
  const cellSize = mR * 0.35;

  // Mosque bounding rectangle (with margin)
  const mosqueMargin = 1.15;
  const mHalfW = mW * 0.5 * mosqueMargin;
  const mHalfD = mD * 0.5 * mosqueMargin;

  const gridExtent = platformR * 0.92;
  const buildingUnit = mR * 0.12; // base unit for building sizing

  let buildingCount = 0;

  for (let gx = -gridExtent; gx < gridExtent; gx += cellSize) {
    for (let gz = -gridExtent; gz < gridExtent; gz += cellSize) {
      // organic jitter
      const px = gx + (rng() - 0.5) * cellSize * 0.7;
      const pz = gz + (rng() - 0.5) * cellSize * 0.7;

      // skip outside platform circle
      const dist = Math.sqrt(px * px + pz * pz);
      if (dist > platformR * 0.9) continue;

      // skip inside mosque footprint
      if (Math.abs(px) < mHalfW && Math.abs(pz) < mHalfD) continue;

      // skip on streets
      if (isStreet(px, pz)) continue;

      // random skip for density variation (sparser at edges)
      const edgeFactor = dist / platformR;
      if (rng() < edgeFactor * 0.15) continue;

      // ── Determine zone ────────────────────────────────────
      const zone = dist < mR * 1.8 ? 1 : dist < mR * 3.2 ? 2 : 3;
      const detailed = zone === 1;

      // ── Building dimensions ───────────────────────────────
      // Height decreases with distance, increases near mosque
      const proximityBoost = Math.max(0, 1 - (dist - mR) / (platformR * 0.5));
      const baseH = buildingUnit * (2.5 + rng() * 3.5) * (0.5 + proximityBoost * 0.8);
      const w = cellSize * (0.5 + rng() * 0.4);
      const d = cellSize * (0.5 + rng() * 0.4);
      const h = Math.max(buildingUnit * 1.5, baseH);

      const color = pickColor();
      const bldg = makeBuilding(w, h, d, color, detailed);
      bldg.position.set(px, 0, pz);
      bldg.rotation.y = rng() * Math.PI * 2;

      // slight age tilt
      if (detailed) {
        bldg.rotation.x = (rng() - 0.5) * 0.02;
        bldg.rotation.z = (rng() - 0.5) * 0.02;
      }

      city.add(bldg);
      buildingCount++;
    }
  }

  console.log(`[DjenneCity] Placed ${buildingCount} buildings, platformR=${platformR.toFixed(1)}, mR=${mR.toFixed(1)}`);

  // ── Trees — scattered in streets and open spaces ──────────
  const treeCount = Math.floor(buildingCount * 0.06);
  for (let i = 0; i < treeCount; i++) {
    const angle = rng() * Math.PI * 2;
    const r = mR * 1.3 + rng() * (platformR * 0.75);
    const tx = Math.cos(angle) * r;
    const tz = Math.sin(angle) * r;

    // only place on streets or near streets
    if (!isStreet(tx, tz) && rng() > 0.3) continue;
    // not inside mosque
    if (Math.abs(tx) < mHalfW && Math.abs(tz) < mHalfD) continue;

    const tree = makeTree(buildingUnit * (1.5 + rng() * 2));
    tree.position.set(tx, 0, tz);
    city.add(tree);
  }

  // ── Atmospheric dust ──────────────────────────────────────
  addDust(city, platformR * 0.85, mH * 1.5);

  // ── Atmospheric fog ───────────────────────────────────────
  scene.fog = new THREE.FogExp2(0xd4b07a, 0.015 / mR);

  scene.add(city);
  return city;
}

// ─────────────────────────────────────────────────────────────
//  ANIMATION TICK
// ─────────────────────────────────────────────────────────────
export function tickCityEnvironment(city, t) {
  if (!city) return;

  // drift dust
  const geo = city.userData._dustGeo;
  const N   = city.userData._dustN;
  const maxH = city.userData._dustH;
  if (geo && N) {
    const p = geo.attributes.position.array;
    for (let i = 0; i < N; i++) {
      p[i * 3]     += Math.sin(t * 0.12 + i) * 0.003;
      p[i * 3 + 2] += Math.cos(t * 0.10 + i * 0.7) * 0.002;
      p[i * 3 + 1] += 0.002;
      if (p[i * 3 + 1] > maxH * 3) p[i * 3 + 1] = 0;
    }
    geo.attributes.position.needsUpdate = true;
  }

  // pulse platform edge & scan rings
  city.traverse(child => {
    if (child.name === 'PlatformEdge' && child.material) {
      child.material.opacity = 0.3 + Math.sin(t * 0.8) * 0.1;
    }
    if (child.name && child.name.startsWith('ScanRing_') && child.material) {
      const idx = parseInt(child.name.split('_')[1], 10);
      child.material.opacity = (0.06 - idx * 0.015) + Math.sin(t * 0.5 + idx * 1.3) * 0.03;
    }
  });
}
