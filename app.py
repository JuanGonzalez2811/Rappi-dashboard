import streamlit as st
import plotly.graph_objects as go
from data_loader import load_all_data, records_to_summary
from chatbot import chat

st.set_page_config(
    page_title="Rappi Store Availability",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand tokens ───────────────────────────────────────────────────────────────
RAPPI_RED    = "#FF441C"
RAPPI_LIGHT  = "rgba(255,68,28,0.08)"
BG_PAGE      = "#F7F7F8"
BG_CARD      = "#FFFFFF"
BG_SIDEBAR   = "#FFFFFF"
BORDER       = "#EBEBEB"
TEXT_PRIMARY = "#1A1A1A"
TEXT_MUTED   = "#8A8A9A"
GRID_COLOR   = "#F0F0F0"

RAPPI_LOGO_SVG = """
<svg width="90" height="26" viewBox="0 0 90 26" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="26" height="26" rx="6" fill="#FF441C"/>
  <text x="5" y="19" font-family="Arial Black,Arial" font-weight="900" font-size="16" fill="white">R</text>
  <text x="32" y="19" font-family="Arial Black,Arial" font-weight="900" font-size="16" fill="#FF441C">rappi</text>
</svg>
"""

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
  /* ── Font ───────────────────────────────────────────────── */
  html, body, [class*="css"], * {{
    font-family: 'Nunito', sans-serif !important;
  }}

  /* ── Base ───────────────────────────────────────────────── */
  [data-testid="stAppViewContainer"] {{ background: {BG_PAGE} !important; }}
  [data-testid="stSidebar"] {{
    background: {BG_SIDEBAR} !important;
    border-right: 1px solid {BORDER} !important;
  }}
  .block-container {{ padding-top: 1.2rem !important; padding-bottom: 2rem !important; }}
  html, body, [class*="css"] {{ color: {TEXT_PRIMARY}; }}

  /* ── Inputs & dropdowns ─────────────────────────────────── */
  input, textarea, select,
  [data-baseweb="input"] input,
  [data-baseweb="select"] div,
  [data-baseweb="textarea"] textarea {{
    background: #FAFAFA !important;
    color: {TEXT_PRIMARY} !important;
    border-color: {BORDER} !important;
  }}
  [data-baseweb="popover"], [data-baseweb="menu"], ul[role="listbox"] {{
    background: #FFFFFF !important;
    border: 1px solid {BORDER} !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
  }}
  li[role="option"], [role="option"] {{ background: #FFFFFF !important; color: {TEXT_PRIMARY} !important; }}
  li[role="option"]:hover, [role="option"]:hover, [aria-selected="true"] {{
    background: {RAPPI_LIGHT} !important; color: {RAPPI_RED} !important;
  }}
  [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {{ background: {RAPPI_RED} !important; }}

  /* ── KPI cards ──────────────────────────────────────────── */
  .kpi-card {{
    background: {BG_CARD};
    border-radius: 10px;
    padding: 16px 18px;
    border: 1px solid {BORDER};
    border-top: 2px solid {RAPPI_RED};
  }}
  .kpi-card .val {{ font-size: 1.75rem; font-weight: 800; color: {TEXT_PRIMARY}; line-height: 1.1; }}
  .kpi-card .lbl {{ font-size: 0.72rem; font-weight: 600; color: {TEXT_MUTED}; margin-top: 4px; letter-spacing: .03em; }}

  /* ── Section titles ─────────────────────────────────────── */
  .section-title {{
    font-size: 0.7rem; font-weight: 700; color: {TEXT_MUTED};
    text-transform: uppercase; letter-spacing: .1em; margin: 16px 0 8px;
  }}

  /* ── Light HTML table ───────────────────────────────────── */
  .light-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
  .light-table th {{
    text-align: left; padding: 7px 12px;
    font-size: 0.68rem; font-weight: 600; color: {TEXT_MUTED};
    text-transform: uppercase; letter-spacing: .06em;
    border-bottom: 1px solid {BORDER}; background: #FAFAFA;
  }}
  .light-table td {{
    padding: 7px 12px; color: {TEXT_PRIMARY};
    border-bottom: 1px solid {BORDER};
  }}
  .light-table tr:last-child td {{ border-bottom: none; }}
  .light-table tr:hover td {{ background: {RAPPI_LIGHT}; }}
  .table-wrap {{
    background: {BG_CARD}; border: 1px solid {BORDER};
    border-radius: 10px; overflow: hidden; margin-top: 4px;
  }}

  /* ── Chat ───────────────────────────────────────────────── */
  [data-testid="stChatMessage"] {{
    background: {BG_CARD} !important;
    border: 1px solid {BORDER}; border-radius: 10px; margin-bottom: 6px;
  }}
  [data-testid="stChatMessage"] p,
  [data-testid="stChatMessage"] span,
  [data-testid="stChatMessage"] div,
  [data-testid="stChatMessage"] li,
  [data-testid="stChatMessage"] strong,
  [data-testid="stChatMessage"] em,
  [data-testid="stChatMessage"] code {{
    color: {TEXT_PRIMARY} !important;
  }}
  [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] * {{
    color: {TEXT_PRIMARY} !important;
  }}
  [data-testid="stChatInput"] textarea {{
    background: {BG_CARD} !important; color: {TEXT_PRIMARY} !important;
    border-color: {BORDER} !important;
  }}

  /* ── Tabs ────────────────────────────────────────────────── */
  button[data-baseweb="tab"] {{ font-weight: 600 !important; color: {TEXT_MUTED} !important; font-size: 0.84rem !important; }}
  button[data-baseweb="tab"][aria-selected="true"] {{ color: {RAPPI_RED} !important; border-bottom-color: {RAPPI_RED} !important; }}

  /* ── Sidebar ─────────────────────────────────────────────── */
  .sidebar-section {{
    font-size: 0.68rem; font-weight: 700; color: {TEXT_MUTED};
    text-transform: uppercase; letter-spacing: .08em; margin: 14px 0 4px;
  }}
  .sidebar-divider {{ border: none; border-top: 1px solid {BORDER}; margin: 10px 0; }}

  /* ── Header ─────────────────────────────────────────────── */
  .page-header {{ margin-bottom: 4px; }}
  .page-header h1 {{ font-size: 1.3rem; font-weight: 800; color: {TEXT_PRIMARY}; margin: 0; display: inline; }}
  .page-header .badge {{
    background: {RAPPI_LIGHT}; color: {RAPPI_RED};
    font-size: 0.65rem; font-weight: 700; padding: 2px 8px;
    border-radius: 20px; letter-spacing: .04em; margin-left: 10px;
    vertical-align: middle;
  }}
  .page-meta {{ font-size: 0.75rem; color: {TEXT_MUTED}; margin: 3px 0 16px; }}

  /* ── Buttons ─────────────────────────────────────────────── */
  .stButton > button {{
    border: 1px solid {BORDER} !important; background: {BG_CARD} !important;
    color: {TEXT_MUTED} !important; border-radius: 7px !important;
    font-size: 0.78rem !important; font-weight: 500 !important; padding: 5px 10px !important;
  }}
  .stButton > button:hover {{
    border-color: {RAPPI_RED} !important; color: {RAPPI_RED} !important;
    background: {RAPPI_LIGHT} !important;
  }}

  hr {{ border-color: {BORDER} !important; }}

  /* ── Sidebar labels & slider text ──────────────────────── */
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] .stSlider label,
  [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
  [data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {{
    color: {TEXT_PRIMARY} !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
  }}
  [data-testid="stSidebar"] [data-testid="stTickBarMin"],
  [data-testid="stSidebar"] [data-testid="stTickBarMax"] {{
    color: {TEXT_MUTED} !important;
  }}

  /* ── Chat input placeholder ─────────────────────────────── */
  [data-testid="stChatInput"] textarea::placeholder {{
    color: #AAAAAA !important;
  }}
  [data-testid="stChatInput"] textarea {{
    color: {TEXT_PRIMARY} !important;
  }}
</style>
""", unsafe_allow_html=True)


# ── Data (cached) ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Cargando datos…")
def get_data():
    records = load_all_data()
    summary = records_to_summary(records)
    return records, summary


records, summary = get_data()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(RAPPI_LOGO_SVG, unsafe_allow_html=True)
    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Filtros</div>', unsafe_allow_html=True)

    all_dates = sorted({r["timestamp"].date() for r in records})
    min_d, max_d = all_dates[0], all_dates[-1]
    date_range = st.date_input("Rango de fechas", value=(min_d, max_d),
                               min_value=min_d, max_value=max_d)
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_d, end_d = date_range
    else:
        start_d, end_d = min_d, max_d

    st.markdown("<br>", unsafe_allow_html=True)
    hour_range = st.slider("Hora del día (Colombia)", 0, 23, (0, 23))

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Acerca del dato</div>', unsafe_allow_html=True)
    st.markdown(
        f"<p style='font-size:0.78rem;color:{TEXT_PRIMARY};line-height:1.5;margin:0'>"
        "Mide cada 10 segundos cuántos puntos de venta son visibles para los usuarios. "
        "Feb 1–11, 2026.</p>",
        unsafe_allow_html=True,
    )


# ── Filter ─────────────────────────────────────────────────────────────────────
filtered = [
    r for r in records
    if start_d <= r["timestamp"].date() <= end_d
    and hour_range[0] <= r["timestamp"].hour <= hour_range[1]
]
fsummary = records_to_summary(filtered) if filtered else {}


# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(
    f"<div class='page-header'>"
    f"<h1>Store Availability</h1>"
    f"<span class='badge'>Feb 2026</span>"
    f"</div>"
    f"<p class='page-meta'>{summary.get('date_range','—')} · {summary.get('days_covered',0)} días · {len(records):,} registros</p>",
    unsafe_allow_html=True,
)

# ── KPI cards ──────────────────────────────────────────────────────────────────
if fsummary:
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, f"{fsummary['overall_avg']:,.0f}", "Promedio tiendas"),
        (c2, f"{fsummary['overall_max']:,.0f}", "Pico máximo"),
        (c3, f"{fsummary['peak_hour']:02d}:00 hs",  "Hora más activa"),
        (c4, f"{fsummary['overall_avg']/fsummary['overall_max']*100:.1f}%", "Avg / pico"),
    ]
    for col, val, lbl in kpis:
        with col:
            st.markdown(
                f'<div class="kpi-card">'
                f'<div class="val">{val}</div>'
                f'<div class="lbl">{lbl}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Tendencia", "Patrones", "Por día", "Asistente"])


# ── Shared chart layout helper ─────────────────────────────────────────────────
def light_layout(**kwargs):
    base = dict(
        plot_bgcolor=BG_CARD,
        paper_bgcolor=BG_CARD,
        font=dict(color=TEXT_PRIMARY, family="Inter, Arial, sans-serif", size=12),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    base.update(kwargs)
    return base


def light_axes():
    return dict(
        xargs=dict(showgrid=False, color=TEXT_MUTED, linecolor=BORDER,
                   tickfont=dict(color=TEXT_MUTED, size=11)),
        yargs=dict(showgrid=True, gridcolor=GRID_COLOR, color=TEXT_MUTED,
                   linecolor=BORDER, tickfont=dict(color=TEXT_MUTED, size=11)),
    )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Timeline
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Disponibilidad de tiendas en el tiempo</div>',
                unsafe_allow_html=True)
    if filtered:
        step    = max(1, len(filtered) // 2000)
        sampled = filtered[::step]
        xs      = [r["timestamp"] for r in sampled]
        ys      = [r["value"]     for r in sampled]
        w       = max(1, len(ys) // 60)
        avg     = [sum(ys[max(0,i-w):i+1]) / min(i+1, w) for i in range(len(ys))]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="lines", name="Visible stores",
            line=dict(color=RAPPI_RED, width=1.5),
            fill="tozeroy", fillcolor=RAPPI_LIGHT,
        ))
        fig.add_trace(go.Scatter(
            x=xs, y=avg, mode="lines", name="Media móvil",
            line=dict(color="#C0C0CC", width=2, dash="dot"),
        ))
        ax = light_axes()
        fig.update_layout(
            **light_layout(height=380),
            xaxis_title="", yaxis_title="Visible stores",
            hovermode="x unified",
            legend=dict(orientation="h", y=1.06, x=1, xanchor="right",
                        font=dict(color=TEXT_MUTED, size=11),
                        bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
        )
        fig.update_xaxes(**ax["xargs"])
        fig.update_yaxes(**ax["yargs"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sin datos para los filtros seleccionados.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Patterns
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-title">Promedio por hora del día</div>',
                    unsafe_allow_html=True)
        if fsummary.get("avg_by_hour"):
            hours  = sorted(fsummary["avg_by_hour"])
            vals   = [fsummary["avg_by_hour"][h] for h in hours]
            max_v  = max(vals)
            colors = [RAPPI_RED if v == max_v else "rgba(255,68,28,0.25)" for v in vals]
            ax     = light_axes()
            fig_h  = go.Figure(go.Bar(
                x=[f"{h:02d}:00" for h in hours], y=vals,
                marker_color=colors, marker_line_width=0,
                hovertemplate="%{x}: %{y:,.0f}<extra></extra>",
            ))
            fig_h.update_layout(**light_layout(height=280))
            fig_h.update_xaxes(**ax["xargs"])
            fig_h.update_yaxes(**ax["yargs"])
            st.plotly_chart(fig_h, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Promedio por día de semana</div>',
                    unsafe_allow_html=True)
        if fsummary.get("avg_by_weekday"):
            order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            es    = {"Monday":"Lun","Tuesday":"Mar","Wednesday":"Mié",
                     "Thursday":"Jue","Friday":"Vie","Saturday":"Sáb","Sunday":"Dom"}
            wdays = [d for d in order if d in fsummary["avg_by_weekday"]]
            wvals = [fsummary["avg_by_weekday"][d] for d in wdays]
            ax    = light_axes()
            fig_w = go.Figure(go.Bar(
                x=[es[d] for d in wdays], y=wvals,
                marker_color=RAPPI_RED, marker_line_width=0,
                hovertemplate="%{x}: %{y:,.0f}<extra></extra>",
            ))
            fig_w.update_layout(**light_layout(height=280))
            fig_w.update_xaxes(**ax["xargs"])
            fig_w.update_yaxes(**ax["yargs"])
            st.plotly_chart(fig_w, use_container_width=True)

    st.markdown('<div class="section-title">Heatmap — Hora × Día de semana</div>',
                unsafe_allow_html=True)
    if filtered:
        wn  = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
        mat = {w: {h: [] for h in range(24)} for w in wn}
        for r in filtered:
            wd = wn[r["timestamp"].weekday()]
            mat[wd][r["timestamp"].hour].append(r["value"])
        z = [[
            (sum(mat[w][h])/len(mat[w][h])) if mat[w][h] else None
            for h in range(24)
        ] for w in wn]
        ax = light_axes()
        fig_hm = go.Figure(go.Heatmap(
            z=z,
            x=[f"{h:02d}:00" for h in range(24)],
            y=wn,
            colorscale=[[0,"#FFF0EC"],[0.5,"#FF9070"],[1, RAPPI_RED]],
            hoverongaps=False,
            hovertemplate="Hora: %{x}<br>Día: %{y}<br>Avg: %{z:,.0f}<extra></extra>",
            colorbar=dict(title="Avg", thickness=10,
                          tickfont=dict(color=TEXT_MUTED, size=10)),
        ))
        fig_hm.update_layout(**light_layout(height=240))
        fig_hm.update_xaxes(**ax["xargs"])
        fig_hm.update_yaxes(**ax["yargs"])
        st.plotly_chart(fig_hm, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Calendar
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Promedio diario</div>', unsafe_allow_html=True)
    if fsummary.get("avg_by_day"):
        days  = sorted(fsummary["avg_by_day"])
        dvals = [fsummary["avg_by_day"][d] for d in days]
        ax    = light_axes()
        fig_d = go.Figure(go.Bar(
            x=days, y=dvals,
            marker_color=RAPPI_RED, marker_line_width=0,
            hovertemplate="%{x}: %{y:,.0f}<extra></extra>",
        ))
        fig_d.update_layout(**light_layout(height=300))
        fig_d.update_xaxes(**ax["xargs"])
        fig_d.update_yaxes(**ax["yargs"])
        st.plotly_chart(fig_d, use_container_width=True)

    if filtered:
        st.markdown('<div class="section-title">Detalle por día</div>',
                    unsafe_allow_html=True)
        by_day = {}
        for r in filtered:
            by_day.setdefault(r["timestamp"].date().isoformat(), []).append(r["value"])

        rows_html = "".join(
            f"<tr><td>{d}</td><td>{sum(v)/len(v):,.0f}</td>"
            f"<td>{max(v):,.0f}</td><td>{min(v):,.0f}</td></tr>"
            for d, v in sorted(by_day.items())
        )
        st.markdown(
            f'<div class="table-wrap"><table class="light-table">'
            f'<thead><tr><th>Fecha</th><th>Promedio</th><th>Pico</th><th>Mínimo</th></tr></thead>'
            f'<tbody>{rows_html}</tbody></table></div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — AI Chatbot
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown(
        '<div class="section-title">Asistente IA — Pregunta sobre los datos</div>',
        unsafe_allow_html=True,
    )
    st.caption("Llama 3.3 70B via Groq · datos: Feb 1–11, 2026")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if not st.session_state.chat_history:
        st.markdown(
            f"<p style='font-size:0.82rem;color:{TEXT_MUTED};margin-bottom:8px'>"
            f"Preguntas frecuentes:</p>",
            unsafe_allow_html=True,
        )
        suggestions = [
            "¿Cuál es el horario con más tiendas disponibles?",
            "¿Hay diferencia entre semana y fin de semana?",
            "¿Cuál fue el día con menor disponibilidad?",
            "¿A qué hora ocurre la mayor caída de tiendas?",
        ]
        c1, c2 = st.columns(2)
        for i, s in enumerate(suggestions):
            if (c1 if i % 2 == 0 else c2).button(s, key=f"sug_{i}"):
                st.session_state._pending = s
                st.rerun()

    for msg in st.session_state.chat_history:
        avatar = "🧑" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    pending    = st.session_state.pop("_pending", None)
    user_input = st.chat_input("Ej: ¿Cuáles son las horas pico de disponibilidad?")
    question   = pending or user_input

    if question and question.strip():
        st.session_state.chat_history.append({"role": "user", "content": question.strip()})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(question.strip())

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Pensando…"):
                try:
                    response = chat(
                        messages=st.session_state.chat_history,
                        summary=summary,
                    )
                except Exception as e:
                    err = str(e)
                    response = (
                        "⚠️ No se encontró GROQ_API_KEY. Obtén una gratis en groq.com y ejecuta: `export GROQ_API_KEY=gsk_...`"
                        if "api_key" in err.lower() or "authentication" in err.lower()
                        else f"Error: {err}"
                    )
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    if st.session_state.chat_history:
        if st.button("Limpiar conversación"):
            st.session_state.chat_history = []
            st.rerun()
