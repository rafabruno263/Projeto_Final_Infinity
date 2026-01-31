requireLogin();
renderHeader();

(async function load() {
  try {
    const data = await apiFetch("/dashboard/summary");
    document.getElementById("totalRecursos").textContent = data.resources_total ?? 0;

    const by = data.resources_by_type || {};
    document.getElementById("qtdEquip").textContent = by.equipment ?? 0;
    document.getElementById("qtdVeic").textContent = by.vehicle ?? 0;
    document.getElementById("qtdSeg").textContent = by.security_device ?? 0;

    const tbody = document.getElementById("tbodyLogs");
    tbody.innerHTML = "";
    (data.recent_activity || []).forEach((l) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${l.data_hora}</td>
        <td>${l.usuario}</td>
        <td><span class="badge">${l.acao}</span></td>
        <td>${l.entidade}</td>
        <td>${l.entidade_id ?? ""}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    document.getElementById("msg").textContent = e.message;
  }
})();