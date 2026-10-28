import { test, describe, before } from "node:test";
import assert from "node:assert";
import { sql } from "../src/db.js";
import { CreditRiskEvaluator } from "../skills/credit-risk-evaluator/evaluator.js";

describe("Batería de Pruebas de Calidad y Validación del Sistema (Hackathon INESDI)", () => {

  // Test 1: Base de datos Cloud
  test("1. Base de datos: Conexión y consulta de datos reales en Neon Cloud", async () => {
    const [result] = await sql`SELECT COUNT(*)::int as count FROM credit_risk`;
    assert.ok(result.count >= 30000, `Se esperaban >=30000 registros, encontrados ${result.count}`);
    console.log(`✓ DB Test superado: ${result.count} registros verificados en Neon.`);
  });

  // Test 2: Skill de Negocio
  test("2. Skill: Cálculo determinista y clasificación del riesgo crediticio", () => {
    const highRiskProfile = {
      person_age: 23,
      person_income: 30000,
      person_home_ownership: "RENT",
      person_emp_length: 1,
      loan_intent: "PERSONAL",
      loan_grade: "E",
      loan_amnt: 15000,
      loan_int_rate: 16.5,
      loan_percent_income: 0.50, // 50% DTI
      cb_person_default_on_file: "Y",
      cb_person_cred_hist_length: 2,
    };

    const evaluation = CreditRiskEvaluator.evaluate(highRiskProfile);
    assert.strictEqual(evaluation.level, "ALTO");
    assert.strictEqual(evaluation.color, "ROJO");
    assert.ok(evaluation.score >= 70, `Score esperado >= 70, obtenido ${evaluation.score}`);
    assert.ok(evaluation.alertRequired === true);
    console.log(`✓ Skill Test superado: Score ${evaluation.score}/100 clasificado correctamente como ALTO.`);
  });

  // Test 3: Backend & Agregaciones BI
  test("3. Backend / KPIs: Validación de métricas de BI con datos originales", async () => {
    const [kpi] = await sql`
      SELECT
        COUNT(*)::int as total,
        ROUND(100.0 * COUNT(*) FILTER (WHERE loan_status = 1) / COUNT(*), 2) as default_rate
      FROM credit_risk;
    `;
    assert.ok(kpi.total === 32581, `Total esperado 32581, obtenido ${kpi.total}`);
    assert.ok(kpi.default_rate > 20 && kpi.default_rate < 25, `Tasa de default esperada entre 20% y 25%, obtenida ${kpi.default_rate}%`);
    console.log(`✓ KPI Test superado: Total ${kpi.total}, Tasa Default ${kpi.default_rate}%.`);
  });

  // Test 4: Gestión de Errores
  test("4. Errores: Manejo de valores faltantes y nulos en el evaluador", () => {
    const incompleteProfile = {
      person_age: 30,
      person_income: 50000,
      person_home_ownership: "",
      person_emp_length: null, // nulo
      loan_intent: "",
      loan_grade: "A",
      loan_amnt: 5000,
      loan_int_rate: null, // nulo
      loan_percent_income: 0.10,
      cb_person_default_on_file: "N",
      cb_person_cred_hist_length: 5,
    };

    const evaluation = CreditRiskEvaluator.evaluate(incompleteProfile);
    assert.strictEqual(evaluation.level, "BAJO");
    assert.strictEqual(evaluation.color, "VERDE");
    console.log(`✓ Error Handling Test superado: Registro con nulos evaluado sin excepción.`);
  });
});
