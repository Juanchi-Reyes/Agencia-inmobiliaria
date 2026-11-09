
from django.urls import path
from . import views

app_name = "inmuebles"

urlpatterns = [
    path("", views.lista_inmuebles, name="lista"),

    path(
        "gestion/",
        views.gestionar_inmuebles,
        name="gestionar"
    ),
    
    path(
    "acceder/",
    views.redireccion_inmuebles,
    name="acceder"
    ),
    
    path(
    "gestion/crear/",
    views.registrar_inmueble,
    name="crear"
    ),
    
    path(
    "gestion/<int:inmueble_id>/editar/",
    views.editar_inmueble,
    name="editar"
    ),
    
    path(
    "gestion/<int:inmueble_id>/eliminar/",
    views.borrar_inmueble,
    name="eliminar"
    ),
    
    # Gestión de ofertas comerciales

    path(
        "gestion/<int:inmueble_id>/ofertas/",
        views.listar_ofertas,
        name="ofertas"
    ),

    path(
        "gestion/<int:inmueble_id>/ofertas/crear/",
        views.registrar_oferta,
        name="crear_oferta"
    ),

    path(
        "gestion/ofertas/<int:oferta_id>/editar/",
        views.editar_oferta,
        name="editar_oferta"
    ),

    path(
        "gestion/ofertas/<int:oferta_id>/eliminar/",
        views.borrar_oferta,
        name="eliminar_oferta"
    ),
    
    path(
    "<int:inmueble_id>/",
    views.detalle_inmueble,
    name="detalle"
    ),


    # ============================================================
    # PROPIETARIOS
    # ============================================================

    path(
        "gestion/propietarios/",
        views.listar_propietarios,
        name="propietarios"
    ),

    path(
        "gestion/propietarios/crear/",
        views.registrar_propietario,
        name="crear_propietario"
    ),

    path(
        "gestion/propietarios/<int:propietario_id>/",
        views.detalle_propietario,
        name="detalle_propietario"
    ),

    path(
        "gestion/propietarios/<int:propietario_id>/editar/",
        views.editar_propietario,
        name="editar_propietario"
    ),

    path(
        "gestion/propietarios/<int:propietario_id>/eliminar/",
        views.borrar_propietario,
        name="eliminar_propietario"
    ),

    # ============================================================
    # ATRIBUTOS DE INMUEBLES
    # ============================================================

    path(
        "gestion/<int:inmueble_id>/atributos/",
        views.gestionar_atributos,
        name="gestionar_atributos"
    ),

    path(
        "gestion/<int:inmueble_id>/atributos/caracteristicas/agregar/",
        views.agregar_caracteristica,
        name="agregar_caracteristica"
    ),

    path(
        "gestion/<int:inmueble_id>/atributos/caracteristicas/<int:caracteristica_id>/editar/",
        views.modificar_caracteristica,
        name="modificar_caracteristica"
    ),

    path(
        "gestion/<int:inmueble_id>/atributos/caracteristicas/<int:caracteristica_id>/eliminar/",
        views.eliminar_caracteristica_asignada,
        name="eliminar_caracteristica_asignada"
    ),

    path(
        "gestion/<int:inmueble_id>/atributos/estancias/agregar/",
        views.agregar_estancia,
        name="agregar_estancia"
    ),

    path(
        "gestion/<int:inmueble_id>/atributos/estancias/<int:estancia_id>/editar/",
        views.modificar_estancia,
        name="modificar_estancia"
    ),

    path(
        "gestion/<int:inmueble_id>/atributos/estancias/<int:estancia_id>/eliminar/",
        views.eliminar_estancia_asignada,
        name="eliminar_estancia_asignada"
    ),

    # CATÁLOGOS GENERALES

    path(
        "gestion/atributos/catalogos/",
        views.catalogos_atributos,
        name="catalogos_atributos"
    ),

    path(
        "gestion/atributos/catalogos/caracteristicas/crear/",
        views.crear_caracteristica_catalogo,
        name="crear_caracteristica_catalogo"
    ),

    path(
        "gestion/atributos/catalogos/estancias/crear/",
        views.crear_estancia_catalogo,
        name="crear_estancia_catalogo"
    ),

    # ============================================================
    # GESTIÓN DE VISITAS
    # ============================================================

    path(
        "gestion/visitas/",
        views.listar_visitas,
        name="visitas"
    ),

    path(
        "gestion/visitas/crear/",
        views.registrar_visita,
        name="crear_visita"
    ),

    path(
        "gestion/visitas/<int:visita_id>/",
        views.detalle_visita,
        name="detalle_visita"
    ),

    path(
        "gestion/visitas/<int:visita_id>/editar/",
        views.editar_visita,
        name="editar_visita"
    ),

    path(
        "gestion/visitas/<int:visita_id>/eliminar/",
        views.borrar_visita,
        name="eliminar_visita"
    ),

    # ============================================================
    # CLIENTES
    # ============================================================

    path(
        "gestion/clientes/",
        views.listar_clientes,
        name="clientes"
    ),

    path(
        "gestion/clientes/crear/",
        views.registrar_cliente,
        name="crear_cliente"
    ),

    path(
        "gestion/clientes/<int:cliente_id>/",
        views.detalle_cliente,
        name="detalle_cliente"
    ),

    path(
        "gestion/clientes/<int:cliente_id>/editar/",
        views.editar_cliente,
        name="editar_cliente"
    ),

    path(
        "gestion/clientes/<int:cliente_id>/vincular/",
        views.vincular_cuenta_cliente,
        name="vincular_cuenta_cliente"
    ),

    path(
        "gestion/clientes/<int:cliente_id>/eliminar/",
        views.borrar_cliente,
        name="eliminar_cliente"
    ),

]
