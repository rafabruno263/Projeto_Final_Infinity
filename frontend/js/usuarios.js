requireAdmin();
renderHeader();

const el = (id) => document.getElementById(id);

async function loadUsers() {
  try {
    const users = await apiFetch("/users");
    const tbody = el("tbody");
    tbody.innerHTML = "";
    users.forEach((u) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${u.id}</td><td>${u.nome}</td><td>${u.email}</td><td>${u.role}</td>`;
      tbody.appendChild(tr);
    });
  } catch (e) {
    el("msg").textContent = e.message;
  }
}

el("btnCriar").addEventListener("click", async () => {
  const payload = {
    nome: el("nome").value.trim(),
    email: el("email").value.trim(),
    senha: el("senha").value,
    role: el("role").value
  };

  el("msgForm").textContent = "";
  el("msgForm").className = "";

  try {
    await apiFetch("/users", { method: "POST", body: JSON.stringify(payload) });
    el("msgForm").textContent = "Usuário criado.";
    el("msgForm").className = "success";
    el("nome").value = "";
    el("email").value = "";
    el("senha").value = "";
    el("role").value = "employee";
    loadUsers();
  } catch (e) {
    el("msgForm").textContent = e.message;
    el("msgForm").className = "error";
  }
});

loadUsers();