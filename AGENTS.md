# Tube Archivist Agent Guide

## Scope
- This file applies to the entire repository unless a deeper `AGENTS.md` overrides it.

## Project Shape
- `backend/` contains the Django backend, split by app (`appsettings`, `channel`, `common`, `download`, `playlist`, `stats`, `task`, `user`, `video`).
- `frontend/` contains the React + TypeScript + Vite frontend.
- `docker-compose.yml`, `Dockerfile`, and `docker_assets/run.sh` describe the containerized runtime and startup flow.
- `README.md`, `backend/README.md`, and `CONTRIBUTING.md` are the primary sources for repo conventions and local development workflow.

## Working Style
- Keep changes focused and consistent with the existing app boundaries; avoid cross-cutting refactors unless the task requires them.
- Prefer fixing behavior at the source instead of adding compatibility shims or duplicate logic.
- Follow existing naming, file placement, and import patterns in the area you are touching.
- Do not introduce new frameworks, build tools, or alternative local setup flows unless explicitly requested.

## Backend Guidance
- Run backend commands from `backend/`.
- Use the existing Django app structure: API changes usually involve matching updates in `urls.py`, `views.py`, and `serializers.py`, with `models.py` changes only when data shape actually changes.
- Reuse helpers and base classes from `backend/common/` where possible instead of re-implementing shared Elasticsearch, Redis, auth, or pagination behavior.
- Keep docstrings and module-level structure aligned with the current backend style.
- The backend depends on Redis and Elasticsearch; native development commonly runs those services in containers.

## Frontend Guidance
- Run frontend commands from `frontend/`.
- Prefer existing abstractions for API access, routing, configuration, and state management before adding new ones.
- Place reusable UI in `frontend/src/components/`, route-level screens in `frontend/src/pages/`, shared helpers in `frontend/src/functions/`, and zustand state in `frontend/src/stores/`.
- Keep TypeScript strictness intact and follow the current functional React style.
- Use the existing linting and formatting setup rather than ad hoc styling changes.

## Validation
- Start with the smallest relevant validation for the files changed.
- Frontend checks:
  - `npm run lint`
  - `npm run build`
- Frontend formatting:
  - `npm run format`
- Backend checks:
  - `python manage.py check`
  - Run targeted Django tests if the task adds or changes tests.
- Use broader container validation with `docker compose up --build` only when the task depends on full-stack behavior.

## Local Development
- Backend setup uses `requirements-dev.txt`; see `CONTRIBUTING.md` for the expected `.env` values and native dev flow.
- Start the backend with `python manage.py runserver` from `backend/`.
- Start the frontend with `npm install` then `npm run dev` from `frontend/`.
- Refer to `docker_assets/run.sh` when backend startup behavior, migrations, or Celery worker expectations matter.

## Pull Requests
- If the user asks for branch or PR guidance, target the `develop` branch as described in `CONTRIBUTING.md`.
