# Contexto maestro del proyecto

## Propósito

Este repositorio es la memoria operativa compartida para trabajos de ingeniería
eléctrica y proyectos de subestaciones. Debe permitir que distintos asistentes,
computadores y sesiones continúen el trabajo con las mismas reglas verificables.

## Fuentes obligatorias

El orden mínimo de lectura es:

1. `AGENTS.md`: reglas comunes y protocolo de trabajo.
2. `README.md`: estructura, flujo y comandos del repositorio.
3. `agents/<rol>/prompt.md`: comportamiento del especialista aplicable.
4. `agents/<rol>/criterios_tecnicos.md` y checklists disponibles.
5. `knowledge_base/reglas_generales/`: criterios reutilizables y trazables.
6. `projects/<PROYECTO>/ficha_proyecto.yaml`: contexto exclusivo del proyecto.
7. Documentos originales, extracciones, cálculos y revisiones del proyecto.

## Principios permanentes registrados

- Actuar con criterio de un especialista con 25 años de experiencia.
- Mantener trazabilidad documental en toda afirmación técnica.
- No inventar datos ni completar vacíos como si fueran hechos.
- Clasificar información como `CONFIRMADO`, `RECALCULADO`, `INFERIDO`,
  `PENDIENTE` o `INCONSISTENTE`.
- Recalcular y verificar; no limitarse a copiar resultados.
- No mezclar antecedentes entre proyectos.
- Leer primero versiones compactas y acudir al original para comprobaciones
  específicas de página o lámina.
- Entregar conclusiones breves, claras, fundamentadas y accionables.

## Registro de nuevas instrucciones

Cuando el usuario indique que una preferencia o regla debe aplicarse en futuras
sesiones, el agente debe:

1. Confirmar si es global, propia de un rol o exclusiva de un proyecto.
2. Escribirla en el archivo de menor alcance que corresponda.
3. Añadir referencias desde `AGENTS.md` o desde este documento cuando sea
   necesario para que resulte descubrible.
4. Evitar guardar secretos, contraseñas, tokens o datos personales innecesarios.
5. Crear commit y push solamente cuando el usuario lo autorice.

## Límite de la memoria

El repositorio no contiene automáticamente el historial de conversaciones de
Codex o Claude. Solo son compartidas las instrucciones y decisiones que hayan
sido escritas aquí y subidas a Git. Las conversaciones antiguas que aún no estén
documentadas deben incorporarse mediante un resumen aportado por el usuario o
una exportación disponible para revisión.
