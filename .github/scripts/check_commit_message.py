import sys
import re

# Obtener el archivo temporal que contiene el mensaje de commit desde los argumentos
commit_msg_filepath = sys.argv[1]

#Leer el mensaje de commit
with open(commit_msg_filepath, "r", encoding="utf-8") as file:
    commit_msg = file.read().strip()

#Definir el patrón regex
pattern = r"^(feat|chore|fix): .+"

#Validar el mensaje
if not re.match(r"^(feat|chore|fix): .+", commit_msg):
    print("Error: El mensaje debe seguir el formato 'tipo: descripción'")
    print("Ejemplos válidos:")
    print("feat: agregar login")
    print("chore: actualizar dependencias")
    print("fix: corregir error en API")
    sys.exit(1)

sys.exit(0)