# npm Troubleshooting (NodeSource apt installs)

When Node.js is installed via the **NodeSource apt package**, npm is bundled
inside the `nodejs` deb and lives at `/usr/bin/npm` /
`/usr/lib/node_modules/npm`. This causes two recurring issues.

## 1. `npm install -g npm@<version>` fails

npm cannot overwrite itself because dpkg owns the files.

**Fix:** upgrade Node (which bundles npm) through apt:

```bash
apt update && apt upgrade nodejs
```

## 2. Global package install fails with ENOTEMPTY

```
ENOTEMPTY: directory not empty, rename '…/codex' -> '…/.codex-XCNbUSl9'
```

A previous failed install left a temp directory (`.package-<random>`) that
blocks the rename on retry.

**Fix:** remove the leftover temp dir and retry:

```bash
rm -rf /usr/lib/node_modules/<scope>/.<package>-*   # e.g. @openai/.codex-*
npm install -g <package>
```

## Notes

- The npmmirror registry (`registry.npmmirror.com` in `~/.npmrc`) is unrelated
  to both issues, though it can lag a few hours behind the official registry for
  brand-new releases.
- If a global install fails for any reason, always check
  `/usr/lib/node_modules/` for leftover `.<name>-<hash>` directories before
  retrying.
