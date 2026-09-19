import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import {
  authApi,
  getAccessToken,
  getTokenExpiry,
  setAccessToken,
  setUnauthorizedHandler,
} from "../api/apiClient";

const AuthContext = createContext(null);

// "checking"       — restoring the session on first load
// "authenticated"  — we hold a live access token
// "unauthenticated"— no valid session; show the login/register flow
export function AuthProvider({ children }) {
  const [status, setStatus] = useState("checking");
  const refreshTimer = useRef(null);

  const scheduleProactiveRefresh = useCallback((token) => {
    clearTimeout(refreshTimer.current);
    const expiry = getTokenExpiry(token);
    if (!expiry) return; // not a decodable JWT — fall back to reactive 401 refresh only
    const fireIn = Math.max(expiry - Date.now() - 60_000, 5_000); // refresh 60s before expiry
    refreshTimer.current = setTimeout(async () => {
      try {
        const token = await authApi.refresh();
        setStatus("authenticated");
        scheduleProactiveRefresh(token);
      } catch {
        handleSessionEnded();
      }
    }, fireIn);
  }, []);

  const handleSessionEnded = useCallback(() => {
    clearTimeout(refreshTimer.current);
    setAccessToken(null);
    setStatus("unauthenticated");
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(handleSessionEnded);
  }, [handleSessionEnded]);

  // On mount: the refresh_token/session_id cookies (httpOnly, set by the
  // backend) are already on the browser if the user has a live session from
  // a previous visit. Calling /auth/refresh exchanges them for a fresh
  // access token without asking the user to log in again.
  useEffect(() => {
    (async () => {
      try {
        const token = await authApi.refresh();
        setStatus("authenticated");
        scheduleProactiveRefresh(token);
      } catch {
        setAccessToken(null);
        setStatus("unauthenticated");
      }
    })();
    return () => clearTimeout(refreshTimer.current);
  }, [scheduleProactiveRefresh]);

  const login = useCallback(
    async (email, password) => {
      const data = await authApi.login(email, password);
      if (!data?.success) return { success: false, message: data?.message || "Login failed" };
      setAccessToken(data.access_token);
      setStatus("authenticated");
      scheduleProactiveRefresh(data.access_token);
      return { success: true };
    },
    [scheduleProactiveRefresh]
  );

  const register = useCallback(async (email, password) => {
    const data = await authApi.register(email, password);
    return { success: !!data?.success, message: data?.message || "" };
  }, []);

  const verifyEmail = useCallback(async (email, otp) => {
    const data = await authApi.verifyEmail(email, otp);
    return { success: !!data?.success, message: data?.message || "" };
  }, []);

  // The backend routes given to us don't expose a /auth/logout endpoint to
  // revoke the session server-side or clear the httpOnly cookies, so this
  // only clears client state. The refresh_token/session_id cookies remain
  // on the browser until they expire (path=/auth). Add a /auth/logout route
  // that clears both cookies and revokes the session in Redis, then call it
  // here, to make this a true logout.
  const logout = useCallback(() => {
    handleSessionEnded();
  }, [handleSessionEnded]);

  const value = {
    status,
    isAuthenticated: status === "authenticated",
    accessToken: getAccessToken(),
    login,
    register,
    verifyEmail,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
