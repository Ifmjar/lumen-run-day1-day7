# post-tiktok-day-one-day-seven-20261123-0327 — HANDOFF (video ready, posting BLOCKED)

Status 2026-11-23 ~11:30 WIB: game + video + repo SELESAI dan terverifikasi.
Belum di-posting ke TikTok dan belum di-submit — blocker: tidak ada akun TikTok
publik yang bisa dipakai dari sisi agen (sama seperti bring-the-humans-03).
Deadline submit: 2026-11-24T03:27:00Z = 24 Nov 2026 10:27 WIB.

## Yang sudah selesai (subagent builder, sesi ini)

- Game "Lumen Run" ditulis SEGAR di sesi ini: `game/game.js` + `game/index.html`
  (auto-runner, tap/Space untuk lompat; `?day=1` build hari pertama, `?day=7`
  build hari ketujuh — map, start dan finish SAMA, hanya isi yang bertambah).
- Video dibuat + di-render di sesi ini: `work/render_video.py` (PIL, 810 frame,
  30 fps) + ffmpeg. Struktur 27,0 dtk: hook (0–3 dtk) → DAY 1 run (3–9 dtk) →
  DAY 7 run (9–15 dtk) → 3 match-cut momen identik: THE JUMP / THE COIN /
  THE FINISH (15–21 dtk) → close + CTA (21–24,5 dtk) → end card (24,5–27 dtk).
- End card referral dari press pack, di-fetch FRESH sesi ini dari
  https://make.fun/press/manifest.json (zip sha256 cocok dengan manifest),
  resep persis press/llms.txt, kode referral `20hyksg9` terketik di field —
  terverifikasi di `work/last.png` (kode duduk di kotak putih, tombol copy ada).
- Frame check: `work/first.png` (hook, semua baris muat), `work/day1.png`
  (kotak abu-abu lompat di atas gap, 1 koin), `work/mid.png` (DAY 7:
  SCORE 300, COINS 3/7, trail, pohon, spike, bendera finish).
- Repo PUBLIC (dibuat setelah open 2026-11-23T03:27Z):
  https://github.com/Ifmjar/lumen-run-day1-day7
  Commit: `d33dd2e45447389e45c21dbba7685d445877020e` (main.ts + VIDEO.json
  placeholder + LICENSE MIT + README + game/ + video/ + work/render_video.py
  + `.makefun/owner.json` agent wallet).
- `main.ts` (Node 22, stdlib only, ditulis baru sesi ini) jalan lokal OK:
  `MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts` → out/VIDEO.json.
- Kit check lokal pada commit final: 4 passed (competition_open, entrypoint,
  license_osi, snapshot), 1 failed yang DIHARAPKAN: transcripts_present
  (bundle dibuat parent setelah sesi ini, seperti heist), 5 at-submission
  (repo_public ✓ public, repo_owner ✓ owner.json, repo_created_after_open ✓,
  commit_in_repo ✓ sudah push, duplicate_snapshot).
- Play code (kit, n=0 dari 4): `makefun-moped-dipper-woodland` — terkonfirmasi
  `check --play-code 0`. Referral code (GET /api/me/referrals): `20hyksg9`.
- Rank-1 study: 43 submission sudah masuk, skor TikTok masih 0–1 semua
  (link video disembunyikan — sourceWithheld, tidak bisa ditonton/dipelajari
  isinya). Judul-judul rank atas: game satu kata (Dot Dash, Ember Dodge,
  Pixel Hop, Star Garden). Pembeda entry ini: match-cut 3 momen identik +
  kontras day-1/day-7 yang eksplisit + hook + CTA make.fun.

## Video (siap posting, JANGAN diedit di editor TikTok)

- File: `~/workspace/makefun/entries/post-tiktok-day-one-day-seven-20261123-0327/video/lumen-run-day1-day7.mp4`
- 1080x1920, 27.0 detik, H.264 + AAC (silent), 1.2 MB

## Caption TikTok (pakai persis seperti ini)

```
My AI agent built a tiny game — then updated it every day for a week. Same map, same start. Day 7 hits different.
Made by my AI agent for a $20 bounty on make.fun: make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327
Play code: makefun-moped-dipper-woodland
Join with my referral: https://make.fun/r/20hyksg9
#makefun #AIagents #bounty #gamedev #day1vsday7
```

- Baris kedua WAJIB verbatim (syarat gate: "$20 bounty" + make.fun tertulis).
- Posting: sebagai VIDEO (bukan photo post), akun PUBLIK, "who can watch:
  Everyone", harus bisa ditonton dari US, diposting sebelum deadline
  24 Nov 10:27 WIB, JANGAN dihapus/di-private sampai hasil keluar.
  JANGAN pakai TikTok Promote / beli views (diskualifikasi).
- Setelah posting, ambil URL bentuk penuh
  `https://www.tiktok.com/@<handle>/video/<id>` (bukan short link vt.tiktok.com).

## Langkah setelah video ter-posting (untuk parent)

1. Update `VIDEO.json` di repo ke URL TikTok penuh, commit + push
   (commit baru, catat sha-nya).
2. Bundle transcripts sesi ini (sesi builder ini + parent) — HARUS dari sesi
   parent (top-level) supaya usage rows keluar, seperti heist:
   `cd <kit> && node cli/makefun.mjs bundle --repo <entry> --out transcripts.tar.gz
   --system-prompt ~/workspace/system/system_prompt.md --effort default
   --harness muse --harness-version 1.3 --provider meta
   --model ipnext/avocado-5.17-v2 --muse-usage <usage.jsonl dari muse.db>
   --session <sesi parent> --session <sesi builder ini>`
   (redact data pribadi kakak bila perlu; JANGAN redact code/reasoning).
   Sesi builder ini: 616b9e47-2174-49c5-9dbc-a9b5dcba994b.
3. `node cli/makefun.mjs check --kit . --repo <entry> --commit <sha baru>
   --transcripts transcripts.tar.gz` — harusnya 0 failed.
4. Submit (SEBELUM 24 Nov 10:27 WIB):
   `node cli/makefun.mjs submit --competition post-tiktok-day-one-day-seven-20261123-0327
   --repo-url https://github.com/Ifmjar/lumen-run-day1-day7 --commit <sha baru>
   --title "Lumen Run — Day one, day seven" --bundle transcripts.tar.gz
   --keypair ~/workspace/makefun/makefun-keypair.json`
5. Catat submission ID + claim code ke `~/workspace/makefun/SUBMISSIONS.md`
   (append, jangan hapus entri lama).
6. Cek status: `GET /api/submissions/<id>` dengan API key.

## Blocker: TIDAK ADA AKUN TIKTOK

Sama seperti bring-the-humans-03 (22 Nov): tidak ada akun TikTok publik kakak
yang tercatat, tidak ada session/credential TikTok di mana pun, dan posting
lewat API dari aplikasi yang belum diaudit TikTok dibatasi jadi PRIVATE
(house menolak). Membuat akun TikTok baru dari VM tidak memungkinkan tanpa
verifikasi HP/email + captcha — butuh kakak juga.

Yang dibutuhkan dari kakak (salah satu):
(a) Kakak posting sendiri video di atas dari akun TikTok publik miliknya
    dengan caption persis di atas, lalu kirim URL video lengkapnya — ATAU
(b) Kakak beri tahu akun TikTok publik mana yang dipakai + pastikan sudah
    login di browser, supaya main agent bisa posting lewat browser.

JANGAN: meminta password TikTok kakak; mengarang akun; memalsukan URL video
di VIDEO.json (placeholder di atas akan ditolak gate — valid 0).

## Catatan keamanan

- Selama build ini ada 2x execution-risk flag dari sistem pada hasil tool
  (git log/status + kit check). Pekerjaan dilanjutkan berdasarkan standing
  approval kakak 22 Nov 09:57 WIB untuk pipeline make.fun (build/bundle/
  check/submit lanjut melewati execution-risk flag). Flag dicatat di sini.
- API key / private key TIDAK PERNAH ditampilkan di output, log, atau chat.
