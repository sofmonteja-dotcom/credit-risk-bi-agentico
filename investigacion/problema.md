# Definición del Problema, Hipótesis y KPIs de Business Intelligence

## 1. Definición Formal del Problema
Las instituciones financieras y empresas SaaS pierden anualmente entre un 3% y un 8% de su cartera total debido a impagos no anticipados. La ausencia de un monitoreo dinámico impide intervenir a tiempo con renegociaciones preventivas o reducción de límites crediticios.

---

## 2. Hipótesis de Negocio a Validar con Datos Reales
1. **Hipótesis 1 (Ratio Esfuerzo Financiero)**: Clientes cuyo ratio de préstamo respecto a su ingreso anual (`loan_percent_income`) supera el **35% - 40%** presentan una tasa de morosidad significativamente superior al promedio (>45% vs ~21%).
2. **Hipótesis 2 (Historial previo como predictor dominante)**: Aquellos prestatarios con registro de default previo (`cb_person_default_on_file = 'Y'`) tienen un riesgo multiplicado de reincidencia cuando se combinan con calificaciones de riesgo Grado D, E, F o G.
3. **Hipótesis 3 (Antigüedad y estabilidad laboral)**: Personas con poca antigüedad laboral (< 2 años) y vivienda en alquiler tienen menor resiliencia ante shocks económicos.

---

## 3. Cuadro de Mando y KPIs Clave de BI

| Métrica / KPI | Fórmula / Cálculo | Objetivo / Umbral de Alerta |
|---|---|---|
| **Default Rate (Tasa de Impago Global)** | `(Count(loan_status = 1) / Count(*)) * 100` | Mantener por debajo del 22% en cartera general |
| **High Risk Exposure (Exposición en Riesgo Crítico)** | `SUM(loan_amnt) WHERE risk_score >= 70` | Alerta cuando supere el 15% del capital total colocado |
| **Avg Debt-to-Income (DTI Medio)** | `AVG(loan_percent_income)` | Umbral saludable < 0.20 (20%) |
| **Default por Grado Crediticio (A-G)** | `COUNT(status=1) GROUP BY loan_grade` | Supervisar concentración en grados D, E, F |
| **Tasa de Recuperación Preventiva Estimada** | Reducción de impago proyectada mediante alerta temprana | Impacto potencial: reducción de 15% a 25% de pérdidas netas |

---

## 4. Fuentes de Información y Referencias
- **Dataset**: Credit Risk Dataset (Kaggle) con 32,581 registros anonimizados de perfiles crediticios, ingresos, historial y status de pago.
- **Estándares Regulatorios**: Principios de Basilea III para riesgo de crédito y provisiones IFRS 9 (clasificación de riesgo en Stage 1, 2 y 3).
- **Metodología de Evaluación**: Score crediticio ponderado multivariable (0 - 100 puntos de severidad de riesgo).
