const API = "http://localhost:8000";

let provinceData = [];
let cellData = [];
let hourlyData = [];
let provinceChart = null;
let hourlyChart = null;

const $ = (id) => document.getElementById(id);

function showError(message) {
  const el = $("error");
  el.textContent = message;
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 5000);
}

function fmt(value) {
  if (value === null || value === undefined) return "—";
  const n = Number(value);
  return Number.isFinite(n) ? n.toLocaleString() : value;
}

async function get(path) {
  const response = await fetch(`${API}${path}`);
  if (!response.ok)
    throw new Error(`${response.status} ${response.statusText}`);
  return response.json();
}

async function loadOverview() {
  provinceData = (await get("/analytics/overview")).data;
  renderOverviewCards();
  renderProvinceChart();
  populateProvinceSelect();
}

function renderOverviewCards() {
  const totals = provinceData.reduce(
    (a, r) => {
      a.sms += Number(r.total_sms_in || 0) + Number(r.total_sms_out || 0);
      a.calls += Number(r.total_call_in || 0) + Number(r.total_call_out || 0);
      a.internet += Number(r.total_internet || 0);
      return a;
    },
    { sms: 0, calls: 0, internet: 0 },
  );

  $("overview-cards").innerHTML = `
    <div class="card"><div class="card-label">Provinces</div><div class="card-value">${fmt(provinceData.length)}</div></div>
    <div class="card"><div class="card-label">Total SMS</div><div class="card-value">${fmt(totals.sms)}</div></div>
    <div class="card"><div class="card-label">Total Calls</div><div class="card-value">${fmt(totals.calls)}</div></div>
    <div class="card"><div class="card-label">Internet Activity</div><div class="card-value">${fmt(totals.internet)}</div></div>
  `;
}

function renderProvinceChart() {
  const labels = provinceData.map((x) => x.provincename);
  const sms = provinceData.map(
    (x) => Number(x.total_sms_in || 0) + Number(x.total_sms_out || 0),
  );
  const calls = provinceData.map(
    (x) => Number(x.total_call_in || 0) + Number(x.total_call_out || 0),
  );
  const internet = provinceData.map((x) => Number(x.total_internet || 0));

  if (provinceChart) provinceChart.destroy();

  provinceChart = new Chart($("province-chart"), {
    type: "bar",
    data: {
      labels,
      datasets: [
        { label: "SMS", data: sms },
        { label: "Calls", data: calls },
        { label: "Internet", data: internet },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      scales: { y: { beginAtZero: true } },
    },
  });
}

async function loadCells() {
  cellData = (await get("/analytics/cells")).data;
  renderCells();
}

function renderCells() {
  const query = $("cell-search").value.trim().toLowerCase();
  const rows = cellData.filter((r) =>
    String(r.cellid).toLowerCase().includes(query),
  );

  $("cells-table").innerHTML = rows
    .map(
      (r) => `
    <tr>
      <td>${r.cellid}</td>
      <td>${fmt(r.total_sms)}</td>
      <td>${fmt(r.total_calls)}</td>
      <td>${fmt(r.total_internet)}</td>
      <td>${fmt(r.urban_vitality_index)}</td>
      <td>${r.land_use_category ?? "—"}</td>
      <td>${Number(r.shannon_entropy_diversity_index ?? 0).toFixed(3)}</td>
    </tr>
  `,
    )
    .join("");
}

async function loadHourly(province = "") {
  hourlyData = (
    await get(
      `/analytics/hourly${province ? `?province=${encodeURIComponent(province)}` : ""}`,
    )
  ).data;
  renderHourlyChart();
}

function renderHourlyChart() {
  const labels = hourlyData.map((x) => `${x.hour}:00`);
  const sms = hourlyData.map((x) => Number(x.total_sms || 0));
  const calls = hourlyData.map((x) => Number(x.total_calls || 0));
  const internet = hourlyData.map((x) => Number(x.total_internet || 0));

  if (hourlyChart) hourlyChart.destroy();

  hourlyChart = new Chart($("hourly-chart"), {
    type: "line",
    data: {
      labels,
      datasets: [
        { label: "SMS", data: sms, tension: 0.25 },
        { label: "Calls", data: calls, tension: 0.25 },
        { label: "Internet", data: internet, tension: 0.25 },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      scales: { y: { beginAtZero: true } },
    },
  });
}

function populateProvinceSelect() {
  $("province-select").innerHTML =
    `<option value="">All provinces</option>` +
    provinceData
      .map(
        (x) => `<option value="${x.provincename}">${x.provincename}</option>`,
      )
      .join("");
}

function switchSection(name) {
  document
    .querySelectorAll(".section")
    .forEach((s) => s.classList.remove("active"));
  document
    .querySelectorAll(".nav-item")
    .forEach((b) => b.classList.remove("active"));

  $(name).classList.add("active");
  document.querySelector(`[data-section="${name}"]`).classList.add("active");

  $("page-title").textContent = {
    overview: "Network Overview",
    cells: "Cell Analytics",
    hourly: "Hourly Activity",
  }[name];

  if (name === "cells" && cellData.length === 0)
    loadCells().catch((e) => showError(e.message));
  if (name === "hourly" && hourlyData.length === 0)
    loadHourly().catch((e) => showError(e.message));
}

const uploadModal = $("upload-modal");
const uploadForm = $("upload-form");
const uploadFile = $("upload-file");
const fileName = $("file-name");
const uploadStatus = $("upload-status");

function openUploadModal() {
  uploadModal.classList.remove("hidden");
  uploadStatus.className = "upload-status hidden";
  uploadStatus.textContent = "";
}

function closeUploadModal() {
  uploadModal.classList.add("hidden");
  uploadForm.reset();
  fileName.textContent = "Choose a CSV file";
}

$("upload-btn").addEventListener("click", openUploadModal);
$("close-upload").addEventListener("click", closeUploadModal);
$("cancel-upload").addEventListener("click", closeUploadModal);

uploadFile.addEventListener("change", () => {
  fileName.textContent = uploadFile.files[0]?.name || "Choose a CSV file";
});

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const file = uploadFile.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  uploadStatus.className = "upload-status";
  uploadStatus.textContent = "Uploading...";

  try {
    const response = await fetch(`${API}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.detail || `Upload failed (${response.status})`);
    }

    uploadStatus.className = "upload-status success";
    uploadStatus.textContent = data.message || "File uploaded successfully.";
    setTimeout(closeUploadModal, 1800);
  } catch (error) {
    uploadStatus.className = "upload-status failure";
    uploadStatus.textContent = error.message;
  }
});

document.querySelectorAll(".nav-item").forEach((btn) => {
  btn.addEventListener("click", () => switchSection(btn.dataset.section));
});

$("cell-search").addEventListener("input", renderCells);
$("province-select").addEventListener("change", (e) =>
  loadHourly(e.target.value).catch((err) => showError(err.message)),
);
$("refresh-btn").addEventListener("click", async () => {
  try {
    await loadOverview();
    if ($("cells").classList.contains("active")) await loadCells();
    if ($("hourly").classList.contains("active"))
      await loadHourly($("province-select").value);
  } catch (e) {
    showError(e.message);
  }
});

loadOverview().catch((e) =>
  showError(`Could not load analytics: ${e.message}`),
);
