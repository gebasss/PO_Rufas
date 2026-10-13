"use strict";

/* ------------------------------------------------------------------ utilidades */
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const nf = (v, d = 2) => (v == null || Number.isNaN(v) ? "—" : Number(v).toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d }));
const usd = (v, d = 0) => (v == null ? "—" : "US$ " + nf(v, d));
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const PALETTE = ["#1f6f4a", "#d9822b", "#3a78b5", "#b3463f", "#7a5aa6", "#2f9aa0", "#9c8a2f", "#c0568a", "#5d6b64", "#8ab04a", "#4a5fa8", "#a8643a"];

async function api(path, body) {
  const res = await fetch(path, body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

const charts = {};
function chart(id, config) {
  if (charts[id]) charts[id].destroy();
  const style = getComputedStyle(document.documentElement);
  Chart.defaults.color = style.getPropertyValue("--muted").trim() || "#5e6a63";
  Chart.defaults.borderColor = style.getPropertyValue("--line").trim() || "#dde2dd";
  config.options = Object.assign({ responsive: true, maintainAspectRatio: false, animation: { duration: 250 } }, config.options || {});
  charts[id] = new Chart($("#" + id), config);
  return charts[id];
}

async function pollJob(job, bar) {
  const box = $(bar);
  box.classList.remove("hidden");
  for (;;) {
    const j = await api("/api/jobs/" + job.id);
    const pct = j.total ? (100 * j.done) / j.total : 4;
    $("div", box).style.width = pct + "%";
    $("span", box).textContent = j.status === "queued" ? "na fila…" : j.total ? `${j.done}/${j.total} simulações do RuFaS` : "simulando no RuFaS…";
    if (j.status === "done") { box.classList.add("hidden"); return j.result; }
    if (j.status === "error") { box.classList.add("hidden"); throw new Error(j.error); }
    await new Promise((r) => setTimeout(r, 1500));
  }
}

/* ------------------------------------------------------------------ abas */
$$(".tab").forEach((btn) => btn.addEventListener("click", () => {
  $$(".tab").forEach((b) => b.classList.toggle("active", b === btn));
  $$(".panel").forEach((p) => p.classList.toggle("active", p.id === "tab-" + btn.dataset.tab));
  if (btn.dataset.tab === "sens") buildSensFactors();
  if (btn.dataset.tab === "curve") drawCurve();
}));

/* ------------------------------------------------------------------ 1. exercício do quadro */
const toy = {
  foods: [
    { name: "Arroz", cost: 1.5, carb: 0.77, prot: 0.08 },
    { name: "Milho", cost: 2.23, carb: 0.66, prot: 0.14 },
  ],
  bounds: [
    { name: "Carboidrato", min: 6.0, max: 9.5 },
    { name: "Proteína", min: 0.9, max: 1.6 },
  ],
};

function renderToyTables() {
  const fb = $("#toy-foods tbody");
  fb.innerHTML = toy.foods.map((f, i) => `<tr>
    <td><input data-i="${i}" data-k="name" value="${esc(f.name)}"></td>
    <td><input type="number" step="0.01" data-i="${i}" data-k="cost" value="${f.cost}"></td>
    <td><input type="number" step="0.01" data-i="${i}" data-k="carb" value="${f.carb}"></td>
    <td><input type="number" step="0.01" data-i="${i}" data-k="prot" value="${f.prot}"></td>
    <td>${toy.foods.length > 2 ? `<button class="x" data-del="${i}" title="remover">×</button>` : ""}</td></tr>`).join("");
  $$("input", fb).forEach((inp) => inp.addEventListener("input", () => {
    const f = toy.foods[inp.dataset.i];
    f[inp.dataset.k] = inp.dataset.k === "name" ? inp.value : parseFloat(inp.value);
  }));
  $$("[data-del]", fb).forEach((b) => b.addEventListener("click", () => { toy.foods.splice(+b.dataset.del, 1); renderToyTables(); renderToyFactors(); }));
  const bb = $("#toy-bounds tbody");
  bb.innerHTML = toy.bounds.map((b, i) => `<tr><td>${esc(b.name)}</td>
    <td><input type="number" step="0.1" data-i="${i}" data-k="min" value="${b.min}"></td>
    <td><input type="number" step="0.1" data-i="${i}" data-k="max" value="${b.max}"></td></tr>`).join("");
  $$("input", bb).forEach((inp) => inp.addEventListener("input", () => { toy.bounds[inp.dataset.i][inp.dataset.k] = parseFloat(inp.value); }));
}

function toyPayload() {
  return {
    foods: toy.foods.map((f) => ({ name: f.name, cost: f.cost, nutrients: { "Carboidrato": f.carb, "Proteína": f.prot } })),
    bounds: Object.fromEntries(toy.bounds.map((b) => [b.name, { min: b.min, max: b.max }])),
  };
}

$("#toy-add-food").addEventListener("click", () => { toy.foods.push({ name: "Alimento " + (toy.foods.length + 1), cost: 1, carb: 0.5, prot: 0.1 }); renderToyTables(); renderToyFactors(); });

$("#toy-solve").addEventListener("click", async () => {
  $("#toy-status").textContent = "resolvendo…";
  try {
    const r = await api("/api/toy", toyPayload());
    $("#toy-status").textContent = "";
    renderToyResult(r);
  } catch (e) { $("#toy-status").innerHTML = `<span class="err">${esc(e.message)}</span>`; }
});

function renderToyResult(r) {
  const box = $("#toy-result");
  if (!r.feasible) {
    box.innerHTML = `<p class="bad"><b>Sem solução viável.</b> Os limites mínimo e máximo são incompatíveis com os alimentos disponíveis.</p>`;
    if (charts["toy-chart"]) { charts["toy-chart"].destroy(); delete charts["toy-chart"]; }
    return;
  }
  const rows = toy.foods.map((f) => `<tr><td>${esc(f.name)}</td><td class="num">${nf(r.amounts[f.name], 3)} kg</td><td class="num">${usd(r.amounts[f.name] * f.cost, 2)}</td></tr>`).join("");
  const nut = toy.bounds.map((b) => {
    const t = r.nutrient_totals[b.name];
    const lim = (k) => Math.abs(t - b[k]) < 1e-6 ? "ativo" : "folga";
    const shadow = r.shadow_prices[b.name + "_min"];
    return `<tr><td>${esc(b.name)}</td><td class="num">${nf(t, 3)} kg</td><td class="num">${nf(b.min, 2)} – ${nf(b.max, 2)}</td>
      <td>${lim("min") === "ativo" ? "mínimo ativo" : lim("max") === "ativo" ? "máximo ativo" : "folga"}</td>
      <td class="num">${shadow ? usd(shadow, 2) + "/kg" : "—"}</td></tr>`;
  }).join("");
  box.innerHTML = `<div class="kpis"><div class="kpi main"><div class="v">${usd(r.cost, 2)}</div><div class="l">custo mínimo por dia</div></div></div>
    <table><thead><tr><th>Alimento</th><th class="num">Quantidade</th><th class="num">Custo</th></tr></thead><tbody>${rows}</tbody></table>
    <h3>Nutrientes</h3>
    <table><thead><tr><th>Nutriente</th><th class="num">Total</th><th class="num">Faixa</th><th>Restrição</th><th class="num">Preço-sombra (mín.)</th></tr></thead><tbody>${nut}</tbody></table>
    <p class="hint">Preço-sombra: quanto o custo ótimo aumenta se o mínimo do nutriente subir 1 kg.</p>`;
  chart("toy-chart", {
    type: "bar",
    data: { labels: toy.foods.map((f) => f.name), datasets: [{ label: "kg por dia", data: toy.foods.map((f) => r.amounts[f.name]), backgroundColor: PALETTE }] },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, title: { display: true, text: "kg/dia" } } } },
  });
}

function toyTargets() {
  return [...toy.foods.map((f) => ({ v: "cost:" + f.name, l: "Custo — " + f.name })), ...toy.bounds.flatMap((b) => [{ v: "min:" + b.name, l: "Mínimo — " + b.name }, { v: "max:" + b.name, l: "Máximo — " + b.name }])];
}
const TOY_FACTOR_DEFAULTS = [["cost:Arroz", 1.0, 2.0, 3], ["cost:Milho", 1.8, 2.6, 3]];
function renderToyFactors() {
  const box = $("#toy-factors");
  const prev = $$(".toy-factor", box).map((d) => d.querySelector("select").value);
  box.innerHTML = [0, 1].map((i) => {
    const d = TOY_FACTOR_DEFAULTS[i];
    const opts = toyTargets().map((t) => `<option value="${esc(t.v)}" ${(prev[i] || d[0]) === t.v ? "selected" : ""}>${esc(t.l)}</option>`).join("");
    return `<div class="toy-factor"><label class="field inline" style="width:210px">Fator ${i + 1}<select>${opts}</select></label>
      <label class="field inline" style="width:90px">De <input type="number" step="0.1" value="${d[1]}"></label>
      <label class="field inline" style="width:90px">Até <input type="number" step="0.1" value="${d[2]}"></label>
      <label class="field inline" style="width:80px">Níveis <input type="number" min="2" max="9" value="${d[3]}"></label></div>`;
  }).join("");
}

$("#toy-sens").addEventListener("click", async () => {
  const factors = $$(".toy-factor").map((d) => {
    const [sel, lo, hi, n] = [d.querySelector("select"), ...d.querySelectorAll("input")];
    return { target: sel.value, low: parseFloat(lo.value), high: parseFloat(hi.value), n: parseInt(n.value, 10) };
  });
  if (factors[0].target === factors[1].target) { $("#toy-sens-status").textContent = "escolha dois fatores diferentes"; return; }
  $("#toy-sens-status").textContent = "calculando…";
  try {
    const r = await api("/api/toy/sensitivity", { problem: toyPayload(), factors });
    $("#toy-sens-status").textContent = `${r.rows.length} cenários`;
    const vals = r.rows.map((x) => x.Res).filter((v) => v != null);
    const [lo, hi] = [Math.min(...vals), Math.max(...vals)];
    const label = (c) => { const [k, n] = c.split(":"); return { cost: "Custo ", min: "Mín. ", max: "Máx. " }[k] + n; };
    const head = r.columns.map((c) => `<th class="num">${c === "Res" ? "Res (US$/dia)" : esc(label(c))}</th>`).join("");
    const body = r.rows.map((x) => `<tr><td><b>${x.cenario}</b></td>${r.columns.map((c) => {
      if (c !== "Res") return `<td class="num">${nf(x[c], 2)}</td>`;
      if (x.Res == null) return `<td class="num bad">inviável</td>`;
      const t = hi === lo ? 0 : (x.Res - lo) / (hi - lo);
      return `<td class="num heat" style="background:color-mix(in srgb, var(--accent) ${Math.round(70 - 60 * t)}%, var(--card))"><b>${nf(x.Res, 2)}</b></td>`;
    }).join("")}<td>${Object.entries(x.amounts).map(([k, v]) => `${esc(k)} ${nf(v, 2)} kg`).join(" · ")}</td></tr>`).join("");
    $("#toy-sens-table").innerHTML = `<table><thead><tr><th></th>${head}<th>Dieta ótima</th></tr></thead><tbody>${body}</tbody></table>`;
  } catch (e) { $("#toy-sens-status").innerHTML = `<span class="err">${esc(e.message)}</span>`; }
});

/* ------------------------------------------------------------------ 2. vaca leiteira (RuFaS) */
const state = { feeds: [], byId: {}, defaults: { milk_price: 0.45, prices: {} }, selected: new Map(), lastSim: null };
const FALLBACK_PRICE = { Forage: 0.12, Conc: 0.35, Mineral: 0.15 };
const PRESET_QUADRO = [50, 110, 44, 167, 138, 230, 23];
const PRESET_WIDE = [50, 51, 110, 104, 95, 44, 47, 138, 167, 164, 169, 58, 193, 194, 24, 1, 230, 23];
const feedName = (f) => (f.description && f.description.toLowerCase() !== "no" ? `${f.name} — ${f.description}` : f.name);
const shortName = (f) => feedName(f).replace(/\s+/g, " ").slice(0, 38);

function priceOf(f) { return state.defaults.prices[f.id] ?? f.default_price ?? FALLBACK_PRICE[f.kind] ?? 0.3; }

function renderFeedList() {
  const q = $("#feed-search").value.trim().toLowerCase();
  const list = state.feeds.filter((f) => !q || feedName(f).toLowerCase().includes(q) || f.kind.toLowerCase().includes(q)).slice(0, 80);
  $("#feed-list").innerHTML = list.map((f) => `<div class="feed-item" data-id="${f.id}">
    <input type="checkbox" ${state.selected.has(f.id) ? "checked" : ""} tabindex="-1"><span>${esc(feedName(f))}</span>
    <span class="tag">${esc(f.kind)} · PB ${nf(f.cp, 0)}% · FDN ${nf(f.ndf, 0)}%</span></div>`).join("") || `<div class="feed-item">nenhum resultado</div>`;
  $$(".feed-item[data-id]").forEach((el) => el.addEventListener("click", () => toggleFeed(+el.dataset.id)));
}

function toggleFeed(id) {
  if (state.selected.has(id)) state.selected.delete(id);
  else { const f = state.byId[id]; state.selected.set(id, { price: priceOf(f), min: 0, max: f.default_max ?? 100 }); }
  renderFeedList(); renderSelected();
}

function setSelection(ids) {
  state.selected = new Map(ids.filter((i) => state.byId[i]).map((i) => [i, { price: priceOf(state.byId[i]), min: 0, max: state.byId[i].default_max ?? 100 }]));
  renderFeedList(); renderSelected();
}

function renderSelected() {
  const box = $("#feed-selected");
  if (!state.selected.size) { box.innerHTML = `<p class="hint">Nenhum alimento selecionado.</p>`; return; }
  box.innerHTML = `<div class="sel head"><span>Alimento</span><span>US$/kg MS</span><span>mín kg</span><span>máx kg</span><span></span></div>` +
    [...state.selected].map(([id, s]) => `<div class="sel" data-id="${id}"><span title="${esc(feedName(state.byId[id]))}">${esc(shortName(state.byId[id]))}</span>
      <input type="number" step="0.01" min="0" data-k="price" value="${s.price}"><input type="number" step="0.1" min="0" data-k="min" value="${s.min}">
      <input type="number" step="0.1" min="0" data-k="max" value="${s.max}"><button class="x" data-rm="${id}">×</button></div>`).join("");
  $$(".sel[data-id] input", box).forEach((inp) => inp.addEventListener("input", () => { state.selected.get(+inp.closest(".sel").dataset.id)[inp.dataset.k] = parseFloat(inp.value); }));
  $$("[data-rm]", box).forEach((b) => b.addEventListener("click", () => toggleFeed(+b.dataset.rm)));
}

$("#feed-search").addEventListener("input", renderFeedList);
$("#cow-preset-quadro").addEventListener("click", () => setSelection(PRESET_QUADRO));
$("#cow-preset-wide").addEventListener("click", () => setSelection(PRESET_WIDE));

function simParams() {
  const prices = {}, limits = {};
  state.selected.forEach((s, id) => { prices[id] = s.price; limits[id] = [s.min, s.max]; });
  return { feeds: [...state.selected.keys()], prices, limits, milk_price: parseFloat($("#cow-milk").value), years: +$("#cow-years").value, max_milk_reduction: parseFloat($("#cow-maxred").value) };
}

$("#cow-run").addEventListener("click", async () => {
  if (state.selected.size < 3) { alert("Selecione pelo menos 3 alimentos (volumoso, concentrado e mineral)."); return; }
  const btn = $("#cow-run"); btn.disabled = true;
  $("#cow-empty").classList.remove("hidden"); $("#cow-empty").textContent = "Simulando com o RuFaS…";
  try {
    const job = await api("/api/jobs/simulate", simParams());
    const result = await pollJob(job, "#cow-progress");
    state.lastSim = result;
    renderCow(result);
  } catch (e) {
    $("#cow-empty").classList.remove("hidden");
    $("#cow-empty").innerHTML = `<span class="err">${esc(e.message)}</span>`;
    $("#cow-out").classList.add("hidden");
  } finally { btn.disabled = false; }
});

function feedColor(ids, id) { return PALETTE[ids.indexOf(String(id)) % PALETTE.length]; }

function renderCow(r) {
  $("#cow-empty").classList.add("hidden"); $("#cow-out").classList.remove("hidden");
  const s = r.summary;
  const avgCows = r.daily.milking_cows.reduce((a, b) => a + b, 0) / r.daily.milking_cows.length;
  const milkPerCow = s.leite_kg / (avgCows * r.daily.day.length);
  $("#cow-kpis").innerHTML = [
    ["Margem sobre custo de alimentação", usd(s.margem), "main"], ["Receita do leite", usd(s.receita)], ["Custo de alimentação (rebanho)", usd(s.custo_alimentacao)],
    ["Custo da ração, vaca em lactação", usd(s.custo_vaca_dia, 2) + "/dia"], ["Leite por vaca", nf(milkPerCow, 1) + " kg/dia"], ["Leite total", nf(s.leite_kg / 1000, 0) + " t"],
    ...(s.reducao_leite > 0.005 ? [["Leite perdido por ração insuficiente", "−" + nf(s.reducao_leite, 2) + " kg/vaca/dia", "warn"]] : []),
  ].map(([l, v, c]) => `<div class="kpi ${c || ""}"><div class="v">${v}</div><div class="l">${l}</div></div>`).join("");

  const ids = r.feeds.map((f) => String(f.id));
  const labels = r.intervals.day.map((d) => d);
  const nameById = Object.fromEntries(r.feeds.map((f) => [String(f.id), f.label]));
  chart("ch-ration", {
    type: "bar",
    data: { labels: labels.map((d) => "dia " + d), datasets: ids.filter((id) => r.intervals.ration.some((x) => (x[id] || 0) > 1e-3)).map((id) => ({
      label: nameById[id].slice(0, 36), data: r.intervals.ration.map((x) => x[id] || 0), backgroundColor: feedColor(ids, id) })) },
    options: { scales: { x: { stacked: true }, y: { stacked: true, title: { display: true, text: "kg MS/vaca/dia" } } }, plugins: { legend: { position: "bottom", labels: { boxWidth: 12 } } } },
  });

  const total = Object.values(r.average_ration).reduce((a, b) => a + b, 0);
  const rows = ids.filter((id) => (r.average_ration[id] || 0) > 1e-3).sort((a, b) => r.average_ration[b] - r.average_ration[a]).map((id) => {
    const kg = r.average_ration[id], price = (r.feeds.find((f) => String(f.id) === id) || {}).price;
    return `<tr><td><span class="swatch" style="background:${feedColor(ids, id)}"></span>${esc(nameById[id])}</td><td class="num">${nf(kg, 2)}</td><td class="num">${nf(100 * kg / total, 1)}%</td><td class="num">${nf(kg * price, 2)}</td></tr>`;
  }).join("");
  $("#cow-ration-table").innerHTML = `<table><thead><tr><th>Alimento</th><th class="num">kg MS/dia</th><th class="num">% MS</th><th class="num">US$/dia</th></tr></thead><tbody>${rows}
    <tr><td><b>Total</b></td><td class="num"><b>${nf(total, 2)}</b></td><td class="num">100%</td><td class="num"><b>${nf(s.custo_vaca_dia, 2)}</b></td></tr></tbody></table>`;

  const q = r.intervals.requirements;
  chart("ch-req", {
    type: "line",
    data: { labels: labels.map((d) => "dia " + d), datasets: [
      { label: "NEL exigida (Mcal/dia)", data: q.map((x) => x.NEl_requirement), borderColor: PALETTE[0], yAxisID: "y", tension: 0.25 },
      { label: "DMI estimado (kg/dia)", data: q.map((x) => x.DMIest_requirement), borderColor: PALETTE[1], yAxisID: "y", tension: 0.25 },
      { label: "Proteína metabolizável (g/dia)", data: q.map((x) => x.MP_requirement), borderColor: PALETTE[2], yAxisID: "y2", tension: 0.25 },
    ] },
    options: { scales: { y: { title: { display: true, text: "Mcal ou kg" } }, y2: { position: "right", grid: { drawOnChartArea: false }, title: { display: true, text: "g" } } }, plugins: { legend: { position: "bottom", labels: { boxWidth: 12 } } } },
  });

  chart("ch-milk", {
    type: "line",
    data: { labels: r.daily.day, datasets: [
      { label: "Leite do rebanho (kg/dia)", data: r.daily.milk_kg, borderColor: PALETTE[0], pointRadius: 0, yAxisID: "y" },
      { label: "Vacas em lactação", data: r.daily.milking_cows, borderColor: PALETTE[3], pointRadius: 0, yAxisID: "y2", borderDash: [4, 3] },
    ] },
    options: { scales: { x: { ticks: { maxTicksLimit: 12 }, title: { display: true, text: "dia da simulação" } }, y: { title: { display: true, text: "kg/dia" } }, y2: { position: "right", grid: { drawOnChartArea: false } } }, plugins: { legend: { position: "bottom", labels: { boxWidth: 12 } } } },
  });
}

/* ------------------------------------------------------------------ 3. curva de lactação */
let curveData = null;
const wood = (t, p) => p.l * Math.pow(t, p.m) * Math.exp(-p.n * t);
const parityLabel = { 1: "1ª lactação", 2: "2ª lactação", 3: "3ª ou mais" };

const milestonePlugin = {
  id: "milestones",
  afterDatasetsDraw(c) {
    const m = c.options.plugins.milestones; if (!m) return;
    const { ctx, chartArea: a, scales: { x } } = c;
    const px = (d) => x.getPixelForValue(d);
    ctx.save();
    ctx.fillStyle = "rgba(31,111,74,0.10)"; ctx.fillRect(px(m.pev), a.top, px(Math.min(m.calving, x.max)) - px(m.pev), a.bottom - a.top);
    [[m.pev, "PEV", "#1f6f4a"], [m.dry, "secagem", "#a4571b"], [m.calving, "parto", "#b3342e"]].forEach(([d, text, color]) => {
      if (d > x.max) return;
      ctx.strokeStyle = color; ctx.setLineDash([5, 4]); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(px(d), a.top); ctx.lineTo(px(d), a.bottom); ctx.stroke();
      ctx.setLineDash([]); ctx.fillStyle = color; ctx.font = "12px system-ui"; ctx.fillText(`${text} (${d} d)`, px(d) + 4, a.top + 13);
    });
    const y = a.bottom - 14;
    ctx.strokeStyle = "#1f6f4a"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(px(m.pev), y); ctx.lineTo(px(Math.min(m.calving, x.max)), y); ctx.stroke();
    ctx.fillStyle = "#1f6f4a"; ctx.textAlign = "center"; ctx.fillText(`gestação ${m.gest} d`, (px(m.pev) + px(Math.min(m.calving, x.max))) / 2, y - 4);
    ctx.restore();
  },
};

async function drawCurve() {
  if (!curveData) curveData = await api("/api/lactation");
  const w = state.lastSim ? state.lastSim.lactation.wood : curveData.wood;
  const fromRufas = state.lastSim ? state.lastSim.lactation.wood_from_rufas : false;
  $("#curve-src").textContent = fromRufas ? "parâmetros calibrados pela simulação RuFaS" : "parâmetros de referência (rode a aba 2 para usar os da simulação)";
  const pev = +$("#curve-pev").value, gest = +$("#curve-gest").value, dry = +$("#curve-dry").value;
  const calving = pev + gest, dryDay = calving - dry;
  const maxDay = Math.max(330, calving + 15);
  const days = Array.from({ length: maxDay }, (_, i) => i + 1);
  chart("ch-curve", {
    type: "line",
    data: { datasets: Object.entries(w).map(([parity, p], i) => ({ label: parityLabel[parity] || "paridade " + parity, data: days.map((d) => ({ x: d, y: wood(d, p) })), borderColor: PALETTE[[0, 1, 2][i % 3]], pointRadius: 0, borderWidth: 2 })) },
    options: { parsing: false, scales: { x: { type: "linear", min: 0, max: maxDay, title: { display: true, text: "dias em lactação" } }, y: { beginAtZero: true, title: { display: true, text: "produção (kg/vaca/dia)" } } },
      plugins: { milestones: { pev, calving, dry: dryDay, gest }, legend: { position: "bottom" } } },
    plugins: [milestonePlugin],
  });
  $("#curve-facts").innerHTML = Object.entries(w).map(([parity, p]) => {
    let peak = [1, 0], total = 0;
    for (let d = 1; d <= 305; d++) { const y = wood(d, p); total += y; if (y > peak[1]) peak = [d, y]; }
    return `<div class="kpi"><div class="v">${nf(peak[1], 1)} kg</div><div class="l">${parityLabel[parity] || parity}: pico no dia ${peak[0]} · ${nf(total / 1000, 1)} t em 305 d</div></div>`;
  }).join("");
}
["#curve-pev", "#curve-gest", "#curve-dry"].forEach((s) => $(s).addEventListener("input", drawCurve));

/* ------------------------------------------------------------------ 4. sensibilidade (RuFaS) */
function buildSensFactors() {
  const box = $("#sens-factors");
  const prev = {};
  $$(".sens-row", box).forEach((r) => { prev[r.dataset.key] = [...r.querySelectorAll("input")].map((i) => i.type === "checkbox" ? i.checked : i.value); });
  const rows = [...state.selected].map(([id, s]) => ({ key: String(id), label: shortName(state.byId[id]), lo: +(s.price * 0.5).toFixed(3), hi: +(s.price * 1.5).toFixed(3), on: [138, 44].includes(id) }));
  const milk = parseFloat($("#cow-milk").value) || 0.45;
  rows.push({ key: "milk_price", label: "Preço do leite (US$/kg)", lo: +(milk * 0.8).toFixed(3), hi: +(milk * 1.2).toFixed(3), on: true });
  if (!state.selected.size) { box.innerHTML = `<p class="hint">Selecione alimentos na aba 2 primeiro.</p>`; updateEstimate(); return; }
  box.innerHTML = rows.map((r) => {
    const p = prev[r.key] || [r.on, r.lo, r.hi];
    return `<div class="sens-row" data-key="${r.key}" data-label="${esc(r.label)}" style="display:grid;grid-template-columns:auto 1fr 64px 64px;gap:6px;align-items:center;margin:6px 0;font-size:13px">
      <input type="checkbox" ${p[0] ? "checked" : ""}><span>${esc(r.label)}</span><input type="number" step="0.01" value="${p[1]}" title="mínimo"><input type="number" step="0.01" value="${p[2]}" title="máximo"></div>`;
  }).join("");
  $$("input", box).forEach((i) => i.addEventListener("input", updateEstimate));
  updateEstimate();
}

function sensFactors() {
  return $$(".sens-row").filter((r) => r.querySelector("input[type=checkbox]").checked).map((r) => {
    const [, lo, hi] = r.querySelectorAll("input");
    return { key: r.dataset.key, label: r.dataset.label, low: parseFloat(lo.value), high: parseFloat(hi.value) };
  });
}

function updateEstimate() {
  const f = sensFactors(), n = +$("#sens-n").value || 2, method = $("#sens-method").value;
  const feedF = f.filter((x) => x.key !== "milk_price").length;
  const points = f.length ? (method === "grid" ? Math.pow(n, f.length) : n) : 0;
  const sims = f.length ? (method === "grid" ? Math.pow(n, feedF) : n) : 0;
  $("#sens-estimate").textContent = f.length ? `${points} cenários, até ${sims} simulações do RuFaS (~${Math.ceil(sims * 17 / 60)} min).` : "Marque ao menos um fator.";
  $("#sens-run").disabled = !f.length;
}
$("#sens-n").addEventListener("input", updateEstimate);
$("#sens-method").addEventListener("change", updateEstimate);

$("#sens-run").addEventListener("click", async () => {
  const btn = $("#sens-run"); btn.disabled = true;
  try {
    const job = await api("/api/jobs/sensitivity", { ...simParams(), factors: sensFactors(), method: $("#sens-method").value, n: +$("#sens-n").value });
    $("#sens-empty").textContent = "Rodando a análise no RuFaS…";
    const r = await pollJob(job, "#sens-progress");
    renderSens(r);
  } catch (e) {
    $("#sens-empty").classList.remove("hidden"); $("#sens-empty").innerHTML = `<span class="err">${esc(e.message)}</span>`; $("#sens-out").classList.add("hidden");
  } finally { btn.disabled = false; }
});

function renderSens(r) {
  $("#sens-empty").classList.add("hidden"); $("#sens-out").classList.remove("hidden");
  const names = Object.fromEntries(r.feeds.map((f) => [String(f.id), f.label.slice(0, 22)]));
  const vals = r.rows.map((x) => x.Res).filter((v) => v != null);
  const [lo, hi] = [Math.min(...vals), Math.max(...vals)];
  const head = r.columns.map((c) => `<th class="num">${esc(c === "Res" ? "Res = margem (US$)" : c)}</th>`).join("");
  const body = r.rows.map((x) => `<tr><td><b>${x.cenario}</b></td>${r.columns.map((c) => {
    if (c !== "Res") return `<td class="num">${nf(x[c], 3)}</td>`;
    if (x.Res == null) return `<td class="num bad" title="${esc(x.erro || "")}">falhou</td>`;
    const t = hi === lo ? 1 : (x.Res - lo) / (hi - lo);
    return `<td class="num heat" style="background:color-mix(in srgb, var(--accent) ${Math.round(10 + 60 * t)}%, var(--card))"><b>${nf(x.Res, 0)}</b></td>`;
  }).join("")}<td class="num">${nf(x.custo_vaca_dia, 2)}</td><td class="num">${x.reducao_leite > 0.005 ? "−" + nf(x.reducao_leite, 2) : "—"}</td><td>${x.ration ? Object.entries(x.ration).sort((a, b) => b[1] - a[1]).slice(0, 4).map(([k, v]) => `${esc(names[k] || k)} ${nf(v, 1)}`).join(" · ") : esc(x.erro || "")}</td></tr>`).join("");
  $("#sens-table").innerHTML = `<table><thead><tr><th></th>${head}<th class="num">US$/vaca/dia</th><th class="num">Leite perdido (kg/vaca/dia)</th><th>Ração (kg MS/vaca/dia)</th></tr></thead><tbody>${body}</tbody></table>`;

  const ef = r.effects.filter((e) => e.spearman != null);
  chart("ch-effects", {
    type: "bar", data: { labels: ef.map((e) => e.fator.slice(0, 26)), datasets: [{ label: "Spearman", data: ef.map((e) => e.spearman), backgroundColor: ef.map((e) => (e.spearman >= 0 ? PALETTE[0] : PALETTE[3])) }] },
    options: { indexAxis: "y", scales: { x: { min: -1, max: 1 } }, plugins: { legend: { display: false } } },
  });
  const ok = r.rows.filter((x) => x.Res != null);
  chart("ch-sens", {
    type: "bar", data: { labels: ok.map((x) => x.cenario), datasets: [{ label: "Margem (US$)", data: ok.map((x) => x.Res), backgroundColor: PALETTE[0] }] },
    options: { plugins: { legend: { display: false } }, scales: { y: { title: { display: true, text: "US$" } } } },
  });
}

/* ------------------------------------------------------------------ início */
(async function init() {
  renderToyTables(); renderToyFactors();
  try {
    [state.feeds, state.defaults] = await Promise.all([api("/api/feeds"), api("/api/defaults")]);
    state.byId = Object.fromEntries(state.feeds.map((f) => [f.id, f]));
    $("#cow-milk").value = state.defaults.milk_price;
    setSelection(PRESET_QUADRO);
    $("#conn").textContent = `conectado · ${state.feeds.length} alimentos NRC`; $("#conn").classList.add("ok");
  } catch (e) {
    $("#conn").textContent = "sem conexão com o servidor"; $("#conn").classList.add("bad");
  }
})();
