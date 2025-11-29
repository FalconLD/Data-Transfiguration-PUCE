# Data Transfiguration: Pipeline de Ingeniería de Datos con IA

![Status](https://img.shields.io/badge/Status-Production_Ready_✅-success)
![Architecture](https://img.shields.io/badge/Arquitectura-Medallion_Lakehouse-blue)
![Stack](https://img.shields.io/badge/Stack-Azure_Fabric_&_Gemini_2.5_Flash-orange)
![IA](https://img.shields.io/badge/IA-Google_Gemini_2.5_Flash-purple)

> **Proyecto Final de Bases de Datos II - PUCE 2025**  
> Pontificia Universidad Católica del Ecuador  
> Autor: Leonardo Falconi

> **Un sistema con "Self-Healing Data"**: usa Inteligencia Artificial para leer el mercado real y corregir automáticamente los datos maestros de precios y productos.

---

## Resumen Ejecutivo

En cualquier empresa, los **precios maestros** se vuelven obsoletos rápidamente.  
Este proyecto resuelve ese problema con un pipeline inteligente que:

- Lee órdenes de compra reales en PDF (documentos no estructurados)
- Extrae información usando **Google Gemini 2.5 Flash**
- Actualiza automáticamente el catálogo maestro con precios reales del mercado
- **Si un producto se vendió más caro que el precio de lista → el maestro evoluciona solo**

### Características Diferenciales

| Ítem                              | Descripción                                                                 |
|-----------------------------------|-----------------------------------------------------------------------------|
| Ingesta Universal              | WebApp propia con Drag & Drop (FastAPI) para subir archivos al Data Lake   |
| IA Generativa Sin Plantillas   | Extracción 100% inteligente de PDFs complejos (OCR + contexto)             |
| Self-Healing Data              | El maestro de precios **aprende y se corrige** con cada venta procesada    |
| Delta Lake + DirectLake        | Tablas transaccionales, versionadas y óptimas para Power BI                |

---

## Arquitectura Técnica – Medallion Lakehouse

Flujo completo sobre **Microsoft Fabric + Azure**:

**Usuario** → WebApp (FastAPI) → Azure Data Lake Gen2 (Bronze) → Microsoft Fabric Lakehouse  
→ Spark + Gemini 2.5 Flash → Tablas Silver → Lógica Self-Healing → Tabla Gold (Delta)  
→ Power BI (DirectLake)

### Capas del Pipeline

| Capa       | Contenido                                                                                  | Tecnología                             |
|------------|--------------------------------------------------------------------------------------------|----------------------------------------|
| **Bronze** | Archivos crudos:<br>• `maestro_productos.csv`<br>• PDFs de órdenes y proformas            | ADLS Gen2 + Shortcuts                  |
| **Silver** | • `silver_maestro_productos` → catálogo limpio<br>• `silver_historial_ventas` → ventas extraídas por IA | PySpark + Google Gemini 2.5 Flash      |
| **Gold**   | `gold_maestro_inteligente` → **Self-Healing**:<br>Precios y productos se actualizan automáticamente | Delta Lake + Merge Inteligente         |

---

## Stack Tecnológico

| Categoría                  | Tecnología                                              |
|----------------------------|---------------------------------------------------------|
| Nube & Almacenamiento      | Microsoft Azure ADLS Gen2 + Microsoft Fabric (OneLake)  |
| Procesamiento              | PySpark, Delta Lake                                     |
| Inteligencia Artificial   | Google Gemini 2.5 Flash (API)                           |
| Backend Ingesta            | Python FastAPI + Uvicorn                                |
| Frontend Ingesta           | HTML5 + CSS3 + Vanilla JavaScript                       |
| Visualización              | Power BI (DirectLake + SQL Endpoint)                    |

---

## Instrucciones de Ejecución

### Prerrequisitos
- Cuenta activa de **Microsoft Fabric**
- Storage Account Azure con **ADLS Gen2**
- API Key de **Google AI Studio** (Gemini)
- Python 3.10+ local

### Paso 1 – Levantar WebApp de Ingesta (Local)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar credenciales
cp .env

# → Edita:
AZURE_ACCOUNT_NAME=xxxxxx
AZURE_FILE_SYSTEM=xxxxxx
AZURE_ACCESS_KEY=xxxxxx

# 3. Ejecutar
uvicorn main:app --reload
```

Abre http://127.0.0.1:8000  
→ Arrastra y suelta el archivo maestro (.csv) y todos los PDFs que quieras procesar

### Paso 2 – Ejecutar Pipeline (Microsoft Fabric)

1. Abre el Notebook dentro de tu workspace de Fabric
2. Configura la variable `GEMINI_API_KEY`
3. Ejecuta todas las celdas (**Run All**)

Los archivos procesados se mueven automáticamente a la carpeta `archive/` y las tablas Delta se actualizan.

### Paso 3 – Visualizar Resultados

Abre el reporte de Power BI conectado al Lakehouse → **Actualizar**  
Verás cómo el maestro inteligente evoluciona en tiempo real

---

## Estructura del Repositorio

```
/
├── main.py                  # Backend API (FastAPI) - EJECUCIÓN DIRECTA
├── requirements.txt         # Dependencias Python
├── .env                     # Variables de entorno y claves secretas
├── .gitignore
├── README.md
├── app/                     # Código principal de la aplicación
│   └── __pycache__/
├── ui/                      # Interfaz de Usuario (Frontend HTML/CSS/JS)
│   ├── assets/
│   ├── css/
│   ├── js/
│   └── index.html
├── resources/               # Material de apoyo
│   └── data/                # (vacío o no visible en la captura)
├── docs/                    # Documentación y material del proyecto
│   ├── Projects.pdf
│   └── PUCE_BD22_Material_P1.pdf
├── notebooks/               # Jupyter Notebooks del proyecto
│   ├── Notebook_V3.1.ipynb
│   ├── Notebook_V3.ipynb
│   └── Notebook_V4.1.ipynb
├── __pycache__/
└── .venv/                   # Entorno virtual (opcional, depende del sistema)
```

---

## Autor

**Leonardo Falconi**  
Ingeniería en Datos – *Bases de Datos II*  
Pontificia Universidad Católica del Ecuador (PUCE) – 2025