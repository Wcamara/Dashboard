const tg = window.Telegram?.WebApp;


/* =========================================================
   TELEGRAM
========================================================= */

if (tg) {

    tg.ready();

    tg.expand();

    // Mantém o fundo compatível com o Mini App
    tg.setHeaderColor("#080b10");
    tg.setBackgroundColor("#080b10");


    const user =
        tg.initDataUnsafe?.user;


    if (user) {

        const greeting =
            document.getElementById(
                "greeting"
            );

        const avatar =
            document.getElementById(
                "avatar"
            );


        if (user.first_name) {

            greeting.textContent =
                `Olá, ${user.first_name}`;

            avatar.textContent =
                user.first_name
                    .charAt(0)
                    .toUpperCase();
        }
    }
}


/* =========================================================
   NAVEGAÇÃO
========================================================= */

const navItems =
    document.querySelectorAll(
        ".nav-item"
    );


navItems.forEach((item) => {

    item.addEventListener(
        "click",
        () => {

            navItems.forEach(
                (nav) => {
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
                "Abrir página:",
                page
            );

            /*
             * Na próxima etapa:
             *
             * home
             * finance
             * tasks
             * studies
             *
             * serão páginas reais.
             */
        }
    );

});


/* =========================================================
   CHECK DE TAREFA
========================================================= */

const taskChecks =
    document.querySelectorAll(
        ".task-check"
    );


taskChecks.forEach((button) => {

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

                button.textContent = "✓";

                button.style.borderColor =
                    "#38d996";

                button.style.color =
                    "#38d996";

            } else {

                button.textContent = "";

                button.style.borderColor =
                    "#596273";
            }

        }
    );

});


/* =========================================================
   NOVA TAREFA
========================================================= */

const newTaskButton =
    document.getElementById(
        "newTaskButton"
    );


if (newTaskButton) {

    newTaskButton.addEventListener(
        "click",
        () => {

            if (tg) {

                tg.showAlert(
                    "Na próxima etapa vamos criar o formulário de nova tarefa."
                );

            } else {

                alert(
                    "Na próxima etapa vamos criar o formulário de nova tarefa."
                );
            }

        }
    );
}
