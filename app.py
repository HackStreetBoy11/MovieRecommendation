import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movierecommendation-xxv3.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
TMDB_IMG_ORIGINAL = "https://image.tmdb.org/t/p/original"

st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================
# DESIGN SYSTEM
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Root tokens ─────────────────────────────────── */
:root {
    --bg:        #0b0c10;
    --surface:   #13151c;
    --surface2:  #1c1f2a;
    --border:    rgba(255,255,255,0.07);
    --accent:    #e8b84b;
    --accent2:   #c96c3c;
    --text:      #e8e9ed;
    --muted:     #7b7f91;
    --radius:    14px;
    --radius-sm: 8px;
}

/* ── Global reset ────────────────────────────────── */
html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

/* Remove Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.5rem 2rem 4rem !important;
    max-width: 1480px !important;
}

/* ── Sidebar ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.06em;
    color: var(--accent);
    margin-bottom: 0.2rem;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown li {
    color: var(--muted) !important;
    font-size: 0.85rem;
}

/* ── Buttons ─────────────────────────────────────── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    padding: 0.3rem 0.6rem !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    color: var(--bg) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 18px rgba(232,184,75,0.25) !important;
}

/* Back / primary button */
.back-btn .stButton > button {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.2rem !important;
    width: auto !important;
}
.back-btn .stButton > button:hover {
    background: var(--surface) !important;
    border-color: var(--muted) !important;
    color: var(--text) !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Inputs ──────────────────────────────────────── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(232,184,75,0.12) !important;
}
.stTextInput label, .stSelectbox label, .stSlider label {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── Slider ──────────────────────────────────────── */
.stSlider [data-testid="stSlider"] > div > div > div {
    background: var(--accent) !important;
}

/* ── Divider ─────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Custom components ───────────────────────────── */
.page-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    letter-spacing: 0.06em;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0 0 0.2rem 0;
}
.page-sub {
    color: var(--muted);
    font-size: 0.88rem;
    font-weight: 300;
    letter-spacing: 0.02em;
    margin-bottom: 1.8rem;
}

/* Movie card */
.movie-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    cursor: pointer;
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.55);
    border-color: rgba(232,184,75,0.3);
}
.movie-card img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
}
.movie-card-body {
    padding: 10px 12px 12px;
}
.movie-card-title {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text);
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 2.15em;
    margin-bottom: 4px;
}
.movie-card-meta {
    font-size: 0.72rem;
    color: var(--muted);
    font-weight: 300;
}
.rating-badge {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    background: rgba(232,184,75,0.15);
    color: var(--accent);
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 0.72rem;
    font-weight: 500;
}
.no-poster {
    width: 100%;
    aspect-ratio: 2/3;
    background: var(--surface2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    color: var(--muted);
}

/* Section label */
.section-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.35rem;
    letter-spacing: 0.08em;
    color: var(--text);
    margin: 2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Details page */
.details-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem;
}
.details-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(1.8rem, 4vw, 3rem);
    letter-spacing: 0.04em;
    color: var(--text);
    line-height: 1.05;
    margin-bottom: 0.4rem;
}
.meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 1rem;
    align-items: center;
}
.meta-chip {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    color: var(--muted);
    font-weight: 300;
}
.genre-chip {
    background: rgba(232,184,75,0.1);
    border: 1px solid rgba(232,184,75,0.25);
    color: var(--accent);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 500;
}
.overview-text {
    font-size: 0.93rem;
    font-weight: 300;
    line-height: 1.7;
    color: rgba(232,233,237,0.85);
    margin-top: 1.2rem;
}
.section-heading {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    margin-bottom: 0.4rem;
    margin-top: 1.4rem;
    font-weight: 500;
}

/* Category pills in sidebar */
.stSelectbox [data-testid="stSelectbox"] > div {
    background: var(--surface2) !important;
}

/* Error / info boxes */
.stAlert {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }
</style>
""",
    unsafe_allow_html=True,
)


# =============================
# STATE + ROUTING
# =============================
def _init_state():
    if "view" not in st.session_state:
        st.session_state.view = "home"
    if "selected_tmdb_id" not in st.session_state:
        st.session_state.selected_tmdb_id = None
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""


_init_state()

# Sync from query params on first load
qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except (ValueError, TypeError):
        pass


def goto_home():
    st.session_state.view = "home"
    st.session_state.selected_tmdb_id = None
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=300)
def api_get_json_cached(path: str, params_str: str = ""):
    """Cached version for stable data (details, home feed)."""
    import json
    params = json.loads(params_str) if params_str else None
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=30)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.HTTPError as e:
        return None, f"Server error {e.response.status_code}"
    except requests.exceptions.ConnectionError:
        return None, "Connection failed — is the server running?"
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except Exception as e:
        return None, f"Unexpected error: {e}"


def api_get_json(path: str, params=None):
    """Uncached version for search (always fresh)."""
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=30)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.HTTPError as e:
        return None, f"Server error {e.response.status_code}"
    except requests.exceptions.ConnectionError:
        return None, "Connection failed — is the server running?"
    except requests.exceptions.Timeout:
        return None, "Request timed out."
    except Exception as e:
        return None, f"Error: {e}"


def api_get_json_stable(path: str, params=None):
    import json
    params_str = json.dumps(params, sort_keys=True) if params else ""
    return api_get_json_cached(path, params_str)


# =============================
# PARSE / NORMALISE HELPERS
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw_items = []
        for m in (data.get("results") or []):
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average"),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": m.get("poster_url"),
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average"),
            })
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = final_list[:limit]
    return suggestions, cards


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in (tfidf_items or []):
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id": tmdb["tmdb_id"],
                "title": tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
                "vote_average": tmdb.get("vote_average"),
                "release_date": tmdb.get("release_date", ""),
            })
    return cards


def star_rating(score):
    """Convert 0-10 score to ★ display."""
    if score is None:
        return ""
    try:
        score = float(score)
        return f"★ {score:.1f}"
    except (ValueError, TypeError):
        return ""


# =============================
# POSTER GRID
# =============================
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.markdown(
            "<p style='color:var(--muted);font-size:0.88rem;padding:1rem 0;'>No movies to display.</p>",
            unsafe_allow_html=True,
        )
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        col_set = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            year = (m.get("release_date") or "")[:4]
            rating = star_rating(m.get("vote_average"))

            with col_set[c]:
                # Build card HTML
                poster_html = (
                    f"<img src='{poster}' alt='{title}' loading='lazy' />"
                    if poster
                    else "<div class='no-poster'>🎬</div>"
                )
                rating_html = (
                    f"<span class='rating-badge'>{rating}</span>" if rating else ""
                )
                year_html = (
                    f"<span class='movie-card-meta'>{year}</span>" if year else ""
                )

                st.markdown(
                    f"""
                    <div class='movie-card'>
                        {poster_html}
                        <div class='movie-card-body'>
                            <div class='movie-card-title'>{title}</div>
                            <div style='display:flex;justify-content:space-between;align-items:center;gap:4px;flex-wrap:wrap;'>
                                {year_html}
                                {rating_html}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button("Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("## 🎬 CineMatch")
    st.markdown(
        "<p style='color:var(--muted);font-size:0.8rem;margin-top:-0.5rem;'>Your personal movie guide</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    if st.button("🏠  Home"):
        goto_home()

    st.divider()

    st.markdown(
        "<p style='color:var(--muted);font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;font-weight:500;margin-bottom:0.5rem;'>Browse Category</p>",
        unsafe_allow_html=True,
    )
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed",
        format_func=lambda x: {
            "trending": "🔥 Trending",
            "popular": "📈 Popular",
            "top_rated": "⭐ Top Rated",
            "now_playing": "🎥 Now Playing",
            "upcoming": "📅 Upcoming",
        }.get(x, x),
    )

    st.divider()

    st.markdown(
        "<p style='color:var(--muted);font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;font-weight:500;margin-bottom:0.5rem;'>Grid Columns</p>",
        unsafe_allow_html=True,
    )
    grid_cols = st.slider("Columns", 3, 8, 6, label_visibility="collapsed")

    st.divider()
    st.markdown(
        "<p style='color:var(--muted);font-size:0.72rem;'>Powered by TMDB & TF-IDF recommendations.</p>",
        unsafe_allow_html=True,
    )


# =============================
# VIEW: HOME
# =============================
if st.session_state.view == "home":

    # Header
    st.markdown("<div class='page-header'>CineMatch</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-sub'>Discover, explore, and find movies tailored to your taste.</div>",
        unsafe_allow_html=True,
    )

    # Search bar
    typed = st.text_input(
        "Search",
        placeholder="🔍   Search by title — try 'Inception', 'Batman', 'Love'...",
        label_visibility="collapsed",
        key="search_input",
    )

    if typed.strip():
        # ── SEARCH MODE ──────────────────────────────
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            with st.spinner("Searching..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"⚠️ Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                if suggestions:
                    labels = ["— Select a movie to jump to details —"] + [s[0] for s in suggestions]
                    selected = st.selectbox(
                        "Suggestions",
                        labels,
                        index=0,
                        label_visibility="collapsed",
                    )
                    if selected != labels[0]:
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])

                result_count = len(cards)
                st.markdown(
                    f"<div class='section-label'>Results <span style='font-family:DM Sans;font-size:0.8rem;color:var(--muted);font-weight:300;letter-spacing:0;'>&nbsp;{result_count} found</span></div>",
                    unsafe_allow_html=True,
                )

                if cards:
                    poster_grid(cards, cols=grid_cols, key_prefix="search_results")
                else:
                    st.info("No results matched. Try a different keyword.")

    else:
        # ── HOME FEED MODE ───────────────────────────
        label_map = {
            "trending": "🔥 Trending Now",
            "popular": "📈 Popular",
            "top_rated": "⭐ Top Rated",
            "now_playing": "🎥 Now Playing",
            "upcoming": "📅 Upcoming Releases",
        }
        st.markdown(
            f"<div class='section-label'>{label_map.get(home_category, home_category)}</div>",
            unsafe_allow_html=True,
        )

        with st.spinner("Loading movies..."):
            home_cards, err = api_get_json_stable(
                "/home", params={"category": home_category, "limit": 24}
            )

        if err or not home_cards:
            st.error(f"⚠️ Could not load feed: {err or 'Empty response from server.'}")
        else:
            poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No movie selected.")
        with st.container():
            st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
            if st.button("← Back to Home"):
                goto_home()
            st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # ── Back button ──────────────────────────────────
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        goto_home()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Fetch details ────────────────────────────────
    with st.spinner("Loading movie details..."):
        data, err = api_get_json_stable(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"⚠️ Could not load details: {err or 'Empty response.'}")
        st.stop()

    # ── Backdrop ─────────────────────────────────────
    if data.get("backdrop_url"):
        st.markdown(
            f"""
            <div style="position:relative;width:100%;margin-bottom:1.5rem;border-radius:{12}px;overflow:hidden;max-height:380px;">
                <img src="{data['backdrop_url']}" style="width:100%;height:380px;object-fit:cover;opacity:0.55;display:block;" />
                <div style="position:absolute;inset:0;background:linear-gradient(to right,rgba(11,12,16,0.95) 0%,rgba(11,12,16,0.4) 60%,rgba(11,12,16,0.1) 100%);"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Details layout ───────────────────────────────
    left, right = st.columns([1, 2.6], gap="large")

    with left:
        poster = data.get("poster_url")
        if poster:
            st.image(poster, use_column_width=True)
        else:
            st.markdown(
                "<div style='background:var(--surface2);border-radius:12px;aspect-ratio:2/3;display:flex;align-items:center;justify-content:center;font-size:3rem;color:var(--muted);'>🎬</div>",
                unsafe_allow_html=True,
            )

    with right:
        title = data.get("title", "Unknown Title")
        release = (data.get("release_date") or "")[:4]
        runtime = data.get("runtime")
        vote = data.get("vote_average")
        vote_count = data.get("vote_count")
        genres = data.get("genres", [])
        overview = data.get("overview") or "No overview available."
        tagline = data.get("tagline", "")

        st.markdown(f"<div class='details-title'>{title}</div>", unsafe_allow_html=True)

        if tagline:
            st.markdown(
                f"<p style='color:var(--muted);font-style:italic;font-size:0.9rem;margin-top:-0.3rem;margin-bottom:0.8rem;'>\u201c{tagline}\u201d</p>",
                unsafe_allow_html=True,
            )

        # Meta chips
        chips_html = ""
        if release:
            chips_html += f"<span class='meta-chip'>📅 {release}</span>"
        if runtime:
            h, m = divmod(int(runtime), 60)
            rt_str = f"{h}h {m}m" if h else f"{m}m"
            chips_html += f"<span class='meta-chip'>⏱ {rt_str}</span>"
        if vote is not None:
            try:
                chips_html += f"<span class='rating-badge'>★ {float(vote):.1f}</span>"
            except (ValueError, TypeError):
                pass
        if vote_count:
            chips_html += f"<span class='meta-chip'>{int(vote_count):,} votes</span>"

        if chips_html:
            st.markdown(f"<div class='meta-row'>{chips_html}</div>", unsafe_allow_html=True)

        # Genres
        if genres:
            genre_html = " ".join(
                [f"<span class='genre-chip'>{g['name']}</span>" for g in genres]
            )
            st.markdown(f"<div class='meta-row'>{genre_html}</div>", unsafe_allow_html=True)

        # Overview
        st.markdown("<div class='section-heading'>Overview</div>", unsafe_allow_html=True)
        st.markdown(f"<p class='overview-text'>{overview}</p>", unsafe_allow_html=True)

    st.divider()

    # ── Recommendations ──────────────────────────────
    title_clean = (data.get("title") or "").strip()

    if title_clean:
        with st.spinner("Finding recommendations..."):
            bundle, err2 = api_get_json_stable(
                "/movie/search",
                params={"query": title_clean, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            genre_cards = bundle.get("genre_recommendations", [])

            if tfidf_cards:
                st.markdown(
                    "<div class='section-label'>🔎 Similar Movies</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(tfidf_cards, cols=grid_cols, key_prefix="details_tfidf")

            if genre_cards:
                st.markdown(
                    "<div class='section-label'>🎭 More in This Genre</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(genre_cards, cols=grid_cols, key_prefix="details_genre")

            if not tfidf_cards and not genre_cards:
                st.info("No recommendations found for this title.")

        else:
            # Graceful fallback to genre-only
            with st.spinner("Loading genre recommendations..."):
                genre_only, err3 = api_get_json_stable(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )

            if not err3 and genre_only:
                st.markdown(
                    "<div class='section-label'>🎭 More in This Genre</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(genre_only, cols=grid_cols, key_prefix="genre_fallback")
            else:
                st.info("Recommendations are not available right now.")
    else:
        st.info("No title available to compute recommendations.")