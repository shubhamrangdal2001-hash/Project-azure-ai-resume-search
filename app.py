"""
app.py  — Shubham Resume Search  (Streamlit)
Google-style search page powered by Azure AI Foundry agent_reference API.
Run: streamlit run app.py
"""

import time
import streamlit as st
from backend import (
    call_azure_agent,
    call_groq,
    build_search_results,
    AZURE_ENDPOINT,
    AZURE_API_KEY,
    AGENT_NAME,
    AGENT_VERSION,
    AZURE_MODEL,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Google Resume Agent — Resume Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS — Google-style ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Product+Sans:wght@400;700&family=Google+Sans:wght@400;500&display=swap');

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: #fff; }
[data-testid="stVerticalBlock"] > div { padding: 0; }

/* ── Home screen ── */
.g-home {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center;
    padding: 100px 20px 10px; background: #fff;
    font-family: 'Google Sans', Arial, sans-serif;
}
.g-logo {
    font-size: 72px; font-weight: 700; letter-spacing: -2px;
    margin-bottom: 10px; line-height: 1; user-select: none;
}
.g-logo .c1{color:#4285F4}.g-logo .c2{color:#EA4335}
.g-logo .c3{color:#FBBC05}.g-logo .c4{color:#34A853}

/* ── Search bar ── */
.g-searchbar {
    width: 100%; max-width: 580px;
    border: 1px solid #dfe1e5; border-radius: 24px;
    padding: 10px 20px 10px 20px; font-size: 16px;
    display: flex; align-items: center; gap: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    margin-bottom: 20px; cursor: text;
    transition: box-shadow 0.2s;
}
.g-searchbar:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.14); border-color: #dfe1e5; }

/* ── Results header ── */
.g-header {
    display: flex; align-items: center; gap: 20px;
    padding: 10px 24px; border-bottom: 1px solid #e8eaed;
    position: sticky; top: 0; background: #fff; z-index: 100;
    font-family: 'Google Sans', Arial, sans-serif;
}
.g-header-logo { font-size: 28px; font-weight: 700; letter-spacing: -1px; cursor:pointer; }
.g-header-logo .c1{color:#4285F4}.g-header-logo .c2{color:#EA4335}
.g-header-logo .c3{color:#FBBC05}.g-header-logo .c4{color:#34A853}

/* ── Result cards ── */
.result-card { margin-bottom: 28px; font-family: Arial, sans-serif; }
.result-url { display: flex; align-items: center; gap: 8px; margin-bottom: 2px; }
.result-favicon {
    width: 18px; height: 18px; border-radius: 3px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: #fff; flex-shrink: 0;
}
.result-url-text { font-size: 14px; color: #202124; line-height: 1.3; }
.result-title {
    font-size: 20px; color: #1a0dab; cursor: pointer;
    text-decoration: none; display: block; margin-bottom: 4px;
    line-height: 1.3; font-family: Arial, sans-serif;
}
.result-title:hover { text-decoration: underline; }
.result-snippet { font-size: 14px; color: #4d5156; line-height: 1.65; }
.result-snippet b { color: #202124; font-weight: 700; }
.ai-pill {
    display: inline-flex; align-items: center; gap: 4px;
    background: #e8f0fe; color: #1a73e8;
    font-size: 11px; padding: 2px 8px; border-radius: 10px;
    margin-bottom: 5px; font-weight: 500;
}
.azure-pill {
    display: inline-flex; align-items: center; gap: 4px;
    background: #e3f2fd; color: #0078D4;
    font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 500;
}

/* ── Stats bar ── */
.result-stats { font-size: 14px; color: #70757a; margin-bottom: 20px; font-family: Arial; }

/* ── AI Overview ── */
.ai-overview-container {
    background: #f0f4f9;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 24px;
    font-family: 'Google Sans', Arial, sans-serif;
    border: 1px solid #e1e3e5;
}
.ai-overview-title-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 500;
    color: #1f1f1f;
    margin-bottom: 12px;
}
.ai-overview-sparkles {
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #1a73e8 0%, #a546f0 50%, #f87099 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 11px;
    font-weight: bold;
}
.ai-overview-content {
    font-size: 15px;
    line-height: 1.6;
    color: #1f1f1f;
}


/* ── Knowledge panel ── */
.kp-card {
    border: 1px solid #dfe1e5; border-radius: 8px;
    padding: 20px; font-family: Arial, sans-serif;
    position: sticky; top: 80px;
}
.kp-avatar {
    width: 72px; height: 72px; border-radius: 50%;
    background: #4285F4; display: flex; align-items: center;
    justify-content: center; color: #fff; font-size: 26px;
    font-weight: 700; margin-bottom: 12px;
}
.kp-name { font-size: 22px; font-weight: 400; color: #202124; margin-bottom: 4px; }
.kp-role { font-size: 14px; color: #70757a; margin-bottom: 14px; }
.kp-section { font-size: 12px; color: #70757a; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin: 14px 0 6px; }
.kp-tag {
    display: inline-block; border: 1px solid #dadce0; border-radius: 16px;
    padding: 3px 12px; font-size: 13px; color: #202124;
    margin: 3px 3px 3px 0; cursor: pointer;
}
.kp-tag:hover { background: #f1f3f4; }
.kp-row { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 6px; font-size: 14px; color: #4d5156; }

/* ── Chat panel ── */
.chat-wrap {
    border: 1px solid #dfe1e5; border-radius: 8px;
    overflow: hidden; margin-top: 16px; font-family: Arial, sans-serif;
}
.chat-header {
    background: #4285F4; color: #fff;
    padding: 12px 16px; font-size: 14px; font-weight: 500;
    display: flex; justify-content: space-between; align-items: center;
}
.chat-messages {
    padding: 14px 16px; background: #f8f9fa;
    min-height: 120px; max-height: 320px; overflow-y: auto;
    display: flex; flex-direction: column; gap: 8px;
}
.msg-bot {
    background: #fff; border: 1px solid #e8eaed;
    border-radius: 12px 12px 12px 2px; padding: 8px 12px;
    font-size: 13px; color: #202124; max-width: 90%;
    align-self: flex-start; line-height: 1.5;
}
.msg-user {
    background: #4285F4; color: #fff;
    border-radius: 12px 12px 2px 12px; padding: 8px 12px;
    font-size: 13px; max-width: 90%; align-self: flex-end; line-height: 1.5;
}
.msg-thinking {
    color: #70757a; font-size: 12px; font-style: italic;
    align-self: flex-start; padding: 4px 0;
}

/* ── Tab bar (results page) ── */
.g-tabs {
    display: flex; gap: 0; padding: 0 24px;
    border-bottom: 1px solid #e8eaed; margin-bottom: 0;
    font-family: Arial, sans-serif;
}
.g-tab {
    padding: 14px 16px; font-size: 13px; color: #70757a !important;
    cursor: pointer; border-bottom: 3px solid transparent;
    margin-bottom: -1px;
    text-decoration: none !important;
}
.g-tab.active { color: #1a73e8 !important; border-bottom-color: #1a73e8 !important; }
.g-tab:hover { color: #202124 !important; background: #f1f3f4; border-radius: 4px 4px 0 0; text-decoration: none !important; }

/* ── Streamlit button overrides ── */
div[data-testid="stButton"] > button {
    background: #f8f9fa !important; border: 1px solid #f8f9fa !important;
    border-radius: 4px !important; color: #3c4043 !important;
    font-family: 'Google Sans', Arial, sans-serif !important;
    font-size: 14px !important; padding: 9px 23px !important;
    cursor: pointer !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: #dadce0 !important; box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    background: #f8f9fa !important;
}
div[data-testid="stTextInput"] input {
    border-radius: 24px !important; border: 1px solid #dfe1e5 !important;
    padding: 12px 20px !important; font-size: 16px !important;
    font-family: Arial, sans-serif !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(0,0,0,0) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.18) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for k, v in {
    "page": "home",
    "query": "",
    "active_tab": "All",
    "results": [],
    "ai_snippet": "",
    "elapsed": 0.0,
    "chat_history": [],
    "chat_messages_ui": [
        {"role": "bot", "text": "Hi! I'm Shubham's Azure AI resume agent. Ask me anything about his experience, skills, or projects."}
    ],
    "chat_open": False,
    "search_loading": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Query parameters handling ──
q_param = st.query_params.get("q", "")
tab_param = st.query_params.get("tab", "All")

if q_param:
    if st.session_state.query != q_param or st.session_state.active_tab != tab_param:
        st.session_state.query = q_param
        st.session_state.active_tab = tab_param
        st.session_state.page = "results"
        st.session_state.search_loading = True


def format_ai_text(text: str) -> str:
    import re
    # Escape HTML characters to prevent raw HTML breakages
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Restore basic formatting safely using <b> and <i>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Convert dash or asterisk bullet list items
    text = re.sub(r'^\s*-\s+(.*?)$', r'• \1', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\*\s+(.*?)$', r'• \1', text, flags=re.MULTILINE)
    # Convert newlines to HTML breaks
    text = text.replace('\n', '<br>')
    return text


def do_search(query: str, tab: str = "All"):
    if not query.strip():
        return
    st.session_state.query = query
    st.session_state.page = "results"
    st.session_state.search_loading = True
    st.session_state.active_tab = tab
    st.query_params["q"] = query
    st.query_params["tab"] = tab


def go_home():
    st.session_state.page = "home"
    st.session_state.query = ""
    st.session_state.results = []
    st.session_state.ai_snippet = ""
    st.session_state.active_tab = "All"
    st.query_params.clear()


# ═════════════════════════════════════════════════════════════════════════════
#  HOME PAGE
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
    <div class="g-home">
      <div class="g-logo">
        <span class="c1">S</span><span class="c2">h</span><span class="c3">u</span><span class="c4">b</span><span class="c1">h</span><span class="c2">a</span><span class="c3">m</span><span style="color:#4d5156">.</span><span class="c4">a</span><span class="c1">i</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Centre the search
    _, col, _ = st.columns([1, 2, 1])
    with col:
        query = st.text_input(
            "Search", placeholder="🔍  Search Shubham's resume...",
            key="home_input", label_visibility="collapsed"
        )

        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            s1, s2 = st.columns(2)
            with s1:
                if st.button("Resume Search", key="btn_search"):
                    do_search(query or "Shubham developer Azure")
            with s2:
                if st.button("Ask AI Agent", key="btn_agent"):
                    do_search(query or "Shubham skills")
                    st.session_state.chat_open = True



    if query:
        do_search(query)
        st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
#  RESULTS PAGE
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "results":

    # ── Header ──
    col_logo, col_search, col_tabs = st.columns([0.15, 0.55, 0.30])

    with col_logo:
        st.markdown("""
        <div class="g-header-logo" style="padding:14px 0 14px 16px;">
          <span class="c1">S</span><span class="c2">h</span><span class="c3">u</span><span class="c4">b</span><span class="c1">h</span><span class="c2">a</span><span class="c3">m</span><span style="color:#4d5156">.</span><span class="c4">a</span><span class="c1">i</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Home", key="back"):
            go_home()
            st.rerun()

    with col_search:
        new_query = st.text_input(
            "Search", value=st.session_state.query,
            key="results_input", label_visibility="collapsed"
        )
        if new_query != st.session_state.query and new_query.strip():
            do_search(new_query, tab=st.session_state.get("active_tab", "All"))
            st.rerun()

    with col_tabs:
        # Construct clickable tabs utilizing query params
        active_tab = st.session_state.get("active_tab", "All")
        q_val = st.session_state.query
        
        tab_all_class = "active" if active_tab == "All" else ""
        tab_skills_class = "active" if active_tab == "Skills" else ""
        tab_projects_class = "active" if active_tab == "Projects" else ""
        tab_contact_class = "active" if active_tab == "Contact" else ""
        
        st.markdown(f"""
        <div class="g-tabs" style="padding:0;">
          <a href="?q={q_val}&tab=All" target="_self" class="g-tab {tab_all_class}">All</a>
          <a href="?q={q_val}&tab=Skills" target="_self" class="g-tab {tab_skills_class}">Skills</a>
          <a href="?q={q_val}&tab=Projects" target="_self" class="g-tab {tab_projects_class}">Projects</a>
          <a href="?q={q_val}&tab=Contact" target="_self" class="g-tab {tab_contact_class}">Contact</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0;border:none;border-top:1px solid #e8eaed'>", unsafe_allow_html=True)

    # ── Body ──
    main_col, side_col = st.columns([0.62, 0.38])

    with main_col:
        st.markdown("<div style='padding:16px 24px 0;'>", unsafe_allow_html=True)

        # Run search + AI call if fresh
        if st.session_state.search_loading:
            with st.spinner("Querying Azure AI Foundry agent..."):
                t0 = time.time()
                results = build_search_results(st.session_state.query)
                
                active_tab = st.session_state.get("active_tab", "All")
                if active_tab == "Skills":
                    prompt = (
                        f"List the technical skills of Shubham Rangdal based on his resume. "
                        f"Group them cleanly by category (e.g. AI/ML, Data Analytics, Programming, etc.) using bullet points. "
                        f"Format the categories and key skills in bold."
                    )
                elif active_tab == "Projects":
                    prompt = (
                        f"Detail the projects completed by Shubham Rangdal based on his resume. "
                        f"List each project name, technologies used, and a brief description. "
                        f"Format project names and technologies in bold."
                    )
                elif active_tab == "Contact":
                    prompt = (
                        f"Provide the contact details of Shubham Rangdal including his email, phone number, "
                        f"LinkedIn profile, and location based on his resume. "
                        f"Format contact methods and values in bold."
                    )
                else:
                    prompt = (
                        f"Answer the user search query: '{st.session_state.query}' based on Shubham's resume. "
                        f"Write a clear, helpful, and concise response (2 to 4 sentences) suitable for a Google search 'AI Overview'. "
                        f"Highlight key details (like skills, projects, and experiences) in bold."
                    )
                
                ai_result = call_azure_agent(prompt)
                elapsed = round(time.time() - t0, 2)

                st.session_state.results = results
                st.session_state.elapsed = elapsed
                st.session_state.ai_snippet = ai_result
                st.session_state.search_loading = False

        results = st.session_state.results
        elapsed = st.session_state.elapsed
        ai_info = st.session_state.ai_snippet

        # Stats bar
        src_label = f"Azure AI Foundry · {AGENT_NAME} v{AGENT_VERSION}"
        st.markdown(
            f'<div class="result-stats">About {len(results)} results ({elapsed:.2f} seconds) · {src_label}</div>',
            unsafe_allow_html=True
        )

        # Error banner
        if isinstance(ai_info, dict) and ai_info.get("error"):
            st.error(f"⚠ Azure agent error: {ai_info['text']}")

        # AI Overview Card
        if isinstance(ai_info, dict) and not ai_info.get("error") and ai_info.get("text"):
            formatted_text = format_ai_text(ai_info["text"])
            st.markdown(f"""
            <div class="ai-overview-container">
              <div class="ai-overview-title-bar">
                <div class="ai-overview-sparkles">✦</div>
                <span style="font-family: 'Google Sans', Arial, sans-serif; font-size: 16px; font-weight: 500; color: #1f1f1f;">AI Overview</span>
              </div>
              <div class="ai-overview-content">
                {formatted_text}
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Results
        active_tab = st.session_state.get("active_tab", "All")
        fav_colors = {"S": "#4285F4", "P": "#24292e", "L": "#0A66C2", "E": "#34A853"}
        for r in results:
            if active_tab in ("Skills", "Projects") and r["favicon"] != "L":
                continue
            color = fav_colors.get(r["favicon"], "#4285F4")
            url = r["url"]
            if not url.startswith("http") and not url.startswith("mailto:"):
                url = "https://" + url
            st.markdown(f"""
            <div class="result-card">
              <div class="result-url">
                <span class="result-favicon" style="background:{color}">{r['favicon']}</span>
                <span class="result-url-text">{r['url']}</span>
              </div>
              <a class="result-title" href="{url}" target="_blank">{r['title']}</a>
              <div class="result-snippet">{r['snippet']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Sidebar: Chat Panel (Powered by Azure Agent) ──
    with side_col:
        st.markdown("<div style='padding:16px 20px 0 0;'>", unsafe_allow_html=True)

        # Chat panel
        st.markdown("""
        <div class="chat-wrap">
          <div class="chat-header">
            🤖 Shubham Resume Agent
            <span style="font-size:11px;opacity:0.85;">Azure AI Foundry · gpt-4.1-mini</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Messages
        msgs_html = ""
        for m in st.session_state.chat_messages_ui:
            cls = "msg-bot" if m["role"] == "bot" else "msg-user"
            msgs_html += f'<div class="{cls}">{m["text"]}</div>'

        st.markdown(f"""
        <div style="background:#f8f9fa;border:1px solid #e8eaed;border-radius:0 0 8px 8px;
                    padding:12px;max-height:280px;overflow-y:auto;display:flex;
                    flex-direction:column;gap:8px;">
          {msgs_html}
        </div>
        """, unsafe_allow_html=True)

        # Input
        chat_q = st.text_input(
            "Chat", placeholder="Ask about Shubham...",
            key="chat_input_field", label_visibility="collapsed"
        )
        c1, c2 = st.columns([3, 1])
        with c2:
            send = st.button("Send →", key="chat_send", use_container_width=True)

        if send and chat_q.strip():
            st.session_state.chat_messages_ui.append({"role": "user", "text": chat_q})
            st.session_state.chat_messages_ui.append({"role": "bot", "text": "⏳ Asking Azure agent..."})
            st.rerun()

        # Process pending "thinking" message
        msgs = st.session_state.chat_messages_ui
        if msgs and msgs[-1]["text"] == "⏳ Asking Azure agent...":
            user_msg = msgs[-2]["text"]
            result = call_azure_agent(user_msg, st.session_state.chat_history)

            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            st.session_state.chat_history.append({"role": "assistant", "content": result["text"]})
            st.session_state.chat_messages_ui[-1] = {"role": "bot", "text": result["text"]}
            st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)
