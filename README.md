# Sistema Agéntico de BI: Monitorización y Alerta Temprana de Riesgo Crediticio en SaaS/Fintech
*Proyecto Oficial - Hackathon INESDI: Sistemas Agénticos para Business Intelligence*

---

## 📌 1. Descripción del Proyecto
Este proyecto implementa una solución integral y funcional de **Business Intelligence Agéntico** para la detección y mitigación temprana del riesgo de impago en carteras de crédito y suscripciones SaaS/Fintech.

Conectado a una base de datos cloud **PostgreSQL en Neon** con **32,581 registros reales**, el sistema articula:
1. **Base de Datos Cloud en Neon**: Almacenamiento serverless persistente de la cartera de crédito.
2. **Skill propia (`credit-risk-evaluator`)**: Algoritmo de scoring heurístico ponderado (0 - 100) que calcula la severidad del riesgo y asigna semáforos de acción operativa.
3. **Servidor MCP (`neon-credit-risk-mcp`)**: Implementación oficial con `@modelcontextprotocol/sdk` para conectar agentes de IA mediante herramientas estándar (`get_portfolio_kpis`, `get_high_risk_alerts`, `evaluate_customer_credit`, `query_credit_data`).
4. **Backend API Express**: Endpoints analíticos y orquestación del agente coordinador.
5. **Frontend Dashboard Interactivo**: Interfaz visual con métricas financieras clave, gráficos de distribución con Chart.js, radar de alertas tempranas y chat interactivo con el agente.

---

## 🏗️ 2. Estructura del Repositorio

```text
credit-risk-neon/
├── README.md               # Documentación general e instrucciones de despliegue
├── AGENTS.md               # Arquitectura, instrucciones y herramientas del agente
├── REFLEXION.md            # Reflexiones individuales y grupales (Kaospilot)
├── neon.ts                 # Configuración oficial de Neon Database
├── .env.example            # Plantilla de variables de entorno
├── investigacion/
│   ├── mercado.md          # Análisis de mercado, competidores y alternativas de BI
│   └── problema.md         # Definición formal, hipótesis y KPIs del negocio
├── skills/
│   └── credit-risk-evaluator/
│       ├── SKILL.md        # Especificación formal de la Skill
│       └── evaluator.ts    # Lógica de scoring crediticio y planes de mitigación
├── data/
│   ├── fuente.md           # Ficha técnica, procedencia Kaggle y diccionario de datos
│   └── credit_risk_dataset.csv # Dataset con 32,581 registros
├── backend/
│   ├── server.ts           # Servidor API Express y orquestación del agente
│   └── mcp-server.ts       # Servidor MCP compatible con STDIO
├── frontend/
│   ├── index.html          # Dashboard visual y chat interactivo
│   ├── style.css           # Estilos e identidad visual
│   └── app.js              # Lógica de consumo de API y renderizado Chart.js
├── config/
│   └── mcp.json            # Configuración para clientes MCP (VS Code, Claude, etc.)
└── tests/
    ├── system.test.ts      # Suite automatizada de pruebas de integración y validación
    └── pruebas.md          # Matriz de las 9 pruebas obligatorias con evidencias
```

---

## 🚀 3. Instrucciones de Instalación y Ejecución

### Prerrequisitos
- Node.js (v18+)
- Conexión a Internet (para conectar con la base de datos Neon)

### Pasos para ejecutar en local:

1. **Clonar / Ubicar el proyecto**:
   ```bash
   cd "C:\Users\sofi montero\Documents\credit-risk-neon"
   ```

2. **Instalar dependencias**:
   ```bash
   npm install
   ```

3. **Compilar el proyecto**:
   ```bash
   npm run build
   ```

4. **Ejecutar la suite de pruebas obligatorias**:
   ```bash
   npm test
   ```

5. **Iniciar el servidor y dashboard web**:
   ```bash
   npm run server
   ```
   Abre tu navegador en: [http://localhost:3000](http://localhost:3000)

6. **(Opcional) Ejecutar el servidor MCP**:
   ```bash
   npm run mcp
   ```

---

## 📊 4. Principales Hallazgos de Business Intelligence
- **Tasa de Impago Global observada**: **21.82%** (7,108 préstamos en default de 32,581).
- **Volumen Total Colocado**: **$312,238,725 USD**.
- **Impacto del Ratio DTI**: Clientes con un ratio préstamo/ingreso mayor al 40% presentan una tasa de impago del **72.4%**, confirmando la hipótesis de riesgo por sobreendeudamiento.
- **Grado Crediticio vs Mora**: Los prestatarios en grados D, E, F y G concentran más del 65% de los impagos, lo que valida la intervención prioritaria del agente sobre estos segmentos.

---

## 👥 Equipo y Entrega
- **Alumna / Investigadora**: Sofia Montero
- **Institución**: INESDI Business Techschool
- **Hackathon**: Sistemas Agénticos para Business Intelligence
