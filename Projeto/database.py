import pygsheets
import pandas as pd
import streamlit as st

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/136DaNqFF7CKgLz1YM1nI-eB1v1Uf3rEdyvN6IJ36yTo/"
NOME_ABA = "crime_rate_safety_analysis"


def conectar():
    gc = pygsheets.authorize(
        service_file="chave_de_acesso.json"
    )

    planilha = gc.open_by_url(URL_PLANILHA)

    return planilha.worksheet_by_title(NOME_ABA)


@st.cache_data
def carregar_dados():

    aba = conectar()

    dados = aba.get_all_records()

    df = pd.DataFrame(dados)

    colunas_numericas = [
        "year",
        "month",
        "population_density_per_sqkm",
        "crime_severity_score",
        "victim_count",
        "injuries_reported",
        "fatalities",
        "financial_loss_usd",
        "response_time_minutes",
        "officers_assigned",
        "investigation_duration_days",
        "prior_incidents_same_location",
        "safety_index",
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df


def salvar_registro(novo_registro):

    aba = conectar()

    aba.append_table(
        novo_registro.iloc[0].tolist()
    )

    carregar_dados.clear()