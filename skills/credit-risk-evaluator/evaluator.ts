export interface CreditProfile {
  id?: number;
  person_age: number;
  person_income: number;
  person_home_ownership: string;
  person_emp_length: number | null;
  loan_intent: string;
  loan_grade: string;
  loan_amnt: number;
  loan_int_rate: number | null;
  loan_status?: number;
  loan_percent_income: number;
  cb_person_default_on_file: string;
  cb_person_cred_hist_length: number;
}

export interface RiskEvaluationResult {
  score: number; // 0 a 100
  level: "BAJO" | "MEDIO" | "ALTO";
  color: "VERDE" | "AMARILLO" | "ROJO";
  factors: string[];
  recommendation: string;
  alertRequired: boolean;
}

export class CreditRiskEvaluator {
  /**
   * Evalúa el perfil crediticio de un solicitante utilizando la heurística de riesgo
   */
  public static evaluate(profile: CreditProfile): RiskEvaluationResult {
    let score = 0;
    const factors: string[] = [];

    // 1. Esfuerzo financiero (Loan-to-Income) - Max 35 pts
    const dti = Number(profile.loan_percent_income);
    if (dti >= 0.40) {
      score += 35;
      factors.push(`Carga de deuda crítica (${(dti * 100).toFixed(1)}% del ingreso anual)`);
    } else if (dti >= 0.30) {
      score += 25;
      factors.push(`Carga de deuda alta (${(dti * 100).toFixed(1)}% del ingreso)`);
    } else if (dti >= 0.20) {
      score += 15;
      factors.push(`Carga de deuda moderada (${(dti * 100).toFixed(1)}%)`);
    } else {
      score += 5;
    }

    // 2. Grado Crediticio (Loan Grade) - Max 30 pts
    const grade = (profile.loan_grade || "").toUpperCase();
    if (["E", "F", "G"].includes(grade)) {
      score += 30;
      factors.push(`Calificación crediticia de alto riesgo (Grado ${grade})`);
    } else if (grade === "D") {
      score += 20;
      factors.push(`Calificación crediticia baja (Grado D)`);
    } else if (grade === "C") {
      score += 12;
    } else if (grade === "B") {
      score += 6;
    }

    // 3. Historial de impago previo - Max 25 pts
    const defaultOnFile = (profile.cb_person_default_on_file || "").toUpperCase();
    if (defaultOnFile === "Y") {
      score += 25;
      factors.push("Registro previo de impago/mora en buró de crédito");
    }

    // 4. Estabilidad laboral y vivienda - Max 10 pts
    const empLength = profile.person_emp_length !== null ? Number(profile.person_emp_length) : 0;
    const isRent = (profile.person_home_ownership || "").toUpperCase() === "RENT";
    if (empLength < 2 && isRent) {
      score += 10;
      factors.push("Baja estabilidad combinada: vivienda en alquiler y <2 años de empleo");
    } else if (empLength < 2 || isRent) {
      score += 5;
    }

    // Normalizar a 100 max
    score = Math.min(100, Math.max(0, score));

    let level: "BAJO" | "MEDIO" | "ALTO" = "BAJO";
    let color: "VERDE" | "AMARILLO" | "ROJO" = "VERDE";
    let recommendation = "";
    let alertRequired = false;

    if (score >= 70) {
      level = "ALTO";
      color = "ROJO";
      alertRequired = true;
      recommendation = "EMITIR ALERTA TEMPRANA: Exposición crítica al impago. Requerir co-garantía, restringir ampliaciones de crédito o programar contacto preventivo antes de 15 días.";
    } else if (score >= 40) {
      level = "MEDIO";
      color = "AMARILLO";
      alertRequired = false;
      recommendation = "MONITOREO PREVENTIVO: Perfil vulnerable. Configurar recordatorios automatizados de pago 5 días antes de cada vencimiento.";
    } else {
      level = "BAJO";
      color = "VERDE";
      alertRequired = false;
      recommendation = "RIESGO CONTROLADO: Solvencia crediticia saludable. Cliente apto para condiciones estándar o incremento de cupo.";
    }

    return {
      score,
      level,
      color,
      factors,
      recommendation,
      alertRequired,
    };
  }
}
