# Control de Monitores

Aplicación de escritorio desarrollada en Python y PySide6 para gestionar monitores en Linux con KDE Plasma.

El objetivo del proyecto es facilitar la configuración de las pantallas mediante una interfaz gráfica, sin necesidad de introducir manualmente todos los comandos en la terminal.

## Características

- Consultar información sobre los monitores conectados.
- Cambiar la resolución y la frecuencia de refresco.
- Modificar la posición de los monitores.
- Cambiar la orientación de las pantallas.
- Activar y desactivar monitores.
- Guardar la configuración actual.
- Restaurar una configuración guardada.
- Aplicar un modo de juego con una disposición de pantalla específica.

## Tecnologías utilizadas

- Python
- PySide6
- Qt
- KDE Plasma
- `kscreen-doctor`
- Git y GitHub

## Requisitos

- Linux con KDE Plasma.
- Python 3.
- PySide6.
- `kscreen-doctor`.

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/missingabo/MonitorManager.git
cd MonitorManager
```

Crea un entorno virtual:

```bash
python -m venv .venv
```

Activa el entorno virtual:

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install PySide6
```

## Ejecución

Ejecuta la aplicación con:

```bash
python main.py
```

## Estructura del proyecto

```text
MonitorManager/
├── main.py
├── monitores.py
├── .gitignore
└── README.md
```

### Descripción de los archivos

- `main.py`: contiene la interfaz gráfica y la lógica de interacción con el usuario.
- `monitores.py`: contiene las funciones para consultar y modificar la configuración de los monitores.
- `.gitignore`: especifica los archivos y directorios que Git debe ignorar.
- `README.md`: documentación del proyecto.

## Estado del proyecto

El proyecto se encuentra en desarrollo. Se irán incorporando mejoras y nuevas funcionalidades durante su evolución.

## Objetivos de aprendizaje

Este proyecto me permite practicar:

- Programación con Python.
- Programación orientada a objetos.
- Desarrollo de interfaces gráficas con PySide6.
- Ejecución de comandos del sistema desde Python.
- Gestión de errores.
- Control de versiones con Git y GitHub.