# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Oficina(models.Model):
    id_oficina = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oficina'


class Zona(models.Model):
    id_zona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zona'


class Propietario(models.Model):
    id_propietario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'propietario'


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class Inmueble(models.Model):
    id_inmueble = models.AutoField(primary_key=True)
    referencia = models.CharField(unique=True, max_length=20)
    tipo = models.CharField(max_length=5)
    direccion = models.CharField(max_length=255)
    superficie_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    id_propietario = models.ForeignKey(Propietario, models.DO_NOTHING, db_column='id_propietario')
    id_oficina_gestion = models.ForeignKey(Oficina, models.DO_NOTHING, db_column='id_oficina_gestion')
    id_oficina_llaves = models.ForeignKey(Oficina, models.DB_SET_NULL, db_column='id_oficina_llaves', related_name='inmueble_id_oficina_llaves_set', blank=True, null=True)
    id_zona = models.ForeignKey(Zona, models.DO_NOTHING, db_column='id_zona', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inmueble'
        unique_together = (('id_inmueble', 'tipo'),)


class Oferta(models.Model):
    id_oferta = models.AutoField(primary_key=True)
    id_inmueble = models.ForeignKey(Inmueble, models.DB_CASCADE, db_column='id_inmueble')
    modalidad = models.CharField(max_length=8)
    precio = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    a_convenir = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'oferta'
        unique_together = (('id_inmueble', 'modalidad'),)


class Vivienda(models.Model):
    id_inmueble = models.OneToOneField(Inmueble, models.DB_CASCADE, db_column='id_inmueble', primary_key=True)
    tipo = models.ForeignKey(Inmueble, models.DB_CASCADE, db_column='tipo', to_field='tipo', related_name='vivienda_tipo_set')

    class Meta:
        managed = False
        db_table = 'vivienda'
        unique_together = (('id_inmueble', 'tipo'),)


class Piso(models.Model):
    id_inmueble = models.OneToOneField(Vivienda, models.DB_CASCADE, db_column='id_inmueble', primary_key=True)
    tipo = models.ForeignKey(Vivienda, models.DB_CASCADE, db_column='tipo', to_field='tipo', related_name='piso_tipo_set')
    estado = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'piso'


class Casa(models.Model):
    id_inmueble = models.OneToOneField(Vivienda, models.DB_CASCADE, db_column='id_inmueble', primary_key=True)
    tipo = models.ForeignKey(Vivienda, models.DB_CASCADE, db_column='tipo', to_field='tipo', related_name='casa_tipo_set')

    class Meta:
        managed = False
        db_table = 'casa'


class Villa(models.Model):
    id_inmueble = models.OneToOneField(Vivienda, models.DB_CASCADE, db_column='id_inmueble', primary_key=True)
    tipo = models.ForeignKey(Vivienda, models.DB_CASCADE, db_column='tipo', to_field='tipo', related_name='villa_tipo_set')
    superficie_parcela_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    urbanizacion = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'villa'


class Local(models.Model):
    id_inmueble = models.OneToOneField(Inmueble, models.DB_CASCADE, db_column='id_inmueble', primary_key=True)
    tipo = models.ForeignKey(Inmueble, models.DB_CASCADE, db_column='tipo', to_field='tipo', related_name='local_tipo_set')
    numero_puertas = models.IntegerField(blank=True, null=True)
    es_diafano = models.IntegerField(blank=True, null=True)
    esta_acondicionado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'local'


class Estancia(models.Model):
    id_estancia = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'estancia'


class ViviendaEstancia(models.Model):
    pk = models.CompositePrimaryKey('id_inmueble', 'id_estancia')
    id_inmueble = models.ForeignKey(Vivienda, models.DB_CASCADE, db_column='id_inmueble')
    id_estancia = models.ForeignKey(Estancia, models.DO_NOTHING, db_column='id_estancia')
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vivienda_estancia'


class Caracteristica(models.Model):
    id_caracteristica = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'caracteristica'


class InmuebleCaracteristica(models.Model):
    pk = models.CompositePrimaryKey('id_inmueble', 'id_caracteristica')
    id_inmueble = models.ForeignKey(Inmueble, models.DB_CASCADE, db_column='id_inmueble')
    id_caracteristica = models.ForeignKey(Caracteristica, models.DO_NOTHING, db_column='id_caracteristica')
    detalle = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inmueble_caracteristica'


class Visita(models.Model):
    id_visita = models.AutoField(primary_key=True)
    id_inmueble = models.ForeignKey(Inmueble, models.DO_NOTHING, db_column='id_inmueble')
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    fecha_hora = models.DateTimeField()
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visita'
