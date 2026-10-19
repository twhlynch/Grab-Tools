# GRAB Tools

A level editing toolkit and statistics tracker for [GRAB](https://grabvr.quest).

Built with Vue 3, Vite, Tauri, Three.js, and CodeMirror.

## Setup

Requires `Node.js` 24 and `pnpm`.

```sh
pnpm install
```

## Development

Run the Vite website at `https://127.0.0.1:5173`:

```sh
pnpm dev
```

## Testing

```sh
pnpm test
```

Tests are in `test/` and use [Vitest](https://vitest.dev).

## Linting & Formatting

```sh
pnpm lint
pnpm format
```

Editor integration:

| Editor  | Config                                                                               |
| ------- | ------------------------------------------------------------------------------------ |
| VS Code | Install ESLint and Prettier extensions                                               |
| Neovim  | Setup `prettier` with a formatting plugin, and `vtsls` and `vue-language-server` lsp |

## Build

Build the website to `dist/`:

```sh
pnpm build
pnpm preview
```

## Code Generation

```sh
pnpm proto    # TypeScript types for protobuf
pnpm helpers  # json object builders
pnpm nodes    # node builders
```

## Shell Scripts

Development helper scripts in `scripts/`:

| Script                                | Description                         |
| ------------------------------------- | ----------------------------------- |
| `bump-version.sh major\|minor\|patch` | Bump the project version and commit |
| `build-tauri.sh`                      | Build the desktop app               |
| `build-android.sh`                    | Build the Android APK               |
| `publish-meta.sh`                     | Upload APK to Meta                  |
| `copy-lobbies.sh`                     | Copy lobbys from GRAB               |

## Environment Variables

| Variable         | Description                             |
| ---------------- | --------------------------------------- |
| `OVR_APP_ID`     | Meta/Oculus app ID (for deployment)     |
| `OVR_APP_SECRET` | Meta/Oculus app secret (for deployment) |

## Project Structure

```sh
.
├─ .github/          # github actions
├─ scripts/          # scripts for development
├─ public/           # public website assets
│  ├─ fonts/           # fonts
│  ├─ gasm/            # grab assembly samples
│  ├─ images/          # images
│  ├─ levels/          # levels for editor templates
│  └─ favicon.png      # website icon
├─ src/              # website sources
│  ├─ assets/          # built in assets
│  │  ├─ bookmarklets/   # javascript bookmarklet sources
│  │  ├─ models/         # level models
│  │  ├─ proto/          # level protobuf definition
│  │  ├─ shaders/        # editor shaders
│  │  ├─ textures/       # level textures
│  ├─ common/          # common js & ts code
│  ├─ components/      # vue components
│  │  ├─ EditorPanels/   # components for the json editor
│  │  └─ tools/          # components for tools
│  ├─ editor/          # editor code
│  ├─ generated/       # generated helper functions and types
│  ├─ icons/           # vue svg icon components
│  ├─ layouts/         # vue layout components
│  ├─ pages/           # vue page components
│  ├─ requests/        # fetch requests
│  ├─ stores/          # vue session stores
│  ├─ styles/          # css source
│  ├─ tools/           # tool sources
│  ├─ types/           # global types
│  ├─ App.vue          # vue app structure
│  ├─ config.ts        # general config / globals
│  ├─ main.ts          # website entrypoint
│  └─ router.ts        # vue router config
├─ src-tauri/          # tauri rust application sources
├─ test/               # unit tests
├─ vite/               # vite plugins
├─ .env.example        # example env config
├─ .gitattributes      # git attributes
├─ .gitignore          # gitignore
├─ .nvim.lua           # optional nvim config
├─ .nvmrc              # pinned node version
├─ .prettierignore     # prettier ignore config
├─ .prettierrc.json    # prettier formatting config
├─ CONTRIBUTING.md     # contribution guide
├─ README.md           # this file
├─ eslint.config.ts    # eslint config
├─ index.html          # mountable app html
├─ package.json        # package config and dependencies
├─ pnpm-lock.yaml      # pnpm packages lock file
├─ pnpm-workspace.yaml # pnpm settings
├─ tsconfig.json       # typescript config
├─ vite.config.ts      # vite config
└─ vitest.config.ts    # vitest config
```
