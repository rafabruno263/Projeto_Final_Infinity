requireAdmin();
renderHeader();

const el = (id) => document.getElementById(id);

function clearForm() {
  el("id").value = "";
  el("tipo").value = "equipment";
  el("nome").value = "";
  el("descricao").value = "";
  el("status").value = "ativo";
  el("msgForm").textContent = "";
  el("msgForm").className = "";
}

async function loadList() {
  try {
    const items = await apiFetch("/resources");
    const tbody = el("tbody");
    tbody.innerHTML = "";
    items.forEach((r) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${r.id}</td>
        <td>${r.tipo}</td>
        <td>${r.nome}</td>
        <td>${r.status}</td>
        <td>
          <button data-edit="${r.id}">Editar</button>
          <button class="danger" data-del="${r.id}">Excluir</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    tbody.querySelectorAll("[data-edit]").forEach((btn) => {
      btn.addEventListener("click", () => editItem(parseInt(btn.dataset.edit, 10)));
    });
    tbody.querySelectorAll("[data-del]").forEach((btn) => {
      btn.addEventListener("click", () => delItem(parseInt(btn.dataset.del, 10)));
    });
  } catch (e) {
    el("msg").textContent = e.message;
  }
}

async function editItem(id) {
  const items = await apiFetch("/resources");
  const r = items.find(x => x.id === id);
  if (!r) return;

  el("id").value = r.id;
  el("tipo").value = r.tipo;
  el("nome").value = r.nome;
  el("descricao").value = r.descricao || "";
  el("status").value = r.status;
  el("msgForm").textContent = "Editando recurso " + r.id;
  el("msgForm").className = "success";
}

async function delItem(id) {
  if (!confirm("Excluir recurso " + id + "?")) return;
  try {
    await apiFetch(`/resources/${id}`, { method: "DELETE" });
    await loadList();
    clearForm();
  } catch (e) {
    alert(e.message);
  }
}

el("btnSalvar").addEventListener("click", async () => {
  const payload = {
    tipo: el("tipo").value,
    nome: el("nome").value.trim(),
    descricao: el("descricao").value.trim(),
    status: el("status").value.trim()
  };

  el("msgForm").textContent = "";
  el("msgForm").className = "";

  try {
    const id = el("id").value;
    if (id) {
      await apiFetch(`/resources/${id}`, { method: "PUT", body: JSON.stringify(payload) });
      el("msgForm").textContent = "Recurso atualizado.";
    } else {
      await apiFetch("/resources", { method: "POST", body: JSON.stringify(payload) });
      el("msgForm").textContent = "Recurso criado.";
    }
    el("msgForm").className = "success";
    await loadList();
    clearForm();
  } catch (e) {
    el("msgForm").textContent = e.message;
    el("msgForm").className = "error";
  }
});

el("btnLimpar").addEventListener("click", clearForm);

clearForm();
loadList();