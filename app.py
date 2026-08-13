import streamlit as st
import database
import pandas as pd
import plotly.express as px

from datetime import datetime


# =========================================================
# CONFIGURAÇÃO
# =========================================================
st.set_page_config(
    page_title="Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# FUNÇÃO HTML
# =========================================================
def html(content):
    st.html(content)


# =========================================================
# CSS GLOBAL
# =========================================================
html("""
<style>

:root {
    --bg: #080b10;
    --sidebar: #0d1117;
    --card: #11161f;
    --card-hover: #151b26;
    --border: #202733;

    --text: #f4f7fb;
    --muted: #7d8590;

    --blue: #5b8cff;
    --green: #38d996;
    --red: #ff647c;
}


/* APP */

html,
body,
[data-testid="stAppViewContainer"] {
    background: #080b10;
    color: #f4f7fb;
}

[data-testid="stMain"] {
    background: #080b10;
}

[data-testid="stHeader"] {
    background: transparent;
}


/* CONTAINER */

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    padding-bottom: 4rem;
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid #202733;
}

[data-testid="stSidebarNav"] a {
    border-radius: 8px;
    margin: 3px 8px;
}

[data-testid="stSidebarNav"] a:hover {
    background: #171d28;
}

[data-testid="stSidebarNav"] span {
    color: #c4cad3;
}


/* TIPOGRAFIA */

body,
p,
span,
div,
button,
input {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}


/* HEADER */

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 28px;
}

.dashboard-title {
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -1px;
    color: #f4f7fb;
}

.dashboard-subtitle {
    margin-top: 5px;
    color: #7d8590;
    font-size: 14px;
}

.dashboard-date {
    color: #7d8590;
    font-size: 13px;
}


/* MÉTRICAS */

.metric-card {
    background: #11161f;
    border: 1px solid #202733;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;

    transition:
        0.15s background,
        0.15s border-color,
        0.15s transform;
}

.metric-card:hover {
    background: #151b26;
    border-color: #303949;
    transform: translateY(-2px);
}

.metric-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.metric-label {
    color: #7d8590;
    font-size: 13px;
}

.metric-icon {
    width: 32px;
    height: 32px;

    background: #171d28;
    border: 1px solid #202733;
    border-radius: 8px;

    display: flex;
    align-items: center;
    justify-content: center;
}

.metric-value {
    margin-top: 14px;

    color: #f4f7fb;

    font-size: 28px;
    font-weight: 700;

    letter-spacing: -1px;
}

.metric-description {
    margin-top: 3px;

    color: #7d8590;

    font-size: 12px;
}


/* SECTION */

.section-label {
    color: #6f7783;

    font-size: 11px;
    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 1.4px;

    margin-bottom: 9px;
}

.section-title {
    font-size: 16px;
    font-weight: 650;

    color: #f4f7fb;
}

.section-subtitle {
    color: #7d8590;

    font-size: 12px;

    margin-top: 3px;
}


/* PANEL */

.panel {
    background: #11161f;

    border: 1px solid #202733;

    border-radius: 14px;

    padding: 22px;

    min-height: 285px;
}


/* STUDY */

.study-card {
    background: #0d121a;

    border: 1px solid #202733;

    border-radius: 11px;

    padding: 18px;

    margin-top: 18px;
}

.study-subject {
    color: #5b8cff;

    font-size: 11px;
    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 1px;
}

.study-topic {
    color: #f4f7fb;

    font-size: 18px;
    font-weight: 650;

    margin-top: 5px;
}

.progress-info {
    display: flex;

    justify-content: space-between;

    color: #7d8590;

    font-size: 12px;

    margin-top: 22px;
}

.progress-track {
    height: 7px;

    margin-top: 7px;

    background: #1a202b;

    border-radius: 999px;

    overflow: hidden;
}

.progress-fill {
    height: 100%;

    background: #5b8cff;

    border-radius: 999px;
}


/* EMPTY STATE */

.empty-state {
    background: #0d121a;

    border: 1px dashed #252d3a;

    border-radius: 11px;

    min-height: 170px;

    margin-top: 18px;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    text-align: center;
}

.empty-icon {
    width: 40px;
    height: 40px;

    border: 1px solid #202733;

    border-radius: 10px;

    background: #151b26;

    display: flex;

    align-items: center;

    justify-content: center;

    color: #7d8590;

    margin-bottom: 12px;
}

.empty-title {
    font-size: 14px;

    font-weight: 600;

    color: #d1d5dc;
}

.empty-description {
    color: #7d8590;

    font-size: 12px;

    margin-top: 4px;
}


/* TAREFAS */

.tasks-card {
    background: #11161f;

    border: 1px solid #202733;

    border-radius: 14px;

    margin-top: 14px;

    padding: 4px 20px;
}

.task-row {
    min-height: 58px;

    display: flex;

    align-items: center;

    justify-content: space-between;

    border-bottom: 1px solid #202733;
}

.task-row:last-child {
    border-bottom: none;
}

.task-left {
    display: flex;

    align-items: center;

    gap: 11px;
}

.task-circle {
    width: 15px;
    height: 15px;

    border: 1.5px solid #596273;

    border-radius: 50%;
}

.task-name {
    color: #dfe4ec;

    font-size: 13px;
}

.task-date {
    color: #7d8590;

    font-size: 12px;
}


/* PLOTLY */

[data-testid="stPlotlyChart"] {
    background: #11161f;

    border: 1px solid #202733;

    border-radius: 14px;

    padding: 8px 12px;
}


/* STREAMLIT */

footer {
    visibility: hidden;
}


/* MOBILE */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .dashboard-header {
        display: block;
    }

    .dashboard-date {
        margin-top: 10px;
    }
}

</style>
""")


# =========================================================
# BANCO
# =========================================================
database.init_db()

fin_data = database.get_finances()
tasks_data = database.get_tasks()
studies_data = database.get_studies()


# =========================================================
# FINANCEIRO
# =========================================================
total_rec = 0.0
total_desp = 0.0
df_fin = pd.DataFrame()

if fin_data:

    df_fin = pd.DataFrame(
        fin_data,
        columns=[
            "ID",
            "Descrição",
            "Valor",
            "Tipo",
            "Categoria",
            "Data"
        ]
    )

    total_rec = df_fin[
        df_fin["Tipo"] == "Receita"
    ]["Valor"].sum()

    total_desp = df_fin[
        df_fin["Tipo"] == "Despesa"
    ]["Valor"].sum()


saldo = total_rec - total_desp


# =========================================================
# TAREFAS
# =========================================================
pending_tasks_count = 0
pending_tasks_list = []

if tasks_data:

    df_tasks = pd.DataFrame(
        tasks_data,
        columns=[
            "ID",
            "Tarefa",
            "Data",
            "Status"
        ]
    )

    pending_df = df_tasks[
        df_tasks["Status"] == "Pendente"
    ]

    pending_tasks_count = len(pending_df)

    pending_tasks_list = (
        pending_df
        .head(5)
        .values
        .tolist()
    )


# =========================================================
# ESTUDOS
# =========================================================
last_subject = ""
last_topic = ""
last_progress = 0

if studies_data:

    df_stud = pd.DataFrame(
        studies_data,
        columns=[
            "ID",
            "Matéria",
            "Tópico",
            "Status",
            "Progresso"
        ]
    )

    last_row = df_stud.iloc[-1]

    last_subject = str(last_row["Matéria"])

    last_topic = str(last_row["Tópico"])

    last_progress = int(last_row["Progresso"])


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    html("""
    <div style="
        padding: 5px 14px 20px 14px;
        border-bottom: 1px solid #202733;
        margin-bottom: 10px;
    ">

        <div style="
            display:flex;
            align-items:center;
            gap:10px;
        ">

            <div style="
                width:34px;
                height:34px;
                border-radius:9px;
                background:#171d28;
                border:1px solid #202733;
                display:flex;
                justify-content:center;
                align-items:center;
                font-size:14px;
                font-weight:700;
                color:#5b8cff;
            ">
                C
            </div>

            <div>

                <div style="
                    color:#f4f7fb;
                    font-size:15px;
                    font-weight:700;
                ">
                    COMMAND
                </div>

                <div style="
                    color:#6f7783;
                    font-size:10px;
                    margin-top:2px;
                ">
                    PERSONAL WORKSPACE
                </div>

            </div>

        </div>

    </div>
    """)


# =========================================================
# DATA
# =========================================================
agora = datetime.now()

dias = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

data_formatada = (
    f"{dias[agora.weekday()]}, "
    f"{agora.day} de {meses[agora.month]}"
)


# =========================================================
# HEADER
# =========================================================
html(f"""
<div class="dashboard-header">

    <div>

        <div class="dashboard-title">
            Command Center
        </div>

        <div class="dashboard-subtitle">
            Visão geral da sua rotina pessoal
        </div>

    </div>

    <div class="dashboard-date">
        {data_formatada}
    </div>

</div>
""")


# =========================================================
# MÉTRICAS
# =========================================================
m1, m2, m3, m4 = st.columns(
    4,
    gap="medium"
)


with m1:

    html(f"""
    <div class="metric-card">

        <div class="metric-top">

            <div class="metric-label">
                Receitas
            </div>

            <div class="metric-icon">
                <span style="color:#38d996;">
                    ↗
                </span>
            </div>

        </div>

        <div class="metric-value">
            R$ {total_rec:,.2f}
        </div>

        <div class="metric-description">
            Total registrado
        </div>

    </div>
    """)


with m2:

    html(f"""
    <div class="metric-card">

        <div class="metric-top">

            <div class="metric-label">
                Despesas
            </div>

            <div class="metric-icon">
                <span style="color:#ff647c;">
                    ↘
                </span>
            </div>

        </div>

        <div class="metric-value">
            R$ {total_desp:,.2f}
        </div>

        <div class="metric-description">
            Total registrado
        </div>

    </div>
    """)


with m3:

    saldo_cor = (
        "#38d996"
        if saldo >= 0
        else "#ff647c"
    )

    saldo_status = (
        "Saldo positivo"
        if saldo >= 0
        else "Saldo negativo"
    )

    html(f"""
    <div class="metric-card">

        <div class="metric-top">

            <div class="metric-label">
                Saldo líquido
            </div>

            <div class="metric-icon">

                <span style="
                    color:{saldo_cor};
                    font-size:10px;
                ">
                    ●
                </span>

            </div>

        </div>

        <div class="metric-value">
            R$ {saldo:,.2f}
        </div>

        <div
            class="metric-description"
            style="color:{saldo_cor};"
        >
            {saldo_status}
        </div>

    </div>
    """)


with m4:

    html(f"""
    <div class="metric-card">

        <div class="metric-top">

            <div class="metric-label">
                Tarefas
            </div>

            <div class="metric-icon">
                ✓
            </div>

        </div>

        <div class="metric-value">
            {pending_tasks_count}
        </div>

        <div class="metric-description">
            Pendentes no momento
        </div>

    </div>
    """)


html("""
<div style="height:36px;"></div>
""")


# =========================================================
# GRID PRINCIPAL
# =========================================================
left, right = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# ESTUDOS
# =========================================================
with left:

    html("""
    <div class="section-label">
        Estudos
    </div>
    """)

    if studies_data:

        html(f"""
        <div class="panel">

            <div class="section-title">
                Continuar estudando
            </div>

            <div class="section-subtitle">
                Último conteúdo registrado
            </div>

            <div class="study-card">

                <div class="study-subject">
                    {last_subject}
                </div>

                <div class="study-topic">
                    {last_topic}
                </div>

                <div class="progress-info">

                    <span>
                        Progresso
                    </span>

                    <span>
                        {last_progress}%
                    </span>

                </div>

                <div class="progress-track">

                    <div
                        class="progress-fill"
                        style="width:{last_progress}%;">
                    </div>

                </div>

            </div>

        </div>
        """)

    else:

        html("""
        <div class="panel">

            <div class="section-title">
                Continuar estudando
            </div>

            <div class="section-subtitle">
                Último conteúdo registrado
            </div>

            <div class="empty-state">

                <div class="empty-icon">
                    ◫
                </div>

                <div class="empty-title">
                    Nenhum estudo registrado
                </div>

                <div class="empty-description">
                    Seus estudos recentes aparecerão aqui.
                </div>

            </div>

        </div>
        """)


# =========================================================
# FINANCEIRO
# =========================================================
with right:

    html("""
    <div class="section-label">
        Financeiro
    </div>
    """)

    if not df_fin.empty:

        despesas = df_fin[
            df_fin["Tipo"] == "Despesa"
        ]

    else:

        despesas = pd.DataFrame()


    if not despesas.empty:

        html("""
        <div
            class="panel"
            style="
                min-height:70px;
                padding-bottom:5px;
            "
        >

            <div class="section-title">
                Distribuição de despesas
            </div>

            <div class="section-subtitle">
                Gastos agrupados por categoria
            </div>

        </div>
        """)

        resumo_categoria = (
            despesas
            .groupby(
                "Categoria",
                as_index=False
            )["Valor"]
            .sum()
        )

        fig = px.pie(
            resumo_categoria,
            values="Valor",
            names="Categoria",
            hole=0.72
        )

        fig.update_traces(
            textposition="outside",

            textinfo="percent+label",

            marker=dict(
                line=dict(
                    color="#11161f",
                    width=3
                )
            ),

            hovertemplate=(
                "<b>%{label}</b><br>"
                "R$ %{value:,.2f}<br>"
                "%{percent}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            paper_bgcolor="#11161f",

            plot_bgcolor="#11161f",

            font=dict(
                color="#aab2bf",
                size=11
            ),

            height=280,

            margin=dict(
                l=20,
                r=20,
                t=10,
                b=10
            ),

            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        html("""
        <div class="panel">

            <div class="section-title">
                Distribuição de despesas
            </div>

            <div class="section-subtitle">
                Gastos agrupados por categoria
            </div>

            <div class="empty-state">

                <div class="empty-icon">
                    ◌
                </div>

                <div class="empty-title">
                    Sem dados financeiros
                </div>

                <div class="empty-description">
                    Adicione despesas para gerar o gráfico.
                </div>

            </div>

        </div>
        """)


# =========================================================
# ESPAÇO
# =========================================================
html("""
<div style="height:36px;"></div>
""")


# =========================================================
# TAREFAS
# =========================================================
html("""
<div class="section-label">
    Tarefas
</div>

<div class="section-title">
    Próximas tarefas
</div>

<div class="section-subtitle">
    Pendências que precisam da sua atenção
</div>
""")


if pending_tasks_list:

    tarefas_html = ""

    for tarefa in pending_tasks_list:

        nome = str(tarefa[1])
        data = str(tarefa[2])

        tarefas_html += f"""
        <div class="task-row">

            <div class="task-left">

                <div class="task-circle"></div>

                <div class="task-name">
                    {nome}
                </div>

            </div>

            <div class="task-date">
                {data}
            </div>

        </div>
        """

    html(f"""
    <div class="tasks-card">
        {tarefas_html}
    </div>
    """)

else:

    html("""
    <div
        class="empty-state"
        style="
            min-height:120px;
            margin-top:14px;
        "
    >

        <div class="empty-icon">
            ✓
        </div>

        <div class="empty-title">
            Tudo limpo por aqui
        </div>

        <div class="empty-description">
            Nenhuma tarefa pendente no momento.
        </div>

    </div>
    """)