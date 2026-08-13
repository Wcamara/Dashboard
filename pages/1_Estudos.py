import streamlit as st
import database

from html import escape

from styles import (
    apply_global_style,
    html,
    page_header,
    section_header,
    spacer,
    empty_state
)


# =========================================================
# CONFIGURAÇÃO
# =========================================================
st.set_page_config(
    page_title="Estudos",
    page_icon="📚",
    layout="wide"
)

apply_global_style()


# =========================================================
# BANCO
# =========================================================
database.init_db()


# =========================================================
# HEADER
# =========================================================
page_header(
    "Estudos",
    "Organize sua trilha de estudos e acompanhe seu progresso."
)


# =========================================================
# NOVO ESTUDO
# =========================================================
section_header(
    "Novo estudo",
    "Adicionar tópico",
    "Cadastre uma matéria, tópico e o progresso atual."
)

spacer(14)


with st.expander(
    "Adicionar novo estudo",
    expanded=False
):

    with st.form(
        "study_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(
            2,
            gap="large"
        )

        with col1:

            subject = st.text_input(
                "Matéria / Área",
                placeholder="Ex: Cybersecurity"
            )

            topic = st.text_input(
                "Tópico específico",
                placeholder="Ex: SQL Injection"
            )

        with col2:

            status = st.selectbox(
                "Status",
                [
                    "Não Iniciado",
                    "Em Andamento",
                    "Concluído"
                ]
            )

            progress = st.slider(
                "Progresso (%)",
                min_value=0,
                max_value=100,
                value=0
            )

        submitted = st.form_submit_button(
            "Adicionar estudo",
            use_container_width=True
        )

        if submitted:

            subject_clean = subject.strip()
            topic_clean = topic.strip()

            if not subject_clean or not topic_clean:

                st.warning(
                    "Preencha a matéria e o tópico antes de cadastrar."
                )

            else:

                # Se o usuário definir como concluído,
                # automaticamente consideramos 100%.
                if status == "Concluído":
                    progress = 100

                database.add_study(
                    subject_clean,
                    topic_clean,
                    status,
                    progress
                )

                st.success(
                    "Estudo cadastrado com sucesso."
                )

                st.rerun()


spacer(38)


# =========================================================
# DADOS
# =========================================================
studies_data = database.get_studies()


# =========================================================
# BIBLIOTECA
# =========================================================
section_header(
    "Biblioteca",
    "Seus tópicos",
    "Acompanhe matérias, status e progresso."
)

spacer(15)


# =========================================================
# SEM ESTUDOS
# =========================================================
if not studies_data:

    empty_state(
        "Nenhum estudo cadastrado",
        "Adicione seu primeiro tópico usando o formulário acima.",
        "◫"
    )

    st.stop()


# =========================================================
# RESUMO DOS ESTUDOS
# =========================================================
total_estudos = len(studies_data)

em_andamento = sum(
    1
    for row in studies_data
    if row[3] == "Em Andamento"
)

concluidos = sum(
    1
    for row in studies_data
    if row[3] == "Concluído"
)

nao_iniciados = sum(
    1
    for row in studies_data
    if row[3] == "Não Iniciado"
)


m1, m2, m3, m4 = st.columns(
    4,
    gap="medium"
)


def study_metric(
    label,
    value,
    description,
    icon,
    color
):

    html(f"""
    <div class="metric-card">

        <div class="metric-top">

            <div class="metric-label">
                {escape(label)}
            </div>

            <div class="metric-icon">
                <span style="color:{color};">
                    {icon}
                </span>
            </div>

        </div>

        <div class="metric-value">
            {value}
        </div>

        <div class="metric-description">
            {escape(description)}
        </div>

    </div>
    """)


with m1:
    study_metric(
        "Total",
        total_estudos,
        "Tópicos cadastrados",
        "≡",
        "#7d8590"
    )

with m2:
    study_metric(
        "Em andamento",
        em_andamento,
        "Estudos ativos",
        "●",
        "#5b8cff"
    )

with m3:
    study_metric(
        "Concluídos",
        concluidos,
        "Finalizados",
        "✓",
        "#38d996"
    )

with m4:
    study_metric(
        "Não iniciados",
        nao_iniciados,
        "Aguardando início",
        "○",
        "#9da5b0"
    )


spacer(32)


# =========================================================
# CARDS DE ESTUDO
# =========================================================
for row in studies_data:

    study_id = int(row[0])

    subject = escape(
        str(row[1])
    )

    topic = escape(
        str(row[2])
    )

    status = str(row[3])

    try:
        progress = int(row[4])
    except (ValueError, TypeError):
        progress = 0

    progress = max(
        0,
        min(100, progress)
    )


    # =====================================================
    # STATUS
    # =====================================================
    if status == "Concluído":

        status_class = "status-done"

    elif status == "Em Andamento":

        status_class = "status-progress"

    else:

        status_class = "status-not-started"


    html(f"""
    <div class="study-card">

        <div class="study-top">

            <div>

                <div class="study-subject">
                    {subject}
                </div>

                <div class="study-topic">
                    {topic}
                </div>

            </div>

            <div class="status-badge {status_class}">
                {escape(status)}
            </div>

        </div>

        <div class="progress-meta">

            <span>
                Progresso
            </span>

            <span>
                {progress}%
            </span>

        </div>

        <div class="progress-track">

            <div
                class="progress-fill"
                style="width:{progress}%;"
            ></div>

        </div>

    </div>
    """)


spacer(26)


# =========================================================
# ATUALIZAR PROGRESSO
# =========================================================
with st.expander(
    "Atualizar progresso",
    expanded=False
):

    study_options = {
        f"{row[1]} • {row[2]}": row[0]
        for row in studies_data
    }

    selected_label = st.selectbox(
        "Selecione o tópico",
        options=list(study_options.keys()),
        key="study_update_selection"
    )

    selected_id = study_options[
        selected_label
    ]

    current_item = next(
        row
        for row in studies_data
        if row[0] == selected_id
    )


    status_options = [
        "Não Iniciado",
        "Em Andamento",
        "Concluído"
    ]

    current_status = str(
        current_item[3]
    )

    if current_status in status_options:

        current_index = (
            status_options.index(
                current_status
            )
        )

    else:

        current_index = 0


    try:

        current_progress = int(
            current_item[4]
        )

    except (ValueError, TypeError):

        current_progress = 0


    current_progress = max(
        0,
        min(100, current_progress)
    )


    col_edit1, col_edit2 = st.columns(
        2,
        gap="large"
    )


    with col_edit1:

        new_status = st.selectbox(
            "Novo status",
            status_options,
            index=current_index
        )


    with col_edit2:

        new_progress = st.slider(
            "Novo progresso (%)",
            min_value=0,
            max_value=100,
            value=current_progress
        )


    if st.button(
        "Salvar alterações",
        use_container_width=True,
        key="update_study"
    ):

        if new_status == "Concluído":
            new_progress = 100

        elif (
            new_status == "Não Iniciado"
            and new_progress > 0
        ):
            new_status = "Em Andamento"

        database.update_study(
            selected_id,
            new_status,
            new_progress
        )

        st.success(
            "Progresso atualizado."
        )

        st.rerun()
