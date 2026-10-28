document.addEventListener("DOMContentLoaded", () => {
  fetchKpis();
  fetchAlerts();
  setupChat();

  document.getElementById("refresh-alerts-btn").addEventListener("click", fetchAlerts);
});

let gradesChart = null;
let intentChart = null;

async function fetchKpis() {
  try {
    const res = await fetch("/api/kpis");
    const data = await res.json();
    if (!data.success) return;

    const { kpis, gradeDistribution, intentDistribution } = data;

    // Render Metric Cards
    document.getElementById("kpi-exposure").textContent = `$${Number(kpis.total_exposure_usd).toLocaleString()} USD`;
    document.getElementById("kpi-records").textContent = `${Number(kpis.total_records).toLocaleString()} préstamos analizados`;
    document.getElementById("kpi-default-rate").textContent = `${kpis.default_rate_percentage}%`;
    document.getElementById("kpi-avg-loan").textContent = `$${Number(kpis.avg_loan_amount).toLocaleString()} USD`;
    document.getElementById("kpi-avg-income").textContent = `Ingreso medio: $${Number(kpis.avg_income).toLocaleString()}`;
    document.getElementById("kpi-historic-default").textContent = `${kpis.historic_default_percentage}%`;

    // Render Charts
    renderGradesChart(gradeDistribution);
    renderIntentChart(intentDistribution);
  } catch (err) {
    console.error("Error al cargar KPIs:", err);
  }
}

function renderGradesChart(data) {
  const ctx = document.getElementById("chart-grades").getContext("2d");
  const labels = data.map((d) => `Grado ${d.loan_grade}`);
  const values = data.map((d) => d.default_pct);

  if (gradesChart) gradesChart.destroy();
  gradesChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "% Tasa de Impago Observada",
          data: values,
          backgroundColor: ["#2ea043", "#48c774", "#f5d04a", "#ff9800", "#f85149", "#d73a49", "#8b0000"],
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: "#8b9bb4" },
          grid: { color: "#26333e" },
        },
        x: {
          ticks: { color: "#8b9bb4" },
          grid: { display: false },
        },
      },
      plugins: {
        legend: { labels: { color: "#f0f6fc" } },
      },
    },
  });
}

function renderIntentChart(data) {
  const ctx = document.getElementById("chart-intent").getContext("2d");
  const labels = data.map((d) => d.loan_intent);
  const counts = data.map((d) => d.count);

  if (intentChart) intentChart.destroy();
  intentChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          data: counts,
          backgroundColor: ["#25c9e8", "#f5d04a", "#f85149", "#a371f7", "#3fb950", "#58a6ff"],
          borderColor: "#151b22",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "right",
          labels: { color: "#f0f6fc", font: { size: 11 } },
        },
      },
    },
  });
}

async function fetchAlerts() {
  const tbody = document.getElementById("alerts-tbody");
  tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;">Cargando alertas desde Neon...</td></tr>';

  try {
    const res = await fetch("/api/alerts?limit=12");
    const data = await res.json();
    if (!data.success || !data.alerts) return;

    tbody.innerHTML = "";
    data.alerts.forEach((alert) => {
      const tr = document.createElement("tr");
      const evalData = alert.evaluation;
      const badgeClass = `badge-${evalData.color.toLowerCase()}`;

      tr.innerHTML = `
        <td><strong>#${alert.id}</strong></td>
        <td>${alert.person_age} años<br><small style="color:#8b9bb4">$${Number(alert.person_income).toLocaleString()}</small></td>
        <td>$${Number(alert.loan_amnt).toLocaleString()}<br><small style="color:#25c9e8">${alert.loan_intent}</small></td>
        <td><strong>${(Number(alert.loan_percent_income) * 100).toFixed(1)}%</strong></td>
        <td>Grado ${alert.loan_grade}</td>
        <td>${alert.cb_person_default_on_file === 'Y' ? '<span style="color:#f85149; font-weight:700">SÍ</span>' : 'No'}</td>
        <td><strong>${evalData.score} / 100</strong></td>
        <td><span class="badge ${badgeClass}">${evalData.level}</span></td>
        <td style="font-size:12px; color:#cbe6f7;">${evalData.recommendation}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Error al obtener alertas:", err);
    tbody.innerHTML = '<tr><td colspan="9" style="text-align:center; color:#f85149;">Error al conectar con la base de datos.</td></tr>';
  }
}

function setupChat() {
  const input = document.getElementById("chat-input");
  const sendBtn = document.getElementById("chat-send-btn");
  const messages = document.getElementById("chat-messages");

  async function handleSend() {
    const text = input.value.trim();
    if (!text) return;

    // Agregar mensaje usuario
    const userMsg = document.createElement("div");
    userMsg.className = "msg user";
    userMsg.textContent = text;
    messages.appendChild(userMsg);
    input.value = "";
    messages.scrollTop = messages.scrollHeight;

    // Llamar al endpoint del Agente
    try {
      const res = await fetch("/api/agent/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: text }),
      });
      const data = await res.json();

      const botMsg = document.createElement("div");
      botMsg.className = "msg bot";
      botMsg.textContent = data.answer || "No obtuve respuesta del agente.";
      messages.appendChild(botMsg);
      messages.scrollTop = messages.scrollHeight;
    } catch (err) {
      const botMsg = document.createElement("div");
      botMsg.className = "msg bot";
      botMsg.textContent = "Error al comunicar con el agente coordinador.";
      messages.appendChild(botMsg);
    }
  }

  sendBtn.addEventListener("click", handleSend);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleSend();
  });
}
