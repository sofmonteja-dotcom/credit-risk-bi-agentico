import express from "express";
import cors from "cors";
import path from "path";
import { sql } from "../src/db.js";
import { CreditRiskEvaluator } from "../skills/credit-risk-evaluator/evaluator.js";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Servir frontend estático
app.use(express.static(path.resolve(process.cwd(), "frontend")));

// 1. Endpoint de KPIs para BI Dashboard
app.get("/api/kpis", async (req, res) => {
  try {
    const [kpis] = await sql`
      SELECT
        COUNT(*)::int as total_records,
        ROUND(SUM(loan_amnt), 2) as total_exposure_usd,
        ROUND(AVG(person_income), 2) as avg_income,
        ROUND(AVG(loan_amnt), 2) as avg_loan_amount,
        ROUND(AVG(loan_int_rate), 2) as avg_interest_rate,
        ROUND(100.0 * COUNT(*) FILTER (WHERE loan_status = 1) / COUNT(*), 2) as default_rate_percentage,
        ROUND(100.0 * COUNT(*) FILTER (WHERE cb_person_default_on_file = 'Y') / COUNT(*), 2) as historic_default_percentage
      FROM credit_risk;
    `;

    const gradeDistribution = await sql`
      SELECT loan_grade, COUNT(*)::int as count,
             ROUND(100.0 * COUNT(*) FILTER (WHERE loan_status = 1) / COUNT(*), 2) as default_pct
      FROM credit_risk
      WHERE loan_grade IS NOT NULL
      GROUP BY loan_grade
      ORDER BY loan_grade ASC;
    `;

    const intentDistribution = await sql`
      SELECT loan_intent, COUNT(*)::int as count,
             ROUND(100.0 * COUNT(*) FILTER (WHERE loan_status = 1) / COUNT(*), 2) as default_pct
      FROM credit_risk
      WHERE loan_intent IS NOT NULL
      GROUP BY loan_intent
      ORDER BY count DESC;
    `;

    res.json({ success: true, kpis, gradeDistribution, intentDistribution });
  } catch (err: any) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 2. Endpoint de Alertas Tempranas (Riesgo Alto)
app.get("/api/alerts", async (req, res) => {
  try {
    const limit = Number(req.query.limit) || 15;
    const rows = await sql`
      SELECT id, person_age, person_income, person_home_ownership, person_emp_length,
             loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_percent_income,
             cb_person_default_on_file, cb_person_cred_hist_length, loan_status
      FROM credit_risk
      WHERE loan_percent_income >= 0.35 OR (cb_person_default_on_file = 'Y' AND loan_grade IN ('D', 'E', 'F', 'G'))
      ORDER BY loan_percent_income DESC
      LIMIT ${limit};
    `;

    const alerts = rows.map((r: any) => ({
      ...r,
      evaluation: CreditRiskEvaluator.evaluate(r),
    }));

    res.json({ success: true, count: alerts.length, alerts });
  } catch (err: any) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 3. Endpoint de Evaluación On-Demand de un Solicitante (Skill)
app.post("/api/evaluate", (req, res) => {
  try {
    const profile = req.body;
    if (!profile || profile.loan_percent_income === undefined) {
      return res.status(400).json({ success: false, error: "Datos del perfil crediticio incompletos." });
    }
    const evaluation = CreditRiskEvaluator.evaluate(profile);
    res.json({ success: true, evaluation });
  } catch (err: any) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 4. Endpoint de Interacción con el Agente Coordinador
app.post("/api/agent/chat", async (req, res) => {
  try {
    const { prompt } = req.body;
    if (!prompt) {
      return res.status(400).json({ success: false, error: "Falta la petición al agente." });
    }

    const lower = prompt.toLowerCase();
    let responseText = "";
    let dataPayload: any = null;

    if (lower.includes("kpi") || lower.includes("tasa") || lower.includes("resumen") || lower.includes("mora")) {
      const [kpi] = await sql`
        SELECT
          COUNT(*)::int as total_records,
          ROUND(SUM(loan_amnt), 2) as total_exposure_usd,
          ROUND(100.0 * COUNT(*) FILTER (WHERE loan_status = 1) / COUNT(*), 2) as default_rate_percentage,
          ROUND(AVG(loan_amnt), 2) as avg_loan_amount
        FROM credit_risk;
      `;
      responseText = `[Agente BI] Análisis de cartera en Neon DB:\n- Registros totales: ${kpi.total_records.toLocaleString()}\n- Exposición total: $${Number(kpi.total_exposure_usd).toLocaleString()} USD\n- Tasa de impago observada: ${kpi.default_rate_percentage}%\n- Ticket promedio de crédito: $${Number(kpi.avg_loan_amount).toLocaleString()} USD.`;
      dataPayload = kpi;
    } else if (lower.includes("alerta") || lower.includes("riesgo alto") || lower.includes("peligro")) {
      const rows = await sql`
        SELECT id, person_age, person_income, loan_intent, loan_grade, loan_amnt, loan_percent_income, cb_person_default_on_file
        FROM credit_risk
        WHERE loan_percent_income >= 0.40 AND cb_person_default_on_file = 'Y'
        LIMIT 5;
      `;
      const analyzed = rows.map((r: any) => ({ ...r, eval: CreditRiskEvaluator.evaluate(r) }));
      responseText = `[Agente BI] Se han identificado ${rows.length} perfiles con ALERTA CRÍTICA (deuda >40% de ingresos con default previo en buró). Se aconseja iniciar acción preventiva inmediata.`;
      dataPayload = analyzed;
    } else if (lower.includes("cliente") || lower.includes("evaluar") || lower.includes("id")) {
      const matchId = prompt.match(/\d+/);
      const id = matchId ? parseInt(matchId[0], 10) : 1;
      const rows = await sql`SELECT * FROM credit_risk WHERE id = ${id} LIMIT 1`;
      if (rows.length > 0) {
        const evalResult = CreditRiskEvaluator.evaluate(rows[0] as any);
        responseText = `[Agente BI] Evaluación para Cliente ID #${id}:\n- Nivel de Riesgo: ${evalResult.level} (Score: ${evalResult.score}/100)\n- Factores: ${evalResult.factors.join("; ")}\n- Recomendación: ${evalResult.recommendation}`;
        dataPayload = { customer: rows[0], evaluation: evalResult };
      } else {
        responseText = `[Agente BI] No se encontró ningún cliente con ID #${id} en Neon DB.`;
      }
    } else {
      responseText = `[Agente BI] Consulta recibida: "${prompt}". Puedes solicitarme "KPIs de cartera", "Alertas de riesgo alto" o "Evaluar cliente #ID".`;
    }

    res.json({ success: true, answer: responseText, data: dataPayload });
  } catch (err: any) {
    res.status(500).json({ success: false, error: err.message });
  }
});

export function startServer() {
  return app.listen(PORT, () => {
    console.log(`Backend de BI y Alerta Temprana activo en http://localhost:${PORT}`);
  });
}

if (process.argv[1]?.endsWith("server.ts") || process.argv[1]?.endsWith("server.js")) {
  startServer();
}
