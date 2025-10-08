import { UserManager } from "oidc-client";

const redirectUri:string = new URL(`${import.meta.env.BASE_URL}callback`, window.location.href).href;
const oidcSettings = {
  authority: import.meta.env.VITE_OIDC_PROVIDER_URL,
  client_id: import.meta.env.VITE_OIDC_CLIENT_ID,
  redirect_uri: redirectUri,
  response_type: "code",
  scope: "openid email profile https://id.fedoraproject.org/scope/groups https://id.fedoraproject.org/scope/agreements",
  post_logout_redirect_uri: new URL("/", window.location.href).href,
  monitorSession: true,
  loadUserInfo: true,
};

export const userManager: UserManager = new UserManager(oidcSettings);
