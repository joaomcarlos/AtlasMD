#!/usr/bin/env bash
# Syncs AI skill assets into the atlasmd-scaffold consumer template.
# Run from the repo root: ./sync-skills.sh

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

# Copies are read-only so edits land on the source, not the synced copies.
cp -f atlasmd-doc-standards/DOCUMENTATION-STANDARD.md ai/skills/atlasmd-docs/DOCUMENTATION-STANDARD.md
chmod a-w ai/skills/atlasmd-docs/DOCUMENTATION-STANDARD.md

cp -Rf ai/skills/. atlasmd-scaffold/.agents/skills/
find atlasmd-scaffold/.agents/skills -type f -exec chmod a-w {} +

echo "Sync complete. Files are read-only in the scaffold to prevent accidental edits."