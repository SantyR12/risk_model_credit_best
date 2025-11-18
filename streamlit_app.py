import streamlit as st
import pandas as pd
import requests

# CONFIGURACIÓN DE CONEXIÓN Y DATOS 
FLASK_API_URL = 'http://127.0.0.1:5000/credit_risk'

# Lista de 31 columnas esperadas por el modelo 
COLUMNAS_ESPERADAS = [
    'Credit_Score', 'income', 'dtir1', 'loan_amount', 'LTV', 'property_value',
    'open_credit', 'credit_type', 'co-applicant_credit_type', 'loan_type',
    'loan_purpose', 'term', 'age', 'Gender', 'approv_in_adv',
    'business_or_commercial', 'occupancy_type', 'total_units', 'Region',
    'Secured_by', 'Security_Type', 'submission_of_application',
    'construction_type', 'loan_limit', 'Neg_ammortization',
    'interest_only', 'lump_sum_payment',
    'Interest_rate_spread', 
    'Credit_Worthiness',     
    'rate_of_interest',      
    'Upfront_charges'        
]

# Diccionario de Mapeo
OPCIONES_ESPANOL = {
    'open_credit': {'Sin Crédito Abierto': 'nopc', 'Con Crédito Abierto': 'opc'},
    'credit_type': {'EXP': 'EXP', 'EQUI': 'EQUI', 'CRIF': 'CRIF', 'CIB': 'CIB'}, 
    'co-applicant_credit_type': {'CIB': 'CIB', 'EXP': 'EXP', 'EQUI': 'EQUI', 'CRIF': 'CRIF'},
    'loan_type': {'Tipo 1': 'type1', 'Tipo 2': 'type2', 'Tipo 3': 'type3'},
    'loan_purpose': {'Propósito A1': 'A1', 'Propósito A2': 'A2', 'Propósito A3': 'A3', 'Propósito A4': 'A4', 
                     'Propósito A13': 'A13', 'Propósito A23': 'A23', 'Propósito A34': 'A34', 'Propósito A41': 'A41'}, 
    'Gender': {'Hombre': 'Male', 'Mujer': 'Female'},
    'approv_in_adv': {'Sí': 'Y', 'No': 'N'},
    'business_or_commercial': {'Comercial': 'com', 'No Comercial': 'not_com'},
    'occupancy_type': {'Residencia Principal (PR)': 'PR', 'Inversión/Alquiler (IR)': 'IR', 'Segunda Vivienda (SP)': 'SP'},
    'Region': {'Norte': 'North', 'Sur': 'South', 'Este': 'East', 'Oeste': 'West', 'Central': 'Central'}, 
    'Secured_by': {'Vivienda/Inmueble': 'home', 'Terreno': 'land'},
    'Security_Type': {'Directa': 'direct', 'Cooperativa': 'co-op'},
    'submission_of_application': {'A la Institución': 'to_inst', 'No a la Institución': 'not_inst'},
    'construction_type': {'Construcción en Sitio (SB)': 'sb', 'Prefabricada/Móvil (MF)': 'mf'},
    'loan_limit': {'Conforme a Límite (CF)': 'cf', 'No Conforme a Límite (NCF)': 'ncf'},
    'Neg_ammortization': {'Sí (Negativa)': 'neg_amm', 'No (Estándar)': 'not_neg'},
    'interest_only': {'Solo Intereses': 'int_only', 'Interés y Principal': 'not_int'},
    'lump_sum_payment': {'Sí (Pago Global)': 'lpsm', 'No (Sin Pago Global)': 'not_lpsm'}
}

# Función para manejar Selectbox con Mapeo 
def get_selectbox_input(key, label):
    """Muestra opciones en español y devuelve el código técnico."""
    options_dict = OPCIONES_ESPANOL[key]
    spanish_options = list(options_dict.keys())
    
    selected_spanish = st.selectbox(
        label, 
        spanish_options
    )
    # Devuelve el valor técnico al diccionario de datos_cliente
    return options_dict[selected_spanish]


# INTERFAZ 

st.title("Clasificación de Riesgo Crediticio ")
st.markdown("---")

# INPUTS DEL USUARIO 
datos_cliente = {}

col1, col_space, col2, col_space2, col3 = st.columns([1, 0.5, 1, 0.5, 1])

with col1:
    st.subheader("Datos Financieros y Crediticios")
    
    datos_cliente['Credit_Score'] = st.number_input("Puntuación Crediticia", min_value=500, max_value=900, value=750)
    datos_cliente['income'] = st.number_input("Ingreso Mensual", min_value=0.0, value=5000.0)
    datos_cliente['dtir1'] = st.slider("Ratio Deuda/Ingreso (DTI)", min_value=0.0, max_value=60.0, value=35.0, step=0.5)
    datos_cliente['loan_amount'] = st.number_input("Monto del Préstamo", min_value=10000, value=250000)
    datos_cliente['LTV'] = st.slider("Loan to Value (LTV) %", min_value=0.0, max_value=100.0, value=70.0, step=0.1)
    datos_cliente['property_value'] = st.number_input("Valor de la Propiedad", min_value=10000, value=350000)
    
    datos_cliente['open_credit'] = get_selectbox_input('open_credit', "Crédito Abierto")
    datos_cliente['credit_type'] = get_selectbox_input('credit_type', "Tipo de Crédito")
    datos_cliente['co-applicant_credit_type'] = get_selectbox_input('co-applicant_credit_type', "Crédito Co-aplicante") 

    datos_cliente['Credit_Worthiness'] = st.number_input("Solvencia Crediticia", min_value=0.0, value=1.0) 
    datos_cliente['rate_of_interest'] = st.number_input("Tasa de Interés (%)", min_value=0.0, value=4.5)

with col_space:
    pass

with col2:
    st.subheader("Datos del Préstamo y Personales")
    
    datos_cliente['loan_type'] = get_selectbox_input('loan_type', "Tipo de Préstamo")
    datos_cliente['loan_purpose'] = get_selectbox_input('loan_purpose', "Propósito del Préstamo")
    datos_cliente['Gender'] = get_selectbox_input('Gender', "Género")
    datos_cliente['approv_in_adv'] = get_selectbox_input('approv_in_adv', "Aprobado Anticipado")
    datos_cliente['business_or_commercial'] = get_selectbox_input('business_or_commercial', "Comercial")
    datos_cliente['occupancy_type'] = get_selectbox_input('occupancy_type', "Tipo de Ocupación")
    
    datos_cliente['term'] = st.selectbox("Plazo (meses)", [180, 360], index=1)
    datos_cliente['age'] = st.number_input("Edad", min_value=18, max_value=80, value=40)
    datos_cliente['total_units'] = st.number_input("Unidades Totales", min_value=1, max_value=4, value=1)

with col_space2:
    pass

with col3:
    st.subheader("Garantías y Condiciones")
    
    datos_cliente['Region'] = get_selectbox_input('Region', "Región")
    datos_cliente['Secured_by'] = get_selectbox_input('Secured_by', "Garantizado por")
    datos_cliente['Security_Type'] = get_selectbox_input('Security_Type', "Tipo de Garantía")
    datos_cliente['submission_of_application'] = get_selectbox_input('submission_of_application', "Envío Aplicación")
    datos_cliente['construction_type'] = get_selectbox_input('construction_type', "Tipo de Construcción")
    datos_cliente['loan_limit'] = get_selectbox_input('loan_limit', "Límite de Préstamo")
    datos_cliente['Neg_ammortization'] = get_selectbox_input('Neg_ammortization', "Amort. Negativa")
    datos_cliente['interest_only'] = get_selectbox_input('interest_only', "Solo Intereses")
    datos_cliente['lump_sum_payment'] = get_selectbox_input('lump_sum_payment', "Pago Global")
    
    datos_cliente['Interest_rate_spread'] = st.number_input("Diferencial de Tasa de Interés", min_value=-5.0, value=1.0)
    datos_cliente['Upfront_charges'] = st.number_input("Cargos Iniciales/Adelantados", min_value=0.0, value=1500.0)


# LÓGICA DE PREDICCIÓN (Llamada a Flask) 
st.markdown("---")
if st.button("Evaluar Riesgo Crediticio "):
    
    with st.spinner('Evaluando riesgo con la API...'):
        try:
            # Llama al Endpoint de Flask
            # Aseguramos que solo se envíen las 31 columnas necesarias y en el orden correcto
            data_to_send = {col: datos_cliente[col] for col in COLUMNAS_ESPERADAS}
            response = requests.post(FLASK_API_URL, json=data_to_send)
            
            if response.status_code == 200:
                result = response.json()
                
                # Obtener Resultados
                prob_default = result['probability_default']
                prediction_class = result['predicted_class']
                risk_status = result['prediction_status']
                threshold = result['threshold_used']

                # Mostrar Resultados
                st.markdown("### Resultado de la Evaluación")
                
                if prediction_class == 1:
                    st.error(f"**{risk_status}**")
                    st.write(f"Clasificado como Alto Riesgo basado en el umbral ajustado de: {threshold}")
                else:
                    st.success(f"**{risk_status}**")
                    st.write(f"Clasificado como Bajo Riesgo basado en el umbral ajustado de: {threshold}")

                st.metric("Probabilidad de Default (Riesgo)", f"{prob_default:.2%}", delta=f"Umbral: {threshold}")
                
                # Gráfico de barras
                chart_data = pd.DataFrame({
                    'Clase': ['Bajo Riesgo (0)', 'Alto Riesgo (1)'],
                    'Probabilidad': [result['probability_solvency'], prob_default]
                })
                st.bar_chart(chart_data.set_index('Clase'))

            else:
                st.error(f"❌ Error al conectar con la API de Flask (Código: {response.status_code}).")
                st.json(response.json())
                
        except requests.exceptions.ConnectionError:
            st.error(f"❌ ERROR: No se pudo conectar a la API de Flask en {FLASK_API_URL}. Por favor, asegúrese de que 'app.py' esté corriendo.")
        except Exception as e:
            st.error(f"Error inesperado: {e}")