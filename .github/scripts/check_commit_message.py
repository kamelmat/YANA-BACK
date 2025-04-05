import sys
import re

# Obtener el archivo temporal que contiene el mensaje de commit desde los argumentos
commit_msg_filepath = sys.argv[1]

# Leer el mensaje de commit
try:
    with open(commit_msg_filepath, "r", encoding="utf-8") as file:
        commit_msg = file.read().strip()
except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{commit_msg_filepath}'. Verifique la ruta y vuelva a intentarlo.")
    sys.exit(1)
except IOError as e:
    print(f"Error: No se pudo leer el archivo '{commit_msg_filepath}'. Detalles: {e}")
    sys.exit(1)

# Definir el patrón regex: debe empezar con feat, chore o fix seguido de dos puntos y un espacio
pattern = r"^(feat|chore|fix): .+"

# Validar el mensaje
if not re.match(pattern, commit_msg):
    print(f"Error: El mensaje de commit '{commit_msg}' no sigue el formato 'feat|chore|fix: <descripción>'")
    print("Ejemplo válido: 'feat: agregar nueva funcionalidad'")
    sys.exit(1)

# Si pasa la validación, salir con éxito
sys.exit(0)