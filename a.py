import re, random
from Menu import menuPrincipal, despedida
reglas = {}
no_terminales = []
terminales = []

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
    global reglas, no_terminales, terminales 
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
    global Identificacion, sigma, Finales
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
                    reglas[lado_izq].extend(lado_der)
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

def verificarAutomata():
    if not reglas:
        print("No hay automata cargado: por favor cargue un automata")
        return
    if len(lado_der) > 1:
        Identificacion = "Es un Automata Finito No Determinista"
    else:
        Identificacion = "Es un Automata Finito Determinista"
            
    print(Identificacion)

def validarCadenaAutomata():
    if not reglas: 
        print("No hay automata cargado: por favor cargue un automata")
        return
    CadenaEvaluar = input("Ingrese la cadena a evaluar: ")
    for i in CadenaEvaluar:
        if i not in sigma:
            validacion = "La cadena no es valida"
        else:
            validacion = "Cadena Valida"
    print(validacion)
    return


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
            return
        case "5":
            return
        case "6":
            menuPrincipal()
        case _:
            print("Opción incorrecta\n")

    return
#validarCadenaAutomata
if __name__ == '__main__':
    iniciarPrograma()