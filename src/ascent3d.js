// The ascent, in three dimensions: four floating low-poly islands, one per stream,
// each with a snow peak whose summit is PASS. Every file is a lantern-lit camp at
// the altitude its evidence has reached; cold files sit in fog; the next firing's
// file gets a beacon and a climber on the route. Loaded only when the section is near.
import * as THREE from './vendor/three.module.min.js';

const CAMP_H = { unworked: 0, working: .3, blocked: .3, panel: .52, held: .72 };
const STAGE_HEX = { held: 0xf0884a, panel: 0xd6d05a, working: 0x45c7b9, blocked: 0xe45a6a, unworked: 0x6a9cf2 };
const ISLAND_R = 3.7, PEAK_R = 2.35, PEAK_H = 5.6, RING = 8.4;

// Deterministic noise, so every visit sees the same islands.
const rng = seed => () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const hash = s => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);

// Low-poly: jitter shared vertices identically, unweld, then colour face by face.
function lowPoly(geo, amount, seed, colourOf) {
  const r = rng(seed), pos = geo.attributes.position, moved = new Map();
  for (let i = 0; i < pos.count; i++) {
    const k = `${pos.getX(i).toFixed(3)},${pos.getY(i).toFixed(3)},${pos.getZ(i).toFixed(3)}`;
    if (!moved.has(k)) moved.set(k, [(r() - .5) * amount, (r() - .5) * amount * .7, (r() - .5) * amount]);
    const [dx, dy, dz] = moved.get(k);
    pos.setXYZ(i, pos.getX(i) + dx, pos.getY(i) + dy, pos.getZ(i) + dz);
  }
  const g = geo.index ? geo.toNonIndexed() : geo;
  const p = g.attributes.position, col = new Float32Array(p.count * 3), c = new THREE.Color();
  for (let i = 0; i < p.count; i += 3) {
    const cy = (p.getY(i) + p.getY(i + 1) + p.getY(i + 2)) / 3;
    const cx = (p.getX(i) + p.getX(i + 1) + p.getX(i + 2)) / 3, cz = (p.getZ(i) + p.getZ(i + 1) + p.getZ(i + 2)) / 3;
    colourOf(c, cy, cx, cz, r);
    for (let k = 0; k < 3; k++) c.toArray(col, (i + k) * 3);
  }
  g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  g.computeVertexNormals();
  return g;
}
const flat = () => new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: .9, metalness: 0 });

// A soft round glow, drawn once and shared by every lantern.
function glowTexture() {
  const cv = document.createElement('canvas'); cv.width = cv.height = 64;
  const x = cv.getContext('2d'), g = x.createRadialGradient(32, 32, 0, 32, 32, 32);
  g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.25, 'rgba(255,255,255,.55)'); g.addColorStop(1, 'rgba(255,255,255,0)');
  x.fillStyle = g; x.fillRect(0, 0, 64, 64);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t;
}

function cloud(seed, scale, opacity = 1) {
  const r = rng(seed), g = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({ color: 0xe9eef3, flatShading: true, roughness: 1, transparent: opacity < 1, opacity, depthWrite: opacity > .9 });
  const n = 4 + Math.floor(r() * 3);
  for (let i = 0; i < n; i++) {
    const m = new THREE.Mesh(new THREE.IcosahedronGeometry(.5 + r() * .45, 0), mat);
    m.position.set((i - n / 2) * .55 + (r() - .5) * .3, (r() - .3) * .35, (r() - .5) * .5);
    m.scale.set(1, .7 + r() * .3, .9);
    g.add(m);
  }
  g.scale.setScalar(scale);
  return g;
}

export function mount(host, { streams, pick, onOpen, onTip, onUntip, reduced }) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  host.appendChild(renderer.domElement);
  renderer.domElement.setAttribute('aria-hidden', 'true');
  const labels = document.createElement('div'); labels.className = 'a3-labels'; host.appendChild(labels);

  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(0x0b1420, 38, 82);
  const camera = new THREE.PerspectiveCamera(34, 1, .1, 200);

  // Dusk light: a low warm sun, a cool sky, a faint rim from behind.
  scene.add(new THREE.HemisphereLight(0xa9c0e0, 0x2a2018, 1.15));
  const sun = new THREE.DirectionalLight(0xffd6a0, 2.6);
  sun.position.set(-16, 20, 10); sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  Object.assign(sun.shadow.camera, { left: -16, right: 16, top: 16, bottom: -16, near: 1, far: 70 });
  sun.shadow.bias = -.0008;
  scene.add(sun);
  const rim = new THREE.DirectionalLight(0x7fa6ff, .7); rim.position.set(14, 6, -16); scene.add(rim);

  const glow = glowTexture();
  const hits = [], bobbers = [], waters = [], falls = [], flags = [], fogs = [], lanterns = [], tags = [];
  const treeGeo = new THREE.ConeGeometry(.32, .9, 6), trunkGeo = new THREE.CylinderGeometry(.06, .08, .3, 5);
  const treeMats = [0x3f7a3a, 0x4f8c3c, 0x2f6a3a, 0x6b9a3a].map(c => new THREE.MeshStandardMaterial({ color: c, flatShading: true, roughness: .9 }));
  const trunkMat = new THREE.MeshStandardMaterial({ color: 0x5a3b24, flatShading: true });

  streams.forEach((s, i) => {
    const seed = hash(s.id) + 101, r = rng(seed);
    const island = new THREE.Group();
    const ang = i * Math.PI / 2 + Math.PI / 4;
    island.position.set(Math.cos(ang) * RING, (i % 2 ? .6 : -.4), Math.sin(ang) * RING);
    island.rotation.y = -ang + Math.PI / 2;
    scene.add(island);
    bobbers.push({ o: island, base: island.position.y, phase: i * 1.7 });

    // Grass cap and the rock beneath it, falling away to a point.
    const top = lowPoly(new THREE.CylinderGeometry(ISLAND_R, ISLAND_R * .96, .7, 11, 1), .32, seed, (c, y) => c.setHSL(.27 + (r() - .5) * .04, .55, y > .2 ? .33 + r() * .06 : .24));
    const topMesh = new THREE.Mesh(top, flat()); topMesh.receiveShadow = true; topMesh.castShadow = true; island.add(topMesh);
    const rock = lowPoly(new THREE.ConeGeometry(ISLAND_R * .97, 4.6, 11, 4), .5, seed + 1, (c, y, x) => {
      const t = (y + 2.3) / 4.6; c.setHSL(x > 0 ? .06 : .72, x > 0 ? .38 : .18, .16 + t * .2 + r() * .03);
    });
    const rockMesh = new THREE.Mesh(rock, flat()); rockMesh.rotation.x = Math.PI; rockMesh.position.y = -2.65; rockMesh.castShadow = true; island.add(rockMesh);

    // The peak: rock below the snow line, snow above it.
    const peakGeo = lowPoly(new THREE.ConeGeometry(PEAK_R, PEAK_H, 9, 7), .38, seed + 2, (c, y) => {
      const t = (y + PEAK_H / 2) / PEAK_H;
      if (t > .56 + r() * .1) c.setHSL(.58, .3, .95 + r() * .04);
      else c.setHSL(.64, .16, .11 + t * .14 + r() * .035);
    });
    const peak = new THREE.Mesh(peakGeo, flat());
    const peakPos = new THREE.Vector3(-.35, .35 + PEAK_H / 2, -.45);
    peak.position.copy(peakPos); peak.castShadow = peak.receiveShadow = true; island.add(peak);
    const shoulder = new THREE.Mesh(lowPoly(new THREE.ConeGeometry(1.2, 2.6, 7, 3), .3, seed + 3, (c, y) => y > .45 ? c.setHSL(.58, .3, .94) : c.setHSL(.64, .16, .14 + r() * .04)), flat());
    shoulder.position.set(1.1, .35 + 1.3, -1.2); shoulder.castShadow = true; island.add(shoulder);
    const summit = peakPos.clone().add(new THREE.Vector3(0, PEAK_H / 2, 0));

    // The river runs from the peak's foot to the rim, and pours off as a waterfall.
    const waterMat = new THREE.MeshStandardMaterial({ color: 0x3f86c9, emissive: 0x0d3557, roughness: .2, metalness: .1, flatShading: true });
    const river = new THREE.Mesh(new THREE.PlaneGeometry(.55, 2.4, 2, 8), waterMat);
    river.rotation.x = -Math.PI / 2; river.position.set(.9, .37, 2.45); island.add(river);
    waters.push(river);
    const fallN = 70, fallGeo = new THREE.BufferGeometry(), fp = new Float32Array(fallN * 3), fs = [];
    for (let k = 0; k < fallN; k++) { fs.push({ x: .9 + (r() - .5) * .6, y: -r() * 4.2, z: 3.68 + r() * .2, v: .9 + r() * .8 }); }
    fallGeo.setAttribute('position', new THREE.BufferAttribute(fp, 3));
    const fall = new THREE.Points(fallGeo, new THREE.PointsMaterial({ color: 0xbfe0ff, size: .09, transparent: true, opacity: .85, depthWrite: false }));
    island.add(fall); falls.push({ geo: fallGeo, drops: fs });
    const sheet = new THREE.Mesh(new THREE.PlaneGeometry(.45, 3.6, 1, 6), new THREE.MeshStandardMaterial({ color: 0x8cc4ee, transparent: true, opacity: .28, emissive: 0x1d5a86, side: THREE.DoubleSide, depthWrite: false }));
    sheet.position.set(.9, -1.5, 3.7); island.add(sheet);

    // Pines around the rim, kept clear of the river.
    for (let k = 0; k < 16; k++) {
      const a = r() * Math.PI * 2, d = 2.2 + r() * 1.25;
      const x = Math.cos(a) * d, z = Math.sin(a) * d;
      if (Math.abs(x - .9) < .7 && z > 1) continue;
      const tree = new THREE.Group(), h = .8 + r() * .7, m = treeMats[(k + i) % treeMats.length];
      const t1 = new THREE.Mesh(treeGeo, m); t1.position.y = .45 + .3; t1.castShadow = true;
      const t2 = new THREE.Mesh(treeGeo, m); t2.scale.setScalar(.72); t2.position.y = .45 + .72; t2.castShadow = true;
      const tr = new THREE.Mesh(trunkGeo, trunkMat); tr.position.y = .3;
      tree.add(tr, t1, t2); tree.scale.setScalar(h); tree.position.set(x, .3, z);
      island.add(tree);
    }

    // The summit flag: nobody has planted one. Pale and translucent, waving.
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(.025, .025, .9, 5), new THREE.MeshStandardMaterial({ color: 0xcfd5d8 }));
    pole.position.copy(summit).add(new THREE.Vector3(0, .45, 0)); island.add(pole);
    const flagGeo = new THREE.PlaneGeometry(.55, .32, 6, 1);
    const flag = new THREE.Mesh(flagGeo, new THREE.MeshStandardMaterial({ color: 0x70c28a, transparent: true, opacity: .45, side: THREE.DoubleSide, emissive: 0x204a2c }));
    flag.position.copy(summit).add(new THREE.Vector3(.3, .72, 0)); island.add(flag);
    flags.push({ geo: flagGeo, base: Float32Array.from(flagGeo.attributes.position.array) });

    // Camps: each file at the altitude of its stage, spread around the peak.
    const surfaceAt = (h, a) => {
      if (h === 0) return new THREE.Vector3(peakPos.x + Math.cos(a) * (PEAK_R + .55 + (a % 1) * .2), .45, peakPos.z + Math.sin(a) * (PEAK_R + .55));
      const rad = PEAK_R * (1 - h) + .14;
      return new THREE.Vector3(peakPos.x + Math.cos(a) * rad, peakPos.y - PEAK_H / 2 + h * PEAK_H + .06, peakPos.z + Math.sin(a) * rad);
    };
    const groups = {};
    for (const f of s.files) (groups[f.stage === 'blocked' ? 'working' : f.stage] ||= []).push(f);
    let highest = 0, pickPos = null;
    for (const [k, list] of Object.entries(groups)) {
      list.sort((a, b) => b.debt - a.debt).forEach((f, j) => {
        const h = CAMP_H[f.stage] ?? 0;
        highest = Math.max(highest, h);
        // Spread around the front of the peak first, where the camera spends most time.
        const a = Math.PI * .5 + (j - (list.length - 1) / 2) * (k === 'unworked' ? .55 : .62) + (hash(s.id + k) % 7) * .05;
        const p = surfaceAt(h, a);
        const col = STAGE_HEX[f.stage] ?? 0x6a9cf2;
        const camp = new THREE.Group(); camp.position.copy(p); island.add(camp);
        const tent = new THREE.Mesh(new THREE.ConeGeometry(f.stage === 'held' ? .2 : .14, f.stage === 'held' ? .26 : .2, 4), new THREE.MeshStandardMaterial({ color: col, flatShading: true, roughness: .6, emissive: col, emissiveIntensity: .25 }));
        tent.position.y = .1; tent.rotation.y = Math.PI / 4; tent.castShadow = true; camp.add(tent);
        const cold = f.movable && f.idleNow > 14;
        const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: glow, color: col, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: cold ? .35 : .9 }));
        sprite.scale.setScalar(f.stage === 'held' ? 1.1 : .75); sprite.position.y = .16; camp.add(sprite);
        lanterns.push({ s: sprite, base: sprite.scale.x, phase: hash(f.slug) % 100, cold });
        const hit = new THREE.Mesh(new THREE.SphereGeometry(.34, 8, 6), new THREE.MeshBasicMaterial({ visible: false }));
        hit.position.y = .12; hit.userData = { slug: f.slug }; camp.add(hit); hits.push(hit);
        if (cold) {
          const fog = cloud(hash(f.slug), .42, .38);
          fog.position.copy(p).add(new THREE.Vector3(0, .15, 0)); island.add(fog);
          fogs.push({ o: fog, base: fog.position.clone(), phase: hash(f.slug) % 60 });
        }
        if (f.stage === 'held') tags.push({ el: label(`${f.name}${f.pickup ? '<i>pick-up rule</i>' : ''}`, 'held'), obj: camp, up: .5, axis: peak });
        if (f.slug === pick?.slug) pickPos = { camp, p };
      });
    }
    // The route: a switchback up the peak, inked as far as anyone has climbed.
    const routePts = [];
    for (let t = 0; t <= 1.0001; t += .02) { const a = Math.PI * .5 + Math.sin(t * Math.PI * 3) * .9; routePts.push(surfaceAt(Math.min(.97, t), a).add(new THREE.Vector3(0, .03, 0))); }
    const route = new THREE.CatmullRomCurve3(routePts);
    const done = new THREE.Line(new THREE.BufferGeometry().setFromPoints(route.getPoints(160).filter(v => (v.y - (peakPos.y - PEAK_H / 2)) / PEAK_H <= highest + .02)), new THREE.LineBasicMaterial({ color: 0xf2eee5, transparent: true, opacity: .7 }));
    const rest = new THREE.Line(new THREE.BufferGeometry().setFromPoints(route.getPoints(160)), new THREE.LineDashedMaterial({ color: 0x8d9aa3, dashSize: .12, gapSize: .12, transparent: true, opacity: .45 }));
    rest.computeLineDistances(); island.add(rest, done);

    // The next firing: a beacon over its file, and a climber on the route below it.
    if (pickPos) {
      const beam = new THREE.Mesh(new THREE.CylinderGeometry(.05, .22, 7, 10, 1, true), new THREE.MeshBasicMaterial({ color: 0x45c7b9, transparent: true, opacity: .22, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
      beam.position.y = 3.6; pickPos.camp.add(beam);
      tags.push({ el: label('Next ascent', 'next'), obj: pickPos.camp, up: .75, axis: peak });
      const climber = new THREE.Group();
      const body = new THREE.Mesh(new THREE.CapsuleGeometry(.05, .12, 3, 6), new THREE.MeshStandardMaterial({ color: 0x45c7b9, emissive: 0x1b6a62 }));
      const lamp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glow, color: 0x9ff3ea, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
      lamp.scale.setScalar(.45); lamp.position.y = .12; body.position.y = .1; climber.add(body, lamp); island.add(climber);
      bobbers.push({ climber, route, from: pickPos.p.y });
    }
    tags.push({ el: label(`<b>${s.id}</b>${s.label}`, 'stream'), obj: island, up: -1.2, at: new THREE.Vector3(0, -.4, ISLAND_R + .4) });

    // Clouds drift around each island.
    for (let k = 0; k < 2; k++) {
      const c = cloud(seed + 50 + k, .5 + r() * .3, .92), ca = r() * Math.PI * 2, cr = 4.6 + r() * 1.6;
      c.position.set(Math.cos(ca) * cr, 3.2 + r() * 3.4, Math.sin(ca) * cr); island.add(c);
      fogs.push({ o: c, base: c.position.clone(), phase: k * 20 + i * 7, wide: true });
    }
  });

  const sea = new THREE.Group(), sr = rng(4242);
  for (let k = 0; k < 26; k++) {
    const c = cloud(9000 + k, 1.2 + sr() * 1.3, .42), a = sr() * Math.PI * 2, d = 3 + sr() * 18;
    c.position.set(Math.cos(a) * d, -9.5 - sr() * 3, Math.sin(a) * d); c.rotation.y = sr() * 6;
    sea.add(c);
  }
  scene.add(sea);
  const starGeo = new THREE.BufferGeometry(), sp = new Float32Array(500 * 3);
  for (let k = 0; k < 500; k++) {
    const th = sr() * Math.PI * 2, ph = Math.acos(sr() * .9 + .1), R = 90;
    sp.set([R * Math.sin(ph) * Math.cos(th), R * Math.cos(ph) - 10, R * Math.sin(ph) * Math.sin(th)], k * 3);
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(sp, 3));
  const stars = new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xcfd8e6, size: 1.6, sizeAttenuation: false, transparent: true, opacity: .7, fog: false, depthWrite: false }));
  scene.add(stars);

  function label(html, cls) {
    const d = document.createElement('div'); d.className = `a3-tag ${cls}`; d.innerHTML = html; labels.appendChild(d); return d;
  }

  // Camera: a slow orbit, which a drag takes over and lets go of.
  let yaw = .35, pitch = .44, dist = 34, auto = !reduced, dragging = null, idleAt = 0;
  const target = new THREE.Vector3(0, .6, 0);
  const place = () => {
    camera.position.set(target.x + Math.sin(yaw) * Math.cos(pitch) * dist, target.y + Math.sin(pitch) * dist, target.z + Math.cos(yaw) * Math.cos(pitch) * dist);
    camera.lookAt(target);
  };
  const cv = renderer.domElement;
  cv.style.touchAction = 'pan-y';
  cv.addEventListener('pointerdown', e => { dragging = { x: e.clientX, y: e.clientY, yaw, pitch, moved: false }; });
  addEventListener('pointerup', () => { if (dragging) idleAt = performance.now(); dragging = null; });
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  const pickAt = e => {
    const b = cv.getBoundingClientRect();
    ndc.set(((e.clientX - b.left) / b.width) * 2 - 1, -((e.clientY - b.top) / b.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    return ray.intersectObjects(hits, false)[0]?.object.userData.slug;
  };
  cv.addEventListener('pointermove', e => {
    if (dragging) {
      const dx = e.clientX - dragging.x, dy = e.clientY - dragging.y;
      if (Math.abs(dx) + Math.abs(dy) > 4) dragging.moved = true;
      yaw = dragging.yaw - dx * .006;
      if (e.pointerType !== 'touch') pitch = Math.min(.9, Math.max(.12, dragging.pitch + dy * .004));
      auto = false; onUntip(); return;
    }
    if (e.pointerType === 'touch') return;
    const slug = pickAt(e);
    cv.style.cursor = slug ? 'pointer' : 'grab';
    if (slug) { auto = false; idleAt = performance.now(); onTip(slug, { left: e.clientX - 1, width: 2, top: e.clientY - 1, bottom: e.clientY + 1 }); } else onUntip();
  });
  cv.addEventListener('pointerleave', () => { onUntip(); idleAt = performance.now(); });
  cv.addEventListener('click', e => { if (dragging?.moved) return; const slug = pickAt(e); if (slug) onOpen(slug); });

  const resize = () => {
    const w = host.clientWidth, h = host.clientHeight;
    renderer.setSize(w, h, false); camera.aspect = w / h;
    dist = Math.max(33, 12.5 / (Math.tan(THREE.MathUtils.degToRad(17)) * camera.aspect));
    scene.fog.near = dist + 4; scene.fog.far = dist + 50;
    target.y = camera.aspect < 1 ? -3.2 : .6;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(host); resize();

  let visible = true, last = performance.now();
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) { last = performance.now(); requestAnimationFrame(frame); } }).observe(host);
  const v = new THREE.Vector3(), camDir = new THREE.Vector3(), toObj = new THREE.Vector3();

  function frame(now) {
    if (!visible || document.hidden) return;
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    const t = now / 1000;
    if (!auto && !dragging && !reduced && now - idleAt > 4000) auto = true;
    if (auto) yaw += dt * .06;
    place();
    if (!reduced) {
      for (const b of bobbers) {
        if (b.o) b.o.position.y = b.base + Math.sin(t * .5 + b.phase) * .22;
        if (b.climber) {
          // The climber walks from base camp up to the pick's camp, rests, and starts again.
          const cycle = (t % 14) / 14, top = Math.max(.05, Math.min(.9, (b.from - .4) / PEAK_H));
          const u = Math.min(1, cycle / .8) * top;
          b.climber.position.copy(b.route.getPointAt(u));
          b.climber.visible = cycle < .97;
        }
      }
      for (const w of waters) w.material.emissiveIntensity = .8 + Math.sin(t * 2.2) * .2;
      for (const f of falls) {
        const p = f.geo.attributes.position;
        f.drops.forEach((d, k) => { d.y -= d.v * dt * 2.2; if (d.y < -4.4) d.y = 0; p.setXYZ(k, d.x + Math.sin(d.y * 3 + k) * .03, d.y + .2, d.z - d.y * .05); });
        p.needsUpdate = true;
      }
      for (const fl of flags) {
        const p = fl.geo.attributes.position;
        for (let k = 0; k < p.count; k++) { const x = fl.base[k * 3]; p.setZ(k, Math.sin(t * 3 + x * 7) * .06 * (x + .28)); }
        p.needsUpdate = true;
      }
      for (const f of fogs) f.o.position.set(f.base.x + Math.sin(t * .15 + f.phase) * (f.wide ? 1.4 : .12), f.base.y + Math.sin(t * .3 + f.phase) * .06, f.base.z + Math.cos(t * .12 + f.phase) * (f.wide ? 1.1 : .1));
      sea.rotation.y = t * .012;
      stars.rotation.y = t * .004;
      for (const l of lanterns) l.s.scale.setScalar(l.base * (1 + Math.sin(t * 1.6 + l.phase) * (l.cold ? .02 : .07)));
    }
    renderer.render(scene, camera);
    // Labels follow their objects and fade when the peak turns them away.
    camera.getWorldDirection(camDir);
    const W = host.clientWidth, H = host.clientHeight;
    for (const tg of tags) {
      if (tg.at) v.copy(tg.at); else v.set(0, tg.up, 0);
      tg.obj.localToWorld(v);
      toObj.copy(v).sub(camera.position).normalize();
      let facing = 1;
      if (tg.axis) {
        const axis = new THREE.Vector3(); tg.axis.getWorldPosition(axis);
        const out = new THREE.Vector3(v.x - axis.x, 0, v.z - axis.z).normalize();
        facing = -out.dot(new THREE.Vector3(toObj.x, 0, toObj.z).normalize());
      }
      v.project(camera);
      const x = (v.x * .5 + .5) * W, y = (-v.y * .5 + .5) * H;
      tg.el.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, -100%)`;
      tg.el.style.opacity = v.z > 1 ? 0 : Math.max(0, Math.min(1, facing * 3 + .2)).toFixed(2);
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  return { renderer };
}
