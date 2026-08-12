# Cleanup Notes

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
