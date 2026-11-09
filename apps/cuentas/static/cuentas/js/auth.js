
document.addEventListener("DOMContentLoaded", () => {

    const botones = document.querySelectorAll(
        ".password-toggle"
    );

    botones.forEach(boton => {

        boton.addEventListener("click", () => {

            const contenedor = boton.closest(
                ".input-wrapper"
            );

            const input = contenedor?.querySelector(
                "input"
            );

            if (!input) return;

            const mostrar = input.type === "password";

            input.type = mostrar ? "text" : "password";

            input.classList.toggle(
                "password-visible",
                mostrar
            );

            const icono = boton.querySelector(
                ".material-symbols-outlined"
            );

            if (icono) {
                icono.textContent = mostrar
                    ? "visibility_off"
                    : "visibility";
            }

            boton.setAttribute(
                "aria-label",
                mostrar
                    ? "Ocultar contraseña"
                    : "Mostrar contraseña"
            );

            boton.setAttribute(
                "aria-pressed",
                String(mostrar)
            );

        });

    });

});
