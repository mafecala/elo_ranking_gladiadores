#  Sistema de Ranking para Gladiadores ⚔️

##  Autora🥝
María Fernanda Cala

##  Descripción 🗒️

Este sistema es una aplicación de escritorio desarrollada en Python con Tkinter que permite gestionar un ranking de jugadores y equipos utilizando el sistema de puntuación ELO. Puede mantener un registro de enfrentamientos, calcular automáticamente los rankings y organizar torneos entre los participantes. Está hecho teniendo en mente un ranking de softcombat.

  

##  Características principales 🌷

  

###  Gestión de Jugadores 

- Crear, editar y eliminar jugadores

- Asignar varias armas a cada jugador

- Seguimiento automático del puntaje ELO de cada jugador

  

###  Gestión de Equipos

- Crear, editar y eliminar equipos

- Asignar jugadores a cada equipo

- Seguimiento automático del puntaje ELO de cada equipo

  

###  Registro de Enfrentamientos

- Registrar enfrentamientos entre jugadores o entre equipos

- Seleccionar las armas utilizadas en cada enfrentamiento (modo jugador)

- Actualización automática de puntajes ELO según resultados

- Historial completo de todos los enfrentamientos realizados

  

###  Organización de Torneos

- Generar emparejamientos en formato Round Robin (todos contra todos)

- Generar enfrentamientos por eliminación directa

- Exportar la información del torneo a Excel

  

###  Funciones de Respaldo y Exportación

- Crear copias de seguridad de todos los datos

- Restaurar datos desde copias de seguridad

- Exportar toda la información a Excel (jugadores, equipos, historial)

  

##  Requisitos del sistema 💻

- Python 3.x

- Tkinter (incluido con la mayoría de las instalaciones de Python)

- pandas y openpyxl (para exportación a Excel)

  

##  Instalación ⏬

  

1. Asegúrate de tener Python instalado

2. Instala los paquetes necesarios:

```

pip install pandas openpyxl

```

3. Ejecuta el script:

```

python main.py

```


##  Sistema de Puntuación ELO 🏆

  

El programa utiliza el sistema ELO para calcular los rankings:

- Todos los jugadores y equipos comienzan con 1000 puntos

- Después de cada enfrentamiento, los puntos se recalculan según el resultado

- La fórmula considera la diferencia de puntuación entre los contrincantes

- Ganar contra un oponente de mayor puntuación otorga más puntos que ganar contra uno de menor puntuación

  

##  Almacenamiento de datos 📖

Todos los datos se guardan en un archivo JSON (`datos_ranking.json`) que mantiene la persistencia de la información entre sesiones.

  

##  Funciones adicionales 💕

- Recálculo automático de ELO si se elimina un enfrentamiento

- Opción para hacer copias de seguridad y restaurarlas

- Exportación de datos a Excel para análisis externos