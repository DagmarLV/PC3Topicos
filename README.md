# 🏦 UniBank - Sistema Bancario con Programación Orientada a Aspectos (AOP)

![UniBank](https://img.shields.io/badge/UniBank-Sistema%20Bancario-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![AOP](https://img.shields.io/badge/AOP-Programaci%C3%B3n%20Orientada%20a%20Aspectos-orange)

## 📋 Descripción

UniBank es un sistema bancario completo que demuestra la implementación de **Programación Orientada a Aspectos (AOP)** utilizando:
- **Backend:** FastAPI (Python) con aspectos implementados como decoradores
- **Frontend:** React con Tailwind CSS
- **Aspectos:** Logging, Autenticación, Notificaciones

## ✨ Características Principales

- 🔐 **Autenticación JWT** con aspecto de autenticación
- 🏧 **Gestión de cuentas bancarias**
- 💸 **Transacciones:** Transferencias, depósitos, retiros
- 📊 **Logging automático** de todas las acciones (aspecto de auditoría)
- 📧 **Notificaciones por email** automáticas (aspecto de notificaciones)
- 🎨 **Interfaz moderna** con React y Tailwind CSS

## 🏗️ Aspectos Implementados (AOP)

### 1. **Aspecto de Logging** (`@log_access`)
- Registra automáticamente todas las acciones del usuario
- Captura: IP, user-agent, timestamp, acción realizada
- Se aplica transparentemente a todos los endpoints

### 2. **Aspecto de Autenticación** (`@authenticated`)
- Valida tokens JWT automáticamente
- Inyecta el usuario actual en las funciones
- Maneja errores 401 de forma centralizada

### 3. **Aspecto de Notificaciones** (`@notify_on_transaction`)
- Envía emails automáticos en transacciones
- Notifica tanto al remitente como al receptor
- Envía alertas de seguridad a administradores

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8+** - [Descargar aquí](https://python.org)
- **Node.js 16+** - [Descargar aquí](https://nodejs.org)
- **Git** - [Descargar aquí](https://git-scm.com)

### Verificar instalación:
```bash
python --version    # Debe mostrar Python 3.8+
node --version      # Debe mostrar v16+
npm --version       # Debe mostrar 8+
git --version       # Debe mostrar git version
```

## 🚀 Instalación y Configuración

### 1. **Clonar el Repositorio**
```bash
git clone https://github.com/DagmarLV/PC3Topicos/tree/test1
cd PC3Topicos
```

### 2. **Configurar Backend (FastAPI)**

#### 2.1 Crear y activar entorno virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

#### 2.2 Instalar dependencias Python
```bash
pip install -r requirements.txt
```

#### 2.3 Configurar variables de entorno
El archivo `.env` ya está configurado con valores por defecto:
```env
SECRET_KEY=UNIBANK_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./app/database/unibank.db
```

### 3. **Configurar Frontend (React)**

#### 3.1 Instalar dependencias Node.js
```bash
cd frontend
npm install
```

#### 3.2 Verificar instalación
Las dependencias incluyen:
- `react` y `react-dom` - Framework React
- `lucide-react` - Iconos
- `tailwindcss` - Estilos CSS

## ▶️ Ejecutar la Aplicación

### **Terminal 1: Backend**
```bash
# Desde la raíz del proyecto
# Asegúrate de que el entorno virtual esté activado
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Ejecutar servidor FastAPI
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**✅ Deberías ver:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
Usuario de la bóveda creada
Cuenta bancaria de la bóveda creada
```

### **Terminal 2: Frontend**
```bash
# Desde la carpeta frontend/
cd frontend
npm start
```

**✅ Deberías ver:**
```
Local:            http://localhost:3000
webpack compiled successfully
```

## 🌐 Acceder a la Aplicación

- **Frontend (Interfaz Usuario):** http://localhost:3000
- **Backend API:** http://127.0.0.1:8000
- **Documentación API:** http://127.0.0.1:8000/docs
- **API Alternativa:** http://127.0.0.1:8000/redoc

## 🧪 Guía de Pruebas

### 1. **Registro de Usuario**
1. Abrir http://localhost:3000
2. Llenar formulario "Registrarse":
   - **Email:** `test@uni.pe`
   - **Nombre:** `Usuario Test`
   - **Contraseña:** `123456`
   - **Rol:** `Usuario`
3. Click "Registrarse"

### 2. **Iniciar Sesión**
1. Usar las credenciales del registro
2. Click "Iniciar Sesión"
3. Serás redirigido al dashboard

### 3. **Crear Cuenta Bancaria**
1. Click "Nueva Cuenta"
2. Se generará automáticamente un número de cuenta
3. Saldo inicial: $0.00

### 4. **Realizar Transacciones**

#### Depósito:
1. Ir a pestaña "Transacciones"
2. Sección "Depositar": Monto `500`, seleccionar cuenta
3. Click "Depositar"

#### Retiro:
1. Sección "Retirar": Monto `100`, seleccionar cuenta
2. Click "Retirar"

#### Transferencia:
1. Crear segunda cuenta
2. Sección "Transferir": Cuenta origen, ID destino, monto
3. Click "Transferir"

### 5. **Ver Logs de Auditoría**
1. Click pestaña "Logs"
2. Ver todas las acciones registradas automáticamente

## 📁 Estructura del Proyecto

```
📂 UniBank/
├── 📂 app/                          # Backend FastAPI
│   ├── 📂 aspects/                  # Aspectos AOP
│   │   ├── auth_aspect.py          # Aspecto de autenticación
│   │   ├── log_aspect.py           # Aspecto de logging
│   │   └── notify_aspect.py        # Aspecto de notificaciones
│   ├── 📂 models/                   # Modelos de base de datos
│   ├── 📂 routes/                   # Endpoints de la API
│   ├── 📂 services/                 # Lógica de negocio
│   ├── 📂 schemas/                  # Schemas Pydantic
│   └── main.py                     # Punto de entrada
├── 📂 frontend/                     # Frontend React
│   ├── 📂 src/
│   │   ├── App.js                  # Componente principal
│   │   └── index.css               # Estilos Tailwind
│   ├── package.json                # Dependencias Node.js
│   └── tailwind.config.js          # Configuración Tailwind
├── requirements.txt                 # Dependencias Python
├── .env                            # Variables de entorno
├── .gitignore                      # Archivos ignorados
└── README.md                       # Este archivo
```

## 🔧 API Endpoints

### Autenticación
- `POST /auth/register` - Registrar usuario
- `POST /auth/token` - Obtener token JWT

### Cuentas Bancarias
- `GET /accounts` - Listar cuentas del usuario
- `POST /accounts` - Crear nueva cuenta
- `DELETE /accounts/{id}` - Eliminar cuenta

### Transacciones
- `POST /transactions` - Transferencia entre cuentas
- `POST /transactions/deposit` - Depositar dinero
- `POST /transactions/withdraw` - Retirar dinero
- `GET /transactions/{account_id}` - Historial de transacciones

### Logs
- `GET /access-logs` - Logs del usuario actual
- `GET /access-logs/all` - Todos los logs (solo admin)

## 💻 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno para Python
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **JWT** - Autenticación con tokens
- **SQLite** - Base de datos

### Frontend
- **React 18** - Framework de JavaScript
- **Tailwind CSS** - Framework de estilos
- **Lucide React** - Iconos
- **Fetch API** - Comunicación con backend

### Aspectos (AOP)
- **Decoradores Python** - Implementación de aspectos
- **Functools** - Preservación de metadatos de funciones

## 🔧 Solución de Problemas

### ❌ Error: "No module named 'app'"
```bash
# Asegúrate de estar en la raíz del proyecto y entorno activado
venv\Scripts\activate
pip install -r requirements.txt
```

### ❌ Error: "npm command not found"
```bash
# Instalar Node.js desde https://nodejs.org
node --version  # Verificar instalación
```

### ❌ Error de CORS en el frontend
```bash
# Verificar que el backend esté ejecutándose en puerto 8000
# El CORS ya está configurado en app/main.py
```

### ❌ Error: "Command 'tailwindcss' not found"
```bash
cd frontend
npm install  # Reinstalar dependencias
npm start
```

### ❌ Base de datos no se crea
```bash
# La base de datos se crea automáticamente al iniciar
# Si hay problemas, eliminar archivo .db y reiniciar
rm app/database/unibank.db  # Linux/Mac
del app\database\unibank.db  # Windows
```

## 🎯 Demostración de AOP

### Ver Aspectos en Acción:

1. **Logging:** Cada acción se registra automáticamente
2. **Notificaciones:** En la terminal del backend verás:
   ```
   [MOCK] send_email called
   Sending email to test@uni.pe
   Subject: Transaction Received
   Body: You have received 500.0 from account 0000-0000-0000-0000
   ```
3. **Autenticación:** Protección automática de endpoints

### Código de Ejemplo (Aspecto):
```python
@notify_on_transaction("sender")
@notify_on_transaction("receiver")
@log_access("create_transaction")
async def create_transaction():
    # Solo lógica de negocio - aspectos son transparentes
    return transfer_money()
```

## 👥 Colaboradores

- **Desarrolladores:** Tu equipo de clase
- **Curso:** Tópicos de Ingeniería de Software
- **Institución:** Universidad Nacional de Ingeniería

## 📝 Licencia

Este proyecto es parte de un trabajo académico para demostrar conceptos de Programación Orientada a Aspectos.

---

## 🚀 ¡Listo para Usar!

Una vez que sigas todos los pasos, tendrás:
- ✅ Backend FastAPI funcionando con AOP
- ✅ Frontend React complementado con Tailwind
- ✅ Sistema bancario completo
- ✅ Demostración práctica de aspectos

**¿Problemas?** Revisa la sección de solución de problemas o contacta al equipo.