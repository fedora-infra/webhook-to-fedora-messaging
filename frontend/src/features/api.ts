import { userManager } from "../config/oidc.ts";

interface ApiCallParams {
  method: string | undefined
  path: string
  body?: Object
}

export async function apiCall({ method, path, body }: ApiCallParams) {
  const userdata = await userManager.getUser();
  if (!userdata || userdata.expired) {
    throw new Error("Unauthenticated", { cause: new Response(null, { status: 401, statusText: "Unauthenticated" }) });
  }
  const resp = await fetch(`${import.meta.env.VITE_API_URL}/api/v1${path}`, {
    method: method,
    headers: {
      Authorization: `Bearer ${userdata.access_token}`,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!resp.ok) {
    const serverMessage = (await resp.json()).detail;
    throw new Error(`${resp.status}: ${serverMessage}`, { cause: resp });
  }
  const data = await resp.json();
  return data.data;
}
