# Fase 01: Investigación de Mercado y Contexto de Negocio

## Problema Seleccionado
**Monitorización y alerta temprana de riesgo crediticio o impagados en SaaS/Fintech.**

---

## 1. Contexto y Relevancia en la Industria
En los modelos de negocio SaaS (Software as a Service) con facturación periódica y en empresas Fintech (BNPL, líneas de crédito, lending B2B/B2C), el principal destructor de margen operativo y flujo de caja es el **Default Rate** (tasa de impago) y el **DSO (Days Sales Outstanding)** elevado.

Los sistemas tradicionales de gestión de cobros suelen ser:
- **Reactivos**: Actúan cuando la cuota o factura ya está vencida (>30 o >60 días).
- **Aislados**: Los equipos de riesgo evalúan al alta del cliente (onboarding), pero no monitorizan el comportamiento continuo ni correlacionan factores dinámicos (ratio de apalancamiento, historial, historial crediticio).
- **Poco explicables**: Generan una alerta rígida o una puntuación numérica sin contexto cualitativo ni un plan de acción agéntico.

---

## 2. Análisis del Mercado y Competidores
| Solución / Competidor | Tipo de Enfoque | Limitaciones Actuales | Nuestra Oportunidad Agéntica |
|---|---|---|---|
| **Experian / Equifax** | Buró de crédito estático | Datos con latencia, costos por consulta altos, scoring rígido | Análisis continuo con datos propios en Neon DB y evaluación heurística en tiempo real. |
| **HighRadius / Upflow** | Automatización de cuentas por cobrar (AR) | Basado en reglas manuales de emails y recordatorios | Agente autónomo con capacidad de razonamiento contextual, cálculo de métricas financieras y recomendación de mitigación personalizada. |
| **Modelos ML Tradicionales (Scikit-Learn/XGBoost)** | Modelos de scoring en batch | 'Caja negra' que entrega probabilidad sin narrativa ni plan de mitigación ejecutable | Agente con Tool Calling (MCP/Skill) que explica los causantes del riesgo y sugiere acciones operativas. |

---

## 3. Pensamiento Divergente: 5 Problemas de BI Evaluados

Antes de seleccionar la monitorización de riesgo crediticio, se evaluaron 5 alternativas de Business Intelligence:
1. **Detección y alerta temprana de riesgo crediticio e impagados en Fintech/SaaS (ELEGIDO)**:
   - *Ventajas*: Impacto financiero directo en EBITDA y liquidez, disponibilidad de datos estructurados, aplicabilidad real de alertas y mitigación.
2. **Predicción de Churn de clientes en SaaS B2B**:
   - *Descarte*: Dificultad para obtener datasets reales con logs de telemetría de producto fiables.
3. **Optimización de inventario y rotación de stock en e-commerce**:
   - *Descarte*: Menor adecuación para toma de decisiones agéntica explicable.
4. **Análisis de sentimiento y reputación en atención al cliente**:
   - *Descarte*: Menor impacto cuantitativo en el balance financiero.
5. **Detección de anomalías en transacciones para prevención de fraude**:
   - *Descarte*: Requiere baja latencia milimétrica que compite con motores de reglas de streaming antes que BI de decisión.

---

## 4. Usuario Objetivo y Propuesta de Valor
- **Usuario objetivo**: Chief Risk Officer (CRO), Analistas de Riesgo Crediticio, Head of Collections y Directores Financieros (CFO) de Fintechs y SaaS.
- **Propuesta de Valor**: Sistema agéntico de Business Intelligence conectado a la base de datos cloud en Neon PostgreSQL que:
  1. Detecta carteras o perfiles con alta propensión a impago antes del vencimiento.
  2. Diagnostica causas raíz (alta carga de deuda sobre ingreso, calificación crediticia baja, historial previo).
  3. Recomienda y redacta planes de contingencia (ajuste de línea, garantías adicionales o renegociación preventiva).
  4. Permite interactuar conversacionalmente con la base de datos mediante lenguaje natural y herramientas estandarizadas.
