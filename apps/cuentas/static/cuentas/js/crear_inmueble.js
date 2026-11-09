
document.addEventListener("DOMContentLoaded", () => {

    const selectorTipo = document.getElementById("id_tipo");

    const selectorZona = document.getElementById("id_id_zona");

    const grupos = document.querySelectorAll(".tipo-campos");

    const placeholder = document.getElementById(
        "tipo-placeholder"
    );

    if (!selectorTipo) return;

    function actualizarCampos() {

        const tipo = selectorTipo.value;

        grupos.forEach(grupo => {

            const corresponde = grupo.dataset.tipo === tipo;

            grupo.hidden = !corresponde;

            // Solo se envían los campos del tipo activo.
            grupo.querySelectorAll(
                "input, select, textarea"
            ).forEach(campo => {
                campo.disabled = !corresponde;
            });

        });

        if (placeholder) {
            placeholder.hidden = Boolean(tipo);
        }

        // MariaDB exige que una villa no tenga zona.
        if (selectorZona) {

            if (tipo === "VILLA") {
                selectorZona.value = "";
                selectorZona.disabled = true;
            } else {
                selectorZona.disabled = false;
            }

        }
    }

    selectorTipo.addEventListener(
        "change",
        actualizarCampos
    );

    actualizarCampos();

});
