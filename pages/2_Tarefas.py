import streamlit as st
import database
import requests

from datetime import datetime, date
from html import escape

from styles import (
    apply_global_style,
    html,
    page_header,
    section_header,
    spacer,
    empty_state,
    metric_card
)


# =========================================================
# CONFIGURAÇÃO
# =========================================================
st.set_page_config(
    page_title="Tarefas",
    page_icon="✓",
    layout="wide"
)

apply_global_style()


# =========================================================
# CSS EXCLUSIVO DA PÁGINA DE TAREFAS
# =========================================================
html("""
<style>

/* Botão usado como checkbox */
div[data-testid="stButton"]:has(
    button[kind="secondary"]
) button.task-toggle {
    min-width: 42px;
}


/* Tarefa concluída */
.task-card-completed {
    opacity: 0.62;
}

.task-card-completed .task-name {
    text-decoration: line-through;
    color: #7d8590;
}


/* Bolinha concluída */
.task-check-done {
    width: 18px;
    height: 18px;

    border-radius: 50%;

    background: rgba(56, 217, 150, 0.15);
    border: 1.5px solid #38d996;

    display: flex;
    align-items: center;
    justify-content: center;

    color: #38d996;

    font-size: 11px;
    font-weight: 800;

    flex-shrink: 0;
}


/* Botão concluir */
.task-complete-button button {
    height: 48px !important;

    font-size: 17px !important;

    border-radius: 12px !important;

    background: #11161f !important;

    border: 1px solid #293241 !important;
}


/* Pendente */
.task-complete-button.pending button:hover {
    border-color: #5b8cff !important;
    color: #5b8cff !important;
}


/* Concluída */
.task-complete-button.done button {
    color: #38d996 !important;

    border-color:
        rgba(56, 217, 150, .35) !important;

    background:
        rgba(56, 217, 150, .06) !important;
}


/* Botão deletar */
.delete-task-button button {
    height: 48px !important;

    color: #7d8590 !important;

    font-size: 18px !important;
}

.delete-task-button button:hover {
    border-color: #ff647c !important;

    color: #ff647c !important;

    background:
        rgba(255, 100, 124, .05) !important;
}

</style>
""")


# =========================================================
# BANCO
# =========================================================
database.init_db()


# =========================================================
# WHATSAPP
# =========================================================
def send_whatsapp(task_text):

    PHONE = "SEU_NUMERO"
    API_KEY = "SUA_API_KEY"

    if (
        PHONE == "SEU_NUMERO"
        or API_KEY == "SUA_API_KEY"
    ):

        return (
            False,
            "WhatsApp ainda não foi configurado."
        )

    url = (
        "https://api.callmebot.com/"
        "whatsapp.php"
    )

    params = {
        "phone": PHONE,
        "text": f"Lembrete: {task_text}",
        "apikey": API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.ok:

            return True, None

        return (
            False,
            f"Erro da API: HTTP {response.status_code}"
        )

    except requests.RequestException as error:

        return (
            False,
            f"Falha de conexão: {error}"
        )


# =========================================================
# DATA
# =========================================================
def parse_task_date(value):

    if value is None:
        return None

    raw = str(value)

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y"
    ]

    for date_format in formats:

        try:

            return datetime.strptime(
                raw,
                date_format
            ).date()

        except ValueError:
            pass

    return None


# =========================================================
# DADOS
# =========================================================
tasks = database.get_tasks()

today = date.today()


# =========================================================
# MÉTRICAS
# =========================================================
total_tasks = (
    len(tasks)
    if tasks
    else 0
)

pending_tasks = 0
completed_tasks = 0
late_tasks = 0


if tasks:

    for task in tasks:

        task_status = str(
            task[3]
        )

        task_date = parse_task_date(
            task[2]
        )


        if task_status == "Concluído":

            completed_tasks += 1

        else:

            pending_tasks += 1

            if (
                task_date is not None
                and task_date < today
            ):

                late_tasks += 1


# =========================================================
# HEADER
# =========================================================
page_header(
    "Tarefas",
    "Organize suas pendências e acompanhe o que precisa da sua atenção."
)


# =========================================================
# MÉTRICAS VISUAIS
# =========================================================
m1, m2, m3, m4 = st.columns(
    4,
    gap="medium"
)


with m1:

    metric_card(
        "Total",
        total_tasks,
        "Tarefas cadastradas",
        "≡",
        "#7d8590"
    )


with m2:

    metric_card(
        "Pendentes",
        pending_tasks,
        "Precisam de atenção",
        "●",
        "#f6c453"
    )


with m3:

    metric_card(
        "Concluídas",
        completed_tasks,
        "Finalizadas",
        "✓",
        "#38d996"
    )


with m4:

    metric_card(
        "Atrasadas",
        late_tasks,
        "Fora do prazo",
        "!",
        "#ff647c"
    )


spacer(38)


# =========================================================
# NOVA TAREFA
# =========================================================
section_header(
    "Nova tarefa",
    "Adicionar pendência",
    "Defina o que precisa ser feito e quando."
)

spacer(14)


with st.expander(
    "Adicionar nova tarefa",
    expanded=False
):

    with st.form(
        "task_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(
            [2, 1],
            gap="large"
        )


        with col1:

            task_desc = st.text_input(
                "Tarefa",
                placeholder=(
                    "Ex: Finalizar módulo "
                    "de SQL Injection"
                )
            )


        with col2:

            due_date = st.date_input(
                "Data de vencimento"
            )


        submitted = (
            st.form_submit_button(
                "Salvar tarefa",
                use_container_width=True
            )
        )


        if submitted:

            task_clean = (
                task_desc.strip()
            )

            if not task_clean:

                st.warning(
                    "Digite uma descrição para a tarefa."
                )

            else:

                database.add_task(
                    task_clean,
                    str(due_date)
                )

                st.success(
                    "Tarefa adicionada."
                )

                st.rerun()


spacer(38)


# =========================================================
# FILTROS
# =========================================================
section_header(
    "Pendências",
    "Suas tarefas",
    "Clique no círculo para concluir ou reabrir uma tarefa."
)

spacer(14)


filter_col1, filter_col2 = st.columns(
    [2, 1],
    gap="large"
)


with filter_col1:

    filter_status = st.segmented_control(
        "Exibir",
        options=[
            "Todas",
            "Pendentes",
            "Concluídas"
        ],
        default="Todas",
        label_visibility="collapsed"
    )


with filter_col2:

    order_option = st.selectbox(
        "Ordenar",
        [
            "Prazo mais próximo",
            "Prazo mais distante"
        ],
        label_visibility="collapsed"
    )


spacer(10)


# =========================================================
# SEM TAREFAS
# =========================================================
if not tasks:

    empty_state(
        "Nenhuma tarefa cadastrada",
        "Adicione sua primeira tarefa usando o formulário acima.",
        "✓"
    )

    st.stop()


# =========================================================
# FILTRAGEM
# =========================================================
filtered_tasks = []


for task in tasks:

    task_status = str(
        task[3]
    )

    if (
        filter_status == "Pendentes"
        and task_status == "Concluído"
    ):
        continue

    if (
        filter_status == "Concluídas"
        and task_status != "Concluído"
    ):
        continue

    filtered_tasks.append(
        task
    )


# =========================================================
# ORDENAÇÃO
# =========================================================
def task_sort_key(task):

    task_date = parse_task_date(
        task[2]
    )

    if task_date is None:

        return date.max

    return task_date


reverse_order = (
    order_option
    == "Prazo mais distante"
)


filtered_tasks = sorted(
    filtered_tasks,
    key=task_sort_key,
    reverse=reverse_order
)


# =========================================================
# LISTAGEM
# =========================================================
if not filtered_tasks:

    empty_state(
        "Nenhuma tarefa neste filtro",
        "Altere o filtro acima para visualizar outras tarefas.",
        "✓"
    )


for task in filtered_tasks:

    task_id = int(
        task[0]
    )

    task_name_raw = str(
        task[1]
    )

    task_name = escape(
        task_name_raw
    )

    task_date_obj = (
        parse_task_date(
            task[2]
        )
    )

    task_status = str(
        task[3]
    )


    # =====================================================
    # STATUS
    # =====================================================
    completed = (
        task_status == "Concluído"
    )

    late = (
        not completed
        and task_date_obj is not None
        and task_date_obj < today
    )


    if completed:

        badge_class = "status-done"
        badge_text = "Concluída"

    elif late:

        badge_class = "status-late"
        badge_text = "Atrasada"

    else:

        badge_class = "status-pending"
        badge_text = "Pendente"


    # =====================================================
    # DATA
    # =====================================================
    if task_date_obj:

        task_date_display = (
            task_date_obj.strftime(
                "%d/%m/%Y"
            )
        )

    else:

        task_date_display = escape(
            str(task[2])
        )


    # =====================================================
    # TEXTO DE DATA
    # =====================================================
    if completed:

        date_extra = "Finalizada"

    elif late:

        days_late = (
            today
            - task_date_obj
        ).days

        if days_late == 1:

            date_extra = "1 dia atrasada"

        else:

            date_extra = (
                f"{days_late} dias atrasada"
            )

    elif (
        task_date_obj
        == today
    ):

        date_extra = "Vence hoje"

    elif (
        task_date_obj is not None
        and task_date_obj
        == today.replace()
    ):

        date_extra = ""

    else:

        date_extra = ""


    # =====================================================
    # COLUNAS
    # =====================================================
    col_check, col_task, col_notify, col_delete = st.columns(
        [
            0.55,
            6.45,
            1.25,
            0.65
        ],
        gap="small"
    )


    # =====================================================
    # CHECKBOX / STATUS
    # =====================================================
    with col_check:

        html(
            '<div class="task-complete-button '
            + (
                'done'
                if completed
                else 'pending'
            )
            + '">'
        )

        button_label = (
            "✓"
            if completed
            else "○"
        )

        if st.button(
            button_label,
            key=f"toggle_{task_id}",
            use_container_width=True,
            help=(
                "Reabrir tarefa"
                if completed
                else "Marcar como concluída"
            )
        ):

            new_status = (
                "Pendente"
                if completed
                else "Concluído"
            )

            database.update_task_status(
                task_id,
                new_status
            )

            st.rerun()

        html("</div>")


    # =====================================================
    # CARD PRINCIPAL
    # =====================================================
    with col_task:

        completed_class = (
            "task-card-completed"
            if completed
            else ""
        )

        check_html = (
            """
            <div class="task-check-done">
                ✓
            </div>
            """
            if completed
            else
            """
            <div class="task-check"></div>
            """
        )


        extra_html = ""

        if date_extra:

            extra_html = f"""
            <span class="task-id">
                {escape(date_extra)}
            </span>
            """


        html(f"""
        <div class="
            task-card
            {completed_class}
        ">

            <div class="task-main">

                {check_html}

                <div>

                    <div class="task-name">
                        {task_name}
                    </div>

                    <div class="task-meta">

                        <span class="task-date">
                            {task_date_display}
                        </span>

                        {extra_html}

                        <span class="task-id">
                            ID {task_id}
                        </span>

                    </div>

                </div>

            </div>

            <div class="
                status-badge
                {badge_class}
            ">
                {badge_text}
            </div>

        </div>
        """)


    # =====================================================
    # WHATSAPP
    # =====================================================
    with col_notify:

        # Para concluídas não faz muito sentido
        # mandar lembrete.
        if completed:

            st.button(
                "Avisar",
                key=f"disabled_notif_{task_id}",
                disabled=True,
                use_container_width=True
            )

        else:

            if st.button(
                "Avisar",
                key=f"notif_{task_id}",
                use_container_width=True
            ):

                success, message = (
                    send_whatsapp(
                        task_name_raw
                    )
                )

                if success:

                    st.toast(
                        "Lembrete enviado pelo WhatsApp."
                    )

                else:

                    st.error(
                        message
                        or
                        "Não foi possível enviar."
                    )


    # =====================================================
    # EXCLUSÃO
    # =====================================================
    with col_delete:

        html(
            '<div class="delete-task-button">'
        )

        if st.button(
            "×",
            key=f"delete_{task_id}",
            use_container_width=True,
            help="Excluir tarefa"
        ):

            database.delete_task(
                task_id
            )

            st.rerun()

        html("</div>")
