# 📋 Gestor de Tareas Inteligente

Un gestor de tareas moderno y funcional desarrollado en Python con capacidades potenciadas por IA para desglosar tareas complejas en subtareas simples.

## 🎯 Características Principales

### ✨ Funcionalidades Básicas
- **Añadir tareas**: Crea nuevas tareas con descripción
- **Ver tareas**: Lista todas las tareas con su estado
- **Completar tareas**: Marca tareas como completadas
- **Eliminar tareas**: Elimina tareas del gestor
- **Persistencia**: Guarda automáticamente las tareas en archivo JSON

### 🤖 Inteligencia Artificial
- **Desglose de tareas complejas**: Utiliza OpenAI (GPT-4) para dividir tareas complejas en subtareas accionables (3-5 subtareas)
- **Generación automática**: Las subtareas se crean automáticamente a partir de una descripción compleja

### 💾 Gestión de Datos
- **Almacenamiento persistente**: Las tareas se guardan en `tasks.json`
- **Auto-carga**: Las tareas se cargan automáticamente al iniciar el programa
- **IDs auto-incrementales**: Cada tarea recibe un ID único que se mantiene tras eliminaciones

## 📁 Estructura del Proyecto

```
TaskManager/
├── main.py                    # Interfaz principal con menú interactivo
├── task_manager.py            # Lógica del gestor de tareas (Task, TaskManager)
├── ai_service.py              # Servicio de integración con OpenAI
├── test_task_manager.py       # Tests unitarios (20 tests)
├── requirements.txt           # Dependencias del proyecto
├── .env                       # Configuración de variables de entorno
├── .env.example               # Plantilla de configuración
├── tasks.json                 # Archivo de persistencia de datos
├── README.md                  # Este archivo
└── __pycache__/              # Caché de Python


```

## 🚀 Instalación y Configuración

### 1. Requisitos Previos
- **Python 3.10 o superior** (para soporte de `match/case`)
- **pip** (gestor de paquetes de Python)

### 2. Clonar/Descargar el Proyecto
```bash
cd /ruta/al/proyecto
```

### 3. Crear Entorno Virtual (Opcional pero Recomendado)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno (Opcional para IA)

Crea un archivo `.env` en la raíz del proyecto:
```env
OPENAI_API_KEY=tu_clave_api_aqui
```

> **Nota**: Sin la clave de OpenAI, el programa funciona normalmente. Solo la opción 2 (tareas con IA) mostrará un error.

## 📖 Uso del Programa

### Ejecutar el Programa
```bash
python main.py
```

### Menú Principal
```
-----------Gestor de tareas inteligente-----------
1. Añadir tarea
2. Añadir tarea compleja (con IA)
3. Ver tareas
4. Completar tarea
5. Eliminar tarea
6. Salir
```

### Ejemplos de Uso

#### Ejemplo 1: Añadir una Tarea Simple
```
Selecciona una opción: 1
Descripción de la tarea: Comprar leche
Tarea añadida: Comprar leche
```

#### Ejemplo 2: Ver tareas
```
Selecciona una opción: 3
[ ] #1: Comprar leche
[✓] #2: Hacer ejercicio
```

#### Ejemplo 3: Completar una Tarea
```
Selecciona una opción: 4
ID de la tarea a completar: 1
Tarea completada: [✓] #1: Comprar leche
```

#### Ejemplo 4: Usar IA para Desglosar (Requiere OpenAI)
```
Selecciona una opción: 2
Descripción de la tarea compleja: Organizar proyecto de software
- Diseñar arquitectura
- Configurar repositorio Git
- Crear estructura de carpetas
- Establecer pipeline CI/CD
- Documentar API
```

## 🏗️ Estructura del Código

### `task_manager.py`

#### Clase `Task`
```python
class Task:
    def __init__(self, task_id: int, description: str, completed: bool = False)
```
Representa una tarea individual con ID, descripción y estado.

#### Clase `TaskManager`
```python
class TaskManager:
    def add_task(description: str) -> None
    def complete_task(task_id: int) -> None
    def delete_task(task_id: int) -> None
    def list_tasks() -> None
    def load_tasks() -> None
    def save_tasks() -> None
```
Gestiona todas las operaciones con tareas: añadir, completar, eliminar, persistencia.

### `ai_service.py`
```python
def create_simple_task(description: str) -> List[str]
```
Conecta con OpenAI API para generar subtareas a partir de una descripción compleja.

**Parámetros usados:**
- `model`: "gpt-4-turbo"
- `max_tokens`: 150
- `temperature`: por defecto (0.7)

### `main.py`
Interfaz de usuario con menú interactivo usando `match/case` (Python 3.10+).

Incluye manejo de errores:
- Validación de entrada numérica
- Captura de excepciones de valor inválido

## 🧪 Testing

### Ejecutar los Tests
```bash
# Con unittest (incluido en Python)
python -m unittest test_task_manager -v

# Con pytest (si está instalado)
pytest test_task_manager.py -v
```

### Cobertura de Tests (20 Tests)

#### Tests de Task (4 tests)
- ✓ Creación básica de tarea
- ✓ Creación con estado completado
- ✓ Representación en string (incompleta)
- ✓ Representación en string (completa)

#### Tests de TaskManager (16 tests)
- ✓ Inicialización del gestor
- ✓ Añadir tarea individual
- ✓ Añadir múltiples tareas con IDs auto-incrementales
- ✓ Completar tarea existente
- ✓ Intentar completar tarea inexistente
- ✓ Eliminar tarea existente
- ✓ Intentar eliminar tarea inexistente
- ✓ Eliminar tarea específica de múltiples
- ✓ Listar tareas vacías
- ✓ Listar múltiples tareas
- ✓ Guardar tareas en archivo JSON
- ✓ Cargar tareas del archivo
- ✓ Comportamiento cuando archivo no existe
- ✓ Persistencia entre instancias
- ✓ IDs continúan incrementándose tras borrar
- ✓ Estado completado se persiste en archivo

### Resultado de Tests
```
Ran 20 tests in 0.045s - OK ✅
```

## 📦 Dependencias

| Paquete | Versión | Uso |
|---------|---------|-----|
| openai | 2.29.0 | Cliente de API OpenAI |
| python-dotenv | 1.2.2 | Gestión de variables de entorno |
| pydantic | 2.12.5 | Validación de datos |
| requests | 2.32.5 | Solicitudes HTTP |
| tqdm | 4.67.3 | Barra de progreso |

## 🔧 Configuración de Entorno

### Variables de Entorno
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Obtén tu clave en: https://platform.openai.com/api-keys

## 📝 Archivos Generados

- **`tasks.json`**: Almacena todas las tareas en formato JSON
- **`.venv/`**: Entorno virtual de Python (si lo creaste)
- **`__pycache__/`**: Caché de bytecode de Python

## 🐛 Troubleshooting

### Error: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Error: "OPENAI_API_KEY not found"
Solución: Configura la clave en `.env` o la opción 2 (IA) mostrará un error controlado.

### Error: "match/case not supported"
Asegúrate de usar Python 3.10+:
```bash
python --version
```

### Error: "FileNotFoundError: tasks.json"
Normal en la primera ejecución. Se creará automáticamente al añadir la primera tarea.

## 🎓 Flujo de Trabajo Recomendado

1. **Crear tareas**: Usa opción 1 para tareas simples, opción 2 para complejas
2. **Consultar**: Opción 3 para ver todas las tareas
3. **Actualizar estado**: Opción 4 para marcar como completadas
4. **Limpiar**: Opción 5 para eliminar tareas finalizadas
5. **Salir**: Opción 6 (datos se guardan automáticamente)

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~300 (sin tests)
- **Tests unitarios**: 20
- **Cobertura**: Core functionality 100%
- **Dependencias externas**: 5 principales
- **Python mínimo**: 3.10

## 🚀 Mejoras Futuras

- [ ] Interfaz gráfica (Tkinter/PyQt)
- [ ] Base de datos (SQLite/PostgreSQL)
- [ ] Sincronización en la nube
- [ ] Notifications/Recordatorios
- [ ] Categorías/Tags para tareas
- [ ] Filtrado y búsqueda avanzada
- [ ] Prioridades en tareas
- [ ] Fechas límite (deadlines)
- [ ] Registro de historial
- [ ] API REST

## 👤 Autor

Álvaro Rodríguez Corral
Desarrollado como proyecto educativo en Master Big School IA

## 📄 Licencia

Este proyecto es de uso libre para propósitos educativos y personales.

## 📞 Soporte

Para preguntas o problemas, revisa los tests unitarios en `test_task_manager.py` para ejemplos de uso.

---

**Última actualización**: Marzo 2026  
**Estado**: ✅ Funcional y Testeado  
**Versión**: 1.0
