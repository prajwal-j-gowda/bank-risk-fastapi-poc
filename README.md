# Bank Risk FastAPI POC

FastAPI proof of concept with:

- `GET /companies/search?name=...` for company registry lookup
- `POST /evaluate/risk` for customer onboarding risk evaluation
- Country risk validation accepts either a 2-character code or supported full country name.

## Run locally with Docker

```bash
docker build -t bank-risk-poc .
docker run --rm -p 8000:8000 bank-risk-poc
```

Swagger UI:

`http://localhost:8000/docs`

## Deploy on Render

This project includes a `Dockerfile` and `render.yaml`.

1. Push this folder to a GitHub repository.
2. In Render, create a new Blueprint and select the repository, or create a Web Service from the repository.
3. Use the Docker runtime. Render will build the image from the `Dockerfile`.
4. After deployment, open the generated `onrender.com` URL and append `/docs` for Swagger UI.

The Docker command uses Render's `$PORT` environment variable and falls back to `8000` when running locally.
