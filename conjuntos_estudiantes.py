from dataclasses import dataclass, field
from typing import Optional

@dataclass
class NodoEstudiante:
    """Nodo del árbol BST que almacena un estudiante."""
    matricula: str
    nombre: str
    promedio: float
    izquierda: Optional["NodoEstudiante"] = field(default=None, repr=False)
    derecha: Optional["NodoEstudiante"] = field(default=None, repr=False)


class ArbolBST:
    """
    Árbol Binario de Búsqueda de estudiantes.
    Permite insertar y buscar estudiantes en O(log n) promedio.
    """

    def __init__(self):
        self.raiz: Optional[NodoEstudiante] = None

    def insertar(self, matricula: str, nombre: str, promedio: float) -> None:
        """Inserta un estudiante en el árbol."""
        nuevo = NodoEstudiante(matricula=matricula, nombre=nombre, promedio=promedio)
        if self.raiz is None:
            self.raiz = nuevo
        else:
            self._insertar_recursivo(self.raiz, nuevo)

    def _insertar_recursivo(self, nodo: NodoEstudiante, nuevo: NodoEstudiante) -> None:
        if nuevo.matricula < nodo.matricula:
            if nodo.izquierda is None:
                nodo.izquierda = nuevo
            else:
                self._insertar_recursivo(nodo.izquierda, nuevo)
        elif nuevo.matricula > nodo.matricula:
            if nodo.derecha is None:
                nodo.derecha = nuevo
            else:
                self._insertar_recursivo(nodo.derecha, nuevo)

    def buscar(self, matricula: str) -> Optional[NodoEstudiante]:
        """Busca un estudiante por matrícula. Retorna el nodo o None."""
        return self._buscar_recursivo(self.raiz, matricula)

    def _buscar_recursivo(self, nodo: Optional[NodoEstudiante], matricula: str) -> Optional[NodoEstudiante]:
        if nodo is None or nodo.matricula == matricula:
            return nodo
        if matricula < nodo.matricula:
            return self._buscar_recursivo(nodo.izquierda, matricula)
        return self._buscar_recursivo(nodo.derecha, matricula)

    def recorrido_inorden(self) -> list[NodoEstudiante]:
        """Recorre el árbol en inorden (resultado ordenado por matrícula)."""
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo: Optional[NodoEstudiante], resultado: list) -> None:
        if nodo:
            self._inorden(nodo.izquierda, resultado)
            resultado.append(nodo)
            self._inorden(nodo.derecha, resultado)

class SistemaAcademico:
    """
    Sistema de gestión académica que combina:
      - Árbol BST: búsqueda eficiente de estudiantes
      - Diccionario: mapeo materia → conjunto de matrículas
      - Conjuntos (set): operaciones de Unión, Intersección y Diferencia
    """

    def __init__(self):
        self.arbol_estudiantes = ArbolBST()
        self.materias: dict[str, set[str]] = {}
        self._catalogo: dict[str, dict] = {}

    def registrar_estudiante(self, matricula: str, nombre: str, promedio: float) -> None:
        """Registra un estudiante en el catálogo y el BST."""
        if matricula in self._catalogo:
            print(f"  [AVISO] Matrícula {matricula} ya existe en el sistema.")
            return
        self.arbol_estudiantes.insertar(matricula, nombre, promedio)
        self._catalogo[matricula] = {"nombre": nombre, "promedio": promedio}
        print(f"  ✔ Estudiante registrado: {nombre} ({matricula})")

    def crear_materia(self, nombre_materia: str) -> None:
        """Crea una nueva materia en el sistema."""
        if nombre_materia not in self.materias:
            self.materias[nombre_materia] = set()
            print(f"  ✔ Materia creada: {nombre_materia}")

    def inscribir(self, matricula: str, nombre_materia: str) -> None:
        """Inscribe un estudiante en una materia."""
        if matricula not in self._catalogo:
            print(f"  [ERROR] Matrícula {matricula} no encontrada.")
            return
        if nombre_materia not in self.materias:
            self.crear_materia(nombre_materia)
        self.materias[nombre_materia].add(matricula)

    def buscar_estudiante(self, matricula: str) -> None:
        """Busca un estudiante usando el árbol BST."""
        nodo = self.arbol_estudiantes.buscar(matricula)
        if nodo:
            print(f"\n   Estudiante encontrado:")
            print(f"     Matrícula : {nodo.matricula}")
            print(f"     Nombre    : {nodo.nombre}")
            print(f"     Promedio  : {nodo.promedio}")
        else:
            print(f"\n   Estudiante con matrícula {matricula} no encontrado.")

    def union(self, materia_a: str, materia_b: str) -> set[str]:
        """
        UNIÓN (A ∪ B):
        Todos los estudiantes inscritos en A, en B, o en ambas.
        """
        conjunto_a = self.materias.get(materia_a, set())
        conjunto_b = self.materias.get(materia_b, set())
        return conjunto_a | conjunto_b        

    def interseccion(self, materia_a: str, materia_b: str) -> set[str]:
        """
        INTERSECCIÓN (A ∩ B):
        Estudiantes inscritos en A Y en B al mismo tiempo.
        """
        conjunto_a = self.materias.get(materia_a, set())
        conjunto_b = self.materias.get(materia_b, set())
        return conjunto_a & conjunto_b       

    def diferencia(self, materia_a: str, materia_b: str) -> set[str]:
        """
        DIFERENCIA (A − B):
        Estudiantes inscritos en A pero NO en B.
        """
        conjunto_a = self.materias.get(materia_a, set())
        conjunto_b = self.materias.get(materia_b, set())
        return conjunto_a - conjunto_b     

    def diferencia_simetrica(self, materia_a: str, materia_b: str) -> set[str]:
        """
        DIFERENCIA SIMÉTRICA (A △ B):
        Estudiantes que están en A o B, pero NO en ambas.
        """
        conjunto_a = self.materias.get(materia_a, set())
        conjunto_b = self.materias.get(materia_b, set())
        return conjunto_a ^ conjunto_b        

    def nombres_de(self, matriculas: set[str]) -> list[str]:
        """Convierte un conjunto de matrículas a nombres legibles."""
        return sorted(
            f"{m} - {self._catalogo[m]['nombre']}"
            for m in matriculas
            if m in self._catalogo
        )

    def mostrar_materia(self, nombre_materia: str) -> None:
        """Muestra todos los inscritos en una materia."""
        inscritos = self.materias.get(nombre_materia, set())
        print(f"\n   {nombre_materia} ({len(inscritos)} estudiantes):")
        for linea in self.nombres_de(inscritos):
            print(f"     • {linea}")

    def mostrar_todos_ordenados(self) -> None:
        """Muestra todos los estudiantes ordenados por matrícula (inorden BST)."""
        nodos = self.arbol_estudiantes.recorrido_inorden()
        print(f"\n   Directorio completo de estudiantes ({len(nodos)} registros):")
        for n in nodos:
            print(f"     {n.matricula} | {n.nombre:<25} | Prom: {n.promedio:.1f}")

def separador(titulo: str = "") -> None:
    linea = "─" * 60
    if titulo:
        print(f"\n{'─'*20} {titulo} {'─'*20}")
    else:
        print(linea)


def ejecutar_pruebas():
    print("=" * 60)
    print("  SISTEMA DE GESTIÓN ACADÉMICA — DEMO")
    print("  Operaciones con Conjuntos + BST + Diccionarios")
    print("=" * 60)

    sistema = SistemaAcademico()
    separador("PRUEBA 1: Registro de Estudiantes")
    datos = [
        ("A001", "Ana García",       9.2),
        ("A002", "Bruno López",      7.5),
        ("A003", "Carla Méndez",     8.8),
        ("A004", "Diego Ruiz",       6.9),
        ("A005", "Elena Torres",     9.5),
        ("A006", "Felipe Soto",      7.1),
        ("A007", "Gabriela Vega",    8.3),
        ("A008", "Héctor Mora",      5.8),
        ("A009", "Iris Castro",      9.0),
        ("A010", "Jorge Peña",       7.7),
    ]
    for mat, nom, prom in datos:
        sistema.registrar_estudiante(mat, nom, prom)

    print("\n  ─ Intento de matrícula duplicada:")
    sistema.registrar_estudiante("A001", "Otra Persona", 8.0)   # debe avisar

    separador("PRUEBA 2: Inscripción en Materias")
    for mat in ["A001", "A002", "A003", "A004", "A005", "A006"]:
        sistema.inscribir(mat, "Matemáticas Discretas")

    for mat in ["A003", "A004", "A005", "A007", "A008", "A009"]:
        sistema.inscribir(mat, "Estructuras de Datos")

    for mat in ["A001", "A005", "A007", "A009", "A010"]:
        sistema.inscribir(mat, "Bases de Datos")

    sistema.mostrar_materia("Matemáticas Discretas")
    sistema.mostrar_materia("Estructuras de Datos")
    sistema.mostrar_materia("Bases de Datos")

    separador("PRUEBA 3: Búsqueda con Árbol BST")
    sistema.buscar_estudiante("A005")
    sistema.buscar_estudiante("A999")   
    separador("PRUEBA 4: Operaciones con Conjuntos")

    md = "Matemáticas Discretas"
    ed = "Estructuras de Datos"
    bd = "Bases de Datos"

    union_md_ed = sistema.union(md, ed)
    print(f"\n   UNIÓN  ({md}) ∪ ({ed}):")
    print(f"     Total de estudiantes únicos: {len(union_md_ed)}")
    for linea in sistema.nombres_de(union_md_ed):
        print(f"     • {linea}")

    inter_md_ed = sistema.interseccion(md, ed)
    print(f"\n   INTERSECCIÓN  ({md}) ∩ ({ed}):")
    print(f"     Cursan AMBAS materias: {len(inter_md_ed)}")
    for linea in sistema.nombres_de(inter_md_ed):
        print(f"     • {linea}")

    dif_md_menos_ed = sistema.diferencia(md, ed)
    print(f"\n   DIFERENCIA  ({md}) − ({ed}):")
    print(f"     Solo en Matemáticas: {len(dif_md_menos_ed)}")
    for linea in sistema.nombres_de(dif_md_menos_ed):
        print(f"     • {linea}")

    dif_ed_menos_md = sistema.diferencia(ed, md)
    print(f"\n   DIFERENCIA  ({ed}) − ({md}):")
    print(f"     Solo en Estructuras: {len(dif_ed_menos_md)}")
    for linea in sistema.nombres_de(dif_ed_menos_md):
        print(f"     • {linea}")

    dif_sim = sistema.diferencia_simetrica(md, ed)
    print(f"\n   DIFERENCIA SIMÉTRICA  ({md}) △ ({ed}):")
    print(f"     En una u otra, pero no en ambas: {len(dif_sim)}")
    for linea in sistema.nombres_de(dif_sim):
        print(f"     • {linea}")

    triple = (sistema.materias[md] & sistema.materias[ed] & sistema.materias[bd])
    print(f"\n   INTERSECCIÓN TRIPLE  (MD ∩ ED ∩ BD):")
    print(f"     Cursando las 3 materias: {len(triple)}")
    for linea in sistema.nombres_de(triple):
        print(f"     • {linea}")

    separador("PRUEBA 5: Directorio Ordenado (BST Inorden)")
    sistema.mostrar_todos_ordenados()

    separador("PRUEBA 6: Verificación de Propiedades")
    A = sistema.materias[md]
    B = sistema.materias[ed]

    # Ley de identidad
    assert A | set() == A,              "Fallo: identidad unión"
    assert A & A == A,                  "Fallo: idempotencia intersección"
    assert A | B == B | A,              "Fallo: conmutatividad unión"
    assert A & B == B & A,              "Fallo: conmutatividad intersección"
    universo = set(sistema._catalogo.keys())
    comp_A = universo - A
    comp_B = universo - B
    assert (universo - (A | B)) == (comp_A & comp_B), "Fallo: De Morgan"
    card_union = len(A | B)
    card_formula = len(A) + len(B) - len(A & B)
    assert card_union == card_formula,  "Fallo: principio de inclusión-exclusión"

    print("\n   Todas las propiedades matemáticas verificadas:")
    print(f"     |A| = {len(A)}, |B| = {len(B)}")
    print(f"     |A ∩ B| = {len(A & B)}")
    print(f"     |A ∪ B| = {card_union}  (fórmula: {len(A)}+{len(B)}-{len(A&B)} = {card_formula})")
    print("     ✔ Idempotencia, Conmutatividad, De Morgan ✔")

    separador()
    print("  Demo completada exitosamente.\n")


if __name__ == "__main__":
    ejecutar_pruebas()
