import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import math
import random


DATA_FILE = "datos_ranking.json"

def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"jugadores": {}, "equipos": {}, "historial": []}

def guardar_datos():
    global datos
    with open(DATA_FILE, 'w') as f:
        json.dump(datos, f, indent=4)

def calcular_elo(elo1, elo2, resultado):
    K = 32
    expectativa = 1 / (1 + 10 ** ((elo2 - elo1) / 400))
    nuevo_elo1 = elo1 + K * (resultado - expectativa)
    return round(nuevo_elo1)

datos = cargar_datos()

ventana = tk.Tk()
ventana.title("Ranking de Jugadores y Equipos")
ventana.geometry("1000x700")

pestanas = ttk.Notebook(ventana)
pestanas.pack(fill='both', expand=True)

# ======================= PESTAÑA JUGADORES =============================
frame_jugadores = ttk.Frame(pestanas)
pestanas.add(frame_jugadores, text="Jugadores")

entry_nombre = ttk.Entry(frame_jugadores)
entry_arma = ttk.Entry(frame_jugadores)

btn_borrar_jugador = ttk.Button(frame_jugadores, text="Borrar Jugador")
btn_editar_jugador = ttk.Button(frame_jugadores, text="Editar Jugador")

lista_jugadores = tk.Listbox(frame_jugadores, width=50)
lista_jugadores.grid(row=3, column=0, columnspan=2, pady=10)

def actualizar_lista_jugadores():
    lista_jugadores.delete(0, tk.END)
    for nombre, info in sorted(datos['jugadores'].items(), key=lambda item: item[1]['elo'], reverse=True):
        armas = ', '.join(info['armas'])
        lista_jugadores.insert(tk.END, f"{nombre} - ELO: {info['elo']} - Armas: {armas}")

def crear_jugador():
    nombre = entry_nombre.get()
    armas = [a.strip() for a in entry_arma.get().split(',') if a.strip()]
    if nombre and armas:
        if nombre in datos['jugadores']:
            messagebox.showerror("Error", "Jugador ya existe")
            return
        datos['jugadores'][nombre] = {"elo": 1000, "armas": armas}
        guardar_datos()
        actualizar_lista_jugadores()
        actualizar_lista_jugadores_equipo()
        actualizar_comboboxes()
        actualizar_interfaz()
        entry_nombre.delete(0, tk.END)
        entry_arma.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "Completa todos los campos")

def borrar_jugador():
    seleccion = lista_jugadores.curselection()
    if not seleccion:
        return
    nombre = lista_jugadores.get(seleccion[0]).split(" - ")[0]
    if messagebox.askyesno("Confirmar", f"¿Eliminar al jugador '{nombre}'?"):
        datos['jugadores'].pop(nombre, None)
        guardar_datos()
        actualizar_lista_jugadores()
        actualizar_interfaz()
        actualizar_lista_jugadores_equipo()
        actualizar_comboboxes()

jugador_en_edicion = None 

def preparar_edicion_jugador():
    global jugador_en_edicion

    seleccion = lista_jugadores.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Selecciona un jugador para editar")
        return

    nombre = lista_jugadores.get(seleccion[0]).split(" - ")[0]
    jugador = datos['jugadores'][nombre]
    jugador_en_edicion = nombre

    # Rellenar los campos
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, nombre)
    entry_arma.delete(0, tk.END)
    entry_arma.insert(0, ', '.join(jugador['armas']))

    # Mostrar botón de guardar cambios
    btn_guardar_cambios_jugador.grid()

def guardar_cambios_jugador():
    global jugador_en_edicion

    if not jugador_en_edicion:
        return

    nuevo_nombre = entry_nombre.get().strip()
    nuevas_armas = [a.strip() for a in entry_arma.get().split(',') if a.strip()]

    if nuevo_nombre and nuevas_armas:
        # Actualizar datos del jugador
        jugador = datos['jugadores'].pop(jugador_en_edicion)
        jugador['armas'] = nuevas_armas
        datos['jugadores'][nuevo_nombre] = jugador

        # Actualizar nombre en el historial
        for entrada in datos['historial']:
            if entrada['tipo'] == "Jugador":
                if entrada['entidad1'] == jugador_en_edicion:
                    entrada['entidad1'] = nuevo_nombre
                if entrada['entidad2'] == jugador_en_edicion:
                    entrada['entidad2'] = nuevo_nombre
                if entrada['ganador'] == jugador_en_edicion:
                    entrada['ganador'] = nuevo_nombre

        guardar_datos()
        actualizar_lista_jugadores()
        actualizar_lista_jugadores_equipo()
        actualizar_interfaz()
        actualizar_comboboxes()
        actualizar_historial()

        # Limpiar y ocultar botón
        entry_nombre.delete(0, tk.END)
        entry_arma.delete(0, tk.END)
        btn_guardar_cambios_jugador.grid_remove()
        jugador_en_edicion = None

        messagebox.showinfo("Éxito", "¡Jugador actualizado!")
    else:
        messagebox.showwarning("Advertencia", "Completa todos los campos")
btn_guardar_cambios_jugador = ttk.Button(frame_jugadores, text="Guardar cambios", command=guardar_cambios_jugador)
btn_guardar_cambios_jugador.grid(row=5, column=0, columnspan=2, pady=5)
btn_guardar_cambios_jugador.grid_remove()  # Oculto por defecto


btn_crear_jugador = ttk.Button(frame_jugadores, text="Crear Jugador", command=crear_jugador)
btn_crear_jugador.grid(row=2, column=0, columnspan=2, pady=10)

btn_editar_jugador.config(command=preparar_edicion_jugador)
btn_editar_jugador.grid(row=4, column=0, pady=5)

btn_borrar_jugador.config(command=borrar_jugador)
btn_borrar_jugador.grid(row=4, column=1, pady=5)

entry_nombre.grid(row=0, column=1)
entry_arma.grid(row=1, column=1)
ttk.Label(frame_jugadores, text="Nombre:").grid(row=0, column=0)
ttk.Label(frame_jugadores, text="Armas (separadas por coma):").grid(row=1, column=0)

actualizar_lista_jugadores()

# ======================= PESTAÑA EQUIPOS =============================
equipo_en_edicion = None  

frame_equipos = ttk.Frame(pestanas)
pestanas.add(frame_equipos, text="Equipos")

entry_equipo = ttk.Entry(frame_equipos)
ttk.Label(frame_equipos, text="Nombre del equipo:").grid(row=0, column=0)
entry_equipo.grid(row=0, column=1)

lista_jugadores_equipo = tk.Listbox(frame_equipos, selectmode=tk.MULTIPLE, width=40, height=10)
lista_jugadores_equipo.grid(row=1, column=0, columnspan=2, pady=10)

lista_equipos = tk.Listbox(frame_equipos, width=50)
lista_equipos.grid(row=3, column=0, columnspan=2, pady=10)

btn_borrar_equipo = ttk.Button(frame_equipos, text="Borrar Equipo")
btn_editar_equipo = ttk.Button(frame_equipos, text="Editar Equipo")
btn_guardar_cambios = ttk.Button(frame_equipos, text="Guardar Cambios")  # Aparece solo si se edita

def actualizar_lista_jugadores_equipo():
    lista_jugadores_equipo.delete(0, tk.END)
    for nombre in sorted(datos['jugadores'], key=lambda n: datos['jugadores'][n]['elo'], reverse=True):
        lista_jugadores_equipo.insert(tk.END, nombre)

def actualizar_lista_equipos():
    lista_equipos.delete(0, tk.END)
    for nombre, info in sorted(datos['equipos'].items(), key=lambda item: item[1]['elo'], reverse=True):
        lista_equipos.insert(tk.END, f"{nombre} - ELO: {info['elo']} - Miembros: {', '.join(info['miembros'])}")
    entry_equipo.delete(0, tk.END)

def crear_equipo():
    nombre_equipo = entry_equipo.get().strip()
    indices = lista_jugadores_equipo.curselection()
    miembros = [lista_jugadores_equipo.get(i) for i in indices]
    if nombre_equipo and miembros:
        if nombre_equipo in datos['equipos']:
            messagebox.showerror("Error", "Equipo ya existe 😕")
            return
        datos['equipos'][nombre_equipo] = {"elo": 1000, "miembros": miembros}
        guardar_datos()
        actualizar_lista_equipos()
        actualizar_comboboxes()
        entry_equipo.delete(0, tk.END)
        lista_jugadores_equipo.selection_clear(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "Completa todos los campos y selecciona jugadores")

def borrar_equipo():
    seleccion = lista_equipos.curselection()
    if not seleccion:
        return
    nombre = lista_equipos.get(seleccion[0]).split(" - ")[0]
    if messagebox.askyesno("Confirmar", f"¿Eliminar el equipo '{nombre}'?"):
        datos['equipos'].pop(nombre, None)
        guardar_datos()
        actualizar_lista_equipos()
        actualizar_comboboxes()

def preparar_edicion_equipo():
    global equipo_en_edicion

    seleccion = lista_equipos.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Selecciona un equipo para editar")
        return

    nombre = lista_equipos.get(seleccion[0]).split(" - ")[0]
    equipo = datos['equipos'][nombre]
    equipo_en_edicion = nombre

    # Rellenar formulario
    entry_equipo.delete(0, tk.END)
    entry_equipo.insert(0, nombre)

    lista_jugadores_equipo.selection_clear(0, tk.END)
    for i in range(lista_jugadores_equipo.size()):
        jugador = lista_jugadores_equipo.get(i)
        if jugador in equipo['miembros']:
            lista_jugadores_equipo.selection_set(i)

    # Mostrar botón de guardar cambios
    btn_guardar_cambios.grid(row=5, column=0, columnspan=2, pady=5)

def guardar_cambios_equipo():
    global equipo_en_edicion

    if not equipo_en_edicion:
        return

    nuevo_nombre = entry_equipo.get().strip()
    indices = lista_jugadores_equipo.curselection()
    nuevos_miembros = [lista_jugadores_equipo.get(i) for i in indices]

    if not nuevo_nombre or not nuevos_miembros:
        messagebox.showwarning("Advertencia", "Completa todos los campos y selecciona jugadores")
        return

    if nuevo_nombre != equipo_en_edicion and nuevo_nombre in datos['equipos']:
        messagebox.showerror("Error", f"Ya existe un equipo con el nombre '{nuevo_nombre}'")
        return

    # Actualizar datos del equipo
    equipo = datos['equipos'].pop(equipo_en_edicion)
    equipo['miembros'] = nuevos_miembros
    datos['equipos'][nuevo_nombre] = equipo

    # ACTUALIZAR HISTORIAL 📝
    for entrada in datos['historial']:
        if entrada['tipo'] == "Equipo":
            if entrada['entidad1'] == equipo_en_edicion:
                entrada['entidad1'] = nuevo_nombre
            if entrada['entidad2'] == equipo_en_edicion:
                entrada['entidad2'] = nuevo_nombre
            if entrada['ganador'] == equipo_en_edicion:
                entrada['ganador'] = nuevo_nombre

    guardar_datos()
    actualizar_lista_equipos()
    actualizar_comboboxes()
    actualizar_historial()

    # Limpiar y ocultar botón
    entry_equipo.delete(0, tk.END)
    lista_jugadores_equipo.selection_clear(0, tk.END)
    btn_guardar_cambios.grid_remove()
    equipo_en_edicion = None

    messagebox.showinfo("Éxito", "¡Equipo actualizado!")


# Botones
btn_crear_equipo = ttk.Button(frame_equipos, text="Crear Equipo", command=crear_equipo)
btn_crear_equipo.grid(row=2, column=0, columnspan=2, pady=10)

btn_editar_equipo.config(command=preparar_edicion_equipo)
btn_editar_equipo.grid(row=4, column=0, pady=5)

btn_borrar_equipo.config(command=borrar_equipo)
btn_borrar_equipo.grid(row=4, column=1, pady=5)

btn_guardar_cambios.config(command=guardar_cambios_equipo)
btn_guardar_cambios.grid_remove()  # Inicialmente oculto

# Cargar datos al iniciar
actualizar_lista_jugadores_equipo()
actualizar_lista_equipos()


# ======================= PESTAÑA ENFRENTAMIENTOS =============================
frame_enfrentamientos = ttk.Frame(pestanas)
pestanas.add(frame_enfrentamientos, text="Enfrentamientos")

modo_var = tk.StringVar(value="Jugador")
ttk.Radiobutton(frame_enfrentamientos, text="Jugador vs Jugador", variable=modo_var, value="Jugador").grid(row=0, column=0)
ttk.Radiobutton(frame_enfrentamientos, text="Equipo vs Equipo", variable=modo_var, value="Equipo").grid(row=0, column=1)

combo_1 = ttk.Combobox(frame_enfrentamientos)
combo_2 = ttk.Combobox(frame_enfrentamientos)
combo_1.grid(row=1, column=0, padx=10, pady=10)
combo_2.grid(row=1, column=1, padx=10, pady=10)

arma_1 = ttk.Combobox(frame_enfrentamientos)
arma_2 = ttk.Combobox(frame_enfrentamientos)
arma_1.grid(row=2, column=0)
arma_2.grid(row=2, column=1)

def actualizar_armas(*args):
    if modo_var.get() == "Jugador":
        j1 = combo_1.get()
        j2 = combo_2.get()
        arma_1['values'] = datos['jugadores'].get(j1, {}).get('armas', [])
        arma_2['values'] = datos['jugadores'].get(j2, {}).get('armas', [])
    else:
        arma_1.grid_remove()
        arma_2.grid_remove()

combo_1.bind("<<ComboboxSelected>>", actualizar_armas)
combo_2.bind("<<ComboboxSelected>>", actualizar_armas)

modo_var.trace_add('write', lambda *args: actualizar_comboboxes())

combo_ganador = ttk.Combobox(frame_enfrentamientos)
ttk.Label(frame_enfrentamientos, text="Ganador:").grid(row=3, column=0)
combo_ganador.grid(row=3, column=1)

def actualizar_comboboxes():
    tipo = modo_var.get()
    if tipo == "Jugador":
        opciones = list(datos['jugadores'].keys())
        arma_1.grid()  # Mostrar armas
        arma_2.grid()
    else:
        opciones = list(datos['equipos'].keys())
        arma_1.grid_remove()  # Ocultar armas
        arma_2.grid_remove()

    combo_1['values'] = opciones
    combo_2['values'] = opciones
    combo_ganador['values'] = opciones

    combo_1.set("")
    combo_2.set("")
    combo_ganador.set("")

    if tipo == "Jugador":
        arma_1.set("")
        arma_2.set("")
        arma_1['values'] = []
        arma_2['values'] = []


actualizar_comboboxes()

btn_registrar = ttk.Button(frame_enfrentamientos, text="Registrar Enfrentamiento")
btn_registrar.grid(row=4, column=0, columnspan=2, pady=10)

lista_historial = tk.Listbox(frame_enfrentamientos, width=100)
lista_historial.grid(row=5, column=0, columnspan=2, pady=10)

btn_borrar_enfrentamiento = ttk.Button(frame_enfrentamientos, text="Borrar Enfrentamiento")
btn_borrar_enfrentamiento.grid(row=6, column=0, columnspan=2, pady=5)

def registrar_enfrentamiento():
    tipo = modo_var.get()
    entidad1 = combo_1.get()
    entidad2 = combo_2.get()
    ganador = combo_ganador.get()
    arma1 = arma_1.get() if tipo == "Jugador" else None
    arma2 = arma_2.get() if tipo == "Jugador" else None

    if not entidad1 or not entidad2 or not ganador:
        messagebox.showwarning("Advertencia", "Completa todos los campos")
        return
    if entidad1 == entidad2:
        messagebox.showerror("Error", "No pueden enfrentarse la misma entidad")
        return

    resultado = 1 if ganador == entidad1 else 0
    if tipo == "Jugador":
        if not arma1 or not arma2:
            messagebox.showwarning("Advertencia", "Selecciona armas usadas por cada jugador")
            return
        elo1, elo2 = datos['jugadores'][entidad1]['elo'], datos['jugadores'][entidad2]['elo']
        datos['jugadores'][entidad1]['elo'] = calcular_elo(elo1, elo2, resultado)
        datos['jugadores'][entidad2]['elo'] = calcular_elo(elo2, elo1, 1 - resultado)
    else:
        elo1, elo2 = datos['equipos'][entidad1]['elo'], datos['equipos'][entidad2]['elo']
        datos['equipos'][entidad1]['elo'] = calcular_elo(elo1, elo2, resultado)
        datos['equipos'][entidad2]['elo'] = calcular_elo(elo2, elo1, 1 - resultado)

    datos['historial'].append({
        "tipo": tipo,
        "entidad1": entidad1,
        "arma1": arma1,
        "entidad2": entidad2,
        "arma2": arma2,
        "ganador": ganador
    })
    guardar_datos()
    actualizar_lista_jugadores()
    actualizar_lista_equipos()
    actualizar_comboboxes()
    actualizar_historial()
    messagebox.showinfo("Éxito", "Enfrentamiento registrado")

btn_registrar.config(command=registrar_enfrentamiento)

def actualizar_historial():
    lista_historial.delete(0, tk.END)
    for i, entrada in enumerate(datos['historial']):
        tipo = entrada['tipo']
        ent1, ent2 = entrada['entidad1'], entrada['entidad2']
        arma1, arma2 = entrada.get('arma1', ''), entrada.get('arma2', '')
        ganador = entrada['ganador']
        detalle_armas = f" ({arma1} vs {arma2})" if tipo == "Jugador" else ""
        lista_historial.insert(tk.END, f"{i+1}. {tipo}: {ent1} vs {ent2}{detalle_armas} → Ganador: {ganador}")

actualizar_historial()

def recalcular_elos():
    # Reiniciar ELOs de jugadores y equipos
    for j in datos['jugadores']:
        datos['jugadores'][j]['elo'] = 1000
    for e in datos['equipos']:
        datos['equipos'][e]['elo'] = 1000

    # Reaplicar todos los enfrentamientos del historial
    for entrada in datos['historial']:
        tipo = entrada['tipo']
        entidad1 = entrada['entidad1']
        entidad2 = entrada['entidad2']
        ganador = entrada['ganador']

        if tipo == "Jugador":
            resultado = 1 if ganador == entidad1 else 0
            elo1 = datos['jugadores'][entidad1]['elo']
            elo2 = datos['jugadores'][entidad2]['elo']
            datos['jugadores'][entidad1]['elo'] = calcular_elo(elo1, elo2, resultado)
            datos['jugadores'][entidad2]['elo'] = calcular_elo(elo2, elo1, 1 - resultado)
        else:
            resultado = 1 if ganador == entidad1 else 0
            elo1 = datos['equipos'][entidad1]['elo']
            elo2 = datos['equipos'][entidad2]['elo']
            datos['equipos'][entidad1]['elo'] = calcular_elo(elo1, elo2, resultado)
            datos['equipos'][entidad2]['elo'] = calcular_elo(elo2, elo1, 1 - resultado)

def actualizar_interfaz():
    actualizar_lista_jugadores()
    actualizar_lista_jugadores_equipo()
    actualizar_lista_equipos()
    actualizar_comboboxes()
    actualizar_historial()
    actualizar_lista_torneo()

def borrar_enfrentamiento():
    seleccion = lista_historial.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Selecciona un enfrentamiento para borrar")
        return

    indice = seleccion[0]
    if messagebox.askyesno("Confirmar", "¿Eliminar este enfrentamiento del historial?"):
        datos['historial'].pop(indice)
        recalcular_elos()
        guardar_datos()
        actualizar_lista_jugadores()
        actualizar_lista_equipos()
        actualizar_comboboxes()
        actualizar_historial()

def hacer_backup_json():
    ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivo JSON", "*.json")])
    if ruta:
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Backup", f"Backup guardado exitosamente:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el backup:\n{str(e)}")

def guardar_datos_json():
    with open("datos_ranking.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def restaurar_backup_json():
    ruta_archivo = filedialog.askopenfilename(defaultextension=".json", filetypes=[("Archivo JSON", "*.json")])
    if not ruta_archivo:
        return

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            nuevos_datos = json.load(f)

        # Validar que las claves principales existan para evitar errores simples
        if not all(k in nuevos_datos for k in ("jugadores", "equipos", "historial")):
            raise ValueError("El archivo JSON no tiene la estructura esperada.")

        datos.clear()
        datos.update(nuevos_datos)

        guardar_datos_json()  # <<< Esta línea asegura la persistencia en disco

        messagebox.showinfo("Éxito", "Datos restaurados correctamente.")
        actualizar_interfaz()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo restaurar el backup:\n{e}")


def exportar_a_excel():
    # Importar pandas y asegurarnos que sea el primero que se ejecute en esta función
    try:
        import pandas as pd
    except ImportError:
        messagebox.showerror("Error", "Se requiere la biblioteca pandas. Instálala con 'pip install pandas openpyxl'")
        return
    
    # Solicitar ubicación donde guardar el archivo
    ruta = filedialog.asksaveasfilename(
        defaultextension=".xlsx", 
        filetypes=[("Archivo Excel", "*.xlsx")]
    )
    
    if not ruta:  # El usuario canceló la operación
        return
    
    try:
        # Crear un objeto ExcelWriter para escribir en múltiples hojas
        with pd.ExcelWriter(ruta, engine='openpyxl') as writer:
            # Exportar datos de jugadores
            jugadores_data = []
            for nombre, info in datos['jugadores'].items():
                jugadores_data.append({
                    'Nombre': nombre,
                    'ELO': info['elo'],
                    'Armas': ', '.join(info['armas'])
                })
            
            if jugadores_data:
                df_jugadores = pd.DataFrame(jugadores_data)
                df_jugadores = df_jugadores.sort_values('ELO', ascending=False)
                df_jugadores.to_excel(writer, sheet_name='Jugadores', index=False)
            
            # Exportar datos de equipos
            equipos_data = []
            for nombre, info in datos['equipos'].items():
                equipos_data.append({
                    'Nombre': nombre,
                    'ELO': info['elo'],
                    'Miembros': ', '.join(info['miembros'])
                })
            
            if equipos_data:
                df_equipos = pd.DataFrame(equipos_data)
                df_equipos = df_equipos.sort_values('ELO', ascending=False)
                df_equipos.to_excel(writer, sheet_name='Equipos', index=False)
            
            # Exportar historial de enfrentamientos
            historial_data = []
            for i, entrada in enumerate(datos['historial']):
                fila = {
                    'N°': i+1,
                    'Tipo': entrada['tipo'],
                    'Entidad 1': entrada['entidad1'],
                    'Entidad 2': entrada['entidad2'],
                    'Ganador': entrada['ganador']
                }
                
                # Agregar información de armas si es un enfrentamiento entre jugadores
                if entrada['tipo'] == 'Jugador':
                    fila['Arma 1'] = entrada.get('arma1', '')
                    fila['Arma 2'] = entrada.get('arma2', '')
                
                historial_data.append(fila)
            
            if historial_data:
                df_historial = pd.DataFrame(historial_data)
                df_historial.to_excel(writer, sheet_name='Historial', index=False)
        
        messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{ruta}")
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron exportar los datos:\n{str(e)}")

btn_exportar_excel = ttk.Button(frame_enfrentamientos, text="Exportar a Excel", command=exportar_a_excel)
btn_exportar_excel.grid(row=9, column=0, columnspan=2, pady=10)
btn_borrar_enfrentamiento = ttk.Button(frame_enfrentamientos, text="Borrar Enfrentamiento", command=borrar_enfrentamiento)
btn_borrar_enfrentamiento.grid(row=6, column=0, columnspan=2, pady=5)

btn_backup = ttk.Button(frame_enfrentamientos, text="Hacer Backup", command=hacer_backup_json)
btn_backup.grid(row=7, column=0, columnspan=2, pady=10)

btn_restaurar = ttk.Button(frame_enfrentamientos, text="Restaurar Backup", command=restaurar_backup_json)
btn_restaurar.grid(row=8, column=0, columnspan=2, pady=5)

btn_exportar_excel = ttk.Button(frame_enfrentamientos, text="Exportar a Excel", command=exportar_a_excel)
btn_exportar_excel.grid(row=9, column=0, columnspan=2, pady=10)

# ======================= PESTAÑA TORNEO =============================
frame_torneo = ttk.Frame(pestanas)
pestanas.add(frame_torneo, text="Torneo")

ttk.Label(frame_torneo, text="Selecciona jugadores para el torneo:").pack(pady=5)
lista_torneo_jugadores = tk.Listbox(frame_torneo, selectmode=tk.MULTIPLE, width=40, height=10)
lista_torneo_jugadores.pack(pady=5)

def actualizar_lista_torneo():
    lista_torneo_jugadores.delete(0, tk.END)
    for nombre in sorted(datos['jugadores'], key=lambda n: datos['jugadores'][n]['elo'], reverse=True):
        lista_torneo_jugadores.insert(tk.END, nombre)

actualizar_lista_torneo()

ttk.Label(frame_torneo, text="Enfrentamientos generados:").pack(pady=5)
lista_enfrentamientos_torneo = tk.Listbox(frame_torneo, width=80, height=15)
lista_enfrentamientos_torneo.pack(pady=5)

jugadores_torneo_actual = []  

def generar_round_robin():
    global jugadores_torneo_actual
    indices = lista_torneo_jugadores.curselection()
    jugadores = [lista_torneo_jugadores.get(i) for i in indices]

    lista_enfrentamientos_torneo.delete(0, tk.END)
    indices = lista_torneo_jugadores.curselection()
    jugadores = [lista_torneo_jugadores.get(i) for i in indices]
    if len(jugadores) < 2:
        messagebox.showwarning("Advertencia", "Selecciona al menos 2 jugadores")
        return
    enfrentamientos = [(a, b) for i, a in enumerate(jugadores) for b in jugadores[i+1:]]
    for j1, j2 in enfrentamientos:
        lista_enfrentamientos_torneo.insert(tk.END, f"{j1} vs {j2}")
    jugadores_torneo_actual = jugadores

def generar_eliminacion_directa():
    global jugadores_torneo_actual
    indices = lista_torneo_jugadores.curselection()
    jugadores = [lista_torneo_jugadores.get(i) for i in indices]
    lista_enfrentamientos_torneo.delete(0, tk.END)

    indices = lista_torneo_jugadores.curselection()
    jugadores = [lista_torneo_jugadores.get(i) for i in indices]
    if len(jugadores) < 2 or (len(jugadores) & (len(jugadores) - 1)) != 0:
        messagebox.showwarning("Advertencia", "Selecciona una cantidad de jugadores que sea potencia de 2 (2, 4, 8, 16...)")
        return
    random.shuffle(jugadores)
    ronda = 1
    while len(jugadores) > 1:
        lista_enfrentamientos_torneo.insert(tk.END, f"--- Ronda {ronda} ---")
        siguiente_ronda = []
        for i in range(0, len(jugadores), 2):
            j1, j2 = jugadores[i], jugadores[i+1]
            lista_enfrentamientos_torneo.insert(tk.END, f"{j1} vs {j2}")
            siguiente_ronda.append(f"Ganador({j1}/{j2})")
        jugadores = siguiente_ronda
        ronda += 1
    jugadores_torneo_actual = jugadores


def exportar_torneo_a_excel():
    try:
        import pandas as pd
    except ImportError:
        messagebox.showerror("Error", "Se requiere la biblioteca pandas. Instálala con 'pip install pandas openpyxl'")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Archivo Excel", "*.xlsx")],
        title="Guardar torneo como"
    )

    if not ruta:
        return

    try:
        # Obtener enfrentamientos del Listbox
        enfrentamientos = lista_enfrentamientos_torneo.get(0, tk.END)
        if not enfrentamientos:
            messagebox.showwarning("Sin datos", "No hay enfrentamientos para exportar.")
            return
        
        # usar los jugadores guardados del torneo generado
        if not jugadores_torneo_actual:
            messagebox.showwarning("Advertencia", "No hay datos del torneo para exportar.")
            return

        # Crear DataFrame para enfrentamientos
        df_enfrentamientos = pd.DataFrame({'Enfrentamiento': enfrentamientos})

        # Crear DataFrame resumen de jugadores
        df_jugadores = pd.DataFrame({'Jugadores del Torneo': jugadores_torneo_actual})

        # Crear un ExcelWriter para múltiples hojas
        with pd.ExcelWriter(ruta, engine='openpyxl') as writer:
            df_jugadores.to_excel(writer, sheet_name='Jugadores Torneo', index=False)
            df_enfrentamientos.to_excel(writer, sheet_name='Enfrentamientos', index=False)

        messagebox.showinfo("Éxito", f"Datos del torneo exportados correctamente a:\n{ruta}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron exportar los datos:\n{str(e)}")


frame_botones_torneo = ttk.Frame(frame_torneo)
frame_botones_torneo.pack(pady=10)

ttk.Button(frame_botones_torneo, text="Round Robin (Todos vs Todos)", command=generar_round_robin).grid(row=0, column=0, padx=5)
ttk.Button(frame_botones_torneo, text="Eliminación Directa", command=generar_eliminacion_directa).grid(row=0, column=1, padx=5)

ttk.Button(frame_botones_torneo, text="Exportar Torneo a Excel", command=exportar_torneo_a_excel).grid(row=0, column=3, padx=5)

btn_crear_equipo = ttk.Button(frame_equipos, text="Crear Equipo", command=crear_equipo)
btn_crear_equipo.grid(row=2, column=0, columnspan=2, pady=10)

btn_borrar_equipo.config(command=borrar_equipo)
btn_borrar_equipo.grid(row=4, column=1, pady=5)

actualizar_lista_jugadores_equipo()
actualizar_lista_equipos()

ventana.mainloop()
