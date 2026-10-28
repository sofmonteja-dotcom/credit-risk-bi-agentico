import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { sql } from "../src/db.js";
import { CreditRiskEvaluator } from "../skills/credit-risk-evaluator/evaluator.js";

const server = new Server(
  {
    name: "neon-credit-risk-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_portfolio_kpis",
        description: "Obtiene los KPIs agregados de riesgo de la cartera en Neon PostgreSQL (total colocación, tasa de impago, mora por grado)",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "get_high_risk_alerts",
        description: "Devuelve los clientes o créditos con mayor nivel de riesgo inminente de impago",
        inputSchema: {
          type: "object",
          properties: {
            limit: {
              type: "number",
              description: "Número máximo de alertas a devolver (por defecto 10)",
            },
          },
        },
      },
      {
        name: "evaluate_customer_credit",
        description: "Evalúa un perfil crediticio específico usando la Skill heurística y calcula score y recomendaciones",
        inputSchema: {
          type: "object",
          properties: {
            customer_id: {
              type: "number",
              description: "ID del cliente en la base de datos Neon",
            },
          },
          required: ["customer_id"],
        },
      },
      {
        name: "query_credit_data",
        description: "Permite al agente ejecutar consultas SELECT analíticas en Neon sobre la tabla credit_risk",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Consulta SQL SELECT (solo lectura)",
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});

// Implement tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "get_portfolio_kpis") {
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

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ kpis, gradeDistribution }, null, 2),
          },
        ],
      };
    }

    if (name === "get_high_risk_alerts") {
      const limit = Number(args?.limit) || 10;
      const rows = await sql`
        SELECT id, person_age, person_income, person_home_ownership, person_emp_length,
               loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_percent_income,
               cb_person_default_on_file, cb_person_cred_hist_length, loan_status
        FROM credit_risk
        WHERE loan_percent_income >= 0.35 OR (cb_person_default_on_file = 'Y' AND loan_grade IN ('D', 'E', 'F', 'G'))
        ORDER BY loan_percent_income DESC
        LIMIT ${limit};
      `;

      const evaluations = rows.map((r: any) => ({
        ...r,
        evaluation: CreditRiskEvaluator.evaluate(r),
      }));

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(evaluations, null, 2),
          },
        ],
      };
    }

    if (name === "evaluate_customer_credit") {
      const customerId = Number(args?.customer_id);
      const rows = await sql`
        SELECT * FROM credit_risk WHERE id = ${customerId} LIMIT 1;
      `;

      if (rows.length === 0) {
        return {
          isError: true,
          content: [{ type: "text", text: `Cliente con ID ${customerId} no encontrado.` }],
        };
      }

      const evaluation = CreditRiskEvaluator.evaluate(rows[0] as any);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ customer: rows[0], evaluation }, null, 2),
          },
        ],
      };
    }

    if (name === "query_credit_data") {
      const query = String(args?.query || "").trim();
      if (!query.toLowerCase().startsWith("select")) {
        return {
          isError: true,
          content: [{ type: "text", text: "Solo se permiten consultas analíticas SELECT." }],
        };
      }

      const results = await (sql as any).query(query);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(results.slice(0, 100), null, 2),
          },
        ],
      };
    }

    throw new Error(`Herramienta desconocida: ${name}`);
  } catch (error: any) {
    return {
      isError: true,
      content: [{ type: "text", text: `Error al ejecutar ${name}: ${error.message}` }],
    };
  }
});

export async function startMcpServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Neon Credit Risk MCP Server en ejecución via STDIO");
}

if (process.argv[1]?.endsWith("mcp-server.ts") || process.argv[1]?.endsWith("mcp-server.js")) {
  startMcpServer().catch(console.error);
}
