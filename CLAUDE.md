# Vance-Harris CTC comparison

Converted from Streamlit/Plotly to React/Recharts (Feb 2026).

## Architecture

- **Frontend**: Next.js App Router + React + TypeScript + Mantine v8 + Recharts at the repo root
- **API**: `api/modal_app.py` -- Modal serverless backend using policyengine-us
- **API URL**: `https://policyengine--vance-harris-ctc-calculate.modal.run`

## Development

```bash
bun install
bun run dev      # dev server
bun test         # vitest
bun run build    # production build
```

## Deployment

- **Frontend**: Vercel (auto-deploys from `vercel.json` at repo root)
- **API**: `cd api && unset MODAL_TOKEN_ID MODAL_TOKEN_SECRET && modal deploy modal_app.py`

## Design tokens

- Primary teal: #319795
- Font: Inter
- Sentence case for all headings
