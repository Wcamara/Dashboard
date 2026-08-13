import streamlit as st


def html(content):
    st.html(content)


def apply_global_style():
    html("""
    <style>

    :root {
        --bg: #080b10;
        --sidebar: #0d1117;
        --card: #11161f;
        --card-hover: #151b26;
        --card-inner: #0d121a;
        --border: #202733;

        --text: #f4f7fb;
        --muted: #7d8590;

        --blue: #5b8cff;
        --green: #38d996;
        --red: #ff647c;
        --yellow: #f6c453;
    }


    /* =====================================================
       APP
    ===================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"] {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stMain"] {
        background: var(--bg);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }


    /* =====================================================
       CONTAINER PRINCIPAL
    ===================================================== */

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       SIDEBAR
    ===================================================== */

    [data-testid="stSidebar"] {
        background: var(--sidebar);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebarNav"] a {
        border-radius: 8px;
        margin: 3px 8px;
        transition: background .15s ease;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: #171d28;
    }

    [data-testid="stSidebarNav"] span {
        color: #c4cad3;
    }


    /* =====================================================
       TIPOGRAFIA
    ===================================================== */

    body,
    p,
    span,
    div,
    button,
    input,
    textarea,
    select {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }


    /* =====================================================
       HEADER
    ===================================================== */

    .page-header,
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 28px;
    }

    .page-title,
    .dashboard-title {
        color: var(--text);
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -1px;
    }

    .page-subtitle,
    .dashboard-subtitle {
        color: var(--muted);
        margin-top: 5px;
        font-size: 14px;
    }

    .dashboard-date {
        color: var(--muted);
        font-size: 13px;
    }


    /* =====================================================
       SEÇÕES
    ===================================================== */

    .section-label {
        color: #6f7783;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        margin-bottom: 9px;
    }

    .section-title,
    .panel-title {
        color: var(--text);
        font-size: 17px;
        font-weight: 650;
    }

    .section-subtitle,
    .panel-subtitle {
        color: var(--muted);
        font-size: 12px;
        margin-top: 3px;
    }


    /* =====================================================
       PAINÉIS
    ===================================================== */

    .panel {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 22px;
        min-height: 285px;
    }


    /* =====================================================
       MÉTRICAS
    ===================================================== */

    .metric-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;

        transition:
            transform .15s ease,
            background .15s ease,
            border-color .15s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        background: var(--card-hover);
        border-color: #303949;
    }

    .metric-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .metric-label {
        color: var(--muted);
        font-size: 12px;
    }

    .metric-icon {
        width: 32px;
        height: 32px;

        background: #171d28;
        border: 1px solid var(--border);
        border-radius: 8px;

        display: flex;
        justify-content: center;
        align-items: center;
    }

    .metric-value {
        color: var(--text);
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -1px;
        margin-top: 13px;
    }

    .metric-description {
        color: var(--muted);
        font-size: 11px;
        margin-top: 3px;
    }


    /* =====================================================
       INPUTS
    ===================================================== */

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: var(--card-inner) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
        border-radius: 9px !important;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stDateInput"] input:focus {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 1px var(--blue) !important;
    }

    [data-testid="stWidgetLabel"] p {
        color: #aeb6c2 !important;
        font-size: 12px !important;
    }


    /* =====================================================
       BOTÕES
    ===================================================== */

    .stButton > button,
    [data-testid="stFormSubmitButton"] button {
        border-radius: 9px;
        border: 1px solid #2b3544;
        background: #171d28;
        color: var(--text);
        font-weight: 600;
        transition: all .15s ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        border-color: var(--blue);
        color: var(--blue);
        background: var(--card);
    }


    /* =====================================================
       EXPANDER
    ===================================================== */

    [data-testid="stExpander"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
    }

    [data-testid="stExpander"] details {
        border: none !important;
    }

    [data-testid="stExpander"] summary {
        color: #dfe4ec !important;
    }


    /* =====================================================
       ESTUDOS
    ===================================================== */

    .study-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;

        transition:
            transform .15s ease,
            background .15s ease,
            border-color .15s ease;
    }

    .study-card:hover {
        transform: translateY(-2px);
        background: var(--card-hover);
        border-color: #303949;
    }

    .study-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 20px;
    }

    .study-subject {
        color: var(--blue);
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .study-topic {
        color: var(--text);
        font-size: 17px;
        font-weight: 650;
        margin-top: 4px;
    }

    .progress-meta,
    .progress-info {
        display: flex;
        justify-content: space-between;
        color: var(--muted);
        font-size: 11px;
        margin-top: 18px;
    }

    .progress-track {
        background: #1a202b;
        height: 7px;
        border-radius: 999px;
        overflow: hidden;
        margin-top: 7px;
    }

    .progress-fill {
        height: 100%;
        background: var(--blue);
        border-radius: 999px;
    }


    /* =====================================================
       STATUS BADGES
    ===================================================== */

    .status-badge {
        padding: 5px 9px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 700;
        white-space: nowrap;
    }

    .status-not-started {
        background: rgba(125, 133, 144, .12);
        color: #9da5b0;
        border: 1px solid rgba(125, 133, 144, .2);
    }

    .status-progress {
        background: rgba(91, 140, 255, .12);
        color: #7da4ff;
        border: 1px solid rgba(91, 140, 255, .25);
    }

    .status-pending {
        background: rgba(246, 196, 83, .10);
        color: var(--yellow);
        border: 1px solid rgba(246, 196, 83, .22);
    }

    .status-done {
        background: rgba(56, 217, 150, .10);
        color: #58e3aa;
        border: 1px solid rgba(56, 217, 150, .22);
    }

    .status-late {
        background: rgba(255, 100, 124, .10);
        color: #ff7a8f;
        border: 1px solid rgba(255, 100, 124, .22);
    }


    /* =====================================================
       TAREFAS
    ===================================================== */

    .task-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 17px 18px;
        margin-bottom: 10px;

        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;

        transition:
            transform .15s ease,
            background .15s ease,
            border-color .15s ease;
    }

    .task-card:hover {
        transform: translateY(-1px);
        background: var(--card-hover);
        border-color: #303949;
    }

    .task-main {
        display: flex;
        align-items: center;
        gap: 13px;
        min-width: 0;
    }

    .task-check {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 1.5px solid #596273;
        flex-shrink: 0;
    }

    .task-name {
        color: #e5e9ef;
        font-size: 14px;
        font-weight: 600;
    }

    .task-meta {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 5px;
    }

    .task-date {
        color: var(--muted);
        font-size: 11px;
    }

    .task-id {
        color: #596273;
        font-size: 10px;
    }


    /* =====================================================
       EMPTY STATE
    ===================================================== */

    .empty-state {
        background: var(--card);
        border: 1px dashed #252d3a;
        border-radius: 14px;
        min-height: 165px;

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        text-align: center;
        margin-top: 14px;
        padding: 20px;
    }

    .empty-icon {
        width: 42px;
        height: 42px;

        background: #151b26;
        border: 1px solid var(--border);
        border-radius: 10px;

        display: flex;
        align-items: center;
        justify-content: center;

        color: var(--muted);
        margin-bottom: 12px;
    }

    .empty-title {
        color: #d5dae2;
        font-size: 14px;
        font-weight: 600;
    }

    .empty-description {
        color: var(--muted);
        font-size: 12px;
        margin-top: 4px;
    }


    /* =====================================================
       DATAFRAME
    ===================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }


    /* =====================================================
       ALERTAS
    ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* =====================================================
       PLOTLY
    ===================================================== */

    [data-testid="stPlotlyChart"] {
        border-radius: 14px;
    }


    /* =====================================================
       ZONA DE EXCLUSÃO
    ===================================================== */

    .delete-zone {
        background: rgba(255, 100, 124, .035);
        border: 1px solid rgba(255, 100, 124, .15);
        border-radius: 14px;
        padding: 18px;
    }

    .delete-title {
        color: #ff8295;
        font-size: 14px;
        font-weight: 650;
    }

    .delete-description {
        color: var(--muted);
        font-size: 11px;
        margin-top: 4px;
    }


    /* =====================================================
       FOOTER
    ===================================================== */

    footer {
        visibility: hidden;
    }


    /* =====================================================
       RESPONSIVO
    ===================================================== */

    @media (max-width: 900px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .page-header,
        .dashboard-header {
            display: block;
        }

        .dashboard-date {
            margin-top: 10px;
        }

    }

    </style>
    """)


def page_header(title, subtitle):
    html(f"""
    <div class="page-header">
        <div>
            <div class="page-title">
                {title}
            </div>

            <div class="page-subtitle">
                {subtitle}
            </div>
        </div>
    </div>
    """)


def section_header(label, title, subtitle=None):
    subtitle_html = ""

    if subtitle:
        subtitle_html = f"""
        <div class="section-subtitle">
            {subtitle}
        </div>
        """

    html(f"""
    <div class="section-label">
        {label}
    </div>

    <div class="section-title">
        {title}
    </div>

    {subtitle_html}
    """)


def spacer(height=30):
    html(
        f'<div style="height:{height}px;"></div>'
    )


def empty_state(title, description, icon="•"):
    html(f"""
    <div class="empty-state">

        <div class="empty-icon">
            {icon}
        </div>

        <div class="empty-title">
            {title}
        </div>

        <div class="empty-description">
            {description}
        </div>

    </div>
    """)


def metric_card(
    label,
    value,
    description,
    icon="•",
    icon_color="#7d8590",
    description_color=None
):
    description_style = ""

    if description_color:
        description_style = (
            f'style="color:{description_color};"'
        )

    html(f"""
    <div class="metric-card">

        <div class="metric-top">

            <div class="metric-label">
                {label}
            </div>

            <div class="metric-icon">
                <span style="color:{icon_color};">
                    {icon}
                </span>
            </div>

        </div>

        <div class="metric-value">
            {value}
        </div>

        <div
            class="metric-description"
            {description_style}
        >
            {description}
        </div>

    </div>
    """)