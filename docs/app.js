const API_URL =
  "https://command-center-api.willpccamara.workers.dev";


const tg =
  window.Telegram?.WebApp;


// =========================================================
// TELEGRAM
// =========================================================

if (tg) {

  tg.ready();

  tg.expand();

  try {

    tg.setHeaderColor("#080b10");

    tg.setBackgroundColor("#080b10");

  } catch (_) {}

}


// =========================================================
// STATE
// =========================================================

const state = {

  user: null,

  tasks: [],

  studies: [],

  finances: [],

  taskFilter:
    "pending",

  financeMonth:
    getCurrentMonth(),

  financeContext:
    "",

  creditCard: {
    configured: false,
    closing_day: null
  }

};



// =========================================================
// ELEMENTS
// =========================================================

const loading =
  document.getElementById("loading");


const errorBox =
  document.getElementById("error-box");


const toast =
  document.getElementById("toast");



// =========================================================
// API
// =========================================================

async function api(
  path,
  options = {}
) {

  const headers = {
    "Content-Type":
      "application/json",

    "X-Telegram-Init-Data":
      tg?.initData || "",

    ...(options.headers || {})
  };


  const response =
    await fetch(
      `${API_URL}${path}`,
      {
        ...options,
        headers
      }
    );


  let data;


  try {

    data =
      await response.json();

  } catch {

    data = {
      ok: false,
      error:
        "Resposta inválida do servidor."
    };

  }


  if (!response.ok) {

    throw new Error(
      data.error ||
      "Erro no servidor."
    );

  }


  return data;
}



// =========================================================
// INIT
// =========================================================

async function init() {

  setLoading(true);


  try {

    await loadUser();

    await Promise.all([
      loadTasks(),
      loadStudies(),
      loadCreditCard()
    ]);


    await Promise.all([
      loadHomeFinance(),
      loadFinance()
    ]);


    renderEverything();


    setLoading(false);


  } catch (error) {

    setLoading(false);

    showError(
      error.message
    );

  }

}


init();



// =========================================================
// USER
// =========================================================

async function loadUser() {

  const data =
    await api(
      "/auth/me"
    );


  state.user =
    data.user;


  const name =
    state.user.first_name ||
    state.user.username ||
    "Usuário";


  document
    .getElementById(
      "user-name"
    )
    .textContent =
      name;

}



// =========================================================
// NAVIGATION
// =========================================================

document
  .querySelectorAll(
    ".nav-item"
  )
  .forEach(button => {

    button.addEventListener(
      "click",
      () => {

        showPage(
          button.dataset.page
        );

      }
    );

  });



document
  .querySelectorAll(
    "[data-go-page]"
  )
  .forEach(button => {

    button.addEventListener(
      "click",
      async () => {

        if (
          button.dataset.monthMode ===
          "next"
        ) {

          state.financeMonth =
            addMonths(
              getCurrentMonth(),
              1
            );


          await loadFinance();

        }


        showPage(
          button.dataset.goPage
        );

      }
    );

  });



function showPage(page) {

  document
    .querySelectorAll(
      ".page"
    )
    .forEach(element => {

      element.classList
        .remove("active");

    });


  document
    .getElementById(
      `page-${page}`
    )
    .classList
    .add("active");


  document
    .querySelectorAll(
      ".nav-item"
    )
    .forEach(button => {

      button.classList
        .toggle(
          "active",
          button.dataset.page === page
        );

    });


  const titles = {

    home:
      "Início",

    tasks:
      "Tarefas",

    studies:
      "Estudos",

    finance:
      "Financeiro"

  };


  document
    .getElementById(
      "page-title"
    )
    .textContent =
      titles[page] || "Command Center";


  window.scrollTo(
    {
      top: 0,
      behavior: "smooth"
    }
  );

}



// =========================================================
// REFRESH
// =========================================================

document
  .getElementById(
    "refresh-button"
  )
  .addEventListener(
    "click",
    async () => {

      setLoading(true);


      try {

        await Promise.all([
          loadTasks(),
          loadStudies(),
          loadCreditCard(),
          loadHomeFinance(),
          loadFinance()
        ]);


        renderEverything();

        showToast(
          "Atualizado"
        );


      } catch (error) {

        showToast(
          error.message
        );

      }


      setLoading(false);

    }
  );



// =========================================================
// HOME
// =========================================================

async function loadHomeFinance() {

  const currentMonth =
    getCurrentMonth();


  const nextMonth =
    addMonths(
      currentMonth,
      1
    );


  const [
    current,
    next
  ] =
    await Promise.all([

      api(
        `/finances?month=${currentMonth}`
      ),

      api(
        `/finances?month=${nextMonth}`
      )

    ]);


  state.homeCurrentFinance =
    current;


  state.homeNextFinance =
    next;

}



function renderHome() {

  const current =
    state.homeCurrentFinance;


  const next =
    state.homeNextFinance;


  if (!current || !next) {
    return;
  }


  setText(
    "home-current-month",
    current.month_label
  );


  setText(
    "home-balance",
    formatMoney(
      current.summary.balance
    )
  );


  setText(
    "home-income",
    formatMoney(
      current.summary.income
    )
  );


  setText(
    "home-expense",
    formatMoney(
      current.summary.expense
    )
  );


  setText(
    "home-next-month",
    next.month_label
  );


  setText(
    "home-next-expense",
    formatMoney(
      next.summary.expense
    )
  );


  setText(
    "home-next-balance",
    formatMoney(
      next.summary.balance
    )
  );


  const pending =
    state.tasks.filter(
      task =>
        task.status === "pending"
    );


  setText(
    "home-pending-tasks",
    pending.length
  );


  setText(
    "home-card-closing",
    state.creditCard.configured
      ? `Dia ${state.creditCard.closing_day}`
      : "--"
  );


  const container =
    document.getElementById(
      "home-task-list"
    );


  const latest =
    pending.slice(0, 4);


  if (!latest.length) {

    container.innerHTML =
      emptyState(
        "Nenhuma tarefa pendente."
      );

    return;

  }


  container.innerHTML =
    latest
      .map(
        task =>
          taskHtml(
            task,
            true
          )
      )
      .join("");

}



// =========================================================
// TASKS
// =========================================================

async function loadTasks() {

  const data =
    await api(
      "/tasks"
    );


  state.tasks =
    data.tasks || [];

}



function renderTasks() {

  const container =
    document.getElementById(
      "task-list"
    );


  let tasks =
    [...state.tasks];


  if (
    state.taskFilter !== "all"
  ) {

    tasks =
      tasks.filter(
        task =>
          task.status ===
          state.taskFilter
      );

  }


  if (!tasks.length) {

    container.innerHTML =
      emptyState(
        "Nenhuma tarefa aqui."
      );

    return;

  }


  container.innerHTML =
    tasks
      .map(
        task =>
          taskHtml(
            task,
            false
          )
      )
      .join("");

}



function taskHtml(
  task,
  compact = false
) {

  const completed =
    task.status ===
    "completed";


  const reminder =
    Number(
      task.reminder_enabled
    ) === 1;


  return `
    <article
      class="list-item
      ${completed ? "completed" : ""}"
    >

      <div class="list-item-top">

        <div>

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

        </div>

        <span>
          ${completed ? "✓" : "○"}
        </span>

      </div>


      <div class="badges">

        ${
          task.due_date
            ? `
              <span class="badge">
                📅 ${formatDate(task.due_date)}
              </span>
            `
            : ""
        }

        ${
          reminder
            ? `
              <span class="badge">
                🔔 Lembrete ativo
              </span>
            `
            : ""
        }

      </div>


      ${
        compact
          ? ""
          : `
            <div class="item-actions">

              <button
                class="small-button
                ${completed
                  ? ""
                  : "success"}"
                onclick="
                  toggleTask(
                    ${task.id},
                    '${task.status}'
                  )
                "
              >

                ${
                  completed
                    ? "Reabrir"
                    : "Concluir"
                }

              </button>


              ${
                reminder
                  ? `
                    <button
                      class="small-button"
                      onclick="
                        disableReminder(
                          ${task.id}
                        )
                      "
                    >
                      🔕 Parar
                    </button>
                  `
                  : ""
              }


              <button
                class="small-button danger"
                onclick="
                  deleteTask(
                    ${task.id}
                  )
                "
              >
                Excluir
              </button>

            </div>
          `
      }

    </article>
  `;

}



// =========================================================
// TASK FILTER
// =========================================================

document
  .querySelectorAll(
    "[data-task-filter]"
  )
  .forEach(button => {

    button.addEventListener(
      "click",
      () => {

        state.taskFilter =
          button.dataset.taskFilter;


        document
          .querySelectorAll(
            "[data-task-filter]"
          )
          .forEach(item => {

            item.classList
              .toggle(
                "active",
                item === button
              );

          });


        renderTasks();

      }
    );

  });



// =========================================================
// TASK MODAL
// =========================================================

document
  .getElementById(
    "new-task-button"
  )
  .addEventListener(
    "click",
    () => {

      openModal(
        "task-modal"
      );

    }
  );



document
  .getElementById(
    "task-reminder-enabled"
  )
  .addEventListener(
    "change",
    event => {

      document
        .getElementById(
          "task-reminder-options"
        )
        .classList
        .toggle(
          "hidden",
          !event.target.checked
        );

    }
  );



document
  .getElementById(
    "task-form"
  )
  .addEventListener(
    "submit",
    async event => {

      event.preventDefault();


      const reminderEnabled =
        document
          .getElementById(
            "task-reminder-enabled"
          )
          .checked;


      const reminderAt =
        document
          .getElementById(
            "task-reminder-at"
          )
          .value;


      try {

        await api(
          "/tasks",
          {

            method: "POST",

            body:
              JSON.stringify({

                title:
                  valueOf(
                    "task-title"
                  ),

                description:
                  valueOf(
                    "task-description"
                  ),

                due_date:
                  valueOf(
                    "task-due-date"
                  ) || null,

                reminder_enabled:
                  reminderEnabled,

                reminder_at:
                  reminderEnabled &&
                  reminderAt
                    ? new Date(
                        reminderAt
                      ).toISOString()
                    : null

              })

          }
        );


        closeModal(
          "task-modal"
        );


        event.target.reset();


        document
          .getElementById(
            "task-reminder-options"
          )
          .classList
          .add("hidden");


        await loadTasks();


        renderTasks();

        renderHome();


        showToast(
          "Tarefa criada"
        );


      } catch (error) {

        showToast(
          error.message
        );

      }

    }
  );



async function toggleTask(
  id,
  currentStatus
) {

  const status =
    currentStatus === "pending"
      ? "completed"
      : "pending";


  try {

    await api(
      `/tasks/${id}`,
      {

        method: "PUT",

        body:
          JSON.stringify({
            status
          })

      }
    );


    await loadTasks();


    renderTasks();

    renderHome();


  } catch (error) {

    showToast(
      error.message
    );

  }

}



async function disableReminder(
  id
) {

  try {

    await api(
      `/tasks/${id}/reminder/disable`,
      {
        method: "POST"
      }
    );


    await loadTasks();


    renderTasks();

    renderHome();


    showToast(
      "Lembrete desativado"
    );


  } catch (error) {

    showToast(
      error.message
    );

  }

}



async function deleteTask(
  id
) {

  if (
    !confirm(
      "Excluir essa tarefa?"
    )
  ) {
    return;
  }


  try {

    await api(
      `/tasks/${id}`,
      {
        method: "DELETE"
      }
    );


    await loadTasks();


    renderTasks();

    renderHome();


    showToast(
      "Tarefa excluída"
    );


  } catch (error) {

    showToast(
      error.message
    );

  }

}



// =========================================================
// STUDIES
// =========================================================

async function loadStudies() {

  const data =
    await api(
      "/studies"
    );


  state.studies =
    data.studies || [];

}



function renderStudies() {

  const container =
    document.getElementById(
      "study-list"
    );


  if (!state.studies.length) {

    container.innerHTML =
      emptyState(
        "Nenhum estudo registrado."
      );

    return;

  }


  container.innerHTML =
    state.studies
      .map(study => `

        <article class="list-item">

          <div class="list-item-top">

            <div>

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

            </div>


            <strong>
              ${Number(study.progress)}%
            </strong>

          </div>


          <div class="progress-bar">

            <div
              style="
                width:
                ${Number(study.progress)}%
              "
            ></div>

          </div>


          ${
            study.notes
              ? `
                <p>
                  ${escapeHtml(study.notes)}
                </p>
              `
              : ""
          }


          <div class="item-actions">

            <button
              class="small-button danger"
              onclick="
                deleteStudy(
                  ${study.id}
                )
              "
            >
              Excluir
            </button>

          </div>

        </article>

      `)
      .join("");

}



// =========================================================
// STUDY MODAL
// =========================================================

document
  .getElementById(
    "new-study-button"
  )
  .addEventListener(
    "click",
    () => {

      openModal(
        "study-modal"
      );

    }
  );



document
  .getElementById(
    "study-progress"
  )
  .addEventListener(
    "input",
    event => {

      setText(
        "study-progress-value",
        `${event.target.value}%`
      );

    }
  );



document
  .getElementById(
    "study-form"
  )
  .addEventListener(
    "submit",
    async event => {

      event.preventDefault();


      try {

        await api(
          "/studies",
          {

            method:
              "POST",

            body:
              JSON.stringify({

                subject:
                  valueOf(
                    "study-subject"
                  ),

                topic:
                  valueOf(
                    "study-topic"
                  ),

                progress:
                  Number(
                    valueOf(
                      "study-progress"
                    )
                  ),

                notes:
                  valueOf(
                    "study-notes"
                  )

              })

          }
        );


        closeModal(
          "study-modal"
        );


        event.target
          .reset();


        setText(
          "study-progress-value",
          "0%"
        );


        await loadStudies();


        renderStudies();


        showToast(
          "Estudo salvo"
        );


      } catch (error) {

        showToast(
          error.message
        );

      }

    }
  );



async function deleteStudy(
  id
) {

  if (
    !confirm(
      "Excluir este estudo?"
    )
  ) {
    return;
  }


  try {

    await api(
      `/studies/${id}`,
      {
        method:
          "DELETE"
      }
    );


    await loadStudies();


    renderStudies();


    showToast(
      "Estudo excluído"
    );


  } catch (error) {

    showToast(
      error.message
    );

  }

}



// =========================================================
// CREDIT CARD
// =========================================================

async function loadCreditCard() {

  const data =
    await api(
      "/credit-card"
    );


  state.creditCard = {

    configured:
      data.configured,

    closing_day:
      data.closing_day

  };

}



function renderCreditCard() {

  const input =
    document.getElementById(
      "credit-closing-day"
    );


  const status =
    document.getElementById(
      "credit-card-status"
    );


  if (
    state.creditCard.configured
  ) {

    input.value =
      state.creditCard.closing_day;


    status.textContent =
      `Fecha dia ${state.creditCard.closing_day}`;

  } else {

    input.value = "";

    status.textContent =
      "Não configurado";

  }

}



document
  .getElementById(
    "save-credit-card-button"
  )
  .addEventListener(
    "click",
    async () => {

      const closingDay =
        Number(
          valueOf(
            "credit-closing-day"
          )
        );


      if (
        !Number.isInteger(
          closingDay
        ) ||
        closingDay < 1 ||
        closingDay > 31
      ) {

        showToast(
          "Digite um dia entre 1 e 31"
        );

        return;

      }


      try {

        await api(
          "/credit-card",
          {

            method:
              "POST",

            body:
              JSON.stringify({
                closing_day:
                  closingDay
              })

          }
        );


        await loadCreditCard();


        renderCreditCard();

        renderHome();


        showToast(
          "Cartão configurado"
        );


      } catch (error) {

        showToast(
          error.message
        );

      }

    }
  );



// =========================================================
// FINANCE
// =========================================================

async function loadFinance() {

  let path =
    `/finances?month=${state.financeMonth}`;


  if (
    state.financeContext
  ) {

    path +=
      `&context=${encodeURIComponent(
        state.financeContext
      )}`;

  }


  const data =
    await api(path);


  state.financeData =
    data;


  state.finances =
    data.finances || [];

}



function renderFinance() {

  const data =
    state.financeData;


  if (!data) {
    return;
  }


  setText(
    "finance-month-label",
    data.month_label
  );


  setText(
    "finance-income",
    formatMoney(
      data.summary.income
    )
  );


  setText(
    "finance-expense",
    formatMoney(
      data.summary.expense
    )
  );


  setText(
    "finance-balance",
    formatMoney(
      data.summary.balance
    )
  );


  const current =
    getCurrentMonth();


  const next =
    addMonths(
      current,
      1
    );


  document
    .getElementById(
      "finance-current-month-button"
    )
    .classList
    .toggle(
      "active",
      state.financeMonth ===
      current
    );


  document
    .getElementById(
      "finance-next-month-button"
    )
    .classList
    .toggle(
      "active",
      state.financeMonth ===
      next
    );


  const container =
    document.getElementById(
      "finance-list"
    );


  if (
    !state.finances.length
  ) {

    container.innerHTML =
      emptyState(
        "Nenhum lançamento neste mês."
      );

    return;

  }


  container.innerHTML =
    state.finances
      .map(financeHtml)
      .join("");

}



function financeHtml(item) {

  const expense =
    item.type ===
    "expense";


  const credit =
    item.payment_method ===
    "credit";


  return `

    <article class="list-item">

      <div class="list-item-top">

        <div>

          <h3>
            ${escapeHtml(
              item.description
            )}
          </h3>

          <p>
            ${formatDate(item.date)}
          </p>

        </div>


        <span
          class="
            item-value
            ${expense
              ? "negative"
              : "positive"}
          "
        >
          ${expense ? "-" : "+"}
          ${formatMoney(item.amount)}
        </span>

      </div>


      <div class="badges">

        ${
          credit
            ? `
              <span class="badge credit">
                💳 Crédito
              </span>
            `
            : ""
        }


        ${
          item.context
            ? `
              <span class="badge context">
                🏷️ ${escapeHtml(
                  capitalize(
                    item.context
                  )
                )}
              </span>
            `
            : ""
        }


        ${
          item.category
            ? `
              <span class="badge">
                ${escapeHtml(
                  item.category
                )}
              </span>
            `
            : ""
        }

      </div>


      <div class="item-actions">

        <button
          class="small-button danger"
          onclick="
            deleteFinance(
              ${item.id}
            )
          "
        >
          Excluir
        </button>

      </div>

    </article>

  `;

}



// =========================================================
// MONTH BUTTONS
// =========================================================

document
  .getElementById(
    "finance-current-month-button"
  )
  .addEventListener(
    "click",
    async () => {

      state.financeMonth =
        getCurrentMonth();


      await reloadFinanceView();

    }
  );



document
  .getElementById(
    "finance-next-month-button"
  )
  .addEventListener(
    "click",
    async () => {

      state.financeMonth =
        addMonths(
          getCurrentMonth(),
          1
        );


      await reloadFinanceView();

    }
  );



document
  .getElementById(
    "finance-prev-month"
  )
  .addEventListener(
    "click",
    async () => {

      state.financeMonth =
        addMonths(
          state.financeMonth,
          -1
        );


      await reloadFinanceView();

    }
  );



document
  .getElementById(
    "finance-next-month"
  )
  .addEventListener(
    "click",
    async () => {

      state.financeMonth =
        addMonths(
          state.financeMonth,
          1
        );


      await reloadFinanceView();

    }
  );



async function reloadFinanceView() {

  try {

    await loadFinance();

    renderFinance();


  } catch (error) {

    showToast(
      error.message
    );

  }

}



// =========================================================
// CONTEXT FILTER
// =========================================================

document
  .getElementById(
    "finance-context-filter"
  )
  .addEventListener(
    "change",
    async event => {

      state.financeContext =
        event.target.value.trim();


      await reloadFinanceView();

    }
  );



document
  .getElementById(
    "clear-context-filter"
  )
  .addEventListener(
    "click",
    async () => {

      state.financeContext = "";


      document
        .getElementById(
          "finance-context-filter"
        )
        .value = "";


      await reloadFinanceView();

    }
  );



// =========================================================
// FINANCE MODAL
// =========================================================

document
  .getElementById(
    "new-finance-button"
  )
  .addEventListener(
    "click",
    () => {

      document
        .getElementById(
          "finance-date"
        )
        .value =
          todayLocal();


      openModal(
        "finance-modal"
      );


      updateFinanceForm();

    }
  );



document
  .getElementById(
    "finance-type"
  )
  .addEventListener(
    "change",
    updateFinanceForm
  );



document
  .getElementById(
    "finance-payment-method"
  )
  .addEventListener(
    "change",
    updateFinanceForm
  );



function updateFinanceForm() {

  const type =
    valueOf(
      "finance-type"
    );


  const payment =
    valueOf(
      "finance-payment-method"
    );


  const isExpense =
    type === "expense";


  const isCredit =
    payment === "credit" &&
    isExpense;


  document
    .getElementById(
      "expense-options"
    )
    .classList
    .toggle(
      "hidden",
      !isExpense
    );


  document
    .getElementById(
      "reference-month-wrapper"
    )
    .classList
    .toggle(
      "hidden",
      isCredit
    );


  document
    .getElementById(
      "credit-auto-message"
    )
    .classList
    .toggle(
      "hidden",
      !isCredit
    );

}



// =========================================================
// CREATE FINANCE
// =========================================================

document
  .getElementById(
    "finance-form"
  )
  .addEventListener(
    "submit",
    async event => {

      event.preventDefault();


      const type =
        valueOf(
          "finance-type"
        );


      const paymentMethod =
        type === "expense"
          ? valueOf(
              "finance-payment-method"
            )
          : "other";


      const referenceChoice =
        valueOf(
          "finance-reference-month"
        );


      const date =
        valueOf(
          "finance-date"
        );


      let referenceMonth =
        date.slice(
          0,
          7
        );


      if (
        referenceChoice ===
        "next"
      ) {

        referenceMonth =
          "next";

      }


      const body = {

        type,

        description:
          valueOf(
            "finance-description"
          ),

        amount:
          Number(
            valueOf(
              "finance-amount"
            )
          ),

        date,

        category:
          type === "income"
            ? "Recebimento"
            : (
                paymentMethod ===
                "credit"
                  ? "Crédito"
                  : "Compra"
              ),

        payment_method:
          paymentMethod,

        context:
          valueOf(
            "finance-context"
          ),

        reference_month:
          referenceMonth

      };


      try {

        const result =
          await api(
            "/finances",
            {

              method:
                "POST",

              body:
                JSON.stringify(
                  body
                )

            }
          );


        closeModal(
          "finance-modal"
        );


        event.target
          .reset();


        document
          .getElementById(
            "finance-date"
          )
          .value =
            todayLocal();


        state.financeMonth =
          result.reference_month;


        await Promise.all([
          loadFinance(),
          loadHomeFinance()
        ]);


        renderFinance();

        renderHome();


        showToast(
          `Lançado em ${result.reference_month_label}`
        );


      } catch (error) {

        showToast(
          error.message
        );

      }

    }
  );



// =========================================================
// DELETE FINANCE
// =========================================================

async function deleteFinance(
  id
) {

  if (
    !confirm(
      "Excluir este lançamento?"
    )
  ) {
    return;
  }


  try {

    await api(
      `/finances/${id}`,
      {
        method:
          "DELETE"
      }
    );


    await Promise.all([
      loadFinance(),
      loadHomeFinance()
    ]);


    renderFinance();

    renderHome();


    showToast(
      "Lançamento excluído"
    );


  } catch (error) {

    showToast(
      error.message
    );

  }

}



// =========================================================
// MODALS
// =========================================================

document
  .querySelectorAll(
    ".close-modal"
  )
  .forEach(button => {

    button.addEventListener(
      "click",
      () => {

        closeModal(
          button.dataset.close
        );

      }
    );

  });



document
  .querySelectorAll(
    ".modal-backdrop"
  )
  .forEach(backdrop => {

    backdrop.addEventListener(
      "click",
      () => {

        const modal =
          backdrop.closest(
            ".modal"
          );


        modal.classList
          .add("hidden");

      }
    );

  });



function openModal(id) {

  document
    .getElementById(id)
    .classList
    .remove("hidden");

}



function closeModal(id) {

  document
    .getElementById(id)
    .classList
    .add("hidden");

}



// =========================================================
// RENDER
// =========================================================

function renderEverything() {

  renderHome();

  renderTasks();

  renderStudies();

  renderCreditCard();

  renderFinance();

}



// =========================================================
// UI HELPERS
// =========================================================

function setLoading(
  active
) {

  loading.classList
    .toggle(
      "hidden",
      !active
    );

}



function showError(
  message
) {

  errorBox.textContent =
    message;


  errorBox.classList
    .remove(
      "hidden"
    );

}



let toastTimer;


function showToast(
  message
) {

  toast.textContent =
    message;


  toast.classList
    .remove(
      "hidden"
    );


  clearTimeout(
    toastTimer
  );


  toastTimer =
    setTimeout(
      () => {

        toast.classList
          .add(
            "hidden"
          );

      },
      2600
    );

}



function emptyState(
  text
) {

  return `
    <div class="empty">
      ${escapeHtml(text)}
    </div>
  `;

}



function setText(
  id,
  value
) {

  document
    .getElementById(id)
    .textContent =
      value;

}



function valueOf(id) {

  return document
    .getElementById(id)
    .value
    .trim();

}



// =========================================================
// MONEY
// =========================================================

function formatMoney(
  value
) {

  return new Intl
    .NumberFormat(
      "pt-BR",
      {
        style:
          "currency",
        currency:
          "BRL"
      }
    )
    .format(
      Number(
        value || 0
      )
    );

}



// =========================================================
// DATE
// =========================================================

function getCurrentMonth() {

  const now =
    new Date();


  return (
    `${now.getFullYear()}-` +
    `${String(
      now.getMonth() + 1
    ).padStart(
      2,
      "0"
    )}`
  );

}



function addMonths(
  referenceMonth,
  amount
) {

  const [
    year,
    month
  ] =
    referenceMonth
      .split("-")
      .map(Number);


  const date =
    new Date(
      year,
      month - 1 + amount,
      1
    );


  return (
    `${date.getFullYear()}-` +
    `${String(
      date.getMonth() + 1
    ).padStart(
      2,
      "0"
    )}`
  );

}



function todayLocal() {

  const now =
    new Date();


  const year =
    now.getFullYear();


  const month =
    String(
      now.getMonth() + 1
    )
      .padStart(
        2,
        "0"
      );


  const day =
    String(
      now.getDate()
    )
      .padStart(
        2,
        "0"
      );


  return (
    `${year}-${month}-${day}`
  );

}



function formatDate(
  value
) {

  if (!value) {
    return "";
  }


  const [
    year,
    month,
    day
  ] =
    value.split("-");


  return (
    `${day}/${month}/${year}`
  );

}



// =========================================================
// TEXT
// =========================================================

function escapeHtml(
  value
) {

  return String(
    value ?? ""
  )
    .replaceAll(
      "&",
      "&amp;"
    )
    .replaceAll(
      "<",
      "&lt;"
    )
    .replaceAll(
      ">",
      "&gt;"
    )
    .replaceAll(
      '"',
      "&quot;"
    )
    .replaceAll(
      "'",
      "&#039;"
    );

}



function capitalize(
  value
) {

  return String(
    value || ""
  )
    .split(" ")
    .map(word => {

      if (!word) {
        return "";
      }


      return (
        word.charAt(0)
          .toUpperCase() +
        word.slice(1)
      );

    })
    .join(" ");

}



// =========================================================
// GLOBAL FUNCTIONS
// =========================================================

window.toggleTask =
  toggleTask;


window.disableReminder =
  disableReminder;


window.deleteTask =
  deleteTask;


window.deleteStudy =
  deleteStudy;


window.deleteFinance =
  deleteFinance;
