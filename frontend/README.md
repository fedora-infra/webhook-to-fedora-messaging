# W2FM UI

The setup is admittedly wild. There is a lot of moving parts here, including
the frontend, the backend and the identity provider.

If you follow the instructions to the word and keep your common sense about,
you should be able to get this thing started in no time.

## For development

1.  Follow the instructions on the
    [backend documentation](https://github.com/fedora-infra/webhook-to-fedora-messaging/blob/main/README.md)
    to get it started.

2.  Take note of the host and the port on which the backend service is running.

3.  Install `npm` if it is not installed already.

    ```
    $ sudo dnf install npm --setopt=install_weak_deps=False
    ```

4.  In a separate terminal session, navigate into the `frontend` directory.

    ```
    $ cd frontend
    ```

5.  Ensure that the runtime dependencies for the frontend are installed.

    ```
    $ npm install
    ```

    For example,

    ```
    added 464 packages, and audited 465 packages in 43s

    188 packages are looking for funding
      run `npm fund` for details

    found 0 vulnerabilities
    ```

6.  Ensure that the backend service is accessible from the device.

    ```
    $ curl -i http://localhost:5000
    ```

    For example,

    ```
    HTTP/1.1 307 Temporary Redirect
    date: Mon, 21 Jul 2025 06:26:03 GMT
    server: uvicorn
    content-length: 0
    location: /docs
    ```

7.  Edit the `package.json` file to point to the backend service.

    ```
    $ nano package.json
    ```

    For example,

    ```
    "proxy": "http://localhost:5000/",
    ```

8.  Edit the `data.js` file to reflect the reachable hostname.

    ```
    $ nano src/config/data.js
    ```

    For example,

    ```
    export const hostname = "w2fm.gridhead.net";
    ```

9.  Ensure that the paths to the backend service is passed through.

    ```
    $ nano vite.config.js
    ```

    For example,

    ```
    proxy: {
      "/docs": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
      "/openapi.json": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
    },
    ```

10. Ensure that the OIDC client configuration has been registered.

    ```
    https://pagure.io/fedora-infra/ansible/blob/main/f/roles/ipsilon/templates/openidc.staging.static.j2
    ```

    For example,

    ```
    w2fm client_name="Webhook To Fedora Messaging"
    w2fm client_secret="notsecret"
    w2fm redirect_uris=["https://w2fm.gridhead.net/docs/oauth2-redirect", "https://w2fm.gridhead.net/callback"]
    w2fm client_uri="https://w2fm.gridhead.net/"
    w2fm ipsilon_internal={"type":"static","client_id":"w2fm","trusted":true}
    w2fm contacts=["admin@fedoraproject.org"]
    w2fm client_id=null
    w2fm policy_uri="https://fedoraproject.org/wiki/Legal:PrivacyPolicy"
    w2fm grant_types="authorization_code"
    w2fm response_types="code"
    w2fm application_type="native"
    w2fm subject_type="public"
    w2fm logo_uri=null
    w2fm tos_uri=null
    w2fm jwks_uri=null
    w2fm jwks=null
    w2fm sector_identifier_uri=null
    w2fm request_uris=[]
    w2fm require_auth_time=null
    w2fm token_endpoint_auth_method="none"
    w2fm id_token_signed_response_alg="RS256"
    w2fm request_object_signing_alg="none"
    w2fm initiate_login_uri=null
    w2fm default_max_age=null
    w2fm default_acr_values=null
    w2fm client_secret_expires_at=0
    ```

11. Ensure that the OpenID Connect client is properly configured.

    ```
    $ nano src/config/oidc.js
    ```

    For example,

    ```
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
    ```

12. Execute the linter and formatter to clean after the recent changes.

    ```
    $ npm run lint
    ```

    ```
    $ npm run format
    ```

    For example,

    ```
    > frontend@0.1.0 lint
    > eslint .
    ```

    ```
    > frontend@0.1.0 format
    > prettier --write .

    eslint.config.js 26ms (unchanged)
    index.html 16ms (unchanged)
    package-lock.json 41ms (unchanged)
    package.json 1ms (unchanged)
    README.md 22ms
    src/assets/docs/fogo.md 4ms (unchanged)
    src/assets/docs/gthb.md 3ms (unchanged)
    src/assets/docs/gtlb.md 3ms (unchanged)
    src/components/call.jsx 6ms (unchanged)
    src/components/code.jsx 10ms (unchanged)
    src/components/diff.jsx 3ms (unchanged)
    src/components/edit.jsx 6ms (unchanged)
    src/components/fact.jsx 1ms (unchanged)
    src/components/flag.jsx 2ms (unchanged)
    src/components/flaw.jsx 1ms (unchanged)
    src/components/list.jsx 3ms (unchanged)
    src/components/make.jsx 6ms (unchanged)
    src/components/mode.jsx 2ms (unchanged)
    src/components/navi.jsx 4ms (unchanged)
    src/components/side.jsx 2ms (unchanged)
    src/components/unit.jsx 5ms (unchanged)
    src/components/wipe.jsx 5ms (unchanged)
    src/config/data.js 1ms (unchanged)
    src/config/oidc.js 1ms (unchanged)
    src/features/auth.jsx 2ms (unchanged)
    src/features/data.jsx 1ms (unchanged)
    src/features/part.jsx 5ms (unchanged)
    src/main.jsx 1ms (unchanged)
    src/styles/core.css 16ms (unchanged)
    vite.config.js 2ms (unchanged)
    ```

13. Configure your reverse proxy to point the reachable hostname.

    ```
    https://w2fm.gridhead.net -> http://localhost:5173
    ```

14. Start the frontend development service.

    ```
    $ npm run dev
    ```

    For example,

    ```

    VITE v7.0.5  ready in 122 ms

    ➜  Local:   http://localhost:5173/
    ➜  Network: http://192.168.29.100:5173/
    ➜  press h + enter to show help
    ```

15. Access the reachable hostname to view the homepage.

    ```
    $ curl -i https://w2fm.gridhead.net
    ```

    For example,

    ```
    HTTP/2 200
    date: Mon, 21 Jul 2025 07:01:42 GMT
    content-type: text/html
    cache-control: no-cache
    vary: Origin
    cf-cache-status: DYNAMIC
    nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
    server: cloudflare
    cf-ray: 9628d4140e3f9f8d-AMS
    alt-svc: h3=":443"; ma=86400
    ```

16. Verify whether the backend paths have been passed through.

    ```
    $ curl -i https://w2fm.gridhead.net/docs
    ```

    ```
    $ curl -i https://w2fm.gridhead.net/api
    ```

    ```
    $ curl -i https://w2fm.gridhead.net/openapi.json
    ```

17. Attempt logging into the frontend service using an internet browser.

    ```
    https://w2fm.gridhead.net/
    ```

18. Ensure that you are safely able to logout after performing functions.
    ```
    https://w2fm.gridhead.net/
    ```
