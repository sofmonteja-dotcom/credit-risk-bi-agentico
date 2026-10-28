import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen slides
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # INESDI Color Palette
    c_dark = RGBColor(21, 27, 32)        # #151b20
    c_cyan = RGBColor(37, 201, 232)      # #25c9e8
    c_yellow = RGBColor(245, 208, 74)    # #f5d04a
    c_white = RGBColor(255, 255, 255)
    c_light_bg = RGBColor(246, 248, 249) # #f6f8f9
    c_card_bg = RGBColor(255, 255, 255)
    c_card_border = RGBColor(219, 227, 230)
    c_text_dark = RGBColor(23, 32, 39)
    c_text_muted = RGBColor(96, 112, 121)

    def add_bg(slide, color):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.color.rgb = color
        return shape

    def add_header(slide, tag_text, title_text, dark=False):
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.2))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        
        p_tag = tf.paragraphs[0]
        p_tag.space_after = Pt(2)
        r_tag = p_tag.add_run()
        r_tag.text = tag_text.upper()
        r_tag.font.size = Pt(11)
        r_tag.font.bold = True
        r_tag.font.color.rgb = c_cyan

        p_title = tf.add_paragraph()
        r_title = p_title.add_run()
        r_title.text = title_text
        r_title.font.size = Pt(26)
        r_title.font.bold = True
        r_title.font.color.rgb = c_white if dark else c_text_dark

    # ==========================================
    # SLIDE 1: Portada (1 min)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, c_dark)

    tx_s1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.5))
    tf1 = tx_s1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.space_after = Pt(10)
    r0 = p0.add_run()
    r0.text = "HACKATHON INESDI · BUSINESS INTELLIGENCE × SISTEMAS AGÉNTICOS"
    r0.font.size = Pt(13)
    r0.font.bold = True
    r0.font.color.rgb = c_cyan

    p1 = tf1.add_paragraph()
    p1.space_after = Pt(16)
    r1 = p1.add_run()
    r1.text = "Monitorización & Alerta Temprana de\nRiesgo Crediticio en SaaS/Fintech"
    r1.font.size = Pt(38)
    r1.font.bold = True
    r1.font.color.rgb = c_white

    p2 = tf1.add_paragraph()
    p2.space_after = Pt(24)
    r2 = p2.add_run()
    r2.text = "Un sistema agéntico conectado a Neon PostgreSQL Cloud con capacidad de razonamiento, Skill propia de scoring y protocolo estándar MCP."
    r2.font.size = Pt(18)
    r2.font.color.rgb = RGBColor(218, 229, 234)

    p3 = tf1.add_paragraph()
    r3 = p3.add_run()
    r3.text = "Autora: Sofia Montero  |  Tiempo estimado de defensa: 8 - 10 minutos\nRepositorio: github.com/sofmonteja-dotcom/credit-risk-bi-agentico"
    r3.font.size = Pt(13)
    r3.font.italic = True
    r3.font.color.rgb = c_yellow

    # ==========================================
    # SLIDE 2: Problema y Contexto de Negocio (1.5 min)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2, c_light_bg)
    add_header(s2, "01 / Investigación y Problema", "¿Por qué falla la gestión de riesgo tradicional?")

    cards_s2 = [
        ("El Dolor en SaaS & Fintech", 
         "• El impago destruye entre 3% y 8% del flujo de caja anual.\n• Incremento severo del DSO (Days Sales Outstanding).\n• La cobranza reactiva recupera menos del 30% una vez vencida la deuda."),
        ("Limitación de Soluciones Actuales", 
         "• Burós estáticos (Experian/Equifax): Consultas lentas y datos desfasados.\n• Motores de reglas rígidas: Emails genéricos sin contexto.\n• ML en caja negra: Puntuaciones numéricas sin plan de acción ejecutable."),
        ("Nuestra Propuesta de Valor", 
         "• Detección preventiva antes de la fecha de corte.\n• Modelo transparente y explicable en 4 dimensiones.\n• Agente autónomo con capacidad de accionar planes de mitigación (Human-in-the-Loop).")
    ]

    for i, (title, content) in enumerate(cards_s2):
        left = Inches(0.8 + i * 3.95)
        top = Inches(2.0)
        width = Inches(3.75)
        height = Inches(4.7)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = c_card_border

        tx = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.25), width - Inches(0.4), height - Inches(0.5))
        tf = tx.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.space_after = Pt(14)
        rt = pt.add_run()
        rt.text = title
        rt.font.size = Pt(16)
        rt.font.bold = True
        rt.font.color.rgb = c_text_dark

        pc = tf.add_paragraph()
        rc = pc.add_run()
        rc.text = content
        rc.font.size = Pt(13)
        rc.font.color.rgb = c_text_muted

    # ==========================================
    # SLIDE 3: Datos Reales y Neon Cloud (1 min)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3, c_light_bg)
    add_header(s3, "02 / Datos Reales e Infraestructura", "Persistencia Cloud Serverless en Neon PostgreSQL")

    kpis_s3 = [
        ("32,581", "REGISTROS REALES", "Dataset Credit Risk (Kaggle)\n12 variables financieras"),
        ("$312.4M", "VOLUMEN COLOCADO", "Exposición total evaluada\nen Neon Cloud"),
        ("21.82%", "TASA DE DEFAULT", "7,108 clientes en impago\nBase real para modelado"),
        ("< 150 ms", "LATENCIA CLOUD", "Pooler optimizado de Neon\nen AWS us-east-2")
    ]

    for i, (metric, label, desc) in enumerate(kpis_s3):
        left = Inches(0.8 + i * 2.95)
        top = Inches(2.0)
        width = Inches(2.8)
        height = Inches(2.3)

        box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = c_dark
        box.line.color.rgb = c_dark

        tx = s3.shapes.add_textbox(left + Inches(0.15), top + Inches(0.2), width - Inches(0.3), height - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = metric
        r1.font.size = Pt(32)
        r1.font.bold = True
        r1.font.color.rgb = c_cyan

        p2 = tf.add_paragraph()
        p2.space_after = Pt(6)
        r2 = p2.add_run()
        r2.text = label
        r2.font.size = Pt(11)
        r2.font.bold = True
        r2.font.color.rgb = c_yellow

        p3 = tf.add_paragraph()
        r3 = p3.add_run()
        r3.text = desc
        r3.font.size = Pt(11)
        r3.font.color.rgb = RGBColor(180, 195, 205)

    bot_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(2.0))
    bot_box.fill.solid()
    bot_box.fill.fore_color.rgb = c_card_bg
    bot_box.line.color.rgb = c_card_border

    tx_bot = s3.shapes.add_textbox(Inches(1.1), Inches(4.9), Inches(11.1), Inches(1.6))
    tf_b = tx_bot.text_frame
    tf_b.word_wrap = True
    pb = tf_b.paragraphs[0]
    pb.space_after = Pt(6)
    rb = pb.add_run()
    rb.text = "Calidad de Datos y Aprovisionamiento:"
    rb.font.size = Pt(15)
    rb.font.bold = True
    rb.font.color.rgb = c_text_dark

    pb2 = tf_b.add_paragraph()
    rb2 = pb2.add_run()
    rb2.text = "• Tabla PostgreSQL nativa: credit_risk provisionada automáticamente con neon deploy.\n• Tratamiento de Nulos: Conservación y manejo explícito de valores nulos en antigüedad laboral y tasa de interés.\n• Conexión de Alta Eficiencia: Driver oficial @neondatabase/serverless configurado para entornos sin estado y web."
    rb2.font.size = Pt(13)
    rb2.font.color.rgb = c_text_muted

    # ==========================================
    # SLIDE 4: Arquitectura del Sistema (1.5 min)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4, c_dark)
    add_header(s4, "03 / Arquitectura de Sistemas", "Flujo Funcional de Principio a Fin (End-to-End)", dark=True)

    arch_steps = [
        ("1. Frontend", "Dashboard Web", "Chart.js, tarjetas KPI, radar de alertas y chat en lenguaje natural."),
        ("2. Backend API", "Express + TS", "Endpoints REST (/api/kpis, /api/alerts) y orquestador del agente."),
        ("3. Skill de Negocio", "credit-risk-evaluator", "Scoring heurístico 0-100 ponderado en 4 dimensiones financieras."),
        ("4. Servidor MCP", "Protocolo Oficial", "Tools estandarizadas: get_kpis, get_alerts, evaluate_customer, query_data."),
        ("5. Persistencia", "Neon PostgreSQL", "32,581 registros reales, pooler optimizado y escalabilidad automática.")
    ]

    for i, (step_num, title, desc) in enumerate(arch_steps):
        left = Inches(0.8 + i * 2.38)
        top = Inches(2.2)
        width = Inches(2.25)
        height = Inches(4.3)

        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(28, 38, 46)
        box.line.color.rgb = c_cyan if i in [2, 3] else RGBColor(54, 72, 84)

        tx = s4.shapes.add_textbox(left + Inches(0.12), top + Inches(0.2), width - Inches(0.24), height - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = step_num
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = c_yellow

        p2 = tf.add_paragraph()
        p2.space_after = Pt(10)
        r2 = p2.add_run()
        r2.text = title
        r2.font.size = Pt(16)
        r2.font.bold = True
        r2.font.color.rgb = c_white

        p3 = tf.add_paragraph()
        r3 = p3.add_run()
        r3.text = desc
        r3.font.size = Pt(12)
        r3.font.color.rgb = RGBColor(200, 215, 225)

    # ==========================================
    # SLIDE 5: La Skill Propia de Scoring (1.5 min)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5, c_light_bg)
    add_header(s5, "04 / Inteligencia de Negocio", "Skill Propia: Modelo Heurístico de Riesgo (0 - 100)")

    p_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(6.8), Inches(4.7))
    p_box.fill.solid()
    p_box.fill.fore_color.rgb = c_card_bg
    p_box.line.color.rgb = c_card_border

    tx_p = s5.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(6.4), Inches(4.3))
    tf_p = tx_p.text_frame
    tf_p.word_wrap = True

    pp0 = tf_p.paragraphs[0]
    pp0.space_after = Pt(10)
    rp0 = pp0.add_run()
    rp0.text = "4 Dimensiones Ponderadas de Solvencia:"
    rp0.font.size = Pt(16)
    rp0.font.bold = True
    rp0.font.color.rgb = c_text_dark

    pillars = [
        ("1. Esfuerzo Financiero (DTI)", "Máx 35 pts", "Ratio préstamo / ingreso anual. Penaliza severamente >= 40%."),
        ("2. Calificación Crediticia", "Máx 30 pts", "Grados E, F, G (+30 pts), Grado D (+20 pts), Grado C (+12 pts)."),
        ("3. Mora Previa en Buró", "Máx 25 pts", "Registro histórico de default = 25 pts directos."),
        ("4. Estabilidad Laboral/Vivienda", "Máx 10 pts", "Vivienda en alquiler con menos de 2 años en empleo actual.")
    ]
    for name, pts, d in pillars:
        p = tf_p.add_paragraph()
        p.space_after = Pt(6)
        r_n = p.add_run()
        r_n.text = f"• {name} [{pts}]: "
        r_n.font.bold = True
        r_n.font.size = Pt(12.5)
        r_n.font.color.rgb = c_text_dark
        r_d = p.add_run()
        r_d.text = d
        r_d.font.size = Pt(12)
        r_d.font.color.rgb = c_text_muted

    s_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(2.0), Inches(4.7), Inches(4.7))
    s_box.fill.solid()
    s_box.fill.fore_color.rgb = c_card_bg
    s_box.line.color.rgb = c_card_border

    tx_s = s5.shapes.add_textbox(Inches(8.0), Inches(2.2), Inches(4.3), Inches(4.3))
    tf_s = tx_s.text_frame
    tf_s.word_wrap = True

    ps0 = tf_s.paragraphs[0]
    ps0.space_after = Pt(14)
    rs0 = ps0.add_run()
    rs0.text = "Semáforo y Protocolo de Decisión:"
    rs0.font.size = Pt(16)
    rs0.font.bold = True
    rs0.font.color.rgb = c_text_dark

    traffic = [
        ("🟢 RIESGO BAJO (0 - 39 pts)", "Solvencia saludable. Apto para condiciones estándar o aumento de cupo."),
        ("🟡 RIESGO MEDIO (40 - 69 pts)", "Vulnerable. Recordatorios automatizados 5 días antes de vencimiento."),
        ("🔴 RIESGO ALTO (70 - 100 pts)", "Alerta crítica temprana. Intervención humana: requerir co-garantía o renegociación preventiva.")
    ]
    for tag, desc in traffic:
        p = tf_s.add_paragraph()
        p.space_after = Pt(10)
        rt = p.add_run()
        rt.text = tag + "\n"
        rt.font.bold = True
        rt.font.size = Pt(13)
        rt.font.color.rgb = c_text_dark
        rd = p.add_run()
        rd.text = desc
        rd.font.size = Pt(12)
        rd.font.color.rgb = c_text_muted

    # ==========================================
    # SLIDE 6: Servidor MCP y Protocolo (1 min)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6, c_light_bg)
    add_header(s6, "05 / Integración Estándar", "Servidor MCP (Model Context Protocol) en Acción")

    mcp_tools = [
        ("get_portfolio_kpis", "Agregaciones de Cartera", "Ejecuta queries en Neon DB calculando volumen total colocado, mora global, ticket promedio e historial de mora."),
        ("get_high_risk_alerts", "Radar de Alertas", "Filtra prestatarios con DTI crítico (>=35%) o antecedentes negativos y grado bajo. Los prioriza por severidad."),
        ("evaluate_customer_credit", "Evaluación On-Demand", "Aplica la Skill heurística sobre un cliente específico por ID, calculando su score (0-100) y recomendación."),
        ("query_credit_data", "Consultas Ad-Hoc", "Permite al agente ejecutar consultas analíticas SELECT controladas para resolver preguntas complejas de negocio.")
    ]

    for i, (tool, sub, desc) in enumerate(mcp_tools):
        row = i // 2
        col = i % 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(2.0 + row * 2.45)
        width = Inches(5.75)
        height = Inches(2.25)

        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = c_card_border

        tx = s6.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = f"Tool: {tool}"
        r1.font.size = Pt(15)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0, 142, 170)

        p2 = tf.add_paragraph()
        p2.space_after = Pt(4)
        r2 = p2.add_run()
        r2.text = sub
        r2.font.size = Pt(11)
        r2.font.bold = True
        r2.font.color.rgb = c_text_muted

        p3 = tf.add_paragraph()
        r3 = p3.add_run()
        r3.text = desc
        r3.font.size = Pt(12)
        r3.font.color.rgb = c_text_dark

    # ==========================================
    # SLIDE 7: Demostración en Vivo y Resultados (1.5 min)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7, c_dark)
    add_header(s7, "06 / Demostración en Vivo", "Dashboard de Business Intelligence & Chat del Agente", dark=True)

    demo_bullets = [
        ("Dashboard Visual Reactivo", "Renderizado con Chart.js consumiendo la API de Express conectada a Neon. Gráfico de impago por grado (A a G) y dona de destino del crédito."),
        ("Radar de Alertas Tempranas", "Tabla en tiempo real que lista los créditos de mayor riesgo, su semáforo de color y la recomendación algorítmica para el equipo de riesgo."),
        ("Chat del Agente Coordinador", "Interfaz conversacional donde el usuario pregunta en lenguaje natural ('¿Cuáles son los KPIs?' o 'Evaluar cliente #1') y el agente ejecuta las tools MCP."),
        ("Validación de Hipótesis BI", "Los datos demuestran que prestatarios con DTI >= 40% tienen un 72.4% de impago (frente al 21.8% global), validando la urgencia de alertas preventivas.")
    ]

    for i, (title, text) in enumerate(demo_bullets):
        top = Inches(2.0 + i * 1.25)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.1))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(28, 38, 46)
        card.line.color.rgb = RGBColor(54, 72, 84)

        tx = s7.shapes.add_textbox(Inches(1.1), top + Inches(0.12), Inches(11.1), Inches(0.85))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = title + " — "
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = c_cyan

        r2 = p1.add_run()
        r2.text = text
        r2.font.size = Pt(13)
        r2.font.color.rgb = RGBColor(218, 229, 234)

    # ==========================================
    # SLIDE 8: Verificación y Pruebas (1 min)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8, c_light_bg)
    add_header(s8, "07 / Calidad del Software", "9 de 9 Pruebas Obligatorias Verificadas (100% OK)")

    tests = [
        ("1. Agente", "Interpreta peticiones y clasifica riesgo"),
        ("2. Skill", "Cálculo determinista de score 0-100"),
        ("3. MCP", "Llamadas estandarizadas con retorno tipado"),
        ("4. Base de Datos", "32,581 filas leídas sin error en Neon"),
        ("5. Backend", "Endpoints REST con latencia < 150 ms"),
        ("6. Frontend", "Dashboard interactivo y chat funcional"),
        ("7. Flujo Completo", "Ciclo usuario -> agente -> Neon -> alerta"),
        ("8. Errores", "Manejo seguro de valores nulos y excepciones"),
        ("9. Validación BI", "Métricas SQL idénticas a los datos crudos")
    ]

    for i, (comp, desc) in enumerate(tests):
        row = i // 3
        col = i % 3
        left = Inches(0.8 + col * 3.95)
        top = Inches(2.0 + row * 1.6)
        width = Inches(3.75)
        height = Inches(1.4)

        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = RGBColor(46, 160, 67) # Green border

        tx = s8.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), width - Inches(0.3), height - Inches(0.3))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        r_ok = p1.add_run()
        r_ok.text = "✅ "
        r1 = p1.add_run()
        r1.text = comp
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = c_text_dark

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = desc
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = c_text_muted

    # ==========================================
    # SLIDE 9: Reflexión y Compromisos (1 min)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9, c_light_bg)
    add_header(s9, "08 / Aprendizaje Kaospilot", "Reflexión y Compromisos de Mejora")

    commitments = [
        ("VAMOS A MANTENER", c_cyan,
         "• La validación empírica y suite de pruebas obligatorias con evidencias reproducibles.\n• El rigor de conectar datos reales en producción cloud desde el día uno."),
        ("VAMOS A CAMBIAR", c_yellow,
         "• La adopción de configuraciones por defecto sin antes auditar los poolers de conexión.\n• Desarrollar con enfoque TDD (definir las pruebas antes del código del backend)."),
        ("VAMOS A EXPERIMENTAR", RGBColor(163, 113, 247),
         "• Con agentes colaborativos multi-rol que negocien automáticamente planes de pago.\n• Con búsqueda semántica mediante pgvector/Lakebase Search en Neon.")
    ]

    for i, (title, color, text) in enumerate(commitments):
        left = Inches(0.8 + i * 3.95)
        top = Inches(2.0)
        width = Inches(3.75)
        height = Inches(4.7)

        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = c_card_border

        tx = s9.shapes.add_textbox(left + Inches(0.2), top + Inches(0.25), width - Inches(0.4), height - Inches(0.5))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.space_after = Pt(12)
        r1 = p1.add_run()
        r1.text = title
        r1.font.bold = True
        r1.font.size = Pt(15)
        r1.font.color.rgb = color

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = text
        r2.font.size = Pt(13)
        r2.font.color.rgb = c_text_dark

    # ==========================================
    # SLIDE 10: Conclusión y Cierre (0.5 min)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10, c_dark)

    tx_s10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.5))
    tf10 = tx_s10.text_frame
    tf10.word_wrap = True

    p0 = tf10.paragraphs[0]
    p0.space_after = Pt(12)
    r0 = p0.add_run()
    r0.text = "CONCLUSIÓN · HACKATHON INESDI"
    r0.font.size = Pt(13)
    r0.font.bold = True
    r0.font.color.rgb = c_cyan

    p1 = tf10.add_paragraph()
    p1.space_after = Pt(18)
    r1 = p1.add_run()
    r1.text = "Un sistema sencillo, real y probado\nvale más que una arquitectura no ejecutable."
    r1.font.size = Pt(36)
    r1.font.bold = True
    r1.font.color.rgb = c_white

    p2 = tf10.add_paragraph()
    p2.space_after = Pt(24)
    r2 = p2.add_run()
    r2.text = "El proyecto demostró que la unión de PostgreSQL Serverless en Neon, el protocolo MCP y una Skill propia permite transformar dashboards tradicionales en agentes de acción empresarial."
    r2.font.size = Pt(17)
    r2.font.color.rgb = RGBColor(218, 229, 234)

    p3 = tf10.add_paragraph()
    r3 = p3.add_run()
    r3.text = "¡Muchas gracias! Estamos listos para la sesión de preguntas.\nRepositorio: https://github.com/sofmonteja-dotcom/credit-risk-bi-agentico"
    r3.font.size = Pt(14)
    r3.font.bold = True
    r3.font.color.rgb = c_yellow

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "Presentacion_Hackathon_INESDI_BI_Agentico.pptx")
    prs.save(out_path)
    print("Presentation successfully created at:", out_path)

if __name__ == "__main__":
    create_deck()
