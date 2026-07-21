import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const templates = path.join(repo, "templates");
const projectTemplate = path.join(repo, "projects", "_TEMPLATE_PROYECTO");

function header(sheet, range, values) {
  sheet.getRange(range).values = [values];
  sheet.getRange(range).format = {
    fill: "#1F4E79",
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
  };
}

async function saveWorkbook(workbook, outputPath) {
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  const errors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 50 },
    summary: "formula error scan",
  });
  if (errors.ndjson && errors.ndjson.includes("#")) {
    console.warn(errors.ndjson);
  }
  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(outputPath);
}

function styleWorkbook(workbook) {
  for (const sheet of workbook.worksheets.items) {
    sheet.freezePanes.freezeRows(1);
    const used = sheet.getUsedRange();
    used.format.wrapText = true;
    used.format.borders = { preset: "all", style: "thin", color: "#D9D9D9" };
  }
}

function buildAuditoria() {
  const workbook = Workbook.create();
  const sheetNames = [
    "00_Instrucciones",
    "01_Ficha_Proyecto",
    "02_Registro_Documentos",
    "03_Catalogo_Conductores",
    "04_Catalogo_Ductos",
    "05_Cables_Equipos",
    "06_Resumen_CAG",
    "07_Tramos_Camaras",
    "08_Matriz_Paso",
    "09_Resumen_PVC",
    "10_Observaciones",
    "11_Referencia_Documental",
  ];
  for (const name of sheetNames) workbook.worksheets.add(name);

  let sheet = workbook.worksheets.getItem("00_Instrucciones");
  sheet.getRange("A1:B6").values = [
    ["Campo", "Instruccion"],
    ["Regla principal", "No mezclar proyectos ni subestaciones."],
    ["Datos faltantes", "Usar PENDIENTE DE VALIDAR."],
    ["Estados", "CONFIRMADO, RECALCULADO, INFERIDO, PENDIENTE, INCONSISTENTE."],
    ["Calculo de area", "Usar diametro exterior del cable."],
    ["Trazabilidad", "Registrar documento, codigo, revision y pagina o lamina."],
  ];
  header(sheet, "A1:B1", ["Campo", "Instruccion"]);

  sheet = workbook.worksheets.getItem("01_Ficha_Proyecto");
  sheet.getRange("A1:C9").values = [
    ["Campo", "Valor", "Estado"],
    ["Proyecto", "PENDIENTE DE VALIDAR", "PENDIENTE"],
    ["Subestacion", "PENDIENTE DE VALIDAR", "PENDIENTE"],
    ["Cliente", "PENDIENTE DE VALIDAR", "PENDIENTE"],
    ["Ubicacion", "PENDIENTE DE VALIDAR", "PENDIENTE"],
    ["Revision", "PENDIENTE DE VALIDAR", "PENDIENTE"],
    ["Responsable", "PENDIENTE DE VALIDAR", "PENDIENTE"],
    ["Fecha", "PENDIENTE DE VALIDAR", "PENDIENTE"],
    ["Regla", "No reutilizar datos de otra subestacion sin validacion expresa.", "CONFIRMADO"],
  ];
  header(sheet, "A1:C1", ["Campo", "Valor", "Estado"]);

  sheet = workbook.worksheets.getItem("02_Registro_Documentos");
  header(sheet, "A1:N1", [
    "Proyecto",
    "Subestacion",
    "Codigo documental",
    "Titulo",
    "Revision o edicion",
    "Fecha",
    "Disciplina",
    "Tipo de documento",
    "Estado documental",
    "Paginas o laminas",
    "Fuente",
    "Nivel de confianza",
    "Archivo",
    "Advertencias",
  ]);

  sheet = workbook.worksheets.getItem("03_Catalogo_Conductores");
  header(sheet, "A1:E1", ["Conductor", "Diametro exterior mm", "Area exterior mm2", "Fuente", "Estado"]);
  sheet.getRange("C2").formulas = [["=IF(ISNUMBER(B2),PI()*(B2/2)^2,\"\")"]];
  sheet.getRange("C2:C200").fillDown();

  sheet = workbook.worksheets.getItem("04_Catalogo_Ductos");
  header(sheet, "A1:G1", ["Ducto", "Diametro exterior mm", "Espesor mm", "Diametro interior mm", "Area util mm2", "Fuente", "Estado"]);
  sheet.getRange("D2").formulas = [["=IF(AND(ISNUMBER(B2),ISNUMBER(C2)),B2-2*C2,\"\")"]];
  sheet.getRange("E2").formulas = [["=IF(ISNUMBER(D2),PI()*(D2/2)^2,\"\")"]];
  sheet.getRange("D2:E200").fillDown();

  sheet = workbook.worksheets.getItem("05_Cables_Equipos");
  header(sheet, "A1:T1", [
    "ID cable",
    "Proyecto",
    "Pano",
    "Equipo origen",
    "Caja agrupamiento",
    "Camara ingreso",
    "Destino",
    "Funcion",
    "Conductor",
    "Cantidad",
    "Diametro exterior catalogo",
    "Diametro exterior manual",
    "Diametro utilizado",
    "Area unitaria",
    "Area total",
    "Clasificacion",
    "Fuente documental",
    "Pagina o lamina",
    "Estado",
    "Observacion",
  ]);
  sheet.getRange("M2").formulas = [["=IF(ISNUMBER(L2),L2,IF(ISNUMBER(K2),K2,\"\"))"]];
  sheet.getRange("N2").formulas = [["=IF(ISNUMBER(M2),PI()*(M2/2)^2,\"\")"]];
  sheet.getRange("O2").formulas = [["=IF(AND(ISNUMBER(J2),ISNUMBER(N2)),J2*N2,\"\")"]];
  sheet.getRange("M2:O200").fillDown();

  sheet = workbook.worksheets.getItem("06_Resumen_CAG");
  header(sheet, "A1:E1", ["Tramo", "Area total", "Ductos", "% ocupacion", "Estado"]);

  sheet = workbook.worksheets.getItem("07_Tramos_Camaras");
  header(sheet, "A1:H1", ["ID tramo", "Origen", "Destino", "Tipo ducto", "Cantidad ductos", "Area util por ducto", "Fuente", "Estado"]);

  sheet = workbook.worksheets.getItem("08_Matriz_Paso");
  header(sheet, "A1:G1", ["ID cable", "Equipo", "Clasificacion", "Area total", "TR-01", "TR-02", "TR-03"]);

  sheet = workbook.worksheets.getItem("09_Resumen_PVC");
  header(sheet, "A1:L1", [
    "Tramo",
    "Area control",
    "Ductos control",
    "% ocupacion control",
    "Area fuerza",
    "Ductos fuerza",
    "% ocupacion fuerza",
    "Reserva",
    "Total ductos",
    "Area util ducto",
    "% maximo",
    "Estado",
  ]);
  sheet.getRange("C2").formulas = [["=IF(AND(ISNUMBER(B2),ISNUMBER(J2),ISNUMBER(K2)),ROUNDUP(B2/(J2*K2),0),\"\")"]];
  sheet.getRange("D2").formulas = [["=IF(AND(ISNUMBER(B2),ISNUMBER(C2),ISNUMBER(J2)),B2/(C2*J2),\"\")"]];
  sheet.getRange("F2").formulas = [["=IF(AND(ISNUMBER(E2),ISNUMBER(J2),ISNUMBER(K2)),ROUNDUP(E2/(J2*K2),0),\"\")"]];
  sheet.getRange("G2").formulas = [["=IF(AND(ISNUMBER(E2),ISNUMBER(F2),ISNUMBER(J2)),E2/(F2*J2),\"\")"]];
  sheet.getRange("I2").formulas = [["=IF(AND(ISNUMBER(C2),ISNUMBER(F2)),C2+F2,\"\")"]];
  sheet.getRange("C2:I100").fillDown();

  sheet = workbook.worksheets.getItem("10_Observaciones");
  header(sheet, "A1:H1", ["ID", "Documento", "Codigo", "Revision", "Pagina o lamina", "Observacion", "Estado", "Accion recomendada"]);

  sheet = workbook.worksheets.getItem("11_Referencia_Documental");
  header(sheet, "A1:G1", ["ID dato", "Documento", "Codigo", "Revision", "Pagina o lamina", "Fuente", "Nivel confianza"]);

  styleWorkbook(workbook);
  return workbook;
}

function buildSimple(sheetName, headers) {
  const workbook = Workbook.create();
  const sheet = workbook.worksheets.add(sheetName);
  const endCol = String.fromCharCode("A".charCodeAt(0) + headers.length - 1);
  header(sheet, `A1:${endCol}1`, headers);
  styleWorkbook(workbook);
  return workbook;
}

await saveWorkbook(buildAuditoria(), path.join(templates, "auditoria_canalizaciones.xlsx"));
await saveWorkbook(buildAuditoria(), path.join(projectTemplate, "registro_documentos.xlsx"));
await saveWorkbook(
  buildSimple("Registro", [
    "Proyecto",
    "Subestacion",
    "Codigo documental",
    "Titulo",
    "Revision o edicion",
    "Fecha",
    "Disciplina",
    "Tipo de documento",
    "Estado documental",
    "Paginas o laminas",
    "Fuente",
    "Nivel de confianza",
    "Archivo",
    "Advertencias",
  ]),
  path.join(templates, "registro_documentos.xlsx"),
);
await saveWorkbook(
  buildSimple("Matriz_Trazabilidad", ["ID dato", "Proyecto", "Documento", "Codigo", "Revision", "Pagina o lamina", "Dato", "Estado", "Observacion"]),
  path.join(templates, "matriz_trazabilidad.xlsx"),
);
await saveWorkbook(
  buildSimple("Observaciones", ["ID", "Proyecto", "Documento", "Codigo", "Pagina o lamina", "Observacion", "Estado", "Accion recomendada", "Respuesta"]),
  path.join(templates, "listado_observaciones.xlsx"),
);

console.log("Plantillas Excel generadas.");
