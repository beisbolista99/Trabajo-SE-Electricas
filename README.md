# Subestaciones Agentes

Repositorio base para revision tecnica trazable de documentacion de subestaciones AT/MT.

El objetivo es apoyar analisis de planos, memorias de calculo, especificaciones, HCTG, catalogos y listados de materiales sin mezclar antecedentes entre proyectos.

## Regla principal

Cada subestacion vive en su propia carpeta dentro de `projects/`. Ningun dato de un proyecto debe reutilizarse en otro salvo que exista una indicacion expresa y trazable.

Toda afirmacion tecnica debe marcarse como:

- `CONFIRMADO`: aparece expresamente en un documento.
- `RECALCULADO`: se obtuvo matematicamente desde datos visibles.
- `INFERIDO`: es razonable, pero no aparece expresamente.
- `PENDIENTE`: requiere validar con documento o proyectista.
- `INCONSISTENTE`: existe contradiccion interna o documental.

## Flujo de trabajo

1. Crear o seleccionar proyecto.
2. Copiar originales en `00_entrada/`.
3. Registrar metadatos documentales.
4. Verificar coherencia entre nombre de archivo y contenido.
5. Extraer texto, tablas e indice tecnico.
6. Generar documento compacto y reporte de compresion.
7. Leer primero el compacto.
8. Volver al PDF original solo para paginas especificas.
9. Reconstruir topologia de canalizaciones.
10. Calcular areas, matriz de paso, ocupaciones y observaciones.

## Crear una nueva subestacion

```powershell
python scripts/crear_proyecto.py --nombre PENDIENTE_DE_VALIDAR --subestacion PENDIENTE_DE_VALIDAR
```

El script crea una carpeta independiente bajo `projects/`, copia la estructura del template y deja una `ficha_proyecto.yaml` inicial con campos pendientes.

## Cargar planos, memorias y catalogos

Copie los archivos originales en la carpeta que corresponda:

- Planos: `projects/<PROYECTO>/00_entrada/planos/`
- Memorias: `projects/<PROYECTO>/00_entrada/memorias_calculo/`
- Especificaciones: `projects/<PROYECTO>/00_entrada/especificaciones_tecnicas/`
- HCTG: `projects/<PROYECTO>/00_entrada/hctg/`
- Catalogos: `projects/<PROYECTO>/00_entrada/catalogos/`

Luego registre los documentos:

```powershell
python scripts/registrar_documentos.py --project projects/<PROYECTO>
```

## Preprocesar una memoria PDF

```powershell
python scripts/preparar_pdf.py --pdf ruta/al/documento.pdf --project projects/<PROYECTO> --codigo CODIGO_PENDIENTE
python scripts/extraer_texto_pdf.py --pdf projects/<PROYECTO>/02_extracciones/documentos_compactos/CODIGO_PENDIENTE/original.pdf --output projects/<PROYECTO>/02_extracciones/documentos_compactos/CODIGO_PENDIENTE/texto_completo_por_pagina.md
python scripts/generar_indice_tecnico.py --text projects/<PROYECTO>/02_extracciones/documentos_compactos/CODIGO_PENDIENTE/texto_completo_por_pagina.md --output projects/<PROYECTO>/02_extracciones/documentos_compactos/CODIGO_PENDIENTE/indice_tecnico.md
python scripts/condensar_memoria_calculo.py --text projects/<PROYECTO>/02_extracciones/documentos_compactos/CODIGO_PENDIENTE/texto_completo_por_pagina.md --output projects/<PROYECTO>/02_extracciones/documentos_compactos/CODIGO_PENDIENTE/documento_compacto.md
python scripts/validar_compresion.py --original projects/<PROYECTO>/02_extracciones/documentos_compactos/CODIGO_PENDIENTE/texto_completo_por_pagina.md --compacto projects/<PROYECTO>/02_extracciones/documentos_compactos/CODIGO_PENDIENTE/documento_compacto.md --output projects/<PROYECTO>/02_extracciones/documentos_compactos/CODIGO_PENDIENTE/reporte_compresion.yaml
```

## Colaboracion entre agentes

El orden recomendado es:

```text
PDF original -> preprocesador_documental -> coordinador -> electromecanico -> ingeniero_estudios -> profesor
```

El coordinador decide que agente interviene, exige trazabilidad y consolida la respuesta final.
