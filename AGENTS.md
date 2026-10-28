# Documentación del Sistema Agéntico (AGENTS.md)

Este documento especifica la arquitectura, comportamiento, herramientas y reglas de decisión del **Agente Coordinador de Riesgo Crediticio** para Business Intelligence.

---

## 1. Identidad y Misión del Agente
- **Nombre**: CreditRiskCoordinatingAgent
- **Rol**: Agente Coordinador de BI y Riesgo Financiero
- **Objetivo**: Proveer monitorización continua de carteras de crédito en SaaS y Fintech, detectando prestatarios en riesgo de impago, calculando scores de solvencia e instruyendo estrategias operativas de contingencia.

---

## 2. Diagrama de Arquitectura de Principio a Fin

```
┌────────────────────────────────────────────────────────┐
│               Usuario / Frontend Dashboard             │
│            (Chart.js, Métricas KPI, Radar)             │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP REST / WebSocket
                           ▼
┌────────────────────────────────────────────────────────┐
│             Backend API Express (Node.js)              │
│       Endpoints: /api/kpis, /api/alerts, /api/agent    │
└──────────────────────────┬─────────────────────────────┘
                           │
       ┌───────────────────┴───────────────────┐
       ▼                                       ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│     Agente + Skill      │         │     Servidor MCP        │
│  (Algoritmo Heurístico  │         │  (Tools: KPIs, Alertas, │
│     de Riesgo 0-100)    │         │  Consultas Analíticas)  │
└────────────┬────────────┘         └────────────┬────────────┘
             │                                   │
             └─────────────────┬─────────────────┘
                               │ Consultas SQL (@neondatabase/serverless)
                               ▼
┌────────────────────────────────────────────────────────┐
│           Neon PostgreSQL Cloud Database               │
│           (32,581 registros en tabla credit_risk)      │
└────────────────────────────────────────────────────────┘
```

---

## 3. Herramientas MCP Disponibles (Model Context Protocol)

El agente expone e interactúa con un servidor MCP compatible con `@modelcontextprotocol/sdk`:

1. `get_portfolio_kpis`:
   - **Propósito**: Ejecuta agregaciones en Neon DB para calcular volumen colocado, mora global, ticket promedio e historial de impago.
   - **Salida**: Resumen analítico cuantitativo.

2. `get_high_risk_alerts`:
   - **Propósito**: Filtra y ordena los créditos con DTI crítico ($\ge 35\%$) o antecedentes de mora con calificación D/E/F/G.
   - **Salida**: Listado de préstamos priorizados con su evaluación de riesgo asociada.

3. `evaluate_customer_credit`:
   - **Propósito**: Aplica la Skill `credit-risk-evaluator` a un cliente específico por `customer_id`.
   - **Salida**: Puntuación (0-100), semáforo (Verde, Amarillo, Rojo), factores de riesgo y plan de acción recomendado.

4. `query_credit_data`:
   - **Propósito**: Consulta analítica de solo lectura (`SELECT`) directa sobre Neon para exploración ad-hoc.

---

## 4. Skill Propia: `credit-risk-evaluator`
- Ubicación: `skills/credit-risk-evaluator/`
- Algoritmo: Ponderación multivariable de esfuerzo financiero (DTI), grado crediticio, mora histórica en buró y estabilidad laboral/vivienda.

---

## 5. Protocolo de Mitigación y Autorizaciones
- **Riesgo Bajo (Score < 40)**: Aprobación automática de ampliación de cupos o mantenimiento de condiciones.
- **Riesgo Medio (Score 40 - 69)**: Acción automática: Programación de alertas y recordatorios 5 días antes de vencimiento.
- **Riesgo Alto (Score $\ge$ 70)**: **Requiere intervención humana (Human-in-the-Loop)**: Bloqueo cautelar de líneas adicionales, requerimiento de garantías o reestructuración de la deuda.
