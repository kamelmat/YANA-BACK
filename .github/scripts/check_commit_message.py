import sys
import re

# El mensaje de commit se pasa como argumento al script
commit_msg = sys.argv[1]

# Regex para validar el formato: fix:, chore:, feat:
pattern = r"^(fix|chore|feat): .+"

if not re.match(pattern, commit_msg):
    print(f"Error: El mensaje de commit '{commit_msg}' no sigue el formato 'fix/chore/feat: <descripción>'")
    sys.exit(1)

sys.exit(0)