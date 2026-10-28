import { sql } from "./db.js";
import fs from "fs";
import path from "path";
import readline from "readline";

export async function importData() {
  console.log("Checking and creating table 'credit_risk' in Neon...");

  await sql`
    CREATE TABLE IF NOT EXISTS credit_risk (
      id SERIAL PRIMARY KEY,
      person_age INT,
      person_income NUMERIC,
      person_home_ownership VARCHAR(50),
      person_emp_length NUMERIC,
      loan_intent VARCHAR(50),
      loan_grade VARCHAR(10),
      loan_amnt NUMERIC,
      loan_int_rate NUMERIC,
      loan_status INT,
      loan_percent_income NUMERIC,
      cb_person_default_on_file VARCHAR(10),
      cb_person_cred_hist_length INT
    );
  `;
  console.log("Table 'credit_risk' verified/created.");

  const csvPath = path.resolve(process.cwd(), "credit_risk_dataset.csv");
  if (!fs.existsSync(csvPath)) {
    throw new Error(`CSV file not found at ${csvPath}`);
  }

  // Count existing rows
  const [countResult] = await sql`SELECT COUNT(*)::int as count FROM credit_risk`;
  console.log(`Current row count in database: ${countResult.count}`);

  if (countResult.count >= 30000) {
    console.log("Data already populated! Skipping bulk import.");
    return;
  }

  console.log("Reading and uploading data in batches...");
  const fileStream = fs.createReadStream(csvPath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });

  let isHeader = true;
  let batch: any[] = [];
  let totalInserted = 0;
  const BATCH_SIZE = 500;

  for await (const line of rl) {
    if (isHeader) {
      isHeader = false;
      continue;
    }
    if (!line.trim()) continue;

    const parts = line.split(",");
    batch.push({
      person_age: parts[0] ? parseInt(parts[0], 10) : null,
      person_income: parts[1] ? parseFloat(parts[1]) : null,
      person_home_ownership: parts[2] || null,
      person_emp_length: parts[3] ? parseFloat(parts[3]) : null,
      loan_intent: parts[4] || null,
      loan_grade: parts[5] || null,
      loan_amnt: parts[6] ? parseFloat(parts[6]) : null,
      loan_int_rate: parts[7] ? parseFloat(parts[7]) : null,
      loan_status: parts[8] ? parseInt(parts[8], 10) : null,
      loan_percent_income: parts[9] ? parseFloat(parts[9]) : null,
      cb_person_default_on_file: parts[10] || null,
      cb_person_cred_hist_length: parts[11] ? parseInt(parts[11], 10) : null,
    });

    if (batch.length >= BATCH_SIZE) {
      await insertBatch(batch);
      totalInserted += batch.length;
      process.stdout.write(`Inserted ${totalInserted} records...\r`);
      batch = [];
    }
  }

  if (batch.length > 0) {
    await insertBatch(batch);
    totalInserted += batch.length;
  }

  console.log(`\nImport completed! Total inserted this session: ${totalInserted}`);
}

async function insertBatch(rows: any[]) {
  const values: string[] = [];
  for (const r of rows) {
    const age = r.person_age !== null ? r.person_age : "NULL";
    const income = r.person_income !== null ? r.person_income : "NULL";
    const ownership = r.person_home_ownership ? `'${r.person_home_ownership.replace(/'/g, "''")}'` : "NULL";
    const empLength = r.person_emp_length !== null ? r.person_emp_length : "NULL";
    const intent = r.loan_intent ? `'${r.loan_intent.replace(/'/g, "''")}'` : "NULL";
    const grade = r.loan_grade ? `'${r.loan_grade.replace(/'/g, "''")}'` : "NULL";
    const amnt = r.loan_amnt !== null ? r.loan_amnt : "NULL";
    const intRate = r.loan_int_rate !== null ? r.loan_int_rate : "NULL";
    const status = r.loan_status !== null ? r.loan_status : "NULL";
    const pctInc = r.loan_percent_income !== null ? r.loan_percent_income : "NULL";
    const defaultOnFile = r.cb_person_default_on_file ? `'${r.cb_person_default_on_file.replace(/'/g, "''")}'` : "NULL";
    const credHist = r.cb_person_cred_hist_length !== null ? r.cb_person_cred_hist_length : "NULL";

    values.push(`(${age}, ${income}, ${ownership}, ${empLength}, ${intent}, ${grade}, ${amnt}, ${intRate}, ${status}, ${pctInc}, ${defaultOnFile}, ${credHist})`);
  }

  const query = `
    INSERT INTO credit_risk (
      person_age, person_income, person_home_ownership, person_emp_length,
      loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_status,
      loan_percent_income, cb_person_default_on_file, cb_person_cred_hist_length
    ) VALUES ${values.join(", ")};
  `;
  await (sql as any).query(query);
}
