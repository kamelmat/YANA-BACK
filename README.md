## **Requisitos Previos**  
- Python 3.7+ instalado.  
- Git instalado y configurado.  
- (Opcional) Entorno virtual recomendado.  

---

## **1. Configuración Inicial**  

### **1.1. Crear y activar entorno virtual (recomendado)**  
```bash
# Crear entorno virtual (Windows/Linux/macOS)
python -m venv venv

# Activar entorno en Windows
venv\Scripts\activate

# Activar entorno en Linux
source venv/Scripts/activate

# Instalar pre-commit**  
pip install pre-commit
```

---

## **2. Configurar el Hook para Mensajes de Commit**  

### **2.1. Crear el script de validación**  
- **Ruta del archivo**:  
  ```plaintext
  .github/scripts/check_commit_message.py
  ```  
- **Contenido del script**:  
  ```python
  import sys
  import re

  #Obtener el archivo temporal que contiene el mensaje de commit desde los argumentos
  commit_msg_filepath = sys.argv[1]

  #Leer el mensaje de commit
  with open(commit_msg_filepath, "r", encoding="utf-8") as file:
      commit_msg = file.read().strip()

  # Definir el patrón regex
  if not re.match(r"^(feat|chore|fix): .+", commit_msg):
      print("Error: El mensaje debe seguir el formato 'tipo: descripción'")
      print("Ejemplos válidos:")
      print("feat: agregar login")
      print("chore: actualizar dependencias")
      print("fix: corregir error en API")
      sys.exit(1)

  sys.exit(0)
  ```

### **2.2. Configurar `.pre-commit-config.yaml`**  
- **Archivo en la raíz del proyecto**:  
  ```yaml
  repos:
    - repo: local
      hooks:
        - id: check-commit-message
          name: Validar formato de commit
          entry: python .github/scripts/check_commit_message.py
          language: python
          stages: [commit-msg]
  ```

---

## **3. Instalar el Hook en el Repositorio**  
- **Instalar el hook (solo una vez por repositorio)**:  
  ```bash
  pre-commit install --hook-type commit-msg
  ```

- **Probar manualmente (opcional)**:  
  ```bash
  pre-commit run --all-files
  ```

---

## **4. Ejecutar el Servidor con Hooks**  

- **Instalar dependencias**:   
  ```bash
  pip install - r requirements.txt 
  ```

- **Iniciar el servidor**:   

  ```bash
  python3 site_app/manage.py runserver
  ```
