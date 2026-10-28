---
name: credit-risk-evaluator
description: >-
  Skill de Business Intelligence para cálculo algorítmico de riesgo crediticio,
  evaluación de insolvencia y generación de alertas tempranas de impago en carteras SaaS y Fintech.
version: 1.0.0
---

# Skill: Credit Risk Evaluator

## Propósito
Esta Skill encapsula la lógica matemática y de negocio para calcular el índice de riesgo crediticio ponderado de un cliente o grupo de clientes, categorizar la severidad del riesgo y formular recomendaciones preventivas de mitigación.

---

## Modelo Heurístico de Scoring (0 a 100 puntos)

El algoritmo pondera 4 dimensiones financieras críticas:

### 1. Ratio Esfuerzo Financiero (Deuda / Ingreso) - Máx 35 pts
- `loan_percent_income >= 0.40`: **35 pts** (Crítico)
- `loan_percent_income >= 0.30`: **25 pts** (Alto)
- `loan_percent_income >= 0.20`: **15 pts** (Moderado)
- `loan_percent_income < 0.20`: **5 pts** (Bajo)

### 2. Calificación Crediticia (Loan Grade) - Máx 30 pts
- Grados `E`, `F`, `G`: **30 pts** (Alto riesgo estructural)
- Grado `D`: **20 pts**
- Grado `C`: **12 pts**
- Grado `B`: **6 pts**
- Grado `A`: **0 pts** (Excelente)

### 3. Registro Histórico de Impago (Default on File) - Máx 25 pts
- `cb_person_default_on_file = 'Y'`: **25 pts** (Antecedente negativo directo)
- `cb_person_default_on_file = 'N'`: **0 pts**

### 4. Estabilidad Laboral y de Vivienda - Máx 10 pts
- `person_emp_length < 2` y vivienda `RENT`: **10 pts**
- Solo una de las anteriores: **5 pts**
- Antigüedad > 2 años o vivienda propia/hipoteca: **0 pts**

---

## Clasificación del Semáforo de Riesgo

| Rango de Score | Nivel de Riesgo | Color Semáforo | Acción Recomendada |
|---|---|---|---|
| **70 - 100** | **ALTO / CRÍTICO** | 🔴 Rojo | Alerta temprana inmediata: Solicitar aval, congelar aumento de cupo o iniciar renegociación preventiva. |
| **40 - 69** | **MEDIO / VULNERABLE**| 🟡 Amarillo | Monitoreo cercano: Revisión mensual de pagos y recordatorios previos a fecha de corte. |
| **0 - 39** | **BAJO / SEGURO** | 🟢 Verde | Riesgo controlado: Elegible para ampliación de línea o condiciones preferenciales. |

---

## Funciones Exportables del Módulo
1. `calculateRiskScore(record)`: Retorna puntuación de 0 a 100, categoría y factores detonantes.
2. `generateMitigationStrategy(score, factors)`: Genera recomendaciones accionables para el equipo de riesgo/cobranza.
3. `analyzePortfolioRisks(records)`: Genera estadísticas agregadas de distribución de riesgo.
