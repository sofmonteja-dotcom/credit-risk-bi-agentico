# Documentación del Dataset y Fuente de Datos

## 1. Origen y Ficha Técnica
- **Nombre**: Credit Risk Dataset.
- **Fuente original**: Repositorio público de [Kaggle](https://www.kaggle.com/datasets/laotse/credit-risk-dataset).
- **Licencia**: Open Data Commons / Dominio Público (CC0: Public Domain).
- **Volumen**: **32,581 registros** y **12 variables** cuantitativas y cualitativas.
- **Ubicación en el repositorio**: `data/credit_risk_dataset.csv`.

---

## 2. Base de Datos Cloud: Neon PostgreSQL
Los datos han sido desplegados y almacenados en una base de datos PostgreSQL Serverless en **Neon**:
- **Organización Neon**: `org-silent-band-87686821` (Sofia)
- **Proyecto Neon**: `aged-union-42966233` (*Monitorización y alerta temprana de riesgo crediticio o impagado*)
- **Rama**: `production` (`br-wispy-sea-b4j6fjvj`)
- **Región**: `aws-us-east-2`
- **Tabla**: `credit_risk`

---

## 3. Diccionario de Datos

| Campo | Tipo SQL | Descripción | Ejemplo / Rango |
|---|---|---|---|
| `id` | `SERIAL PRIMARY KEY` | Identificador único autoincremental en PostgreSQL | `1`, `2`, `3`... |
| `person_age` | `INT` | Edad del solicitante en años | `20 - 70` |
| `person_income` | `NUMERIC` | Ingreso anual declarado | `$4,000 - $6,000,000` |
| `person_home_ownership` | `VARCHAR(50)` | Régimen de vivienda | `RENT`, `OWN`, `MORTGAGE`, `OTHER` |
| `person_emp_length` | `NUMERIC` | Años de antigüedad en el empleo | `0.0 - 123.0` |
| `loan_intent` | `VARCHAR(50)` | Finalidad del préstamo | `PERSONAL`, `EDUCATION`, `MEDICAL`, `VENTURE`, `HOMEIMPROVEMENT`, `DEBTCONSOLIDATION` |
| `loan_grade` | `VARCHAR(10)` | Calificación crediticia asignada | `A`, `B`, `C`, `D`, `E`, `F`, `G` |
| `loan_amnt` | `NUMERIC` | Monto del préstamo solicitado en USD | `$500 - $35,000` |
| `loan_int_rate` | `NUMERIC` | Tasa de interés anual (%) | `5.42% - 23.22%` |
| `loan_status` | `INT` | Estado del préstamo (**Target**): `0` = Cumplido / al día, `1` = Default / Impago | `0` o `1` |
| `loan_percent_income` | `NUMERIC` | Ratio de préstamo respecto al ingreso anual (DTI) | `0.01 - 0.83` |
| `cb_person_default_on_file` | `VARCHAR(10)` | Registro previo de incumplimiento en buró de crédito | `Y` (Sí) / `N` (No) |
| `cb_person_cred_hist_length`| `INT` | Años de historial crediticio en buró | `2 - 30` |

---

## 4. Calidad de Datos, Limpieza y Tratamiento
- **Valores nulos**: Se identificaron valores ausentes en `person_emp_length` (~2.7%) y en `loan_int_rate` (~9.5%). Durante la ingesta a PostgreSQL se insertaron como valores `NULL` sin truncar el dataset para permitir análisis condicionales con `COALESCE` o `WHERE IS NOT NULL`.
- **Comprobación de Integridad**:
  - Total de filas importadas en Neon: **32,581 registros**.
  - Conteo verificado mediante: `SELECT COUNT(*) FROM credit_risk;`
