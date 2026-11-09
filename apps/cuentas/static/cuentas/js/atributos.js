
document.addEventListener("DOMContentLoaded", () => {

    const formularios = document.querySelectorAll(
        ".form-quitar-atributo"
    );

    const modal = document.getElementById(
        "modal-quitar-atributo"
    );

    if (!modal || !formularios.length) {
        return;
    }

    const titulo = document.getElementById(
        "titulo-quitar-atributo"
    );

    const nombre = document.getElementById(
        "nombre-atributo-eliminar"
    );

    const cancelar = document.getElementById(
        "cancelar-quitar-atributo"
    );

    const confirmar = document.getElementById(
        "confirmar-quitar-atributo"
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

        formulario.addEventListener("submit", evento => {

            evento.preventDefault();

            formularioSeleccionado = formulario;
            botonOrigen = evento.submitter;

            const tipo = formulario.dataset.tipo || "atributo";
            const nombreAtributo = formulario.dataset.nombre || "";

            titulo.textContent = `¿Quitar ${tipo}?`;
            nombre.textContent = nombreAtributo;

            confirmar.disabled = false;
            modal.hidden = false;

            document.body.classList.add(
                "modal-abierto"
            );

            cancelar.focus();
        });

    });

    cancelar.addEventListener("click", cerrarModal);

    confirmar.addEventListener("click", () => {

        if (!formularioSeleccionado) {
            return;
        }

        confirmar.disabled = true;
        formularioSeleccionado.submit();
    });

    modal.addEventListener("click", evento => {

        if (evento.target === modal) {
            cerrarModal();
        }
    });

    document.addEventListener("keydown", evento => {

        if (modal.hidden) {
            return;
        }

        if (evento.key === "Escape") {
            cerrarModal();
        }

        if (evento.key === "Tab") {

            const controles = [
                cancelar,
                confirmar
            ].filter(elemento => !elemento.disabled);

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
