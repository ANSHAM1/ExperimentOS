# Signal — experiment console frontend

A React + Vite + Tailwind frontend for the FastAPI auth/experiment backend you shared.

## How the session survives closing the tab

Your backend already does the hard part right, so the frontend just has to respect it:

- `POST /auth/login` and `POST /auth/refresh` set two **httpOnly** cookies (`refresh_token`,
  `session_id`, scoped to `path=/auth`) and return a short-lived `access_token` in the JSON body.
- Because the cookies are httpOnly, JavaScript can never read them — that's intentional, it's
  what protects the refresh token from XSS. The frontend never tries to.
- The `access_token` is kept **only in memory** (a variable inside `src/lib/apiClient.js`,
  surfaced through `AuthContext`). It is *not* written to `localStorage`/`sessionStorage`, so it
  disappears the moment the tab is closed or the page reloads — also intentional.
- On every app load, `AuthProvider` calls `POST /auth/refresh` before rendering anything else.
  The browser attaches the `refresh_token`/`session_id` cookies automatically (`credentials:
  "include"`). If they're still valid, the backend returns a new `access_token` and the user
  lands straight in the console — no login form. If they've expired or don't exist, the user
  sees `/login`.
- `apiClient` also proactively re-runs `/auth/refresh` ~60 seconds before the current
  `access_token`'s JWT `exp`, and reactively on any `401` from a protected call (de-duplicated so
  concurrent requests trigger one refresh, not several). Either path failing clears state and
  sends the user back to `/login`.

Net effect: the user stays signed in across tab closes and page reloads for as long as
`REFRESH_TOKEN_EXPIRE_SECONDS` says the session is valid, with no token ever sitting in
browser storage.

## One gap to close on the backend

The routes you shared don't include a `/auth/logout` endpoint, so `logout()` in
`AuthContext.jsx` currently only clears in-memory state — the `refresh_token`/`session_id`
cookies stay on the browser until they expire naturally. Add something like:

```python
@auth_router.post("/logout")
async def logout(response: Response, session_id: str | None = Cookie(default=None)):
    if session_id:
        await SessionStore(redis).revoke(UUID(session_id))
    response.delete_cookie("refresh_token", path="/auth")
    response.delete_cookie("session_id", path="/auth")
    return {"success": True}
```

...then call it from `logout()` before clearing local state, so a signed-out user is actually
signed out server-side too.

## CORS, since the frontend and API are different origins in dev

`allow_credentials=True` on the backend requires an explicit origin list (not `"*"`):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

`localhost:5173` and `localhost:8000` are cross-origin but same-site, so the `SameSite=Lax`
cookies your backend sets are still attached to `fetch` calls between them — no cookie changes
needed for local dev. In production, put both behind the same registrable domain (or switch the
cookies to `SameSite=None` if they must live on different domains).

## Running it

```bash
npm install
cp .env.example .env   # point VITE_API_BASE_URL at your backend
npm run dev
```

## Structure

```
src/
  lib/apiClient.js       fetch wrapper: in-memory token, refresh de-dup, 401 retry
  context/AuthContext.jsx session restore on load, login/register/verify/logout
  components/            RouteGuards, AuthShell (split layout), Field, Button, Loader
  pages/                 LoginPage, RegisterPage, VerifyPage, ConsolePage
```

`ConsolePage` calls `POST /experiment/` with the bearer token attached — swap in your real
experiment UI once you're past the auth scaffolding.
