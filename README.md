# CLT+

공공기관 공지사항 통합 뷰어 — Phase 1 (UI shell).

## Quickstart

```powershell
npm install
npm run dev
```

Open the printed URL. Pick a region in the left sidebar, expand it, click a sub-entity to see its source pages. The "최근 공지사항" panel is a placeholder until Phase 2.

## Regenerating `src/data/regions.json`

Whenever `list.xlsx` changes:

```powershell
python scripts/build_regions_json.py
```

Requires `openpyxl` (`pip install openpyxl`).

## Roadmap

- **Phase 1 (current)** — React + Vite UI shell. Regions/sub-entities/source-links rendered from `regions.json`. Deployed to GitHub Pages via `.github/workflows/deploy-pages.yml`.
- **Phase 2** — Per-source crawlers (`scrapers/<region>/<source>.py`) writing directly to a Supabase `notices` table. UI swaps `NoticePlaceholder` for a Supabase-backed list. Scheduled via a cron GitHub Action.

No DB schema design lives in this repo — the `notices` table is created in the Supabase dashboard. No API server, no auth, no embeddings — UI reads Supabase directly with the anon key.

## Live demo

After the first push to `main`, GitHub Pages serves the UI at:
`https://<owner>.github.io/clt-plus/`
