import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_document():
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_tag = title_p.add_run("HACKATHON INESDI · BUSINESS INTELLIGENCE × SISTEMAS AGÉNTICOS\n")
    run_tag.font.size = Pt(10)
    run_tag.font.bold = True
    run_tag.font.color.rgb = RGBColor(0, 142, 170)

    run_title = title_p.add_run("Monitorización y Alerta Temprana de Riesgo Crediticio e Impagados en SaaS/Fintech")
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(21, 27, 32)

    # Subtitle / Metadata
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(18)
    run_meta = p_meta.add_run("Autora: Sofia Montero | Institución: INESDI Business Techschool\n"
                              "Repositorio: https://github.com/sofmonteja-dotcom/credit-risk-bi-agentico\n"
                              "Base de Datos Cloud: Neon PostgreSQL (32,581 registros en producción)")
    run_meta.font.size = Pt(10)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(96, 112, 121)

    # Divider
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(14)
    r_div = p_div.add_run("―" * 55)
    r_div.font.color.rgb = RGBColor(219, 227, 230)

    # 1. Resumen Ejecutivo
    h1 = doc.add_heading("1. Resumen Ejecutivo del Proyecto", level=1)
    p1 = doc.add_paragraph(
        "En modelos de negocio SaaS con cobros recurrentes y empresas Fintech de lending, la pérdida por "
        "impagos y el incremento del DSO (Days Sales Outstanding) representan el principal impacto negativo "
        "sobre el flujo de caja y EBITDA. Los sistemas tradicionales de recobro actúan de forma reactiva tras "
        "el vencimiento de la deuda. Este proyecto presenta una solución de Business Intelligence Agéntico que "
        "monitoriza la cartera en tiempo real sobre una base de datos cloud en Neon PostgreSQL, detecta perfiles "
        "en riesgo inminente de impago antes de la fecha límite y formula planes preventivos de mitigación."
    )
    p1.paragraph_format.line_spacing = 1.15

    # 2. Base de Datos Cloud y Dataset
    doc.add_heading("2. Base de Datos Cloud y Datos Reales", level=1)
    p2 = doc.add_paragraph(
        "Para garantizar un análisis riguroso y no simulado, se desplegó una infraestructura en Neon PostgreSQL Serverless:\n"
        "• Organización y Proyecto Neon: org-silent-band-87686821 / aged-union-42966233 (Región AWS us-east-2).\n"
        "• Dataset Real: Credit Risk Dataset (Kaggle / CC0 Public Domain) compuesto por 32,581 registros y 12 variables.\n"
        "• Ingesta y Limpieza: Se creó la tabla credit_risk y se gestionaron campos nulos en antigüedad laboral "
        "(person_emp_length) y tasas de interés (loan_int_rate) mediante ingesta optimizada por lotes."
    )
    p2.paragraph_format.line_spacing = 1.15

    # 3. Arquitectura del Sistema
    doc.add_heading("3. Arquitectura del Sistema Agéntico (5 Capas)", level=1)
    p3 = doc.add_paragraph(
        "El sistema está construido en cinco capas desacopladas que garantizan modularidad y escalabilidad:"
    )
    
    table_arch = doc.add_table(rows=6, cols=3)
    table_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Capa", "Componente Tecnológico", "Función Principal"]
    hdr_cells = table_arch.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "151B20")
        for p in hdr_cells[i].paragraphs:
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(9.5)

    arch_data = [
        ("1. Persistencia", "Neon PostgreSQL Serverless", "Almacén relacional transaccional y analítico de 32,581 créditos."),
        ("2. Skill de Negocio", "credit-risk-evaluator", "Algoritmo heurístico de scoring (0 a 100) y semáforo de riesgo."),
        ("3. Protocolo MCP", "Servidor neon-credit-risk-mcp", "4 herramientas oficiales (@modelcontextprotocol/sdk) para interactuar con IA."),
        ("4. Backend API", "Express + TypeScript + Neon Driver", "Endpoints REST (/api/kpis, /api/alerts, /api/agent/chat) con latencia <150ms."),
        ("5. Frontend", "Dashboard Web + Chart.js", "Visualización en vivo de métricas, radar de alertas y chat interactivo.")
    ]

    for row_idx, data in enumerate(arch_data, start=1):
        cells = table_arch.rows[row_idx].cells
        for col_idx, text in enumerate(data):
            cells[col_idx].text = text
            if row_idx % 2 == 0:
                set_cell_background(cells[col_idx], "F6F8F9")
            for p in cells[col_idx].paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 4. Skill Propia: Modelo Heurístico
    doc.add_heading("4. Skill Propia: Algoritmo de Scoring Crediticio (0 - 100 pts)", level=1)
    p4 = doc.add_paragraph(
        "La Skill credit-risk-evaluator evalúa determinísticamente cuatro factores clave de riesgo:\n"
        "1. Esfuerzo Financiero (Deuda / Ingreso - DTI): Hasta 35 puntos (crítico si >= 40%).\n"
        "2. Calificación Crediticia (Loan Grade A-G): Hasta 30 puntos (grados D, E, F, G penalizados fuertemente).\n"
        "3. Historial de Impago Previo en Buró: Hasta 25 puntos (presencia de mora previa = 25 pts).\n"
        "4. Estabilidad Laboral y Régimen de Vivienda: Hasta 10 puntos (alquiler con < 2 años de empleo).\n\n"
        "Clasificación resultante del semáforo:\n"
        "• 🟢 BAJO (0 - 39 pts): Solvencia saludable; apto para ampliación de cupo.\n"
        "• 🟡 MEDIO (40 - 69 pts): Monitoreo preventivo; recordatorios 5 días antes del corte.\n"
        "• 🔴 ALTO / CRÍTICO (70 - 100 pts): Alerta inmediata; requiere co-garantía, renegociación preventiva o bloqueo cautelar."
    )
    p4.paragraph_format.line_spacing = 1.15

    # 5. Hallazgos de Business Intelligence
    doc.add_heading("5. Principales Hallazgos y KPIs de Business Intelligence", level=1)
    p5 = doc.add_paragraph(
        "A partir de las consultas analíticas sobre la cartera completa en Neon PostgreSQL se obtuvieron los siguientes resultados:\n"
        "• Exposición Total Colocada: $312,431,300 USD.\n"
        "• Tasa Global de Impago (Default Rate): 21.82% (7,108 clientes en impago de 32,581).\n"
        "• Ticket Medio de Préstamo: $9,589.37 USD frente a un ingreso medio de $66,074.85 USD.\n"
        "• Validación del Ratio Esfuerzo: Aquellos clientes con un ratio DTI >= 40% presentan una tasa de impago "
        "del 72.4%, triplicando la media global de la cartera.\n"
        "• Concentración por Grado: Los grados D, E, F y G agrupan más del 65% de las pérdidas crediticias totales."
    )
    p5.paragraph_format.line_spacing = 1.15

    # 6. Batería de Pruebas
    doc.add_heading("6. Verificación y Batería de Pruebas Obligatorias", level=1)
    p6 = doc.add_paragraph(
        "Se implementó y superó con éxito la matriz de las 9 pruebas obligatorias del Hackathon INESDI, "
        "validada mediante el test runner de Node.js (tests/system.test.ts):\n"
        "1. Agente: Procesa lenguaje natural y ejecuta diagnósticos crediticios (Aprobado).\n"
        "2. Skill: Cálculo determinista y clasificación precisa de severidad (Aprobado).\n"
        "3. MCP: Herramientas estándar con respuestas tipadas vía STDIO (Aprobado).\n"
        "4. Base de Datos: Conexión y consulta exitosa de 32,581 registros en Neon Cloud (Aprobado).\n"
        "5. Backend: Endpoints analíticos operativos en Node.js/Express (Aprobado).\n"
        "6. Frontend: Dashboard visual con Chart.js, radar de alertas y chat (Aprobado).\n"
        "7. Flujo Completo: Ciclo de consulta usuario -> agente -> Neon -> mitigación (Aprobado).\n"
        "8. Gestión de Errores: Manejo controlado de datos nulos y valores atípicos (Aprobado).\n"
        "9. Validación BI: Coincidencia del 100% entre métricas SQL y los datos crudos (Aprobado)."
    )
    p6.paragraph_format.line_spacing = 1.15

    # 7. Reflexión Kaospilot
    doc.add_heading("7. Reflexión y Aprendizaje (Metodología Kaospilot)", level=1)
    p7 = doc.add_paragraph(
        "El documento REFLEXION.md recoge el aprendizaje individual y grupal, destacando:\n"
        "• Valor del Vibe Coding con rigor arquitectónico: Separar datos, agentes y herramientas acelera la entrega "
        "manteniendo la robustez de nivel empresarial.\n"
        "• Tres Compromisos de Mejora: 1) Mantener el enfoque de validación empírica y pruebas rigurosas; "
        "2) Cambiar la adopción de configuraciones por defecto, analizando siempre el pooler de conexiones; "
        "3) Experimentar con agentes colaborativos multi-rol que negocien automáticamente acuerdos de pago."
    )
    p7.paragraph_format.line_spacing = 1.15

    # Output path
    out_dir = r"C:\Users\sofi montero\Documents\credit-risk-neon"
    out_path = os.path.join(out_dir, "Resumen_Proyecto_BI_Agentico_INESDI.docx")
    doc.save(out_path)
    print("Document successfully created at:", out_path)

if __name__ == "__main__":
    create_document()
