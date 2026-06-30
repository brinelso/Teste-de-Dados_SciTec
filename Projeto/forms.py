import streamlit as st
import pandas as pd
from dashboard import carregar_dados
import pygsheets

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/136DaNqFF7CKgLz1YM1nI-eB1v1Uf3rEdyvN6IJ36yTo/"

DIAS_SEMANA = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
ESTACOES = ['Summer', 'Autumn', 'Winter', 'Spring']
PERIODOS_DIA = ['Morning (6am-12pm)', 'Afternoon (12pm-6pm)', 'Evening (6pm-10pm)','Night (10pm-2am)']
TIPOS_AREA = ['Urban', 'Rural', 'Remote']
TIPOS_CRIME = ['Theft', 'Assault', 'Robbery', 'Burglary', 'Fraud', 'Drug Offense', 'Cybercrime', 'Domestic Violence', 'Vandalism', 'Sexual Assault', 'Murder', 'Arson', 'Extortion', 'Kidnapping', 'Trafficking']
GENEROS_VITIMA = ['Male', 'Female', 'Other']
FAIXAS_ETARIAS = ['0-17', '18-25', '26-35', '36-50', '51-65', '65+']
ARMAS = ['Firearm', 'Knife', 'Blunt Object', 'Unknown', 'None']
STATUS_SUSPEITO = ["Arrested", "At Large", "Acquitted", "Under Investigation"]
STATUS_CASO = ["Open - Active", "Closed - Solved", "Closed - Unsolved"]
METODOS_REPORTE = ["Emergency Call", "Police Station", "Anonymous Tip", "Online Report"]
COBERTURA_CCTV = ["No Coverage", "Partial Coverage", "Full Coverage"]
CONDICAO_ILUMINACAO = ["Well Lit", "Partially Lit", "Poorly Lit"]
SIM_NAO = ["Yes", "No"]

def mostrar_formulario():
    st.title('Adicionar Novo Registro')
    st.markdown('Preencha os campos para incluir uma nova ocorrência criminal')
    with st.form('formulario_novo_registro', clear_on_submit = True):
        st.subheader("Dados gerais")
        col1, col2, col3 = st.columns(3)
        with col1:
            year = st.number_input("Ano", min_value=2000, max_value=2100, value=2026, step=1)
            month = st.number_input("Mês", min_value=1, max_value=12, value=1, step=1)
        with col2:
            day_of_week = st.selectbox("Dia da semana", DIAS_SEMANA)
            season = st.selectbox("Estação", ESTACOES)
        with col3:
            time_of_day = st.selectbox("Período do dia", PERIODOS_DIA)
            area_type = st.selectbox("Tipo de área", TIPOS_AREA)
 
        country = st.text_input("País", placeholder="Ex: Brazil")
        population_density_per_sqkm = st.number_input(
            "Densidade populacional (hab/km²)", min_value=0, value=100, step=1
        )
        st.divider()
        st.subheader('Sobre o Crime')
        col4, col5, col6 = st.columns(3)
        with col4:
            crime_type = st.selectbox('Tipo de Crime', TIPOS_CRIME)
            crime_severity_score = st.slider("Severidade do Crime (0-10)", 0.0, 10.0, 5.0, step = 0.1)
        with col5:
            weapon_used = st.selectbox('Arma Utilizada', ARMAS)
            gang_related = st.selectbox('Presença de Alguma Gangue?', SIM_NAO)
        with col6:
            drug_related = st.selectbox('Relacionado à Drogas?', SIM_NAO)
            repeat_offender = st.selectbox('Houve Reincidência', SIM_NAO)

        st.divider()
        st.subheader('Vítima')
        col7, col8, col9 = st.columns(3)
        with col7:
            victim_count = st.number_input('Número de Vítimas', min_value = 0, value = 1, step = 1)
            victim_gender = st.selectbox('Gênero da Vítima', GENEROS_VITIMA)
        with col8:
            victim_age_group = st.selectbox('Faixa Etária da Vítima', FAIXAS_ETARIAS)
            injuries_reported = st.number_input('Quantidade de Feridos', min_value = 0, value = 0, step = 1)
        with col9:
            fatalities = st.number_input('Fatalidades', min_value = 0, value = 0, step = 1)
            financial_loss_usd = st.number_input('Prejuízo em Doláres', min_value = 0.0, value = 0.0, step = 10.0)

        st.divider()
        st.subheader('Investigação')            
        col10, col11, col12 = st.columns(3)
        with col10:
            suspect_status = st.selectbox('Status do Suspeito', STATUS_SUSPEITO)
            case_status = st.selectbox('Status do Caso', STATUS_CASO)
        with col11:
            reporting_method = st.selectbox('Método de Denúncia', METODOS_REPORTE)
            response_time_minutes = st.number_input('Tempo de Resposta (mínimo)', min_value = 0, value = 1, step = 1)
        with col12:
            officers_assigned = st.number_input('Policiais Designados', min_value = 0, value = 1, step = 1)
            investigation_duration_days = st.number_input('Duração da Investigação (em dias)', min_value = 0, value = 1, step = 1)
        
        crime_resolved = st.selectbox('Crime já Resolvido?', SIM_NAO)

        st.divider()
        st.subheader('Local')
        col13, col14, col15 = st.columns(3)
        with col13:
            cctv_coverage = st.selectbox('Cobertura de CFTV', COBERTURA_CCTV)
        with col14:
            lighting_condition = st.selectbox('Condição de iluminação', CONDICAO_ILUMINACAO)
        with col15:
            prior_incidents_same_location = st.number_input('Quantidade de Incidentes Ocorridos no Mesmo Lugal', min_value = 0, value = 1, step = 1)
        safety_index = st.slider('Índice de Segurança (0-100)', 0.0, 100.0, 50.0, step = 0.1)
        enviado = st.form_submit_button('Finalizar Registro')

        if enviado:
            if not country.strip():
                st.error("O campo 'País' é obrigatório.")
                return
            novo_registro = pd.DataFrame([{
                "year": year,
                "month": month,
                "day_of_week": day_of_week,
                "season": season,
                "time_of_day": time_of_day,
                "country": country.strip(),
                "area_type": area_type,
                "population_density_per_sqkm": population_density_per_sqkm,
                "crime_type": crime_type,
                "crime_severity_score": crime_severity_score,
                "victim_count": victim_count,
                "victim_gender": victim_gender,
                "victim_age_group": victim_age_group,
                "injuries_reported": injuries_reported,
                "fatalities": fatalities,
                "financial_loss_usd": financial_loss_usd,
                "weapon_used": weapon_used,
                "suspect_status": suspect_status,
                "case_status": case_status,
                "reporting_method": reporting_method,
                "response_time_minutes": response_time_minutes,
                "officers_assigned": officers_assigned,
                "investigation_duration_days": investigation_duration_days,
                "repeat_offender": repeat_offender,
                "gang_related": gang_related,
                "drug_related": drug_related,
                "cctv_coverage": cctv_coverage,
                "lighting_condition": lighting_condition,
                "prior_incidents_same_location": prior_incidents_same_location,
                "safety_index": safety_index,
                "crime_resolved": crime_resolved,
            }])

            try:

                gc = pygsheets.authorize(
                    service_file="chave_de_acesso.json"
                )

                planilha = gc.open_by_url(URL_PLANILHA)

                aba = planilha.worksheet_by_title(
                    "crime_rate_safety_analysis"
                )

                aba.append_table(
                    novo_registro.values.tolist()[0]
                )

                carregar_dados.clear()

                st.success("Registro adicionado com sucesso!")

            except Exception as erro:
                st.error(f"Não foi possível salvar: {erro}")