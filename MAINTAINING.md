# Maintain the distribution

The product repository owns every file under `skills/`. Do not hand-edit those files here. Improve a skill at its product source, release it through the normal product process, then refresh this package at that exact released commit.

```sh
python3 scripts/sync_from_product.py --source /path/to/oxygen --ref FULL_RELEASED_COMMIT_SHA
python3 scripts/check.py
```

The exporter uses an explicit allowlist, reads only files named in each product skill manifest, preserves their bytes and records SHA-256 hashes in `SOURCE.json`. It also copies the existing product plugin license. It rejects obsolete bundle files instead of silently retaining them. Review any allowlist change against customer availability before publication.

Before publishing a new snapshot:

1. Confirm that the source revision is released and that every included capability is appropriate for customers.
2. Run the package checker and a secret scan. Review privacy-sensitive examples and embedded context.
3. Install from a clean temporary project for each advertised agent. Check that supporting references arrive with the entrypoints.
4. Verify the first free-read prompt with an authorized workspace when account access permits. Never call paid providers or send outreach as an installation test.
5. Keep the account, credit and client requirements clear in the README. Preserve the existing license terms and prior-rights clarification.

The exporter performs no login, API call, automatic update, publication or deployment. Publication is a separate maintainer action.
