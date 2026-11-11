
document.addEventListener("DOMContentLoaded", () => {

    const panel = document.querySelector(
        ".codigo-demostracion"
    );

    const codigo = document.getElementById(
        "codigo-recuperacion-demo"
    );

    const copiar = document.getElementById(
        "copiar-codigo-recuperacion"
    );

    const resultado = document.getElementById(
        "resultado-copiar-codigo"
    );

    const inputCodigo = document.querySelector(
        'input[name="codigo"]'
    );

    // Si no existe un código visible, no se abre el modal.
    if (!panel || !codigo) {
        return;
    }

    // Crear el contenedor del modal.
    const overlay = document.createElement("div");
    overlay.className = "recuperacion-modal-overlay";

    const dialogo = document.createElement("div");
    dialogo.className = "recuperacion-modal-dialog";

    dialogo.setAttribute("role", "dialog");
    dialogo.setAttribute("aria-modal", "true");
    dialogo.setAttribute(
        "aria-label",
        "Código temporal de recuperación"
    );

    // Trasladar el panel existente al modal.
    panel.parentNode.removeChild(panel);
    dialogo.appendChild(panel);

    // Botón para cerrar y continuar.
    const continuar = document.createElement("button");

    continuar.type = "button";
    continuar.className = (
        "boton boton-primario recuperacion-continuar"
    );

    continuar.textContent = "Continuar a verificación";

    dialogo.appendChild(continuar);
    overlay.appendChild(dialogo);
    document.body.appendChild(overlay);

    function cerrarModal() {
        overlay.remove();

        if (inputCodigo) {
            inputCodigo.focus();
        }
    }

    continuar.addEventListener("click", cerrarModal);

    // Copiar el código.
    if (copiar && resultado) {

        copiar.addEventListener("click", async () => {

            const valor = codigo.textContent.trim();

            try {
                await navigator.clipboard.writeText(valor);

                resultado.textContent = (
                    "Código copiado correctamente."
                );

            } catch (error) {
                resultado.textContent = (
                    "No se pudo copiar automáticamente. "
                    + "Selecciona el código y cópialo."
                );
            }

        });

    }

    // Cerrar mediante Escape.
    document.addEventListener("keydown", evento => {

        if (!overlay.isConnected) {
            return;
        }

        if (evento.key === "Escape") {
            cerrarModal();
        }

        // Mantener el foco dentro del diálogo.
        if (evento.key === "Tab") {

            const controles = [
                copiar,
                continuar
            ].filter(elemento => (
                elemento && !elemento.disabled
            ));

            const primero = controles[0];
            const ultimo = controles[controles.length - 1];

            if (
                evento.shiftKey &&
                document.activeElement === primero
            ) {
                evento.preventDefault();
                ultimo.focus();

            } else if (
                !evento.shiftKey &&
                document.activeElement === ultimo
            ) {
                evento.preventDefault();
                primero.focus();
            }
        }
    });

    continuar.focus();

});
