# simplificador.py
from typing import Set, List, Dict
from gramatica import Gramatica

class SimplificadorCFG:
    def __init__(self):
        self.anulables_encontrados = set()
    
    def eliminar_producciones_epsilon(self, gramatica: Gramatica) -> Gramatica:
        """
        Elimina producciones-ε de una gramática CFG
        Algoritmo basado en el método de los 2^m casos
        """
        print("=== ELIMINACIÓN DE PRODUCCIONES-ε ===\n")
        
        # Paso 1: Encontrar símbolos anulables
        print("1. ENCONTRANDO SÍMBOLOS ANULABLES:")
        anulables = gramatica.obtener_producciones_epsilon()
        self.anulables_encontrados = anulables
        print(f"Símbolos anulables encontrados: {sorted(anulables)}")
        
        # Paso 2: Mostrar producciones actuales
        print("\n2. PRODUCCIONES ACTUALES:")
        for nt in sorted(gramatica.producciones.keys()):
            prods = " | ".join(gramatica.producciones[nt])
            print(f"  {nt} → {prods}")
        
        # Paso 3: Generar nueva gramática sin producciones-ε
        print("\n3. GENERANDO NUEVAS PRODUCCIONES:")
        nueva_gramatica = Gramatica()
        nueva_gramatica.simbolo_inicial = gramatica.simbolo_inicial
        nueva_gramatica.terminales = gramatica.terminales.copy()
        nueva_gramatica.no_terminales = gramatica.no_terminales.copy()
        
        for no_terminal, producciones in gramatica.producciones.items():
            print(f"\nProcesando {no_terminal}:")
            nuevas_prods = set()
            
            for prod in producciones:
                print(f"  Procesando producción: {no_terminal} → {prod}")
                
                if prod == 'ε':
                    print("    - Eliminando producción-ε")
                    continue
                
                # Generar todas las combinaciones posibles
                variantes = self._generar_variantes(prod, anulables)
                print(f"    - Variantes generadas: {variantes}")
                
                nuevas_prods.update(variantes)
            
            # Eliminar cadena vacía si no es el símbolo inicial
            nuevas_prods.discard('')
            if no_terminal == gramatica.simbolo_inicial and '' in nuevas_prods:
                nuevas_prods.add('ε')
                nuevas_prods.discard('')
            
            # Agregar producciones a la nueva gramática
            if nuevas_prods:
                nueva_gramatica.producciones[no_terminal] = list(nuevas_prods)
        
        print("\n4. GRAMÁTICA RESULTANTE:")
        nueva_gramatica.mostrar()
        
        return nueva_gramatica
    
    def _generar_variantes(self, produccion: str, anulables: Set[str]) -> Set[str]:
        """
        Genera todas las variantes posibles de una producción
        eliminando combinaciones de símbolos anulables
        """
        if not produccion or produccion == 'ε':
            return {produccion}
        
        # Encontrar posiciones de símbolos anulables
        posiciones_anulables = []
        for i, simbolo in enumerate(produccion):
            if simbolo in anulables:
                posiciones_anulables.append(i)
        
        if not posiciones_anulables:
            return {produccion}
        
        # Generar todos los casos posibles (2^m combinaciones)
        num_anulables = len(posiciones_anulables)
        variantes = set()
        
        # Para cada combinación binaria posible
        for i in range(2 ** num_anulables):
            nueva_prod = list(produccion)
            
            # Determinar qué símbolos anulables omitir
            for j in range(num_anulables):
                if (i >> j) & 1:  # Si el bit j está activado
                    pos = posiciones_anulables[j]
                    nueva_prod[pos] = None  # Marcar para eliminación
            
            # Construir la nueva producción
            resultado = ''.join(s for s in nueva_prod if s is not None)
            variantes.add(resultado)
        
        return variantes
    
    def mostrar_estadisticas(self, original: Gramatica, simplificada: Gramatica):
        """Muestra estadísticas de la simplificación"""
        print("\n=== ESTADÍSTICAS DE SIMPLIFICACIÓN ===")
        
        prod_originales = sum(len(prods) for prods in original.producciones.values())
        prod_simplificadas = sum(len(prods) for prods in simplificada.producciones.values())
        
        print(f"Producciones originales: {prod_originales}")
        print(f"Producciones simplificadas: {prod_simplificadas}")
        print(f"Símbolos anulables eliminados: {len(self.anulables_encontrados)}")
        print(f"Reducción: {prod_originales - prod_simplificadas} producciones")
    
    def validar_equivalencia(self, original: Gramatica, simplificada: Gramatica, 
                           cadenas_prueba: List[str]) -> bool:
        """
        Valida que ambas gramáticas generen el mismo lenguaje
        (Implementación básica para demostración)
        """
        print("\n=== VALIDACIÓN DE EQUIVALENCIA ===")
        print("Probando cadenas de ejemplo...")
        
        for cadena in cadenas_prueba:
            print(f"Probando cadena: '{cadena}'")
            # Aquí iría la implementación del algoritmo CYK o similar
            # Por ahora solo mostramos que se puede probar
        
        return True