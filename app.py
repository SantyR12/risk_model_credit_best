import joblib
import pandas as pd
from flask import Flask, request, jsonify
import numpy as np

# Definicion del modelo 
MODEL_PATH = 'best_credit_risk_model.pkl' 
OPTIMAL_THRESHOLD = 0.35 

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
# CARGA DEL MODELO 
try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modelo cargado exitosamente: {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    model = None

# INICIALIZACIÓN DE FLASK
app = Flask(__name__)

# ENDPOINT DE PREDICCIÓN 
@app.route('/credit_risk', methods=['POST'])
def predict():
    """Recibe datos JSON de un cliente, aplica el pipeline y devuelve la predicción."""
    if model is None:
        return jsonify({"error": "Modelo no cargado. Revisar .pkl"}), 500
    
    # Obtener Datos
    try:
        data = request.get_json(force=True)
        input_df = pd.DataFrame([data], columns=COLUMNAS_ESPERADAS)
    except Exception as e:
        return jsonify({"error": f"Fallo al procesar JSON o columnas incorrectas. Asegúrese de enviar las 31 columnas esperadas: {e}"}), 400

    # Realizar Predicción de Probabilidad
    try:
        probability = model.predict_proba(input_df)[0].tolist()
        prob_default = probability[1] # Probabilidad de clase 1 (Default/Alto Riesgo)

        # Aplicar el Umbral de Decisión Optimo
        prediction_class = 1 if prob_default >= OPTIMAL_THRESHOLD else 0
        
        # Preparar Respuesta
        risk_status = "ALTO RIESGO (DEFAULT)" if prediction_class == 1 else "BAJO RIESGO (SOLVENTE)"

        response = {
            "prediction_status": risk_status,
            "predicted_class": int(prediction_class),
            "probability_default": round(prob_default, 4),
            "probability_solvency": round(probability[0], 4),
            "threshold_used": OPTIMAL_THRESHOLD,
            "model_used": "Optimized SVM"
        }
        
        return jsonify(response)

    except Exception as e:
        print(f"Error en la predicción: {e}")
        return jsonify({"error": f"Error interno en la predicción del modelo: {e}"}), 500

# EJECUCIÓN DE LA APLICACIÓN 
if __name__ == '__main__':
    print("🚀 Iniciando Flask API en http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)