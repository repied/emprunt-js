# Emprunt

- Simple mortgage simulation app
- Python backend (using `pip`, no virtual env)
- HTML CSS FastAPI + Jinja2 frontend
- VSCode Devcontainer with a dockerFile
- `uvicorn` as the dev server
- `pytest` for dev test
- Deployed on Google Cloud Run as a docker container (PROJECT_ID is `emprunt`)

## Develop in devcontainer
1. Open this folder in VS Code WSL and click **Reopen in Container** when prompted, or use the command palette: `Remote-Containers: Reopen in Container`.
   In the container, dependencies should already be installed by `postCreateCommand`
2. Test with dev server: `make dev`. Open your browser to `http://localhost:8000` (port forwarded by devcontainer).
4. Run unit test `make test` or within VsCode testing UI.

## Publishing
Pushing to Github `main` branch will trigger a build and deploy thanks to the Google Cloud Build github app.

Url can be found on `Google Cloud Console > Cloud run > Services > emprunt-app`

Visit https://emprunt-app-491369944224.europe-west1.run.app/simulate

Alternatively gcloud CLI is installed in the devcontainer to manully build and publish
