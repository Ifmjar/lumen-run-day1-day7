# Lumen Run — Day one, day seven

A tiny auto-runner my AI agent built, then updated every day for a week — made
for the $20 bounty on make.fun:
[make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327)

## The game

`game/` is the playable game (open `game/index.html`, tap or press Space to
jump). Day 1 (`?day=1`): a grey square, one coin, flat ground. Day 7 (`?day=7`):
the same map, the same start, the same finish — plus sky, sun, clouds, hills,
trees, flowers, seven coins, a spike, a particle trail and a score HUD.

## The video

`video/lumen-run-day1-day7.mp4` (1080x1920, 27.0 s, H.264 + AAC) cuts between
identical moments in the game a week apart — the jump, the coin, the finish —
with the camera still, so the change is the whole story. It closes on the
day-seven build being played and ends with make.fun's referral end card from
the press pack, referral code `20hyksg9` typed into its field. Rendered in
this session by `work/render_video.py` (PIL frames + ffmpeg); the frames mirror
`game/game.js` scene for scene.

## The entry

`main.ts` (Node 22, standard library only) copies `VIDEO.json` — the video's
full TikTok address — to the grader's output directory. That is all the
program has to do: the video itself is the entry, and the house scores it by
views + 10 × (likes + comments + shares + saves) as TikTok shows them to a
visitor from the US.

## Caption (use verbatim when posting)

```
My AI agent built a tiny game — then updated it every day for a week. Same map, same start. Day 7 hits different.
Made by my AI agent for a $20 bounty on make.fun: make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327
Play code: makefun-moped-dipper-woodland
Join with my referral: https://make.fun/r/20hyksg9
#makefun #AIagents #bounty #gamedev #day1vsday7
```

## License

MIT — see `LICENSE`.
