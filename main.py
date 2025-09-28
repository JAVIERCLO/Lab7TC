# Univeridad del Valle de Guatemala
# Laboratorio 7 - Teoría de la Computación
# Genser Catalan -- Javier Chávez

import os
from gramatica import Gramatica
from simplificador import SimplificadorCFG
from validador import ValidadorGramatica

def crear_archivos_ejemplo():
    archivos = {
        'gramatica1.txt': [
            '# Gramática 1 del ejercicio',
            'S → 0A0 | 1B1 | BB',
            'A → C',
            'B → S | A', 
            'C → S | ε'
        ],
        'gramatica2.txt': [
            '# Gramática 2 del ejercicio',
            'S → aAa | bBb | ε',
            'A → C | a',
            'B → C | b',
            'C → CDE | ε',
            'D → A | B | ab'
        ],
        'gramatica3.txt': [
            '# Gramática 3 del ejercicio',
            'S → ASA | aB',
            'A → B | S',
            'B → b | ε'
        ]
    }
    
    for nombre, contenido in archivos.items():
        if not os.path.exists(nombre):
            with open(nombre, 'w', encoding='utf-8') as f:
                f.write('\n'.join(contenido))
            print(f"✓ Archivo '{nombre}' creado")

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("SIMPLIFICADOR DE GRAMÁTICAS CFG")
    print("Eliminación de Producciones-ε")
    print("="*60)
    print("1. Procesar Gramática 1")
    print("2. Procesar Gramática 2") 
    print("3. Procesar Gramática 3")
    print("0. Salir")
    print("-"*60)
    print("NOTA: Cada opción incluye validación automática con regex")

def procesar_gramatica(archivo: str):
    """Procesa una gramática específica"""
    print(f"\n{'='*80}")
    print(f"PROCESANDO: {archivo}")
    print(f"{'='*80}")
    
    try:
        # Paso 1: Validar archivo
        validador = ValidadorGramatica()
        print("\n" + "="*50)
        print("PASO 1: VALIDACIÓN CON REGEX")
        print("="*50)
        
        if not validador.validar_archivo(archivo):
            print("❌ Archivo inválido. No se puede continuar.")
            return False
        
        # Paso 2: Cargar gramática
        print("\n" + "="*50)
        print("PASO 2: CARGA DE GRAMÁTICA")
        print("="*50)
        
        gramatica_original = validador.cargar_gramatica_desde_archivo(archivo)
        print("\nGRAMÁTICA ORIGINAL:")
        gramatica_original.mostrar()
        
        # Paso 3: Simplificar
        print("\n" + "="*50)
        print("PASO 3: SIMPLIFICACIÓN")
        print("="*50)
        
        simplificador = SimplificadorCFG()
        gramatica_simplificada = simplificador.eliminar_producciones_epsilon(gramatica_original)
        
        # Paso 4: Mostrar resultados
        print("\n" + "="*50)
        print("PASO 4: RESULTADOS")
        print("="*50)
        
        simplificador.mostrar_estadisticas(gramatica_original, gramatica_simplificada)
        
        # Paso 5: Guardar resultado (opcional)
        nombre_salida = archivo.replace('.txt', '_sin_epsilon.txt')
        guardar_resultado(gramatica_simplificada, nombre_salida)
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR al procesar {archivo}: {e}")
        return False

def guardar_resultado(gramatica: Gramatica, nombre_archivo: str):
    """Guarda la gramática simplificada en un archivo"""
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(f"# Gramática simplificada (sin producciones-ε)\n")
            f.write(f"# Símbolo inicial: {gramatica.simbolo_inicial}\n\n")
            
            for no_terminal in sorted(gramatica.producciones.keys()):
                producciones = " | ".join(gramatica.producciones[no_terminal])
                f.write(f"{no_terminal} → {producciones}\n")
        
        print(f"✓ Resultado guardado en: {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error al guardar resultado: {e}")

def procesar_todas_las_gramaticas():
    """Procesa todas las gramáticas del ejercicio"""
    archivos = ['gramatica1.txt', 'gramatica2.txt', 'gramatica3.txt']
    resultados = []
    
    for archivo in archivos:
        if os.path.exists(archivo):
            exito = procesar_gramatica(archivo)
            resultados.append((archivo, exito))
        else:
            print(f"❌ Archivo {archivo} no encontrado")
            resultados.append((archivo, False))
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE PROCESAMIENTO")
    print("="*80)
    
    exitosos = sum(1 for _, exito in resultados if exito)
    total = len(resultados)
    
    for archivo, exito in resultados:
        estado = "✓ EXITOSO" if exito else "❌ FALLÓ"
        print(f"{archivo:20} - {estado}")
    
    print(f"\nTotal procesadas: {exitosos}/{total}")

def main():
    """Función principal"""
    print("=== PROGRAMA CFG - TEORÍA DE LA COMPUTACIÓN ===")
    
    # Crear archivos de ejemplo si no existen
    crear_archivos_ejemplo()
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSeleccione una opción (0-3): ").strip()
            
            if opcion == '0':
                print("¡Hasta luego!")
                break
                
            elif opcion == '1':
                procesar_gramatica('gramatica1.txt')
                
            elif opcion == '2':
                procesar_gramatica('gramatica2.txt')
                
            elif opcion == '3':
                procesar_gramatica('gramatica3.txt')
                
            else:
                print("❌ Opción inválida")
                
            input("\nPresione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()