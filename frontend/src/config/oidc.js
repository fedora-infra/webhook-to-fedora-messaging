import { UserManager } from "oidc-client";
import { hostname } from "./data.js";

const oidcSettings = {
  authority: "https://id.stg.fedoraproject.org/openidc",
  client_id: "w2fm",
  redirect_uri: `https://${hostname}/callback`,
  response_type: "code",
  scope: "openid email profile https://id.fedoraproject.org/scope/groups https://id.fedoraproject.org/scope/agreements",
  post_logout_redirect_uri: `https://${hostname}/`,
  monitorSession: true,
  loadUserInfo: true,
};

export const userManager = new UserManager(oidcSettings);
