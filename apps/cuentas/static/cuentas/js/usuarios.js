
document.addEventListener("DOMContentLoaded", () => {

    const formularios = document.querySelectorAll(
        ".form-accion"
    );

    const modal = document.getElementById(
        "modal-confirmacion"
    );

    const mensaje = document.getElementById(
        "modal-mensaje"
    );

    const botonConfirmar = document.getElementById(
        "modal-confirmar"
    );

    const botonCancelar = document.getElementById(
        "modal-cancelar"
    );

    if (!modal || !mensaje ||
        !botonConfirmar || !botonCancelar) {
        return;
    }

    let formularioSeleccionado = null;

    formularios.forEach(formulario => {

        formulario.addEventListener("submit", evento => {

            evento.preventDefault();

            formularioSeleccionado = formulario;

            const accion = formulario.dataset.accion;
            const usuario = formulario.dataset.usuario;

            mensaje.textContent =
                `¿Deseas ${accion} la cuenta "${usuario}"?`;

            modal.hidden = false;
            botonCancelar.focus();
        });
    });

    botonCancelar.addEventListener("click", () => {
        modal.hidden = true;
        formularioSeleccionado = null;
    });

    botonConfirmar.addEventListener("click", () => {

        if (formularioSeleccionado) {
            formularioSeleccionado.submit();
        }
    });

    modal.addEventListener("click", evento => {
        if (evento.target === modal) {
            modal.hidden = true;
            formularioSeleccionado = null;
        }
    });

    document.addEventListener("keydown", evento => {
        if (evento.key === "Escape" && !modal.hidden) {
            modal.hidden = true;
            formularioSeleccionado = null;
        }
    });

});
