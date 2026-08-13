import sqlite3
import os

from pathlib import Path


# =========================================================
# CAMINHO DO BANCO
# =========================================================

# Localmente:
# dashboard/personal_dashboard.db
#
# No Render:
# /var/data/personal_dashboard.db

DATA_DIR = os.getenv(
    "DATA_DIR"
)

if DATA_DIR:

    BASE_DIR = Path(DATA_DIR)

else:

    BASE_DIR = Path(__file__).resolve().parent


BASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


DB_PATH = (
    BASE_DIR
    / "personal_dashboard.db"
)


# =========================================================
# CONFIGURAÇÃO
# =========================================================

# Garante que o banco fique sempre ao lado deste arquivo,
# independentemente da pasta onde o Streamlit for iniciado.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "personal_dashboard.db"


# Valores permitidos pelo sistema
FINANCE_TYPES = (
    "Receita",
    "Despesa"
)

STUDY_STATUS = (
    "Não Iniciado",
    "Em Andamento",
    "Concluído"
)

TASK_STATUS = (
    "Pendente",
    "Concluído"
)


# =========================================================
# CONEXÃO
# =========================================================
def get_connection():
    """
    Cria e configura uma conexão SQLite.
    """

    conn = sqlite3.connect(
        DB_PATH,
        timeout=10
    )

    # Aguarda um pouco em caso de outra operação
    # estar escrevendo no banco.
    conn.execute(
        "PRAGMA busy_timeout = 10000"
    )

    return conn


# =========================================================
# INICIALIZAÇÃO
# =========================================================
def init_db():

    with get_connection() as conn:

        cursor = conn.cursor()

        # =================================================
        # FINANÇAS
        # =================================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS finances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                amount REAL,
                type TEXT,
                category TEXT,
                date TEXT
            )
        """)

        # =================================================
        # ESTUDOS
        # =================================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS studies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                topic TEXT,
                status TEXT,
                progress INTEGER
            )
        """)

        # =================================================
        # TAREFAS
        # =================================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                due_date TEXT,
                status TEXT
            )
        """)

        # =================================================
        # ÍNDICES
        # =================================================

        # Financeiro
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_finances_type
            ON finances(type)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_finances_category
            ON finances(category)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_finances_date
            ON finances(date)
        """)

        # Estudos
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_studies_status
            ON studies(status)
        """)

        # Tarefas
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_tasks_status
            ON tasks(status)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_tasks_due_date
            ON tasks(due_date)
        """)

        # WAL costuma funcionar melhor em aplicações
        # com leituras frequentes como Streamlit.
        try:
            cursor.execute(
                "PRAGMA journal_mode=WAL"
            )
        except sqlite3.DatabaseError:
            pass


# =========================================================
# UTILIDADES
# =========================================================
def _clean_text(value, field_name):
    """
    Remove espaços extras e impede textos vazios.
    """

    if value is None:
        raise ValueError(
            f"{field_name} não pode ser vazio."
        )

    value = str(value).strip()

    if not value:
        raise ValueError(
            f"{field_name} não pode ser vazio."
        )

    return value


# =========================================================
# FINANÇAS
# =========================================================
def add_finance(
    desc,
    amount,
    ftype,
    category
):

    desc = _clean_text(
        desc,
        "Descrição"
    )

    category = _clean_text(
        category,
        "Categoria"
    )

    if ftype not in FINANCE_TYPES:
        raise ValueError(
            "Tipo financeiro inválido."
        )

    try:
        amount = float(amount)

    except (TypeError, ValueError):
        raise ValueError(
            "Valor financeiro inválido."
        )

    if amount <= 0:
        raise ValueError(
            "O valor deve ser maior que zero."
        )


    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO finances (
                description,
                amount,
                type,
                category,
                date
            )
            VALUES (
                ?,
                ?,
                ?,
                ?,
                date('now')
            )
        """, (
            desc,
            amount,
            ftype,
            category
        ))

        return cursor.lastrowid


def get_finances():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                description,
                amount,
                type,
                category,
                date
            FROM finances
            ORDER BY
                date DESC,
                id DESC
        """)

        return cursor.fetchall()


def get_finance(fin_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                description,
                amount,
                type,
                category,
                date
            FROM finances
            WHERE id = ?
        """, (
            int(fin_id),
        ))

        return cursor.fetchone()


def delete_finance(fin_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM finances
            WHERE id = ?
            """,
            (
                int(fin_id),
            )
        )

        return cursor.rowcount > 0


# =========================================================
# ESTUDOS
# =========================================================
def add_study(
    subject,
    topic,
    status,
    progress
):

    subject = _clean_text(
        subject,
        "Matéria"
    )

    topic = _clean_text(
        topic,
        "Tópico"
    )

    if status not in STUDY_STATUS:
        raise ValueError(
            "Status de estudo inválido."
        )

    try:
        progress = int(progress)

    except (TypeError, ValueError):
        raise ValueError(
            "Progresso inválido."
        )

    progress = max(
        0,
        min(100, progress)
    )

    # Mantém status e progresso coerentes.
    if status == "Concluído":
        progress = 100

    elif progress == 100:
        status = "Concluído"

    elif (
        progress > 0
        and status == "Não Iniciado"
    ):
        status = "Em Andamento"


    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO studies (
                subject,
                topic,
                status,
                progress
            )
            VALUES (?, ?, ?, ?)
        """, (
            subject,
            topic,
            status,
            progress
        ))

        return cursor.lastrowid


def get_studies():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                subject,
                topic,
                status,
                progress
            FROM studies
            ORDER BY id ASC
        """)

        return cursor.fetchall()


def get_study(study_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                subject,
                topic,
                status,
                progress
            FROM studies
            WHERE id = ?
        """, (
            int(study_id),
        ))

        return cursor.fetchone()


def update_study(
    study_id,
    status,
    progress
):

    if status not in STUDY_STATUS:
        raise ValueError(
            "Status de estudo inválido."
        )

    try:
        progress = int(progress)

    except (TypeError, ValueError):
        raise ValueError(
            "Progresso inválido."
        )

    progress = max(
        0,
        min(100, progress)
    )

    # Sincroniza status e progresso.
    if status == "Concluído":
        progress = 100

    elif progress == 100:
        status = "Concluído"

    elif (
        progress > 0
        and status == "Não Iniciado"
    ):
        status = "Em Andamento"


    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE studies
            SET
                status = ?,
                progress = ?
            WHERE id = ?
        """, (
            status,
            progress,
            int(study_id)
        ))

        return cursor.rowcount > 0


def delete_study(study_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM studies
            WHERE id = ?
        """, (
            int(study_id),
        ))

        return cursor.rowcount > 0


# =========================================================
# TAREFAS
# =========================================================
def add_task(
    task,
    due_date
):

    task = _clean_text(
        task,
        "Tarefa"
    )

    due_date = _clean_text(
        due_date,
        "Data"
    )


    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tasks (
                task,
                due_date,
                status
            )
            VALUES (?, ?, ?)
        """, (
            task,
            due_date,
            "Pendente"
        ))

        return cursor.lastrowid


def get_tasks():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                task,
                due_date,
                status
            FROM tasks
            ORDER BY
                CASE
                    WHEN status = 'Pendente'
                    THEN 0
                    ELSE 1
                END,
                due_date ASC,
                id DESC
        """)

        return cursor.fetchall()


def get_task(task_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                task,
                due_date,
                status
            FROM tasks
            WHERE id = ?
        """, (
            int(task_id),
        ))

        return cursor.fetchone()


def update_task_status(
    task_id,
    status
):

    if status not in TASK_STATUS:

        raise ValueError(
            "Status de tarefa inválido."
        )


    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ?
        """, (
            status,
            int(task_id)
        ))

        return cursor.rowcount > 0


def update_task(
    task_id,
    task,
    due_date
):

    task = _clean_text(
        task,
        "Tarefa"
    )

    due_date = _clean_text(
        due_date,
        "Data"
    )


    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET
                task = ?,
                due_date = ?
            WHERE id = ?
        """, (
            task,
            due_date,
            int(task_id)
        ))

        return cursor.rowcount > 0


def delete_task(task_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM tasks
            WHERE id = ?
        """, (
            int(task_id),
        ))

        return cursor.rowcount > 0