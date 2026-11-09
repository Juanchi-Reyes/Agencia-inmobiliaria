
document.addEventListener("DOMContentLoaded", () => {

    // ==========================================
    // FORMULARIO DE OFERTAS
    // ==========================================

    const modalidad = document.getElementById(
        "id_modalidad"
    );

    const precio = document.getElementById(
        "id_precio"
    );

    const aConvenir = document.getElementById(
        "id_a_convenir"
    );

    function actualizarFormulario() {

        if (!modalidad || !precio || !aConvenir) {
            return;
        }

        const esVenta = modalidad.value === "VENTA";

        if (!esVenta) {
            aConvenir.checked = false;
        }

        aConvenir.disabled = !esVenta;

        if (aConvenir.checked) {
            precio.value = "";
            precio.disabled = true;
        } else {
            precio.disabled = false;
        }
    }

    if (modalidad && precio && aConvenir) {

        modalidad.addEventListener(
            "change",
            actualizarFormulario
        );

        aConvenir.addEventListener(
            "change",
            actualizarFormulario
        );

        actualizarFormulario();
    }

    // ==========================================
    // MODAL PARA ELIMINAR OFERTAS
    // ==========================================

    const modal = document.getElementById(
        "modal-eliminar-oferta"
    );

    if (!modal) {
        return;
    }

    const textoModalidad = document.getElementById(
        "modalidad-oferta-eliminar"
    );

    const botonCancelar = document.getElementById(
        "cancelar-eliminar-oferta"
    );

    const botonConfirmar = document.getElementById(
        "confirmar-eliminar-oferta"
    );

    const formularios = document.querySelectorAll(
        ".form-eliminar-oferta"
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
            evento => {

                evento.preventDefault();

                formularioSeleccionado = formulario;
                botonOrigen = evento.submitter;

                textoModalidad.textContent = (
                    formulario.dataset.modalidad || ""
                );

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

            formularioSeleccionado.submit();
        }
    );

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
                botonCancelar,
                botonConfirmar
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

