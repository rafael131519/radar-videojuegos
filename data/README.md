# Formato de `eventos.json`

Cada objeto del array es un evento. Las 4 tareas programadas (diaria, semanal,
mensual, anual) añaden objetos a este archivo; nunca lo sobrescriben entero.

```json
{
  "id": "2026-11-18-silent-hill-f-opencritic",
  "fecha": "2026-11-18",
  "cadencia": "diario",
  "tramo": "A",
  "juego": "Nombre del juego",
  "resumen": "Qué ha pasado, en una frase, sin lenguaje de anuncio.",
  "puntuacion": 87,
  "confianza": "confirmado oficial",
  "fuentes": [
    { "texto": "OpenCritic", "url": "https://..." }
  ],
  "notas": []
}
```

- `cadencia`: `"diario"` | `"semanal"` | `"mensual"` | `"anual"`.
- `tramo`: `"A"` (confirmado con datos) o `"B"` (radar temprano). En B, `puntuacion` es `null`.
- `confianza`: `"confirmado oficial"` | `"fiable"` | `"rumor de comunidad"`.
- `notas`: lista, puede contener `"polemica"`, `"divergencia"`, o ir vacía.
- `id`: fecha + juego en slug + fuente principal, para deduplicar. Si un `id` ya existe en el archivo, no se vuelve a añadir.
