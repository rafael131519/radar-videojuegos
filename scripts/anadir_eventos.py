#!/usr/bin/env python3
"""
Añade eventos nuevos a data/eventos.json sin duplicar y sin tocar los que ya había.

Uso: python3 scripts/anadir_eventos.py nuevos.json
  - nuevos.json: lista de objetos evento (ver data/README.md para el formato).

No se conecta a ninguna fuente externa: solo valida y fusiona. La investigación
(búsqueda web, lectura de páginas, puntuación) la hace la tarea programada antes
de llamar a este script.
"""
import json
import sys
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EVENTOS = RAIZ / "data" / "eventos.json"

CADENCIAS = {"diario", "semanal", "mensual", "anual"}
TRAMOS = {"A", "B"}
CONFIANZAS = {"confirmado oficial", "fiable", "rumor de comunidad"}
FECHA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validar(evento, indice):
    errores = []
    for campo in ("id", "fecha", "cadencia", "tramo", "juego", "resumen", "confianza", "fuentes"):
        if campo not in evento:
            errores.append(f"evento[{indice}]: falta '{campo}'")
    if errores:
        return errores
    if not FECHA_RE.match(evento["fecha"]):
        errores.append(f"evento[{indice}]: fecha '{evento['fecha']}' no es AAAA-MM-DD")
    if evento["cadencia"] not in CADENCIAS:
        errores.append(f"evento[{indice}]: cadencia '{evento['cadencia']}' inválida")
    if evento["tramo"] not in TRAMOS:
        errores.append(f"evento[{indice}]: tramo '{evento['tramo']}' inválido (debe ser A o B)")
    if evento["tramo"] == "A" and not isinstance(evento.get("puntuacion"), (int, float)):
        errores.append(f"evento[{indice}]: tramo A sin 'puntuacion' numérica")
    if evento["tramo"] == "B" and evento.get("puntuacion") not in (None,):
        errores.append(f"evento[{indice}]: tramo B debe llevar puntuacion null")
    if evento["confianza"] not in CONFIANZAS:
        errores.append(f"evento[{indice}]: confianza '{evento['confianza']}' inválida")
    if not isinstance(evento["fuentes"], list) or not evento["fuentes"]:
        errores.append(f"evento[{indice}]: 'fuentes' debe ser una lista no vacía")
    evento.setdefault("notas", [])
    return errores


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 scripts/anadir_eventos.py nuevos.json", file=sys.stderr)
        sys.exit(1)

    nuevos_path = Path(sys.argv[1])
    nuevos = json.loads(nuevos_path.read_text(encoding="utf-8"))
    if not isinstance(nuevos, list):
        print("El archivo de entrada debe ser una lista de eventos.", file=sys.stderr)
        sys.exit(1)

    existentes = json.loads(EVENTOS.read_text(encoding="utf-8")) if EVENTOS.exists() else []
    ids_existentes = {e["id"] for e in existentes}

    errores_totales = []
    anadidos = 0
    for i, evento in enumerate(nuevos):
        errores = validar(evento, i)
        if errores:
            errores_totales.extend(errores)
            continue
        if evento["id"] in ids_existentes:
            continue  # ya estaba, se ignora en silencio (deduplicado)
        existentes.append(evento)
        ids_existentes.add(evento["id"])
        anadidos += 1

    if errores_totales:
        print("Eventos rechazados por formato:", file=sys.stderr)
        for e in errores_totales:
            print(f"  - {e}", file=sys.stderr)

    existentes.sort(key=lambda e: e["fecha"], reverse=True)
    EVENTOS.write_text(json.dumps(existentes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Añadidos: {anadidos}. Rechazados: {len(errores_totales)}. Total en el archivo: {len(existentes)}.")


if __name__ == "__main__":
    main()
