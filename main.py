import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.filedatalake import DataLakeServiceClient
from dotenv import load_dotenv

# --- 1. CONFIGURACIÓN DE RUTAS ---
# BASE_DIR es donde está este archivo main.py (la raíz 'appweb')
BASE_DIR = Path(__file__).resolve().parent

# Cargamos el .env que está en la misma raíz
load_dotenv(dotenv_path=BASE_DIR / '.env')

# Definimos dónde está la UI realmente (dentro de la carpeta 'app')
UI_PATH = BASE_DIR / "app" / "ui"

# Configuración de Azure
AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
AZURE_FILE_SYSTEM = os.getenv("AZURE_FILE_SYSTEM")
AZURE_ACCESS_KEY = os.getenv("AZURE_ACCESS_KEY")
BRONZE_PATH = "bronze"

# Validación rápida
if not AZURE_ACCESS_KEY:
    print("⚠️ ADVERTENCIA: No se encontró AZURE_ACCESS_KEY en el archivo .env")

# --- 2. CONEXIÓN A AZURE ---
file_system_client = None
try:
    if AZURE_ACCOUNT_NAME and AZURE_ACCESS_KEY:
        service_client = DataLakeServiceClient(
            account_url=f"https://{AZURE_ACCOUNT_NAME}.dfs.core.windows.net",
            credential=AZURE_ACCESS_KEY
        )
        file_system_client = service_client.get_file_system_client(file_system=AZURE_FILE_SYSTEM)
        print(f"✅ Conectado a Azure Storage: {AZURE_ACCOUNT_NAME}/{AZURE_FILE_SYSTEM}")
    else:
        print("❌ Faltan credenciales de Azure en el .env")
except Exception as e:
    print(f"❌ Error conectando a Azure: {e}")

app = FastAPI()

# --- 3. SERVIR LA INTERFAZ (UI) ---
# Aquí estaba el error: ahora apuntamos a "app/ui"
if not os.path.exists(UI_PATH):
    print(f"❌ ERROR CRÍTICO: No encuentro la carpeta UI en: {UI_PATH}")
else:
    app.mount("/ui", StaticFiles(directory=UI_PATH), name="ui")

@app.get("/")
async def read_index():
    # Servimos el index desde app/ui/
    return FileResponse(UI_PATH / "index.html")

# --- 4. CONFIGURACIÓN CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 5. ENDPOINTS DE LA API ---

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file_system_client:
        raise HTTPException(status_code=500, detail="No hay conexión con Azure")
    
    try:
        file_path = f"{BRONZE_PATH}/{file.filename}"
        file_client = file_system_client.get_file_client(file_path)
        file_content = await file.read()
        file_client.upload_data(file_content, overwrite=True)
        return {"status": "ok", "filename": file.filename, "location": "bronze"}
    except Exception as e:
        print(f"Error subiendo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
def list_files():
    if not file_system_client:
        return {"files": []}
    try:
        paths = file_system_client.get_paths(path=BRONZE_PATH)
        files = [p.name.replace(f"{BRONZE_PATH}/", "") for p in paths if not p.is_directory]
        return {"files": files}
    except Exception as e:
        return {"error": str(e), "files": []}