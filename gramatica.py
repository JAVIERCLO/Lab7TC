# gramatica.py
from typing import Dict, List, Set, Tuple
import re

class Gramatica:
    def __init__(self):
        self.producciones: Dict[str, List[str]] = {}
        self.simbolo_inicial: str = ""
        self.terminales: Set[str] = set()
        self.no_terminales: Set[str] = set()
    
    def agregar_produccion(self, izquierda: str, derecha: str):
        """Agrega una producción A -> derecha"""
        if izquierda not in self.producciones:
            self.producciones[izquierda] = []
        self.producciones[izquierda].append(derecha)
        self.no_terminales.add(izquierda)
        
        # Identificar terminales y no terminales en el lado derecho
        self._extraer_simbolos(derecha)
    
    def _extraer_simbolos(self, cadena: str):
        """Extrae terminales y no terminales de una cadena de producción"""
        for char in cadena:
            if char.isupper():
                self.no_terminales.add(char)
            elif char.islower() or char.isdigit():
                self.terminales.add(char)
            # ε se maneja como caso especial
    
    def establecer_inicial(self, simbolo: str):
        """Establece el símbolo inicial"""
        self.simbolo_inicial = simbolo
        self.no_terminales.add(simbolo)
    
    def obtener_producciones_epsilon(self) -> Set[str]:
        """Encuentra todos los símbolos que pueden generar ε"""
        anulables = set()
        
        # Paso 1: encontrar símbolos que tienen producción directa a ε
        for no_terminal, prods in self.producciones.items():
            if 'ε' in prods:
                anulables.add(no_terminal)
        
        # Paso 2: iterar hasta no encontrar más anulables
        cambio = True
        while cambio:
            cambio = False
            for no_terminal, prods in self.producciones.items():
                if no_terminal not in anulables:
                    for prod in prods:
                        # Si todos los símbolos de la producción son anulables
                        if self._todos_anulables(prod, anulables):
                            anulables.add(no_terminal)
                            cambio = True
                            break
        
        return anulables
    
    def _todos_anulables(self, produccion: str, anulables: Set[str]) -> bool:
        """Verifica si todos los símbolos en una producción son anulables"""
        if produccion == 'ε':
            return True
        
        for simbolo in produccion:
            if simbolo in self.terminales:
                return False
            elif simbolo in self.no_terminales and simbolo not in anulables:
                return False
        
        return True
    
    def mostrar(self):
        """Muestra la gramática en formato legible"""
        print(f"Símbolo inicial: {self.simbolo_inicial}")
        print("Producciones:")
        for no_terminal in sorted(self.producciones.keys()):
            prods = " | ".join(self.producciones[no_terminal])
            print(f"  {no_terminal} → {prods}")
        print(f"Terminales: {sorted(self.terminales)}")
        print(f"No terminales: {sorted(self.no_terminales)}")
    
    def copiar(self):
        """Crea una copia de la gramática"""
        nueva = Gramatica()
        nueva.simbolo_inicial = self.simbolo_inicial
        nueva.terminales = self.terminales.copy()
        nueva.no_terminales = self.no_terminales.copy()
        
        for nt, prods in self.producciones.items():
            nueva.producciones[nt] = prods.copy()
        
        return nueva