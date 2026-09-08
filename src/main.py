# src/main.py
"""
Main entry point for the Safety Assistant Agent.
"""

import sys  # <--- AÑADE ESTA LÍNEA

# 1️⃣ PRIMER PRINT (al arrancar el archivo)
print("🔹 PASO 1: main.py cargado. A punto de importar el agente...")
sys.stdout.flush()

# 2️⃣ SEGUNDO PRINT (justo antes de la importación)
print("🔹 PASO 2: Importando 'src.agent.agent'...")
sys.stdout.flush()

from src.agent.agent import agent

# 3️⃣ TERCER PRINT (justo después de la importación)
print("🔹 PASO 3: Agente importado correctamente.")
sys.stdout.flush()


def main():
    """Main loop for the agent."""
    
    # 4️⃣ CUARTO PRINT (al entrar en la función main)
    print("🔹 PASO 4: Entrando en main()...")
    sys.stdout.flush()

    print("\n" + "="*50)
    print("   Safety Assistant Agent")
    print("="*50)
    print("\nType 'exit' to quit.\n")
    
    while True:
        question = input("👤 You: ").strip()
        
        if question.lower() in ["exit", "quit", "salir"]:
            print("\n👋 Goodbye!")
            break
        
        if not question:
            continue
        
        print("\n🤔 Agent thinking...")
        
        # 5️⃣ QUINTO PRINT (justo antes de invocar al agente)
        print("🔹 PASO 5: Invocando agent.invoke()...")
        sys.stdout.flush()
        
        response = agent.invoke(question)
        
        print(f"\n🤖 Agent: {response}\n")

if __name__ == "__main__":
    main()