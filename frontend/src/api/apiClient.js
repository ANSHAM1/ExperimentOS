// Base URL of the FastAPI backend. Set VITE_API_BASE_URL in your .env file.
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// --- in-memory access token -------------------------------------------------
// The access token is never persisted to localStorage/sessionStorage. It only
// ever lives in JS memory for the lifetime of the tab. Persistence across a
// closed tab / refreshed page is handled entirely by the httpOnly
// `refresh_token` + `session_id` cookies the backend sets on /auth/login and
// /auth/refresh — the browser sends those automatically, JS never touches them.
let accessToken = null;
let onUnauthorized = () => {};

export function setAccessToken(token) {
  accessToken = token;
}

export function getAccessToken() {
  return accessToken;
}

// Called by AuthContext so the client can tell it "the session is dead,
// clear your state and send the user back to login".
export function setUnauthorizedHandler(handler) {
  onUnauthorized = handler;
}

// --- decode a JWT's exp claim without a dependency --------------------------
function getTokenExpiryMs(token) {
  try {
    const payload = JSON.parse(atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")));
    return typeof payload.exp === "number" ? payload.exp * 1000 : null;
  } catch {
    return null;
  }
}

export function getTokenExpiry(token) {
  return getTokenExpiryMs(token);
}

// --- refresh, de-duplicated -------------------------------------------------
// If five requests all get a 401 at once, we want exactly one call to
// /auth/refresh, and every caller to await the same result.
let refreshPromise = null;

async function refresh() {
  if (!refreshPromise) {
    refreshPromise = fetch(`${BASE_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    })
      .then(async (res) => {
        const data = await res.json().catch(() => null);
        if (!res.ok || !data?.success || !data?.access_token) {
          throw new Error(data?.message || "Session could not be refreshed");
        }
        setAccessToken(data.access_token);
        return data.access_token;
      })
      .finally(() => {
        refreshPromise = null;
      });
  }
  return refreshPromise;
}

// --- core request helper -----------------------------------------------------
// `authenticated: true` attaches the bearer token and retries once through
// /auth/refresh on a 401 before giving up and logging the user out.
export async function apiRequest(
  path,
  { method = "GET", body, authenticated = false, headers = {} } = {}
) {
  const doFetch = () =>
    fetch(`${BASE_URL}${path}`, {
      method,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...(authenticated && accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        ...headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    });

  let res = await doFetch();

  if (authenticated && res.status === 401) {
    try {
      await refresh();
      res = await doFetch();
    } catch (err) {
      onUnauthorized();
      throw err;
    }
    if (res.status === 401) {
      onUnauthorized();
    }
  }

  const data = await res.json().catch(() => null);

  if (!res.ok && !data) {
    throw new Error(`Request failed with status ${res.status}`);
  }

  return data;
}

export const authApi = {
  login: (email, password) =>
    apiRequest("/auth/login", { method: "POST", body: { email, password } }),
  register: (email, password) =>
    apiRequest("/auth/register", { method: "POST", body: { email, password } }),
  verifyEmail: (email, otp) =>
    apiRequest("/auth/verify", { method: "POST", body: { email, otp } }),
  refresh,
};

export const experimentApi = {
  run: (prompt) =>
    apiRequest("/experiment/", { method: "POST", authenticated: true, body: { prompt } }),
};
