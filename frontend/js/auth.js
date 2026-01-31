function requireLogin() {
  const token = getToken();
  if (!token) {
    window.location.href = "index.html";
    return;
  }
}

function requireAdmin() {
  requireLogin();
  const user = getUser();
  if (!user || user.role !== "security_admin") {
    window.location.href = "dashboard.html";
  }
}

function renderHeader(active) {
  const user = getUser();
  const isAdmin = user && user.role === "security_admin";

  const links = [];
  links.push(`<a href="dashboard.html">Dashboard</a>`);
  links.push(`<a href="recursos.html">Recursos</a>`);
  if (isAdmin) {
    links.push(`<a href="gerenciar_recursos.html">Gerenciar Recursos</a>`);
    links.push(`<a href="usuarios.html">Usuários</a>`);
  }
  links.push(`<a href="#" id="logoutLink">Sair</a>`);

  document.getElementById("headerLinks").innerHTML = links.join("");

  const info = user ? `${user.nome} (${user.role})` : "";
  document.getElementById("headerUser").textContent = info;

  document.getElementById("logoutLink").addEventListener("click", (e) => {
    e.preventDefault();
    clearSession();
    window.location.href = "index.html";
  });
}