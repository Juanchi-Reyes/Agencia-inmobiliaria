
document.addEventListener("DOMContentLoaded", () => {

    const formularios = document.querySelectorAll(
        ".form-eliminar-visita"
    );

    const modal = document.getElementById(
        "modal-eliminar-visita"
    );

    if (!modal || !formularios.length) {
        return;
    }

    const descripcion = document.getElementById(
        "descripcion-eliminar-visita"
    );

    const cancelar = document.getElementById(
        "cancelar-eliminar-visita"
    );

    const confirmar = document.getElementById(
        "confirmar-eliminar-visita"
    );

    let formularioSeleccionado = null;
    let botonOrigen = null;

    function cerrarModal() {
        modal.hidden = true;
        formularioSeleccionado = null;

        document.body.classList.remove("modal-abierto");

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

            descripcion.textContent = (
                formulario.dataset.descripcion || ""
            );

            confirmar.disabled = false;
            modal.hidden = false;

            document.body.classList.add("modal-abierto");
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
