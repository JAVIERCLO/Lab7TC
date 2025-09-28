# validador.py
import re
from gramatica import Gramatica

class ValidadorGramatica:
    def __init__(self):
        # Regex para validar que una línea está bien escrita
        # Ejemplo: S → 0A0 | 1B1 | BB
        self.patron_produccion = re.compile(r'^[A-Z]\s*→\s*([A-Za-z0-9ε|\\()\[\]{}^$+.?*_\s]+(\s*\|\s*[A-Za-z0-9ε|\\()\[\]{}^$+.?*_\s]*)*)\s*$')
        
        # Regex para validar producciones individuales
        self.patron_lado_derecho = re.compile(r'^[A-Za-z0-9ε|\\()\[\]{}^$+.?*_\s]*$')
    
    def validar_archivo(self, nombre_archivo: str) -> bool:
        """
        Valida que un archivo de gramática esté bien escrito
        usando expresiones regulares
        """
        print(f"=== VALIDANDO ARCHIVO: {nombre_archivo} ===")
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            
            errores_encontrados = []
            lineas_validas = 0
            
            for num_linea, linea in enumerate(lineas, 1):
                linea = linea.strip()
                
                # Ignorar líneas vacías y comentarios
                if not linea or linea.startswith('#'):
                    continue
                
                # Validar formato de la línea
                if self.patron_produccion.match(linea):
                    lineas_validas += 1
                    print(f"✓ Línea {num_linea}: {linea}")
                    
                    # Validación adicional del contenido
                    if not self._validar_contenido_linea(linea):
                        errores_encontrados.append(f"Línea {num_linea}: contenido inválido - {linea}")
                else:
                    errores_encontrados.append(f"Línea {num_linea}: formato inválido - {linea}")
                    print(f"✗ Línea {num_linea}: {linea}")
            
            # Mostrar resultados
            print(f"\nRESULTADOS DE VALIDACIÓN:")
            print(f"Líneas válidas: {lineas_validas}")
            print(f"Errores encontrados: {len(errores_encontrados)}")
            
            if errores_encontrados:
                print("\nERRORES DETECTADOS:")
                for error in errores_encontrados:
                    print(f"  - {error}")
                return False
            else:
                print("✓ Archivo válido - todas las producciones están bien escritas")
                return True
                
        except FileNotFoundError:
            print(f"ERROR: No se encontró el archivo '{nombre_archivo}'")
            return False
        except Exception as e:
            print(f"ERROR al leer archivo: {e}")
            return False
    
    def _validar_contenido_linea(self, linea: str) -> bool:
        """Validación adicional del contenido de una línea"""
        # Separar lado izquierdo y derecho
        if '→' not in linea:
            return False
        
        partes = linea.split('→', 1)
        if len(partes) != 2:
            return False
        
        lado_izquierdo = partes[0].strip()
        lado_derecho = partes[1].strip()
        
        # Lado izquierdo debe ser un solo no terminal
        if not re.match(r'^[A-Z]$', lado_izquierdo):
            return False
        
        # Validar cada producción del lado derecho
        producciones = lado_derecho.split('|')
        for prod in producciones:
            prod = prod.strip()
            if not self.patron_lado_derecho.match(prod):
                return False
        
        return True
    
    def cargar_gramatica_desde_archivo(self, nombre_archivo: str) -> Gramatica:
        """Carga una gramática desde un archivo validado"""
        if not self.validar_archivo(nombre_archivo):
            raise ValueError(f"Archivo {nombre_archivo} no es válido")
        
        gramatica = Gramatica()
        primer_no_terminal = None
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            
            for linea in lineas:
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue
                
                # Parsear la línea
                partes = linea.split('→', 1)
                no_terminal = partes[0].strip()
                producciones_str = partes[1].strip()
                
                # Establecer símbolo inicial (primer no terminal encontrado)
                if primer_no_terminal is None:
                    primer_no_terminal = no_terminal
                    gramatica.establecer_inicial(no_terminal)
                
                # Separar producciones por |
                producciones = [p.strip() for p in producciones_str.split('|')]
                
                # Agregar cada producción
                for prod in producciones:
                    gramatica.agregar_produccion(no_terminal, prod)
            
            print(f"✓ Gramática cargada exitosamente desde {nombre_archivo}")
            return gramatica
            
        except Exception as e:
            print(f"ERROR al cargar gramática: {e}")
            raise
    
    def generar_regex_ejemplo(self) -> str:
        """
        Genera un ejemplo de regex que acepta producciones para gramáticas
        """
        regex = r"[A-Z](\s)*→(\s)*([A-Za-z0-9ε]|(\s)*|(\|))*"
        
        print("REGEX PARA VALIDAR PRODUCCIONES:")
        print(f"Patrón: {regex}")
        print("\nExplicación:")
        print("- [A-Z]: Símbolo no terminal (mayúscula)")
        print("- (\\s)*: Espacios opcionales")
        print("- →: Símbolo de producción")
        print("- ([A-Za-z0-9ε]|(\\s)*(\\|))*: Lado derecho con terminales, no terminales, ε y |")
        
        return regex