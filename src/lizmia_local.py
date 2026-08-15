import os
import sys
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "lizmia"
MEMORY_FILE = "memory.json"

def load_memory():
    """Carga el historial de conversación desde el archivo local si existe."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
                print(f"🧠 [Memoria]: Se cargaron {len(memory)} mensajes previos.")
                return memory
        except Exception as e:
            print(f"⚠️ [Error al cargar memoria]: {e}. Se iniciará sesión limpia.")
    return []

def save_memory(history):
    """Guarda el historial de conversación en un archivo JSON local."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        print("💾 [Memoria]: Conversación guardada con éxito.")
    except Exception as e:
        print(f"⚠️ [Error al guardar memoria]: {e}")

def chat_with_lizmia():
    history = load_memory()

    print("=" * 50)
    print("🧠 Lizmia Local - Inicializada y Lista")
    print("Escribe 'salir' para guardar y cerrar.")
    print("Escribe 'reset' para borrar la memoria local.")
    print("=" * 50 + "\n")

    while True:
        try:
            user_input = input("Tú: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["salir", "exit", "quit"]:
                print("\nLizmia: ¡Nos vemos!")
                save_memory(history)
                break

            if user_input.lower() == "reset":
                history = []
                if os.path.exists(MEMORY_FILE):
                    os.remove(MEMORY_FILE)
                print("\n🧹 [Memoria limpiada con éxito].\n")
                continue

            history.append({"role": "user", "content": user_input})

            payload = {
                "model": MODEL_NAME,
                "messages": history,
                "stream": True
            }

            print("\nLizmia: ", end="", flush=True)

            response = requests.post(OLLAMA_URL, json=payload, stream=True)
            
            full_response = ""
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        body = json.loads(line)
                        content = body.get("message", {}).get("content", "")
                        print(content, end="", flush=True)
                        full_response += content
                print("\n")
                
                history.append({"role": "assistant", "content": full_response})
            else:
                print(f"\n[Error]: Código {response.status_code} desde Ollama.")

        except KeyboardInterrupt:
            print("\n\nGuardando sesión antes de salir...")
            save_memory(history)
            sys.exit()
        except requests.exceptions.ConnectionError:
            print("\n[Error de conexión]: ¿Ollama está ejecutándose en tu equipo?")
            break

if __name__ == "__main__":
    chat_with_lizmia()
