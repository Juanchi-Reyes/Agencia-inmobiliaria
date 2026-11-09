
document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById(
        "modal-eliminar-inmueble"
    );

    const referenciaTexto = document.getElementById(
        "referencia-eliminar"
    );

    const botonCancelar = document.getElementById(
        "cancelar-eliminacion"
    );

    const botonConfirmar = document.getElementById(
        "confirmar-eliminacion"
    );

    if (
        !modal ||
        !referenciaTexto ||
        !botonCancelar ||
        !botonConfirmar
    ) {
        return;
    }

    const dialogo = modal.querySelector(
        ".modal-eliminar-contenido"
    );

    const formularios = document.querySelectorAll(
        ".form-eliminar-inmueble"
    );

    let formularioSeleccionado = null;
    let botonOrigen = null;

    function cerrarModal() {

        modal.hidden = true;
        formularioSeleccionado = null;

        document.body.classList.remove(
            "modal-abierto"
        );

        if (botonOrigen) {
            botonOrigen.focus();
            botonOrigen = null;
        }
    }

    formularios.forEach(formulario => {

        formulario.addEventListener(
            "submit",
            (evento) => {

                evento.preventDefault();

                formularioSeleccionado = formulario;
                botonOrigen = evento.submitter;

                const referencia = (
                    formulario.dataset.referencia || ""
                );

                referenciaTexto.textContent = referencia;

                modal.hidden = false;

                document.body.classList.add(
                    "modal-abierto"
                );

                botonCancelar.focus();
            }
        );

    });

    botonCancelar.addEventListener(
        "click",
        cerrarModal
    );

    botonConfirmar.addEventListener(
        "click",
        () => {

            if (!formularioSeleccionado) {
                return;
            }

            botonConfirmar.disabled = true;

            // Envía el formulario original con su CSRF.
            formularioSeleccionado.submit();
        }
    );

    modal.addEventListener("click", (evento) => {

        if (evento.target === modal) {
            cerrarModal();
        }

    });

    document.addEventListener("keydown", (evento) => {

        if (modal.hidden) return;

        if (evento.key === "Escape") {
            cerrarModal();
        }

        // Mantener el foco dentro de la ventana.
        if (evento.key === "Tab") {

            const controles = [
                botonCancelar,
                botonConfirmar
            ].filter(elemento => !elemento.disabled);

            if (controles.length === 0) {
                evento.preventDefault();
                return;
            }

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

});
