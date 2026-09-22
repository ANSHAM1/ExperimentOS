// FastAPI backend URL.
// Development/testing:
// VITE_API_BASE_URL=http://localhost:8001
const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8001";

// -----------------------------------------------------------------------------
// In-memory access token
// -----------------------------------------------------------------------------

let accessToken = null;
let onUnauthorized = () => {};

export function setAccessToken(token) {
  accessToken = token;
}

export function getAccessToken() {
  return accessToken;
}

export function setUnauthorizedHandler(handler) {
  onUnauthorized = handler;
}

// -----------------------------------------------------------------------------
// JWT expiry
// -----------------------------------------------------------------------------

function getTokenExpiryMs(token) {
  try {
    const payload = JSON.parse(
      atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")),
    );

    return typeof payload.exp === "number" ? payload.exp * 1000 : null;
  } catch {
    return null;
  }
}

export function getTokenExpiry(token) {
  return getTokenExpiryMs(token);
}

// -----------------------------------------------------------------------------
// Token refresh
// -----------------------------------------------------------------------------

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
          throw new Error(
            data?.message || "Session could not be refreshed",
          );
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

// -----------------------------------------------------------------------------
// Core API request
// -----------------------------------------------------------------------------

export async function apiRequest(
  path,
  { method = "GET", body, authenticated = false, headers = {} } = {},
) {
  const doFetch = () =>
    fetch(`${BASE_URL}${path}`, {
      method,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",

        ...(authenticated && accessToken
          ? {
              Authorization: `Bearer ${accessToken}`,
            }
          : {}),

        ...headers,
      },

      body: body ? JSON.stringify(body) : undefined,
    });

  let res = await doFetch();

  // Access token expired.
  // Refresh once and retry the original request.
  if (authenticated && res.status === 401) {
    try {
      await refresh();
      res = await doFetch();
    } catch (error) {
      onUnauthorized();
      throw error;
    }

    // Refresh succeeded but the retried request is still unauthorized.
    if (res.status === 401) {
      onUnauthorized();
    }
  }

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    if (data?.message) {
      throw new Error(data.message);
    }

    throw new Error(`Request failed with status ${res.status}`);
  }

  return data;
}

// -----------------------------------------------------------------------------
// Authentication API
// -----------------------------------------------------------------------------

export const authApi = {
  login: (email, password) =>
    apiRequest("/auth/login", {
      method: "POST",
      body: { email, password },
    }),

  register: (email, password) =>
    apiRequest("/auth/register", {
      method: "POST",
      body: { email, password },
    }),

  verifyEmail: (email, otp) =>
    apiRequest("/auth/verify", {
      method: "POST",
      body: { email, otp },
    }),

  refresh,
};

// -----------------------------------------------------------------------------
// Experiment API
// -----------------------------------------------------------------------------

export const experimentApi = {
  run: (prompt) =>
    apiRequest("/agent/experiment", {
      method: "POST",
      authenticated: true,
      body: { prompt },
    }),
};

// -----------------------------------------------------------------------------
// Database integrations API
// -----------------------------------------------------------------------------
//
// NEW — this module is not yet implemented on the backend. Add these four
// FastAPI routes (all authenticated, behind the same bearer-token dependency
// used by /agent/experiment) to light up the "Connect a database" screen:
//
//   GET    /integrations/databases
//     -> { success: true, databases: [{
//            id, type, name, host, port, database, ssl, status,
//            created_at
//          }, ...] }
//        `status` is one of "connected" | "error" | "unverified".
//        Never return the stored password/secret in this payload.
//
//   POST   /integrations/databases
//     body: { type, name, host, port, database, username, password,
//             ssl, uri? }
//        `type` is one of "postgresql" | "mysql" | "mongodb" | "redis".
//        `uri` is set instead of host/port/etc. when the user pastes a
//        full connection string.
//     -> { success: true, database: { ...same shape as above } }
//        or { success: false, message: "..." } if the connection
//        attempt made server-side during creation fails.
//
//   POST   /integrations/databases/{id}/test
//     -> { success: true, status: "connected" }
//        or { success: false, status: "error", message: "..." }
//
//   DELETE /integrations/databases/{id}
//     -> { success: true }
//
export const integrationsApi = {
  list: () =>
    apiRequest("/integrations/databases", {
      authenticated: true,
    }),

  create: (payload) =>
    apiRequest("/integrations/databases", {
      method: "POST",
      authenticated: true,
      body: payload,
    }),

  test: (id) =>
    apiRequest(`/integrations/databases/${id}/test`, {
      method: "POST",
      authenticated: true,
    }),

  remove: (id) =>
    apiRequest(`/integrations/databases/${id}`, {
      method: "DELETE",
      authenticated: true,
    }),
};
