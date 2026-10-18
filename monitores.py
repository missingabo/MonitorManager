import subprocess
import json

ROTACIONES = {
    1: "none",
    2: "left",
    4: "right",
    8: "inverted"
}

def obtener_salidas():
    try:
        resultado = subprocess.run(
        ["kscreen-doctor", "--json"],
        capture_output=True,
        text=True
        )
        if resultado.returncode != 0:
            raise ValueError(resultado.stderr)

        datos = json.loads(resultado.stdout)
        salidas = datos["outputs"]
        return salidas
    except json.JSONDecodeError:
        raise
    
def listar_modos(nombre_monitor):
    try:    
        salidas = obtener_salidas()
        for salida in salidas:
            if salida["name"] == nombre_monitor:
                numero = 1
                modos_disponibles = []
                for modo in salida["modes"]:
                    modos_disponibles.append(modo)
                    print(f"{numero}. {modo['size']['width']}x{modo['size']['height']} @ {modo['refreshRate']} Hz")
                    numero += 1    
                return modos_disponibles
    except ValueError as e:
        print(e)


def seleccionar_modo(nombre_monitor):
    while True:
        try:    
            modos_disponibles = listar_modos(nombre_monitor)
            seleccion = int(input("Selecciona un número: "))
            if 1 <= seleccion <= len(modos_disponibles):
                seleccion -= 1
                modo_elegido = modos_disponibles[seleccion]
                return modo_elegido
            else: 
                print("Elección inválida")
        except ValueError:
            print("Tiene que ser un número")
def cambiar_modo(nombre_monitor, modo_elegido):
    comando = "output." + nombre_monitor + ".mode." + modo_elegido["id"]
    resultado = subprocess.run(
        ["kscreen-doctor", comando],
        capture_output=True,
        text=True
    )
    if resultado.returncode == 0:
        print("Modo cambiado correctamente.")
    return resultado.returncode

def posicionar_monitor(nombre_monitor, x, y):
    comando = "output." + nombre_monitor + ".position." + str(x) + "," + str(y)
    print(comando)
    resultado = subprocess.run(
        ["kscreen-doctor", comando],
        capture_output=True,
        text=True
    )
    if resultado.returncode == 0:
        print("Posición cambiada correctamente.")
    return resultado.returncode

def rotar_monitor(nombre_monitor, orientacion):
    comando = "output." + nombre_monitor + ".rotation." + orientacion
    resultado = subprocess.run(
        ["kscreen-doctor", comando],
        capture_output=True,
        text=True
    )
    if resultado.returncode == 0:
        print("Rotación cambiada con éxito.")
    return resultado.returncode

def mostrar_estado_monitores():
    salidas = obtener_salidas()
    texto = ""
    for salida in salidas:        
        for modo in salida["modes"]:
            if modo["id"] == salida["currentModeId"]:
                texto += f"Nombre: {salida["name"]}\n"
                texto += f"Resolución: {modo["size"]["width"]} x {modo["size"]["height"]}\n"
                texto += f"Hz: {modo["refreshRate"]}\n"
                texto += f"Posición: {salida["pos"]["x"]} {salida["pos"]["y"]}\n"
                texto += f"Rotación: {salida["rotation"]}\n\n"
    return texto

def seleccionar_monitor():   
    while True:
        salidas = obtener_salidas()
        numero = 1
        monitores = []
    
        for salida in salidas:       
            if salida["enabled"] and salida["connected"]:
                monitores.append(salida["name"])
                print(f"{numero}. {salida["name"]}")
                numero += 1
        try:
            eleccion = int(input("Escoge un monitor: "))
            if 1 <= eleccion <= len(monitores):
                print(f"Monitor elegido: {monitores[eleccion -1]}")
                return monitores[eleccion -1]
            else:
                print("Elección no válida")
                
        except ValueError:
            print("Debe ser un número.")
            
def activar_o_desactivar(nombre_monitor, accion):
    encontrado = False
    salidas = obtener_salidas()
    for salida in salidas:
        if salida["name"] == nombre_monitor:            
            encontrado = True
            if accion == "enable" and salida["enabled"] is True:
                raise ValueError("Error, el monitor ya está activado")               
            if accion == "disable" and salida["enabled"] is False:
                raise ValueError("Error, el monitor ya está desactivado")
                
    if not encontrado:
        raise ValueError("Monitor no encontrado")
    if accion not in ["enable", "disable"]:
            raise ValueError("Acción no válida")
    comando = "output." + nombre_monitor + "." + accion
    resultado = subprocess.run(
        ["kscreen-doctor", comando],
        capture_output=True,
        text=True
    )
    
    if resultado.returncode == 0:
        print("Operación realizada con éxito")
    else:
        raise ValueError(resultado.stderr)

def obtener_monitor_principal():
    salidas = obtener_salidas()
    for salida in salidas:
        if salida["name"] == "DisplayPort-0":
            return salida["name"]
    raise ValueError("Monitor principal no encontrado")

def guardar_config():
    configuracion = []
    salidas = obtener_salidas()
    for salida in salidas:
        if salida["connected"]:
            datos_monitor = {
                "name" : salida["name"],
                "mode" : salida["currentModeId"],
                "x" : salida["pos"]["x"],
                "y" : salida["pos"]["y"],
                "rotation" : salida["rotation"],
                "enabled" : salida["enabled"]
            }
            configuracion.append(datos_monitor)
    
    return configuracion

def modo_juego():
    
    configuracion = guardar_config()
    print("CONFIGURACIÓN GUARDADA:")
    print(configuracion)
    monitor_principal = obtener_monitor_principal()
    for monitor in configuracion:
        if monitor["name"] != monitor_principal:
            monitor_secundario = monitor
    activar_o_desactivar(monitor_secundario["name"], "disable")
    posicionar_monitor(monitor_principal, 0, 0)
    modos = listar_modos(monitor_principal)
    mejor_modo = None
    for modo in modos:
        if modo["size"]["width"] == 1440 and modo["size"]["height"] == 900:
            if mejor_modo is None or modo["refreshRate"] > mejor_modo["refreshRate"]:
                    mejor_modo = modo
            
    if mejor_modo is None:
        raise ValueError("Modo no encontrado")
    cambiar_modo(monitor_principal, mejor_modo)
    return configuracion

def restaurar_config(configuracion):
    comandos = []
    salidas = obtener_salidas()
    for monitor in configuracion:     
        comando = "output." + monitor["name"] + ".mode." + monitor["mode"]
        comandos.append(comando)
        comando_posicion = "output." + monitor["name"] + ".position." + str(monitor["x"]) + "," + str(monitor["y"])
        comandos.append(comando_posicion)
        comando_enabled = "output." + monitor["name"] + ".enable"     
        comando_disabled = "output." + monitor["name"] + ".disable"   
        rotacion = ROTACIONES.get(monitor["rotation"], "none")
        if rotacion is None:
            raise ValueError(f"Rotación desconocida: {monitor['rotacion']}")
        comando_rotacion = "output." + monitor["name"] + ".rotation." + rotacion
        comandos.append(comando_rotacion)   
        for salida in salidas:
            if monitor["enabled"] and not salida["enabled"]:
                comandos.append(comando_enabled)
            elif not monitor["enabled"] and salida["enabled"]:
                comandos.append(comando_disabled)
    print(comandos)
    resultado = subprocess.run(
            ["kscreen-doctor"] + comandos,
            capture_output=True,
            text=True
        )
    if resultado.returncode != 0:
        raise ValueError(resultado.stderr)
    print("Configuración restaurada")
    print("Código de salida:", resultado.returncode)
    print("Salida:", resultado.stdout)
    print("Errores:", resultado.stderr)




def menu():
    configuracion = None
    while True:
        print("--- MENÚ DE SISTEMA ---")
        print("1.- Mostrar estado de monitores")
        print("2.- Cambiar resolución / Hz")
        print("3.- Cambiar posición")
        print("4.- Rotar monitor")
        print("5.- Activar/Desactivar monitor")
        print("6.- Modo juego / Modo Normal")
        print("7.- Restaurar configuración")
        print("8.- Salir")

        try:
            opcion = input("Escoge un número: ")
            if opcion == "1":
                mostrar_estado_monitores()
            elif opcion == "2":
                try:
                    monitor = seleccionar_monitor()
                    modo = seleccionar_modo(monitor)
                    cambiar_modo(monitor, modo)
                except ValueError as e:
                    print(e)
            elif opcion == "3":
                while True:
                    try:
                        monitor = seleccionar_monitor()
                        x = int(input("Posición X: "))
                        y = int(input("Posición Y: "))
                        posicionar_monitor(monitor, x, y)
                        break
                    except ValueError:
                        print("Tiene que ser un número")
            elif opcion == "4":
                monitor = seleccionar_monitor()
                print("1. Normal")
                print("2. 90º Izquierda")
                print("3. 90º Derecha")
                print("4. 180º")
                while True:
                    try:
                        orientacion = input("¿A qué orientación quieres rotar la pantalla? Selecciona un número: ")
                        if orientacion == "1":
                            orientacion = "none"
                        elif orientacion == "2":
                            orientacion = "left"
                        elif orientacion == "3":
                            orientacion = "right"
                        elif orientacion == "4":
                            orientacion = "inverted"
                        else:
                            print("Elección inválida")
                            continue
                        rotar_monitor(monitor, orientacion)
                        break
                    except ValueError:
                        print("Tiene que ser un número")
            elif opcion == "5":
                monitor = seleccionar_monitor()
                print("1. Activar")
                print("2. Desactivar")
                accion = input("Selecciona una opción:")
                if accion == "1":
                    accion = "enable"
                elif accion == "2":
                    accion = "disable"
                activar_o_desactivar(monitor, accion)

            elif opcion == "6":
                configuracion = modo_juego()
            elif opcion == "7":
                if configuracion is None:
                    print("No hay ninguna configuración guardada")
                else:
                    restaurar_config(configuracion)
                    configuracion = None
            elif opcion == "8":
                break
            else:
                print("Elección inválida")
        except ValueError:
            print("Debe ser un número")