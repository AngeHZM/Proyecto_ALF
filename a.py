import re, random
from Menu import menuPrincipal, despedida
from collections import deque
reglas = {}
no_terminales = []
terminales = []
ALeido = "no"
def selArchivo():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(title="Selecciona un archivo")
    return archivo
        
        
def iniciarPrograma():
    menuPrincipal()
    elect = input(f"Ingresa la opción a realizar: ")
    match elect:
        case "1":
            menuGramatica()
        case "2":
            menuAutomatas()
        case "3":
            print("en proceso...")
        case "4":
            despedida()
        case _:
            print("Opción incorrecta...\n")
            iniciarPrograma()

def seleccionOpcion():
    eleccion = input("""Desea realizar otra opción? (๑ᵔ⤙ᵔ๑)  
    escriba: [SI]   [NO] : """).upper().strip()
    match eleccion:
        case "SI":
            iniciarPrograma()
        case "NO":
            despedida()
            
        case _:
            print("Elección incorrecta, intenta volver a escribirla (⸝⸝๑﹏๑⸝⸝) ")
            seleccionOpcion()
    return

def seleccionOpcionAutomatas():
    eleccion = input("""\nDesea realizar otra opción? (๑ᵔ⤙ᵔ๑)  
    escriba: [SI]   [NO] :\n """).upper().strip()
    match eleccion:
        case "SI":
            menuAutomatas()
        case "NO":
            despedida()
            
        case _:
            print("Elección incorrecta, intenta volver a escribirla (⸝⸝๑﹏๑⸝⸝) ")
            seleccionOpcion()
    return

def leerArchivo():
    global reglas, no_terminales, terminales, Bandera
    archivo = selArchivo()
    with open(archivo, 'r') as f:
        contenido = f.read()
    
    no_terminales = re.search(r'N\{(.*?)\}', contenido)
    terminales = re.search(r'T\{(.*?)\}', contenido)
    producciones = re.search(r'P\{(.*?)\}', contenido, re.DOTALL)
    
    if no_terminales:
        no_terminales = no_terminales.group(1).split(',')
    else:
        print("No hay elementos no_terminales en el archivo")
    if terminales:
        terminales = terminales.group(1).split(',')
    else:
        print("No hay terminales en el archivo")
        
    reglas = {}
    global ALeido
    ALeido = "si"

    if producciones:
        print(producciones)
        for linea in producciones.group(1).split(','):
            linea = linea.strip()
            if linea:
                lado_izq, lado_der = linea.split('>')
                lado_izq = lado_izq.strip()
                lado_der = [p.strip() for p in lado_der.split('|')]
                if lado_izq in reglas:
                    reglas[lado_izq].extend(lado_der)
                else:
                    reglas[lado_izq] = lado_der

def mostrarGramatica():
    global no_terminales, terminales, reglas
    print("No terminales:", no_terminales)
    print("Terminales:", terminales)
    print("Producciones:")
    for L, P in reglas.items():
        print(f"  {L} -> {' | '.join(P)}")

def menuGramatica():
    print(""" Submenú Gramáticas 
        - 1.- Cargar Gramatica 
        - 2.- Conteo de Reglas Recursivas 
        - 3.- Generar cadena 
        - 4.- Salir 
    """)
    opcion = input("¿Qué operación realizarás?  ").strip()
    match opcion:
        case "1":
            leerArchivo()
            mostrarGramatica()
            print("\nGramatica cargada con exito /ᐠ - ˕ -マ\n")
            seleccionOpcion()
        case "2":
            conteoReglasR() 
            seleccionOpcion()
        case "3":
            generarCadenas()
            seleccionOpcion()
        case _:
            print("Opción incorrecta\n")

def conteoReglasR():
    global reglas
    cont_Recursiones = 0
    
    for L, P in reglas.items():   
        if any(L in produccion for produccion in P):
            cont_Recursiones += 1
    print(f"El total de reglas recursivas es: {cont_Recursiones}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def generarCadenas():
    global reglas, no_terminales, terminales
    #cadenaFinal = ""
    for L, P in reglas.items(): 
        if any(L in produccion for produccion in P):
            cadenaFinal = P
            print(cadenaFinal)
    return cadenaFinal








# A U T O M A T A S : - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def leerArchivoAutomatas():
    global reglas, lado_izq, lado_der
    global Identificacion, sigma, Finales, producciones
    archivo = selArchivo()
    with open(archivo, 'r') as f:
        contenido = f.read()
    
    sigma = re.search(r'Sig\{(.*?)\}', contenido)
    Finales = re.search(r'F\{(.*?)\}', contenido)
    produccion1 = re.findall(r'\{(.*?)\}', contenido, re.DOTALL)
    producciones = produccion1[-1]
    #print(producciones)
    
    reglas = {}
    if producciones:
        for linea in producciones.split(','):
            linea = linea.strip()
            #print(linea)
            if linea:
                lado_izq, lado_der = linea.split('>')
                lado_izq = lado_izq.strip()
                lado_der = [p.strip() for p in lado_der.split('|')]
                if lado_izq in reglas:
                    reglas[lado_izq].extend(int(lado_der))
                else:
                    reglas[lado_izq] = lado_der
    #print(lado_der)
    
    if sigma:
        sigma = sigma.group(1).split(',')
    else:
        print("No hay elementos sigma en el archivo")
    
    if Finales:
        Finales = Finales.group(1).split(',')
    else:
        print("No hay Estados Finales")
    

    print(f"""Automata Cargado Con Exito:
          Sigma: {sigma}
          Estados Finales: {Finales}
          Producciones: {reglas}""")

    
def validarCadenaAutomata():
    global reglas, sigma, Finales
    
    # Verificamos si hay un autómata cargado
    if not sigma or not reglas or not Finales:
        print("No hay autómata cargado: por favor cargue un autómata")
        return False

    # Convertimos todo a enteros
    Finales = [int(e) for e in Finales]
    transiciones = {
    estado if estado == 'NULL' else int(estado): [int(t) if t != 'NULL' else t for t in trans]
    for estado, trans in reglas.items()
}
    print(f"Transiciones: {transiciones}, finales: {Finales}", "sigma:", sigma)
    estado_actual = 0  # Estado inicial siempre es 0
    cadena = input("Ingresa la cadena a validar: ").strip()
    cadena = re.sub(r'\s+', '', cadena)  # Eliminar espacios

    print(f"\nValidando cadena: {cadena}")
    print(f"Estado inicial: {estado_actual}")

    for simbolo in cadena:
        if simbolo not in sigma:
            print(f"Error: Símbolo '{simbolo}' no está en el alfabeto")
            return False
        
        idx_simbolo = sigma.index(simbolo)
        
        if estado_actual in transiciones and idx_simbolo < len(transiciones[estado_actual]):
            nuevo_estado = transiciones[estado_actual][idx_simbolo]
            print(f"Transición: {estado_actual} --'{simbolo}'--> {nuevo_estado}")
            estado_actual = nuevo_estado
        else:
            print(f"Error: No hay transición desde {estado_actual} con '{simbolo}'")
            return False

    if estado_actual in Finales:
        print(f"RESULTADO: La cadena '{cadena}' ES VÁLIDA (termina en estado {estado_actual})")
        return True
    else:
        print(f"RESULTADO: La cadena '{cadena}' NO ES VÁLIDA (termina en estado {estado_actual})")
        return False
    

def verificarAutomata():
    if not reglas:
        print("No hay automata cargado: por favor cargue un automata")
        return
    if len(lado_der) > 1:
        Identificacion = "Es un Automata Finito No Determinista"
    else:
        Identificacion = "Es un Automata Finito Determinista"
            
    print(Identificacion)

from collections import deque

def afnd_a_afd():
    global reglas, sigma, Finales

    # Función para procesar las transiciones
    def procesar_transicion(trans):
        if trans == 'NULL':
            return []
        if isinstance(trans, list):
            return [int(x) for x in trans]
        # Maneja casos como '01', '02' tratándolos como estados individuales
        return [int(trans)] if trans.isdigit() else []

    # Convertir las reglas a formato numérico
    reglas_numericas = {}
    for k, v in reglas.items():
        reglas_numericas[int(k)] = [procesar_transicion(trans) for trans in v]

    # Convertir finales a números
    Finales_numericos = [int(x) for x in Finales if x.isdigit()]

    if not reglas_numericas:
        print("Error: No hay autómata cargado.")
        return None, None, None

    # Resto de la función permanece igual hasta el procesamiento de transiciones
    estado_inicial_afd = frozenset([0])
    cola = deque([estado_inicial_afd])
    visitados = set()
    afd_transiciones = {}
    estados_finales_afd = set()

    simbolo_a_indice = {simbolo: idx for idx, simbolo in enumerate(sigma)}
    estado_vacio = frozenset()

    while cola:
        estado_actual_afd = cola.popleft()

        if estado_actual_afd in visitados:
            continue
        visitados.add(estado_actual_afd)

        transiciones_afd = {}
        for simbolo in sigma:
            idx_simbolo = simbolo_a_indice[simbolo]
            nuevo_estado = set()

            for estado in estado_actual_afd:
                if estado in reglas_numericas and idx_simbolo < len(reglas_numericas[estado]):
                    transiciones = reglas_numericas[estado][idx_simbolo]
                    if transiciones:  # Ya no necesitamos verificar 'NULL' aquí
                        nuevo_estado.update(transiciones)

            nuevo_estado_fs = frozenset(nuevo_estado) if nuevo_estado else estado_vacio
            transiciones_afd[simbolo] = nuevo_estado_fs

            if nuevo_estado_fs and nuevo_estado_fs != estado_vacio and nuevo_estado_fs not in visitados and nuevo_estado_fs not in cola:
                cola.append(nuevo_estado_fs)

        afd_transiciones[estado_actual_afd] = transiciones_afd

        if any(estado in Finales_numericos for estado in estado_actual_afd):
            estados_finales_afd.add(estado_actual_afd)

    # Asignar nombres legibles a los estados
    estado_nombres = {}
    for i, estado in enumerate(visitados):
        if estado:
            estado_nombres[estado] = f"q{'_'.join(str(s) for s in sorted(estado))}"
        else:
            estado_nombres[estado] = "∅"
    
    estado_inicial_nombre = estado_nombres[estado_inicial_afd]
    estados_finales_nombres = {estado_nombres[estado] for estado in estados_finales_afd}

    print("\n=== AFD Generado ===")
    print(f"Estado inicial: {estado_inicial_nombre}")
    print(f"Estados finales: {estados_finales_nombres}")
    print("Transiciones:")
    for estado, trans in afd_transiciones.items():
        nombre_estado = estado_nombres[estado]
        for simbolo, destino in trans.items():
            nombre_destino = estado_nombres.get(destino, "∅")
            print(f"  {nombre_estado} --{simbolo}--> {nombre_destino}")

    return afd_transiciones, estado_inicial_nombre, estados_finales_nombres, afd_transiciones, estado_inicial_afd, estados_finales_afd

from collections import deque

def minimizar_afd():
    global afd_transiciones, estado_inicial, estados_finales, sigma, adf_transiciones, estado_inicial_nombre, estados_finales_nombres
    global afd_transiciones
    # 1. Convertir estados a nombres para identificación
    todos_estados = list(afd_transiciones.keys())
    nombre_estado = {estado: f"q{i}" for i, estado in enumerate(todos_estados)}
    nombre_estado_inverso = {v: k for k, v in nombre_estado.items()}

    estados_finales_nombres = {nombre_estado[e] for e in estados_finales}
    estado_inicial_nombre = nombre_estado[estado_inicial]

    trans_nombre = {
        nombre_estado[estado]: {
            simbolo: nombre_estado.get(destino, "∅")
            for simbolo, destino in trans.items()
        } for estado, trans in afd_transiciones.items()
    }

    # 2. Inicialización
    particion = [set(estados_finales_nombres)]
    no_finales = set(trans_nombre.keys()) - set(estados_finales_nombres)
    if no_finales:
        particion.append(no_finales)

    cola = deque()
    if len(particion[0]) <= len(no_finales):
        cola.append(particion[0])
    else:
        cola.append(no_finales)

    # 3. Refinamiento
    while cola:
        grupo_actual = cola.popleft()
        for simbolo in sigma:
            estados_que_llegan = set()
            for estado, trans in trans_nombre.items():
                if simbolo in trans and trans[simbolo] in grupo_actual:
                    estados_que_llegan.add(estado)

            nuevos_grupos = []
            for grupo in particion:
                inter = grupo & estados_que_llegan
                dif = grupo - estados_que_llegan
                if inter and dif:
                    nuevos_grupos.extend([inter, dif])
                    if grupo in cola:
                        cola.remove(grupo)
                        cola.extend([inter, dif])
                    else:
                        cola.append(inter if len(inter) <= len(dif) else dif)
                else:
                    nuevos_grupos.append(grupo)
            particion = nuevos_grupos

    # 4. Construir el nuevo AFD
    mapeo = {}
    for i, grupo in enumerate(particion):
        nombre_grupo = f"Q{i}"
        for estado in grupo:
            mapeo[estado] = nombre_grupo

    afd_min = {}
    for grupo in particion:
        representante = next(iter(grupo))
        nombre_grupo = mapeo[representante]
        afd_min[nombre_grupo] = {}
        for simbolo in sigma:
            destino = trans_nombre[representante].get(simbolo, "∅")
            afd_min[nombre_grupo][simbolo] = mapeo.get(destino, "∅")

    estado_inicial_min = mapeo[estado_inicial_nombre]
    estados_finales_min = {mapeo[e] for e in estados_finales_nombres}

    print("\n=== AFD Minimizado ===")
    print(f"Estado inicial: {estado_inicial_min}")
    print(f"Estados finales: {estados_finales_min}")
    print("Transiciones:")
    for estado, trans in afd_min.items():
        for simbolo, destino in trans.items():
            print(f"  {estado} --{simbolo}--> {destino}")

    return afd_min, estado_inicial_min, estados_finales_min



# Mostrar el resultado

    
def menuAutomatas():
    print(""" Submenú Automatas
        1.- Cargar Automata 
        2.- Verificar Automata
        3.- Validar Cadena
        4.- Convertir de AFND a AFD
        5.- Minimizar AFD
        6.- Salir
    """)
    opcion = input("¿Qué operación realizarás?  ").strip()
    match opcion:
        case "1":
            leerArchivoAutomatas()
            seleccionOpcionAutomatas()
        case "2":
            verificarAutomata()
            seleccionOpcionAutomatas()
        case "3":
            validarCadenaAutomata()
            seleccionOpcionAutomatas()
        case "4":
            print(f"transiciones: {reglas}, sigma: {sigma}, finales: {Finales}")
            afnd_a_afd()
            seleccionOpcionAutomatas()
        case "5":
            print("En proceso de corrección.... -w-'")
            #minimizar_afd()
            seleccionOpcionAutomatas()
        case "6":
            menuPrincipal()
        case _:
            print("Opción incorrecta\n")

    return
#validarCadenaAutomata
if __name__ == '__main__':
    iniciarPrograma()