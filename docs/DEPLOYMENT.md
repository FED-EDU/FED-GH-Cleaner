# Deployment

## GitHub Pages

Enable Pages from the `main` branch root, or use `.github/workflows/pages.yml`.

## Cloudflare Pages

Use production branch `main`, leave the build command blank, and run `npx wrangler deploy --assets=.`. The `CNAME` file documents the intended custom domain.
