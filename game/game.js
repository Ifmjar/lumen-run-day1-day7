// Lumen Run — a tiny auto-runner my AI agent built, then updated daily for a week.
// Day 1: a grey square, one coin, flat ground. Day 7: same map, same start —
// sky, sun, clouds, hills, trees, flowers, eight coins, spikes, particles, HUD.
// Open game/index.html, or add ?day=7 for the day-seven build. Tap / Space to jump.
(() => {
  'use strict';
  const params = new URLSearchParams(location.search);
  const DAY = params.get('day') === '1' ? 1 : 7;
  const W = 1080, H = 1920, GROUND_Y = 1250, START_X = 180, SPEED = 140;
  const canvas = document.getElementById('game');
  canvas.width = W; canvas.height = H;
  const ctx = canvas.getContext('2d');

  // The level never changes between builds: same map, same start, same finish.
  const LEVEL = {
    gap: { x0: 480, x1: 560 },
    spikes: DAY === 7 ? [{ x: 700 }] : [],
    coins: DAY === 7
      ? [300, 400, 500, 600, 860, 900, 940].map(x => ({ x, y: 1130, got: false }))
      : [{ x: 600, y: 1130, got: false }],
    flagX: 1000,
  };
  const TREES = DAY === 7 ? [120, 340, 640, 900] : [];
  const FLOWERS = DAY === 7 ? [220, 420, 560, 760, 940] : [];

  const player = { x: START_X, y: 0, vy: 0, jumping: false, score: 0, dead: false, won: false };
  let t = 0, last = performance.now(), trail = [], confetti = [];

  function jump() {
    if (!player.jumping && !player.dead && !player.won) {
      player.vy = -760; player.jumping = true;
    }
  }
  addEventListener('keydown', e => { if (e.code === 'Space' || e.code === 'ArrowUp') jump(); });
  canvas.addEventListener('pointerdown', jump);

  function sky() {
    if (DAY === 1) { ctx.fillStyle = '#c9c9c9'; ctx.fillRect(0, 0, W, GROUND_Y); return; }
    const g = ctx.createLinearGradient(0, 0, 0, GROUND_Y);
    g.addColorStop(0, '#7ec8f7'); g.addColorStop(1, '#dff3ff');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, GROUND_Y);
    ctx.fillStyle = '#ffd94d'; ctx.beginPath(); ctx.arc(880, 220, 90, 0, 7); ctx.fill();
    ctx.fillStyle = '#ffffff';
    for (const [cx, cy] of [[220, 260], [520, 180], [800, 320]]) {
      ctx.beginPath(); ctx.ellipse(cx, cy, 90, 34, 0, 0, 7); ctx.fill();
    }
    ctx.fillStyle = '#8fce6e';
    ctx.beginPath(); ctx.ellipse(200, GROUND_Y, 320, 120, 0, Math.PI, 0); ctx.fill();
    ctx.beginPath(); ctx.ellipse(880, GROUND_Y, 360, 140, 0, Math.PI, 0); ctx.fill();
  }

  function ground() {
    ctx.fillStyle = DAY === 1 ? '#8a8a8a' : '#5da24a';
    ctx.fillRect(0, GROUND_Y, W, H - GROUND_Y);
    ctx.fillStyle = DAY === 1 ? '#777' : '#4c8a3d';
    // The gap: a hole in the ground both builds must jump.
    ctx.fillStyle = DAY === 1 ? '#c9c9c9' : '#dff3ff';
    ctx.fillRect(LEVEL.gap.x0, GROUND_Y, LEVEL.gap.x1 - LEVEL.gap.x0, 260);
    ctx.fillStyle = DAY === 1 ? '#6f6f6f' : '#3e7a33';
    ctx.fillRect(LEVEL.gap.x0 - 6, GROUND_Y, 6, 260);
    ctx.fillRect(LEVEL.gap.x1, GROUND_Y, 6, 260);
  }

  function decor() {
    if (DAY === 1) return;
    for (const x of TREES) {
      ctx.fillStyle = '#7a4a21'; ctx.fillRect(x - 12, GROUND_Y - 170, 24, 170);
      ctx.fillStyle = '#2f9e44'; ctx.beginPath(); ctx.arc(x, GROUND_Y - 210, 70, 0, 7); ctx.fill();
    }
    for (const x of FLOWERS) {
      ctx.fillStyle = '#ff6b9d'; ctx.beginPath(); ctx.arc(x, GROUND_Y - 24, 12, 0, 7); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, GROUND_Y - 24, 5, 0, 7); ctx.fill();
    }
  }

  function drawCoins() {
    for (const c of LEVEL.coins) {
      if (c.got) continue;
      ctx.fillStyle = '#ffcf3d'; ctx.beginPath(); ctx.arc(c.x, c.y, 26, 0, 7); ctx.fill();
      ctx.fillStyle = '#c8930a'; ctx.font = 'bold 30px sans-serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText('$', c.x, c.y + 1);
    }
  }

  function drawSpikes() {
    for (const s of LEVEL.spikes) {
      ctx.fillStyle = '#3d3d3d';
      ctx.beginPath(); ctx.moveTo(s.x - 26, GROUND_Y); ctx.lineTo(s.x, GROUND_Y - 64);
      ctx.lineTo(s.x + 26, GROUND_Y); ctx.closePath(); ctx.fill();
    }
  }

  function drawFlag() {
    ctx.fillStyle = '#333'; ctx.fillRect(LEVEL.flagX, GROUND_Y - 220, 8, 220);
    ctx.fillStyle = '#ff5964';
    ctx.beginPath(); ctx.moveTo(LEVEL.flagX + 8, GROUND_Y - 220);
    ctx.lineTo(LEVEL.flagX + 110, GROUND_Y - 185); ctx.lineTo(LEVEL.flagX + 8, GROUND_Y - 150);
    ctx.closePath(); ctx.fill();
  }

  function drawPlayer() {
    const px = player.x, py = GROUND_Y - 70 + player.y;
    if (DAY === 7) {
      for (const p of trail) {
        ctx.globalAlpha = p.a; ctx.fillStyle = '#ffd94d';
        ctx.beginPath(); ctx.arc(p.x, p.y, 14, 0, 7); ctx.fill();
      }
      ctx.globalAlpha = 1;
    }
    ctx.fillStyle = DAY === 1 ? '#555555' : '#ff5964';
    ctx.fillRect(px - 34, py - 34, 68, 68);
    ctx.fillStyle = '#fff';
    ctx.fillRect(px + 6, py - 20, 14, 14); ctx.fillRect(px + 24, py - 20, 14, 14);
    ctx.fillStyle = '#111';
    ctx.fillRect(px + 11, py - 15, 6, 6); ctx.fillRect(px + 29, py - 15, 6, 6);
  }

  function hud() {
    ctx.fillStyle = DAY === 1 ? '#555' : '#123';
    ctx.font = 'bold 54px sans-serif'; ctx.textAlign = 'left'; ctx.textBaseline = 'top';
    ctx.fillText(DAY === 1 ? 'DAY 1' : 'DAY 7', 48, 48);
    if (DAY === 7) {
      ctx.font = 'bold 44px sans-serif';
      ctx.fillText('SCORE ' + player.score, 48, 130);
      ctx.textAlign = 'right';
      ctx.fillText('COINS ' + LEVEL.coins.filter(c => c.got).length + '/' + LEVEL.coins.length, W - 48, 48);
      ctx.textAlign = 'left';
    }
    if (player.won) {
      ctx.fillStyle = '#123'; ctx.font = 'bold 72px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText('FINISH!', W / 2, 620);
    }
  }

  function step(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now; t += dt;
    if (!player.dead && !player.won) {
      player.x = Math.min(LEVEL.flagX, START_X + SPEED * t);
      if (player.jumping) {
        player.vy += 2200 * dt; player.y += player.vy * dt;
        if (player.y >= 0) { player.y = 0; player.vy = 0; player.jumping = false; }
      }
      if (DAY === 7) {
        trail.push({ x: player.x - 40, y: GROUND_Y - 70 + player.y, a: 0.7 });
        if (trail.length > 14) trail.shift();
        for (const p of trail) p.a -= dt * 1.4;
      }
      for (const c of LEVEL.coins) {
        if (!c.got && Math.abs(player.x - c.x) < 46 && player.y > -120) { c.got = true; player.score += 100; }
      }
      const overGap = player.x > LEVEL.gap.x0 - 30 && player.x < LEVEL.gap.x1 + 30;
      if (overGap && player.y === 0) player.dead = true;
      for (const s of LEVEL.spikes) {
        if (Math.abs(player.x - s.x) < 40 && player.y > -70) player.dead = true;
      }
      if (player.x >= LEVEL.flagX) {
        player.won = true;
        if (DAY === 7) for (let i = 0; i < 90; i++) confetti.push({
          x: LEVEL.flagX + (Math.random() - 0.5) * 500, y: 500 + Math.random() * 200,
          vx: (Math.random() - 0.5) * 260, vy: 60 + Math.random() * 220,
          c: ['#ff5964', '#ffd94d', '#4dabff', '#51e07a'][i % 4],
        });
      }
    }
    if (player.won && DAY === 7) {
      for (const p of confetti) { p.x += p.vx * dt; p.y += p.vy * dt; }
    }
    sky(); ground(); decor(); drawFlag(); drawCoins(); drawSpikes(); drawPlayer();
    if (player.won && DAY === 7) {
      for (const p of confetti) { ctx.fillStyle = p.c; ctx.fillRect(p.x, p.y, 12, 18); }
    }
    hud();
    if (player.dead) {
      ctx.fillStyle = '#123'; ctx.font = 'bold 64px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText('OUCH — tap to retry', W / 2, 620);
    }
    requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
})();
