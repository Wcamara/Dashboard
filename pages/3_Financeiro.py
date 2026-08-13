import streamlit as st
import database
import pandas as pd

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
    page_title="Finanças",
    page_icon="💰",
    layout="wide"
)

apply_global_style()


# =========================================================
# BANCO
# =========================================================
database.init_db()


# =========================================================
# FORMATAÇÃO BRL
# =========================================================
def brl(value):

    try:

        value = float(value)

    except (ValueError, TypeError):

        value = 0.0


    formatted = f"{value:,.2f}"

    formatted = (
        formatted
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {formatted}"


# =========================================================
# CARREGAMENTO
# =========================================================
fin_data = database.get_finances()


# =========================================================
# DATAFRAME
# =========================================================
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

    # Garante que Valor seja numérico.
    df_fin["Valor"] = pd.to_numeric(
        df_fin["Valor"],
        errors="coerce"
    ).fillna(0.0)

else:

    df_fin = pd.DataFrame(
        columns=[
            "ID",
            "Descrição",
            "Valor",
            "Tipo",
            "Categoria",
            "Data"
        ]
    )


# =========================================================
# CÁLCULOS
# =========================================================
df_rec = df_fin[
    df_fin["Tipo"] == "Receita"
].copy()

df_desp = df_fin[
    df_fin["Tipo"] == "Despesa"
].copy()


total_rec = (
    df_rec["Valor"].sum()
    if not df_rec.empty
    else 0.0
)

total_desp = (
    df_desp["Valor"].sum()
    if not df_desp.empty
    else 0.0
)

saldo_liquido = (
    total_rec - total_desp
)


# =========================================================
# HEADER
# =========================================================
page_header(
    "Finanças",
    "Controle receitas, despesas e acompanhe seu saldo pessoal."
)


# =========================================================
# CARDS
# =========================================================
m1, m2, m3 = st.columns(
    3,
    gap="medium"
)


with m1:

    metric_card(
        "Receitas",
        brl(total_rec),
        "Total de entradas registradas",
        "↗",
        "#38d996"
    )


with m2:

    metric_card(
        "Despesas",
        brl(total_desp),
        "Total de saídas registradas",
        "↘",
        "#ff647c"
    )


saldo_cor = (
    "#38d996"
    if saldo_liquido >= 0
    else "#ff647c"
)

saldo_texto = (
    "Saldo positivo"
    if saldo_liquido >= 0
    else "Saldo negativo"
)


with m3:

    metric_card(
        "Saldo líquido",
        brl(saldo_liquido),
        saldo_texto,
        "●",
        saldo_cor,
        saldo_cor
    )


spacer(38)


# =========================================================
# NOVA MOVIMENTAÇÃO
# =========================================================
section_header(
    "Movimentação",
    "Novo lançamento",
    "Registre uma receita ou despesa no seu controle financeiro."
)

spacer(14)


with st.expander(
    "Adicionar nova movimentação",
    expanded=False
):

    with st.form(
        "fin_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(
            2,
            gap="large"
        )


        with col1:

            desc = st.text_input(
                "Descrição",
                placeholder=(
                    "Ex: Salário, mercado, "
                    "internet..."
                )
            )

            amount = st.number_input(
                "Valor (R$)",
                min_value=0.01,
                value=0.01,
                step=0.01,
                format="%.2f"
            )


        with col2:

            ftype = st.selectbox(
                "Tipo",
                [
                    "Receita",
                    "Despesa"
                ]
            )

            category = st.selectbox(
                "Categoria",
                [
                    "Salário",
                    "Freelance",
                    "Investimentos",
                    "Fixas (Aluguel/Luz)",
                    "Variáveis",
                    "Lazer",
                    "Outros"
                ]
            )


        submitted = st.form_submit_button(
            "Salvar movimentação",
            use_container_width=True
        )


        if submitted:

            desc_clean = desc.strip()

            if not desc_clean:

                st.warning(
                    "Digite uma descrição para a movimentação."
                )

            elif amount <= 0:

                st.warning(
                    "Informe um valor maior que zero."
                )

            else:

                database.add_finance(
                    desc_clean,
                    float(amount),
                    ftype,
                    category
                )

                st.success(
                    "Movimentação salva com sucesso."
                )

                st.rerun()


spacer(38)


# =========================================================
# HISTÓRICO
# =========================================================
section_header(
    "Histórico",
    "Movimentações",
    "Consulte suas entradas e saídas separadamente."
)

spacer(16)


col_receitas, col_despesas = st.columns(
    2,
    gap="large"
)


# =========================================================
# RECEITAS
# =========================================================
with col_receitas:

    section_header(
        "Entradas",
        "Receitas",
        "Valores que entraram."
    )

    spacer(10)


    if df_rec.empty:

        empty_state(
            "Nenhuma receita",
            "Suas entradas aparecerão aqui.",
            "↗"
        )

    else:

        tabela_receitas = df_rec[
            [
                "ID",
                "Descrição",
                "Valor",
                "Categoria",
                "Data"
            ]
        ].copy()


        st.dataframe(
            tabela_receitas,
            use_container_width=True,
            hide_index=True,
            column_config={

                "ID":
                    st.column_config.NumberColumn(
                        "ID",
                        format="%d",
                        width="small"
                    ),

                "Descrição":
                    st.column_config.TextColumn(
                        "Descrição",
                        width="medium"
                    ),

                "Valor":
                    st.column_config.NumberColumn(
                        "Valor",
                        format="R$ %.2f",
                        width="small"
                    ),

                "Categoria":
                    st.column_config.TextColumn(
                        "Categoria"
                    ),

                "Data":
                    st.column_config.TextColumn(
                        "Data"
                    )
            }
        )


# =========================================================
# DESPESAS
# =========================================================
with col_despesas:

    section_header(
        "Saídas",
        "Despesas",
        "Valores que saíram."
    )

    spacer(10)


    if df_desp.empty:

        empty_state(
            "Nenhuma despesa",
            "Suas saídas aparecerão aqui.",
            "↘"
        )

    else:

        tabela_despesas = df_desp[
            [
                "ID",
                "Descrição",
                "Valor",
                "Categoria",
                "Data"
            ]
        ].copy()


        st.dataframe(
            tabela_despesas,
            use_container_width=True,
            hide_index=True,
            column_config={

                "ID":
                    st.column_config.NumberColumn(
                        "ID",
                        format="%d",
                        width="small"
                    ),

                "Descrição":
                    st.column_config.TextColumn(
                        "Descrição",
                        width="medium"
                    ),

                "Valor":
                    st.column_config.NumberColumn(
                        "Valor",
                        format="R$ %.2f",
                        width="small"
                    ),

                "Categoria":
                    st.column_config.TextColumn(
                        "Categoria"
                    ),

                "Data":
                    st.column_config.TextColumn(
                        "Data"
                    )
            }
        )


spacer(42)


# =========================================================
# EXCLUSÃO
# =========================================================
section_header(
    "Gerenciamento",
    "Remover lançamento",
    "Exclua uma movimentação financeira existente."
)

spacer(12)


if df_fin.empty:

    html("""
    <div class="delete-zone">

        <div class="delete-title">
            Nenhum lançamento disponível
        </div>

        <div class="delete-description">
            Cadastre uma movimentação antes de tentar excluir um registro.
        </div>

    </div>
    """)

else:

    html("""
    <div class="delete-zone">

        <div class="delete-title">
            Zona de exclusão
        </div>

        <div class="delete-description">
            Esta ação remove permanentemente o lançamento selecionado.
        </div>

    </div>
    """)

    spacer(12)


    # =====================================================
    # OPÇÕES MAIS SEGURAS QUE DIGITAR ID MANUALMENTE
    # =====================================================
    delete_options = {}

    for _, row in df_fin.iterrows():

        item_id = int(row["ID"])

        description = str(
            row["Descrição"]
        )

        item_type = str(
            row["Tipo"]
        )

        value = brl(
            row["Valor"]
        )

        label = (
            f"ID {item_id} • "
            f"{description} • "
            f"{item_type} • "
            f"{value}"
        )

        delete_options[
            label
        ] = item_id


    with st.form(
        "delete_finance_form"
    ):

        selected_delete_label = st.selectbox(
            "Selecione o lançamento",
            options=list(
                delete_options.keys()
            )
        )

        confirm_delete = st.checkbox(
            "Confirmo que desejo excluir este lançamento."
        )

        delete_submitted = (
            st.form_submit_button(
                "Excluir registro",
                use_container_width=True
            )
        )


        if delete_submitted:

            if not confirm_delete:

                st.warning(
                    "Marque a confirmação antes de excluir."
                )

            else:

                selected_delete_id = (
                    delete_options[
                        selected_delete_label
                    ]
                )

                database.delete_finance(
                    selected_delete_id
                )

                st.success(
                    "Registro removido com sucesso."
                )

                st.rerun()
