# 🏦 Sistema de Clasificación de Riesgo Crediticio (Credit Risk Classification System)

Este proyecto implementa un sistema de Machine Learning de extremo a extremo (End-to-End) para clasificar el riesgo crediticio de solicitantes de préstamos. Consta de una API (Flask) que aloja un modelo optimizado (SVM/Pipeline) y una interfaz de usuario interactiva (Streamlit) para ingresar datos y visualizar la predicción.

---

## ✨ Características Principales

* **API RESTful (Flask):** Recibe solicitudes JSON y devuelve predicciones de riesgo en tiempo real.
* **Modelo Optimizado:** Utiliza un modelo de Machine Learning pre-entrenado y un umbral de decisión ajustado para maximizar la detección de riesgo (F1-Score).
* **Interfaz Interactiva (Streamlit):** Permite a los usuarios ingresar 31 características del préstamo y el solicitante a través de un formulario intuitivo en español.
* **Manejo de Columnas:** Implementa un control estricto de las 31 columnas requeridas y su orden, asegurando que el modelo reciba los datos correctamente.

---

## 🛠️ Estructura del Proyecto

El proyecto se compone de los siguientes archivos principales:

| Archivo | Descripción |
| :--- | :--- |
| `app.py` | Contiene la lógica de la **API de Flask**. Carga el modelo y define el endpoint `/credit_risk` para la predicción. |
| `streamlit_app.py` | Contiene la **interfaz de usuario (UI)**. Recoge los datos del usuario, los mapea a códigos técnicos y los envía a la API de Flask. |
| `best_credit_risk_model.pkl` | **El modelo pre-entrenado** (un archivo binario serializado que contiene el pipeline de preprocesamiento y el clasificador final). |
| `requirements.txt` | Lista todas las dependencias necesarias para ejecutar la API y la UI. |

---

## 🚀 Instalación y Ejecución

Sigue estos pasos para poner en marcha el sistema:

### 1. Prerrequisitos

Asegúrate de tener Python (versión 3.8+) y `pip` instalados.

### 2. Clona el Repositorio e Instala Dependencias

Necesitarás el archivo del modelo `best_credit_risk_model.pkl` en la raíz del proyecto.

```bash
# Crea o navega al directorio de tu proyecto
cd tu_proyecto_de_riesgo_crediticio

# Instala todas las dependencias usando requirements.txt
pip install -r requirements.txt
