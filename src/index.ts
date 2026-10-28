import { sql } from "./db.js";
import { importData } from "./import-data.js";

async function main() {
  console.log("=== Testing Neon PostgreSQL Connection ===");

  // 1. Connection check
  const [version] = await sql`SELECT version()`;
  console.log("PostgreSQL Version:", version.version);

  const [dbInfo] = await sql`SELECT current_database(), current_user`;
  console.log(`Connected to database '${dbInfo.current_database}' as user '${dbInfo.current_user}'.`);

  // 2. Import dataset if needed
  await importData();

  // 3. Query sample records to prove end-to-end functionality
  console.log("\n=== Querying Sample Records from Neon ===");
  const records = await sql`
    SELECT id, person_age, person_income, loan_intent, loan_amnt, loan_status
    FROM credit_risk
    ORDER BY id ASC
    LIMIT 5;
  `;
  console.table(records);

  // 4. Run an aggregation
  const [stats] = await sql`
    SELECT
      COUNT(*)::int as total_records,
      ROUND(AVG(person_age), 1) as avg_age,
      ROUND(AVG(person_income), 2) as avg_income,
      ROUND(AVG(loan_amnt), 2) as avg_loan_amnt
    FROM credit_risk;
  `;
  console.log("\n=== Dataset Summary in Neon ===");
  console.log(stats);

  console.log("\nEnd-to-end test passed successfully!");
}

main().catch((err) => {
  console.error("Error during execution:", err);
  process.exit(1);
});
