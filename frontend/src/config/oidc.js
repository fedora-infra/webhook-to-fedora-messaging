import { UserManager } from "oidc-client";

const oidcSettings = {
  authority: "https://id.stg.fedoraproject.org/openidc",
  client_id: "w2fm",
  redirect_uri: "https://w2fm.gridhead.net/callback",
  response_type: "code",
  scope: "openid email profile https://id.fedoraproject.org/scope/groups https://id.fedoraproject.org/scope/agreements",
  post_logout_redirect_uri: "https://w2fm.gridhead.net",
  monitorSession: true,
  loadUserInfo: true,
};

const userManager = new UserManager(oidcSettings);
export default userManager;
