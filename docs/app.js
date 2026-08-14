// =========================================================
// CONFIGURAÇÃO
// =========================================================
const API_URL =
    "https://command-center-api.willpccamara.workers.dev";

const tg =
    window.Telegram?.WebApp;

let currentUser = null;


// =========================================================
// TELEGRAM
// =========================================================
function initTelegram() {

    if (!tg) {

        console.warn(
            "Mini App aberto fora do Telegram."
        );

        return;
    }


    tg.ready();

    tg.expand();


    try {

        tg.setHeaderColor(
            "#080b10"
        );

        tg.setBackgroundColor(
            "#080b10"
        );

    } catch (error) {

        console.warn(
            "Não foi possível aplicar as cores do Telegram.",
            error
        );
    }


    // Apenas visual.
    // A autenticação real vem do backend.
    const unsafeUser =
        tg.initDataUnsafe?.user;


    if (unsafeUser) {

        updateGreeting(
            unsafeUser
        );
    }
}


// =========================================================
// HEADER
// =========================================================
function updateGreeting(user) {

    const greeting =
        document.getElementById(
            "greeting"
        );

    const avatar =
        document.getElementById(
            "avatar"
        );


    if (
        greeting &&
        user?.first_name
    ) {

        greeting.textContent =
            `Olá, ${user.first_name}`;
    }


    if (
        avatar &&
        user?.first_name
    ) {

        avatar.textContent =
            user.first_name
                .charAt(0)
                .toUpperCase();
    }
}


// =========================================================
// AUTENTICAÇÃO
// =========================================================
async function authenticateMiniApp() {

    if (!tg) {

        console.warn(
            "Autenticação disponível apenas dentro do Telegram."
        );

        return null;
    }


    const initData =
        tg.initData;


    if (!initData) {

        console.error(
            "Telegram initData não encontrado."
        );

        showTelegramAlert(
            "Não foi possível identificar sua sessão do Telegram."
        );

        return null;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/auth/me`,
                {
                    method: "GET",

                    headers: {
                        "X-Telegram-Init-Data":
                            initData
                    }
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            console.error(
                "Falha de autenticação:",
                data
            );

            showTelegramAlert(
                data.error ||
                "Falha na autenticação."
            );

            return null;
        }


        currentUser =
            data.user;


        console.log(
            "Usuário autenticado:",
            currentUser
        );


        updateGreeting(
            currentUser
        );


        return currentUser;


    } catch (error) {

        console.error(
            "Erro ao conectar ao backend:",
            error
        );

        showTelegramAlert(
            "Não foi possível conectar ao Command Center."
        );

        return null;
    }
}


// =========================================================
// ENVIA MENSAGEM TESTE
// =========================================================
async function sendTelegramMessage(
    text
) {

    if (!tg) {

        console.error(
            "Telegram indisponível."
        );

        return false;
    }


    const initData =
        tg.initData;


    if (!initData) {

        return false;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/telegram/send`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "X-Telegram-Init-Data":
                            initData
                    },

                    body:
                        JSON.stringify({
                            text
                        })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            console.error(
                "Erro Telegram:",
                data
            );

            return false;
        }


        return true;


    } catch (error) {

        console.error(
            "Erro no envio:",
            error
        );

        return false;
    }
}


// =========================================================
// ALERTA
// =========================================================
function showTelegramAlert(
    message
) {

    if (tg?.showAlert) {

        tg.showAlert(
            message
        );

    } else {

        alert(
            message
        );
    }
}


// =========================================================
// NAVEGAÇÃO
// =========================================================
function setupNavigation() {

    const navItems =
        document.querySelectorAll(
            ".nav-item"
        );


    navItems.forEach(
        item => {

            item.addEventListener(
                "click",
                () => {

                    navItems.forEach(
                        nav => {

                            nav.classList.remove(
                                "active"
                            );
                        }
                    );


                    item.classList.add(
                        "active"
                    );


                    const page =
                        item.dataset.page;


                    console.log(
                        "Página:",
                        page
                    );


                    /*
                     * Próxima etapa:
                     *
                     * renderHome()
                     * renderFinance()
                     * renderTasks()
                     * renderStudies()
                     */

                    if (
                        page !== "home"
                    ) {

                        showTelegramAlert(
                            "Essa área será ativada na próxima etapa."
                        );
                    }
                }
            );
        }
    );
}


// =========================================================
// CHECK VISUAL DE TAREFA
// =========================================================
function setupTaskChecks() {

    const taskChecks =
        document.querySelectorAll(
            ".task-check"
        );


    taskChecks.forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    const task =
                        button.closest(
                            ".task"
                        );


                    const completed =
                        task.classList.toggle(
                            "completed"
                        );


                    if (completed) {

                        button.textContent =
                            "✓";

                        button.style.borderColor =
                            "#38d996";

                        button.style.color =
                            "#38d996";

                    } else {

                        button.textContent =
                            "";

                        button.style.borderColor =
                            "#596273";
                    }
                }
            );
        }
    );
}


// =========================================================
// NOVA TAREFA
// =========================================================
function setupNewTaskButton() {

    const button =
        document.getElementById(
            "newTaskButton"
        );


    if (!button) {
        return;
    }


    button.addEventListener(
        "click",
        () => {

            showTelegramAlert(
                "Na próxima etapa esse botão abrirá o formulário de nova tarefa."
            );
        }
    );
}


// =========================================================
// TESTE DE BACKEND
// =========================================================
async function testBackend() {

    try {

        const response =
            await fetch(
                API_URL
            );


        const data =
            await response.json();


        console.log(
            "Backend:",
            data
        );


        return data;


    } catch (error) {

        console.error(
            "Backend indisponível:",
            error
        );

        return null;
    }
}


// =========================================================
// INICIALIZAÇÃO
// =========================================================
async function startApp() {

    initTelegram();

    setupNavigation();

    setupTaskChecks();

    setupNewTaskButton();


    await testBackend();


    const user =
        await authenticateMiniApp();


    if (user) {

        console.log(
            "Command Center pronto."
        );
    }
}


// =========================================================
// START
// =========================================================
document.addEventListener(
    "DOMContentLoaded",
    startApp
);
