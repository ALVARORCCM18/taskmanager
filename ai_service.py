"""
Módulo de Servicio de IA para Desglose de Tareas
==================================================

Proporciona funcionalidad para usar OpenAI (GPT-4) para desglosar
tareas complejas en subtareas simples y accionables.

Utiliza la API de OpenAI con las credenciales del archivo .env

Autor: Master Big School IA
Versión: 1.0
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener la clave API de OpenAI desde variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Inicializar cliente de OpenAI solo si la clave está disponible
if api_key:
    from openai import OpenAI
    # Crear instancia del cliente con la clave API
    client = OpenAI(api_key=api_key)
else:
    # Si no hay clave, cliente es None (se maneja en create_simple_task)
    client = None


def create_simple_task(description):
    """
    Genera subtareas simples a partir de una descripción compleja usando IA.
    
    Utiliza GPT-4 para:
    1. Analizar la descripción de tarea compleja
    2. Dividirla en 3-5 subtareas claras y accionables
    3. Parsear la respuesta en una lista de strings
    
    Args:
        description (str): Descripción de la tarea compleja a desglosar
    
    Returns:
        list[str]: Lista de subtareas generadas, o lista con mensaje de error
        
    Ejemplo:
        >>> create_simple_task("Organizar proyecto de software")
        [
            "Diseñar arquitectura del sistema",
            "Crear repositorio en GitHub",
            "Setupear entorno de desarrollo",
            "Escribir documentación inicial"
        ]
    """
    # Validar que el cliente de OpenAI esté configurado
    if not client:
        return ["Error: La API de OpenAI no está configurada. Configura OPENAI_API_KEY en .env"]
    
    try:
        # Crear el prompt para la IA
        # Le pedimos que genere entre 3-5 subtareas simples
        prompt = f"""Desglosa la siguiente tarea compleja en una lista de 3 a 5 subtareas simples y accionables. 
        Tarea: {description}

        Formato de respuesta:
        -subtarea 1
        -subtarea 2
        -subtarea 3
        -etc.

        Responde solo con la lista de subtareas, una por linea, empezando cada linea con un guion"""
        
        # Configurar parámetros para la llamada a OpenAI
        params = { 
            # Usar GPT-4 Turbo (más eficiente que GPT-4)
            "model": "gpt-4-turbo",
            # Mensajes para la conversación
            "messages": [
                # Rol de sistema: define el comportamiento de la IA
                {"role": "system", "content": "Eres un asistente de productividad experto que ayuda a desglosar tareas complejas en subtareas simples y accionables."},
                # Rol de usuario: la solicitud del usuario
                {"role": "user", "content": prompt}
            ],
            # Limitar la longitud de la respuesta
            "max_tokens": 150
        }

        # Realizar la llamada a la API de OpenAI
        response = client.chat.completions.create(**params)
        # Extraer el contenido de la respuesta y limpiar espacios
        content = response.choices[0].message.content.strip()

        # Lista para almacenar las subtareas parseadas
        subtasks = []

        # Parsear la respuesta línea por línea
        for line in content.split('\n'):
            # Limpiar espacios en blanco
            line = line.strip()
            # Validar que la línea no esté vacía y comience con guion
            if line and line.startswith("-"):
                # Remover el guion y espacios para obtener solo el texto
                subtask = line[1:].strip()
                # Validar que haya contenido después del guion
                if subtask:
                    # Añadir a la lista de subtareas
                    subtasks.append(subtask)
        
        # Retornar subtareas o mensaje de error si no se generaron
        return subtasks if subtasks else ["Error: No se han podido generar subtareas."]

    # Capturar cualquier excepción durante la llamada a la API
    except Exception:
        return [f"Error: No se ha podido realizar la conexion a OpenAI"]