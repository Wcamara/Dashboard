const API_URL =
  "https://command-center-api.willpccamara.workers.dev";

const tg =
  window.Telegram?.WebApp;

let currentUser = null;

let tasks = [];
let studies = [];
let finances = [];


// =============================================
// INIT
// =============================================
document.addEventListener(
  "DOMContentLoaded",
  startApp
);


async function startApp() {

  initTelegram();

  setupNavigation();

  await authenticate();

  if (!currentUser) {
    return;
  }

  await loadEverything();
}


// =============================================
// TELEGRAM
// =============================================
function initTelegram() {

  if (!tg) {
    return;
  }

  tg.ready();
  tg.expand();

  try {
    tg.setHeaderColor("#080b10");
    tg.setBackgroundColor("#080b10");
  } catch {}

  const unsafeUser =
    tg.initDataUnsafe?.user;

  if (unsafeUser) {
    updateUserHeader(unsafeUser);
  }
}


function updateUserHeader(user) {

  const greeting =
    document.getElementById("greeting");

  const avatar =
    document.getElementById("avatar");

  if (user?.first_name) {

    greeting.textContent =
      `Olá, ${user.first_name}`;

    avatar.textContent =
      user.first_name
        .charAt(0)
        .toUpperCase();
  }
}


// =============================================
// AUTH
// =============================================
async function authenticate() {

  if (!tg?.initData) {

    alert(
      "Abra este aplicativo pelo Telegram."
    );

    return;
  }

  const response = await api(
    "/auth/me",
    {
      method: "GET"
    }
  );

  if (!response?.ok) {

    alert(
      response?.error ||
      "Erro de autenticação."
    );

    return;
  }

  currentUser =
    response.user;

  updateUserHeader(
    currentUser
  );
}


// =============================================
// API
// =============================================
async function api(
  path,
  options = {}
) {

  const headers = {
    ...(options.headers || {}),
    "X-Telegram-Init-Data":
      tg?.initData || ""
  };

  if (options.body) {
    headers["Content-Type"] =
      "application/json";
  }

  try {

    const response =
      await fetch(
        API_URL + path,
        {
          ...options,
          headers
        }
      );

    return await response.json();

  } catch (error) {

    console.error(error);

    return {
      ok: false,
      error:
        "Falha ao conectar com o servidor."
    };
  }
}


// =============================================
// LOAD
// =============================================
async function loadEverything() {

  await Promise.all([
    loadTasks(),
    loadStudies(),
    loadFinances()
  ]);

  renderHome();
}


async function loadTasks() {

  const data =
    await api(
      "/tasks",
      {
        method: "GET"
      }
    );

  if (!data.ok) {
    return;
  }

  tasks =
    data.tasks || [];

  renderTasks();
}


async function loadStudies() {

  const data =
    await api(
      "/studies",
      {
        method: "GET"
      }
    );

  if (!data.ok) {
    return;
  }

  studies =
    data.studies || [];

  renderStudies();
}


async function loadFinances() {

  const data =
    await api(
      "/finances",
      {
        method: "GET"
      }
    );

  if (!data.ok) {
    return;
  }

  finances =
    data.finances || [];

  renderFinances(
    data.summary
  );
}


// =============================================
// NAVIGATION
// =============================================
function setupNavigation() {

  document
    .querySelectorAll(".nav-item")
    .forEach(button => {

      button.addEventListener(
        "click",
        () => {

          const page =
            button.dataset.page;

          document
            .querySelectorAll(".nav-item")
            .forEach(item =>
              item.classList.remove("active")
            );

          button
            .classList
            .add("active");

          document
            .querySelectorAll(".page")
            .forEach(item =>
              item.classList.remove("active")
            );

          document
            .getElementById(
              `page-${page}`
            )
            .classList
            .add("active");
        }
      );
    });
}


// =============================================
// TASKS
// =============================================
function renderTasks() {

  const container =
    document.getElementById(
      "tasksList"
    );

  if (!tasks.length) {

    container.innerHTML =
      `<div class="empty">
        Nenhuma tarefa cadastrada.
      </div>`;

    return;
  }

  container.innerHTML =
    tasks
      .map(task => {

        const completed =
          task.status === "completed";

        return `
          <article
            class="list-card
            ${completed ? "completed" : ""}"
          >

            <div class="list-card-content">

              <h3>
                ${escapeHtml(task.title)}
              </h3>

              ${
                task.description
                  ? `
                    <p>
                      ${escapeHtml(task.description)}
                    </p>
                  `
                  : ""
              }

              ${
                task.due_date
                  ? `
                    <p>
                      Prazo:
                      ${formatDate(task.due_date)}
                    </p>
                  `
                  : ""
              }

              <span
                class="status
                ${
                  completed
                    ? "completed"
                    : "pending"
                }"
              >
                ${
                  completed
                    ? "Concluída"
                    : "Pendente"
                }
              </span>

            </div>


            <div class="card-actions">

              <button
                class="icon-button"
                onclick="
                  toggleTask(
                    ${task.id},
                    '${task.status}'
                  )
                "
              >
                ✓
              </button>

              <button
                class="icon-button danger"
                onclick="
                  deleteTask(${task.id})
                "
              >
                ×
              </button>

            </div>

          </article>
        `;
      })
      .join("");
}


async function createTask() {

  const title =
    document
      .getElementById("taskTitle")
      .value
      .trim();

  const description =
    document
      .getElementById("taskDescription")
      .value
      .trim();

  const dueDate =
    document
      .getElementById("taskDueDate")
      .value;


  if (!title) {

    alert(
      "Digite o título da tarefa."
    );

    return;
  }


  const result =
    await api(
      "/tasks",
      {
        method: "POST",

        body:
          JSON.stringify({
            title,
            description,
            due_date:
              dueDate || null
          })
      }
    );


  if (!result.ok) {

    alert(result.error);

    return;
  }


  closeModal(
    "taskModal"
  );

  clearTaskForm();

  await loadTasks();

  renderHome();
}


async function toggleTask(
  id,
  status
) {

  const newStatus =
    status === "completed"
      ? "pending"
      : "completed";


  const result =
    await api(
      `/tasks/${id}`,
      {
        method: "PUT",

        body:
          JSON.stringify({
            status:
              newStatus
          })
      }
    );


  if (!result.ok) {

    alert(result.error);

    return;
  }


  await loadTasks();

  renderHome();
}


async function deleteTask(id) {

  if (
    !confirm(
      "Excluir esta tarefa?"
    )
  ) {
    return;
  }


  const result =
    await api(
      `/tasks/${id}`,
      {
        method: "DELETE"
      }
    );


  if (!result.ok) {

    alert(result.error);

    return;
  }


  await loadTasks();

  renderHome();
}


// =============================================
// STUDIES
// =============================================
function renderStudies() {

  const container =
    document.getElementById(
      "studiesList"
    );


  if (!studies.length) {

    container.innerHTML =
      `<div class="empty">
        Nenhum estudo cadastrado.
      </div>`;

    return;
  }


  container.innerHTML =
    studies
      .map(study => {

        return `
          <article class="list-card">

            <div class="list-card-content">

              <h3>
                ${escapeHtml(study.subject)}
              </h3>

              ${
                study.topic
                  ? `
                    <p>
                      ${escapeHtml(study.topic)}
                    </p>
                  `
                  : ""
              }

              <p>
                Progresso:
                ${study.progress}%
              </p>

              <div class="progress">
                <div
                  style="
                    width:
                    ${study.progress}%;
                  "
                ></div>
              </div>

            </div>


            <div class="card-actions">

              <button
                class="icon-button danger"
                onclick="
                  deleteStudy(${study.id})
                "
              >
                ×
              </button>

            </div>

          </article>
        `;
      })
      .join("");
}


async function createStudy() {

  const subject =
    document
      .getElementById(
        "studySubject"
      )
      .value
      .trim();

  const topic =
    document
      .getElementById(
        "studyTopic"
      )
      .value
      .trim();

  const progress =
    Number(
      document
        .getElementById(
          "studyProgress"
        )
        .value
    );

  const notes =
    document
      .getElementById(
        "studyNotes"
      )
      .value
      .trim();


  if (!subject) {

    alert(
      "Digite a matéria."
    );

    return;
  }


  const result =
    await api(
      "/studies",
      {
        method: "POST",

        body:
          JSON.stringify({
            subject,
            topic,
            progress,
            notes
          })
      }
    );


  if (!result.ok) {

    alert(result.error);

    return;
  }


  closeModal(
    "studyModal"
  );

  clearStudyForm();

  await loadStudies();

  renderHome();
}


async function deleteStudy(id) {

  if (
    !confirm(
      "Excluir este estudo?"
    )
  ) {
    return;
  }


  const result =
    await api(
      `/studies/${id}`,
      {
        method: "DELETE"
      }
    );


  if (!result.ok) {

    alert(result.error);

    return;
  }


  await loadStudies();

  renderHome();
}


// =============================================
// FINANCES
// =============================================
function renderFinances(
  summary
) {

  const income =
    Number(
      summary?.income || 0
    );

  const expense =
    Number(
      summary?.expense || 0
    );

  const balance =
    Number(
      summary?.balance || 0
    );


  document
    .getElementById(
      "financeIncome"
    )
    .textContent =
      money(income);


  document
    .getElementById(
      "financeExpense"
    )
    .textContent =
      money(expense);


  document
    .getElementById(
      "financeBalance"
    )
    .textContent =
      money(balance);


  const container =
    document.getElementById(
      "financesList"
    );


  if (!finances.length) {

    container.innerHTML =
      `<div class="empty">
        Nenhum lançamento.
      </div>`;

    return;
  }


  container.innerHTML =
    finances
      .map(item => {

        const incomeItem =
          item.type === "income";

        return `
          <article class="list-card">

            <div class="list-card-content">

              <h3>
                ${escapeHtml(item.description)}
              </h3>

              <p>
                ${
                  escapeHtml(
                    item.category || "Sem categoria"
                  )
                }
                ·
                ${formatDate(item.date)}
              </p>

              <strong
                class="
                  ${
                    incomeItem
                      ? "positive"
                      : "negative"
                  }
                "
              >
                ${
                  incomeItem
                    ? "+"
                    : "-"
                }
                ${money(item.amount)}
              </strong>

            </div>


            <button
              class="icon-button danger"
              onclick="
                deleteFinance(${item.id})
              "
            >
              ×
            </button>

          </article>
        `;
      })
      .join("");
}


async function createFinance() {

  const type =
    document
      .getElementById(
        "financeType"
      )
      .value;

  const description =
    document
      .getElementById(
        "financeDescription"
      )
      .value
      .trim();

  const amount =
    Number(
      document
        .getElementById(
          "financeAmount"
        )
        .value
    );

  const category =
    document
      .getElementById(
        "financeCategory"
      )
      .value
      .trim();

  const date =
    document
      .getElementById(
        "financeDate"
      )
      .value;


  if (!description) {

    alert(
      "Digite uma descrição."
    );

    return;
  }


  if (!amount || amount <= 0) {

    alert(
      "Digite um valor válido."
    );

    return;
  }


  if (!date) {

    alert(
      "Escolha uma data."
    );

    return;
  }


  const result =
    await api(
      "/finances",
      {
        method: "POST",

        body:
          JSON.stringify({
            type,
            description,
            amount,
            category,
            date
          })
      }
    );


  if (!result.ok) {

    alert(result.error);

    return;
  }


  closeModal(
    "financeModal"
  );

  clearFinanceForm();

  await loadFinances();

  renderHome();
}


async function deleteFinance(id) {

  if (
    !confirm(
      "Excluir este lançamento?"
    )
  ) {
    return;
  }


  const result =
    await api(
      `/finances/${id}`,
      {
        method: "DELETE"
      }
    );


  if (!result.ok) {

    alert(result.error);

    return;
  }


  await loadFinances();

  renderHome();
}


// =============================================
// HOME
// =============================================
function renderHome() {

  const pending =
    tasks.filter(
      task =>
        task.status === "pending"
    );


  document
    .getElementById(
      "homePendingTasks"
    )
    .textContent =
      pending.length;


  const income =
    finances
      .filter(
        item =>
          item.type === "income"
      )
      .reduce(
        (sum, item) =>
          sum +
          Number(item.amount),
        0
      );


  const expenses =
    finances
      .filter(
        item =>
          item.type === "expense"
      )
      .reduce(
        (sum, item) =>
          sum +
          Number(item.amount),
        0
      );


  document
    .getElementById(
      "homeBalance"
    )
    .textContent =
      money(
        income - expenses
      );


  const homeTasks =
    document.getElementById(
      "homeTasks"
    );


  if (!pending.length) {

    homeTasks.innerHTML =
      `<div class="empty">
        Nenhuma tarefa pendente.
      </div>`;

  } else {

    homeTasks.innerHTML =
      pending
        .slice(0, 3)
        .map(task => `
          <article class="list-card">

            <div class="list-card-content">

              <h3>
                ${escapeHtml(task.title)}
              </h3>

              ${
                task.due_date
                  ? `
                    <p>
                      ${formatDate(task.due_date)}
                    </p>
                  `
                  : ""
              }

            </div>

          </article>
        `)
        .join("");
  }


  const homeStudies =
    document.getElementById(
      "homeStudies"
    );


  if (!studies.length) {

    homeStudies.innerHTML =
      `<div class="empty">
        Nenhum estudo cadastrado.
      </div>`;

  } else {

    homeStudies.innerHTML =
      studies
        .slice(0, 3)
        .map(study => `
          <article class="list-card">

            <div class="list-card-content">

              <h3>
                ${escapeHtml(study.subject)}
              </h3>

              <p>
                ${
                  escapeHtml(
                    study.topic || ""
                  )
                }
              </p>

              <div class="progress">
                <div
                  style="
                    width:
                    ${study.progress}%;
                  "
                ></div>
              </div>

            </div>

          </article>
        `)
        .join("");
  }
}


// =============================================
// MODALS
// =============================================
function openTaskModal() {

  document
    .getElementById(
      "taskModal"
    )
    .classList
    .add("open");
}


function openStudyModal() {

  document
    .getElementById(
      "studyModal"
    )
    .classList
    .add("open");
}


function openFinanceModal() {

  const input =
    document.getElementById(
      "financeDate"
    );

  if (!input.value) {

    input.value =
      new Date()
        .toISOString()
        .slice(0, 10);
  }


  document
    .getElementById(
      "financeModal"
    )
    .classList
    .add("open");
}


function closeModal(id) {

  document
    .getElementById(id)
    .classList
    .remove("open");
}


// =============================================
// CLEAR FORMS
// =============================================
function clearTaskForm() {

  document
    .getElementById(
      "taskTitle"
    )
    .value = "";

  document
    .getElementById(
      "taskDescription"
    )
    .value = "";

  document
    .getElementById(
      "taskDueDate"
    )
    .value = "";
}


function clearStudyForm() {

  document
    .getElementById(
      "studySubject"
    )
    .value = "";

  document
    .getElementById(
      "studyTopic"
    )
    .value = "";

  document
    .getElementById(
      "studyProgress"
    )
    .value = 0;

  document
    .getElementById(
      "studyNotes"
    )
    .value = "";
}


function clearFinanceForm() {

  document
    .getElementById(
      "financeDescription"
    )
    .value = "";

  document
    .getElementById(
      "financeAmount"
    )
    .value = "";

  document
    .getElementById(
      "financeCategory"
    )
    .value = "";
}


// =============================================
// HELPERS
// =============================================
function money(value) {

  return new Intl
    .NumberFormat(
      "pt-BR",
      {
        style: "currency",
        currency: "BRL"
      }
    )
    .format(
      Number(value || 0)
    );
}


function formatDate(value) {

  if (!value) {
    return "";
  }

  const [
    year,
    month,
    day
  ] =
    value.split("-");

  return `${day}/${month}/${year}`;
}


function escapeHtml(value) {

  const div =
    document.createElement(
      "div"
    );

  div.textContent =
    String(value ?? "");

  return div.innerHTML;
}
