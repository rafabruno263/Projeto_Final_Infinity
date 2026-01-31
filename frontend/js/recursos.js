requireLogin();
renderHeader();

function tipoLabel(t) {
  if (t === "equipment") return "Equipamento";
  if (t === "vehicle") return "Veículo";
  if (t === "security_device") return "Dispositivo de Segurança";
  return t;
}

(async function load() {
  try {
    const items = await apiFetch("/resources");
    const tbody = document.getElementById("tbody");
    tbody.innerHTML = "";
    items.forEach((r) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${r.id}</td>
        <td>${tipoLabel(r.tipo)}</td>
        <td>${r.nome}</td>
        <td>${r.status}</td>
        <td>${r.atualizado_em}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    document.getElementById("msg").textContent = e.message;
  }
})();