from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Callable, cast

import requests
import streamlit as st

from api_client import APIClient, APIError

DEFAULT_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

STATUS_META = {
    "queued":    {"label": "Queued",    "color": "#8B8FA3", "icon": "⏳"},
    "pending":   {"label": "Pending",   "color": "#F5A623", "icon": "⏳"},
    "completed": {"label": "Completed", "color": "#2ECC71", "icon": "✅"},
    "failed":    {"label": "Failed",    "color": "#E74C3C", "icon": "❌"},
    "unknown":   {"label": "Unknown",   "color": "#8B8FA3", "icon": "❔"},
}


# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------

def init_state() -> None:
    defaults: dict[str, object] = {
        "http_session": requests.Session(),
        "base_url": DEFAULT_BASE_URL,
        "access_token": None,
        "user_email": None,
        "auth_view": "login",       # login | register | verify
        "pending_verify_email": None,
        "experiments": [],          # list[dict]
        "flash": None,              # (kind, message) shown once then cleared
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_client() -> APIClient:
    return APIClient(st.session_state.base_url, st.session_state.http_session)


def is_logged_in() -> bool:
    return st.session_state.access_token is not None


def logout(message: str | None = None) -> None:
    st.session_state.access_token = None
    st.session_state.user_email = None
    st.session_state.http_session = requests.Session()  # drop cookies client-side
    st.session_state.auth_view = "login"
    if message:
        st.session_state.flash = ("info", message)


def set_flash(kind: str, message: str) -> None:
    st.session_state.flash = (kind, message)


def show_flash() -> None:
    if st.session_state.flash:
        kind, message = st.session_state.flash
        getattr(st, kind, st.info)(message)
        st.session_state.flash = None


# --------------------------------------------------------------------------
# Authenticated call helper (access-token refresh-and-retry)
# --------------------------------------------------------------------------

def call_authenticated(
    action: Callable[..., requests.Response], *args: object, **kwargs: object
) -> requests.Response | None:
    client = get_client()

    try:
        resp = action(client, st.session_state.access_token, *args, **kwargs)
    except APIError as exc:
        set_flash("error", str(exc))
        return None

    if resp.status_code != 401:
        return resp

    # Access token expired -- try to rotate it via the refresh cookie flow.
    try:
        refreshed = client.refresh()
    except APIError as exc:
        logout(f"Session expired and could not be renewed: {exc}")
        return None

    if not refreshed.get("success") or not refreshed.get("access_token"):
        logout("Your session has expired. Please log in again.")
        return None

    st.session_state.access_token = refreshed["access_token"]

    try:
        resp = action(client, st.session_state.access_token, *args, **kwargs)
    except APIError as exc:
        set_flash("error", str(exc))
        return None

    if resp.status_code == 401:
        logout("Your session has expired. Please log in again.")
        return None

    return resp


# --------------------------------------------------------------------------
# UI: Auth screens
# --------------------------------------------------------------------------

def render_login() -> None:
    st.subheader("Log in")
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in", use_container_width=True, type="primary")

    if submitted:
        if not email or not password:
            st.error("Email and password are required.")
            return
        client = get_client()
        try:
            result = client.login(email.strip().lower(), password)
        except APIError as exc:
            st.error(str(exc))
            return

        if result.get("success") and result.get("access_token"):
            st.session_state.access_token = result["access_token"]
            st.session_state.user_email = email.strip().lower()
            set_flash("success", "Logged in successfully.")
            st.rerun()
        else:
            st.error(result.get("message") or "Invalid email or password.")

    st.caption("New here?")
    if st.button("Create an account", use_container_width=True):
        st.session_state.auth_view = "register"
        st.rerun()


def render_register() -> None:
    st.subheader("Create an account")
    with st.form("register_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm password", type="password")
        submitted = st.form_submit_button("Register", use_container_width=True, type="primary")

    if submitted:
        if not email or not password:
            st.error("Email and password are required.")
            return
        if password != password_confirm:
            st.error("Passwords do not match.")
            return

        client = get_client()
        try:
            result = client.register(email.strip(), password)
        except APIError as exc:
            st.error(str(exc))
            return

        if result.get("success"):
            st.session_state.pending_verify_email = email.strip().lower()
            st.session_state.auth_view = "verify"
            set_flash("success", result.get("message") or "Check your email for a verification code.")
            st.rerun()
        else:
            st.error(result.get("message") or "Registration failed.")

    if st.button("Back to login", use_container_width=True):
        st.session_state.auth_view = "login"
        st.rerun()


def render_verify() -> None:
    st.subheader("Verify your email")
    email = st.session_state.pending_verify_email or ""
    st.caption(f"We sent a one-time code to **{email}**.")

    with st.form("verify_form"):
        entered_email = st.text_input("Email", value=email)
        otp = st.text_input("Verification code", max_chars=8)
        submitted = st.form_submit_button("Verify", use_container_width=True, type="primary")

    if submitted:
        if not entered_email or not otp:
            st.error("Email and code are required.")
            return
        client = get_client()
        try:
            result = client.verify_email(entered_email.strip().lower(), otp.strip())
        except APIError as exc:
            st.error(str(exc))
            return

        if result.get("success"):
            set_flash("success", "Email verified! You can log in now.")
            st.session_state.pending_verify_email = None
            st.session_state.auth_view = "login"
            st.rerun()
        else:
            st.error(result.get("message") or "Verification failed.")

    if st.button("Back to login", use_container_width=True):
        st.session_state.auth_view = "login"
        st.rerun()


def render_auth_gate() -> None:
    st.markdown(
        "<h1 style='text-align:center;margin-bottom:0;'>🧪 Agent Console</h1>"
        "<p style='text-align:center;color:#8B8FA3;margin-top:4px;'>"
        "Sign in to run and track your experiments</p>",
        unsafe_allow_html=True,
    )
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        with st.container(border=True):
            view = st.session_state.auth_view
            if view == "login":
                render_login()
            elif view == "register":
                render_register()
            elif view == "verify":
                render_verify()


# --------------------------------------------------------------------------
# UI: Main app (post-login)
# --------------------------------------------------------------------------

def status_badge_html(status: str) -> str:
    meta = STATUS_META.get(status, STATUS_META["unknown"])
    return (
        f"<span style='background:{meta['color']}22;color:{meta['color']};"
        f"padding:2px 10px;border-radius:999px;font-size:0.8rem;font-weight:600;'>"
        f"{meta['icon']} {meta['label']}</span>"
    )


def do_submit_experiment(client: APIClient, access_token: str, prompt: str) -> requests.Response:
    return client.submit_experiment(access_token, prompt)


def do_check_status(client: APIClient, access_token: str, experiment_id: str) -> requests.Response:
    return client.get_experiment_status(access_token, experiment_id)


def render_run_tab() -> None:
    st.subheader("Run a new experiment")
    with st.form("experiment_form", clear_on_submit=True):
        prompt = st.text_area(
            "Prompt",
            placeholder="Describe what you want the agent to do...",
            height=140,
        )
        submitted = st.form_submit_button("🚀 Submit experiment", type="primary", use_container_width=True)

    if submitted:
        if not prompt.strip():
            st.error("Please enter a prompt.")
            return

        resp = call_authenticated(do_submit_experiment, prompt.strip())
        if resp is None:
            st.rerun()
            return

        record: dict[str, object] = {
            "local_id": str(uuid.uuid4()),
            "backend_id": None,   # populate here once the backend returns an experiment id
            "prompt": prompt.strip(),
            "submitted_at": datetime.now(timezone.utc),
            "status": "queued",
            "output": None,
        }

        if resp.status_code == 200:
            try:
                body = cast(dict[str, object], resp.json())
            except ValueError:
                body = {}
            record["output"] = body.get("output")
            # Forward-compatible: if the backend is later extended to return
            # an id, pick it up automatically so status polling can work.
            record["backend_id"] = body.get("experiment_id") or body.get("id")
            set_flash("success", "Experiment submitted.")
        else:
            record["status"] = "failed"
            set_flash("error", f"Submission failed ({resp.status_code}).")

        st.session_state.experiments.insert(0, record)
        st.rerun()


def refresh_statuses() -> None:
    """Best-effort poll of a status endpoint that may not exist yet."""
    any_checked = False
    for record in st.session_state.experiments:
        if record["status"] not in ("queued", "pending") or not record["backend_id"]:
            continue
        any_checked = True
        resp = call_authenticated(do_check_status, record["backend_id"])
        if resp is not None and resp.status_code == 200:
            try:
                body = resp.json()
                record["status"] = body.get("status", record["status"])
                record["output"] = body.get("output", record["output"])
            except ValueError:
                pass

    if not any_checked:
        st.info(
            "No live status endpoint detected yet -- experiments will show as "
            "**Queued** until the backend exposes `GET /experiment/{id}`. "
            "See README.md for the suggested contract.",
            icon="ℹ️",
        )


def render_history_tab() -> None:
    st.subheader("Experiment history")

    col_a, _ = st.columns([1, 5])
    with col_a:
        if st.button("🔄 Refresh status", use_container_width=True):
            refresh_statuses()

    if not st.session_state.experiments:
        st.info("No experiments submitted yet -- run one from the **Run Experiment** tab.")
        return

    for record in st.session_state.experiments:
        with st.container(border=True):
            top_left, top_right = st.columns([4, 1])
            with top_left:
                st.markdown(f"**{record['prompt']}**")
                st.caption(record["submitted_at"].strftime("%Y-%m-%d %H:%M:%S UTC"))
            with top_right:
                st.markdown(status_badge_html(record["status"]), unsafe_allow_html=True)

            if record.get("output"):
                st.write(record["output"])
            if record.get("backend_id"):
                st.caption(f"id: `{record['backend_id']}`")


def render_app() -> None:
    with st.sidebar:
        st.markdown("### 🧪 Agent Console")
        st.text_input("API base URL", key="base_url")
        st.divider()
        st.markdown(f"**Signed in as**  \n{st.session_state.user_email or '—'}")
        if st.button("Log out", use_container_width=True):
            logout("You have been logged out.")
            st.rerun()

    st.title("Agent Console")
    tab_run, tab_history = st.tabs(["🚀 Run Experiment", "📜 History"])
    with tab_run:
        render_run_tab()
    with tab_history:
        render_history_tab()


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="Agent Console", page_icon="🧪", layout="centered")
    init_state()
    show_flash()

    if is_logged_in():
        render_app()
    else:
        render_auth_gate()


if __name__ == "__main__":
    main()
