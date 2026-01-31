Claro — aqui está **tudo em um único bloco** pronto pra você **copiar e colar direto** no README do GitHub:

```md
# Projeto Final – Sistema de Segurança e Gestão de Recursos (Indústrias Wayne)

Aplicação web **full stack** desenvolvida com:
- **Frontend:** HTML, CSS e JavaScript (puro)
- **Backend:** Python (Flask)
- **Banco:** SQLite

O sistema atende aos requisitos do projeto:
1) **Controle de acesso** (autenticação e autorização por perfis)  
2) **Gestão de recursos** (equipamentos, veículos e dispositivos de segurança)  
3) **Dashboard** com visualização de dados e atividades recentes  

---

## Funcionalidades

### 1) Autenticação e Autorização (Controle de Acesso)
- Login via email e senha
- Perfis de usuário (roles):
  - `employee` (funcionário)
  - `manager` (gerente)
  - `security_admin` (administrador de segurança)
- Restrições:
  - Páginas e endpoints do backend são protegidos por token
  - Apenas `security_admin` acessa as páginas e rotas de gerenciamento

### 2) Gestão de Recursos
Recursos suportados:
- `equipment` (equipamentos)
- `vehicle` (veículos)
- `security_device` (dispositivos de segurança)

Permissões:
- `employee` e `manager`: **somente leitura** (lista)
- `security_admin`: **CRUD completo** (criar, editar, excluir)

### 3) Dashboard
Exibe:
- Total de recursos
- Quantidade de recursos por tipo
- Atividades recentes (log de ações):
  - LOGIN
  - CREATE_RESOURCE, UPDATE_RESOURCE, DELETE_RESOURCE
  - CREATE_USER

---

## Estrutura do Projeto

```

projeto-wayne/
backend/
app.py
db.py
auth.py
requirements.txt
wayne.db (gerado automaticamente)
frontend/
index.html
dashboard.html
recursos.html
gerenciar_recursos.html
usuarios.html
css/
style.css
js/
api.js
auth.js
dashboard.js
recursos.js
gerenciar_recursos.js
usuarios.js

````

---

## Requisitos de Ambiente
- **Python 3.10+**
- Navegador (Chrome/Edge/Firefox)
- (Opcional) VSCode + extensão **Live Server** para servir o frontend

---

## Como Executar

### 1) Backend (Flask)
Abra o terminal na pasta `backend`:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
````

Backend rodando em:

* `http://127.0.0.1:5000`

Teste rápido:

* `GET http://127.0.0.1:5000/health` → deve retornar `{"status":"ok"}`

### 2) Frontend

Opções:

* Abrir os arquivos `.html` diretamente no navegador, **ou**
* Usar Live Server no VSCode (recomendado)

Arquivos principais:

* `frontend/index.html` (login)
* `frontend/dashboard.html` (dashboard)
* `frontend/recursos.html` (lista de recursos)
* `frontend/gerenciar_recursos.html` (CRUD recursos - admin)
* `frontend/usuarios.html` (gestão de usuários - admin)

---

## Usuários de Teste (Seed)

Quando o backend inicia pela primeira vez, o sistema cria 3 usuários de teste automaticamente (senha `1234`):

* Funcionário: `funcionario@wayne.com` (role: `employee`)
* Gerente: `gerente@wayne.com` (role: `manager`)
* Admin Segurança: `admin@wayne.com` (role: `security_admin`)

---

## Como Usar (Passo a Passo)

### Login

1. Abra `frontend/index.html`
2. Faça login com um dos usuários seed (senha `1234`)
3. O sistema salva o token no `localStorage` e redireciona para o Dashboard

### Dashboard

* Acessível por qualquer usuário autenticado
* Mostra:

  * Total de recursos
  * Recursos por tipo
  * Atividades recentes

### Recursos (somente leitura)

* Acessível por qualquer usuário autenticado
* Lista os recursos cadastrados

### Gerenciar Recursos (CRUD) – somente `security_admin`

* Acesso bloqueado para `employee` e `manager`
* Permite:

  * Criar um recurso
  * Editar um recurso
  * Excluir um recurso

### Usuários – somente `security_admin`

* Acesso bloqueado para `employee` e `manager`
* Permite:

  * Criar usuários e atribuir perfil (`employee`, `manager`, `security_admin`)
  * Listar usuários existentes

---

## Regras de Permissão (Resumo)

| Tela / Recurso            | employee | manager | security_admin |
| ------------------------- | -------: | ------: | -------------: |
| Dashboard                 |        ✅ |       ✅ |              ✅ |
| Listar Recursos           |        ✅ |       ✅ |              ✅ |
| Gerenciar Recursos (CRUD) |        ❌ |       ❌ |              ✅ |
| Usuários (criar/listar)   |        ❌ |       ❌ |              ✅ |

---

## Banco de Dados (SQLite)

Arquivo gerado:

* `backend/wayne.db`

Tabelas:

### `users`

Campos:

* `id` (PK)
* `nome`
* `email` (único)
* `senha_hash`
* `role` (`employee`, `manager`, `security_admin`)

### `resources`

Campos:

* `id` (PK)
* `tipo` (`equipment`, `vehicle`, `security_device`)
* `nome`
* `descricao`
* `status`
* `atualizado_em` (ISO)

### `activity_logs`

Campos:

* `id` (PK)
* `user_id` (FK -> users.id)
* `acao`
* `entidade`
* `entidade_id`
* `data_hora` (ISO)

---

## API do Backend (Endpoints)

### Autenticação

#### `POST /auth/login`

Body (JSON):

```json
{ "email": "admin@wayne.com", "senha": "1234" }
```

Resposta:

```json
{
  "token": "....",
  "user": { "id": 1, "nome": "...", "email": "...", "role": "security_admin" }
}
```

#### `GET /auth/me`

Header:

* `Authorization: Bearer <token>`

Retorna dados do usuário logado.

---

### Usuários (somente `security_admin`)

#### `GET /users`

Retorna lista de usuários.

#### `POST /users`

Body (JSON):

```json
{ "nome": "Novo", "email": "novo@wayne.com", "senha": "1234", "role": "employee" }
```

---

### Recursos

#### `GET /resources` (autenticado)

Lista todos os recursos.

#### `POST /resources` (somente `security_admin`)

Body (JSON):

```json
{
  "tipo": "equipment",
  "nome": "Servidor",
  "descricao": "Sala TI",
  "status": "ativo"
}
```

#### `PUT /resources/<id>` (somente `security_admin`)

Body (JSON) igual ao POST.

#### `DELETE /resources/<id>` (somente `security_admin`)

---

### Dashboard

#### `GET /dashboard/summary` (autenticado)

Retorna:

* total de recursos
* recursos por tipo
* últimas atividades

---

## Segurança (Implementação)

* Senhas armazenadas com hash (`werkzeug.security`)
* Autenticação baseada em token JWT
* Autorização por perfil (role) protegendo:

  * Rotas do backend (`require_auth` e `require_role`)
  * Páginas do frontend (JS redireciona se não tiver permissão)

---

## Observações Importantes

* Caso a porta `5000` esteja ocupada, altere em `backend/app.py`:

  ```python
  app.run(host="127.0.0.1", port=5000, debug=True)
  ```
* Se estiver usando Live Server, apenas confirme que o backend continua em `http://127.0.0.1:5000`.

---

## Autor

* Nome: Rafael Bruno Braz Lopes
* Curso: Desenvolvimento Full-Stack com IA
* Projeto Final: Sistema de Segurança e Gestão de Recursos – Indústrias Wayne

```
```
