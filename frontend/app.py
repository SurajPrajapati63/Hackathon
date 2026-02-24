from __future__ import annotations

from datetime import datetime, time
from typing import Any

import requests
import streamlit as st


st.set_page_config(
    page_title="EventFlow Console",
    page_icon="ET",
    layout="wide",
    initial_sidebar_state="expanded",
)


THEME_PRESETS: dict[str, dict[str, str]] = {
    "Sunrise": {
        "ink": "#102a43",
        "sky": "#e1f5fe",
        "teal": "#00796b",
        "sand": "#f9f7f3",
        "accent": "#ff8f00",
        "bg_a": "#fff2cc",
        "bg_b": "#c8e6c9",
        "bg_c": "#f5fbff",
    },
    "Citrine": {
        "ink": "#1f2937",
        "sky": "#e8f0ff",
        "teal": "#0f766e",
        "sand": "#fffdf7",
        "accent": "#ea580c",
        "bg_a": "#fef3c7",
        "bg_b": "#d1fae5",
        "bg_c": "#f8fafc",
    },
}


ROLE_SECTIONS: dict[str, list[str]] = {
    "customer": ["Customer"],
    "organizer": ["Organizer", "Entry"],
    "admin": ["Admin", "Organizer", "Entry"],
}


def init_state() -> None:
    st.session_state.setdefault("base_url", "http://localhost:8000")
    st.session_state.setdefault("theme_name", "Sunrise")
    st.session_state.setdefault("token", None)
    st.session_state.setdefault("user", None)


def inject_styles(theme: dict[str, str]) -> None:
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

            :root {{
                --brand-ink: {theme['ink']};
                --brand-sky: {theme['sky']};
                --brand-teal: {theme['teal']};
                --brand-sand: {theme['sand']};
                --brand-accent: {theme['accent']};
            }}

            html, body, [class*="css"] {{
                font-family: "Space Grotesk", sans-serif;
                color: var(--brand-ink);
            }}

            .stApp {{
                background:
                    radial-gradient(circle at 8% 18%, {theme['bg_a']} 0%, transparent 35%),
                    radial-gradient(circle at 92% 12%, {theme['bg_b']} 0%, transparent 32%),
                    linear-gradient(140deg, {theme['bg_c']} 0%, var(--brand-sand) 100%);
                animation: fadeIn 0.45s ease;
            }}

            /* Force readable text colors across Streamlit elements even when host theme is dark */
            .stApp, .stApp p, .stApp li, .stApp span, .stApp label,
            .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
                color: var(--brand-ink) !important;
            }}

            [data-testid="stMarkdownContainer"] p {{
                color: var(--brand-ink) !important;
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(5px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            .hero {{
                border: 1px solid rgba(16, 42, 67, 0.14);
                border-radius: 16px;
                padding: 1rem 1.2rem;
                background: linear-gradient(118deg, #ffffff 0%, var(--brand-sky) 100%);
                margin-bottom: 1rem;
            }}

            .hero h2 {{
                margin: 0;
                font-weight: 700;
                letter-spacing: 0.02em;
            }}

            .hero p {{
                margin: 0.3rem 0 0;
            }}

            .mono {{
                font-family: "IBM Plex Mono", monospace;
            }}

            [data-testid="stSidebar"] {{
                background: #f2f5fa !important;
                border-right: 1px solid rgba(16, 42, 67, 0.08);
            }}

            [data-testid="stSidebar"] * {{
                color: var(--brand-ink) !important;
            }}

            [data-testid="stAlertContainer"] [data-testid="stMarkdownContainer"] p {{
                color: inherit !important;
            }}

            /* Better contrast for tabs */
            button[role="tab"] {{
                color: #44576d !important;
            }}

            button[role="tab"][aria-selected="true"] {{
                color: var(--brand-accent) !important;
            }}

            /* Normalize input controls to light cards */
            .stTextInput input,
            .stTextArea textarea,
            .stNumberInput input,
            .stDateInput input,
            .stTimeInput input {{
                background: #ffffff !important;
                color: var(--brand-ink) !important;
                border: 1px solid rgba(16, 42, 67, 0.2) !important;
            }}

            .stSelectbox [data-baseweb="select"] > div,
            .stMultiSelect [data-baseweb="select"] > div {{
                background: #ffffff !important;
                color: var(--brand-ink) !important;
                border: 1px solid rgba(16, 42, 67, 0.2) !important;
            }}

            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder {{
                color: #5c6f82 !important;
            }}

            /* Keep primary actions readable */
            button[kind="primary"] {{
                border-radius: 10px;
                background: var(--brand-teal) !important;
                color: #ffffff !important;
                border: 1px solid var(--brand-teal) !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def normalize_role(user: dict[str, Any] | None) -> str:
    if not user:
        return "unknown"
    return str(user.get("role", "unknown")).strip().lower()


def allowed_sections(role: str) -> list[str]:
    if role in ROLE_SECTIONS:
        return ROLE_SECTIONS[role]
    return ["Customer", "Organizer", "Admin", "Entry"]


def api_request(
    method: str,
    path: str,
    *,
    token: str | None = None,
    json_body: dict[str, Any] | None = None,
) -> tuple[bool, int | None, Any]:
    url = f"{st.session_state.base_url.rstrip('/')}{path}"
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        resp = requests.request(method=method, url=url, headers=headers, json=json_body, timeout=30)
    except requests.RequestException as exc:
        return False, None, {"detail": f"Connection error: {exc}"}

    try:
        payload = resp.json()
    except ValueError:
        payload = {"detail": resp.text}

    return resp.ok, resp.status_code, payload


def render_payload(payload: Any) -> None:
    if isinstance(payload, list) and payload and all(isinstance(item, dict) for item in payload):
        st.dataframe(payload, use_container_width=True)
    else:
        st.json(payload)


def show_result(action: str, ok: bool, status_code: int | None, payload: Any) -> None:
    code = status_code if status_code is not None else "n/a"
    if ok:
        st.success(f"{action} succeeded ({code})")
    else:
        st.error(f"{action} failed ({code})")
    render_payload(payload)


def require_fields(required: dict[str, str]) -> bool:
    missing = [name for name, val in required.items() if not str(val).strip()]
    if missing:
        st.warning("Please provide: " + ", ".join(missing))
        return False
    return True


def sidebar() -> None:
    st.sidebar.title("Frontend Controls")

    st.session_state.base_url = st.sidebar.text_input(
        "Backend Base URL",
        value=st.session_state.base_url,
        help="Example: http://localhost:8000",
    )
    st.session_state.theme_name = st.sidebar.selectbox(
        "Theme",
        options=list(THEME_PRESETS.keys()),
        index=list(THEME_PRESETS.keys()).index(st.session_state.theme_name),
    )

    if st.sidebar.button("Health Check", key="health_check_btn"):
        show_result("Health check", *api_request("GET", "/health"))

    st.sidebar.divider()
    if st.session_state.token and st.session_state.user:
        st.sidebar.markdown("**Session**")
        st.sidebar.write({
            "email": st.session_state.user.get("email"),
            "role": st.session_state.user.get("role"),
            "id": st.session_state.user.get("id"),
        })
        if st.sidebar.button("Logout", key="logout_btn"):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    else:
        st.sidebar.info("Login to access protected routes.")


def auth_block() -> None:
    st.subheader("Authentication")
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            login_endpoint = st.selectbox("Login Route", ["/auth/login", "/entry/login"])
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
        if submitted:
            if require_fields({"Email": email, "Password": password}):
                ok, code, payload = api_request(
                    "POST",
                    login_endpoint,
                    json_body={"email": email, "password": password},
                )
                show_result("Login", ok, code, payload)
                if ok:
                    st.session_state.token = payload.get("access_token")
                    st.session_state.user = payload.get("user")
                    st.rerun()

    with register_tab:
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email", key="register_email")
            phone = st.text_input("Phone (optional)")
            role = st.selectbox("Role", ["customer", "organizer", "admin"])
            password = st.text_input("Password", type="password", key="register_password")
            submitted = st.form_submit_button("Register")
        if submitted:
            if require_fields({"Name": name, "Email": email, "Password": password}):
                body: dict[str, Any] = {
                    "name": name,
                    "email": email,
                    "password": password,
                    "role": role,
                }
                if phone.strip():
                    body["phone"] = phone.strip()
                show_result("Register", *api_request("POST", "/auth/register", json_body=body))


def customer_panel(token: str) -> None:
    st.markdown("### Customer")
    tabs = st.tabs(["Events", "Bookings", "Tickets", "Refunds", "Support"])

    with tabs[0]:
        if st.button("List events", key="cust_list_events"):
            show_result("Get events", *api_request("GET", "/customer/events", token=token))

        event_id = st.text_input("Event ID", key="customer_event_id")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Get event", use_container_width=True, key="cust_get_event"):
                if require_fields({"Event ID": event_id}):
                    show_result("Get event", *api_request("GET", f"/customer/events/{event_id}", token=token))
        with c2:
            if st.button("Get event seats", use_container_width=True, key="cust_get_seats"):
                if require_fields({"Event ID": event_id}):
                    show_result("Get event seats", *api_request("GET", f"/customer/events/{event_id}/seats", token=token))

    with tabs[1]:
        with st.form("create_booking_form"):
            event_id = st.text_input("Event ID", key="book_event_id")
            seats_raw = st.text_input("Seat numbers (comma-separated)")
            submitted = st.form_submit_button("Create booking (lock seats)")
        if submitted:
            seat_numbers = [s.strip() for s in seats_raw.split(",") if s.strip()]
            if require_fields({"Event ID": event_id, "Seat numbers": ",".join(seat_numbers)}):
                show_result(
                    "Create booking",
                    *api_request(
                        "POST",
                        "/customer/bookings",
                        token=token,
                        json_body={"event_id": event_id, "seat_numbers": seat_numbers},
                    ),
                )

        booking_id = st.text_input("Booking ID", key="booking_id_actions")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Confirm booking", use_container_width=True, key="cust_confirm_booking"):
                if require_fields({"Booking ID": booking_id}):
                    show_result(
                        "Confirm booking",
                        *api_request("POST", f"/customer/bookings/{booking_id}/confirm", token=token),
                    )
        with c2:
            if st.button("Get booking summary", use_container_width=True, key="cust_get_booking"):
                if require_fields({"Booking ID": booking_id}):
                    show_result(
                        "Get booking summary",
                        *api_request("GET", f"/customer/bookings/{booking_id}", token=token),
                    )
        with c3:
            if st.button("Cancel booking", use_container_width=True, key="cust_cancel_booking"):
                if require_fields({"Booking ID": booking_id}):
                    show_result(
                        "Cancel booking",
                        *api_request("POST", f"/customer/bookings/{booking_id}/cancel", token=token),
                    )

        if st.button("List my bookings", key="cust_list_bookings"):
            show_result("List my bookings", *api_request("GET", "/customer/bookings", token=token))

    with tabs[2]:
        if st.button("List my tickets", key="cust_list_tickets"):
            show_result("List my tickets", *api_request("GET", "/customer/tickets", token=token))

        ticket_id = st.text_input("Ticket ID", key="ticket_id_customer")
        if st.button("Get ticket by ID", key="cust_get_ticket"):
            if require_fields({"Ticket ID": ticket_id}):
                show_result("Get ticket", *api_request("GET", f"/customer/tickets/{ticket_id}", token=token))

    with tabs[3]:
        with st.form("refund_form"):
            booking_id = st.text_input("Booking ID", key="refund_booking")
            reason = st.text_area("Reason", placeholder="Why do you need a refund?")
            submitted = st.form_submit_button("Request refund")
        if submitted:
            if require_fields({"Booking ID": booking_id, "Reason": reason}):
                show_result(
                    "Request refund",
                    *api_request(
                        "POST",
                        "/customer/refunds",
                        token=token,
                        json_body={"booking_id": booking_id, "reason": reason},
                    ),
                )

    with tabs[4]:
        with st.form("support_create_form"):
            subject = st.text_input("Subject")
            description = st.text_area("Description")
            category = st.selectbox("Category", ["booking", "payment", "refund", "event", "other"])
            booking_id = st.text_input("Booking ID (optional)")
            submitted = st.form_submit_button("Create support ticket")
        if submitted:
            if require_fields({"Subject": subject, "Description": description}):
                body: dict[str, Any] = {
                    "subject": subject,
                    "description": description,
                    "category": category,
                }
                if booking_id.strip():
                    body["booking_id"] = booking_id.strip()
                show_result("Create support ticket", *api_request("POST", "/customer/support", token=token, json_body=body))

        if st.button("List my support tickets", key="cust_list_support"):
            show_result("My support tickets", *api_request("GET", "/customer/support", token=token))


def organizer_panel(token: str) -> None:
    st.markdown("### Organizer")
    tabs = st.tabs(["Events", "Seats", "Insights"])

    with tabs[0]:
        with st.form("create_event_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            category = st.text_input("Category")
            venue_id = st.text_input("Venue ID")
            event_date = st.date_input("Event Date")
            event_time = st.time_input("Event Time", value=time(hour=18, minute=0))
            ticket_price = st.number_input("Ticket Price", min_value=1.0, value=100.0, step=1.0)
            total_seats = st.number_input("Total Seats", min_value=1, value=100, step=1)
            submitted = st.form_submit_button("Create event")
        if submitted:
            if require_fields({"Title": title, "Description": description, "Category": category, "Venue ID": venue_id}):
                dt = datetime.combine(event_date, event_time).isoformat()
                body = {
                    "title": title,
                    "description": description,
                    "category": category,
                    "venue_id": venue_id,
                    "event_date": dt,
                    "ticket_price": ticket_price,
                    "total_seats": int(total_seats),
                }
                show_result("Create event", *api_request("POST", "/organizer/events", token=token, json_body=body))

        if st.button("List my events", key="org_list_events"):
            show_result("My events", *api_request("GET", "/organizer/events", token=token))

        event_id = st.text_input("Event ID for update/delete", key="org_event_id_mut")
        with st.form("update_event_form"):
            new_title = st.text_input("New title (optional)")
            new_desc = st.text_area("New description (optional)")
            new_category = st.text_input("New category (optional)")
            new_status = st.selectbox("Status", ["", "upcoming", "ongoing", "completed", "cancelled"])
            submitted = st.form_submit_button("Update event")
        if submitted:
            update_body: dict[str, Any] = {}
            if new_title.strip():
                update_body["title"] = new_title.strip()
            if new_desc.strip():
                update_body["description"] = new_desc.strip()
            if new_category.strip():
                update_body["category"] = new_category.strip()
            if new_status:
                update_body["status"] = new_status
            if require_fields({"Event ID": event_id}) and update_body:
                show_result(
                    "Update event",
                    *api_request("PUT", f"/organizer/events/{event_id}", token=token, json_body=update_body),
                )
            elif not update_body:
                st.warning("Please provide at least one update field.")

        if st.button("Delete event", key="org_delete_event"):
            if require_fields({"Event ID": event_id}):
                show_result("Delete event", *api_request("DELETE", f"/organizer/events/{event_id}", token=token))

    with tabs[1]:
        event_id = st.text_input("Event ID", key="org_event_id_seats")
        seats_text = st.text_input("Seat numbers (comma-separated)", key="org_seat_numbers")
        if st.button("Create seats", key="org_create_seats"):
            seat_numbers = [s.strip() for s in seats_text.split(",") if s.strip()]
            if require_fields({"Event ID": event_id, "Seat numbers": ",".join(seat_numbers)}):
                show_result(
                    "Create seats",
                    *api_request(
                        "POST",
                        f"/organizer/events/{event_id}/seats",
                        token=token,
                        json_body={"seat_numbers": seat_numbers},
                    ),
                )

    with tabs[2]:
        event_id = st.text_input("Event ID for bookings/entries", key="org_event_id_views")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("View event bookings", use_container_width=True, key="org_view_bookings"):
                if require_fields({"Event ID": event_id}):
                    show_result("Event bookings", *api_request("GET", f"/organizer/events/{event_id}/bookings", token=token))
        with c2:
            if st.button("View event entries", use_container_width=True, key="org_view_entries"):
                if require_fields({"Event ID": event_id}):
                    show_result("Event entries", *api_request("GET", f"/organizer/events/{event_id}/entries", token=token))


def admin_panel(token: str) -> None:
    st.markdown("### Admin")
    tabs = st.tabs(["Overview", "Venues", "Refunds", "Support"])

    with tabs[0]:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Get users", use_container_width=True, key="admin_get_users"):
                show_result("Users", *api_request("GET", "/admin/users", token=token))
        with c2:
            if st.button("Get bookings", use_container_width=True, key="admin_get_bookings"):
                show_result("Bookings", *api_request("GET", "/admin/bookings", token=token))
        with c3:
            if st.button("Get support tickets", use_container_width=True, key="admin_get_support"):
                show_result("Support tickets", *api_request("GET", "/admin/support", token=token))

    with tabs[1]:
        with st.form("create_venue_form"):
            name = st.text_input("Venue name")
            location = st.text_input("Location")
            capacity = st.number_input("Capacity", min_value=1, value=500, step=10)
            description = st.text_area("Description")
            submitted = st.form_submit_button("Create venue")
        if submitted:
            if require_fields({"Venue name": name, "Location": location}):
                show_result(
                    "Create venue",
                    *api_request(
                        "POST",
                        "/admin/venues",
                        token=token,
                        json_body={
                            "name": name,
                            "location": location,
                            "capacity": int(capacity),
                            "description": description,
                        },
                    ),
                )

    with tabs[2]:
        refund_id = st.text_input("Refund ID")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Approve refund", use_container_width=True, key="admin_approve_refund"):
                if require_fields({"Refund ID": refund_id}):
                    show_result("Approve refund", *api_request("PUT", f"/admin/refunds/{refund_id}/approve", token=token))
        with c2:
            admin_note = st.text_input("Reject note", key="refund_reject_note")
            if st.button("Reject refund", use_container_width=True, key="admin_reject_refund"):
                if require_fields({"Refund ID": refund_id}):
                    show_result(
                        "Reject refund",
                        *api_request(
                            "PUT",
                            f"/admin/refunds/{refund_id}/reject",
                            token=token,
                            json_body={"admin_note": admin_note},
                        ),
                    )

    with tabs[3]:
        ticket_id = st.text_input("Support ticket ID")
        status_val = st.selectbox("Ticket status", ["open", "in_progress", "resolved", "closed", "rejected"])
        admin_response = st.text_area("Admin response")
        if st.button("Update support ticket", key="admin_update_support"):
            if require_fields({"Support ticket ID": ticket_id}):
                show_result(
                    "Update support ticket",
                    *api_request(
                        "PUT",
                        f"/support/admin/{ticket_id}",
                        token=token,
                        json_body={"status": status_val, "admin_response": admin_response},
                    ),
                )


def entry_panel(token: str) -> None:
    st.markdown("### Entry")
    tabs = st.tabs(["Validate", "Logs"])

    with tabs[0]:
        with st.form("entry_validate_form"):
            ticket_code = st.text_input("Ticket Code")
            device_info = st.text_input("Device Info")
            submitted = st.form_submit_button("Validate ticket")
        if submitted:
            if require_fields({"Ticket Code": ticket_code}):
                show_result(
                    "Validate ticket",
                    *api_request(
                        "POST",
                        "/entry/validate",
                        token=token,
                        json_body={"ticket_code": ticket_code, "device_info": device_info or None},
                    ),
                )

    with tabs[1]:
        event_id = st.text_input("Event ID", key="entry_event_id")
        ticket_id = st.text_input("Ticket ID", key="entry_ticket_id")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Get event entry logs", use_container_width=True, key="entry_event_logs"):
                if require_fields({"Event ID": event_id}):
                    show_result("Event entry logs", *api_request("GET", f"/entry/event/{event_id}", token=token))
        with c2:
            if st.button("Get ticket entry logs", use_container_width=True, key="entry_ticket_logs"):
                if require_fields({"Ticket ID": ticket_id}):
                    show_result("Ticket entry logs", *api_request("GET", f"/entry/ticket/{ticket_id}", token=token))


def main() -> None:
    init_state()
    sidebar()
    inject_styles(THEME_PRESETS.get(st.session_state.theme_name, THEME_PRESETS["Sunrise"]))

    st.markdown(
        """
        <div class="hero">
            <h2>EventFlow Streamlit Frontend</h2>
            <p class="mono">Theme-aware dashboard with role-based access for customer, organizer, admin, and entry flows.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.token:
        auth_block()
        st.stop()

    user = st.session_state.user or {}
    role = normalize_role(user)
    st.caption(f"Logged in as: {user.get('email', 'n/a')} | role: {role}")

    sections = allowed_sections(role)
    section = st.radio("Workspace", options=sections, horizontal=True)

    if role not in ROLE_SECTIONS:
        st.info("Role is not explicitly mapped, so all workspaces are visible.")

    if section == "Customer":
        customer_panel(st.session_state.token)
    elif section == "Organizer":
        organizer_panel(st.session_state.token)
    elif section == "Admin":
        admin_panel(st.session_state.token)
    elif section == "Entry":
        entry_panel(st.session_state.token)


if __name__ == "__main__":
    main()
