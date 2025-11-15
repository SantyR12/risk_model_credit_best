import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- CONFIGURACIÓN CLAVE ---

# Define el nombre del archivo de tu mejor modelo guardado
MODEL_PATH = "best_credit_risk_model.pkl"

# Estas son las 31 columnas originales (excluyendo 'ID', 'year' y 'Status') 
# en el ORDEN exacto que el modelo (X_train) espera. 
# Esto es CRÍTICO para que el ColumnTransformer funcione correctamente.
EXPECTED_COLUMNS = [
    'loan_limit', 'Gender', 'approv_in_adv', 'loan_type', 'loan_purpose', 
    'Credit_Worthiness', 'open_credit', 'business_or_commercial', 
    'Neg_ammortization', 'interest_only', 'lump_sum_payment', 
    'construction_type', 'occupancy_type', 'Secured_by', 'total_units', 
    'credit_type', 'co-applicant_credit_type', 'age', 
    'submission_of_application', 'Region', 'Security_Type', 
    'loan_amount', 'rate_of_interest', 'Interest_rate_spread', 
    'Upfront_charges', 'term', 'property_value', 'income', 
    'Credit_Score', 'LTV', 'dtir1'
]

# --- INICIALIZACIÓN ---
app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir solicitudes desde otros orígenes
model = None

def load_model():
    """Carga el modelo pre-entrenado al iniciar la aplicación."""
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print(f"✅ Modelo cargado exitosamente desde: {MODEL_PATH}")
    except Exception as e:
        print(f"❌ ERROR al cargar el modelo: {e}")
        model = None

# Cargar el modelo al inicio
load_model()


# --- ENDPOINT DE PREDICCIÓN ---

@app.route('/credit_risk', methods=['POST'])
def predict_credit_risk():
    """
    Endpoint principal para recibir datos de clientes y predecir el riesgo.
    Espera un JSON con las 31 claves de EXPECTED_COLUMNS.
    """
    if model is None:
        return jsonify({"error": "Modelo no cargado. Verifique el archivo .pkl"}), 500

    try:
        # 1. Obtener los datos del cliente desde el cuerpo de la petición POST
        data = request.get_json(force=True)
        
        # 2. Convertir los datos a un DataFrame de Pandas
        # Usamos index=[0] para manejar un solo registro JSON
        new_data = pd.DataFrame([data])
        
        # 3. Validar y reordenar las columnas (CRÍTICO)
        if not all(col in new_data.columns for col in EXPECTED_COLUMNS):
            missing_cols = [col for col in EXPECTED_COLUMNS if col not in new_data.columns]
            return jsonify({
                "error": "Datos de entrada incompletos o incorrectos.",
                "detalles": f"Faltan las siguientes columnas: {missing_cols}"
            }), 400

        # Aseguramos el orden de las columnas para el Pipeline
        new_data = new_data[EXPECTED_COLUMNS]

        # 4. Realizar la predicción
        prediction = model.predict(new_data)[0]
        # Obtener las probabilidades: [Probabilidad_Clase_0, Probabilidad_Clase_1]
        probabilities = model.predict_proba(new_data)[0]

        # 5. Formatear la respuesta
        result = {
            'prediction': int(prediction),
            'probability_no_default': float(probabilities[0]),
            'probability_default': float(probabilities[1]),
            'status_explanation': "0: No Default (Bajo Riesgo), 1: Default (Alto Riesgo)"
        }

        return jsonify(result)

    except Exception as e:
        # Manejo de cualquier otro error no previsto (ej. en el preprocesamiento)
        return jsonify({"error": f"Error interno en la predicción: {str(e)}"}), 500

# --- EJECUCIÓN DEL SERVIDOR ---

if __name__ == '__main__':
    # Usar el puerto 5000 por defecto
    print("Iniciando servidor Flask...")
    # host='0.0.0.0' permite acceder desde otras máquinas en la red (o desde Colab/Ngrok)
    app.run(host='0.0.0.0', port=5000)