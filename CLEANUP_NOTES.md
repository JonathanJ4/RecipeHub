# Cleanup Notes

## Completed Cleanup

- Removed the superseded Python/Flask/static application and obsolete root frontend files.
- Removed Vite starter assets and dead starter CSS that were not referenced by the active application.
- Removed tracked dependency directories and added ignore coverage for dependency, build, environment, log, Python cache, coverage, and common OS-generated files.
- Removed the accidental Vite import from the Mongoose recipe model.
- Added a placeholder-only `server/.env.example`; the local `server/.env` remains ignored and untracked.
- Verified tracked source contains no obvious AWS keys, credentialed MongoDB URIs, API keys, bearer tokens, private keys, or similar committed credentials.
- Verified all declared frontend and backend dependencies are used directly or by the existing build/configuration pipeline.

## Deferred Refactoring

- Express routes and application startup currently live together in `server/index.js`.
- Frontend API URL handling, fetch calls, and error handling are duplicated across components.
- Recipe search happens client-side after the full recipe collection is fetched.
- The recipe creation endpoint does not have request validation, and backend error handling is minimal.
- The frontend uses a hard-coded localhost API fallback.
- Automated tests are not currently present.
- Dependency installation currently reports audit findings (16 frontend and 4 backend vulnerabilities); dependency upgrades were intentionally left for a separate task.
- The MongoDB/Mongoose architecture is intentionally preserved pending a later, separately scoped migration.
- `server/public/images/` contains 13,582 tracked files (about 202 MiB). These assets were preserved because the seed and S3 upload workflows rely on the local recipe image corpus; redundancy should be assessed separately before removal.

## Future Architecture

Planned separately: React → FastAPI → PostgreSQL/pgvector → RAG → LangChain → LangGraph → Voice.
