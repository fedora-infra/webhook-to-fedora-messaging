/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BASE_URL: string
  readonly VITE_OIDC_PROVIDER_URL: string
  readonly VITE_OIDC_CLIENT_ID: string
  readonly VITE_API_URL: string
  // add other env variables here as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}