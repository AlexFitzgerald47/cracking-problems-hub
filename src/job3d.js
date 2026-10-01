// The job, in three dimensions: a noir back room under one hanging lamp. Five crews
// of raccoons in trench coats, each doing its real job, around a safe marked PASS.
// The tumbler lamps, the dial and the speech come from the board's own data.
import * as THREE from './vendor/three.module.min.js';

const rng = seed => () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, flatShading: true, roughness: .85, metalness: 0, ...o });

function canvasTex(w, h, draw) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h;
  draw(cv.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}

// A raccoon in a trench coat. Returns the group and the parts that move.
function raccoon({ coat, band, hat = 0x232326, scale = 1, glasses = true, coatH = 1, head = true }) {
  const g = new THREE.Group(), parts = {};
  const coatMat = std(coat, { roughness: .95 }), dark = std(0x1b1c1f), fur = std(0x8b8f95), cream = std(0xe6e0d4);
  const H = 1.25 * coatH;
  // The coat: a lathe, flared at the hem, nipped at the belt.
  const prof = [[.02, 0], [.44, .06], [.42, .3 * H], [.37, .52 * H], [.31, .62 * H], [.33, .8 * H], [.37, .92 * H], [.34, .98 * H], [.17, 1.0 * H]].map(([r, y]) => new THREE.Vector2(r, y));
  const body = new THREE.Mesh(new THREE.LatheGeometry(prof, 11), coatMat); body.castShadow = true; g.add(body); parts.body = body;
  const belt = new THREE.Mesh(new THREE.TorusGeometry(.315, .035, 4, 14), std(new THREE.Color(coat).multiplyScalar(.7)));
  belt.rotation.x = Math.PI / 2; belt.position.y = .62 * H; g.add(belt);
  const buckle = new THREE.Mesh(new THREE.BoxGeometry(.1, .08, .03), std(0xb89a5e, { metalness: .6, roughness: .4 })); buckle.position.set(0, .62 * H, .33); g.add(buckle);
  // Lapels, collar, two rows of buttons.
  for (const s of [-1, 1]) {
    const lapel = new THREE.Mesh(new THREE.BoxGeometry(.16, .3, .03), std(new THREE.Color(coat).multiplyScalar(.82)));
    lapel.position.set(s * .1, .86 * H, .3); lapel.rotation.set(-.25, 0, s * .45); g.add(lapel);
    for (const y of [.74, .52, .36]) { const b = new THREE.Mesh(new THREE.SphereGeometry(.022, 6, 4), dark); b.position.set(s * .1, y * H, .33 - (y < .5 ? -.04 : 0)); g.add(b); }
  }
  const collar = new THREE.Mesh(new THREE.CylinderGeometry(.2, .3, .16, 10, 1, true), std(new THREE.Color(coat).multiplyScalar(.85), { side: THREE.DoubleSide }));
  collar.position.y = 1.0 * H; g.add(collar);
  // Sleeves with paws, hanging into the pockets unless a pose lifts them.
  for (const s of [-1, 1]) {
    const arm = new THREE.Group(); arm.position.set(s * .36, .92 * H, 0);
    const sleeve = new THREE.Mesh(new THREE.CapsuleGeometry(.075, .42, 3, 7), coatMat); sleeve.position.y = -.26; sleeve.castShadow = true;
    const paw = new THREE.Mesh(new THREE.SphereGeometry(.07, 7, 5), dark); paw.position.y = -.54;
    arm.add(sleeve, paw); arm.rotation.z = s * .12; g.add(arm);
    parts[s < 0 ? 'armL' : 'armR'] = arm;
  }
  // Feet under the hem, and a ringed tail out the back.
  for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.SphereGeometry(.09, 7, 4), dark); f.scale.set(1, .5, 1.5); f.position.set(s * .14, .03, .14); g.add(f); }
  const tail = new THREE.Group(); tail.position.set(0, .16, -.36); g.add(tail); parts.tail = tail;
  for (let i = 0; i < 6; i++) {
    const seg = new THREE.Mesh(new THREE.SphereGeometry(.1 - i * .006, 7, 5), i % 2 ? dark : fur);
    seg.position.set(Math.sin(i * .5) * .05, i * .03, -i * .11); seg.scale.set(1, 1, 1.3); seg.castShadow = true; tail.add(seg);
  }
  if (head) {
    const hd = new THREE.Group(); hd.position.y = H + .2; g.add(hd); parts.head = hd;
    const skull = new THREE.Mesh(new THREE.IcosahedronGeometry(.27, 1), fur); skull.scale.set(1.05, .86, .92); skull.castShadow = true; hd.add(skull);
    // Cheek ruffs, the white brow, the dark mask, the muzzle and nose.
    for (const s of [-1, 1]) {
      const ruff = new THREE.Mesh(new THREE.ConeGeometry(.12, .22, 5), cream); ruff.position.set(s * .25, -.08, .05); ruff.rotation.z = s * 2.1; hd.add(ruff);
      const mask = new THREE.Mesh(new THREE.SphereGeometry(.1, 8, 6), dark); mask.scale.set(1.4, .75, .5); mask.position.set(s * .1, .02, .21); hd.add(mask);
      const ear = new THREE.Mesh(new THREE.ConeGeometry(.08, .15, 4), fur); ear.position.set(s * .19, .22, -.02); ear.rotation.z = -s * .35; hd.add(ear);
      const inner = new THREE.Mesh(new THREE.ConeGeometry(.045, .09, 4), dark); inner.position.set(s * .19, .22, .02); inner.rotation.z = -s * .35; hd.add(inner);
    }
    const brow = new THREE.Mesh(new THREE.SphereGeometry(.1, 8, 5), cream); brow.scale.set(1.9, .45, .5); brow.position.set(0, .11, .2); hd.add(brow);
    const muzzle = new THREE.Mesh(new THREE.ConeGeometry(.1, .2, 7), cream); muzzle.rotation.x = Math.PI / 2; muzzle.position.set(0, -.07, .3); hd.add(muzzle);
    const nose = new THREE.Mesh(new THREE.SphereGeometry(.035, 7, 5), std(0x0b0b0d, { roughness: .3 })); nose.position.set(0, -.06, .4); hd.add(nose);
    if (glasses) {
      const lens = std(0x050608, { roughness: .15, metalness: .5 });
      for (const s of [-1, 1]) { const l = new THREE.Mesh(new THREE.BoxGeometry(.13, .07, .02), lens); l.position.set(s * .085, .02, .26); hd.add(l); }
      const bridge = new THREE.Mesh(new THREE.BoxGeometry(.06, .015, .015), lens); bridge.position.set(0, .04, .265); hd.add(bridge);
    } else {
      for (const s of [-1, 1]) { const e = new THREE.Mesh(new THREE.SphereGeometry(.028, 6, 5), std(0x0a0a0a, { roughness: .2 })); e.position.set(s * .09, .02, .255); hd.add(e); const glint = new THREE.Mesh(new THREE.SphereGeometry(.008, 4, 3), new THREE.MeshBasicMaterial({ color: 0xffffff })); glint.position.set(s * .09 + .01, .03, .28); hd.add(glint); }
    }
    // The fedora, tipped a little; its band is the crew's colour.
    const hatG = new THREE.Group(); hatG.position.y = .2; hatG.rotation.set(-.08, 0, .06); hd.add(hatG);
    const brim = new THREE.Mesh(new THREE.CylinderGeometry(.46, .46, .025, 18), std(hat, { roughness: .9 })); brim.castShadow = true; hatG.add(brim);
    const crown = new THREE.Mesh(new THREE.CylinderGeometry(.21, .26, .18, 14), std(hat, { roughness: .9 })); crown.position.y = .1; crown.scale.z = .88; crown.castShadow = true; hatG.add(crown);
    const pinch = new THREE.Mesh(new THREE.BoxGeometry(.16, .035, .36), std(new THREE.Color(hat).multiplyScalar(.7))); pinch.position.y = .185; hatG.add(pinch);
    const bandM = new THREE.Mesh(new THREE.CylinderGeometry(.263, .263, .055, 14), std(band, { emissive: band, emissiveIntensity: .25 })); bandM.position.y = .045; bandM.scale.z = .88; hatG.add(bandM);
  }
  g.scale.setScalar(scale);
  return { g, parts };
}

export function mount(host, { pick, pickName, overwatchOwed, newPacks, best, streamIds, units, onCrew, onCrewTip, onUntip, reduced }) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.1;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0x07090c);
  host.appendChild(renderer.domElement);
  renderer.domElement.setAttribute('aria-hidden', 'true');
  const overlay = document.createElement('div'); overlay.className = 'j3-labels'; host.appendChild(overlay);

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x07090c, .045);
  const camera = new THREE.PerspectiveCamera(32, 1, .1, 100);
  const r = rng(77);

  // The room: a brick wall, a tiled floor, a skirting board.
  const brick = canvasTex(512, 512, (x, w, h) => {
    x.fillStyle = '#241612'; x.fillRect(0, 0, w, h);
    for (let row = 0; row < 16; row++) for (let col = -1; col < 9; col++) {
      const bx = col * 64 + (row % 2) * 32, by = row * 32, l = 18 + r() * 14;
      x.fillStyle = `hsl(${10 + r() * 8}, ${30 + r() * 15}%, ${l}%)`; x.fillRect(bx + 2, by + 2, 60, 28);
    }
  });
  brick.wrapS = brick.wrapT = THREE.RepeatWrapping; brick.repeat.set(4, 2);
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(26, 10), new THREE.MeshStandardMaterial({ map: brick, roughness: 1 }));
  wall.position.set(0, 5, -2.2); wall.receiveShadow = true; scene.add(wall);
  const tiles = canvasTex(256, 256, (x, w, h) => {
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { x.fillStyle = (i + j) % 2 ? '#2a1d17' : '#3a2a20'; x.fillRect(i * 64, j * 64, 64, 64); x.strokeStyle = '#120c09'; x.strokeRect(i * 64, j * 64, 64, 64); }
  });
  tiles.wrapS = tiles.wrapT = THREE.RepeatWrapping; tiles.repeat.set(8, 3);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(26, 9), new THREE.MeshStandardMaterial({ map: tiles, roughness: .7, metalness: .1 }));
  floor.rotation.x = -Math.PI / 2; floor.position.set(0, 0, 2.2); floor.receiveShadow = true; scene.add(floor);
  const skirt = new THREE.Mesh(new THREE.BoxGeometry(26, .25, .1), std(0x120c09)); skirt.position.set(0, .12, -2.15); scene.add(skirt);

  // Light: one hanging lamp over the safe, a cold fill, a rim from the door.
  scene.add(new THREE.HemisphereLight(0x8090a8, 0x1a120c, .7));
  const key = new THREE.DirectionalLight(0xbfd0ff, .55); key.position.set(0, 3, 10); scene.add(key);
  for (const [x, c, i] of [[-4.6, 0xffc98a, 26], [5.6, 0xb7a6ff, 18]]) {
    const pool = new THREE.SpotLight(c, i, 11, .55, .7, 1.6); pool.position.set(x, 5.6, 1.6); pool.target.position.set(x, 0, -.3); scene.add(pool, pool.target);
  }
  const lampPos = new THREE.Vector3(1.4, 5.4, 1.2);
  const spot = new THREE.SpotLight(0xffd59a, 70, 16, .78, .5, 1.6);
  spot.position.copy(lampPos); spot.target.position.set(1.2, 0, .4); spot.castShadow = true;
  spot.shadow.mapSize.set(1024, 1024); spot.shadow.bias = -.0006; scene.add(spot, spot.target);
  const rim = new THREE.DirectionalLight(0x6f8fd0, .6); rim.position.set(-6, 4, 3); scene.add(rim);
  const fill = new THREE.PointLight(0x7a5a3a, 6, 9, 2); fill.position.set(-4.2, 3, 2); scene.add(fill);
  // The lamp itself: flex, shade, bulb glow, and the cone of light through the dust.
  const flex = new THREE.Mesh(new THREE.CylinderGeometry(.01, .01, 3, 4), std(0x111111)); flex.position.set(lampPos.x, lampPos.y + 1.5, lampPos.z); scene.add(flex);
  const shade = new THREE.Mesh(new THREE.ConeGeometry(.45, .35, 14, 1, true), std(0x2f3a34, { side: THREE.DoubleSide, metalness: .4, roughness: .5 })); shade.position.copy(lampPos).add(new THREE.Vector3(0, .1, 0)); scene.add(shade);
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(.1, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffe2b0 })); bulb.position.copy(lampPos).add(new THREE.Vector3(0, -.05, 0)); scene.add(bulb);
  const beam = new THREE.Mesh(new THREE.ConeGeometry(3.4, 5.4, 32, 1, true), new THREE.MeshBasicMaterial({ color: 0xffd59a, transparent: true, opacity: .045, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
  beam.position.copy(lampPos).add(new THREE.Vector3(-.1, -2.7, -.4)); scene.add(beam);
  const dustN = 260, dustGeo = new THREE.BufferGeometry(), dp = new Float32Array(dustN * 3), dust = [];
  for (let i = 0; i < dustN; i++) { const a = r() * Math.PI * 2, rr = Math.sqrt(r()) * 2.6, y = r() * 5; dust.push({ a, rr, y, s: .05 + r() * .12 }); }
  dustGeo.setAttribute('position', new THREE.BufferAttribute(dp, 3));
  scene.add(new THREE.Points(dustGeo, new THREE.PointsMaterial({ color: 0xffe2b8, size: .025, transparent: true, opacity: .7, depthWrite: false, blending: THREE.AdditiveBlending })));

  // The safe: a steel door, bolts, hinges, seven tumbler lamps and a dial.
  const SX = 2.9, SY = 2.1, SR = 1.75;
  const safe = new THREE.Group(); safe.position.set(SX, SY, -1.6); scene.add(safe);
  const safeFrame = new THREE.Mesh(new THREE.BoxGeometry(SR * 2 + .5, SR * 2 + .5, .5), std(0x1d2429, { metalness: .5, roughness: .6 })); safeFrame.position.z = -.2; safeFrame.castShadow = safeFrame.receiveShadow = true; safe.add(safeFrame);
  const door = new THREE.Mesh(new THREE.CylinderGeometry(SR, SR, .28, 40), std(0x56626b, { metalness: .75, roughness: .38, flatShading: false }));
  door.rotation.x = Math.PI / 2; door.position.z = .12; door.castShadow = door.receiveShadow = true; safe.add(door);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(SR - .14, .03, 6, 48), std(0x2b343a, { metalness: .6 })); ring.position.z = .27; safe.add(ring);
  for (let i = 0; i < 24; i++) { const a = i / 24 * Math.PI * 2, b = new THREE.Mesh(new THREE.SphereGeometry(.045, 8, 6), std(0x9aa5ad, { metalness: .8, roughness: .3, flatShading: false })); b.position.set(Math.cos(a) * (SR - .07), Math.sin(a) * (SR - .07), .27); safe.add(b); }
  for (const y of [.95, -.95]) { const hg = new THREE.Mesh(new THREE.BoxGeometry(.3, .55, .3), std(0x3a454d, { metalness: .6 })); hg.position.set(SR + .1, y, .1); safe.add(hg); }
  const plate = new THREE.Mesh(new THREE.PlaneGeometry(1.2, .24), new THREE.MeshStandardMaterial({ map: canvasTex(512, 102, (x, w, h) => { x.fillStyle = '#262e33'; x.fillRect(0, 0, w, h); x.strokeStyle = '#59656d'; x.lineWidth = 6; x.strokeRect(3, 3, w - 6, h - 6); x.fillStyle = '#b3bec5'; x.font = '600 54px Inter, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.letterSpacing = '22px'; x.fillText('PASS', w / 2 + 10, h / 2 + 3); }), metalness: .5, roughness: .45 }));
  plate.position.set(0, 1.25, .275); safe.add(plate);
  const haloTex = canvasTex(64, 64, (x) => { const g = x.createRadialGradient(32, 32, 0, 32, 32, 32); g.addColorStop(0, 'rgba(255,255,255,.9)'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(0, 0, 64, 64); });
  const lamps = [];
  for (let i = 0; i < 7; i++) {
    const a = Math.PI * (.86 - i * .12), on = i < best;
    const m = new THREE.Mesh(new THREE.SphereGeometry(.09, 12, 8), on ? new THREE.MeshBasicMaterial({ color: 0xf59a52, toneMapped: false }) : std(0x1a2126, { metalness: .4, roughness: .4, flatShading: false }));
    m.position.set(Math.cos(a) * 1.05, Math.sin(a) * 1.05 - .05, .3); safe.add(m); lamps.push({ m, on, phase: i * .7 });
    if (on) { const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: haloTex, color: 0xf0884a, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })); halo.scale.setScalar(.6); halo.position.copy(m.position).add(new THREE.Vector3(0, 0, .05)); safe.add(halo); }
  }
  const dialTex = canvasTex(256, 256, (x, w) => {
    x.fillStyle = '#2b343a'; x.beginPath(); x.arc(128, 128, 126, 0, Math.PI * 2); x.fill();
    x.strokeStyle = '#c8d1d6'; x.lineCap = 'round';
    for (let i = 0; i < 40; i++) { const a = i / 40 * Math.PI * 2; x.lineWidth = i % 10 ? 2 : 4; x.beginPath(); x.moveTo(128 + Math.cos(a) * 112, 128 + Math.sin(a) * 112); x.lineTo(128 + Math.cos(a) * (i % 10 ? 100 : 94), 128 + Math.sin(a) * (i % 10 ? 100 : 94)); x.stroke(); }
    x.fillStyle = '#e8edf0'; x.font = '600 34px "JetBrains Mono", monospace'; x.textAlign = 'center'; x.textBaseline = 'middle';
    streamIds.forEach((id, i) => { const a = i / 4 * Math.PI * 2 - Math.PI / 2; x.fillText(id, 128 + Math.cos(a) * 70, 128 + Math.sin(a) * 70); });
  });
  const dial = new THREE.Mesh(new THREE.CylinderGeometry(.48, .48, .12, 40), [std(0x1c2429, { metalness: .6, flatShading: false }), new THREE.MeshStandardMaterial({ map: dialTex, metalness: .3, roughness: .5 }), std(0x1c2429)]);
  dial.rotation.x = Math.PI / 2; dial.position.set(0, -.1, .34); safe.add(dial);
  const knob = new THREE.Mesh(new THREE.CylinderGeometry(.16, .18, .12, 16), std(0x46535b, { metalness: .7, roughness: .35, flatShading: false })); knob.rotation.x = Math.PI / 2; knob.position.set(0, -.1, .43); safe.add(knob);
  const index = new THREE.Mesh(new THREE.ConeGeometry(.05, .1, 3), new THREE.MeshStandardMaterial({ color: 0x45c7b9, emissive: 0x45c7b9, emissiveIntensity: 1.2 })); index.rotation.z = Math.PI; index.position.set(0, .45, .36); safe.add(index);
  const pickIdx = Math.max(0, streamIds.indexOf(pick?.stream));
  const dialTarget = pickIdx * Math.PI / 2;
  const wheel = new THREE.Group(); wheel.position.set(1.05, -.95, .32); safe.add(wheel);
  for (let i = 0; i < 3; i++) { const sp = new THREE.Mesh(new THREE.CylinderGeometry(.04, .04, .9, 6), std(0x9aa5ad, { metalness: .8, roughness: .3 })); sp.rotation.z = i * Math.PI / 3; wheel.add(sp); }
  wheel.add(new THREE.Mesh(new THREE.SphereGeometry(.08, 10, 8), std(0x5d6a73, { metalness: .8 })));

  // Filing cabinets for the Pathfinders to raid.
  const cabMat = std(0x5d6450, { metalness: .35, roughness: .6 }), cabs = new THREE.Group(); cabs.position.set(-3.55, 0, -1.4); scene.add(cabs);
  const drawers = [];
  for (const [cx, n] of [[-.55, 4], [.55, 3]]) {
    const body = new THREE.Mesh(new THREE.BoxGeometry(1, n * .55, .9), cabMat); body.position.set(cx, n * .55 / 2, 0); body.castShadow = body.receiveShadow = true; cabs.add(body);
    for (let k = 0; k < n; k++) {
      const d = new THREE.Group(); d.position.set(cx, .28 + k * .55, .45); cabs.add(d);
      const front = new THREE.Mesh(new THREE.BoxGeometry(.9, .48, .05), std(0x6a7260, { metalness: .35, roughness: .5 })); front.castShadow = true; d.add(front);
      const handle = new THREE.Mesh(new THREE.BoxGeometry(.24, .04, .05), std(0xb8b8a8, { metalness: .7, roughness: .3 })); handle.position.set(0, .06, .05); d.add(handle);
      const label = new THREE.Mesh(new THREE.PlaneGeometry(.2, .08), std(0xe9e1cc)); label.position.set(0, -.08, .03); d.add(label);
      const box = new THREE.Mesh(new THREE.BoxGeometry(.86, .4, .8), std(0x4d5444)); box.position.z = -.42; d.add(box);
      const papers = new THREE.Mesh(new THREE.BoxGeometry(.78, .3, .7), std(0xe6dcc4)); papers.position.set(0, .07, -.42); d.add(papers);
      drawers.push({ d, base: .45, phase: r() * 6, open: k === n - 1 || k === 1 });
    }
  }
  const paperMat = new THREE.MeshStandardMaterial({ color: 0xeee4cc, side: THREE.DoubleSide, roughness: .9 });
  const flying = Array.from({ length: 14 }, (_, i) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(.22, .3), paperMat); m.castShadow = true; scene.add(m); return { m, t: i / 14, seed: r() * 10, side: .4 + r() * .6 }; });

  const crews = [];
  const hit = (group, k, w, h) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, .9), new THREE.MeshBasicMaterial({ visible: false })); b.position.y = h / 2; b.userData.unit = k; group.add(b); crews.push(b); };
  const U = Object.fromEntries(units.map(u => [u.key, u]));

  // The Irregulars: three of them, one coat, one hat. The middle one peeks out.
  const irr = raccoon({ coat: 0xb39a72, band: U.irregular.color, hat: 0x3b3022, coatH: 2.15 });
  irr.g.position.set(-5.6, 0, -.2); irr.g.rotation.y = .35; scene.add(irr.g); hit(irr.g, 'irregular', 1, 3.4);
  const peek = new THREE.Group(); peek.position.set(0, 1.45, .36); irr.g.add(peek);
  const slit = new THREE.Mesh(new THREE.SphereGeometry(.13, 10, 6), std(0x111214)); slit.scale.set(1.5, .5, .3); peek.add(slit);
  const peekEyes = [];
  for (const s of [-1, 1]) { const e = new THREE.Mesh(new THREE.SphereGeometry(.035, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffffff })); e.position.set(s * .07, .01, .04); peek.add(e); peekEyes.push(e); }
  for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.SphereGeometry(.09, 7, 4), std(0x1b1c1f)); f.scale.set(1, .5, 1.5); f.position.set(s * .32, .03, .2); irr.g.add(f); }

  // The Pathfinders: one in the drawers, one on top passing papers out.
  const pf1 = raccoon({ coat: 0x9a7b52, band: U.finder.color, hat: 0x4a3a28, scale: .82 });
  pf1.g.position.set(-3.0, 0, .35); pf1.g.rotation.y = -.5; scene.add(pf1.g); hit(pf1.g, 'finder', 1, 1.9);
  pf1.parts.armR.rotation.set(-1.3, 0, -.2); pf1.parts.armL.rotation.set(-.9, 0, .3);
  const pf2 = raccoon({ coat: 0x8a6c46, band: U.finder.color, hat: 0x3d2f20, scale: .62, glasses: false });
  pf2.g.position.set(-4.0, 2.2, -1.2); pf2.g.rotation.y = .4; scene.add(pf2.g); hit(pf2.g, 'finder', .8, 1.4);
  pf2.parts.armR.rotation.set(-2.2, 0, -.3);
  const heldPaper = new THREE.Mesh(new THREE.PlaneGeometry(.26, .34), paperMat); heldPaper.position.set(0, -.6, .05); pf2.parts.armR.add(heldPaper);

  // The Tribunal: three seats in olive, placards up.
  const words = [['PARTIAL', '#b24d17'], ['PARTIAL', '#b24d17'], ['REFUTE?', '#a5301d']];
  const placards = [];
  words.forEach(([w, c], i) => {
    const t = raccoon({ coat: 0x5f6b3d, band: U.validator.color, hat: 0x46512c, scale: .72, glasses: i !== 2 });
    t.g.position.set(-1.85 + i * .78, 0, .55 + (i % 2) * .25); t.g.rotation.y = .12 - i * .08; scene.add(t.g); hit(t.g, 'validator', .9, 2.4);
    t.parts.armR.rotation.set(-2.75, 0, -.1);
    const sign = new THREE.Group(); sign.position.set(.3, 2.55, .25); t.g.add(sign);
    const stick = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, 1.1, 5), std(0x6b4a2a)); stick.position.y = -.55; sign.add(stick);
    const card = new THREE.Mesh(new THREE.PlaneGeometry(.95, .5), new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: .9, map: canvasTex(380, 200, (x, cw, ch) => {
      x.fillStyle = '#ece4cf'; x.fillRect(0, 0, cw, ch); x.strokeStyle = c; x.lineWidth = 9; x.strokeRect(18, 18, cw - 36, ch - 36);
      x.fillStyle = c; x.font = '700 64px "Courier Prime", "Courier New", monospace'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(w, cw / 2, ch / 2 + 4);
    }) }));
    card.position.set(0, .18, .04); card.rotation.z = (i - 1) * .06; card.castShadow = true; sign.add(card);
    placards.push({ arm: t.parts.armR, sign, phase: i * 1.3, head: t.parts.head });
  });

  // The Breakers: black coat, ear to the door, stethoscope on the dial.
  const br = raccoon({ coat: 0x16171b, band: U.breaker.color, hat: 0x0f1012, scale: 1.08 });
  br.g.position.set(.75, 0, -.35); br.g.rotation.y = .75; scene.add(br.g); hit(br.g, 'breaker', 1.1, 2.3);
  br.parts.armR.rotation.set(-1.45, .3, -.35); br.parts.armL.rotation.set(-.4, 0, .5);
  const stethEnd = new THREE.Vector3(SX - .55, SY - .1, -1.6 + .4);
  const stethMat = std(0x101114, { roughness: .4 });
  const steth = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, .1, 0)]), 2, .012, 5), stethMat); scene.add(steth);
  const chest = new THREE.Mesh(new THREE.CylinderGeometry(.07, .07, .04, 14), std(0xc9d1d6, { metalness: .8, roughness: .25, flatShading: false })); chest.rotation.x = Math.PI / 2; chest.position.copy(stethEnd); scene.add(chest);

  // Overwatch: up the stepladder in grey, binoculars sweeping the room.
  const ladder = new THREE.Group(); ladder.position.set(5.75, 0, -.4); scene.add(ladder);
  const metal = std(0x7d8a93, { metalness: .6, roughness: .4 });
  for (const s of [-1, 1]) for (const z of [-.35, .35]) { const leg = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, 2.6, 5), metal); leg.position.set(s * .32, 1.28, z * (1 - 0)); leg.rotation.x = z > 0 ? -.16 : .16; ladder.add(leg); }
  for (let k = 0; k < 5; k++) { const rung = new THREE.Mesh(new THREE.BoxGeometry(.66, .04, .12), metal); rung.position.set(0, .45 + k * .45, .35 - k * .07 + .02); ladder.add(rung); }
  const topStep = new THREE.Mesh(new THREE.BoxGeometry(.72, .06, .5), metal); topStep.position.set(0, 2.55, 0); topStep.castShadow = true; ladder.add(topStep);
  const ow = raccoon({ coat: 0x4c5157, band: U.orchestrator.color, hat: 0x2d3034, scale: .82 });
  ow.g.position.set(0, 2.58, 0); ow.g.rotation.y = -.6; ladder.add(ow.g); hit(ow.g, 'orchestrator', .9, 2);
  ow.parts.armR.rotation.set(-2.1, 0, .35); ow.parts.armL.rotation.set(-2.1, 0, -.35);
  const bino = new THREE.Group(); bino.position.set(0, .02, .33); ow.parts.head.add(bino);
  for (const s of [-1, 1]) { const tube = new THREE.Mesh(new THREE.CylinderGeometry(.055, .065, .2, 10), std(0x15161a, { metalness: .4, roughness: .4 })); tube.rotation.x = Math.PI / 2; tube.position.x = s * .08; bino.add(tube); const lens = new THREE.Mesh(new THREE.CircleGeometry(.05, 12), new THREE.MeshStandardMaterial({ color: 0xb79be7, emissive: 0x6a52a0, emissiveIntensity: .8 })); lens.position.set(s * .08, 0, .101); bino.add(lens); }

  // Labels: crew names, and what each one is saying.
  const label = (html, cls) => { const d = document.createElement('div'); d.className = `j3-tag ${cls}`; d.innerHTML = html; overlay.appendChild(d); return d; };
  const tags = [
    { el: label(`<span>Shh. Stream ${pick?.stream || '·'}.</span><b>${pickName || ''}</b><em>next firing <i data-countdown="breaker">--:--:--</i></em>`, 'bubble breaker'), obj: br.parts.head, off: new THREE.Vector3(0, .9, 0) },
    { el: label(`<span>Overwatch here.</span><b>${overwatchOwed} panel${overwatchOwed === 1 ? '' : 's'} owed.</b>`, 'bubble orchestrator'), obj: ow.parts.head, off: new THREE.Vector3(-.2, .9, 0) },
    { el: label(`<span>Found ${newPacks} new.</span><b>Filing them live.</b>`, 'bubble finder'), obj: pf2.parts.head, off: new THREE.Vector3(0, .85, 0) },
  ];
  for (const u of units) tags.push({ el: label(u.key === 'irregular' ? `${u.name}<small>definitely a human</small>` : u.name, `crew ${u.key}`), obj: { breaker: br.g, validator: null, orchestrator: ladder, finder: pf1.g, irregular: irr.g }[u.key] || scene, off: { breaker: new THREE.Vector3(0, -.12, .5), validator: new THREE.Vector3(-1.1, -.12, 1.1), orchestrator: new THREE.Vector3(0, -.12, .6), finder: new THREE.Vector3(0, -.12, .5), irregular: new THREE.Vector3(0, -.32, .6) }[u.key], below: true, world: u.key === 'validator' });

  // Camera: the whole room on a wide screen; on a narrow one, a pan across it.
  const camBase = new THREE.Vector3(0, 2.3, 10.5), look = new THREE.Vector3(0, 1.6, -.6);
  let pan = 1.1, wide = true, minPan = 0, maxPan = 0, drag = null, px = 0, py = 0;
  const hint = document.createElement('p'); hint.className = 'j3-hint mono'; hint.textContent = 'Drag to look around the room'; host.appendChild(hint);
  const resize = () => {
    const w = host.clientWidth, h = host.clientHeight;
    renderer.setSize(w, h, false); camera.aspect = w / h;
    // Fit 13.5 units of room across, or settle for 7 on a narrow screen and let it pan.
    const span = camera.aspect < 1.1 ? 7.2 : 13.5;
    camBase.z = (span / 2) / (Math.tan(THREE.MathUtils.degToRad(16)) * camera.aspect) - .6;
    wide = camera.aspect >= 1.1;
    maxPan = wide ? 0 : 3.6; minPan = wide ? 0 : -3.6;
    if (wide) pan = 0;
    look.y = wide ? 1.6 : 2.25; camBase.y = wide ? 2.3 : 2.75;
    hint.hidden = wide;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(host); resize();
  const cv = renderer.domElement;
  cv.style.touchAction = 'pan-y';
  cv.addEventListener('pointerdown', e => { drag = { x: e.clientX, pan, moved: false }; });
  addEventListener('pointerup', () => { drag = null; });
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  const crewAt = e => { const b = cv.getBoundingClientRect(); ndc.set(((e.clientX - b.left) / b.width) * 2 - 1, -((e.clientY - b.top) / b.height) * 2 + 1); ray.setFromCamera(ndc, camera); return ray.intersectObjects(crews, false)[0]?.object.userData.unit; };
  cv.addEventListener('pointermove', e => {
    const b = cv.getBoundingClientRect();
    px = ((e.clientX - b.left) / b.width - .5); py = ((e.clientY - b.top) / b.height - .5);
    if (drag) { const dx = e.clientX - drag.x; if (Math.abs(dx) > 4) drag.moved = true; if (!wide) pan = Math.max(minPan, Math.min(maxPan, drag.pan - dx * .012)); onUntip(); return; }
    if (e.pointerType === 'touch') return;
    const k = crewAt(e);
    cv.style.cursor = k ? 'pointer' : (wide ? 'default' : 'grab');
    if (k) onCrewTip(k, { left: e.clientX - 1, width: 2, top: e.clientY - 1, bottom: e.clientY + 1 }); else onUntip();
  });
  cv.addEventListener('pointerleave', () => { onUntip(); px = py = 0; });
  cv.addEventListener('click', e => { if (drag?.moved) return; const k = crewAt(e); if (k) onCrew(k); });

  let visible = true, last = performance.now(), dialAngle = dialTarget - 3.4, dialStart = null;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) { last = performance.now(); dialStart ??= last; requestAnimationFrame(frame); } }, { threshold: .05 }).observe(host);
  const v = new THREE.Vector3();

  function frame(now) {
    if (!visible || document.hidden) return;
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    const t = now / 1000;
    // Camera: a slow breathing drift, a little parallax under the pointer.
    const drift = reduced ? 0 : Math.sin(t * .15) * .25;
    camera.position.set(camBase.x + pan + drift + px * .6, camBase.y + py * -.3 + (reduced ? 0 : Math.sin(t * .2) * .08), camBase.z);
    camera.lookAt(look.x + pan * .92 + drift * .5, look.y, look.z);
    // The dial spins in on arrival, then the Breaker works it a click at a time around the pick.
    if (dialStart != null) {
      const e = Math.min(1, (now - dialStart) / 2600), ease = 1 - Math.pow(1 - e, 3);
      const work = reduced || e < 1 ? 0 : Math.round(Math.sin(t * .7) * 3) * .06;
      dialAngle = dialTarget - 3.4 * (1 - ease) + work;
    }
    dial.rotation.y = dialAngle; knob.rotation.y = dialAngle;
    // Steth tube from the Breaker's ear to the door.
    br.parts.head.updateWorldMatrix(true, false);
    const ear = br.parts.head.localToWorld(new THREE.Vector3(.2, -.05, .1));
    const mid = ear.clone().lerp(stethEnd, .5).add(new THREE.Vector3(0, -.55, .15));
    steth.geometry.dispose();
    steth.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3([ear, mid, stethEnd]), 20, .014, 5);
    if (!reduced) {
      br.parts.head.rotation.set(Math.sin(t * .9) * .04, .55, .28 + Math.sin(t * .6) * .05);
      br.parts.tail.rotation.y = Math.sin(t * 1.4) * .25;
      ow.parts.head.rotation.y = Math.sin(t * .35) * .7;
      ow.parts.tail.rotation.y = Math.sin(t * 1.1) * .3;
      irr.g.rotation.z = Math.sin(t * .8) * .025; irr.g.position.x = -5.6 + Math.sin(t * .8) * .03;
      peek.position.y = 1.45 + Math.max(0, Math.sin(t * .5)) * .05;
      const blink = (t % 5) < .12; peekEyes.forEach(e => { e.scale.y = blink ? .1 : 1; });
      for (const p of placards) { const b = Math.sin(t * 1.3 + p.phase); p.sign.position.y = 2.55 + b * .06; p.sign.rotation.z = b * .05; p.arm.rotation.x = -2.75 + b * .05; p.head.rotation.y = Math.sin(t * .5 + p.phase) * .15; }
      for (const d of drawers) if (d.open) d.d.position.z = d.base + .25 + Math.max(0, Math.sin(t * .9 + d.phase)) * .3;
      pf1.parts.armR.rotation.x = -1.3 + Math.sin(t * 2.2) * .25;
      pf2.parts.armR.rotation.x = -2.2 + Math.sin(t * 1.6) * .3;
      // Papers: out of the drawers in arcs, fluttering to the floor, and round again.
      for (const f of flying) {
        f.t = (f.t + dt * .16) % 1;
        const u = f.t, sx = -3.25 + f.side * .3;
        f.m.position.set(sx + f.side * u * 1.2 + Math.sin(u * 9 + f.seed) * .12, 1.6 + Math.sin(u * Math.PI) * 1.4 - u * 1.55, -.6 + u * 1.7);
        f.m.rotation.set(u * 9 + f.seed, u * 5, Math.sin(u * 7 + f.seed));
        f.m.visible = u < .96;
      }
      for (const l of lamps) if (l.on) l.m.material.color.setHSL(.07, .9, .58 + Math.sin(t * 2 + l.phase) * .06);
      // The lamp swings a little on its flex; the light swings with it.
      const sw = Math.sin(t * .6) * .06;
      shade.position.x = bulb.position.x = lampPos.x + sw; spot.position.x = lampPos.x + sw; beam.position.x = lampPos.x - .1 + sw * .6;
      spot.intensity = 70 * (1 + (Math.sin(t * 13) > .985 ? -.25 : 0));
      const p = dustGeo.attributes.position;
      dust.forEach((d, i) => { d.y += d.s * dt; if (d.y > 5) d.y = 0; d.a += dt * .05; p.setXYZ(i, lampPos.x + sw + Math.cos(d.a) * d.rr * (1 - d.y / 6), d.y, lampPos.z - .4 + Math.sin(d.a) * d.rr * (1 - d.y / 6)); });
      p.needsUpdate = true;
    }
    renderer.render(scene, camera);
    const W = host.clientWidth, H = host.clientHeight;
    for (const tg of tags) {
      if (tg.world) v.copy(tg.off); else { v.copy(tg.off); tg.obj.localToWorld(v); }
      v.project(camera);
      const x = (v.x * .5 + .5) * W, y = (-v.y * .5 + .5) * H;
      tg.el.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, ${tg.below ? '0' : '-100%'})`;
      tg.el.style.opacity = x < -40 || x > W + 40 ? 0 : 1;
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  return { renderer };
}
