# Radar de videojuegos

Web estática que muestra lanzamientos, críticas y anuncios de videojuegos en español, actualizada automáticamente a diario, semana, mes y año. Desarrollada en **HTML5, CSS3 y JavaScript**, sin backend ni base de datos: los datos viven en un único archivo JSON.

## Arquitectura

```
4 tareas programadas (investigación + puntuación)
        │  llaman a
scripts/anadir_eventos.py   (valida, deduplica, fusiona)
        │  escribe
data/eventos.json           (una única fuente de verdad)
        │  lee con fetch()
index.html + assets/js/main.js   (agrupa por diario/semanal/mensual/anual)
```

Las vistas (hoy, esta semana, este mes, este año) no son cuatro fuentes de datos distintas: son el mismo archivo filtrado por el campo `cadencia` de cada evento. Añadir una vista nueva, o cambiar cómo se ve una tarjeta, no exige tocar cómo se generan los datos.

## Formato de los datos

Ver `data/README.md`. Cada evento lleva juego, fecha, periodo, tramo (confirmado con puntuación / radar temprano sin puntuación), etiqueta de confianza de la fuente, enlaces y notas (polémica, divergencia).

## Cómo se alimenta

Cuatro tareas programadas (diaria entre semana, semanal, mensual, anual) investigan con búsqueda web, verifican cada dato abriendo la página de origen y escriben los eventos nuevos con `scripts/anadir_eventos.py`, que rechaza cualquier objeto mal formado y evita duplicados por `id`. El resultado se sube a este repositorio, que GitHub Pages sirve sin pasos intermedios.

## Monetización

Hueco reservado en la portada para patrocinio de estudios indie (`<div class="patrocinado">` en `index.html`), pensado para encajar con los servicios de auditoría y campaña de Steam que ya ofrece Kizary.

## Desarrollo

```
python3 -m http.server      # servir en local
python3 scripts/anadir_eventos.py nuevos.json   # añadir eventos a mano
```

---
Rafael Izquierdo · Kizary
