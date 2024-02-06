# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class nutrete(models.Model):
#     _name = 'nutrete.nutrete'
#     _description = 'nutrete.nutrete'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class Cliente(models.Model):
    _name = 'nutrete.cliente'
    _description = 'Modelo para clientes'

    name = fields.Char(string='Nombre', required=True)
    dni = fields.Char(string='DNI')
    foto = fields.Image(string='Foto',max_width=200, max_height=200)
    historial = fields.Text(string='Historial')
    motivo_consulta = fields.Selection([
        ('cambiar_alimentacion', 'Cambiar hábitos alimenticios'),
        ('aprender_comer_sano', 'Aprender a comer sano'),
        ('aumentar_peso', 'Aumentar de peso'),
        ('asesoramiento_embarazo', 'Asesoramiento en embarazo o lactancia'),
        ('mejora_rendimiento_deportivo', 'Mejora de rendimiento deportivo'),
        ('leer_etiquetado_alimentos', 'Aprender a leer etiquetado de alimentos'),
        ('otros', 'Otros'),
    ], string='Motivo de Consulta')

class Dietista(models.Model):
    _name = 'nutrete.dietista'
    _description = 'Modelo para dietistas'

    name = fields.Char(string='Nombre', required=True)
    dni = fields.Char(string='DNI')
    foto = fields.Image(string='Foto',max_width=200, max_height=200)
    especialidad = fields.Selection([
        ('vegetariana', 'Dieta vegetariana'),
        ('paleo', 'Dieta paleo'),
        ('detox', 'Dieta detox'),
        ('hipocalorica', 'Dieta hipocalórica'),
        ('proteica', 'Dieta proteica'),
    ], string='Especialidad')

class Nutricionista(models.Model):
    _name = 'nutrete.nutricionista'
    _description = 'Modelo para nutricionistas'

    name = fields.Char(string='Nombre', required=True)
    dni = fields.Char(string='DNI')
    foto = fields.Image(string='Foto',max_width=200, max_height=200)
    especialidad = fields.Selection([
        ('deportiva', 'Nutrición deportiva'),
        ('pediatrica', 'Nutrición pediátrica'),
        ('clinica', 'Nutrición clínica'),
        ('otros', 'Otros'),
    ], string='Especialidad')

class Dieta(models.Model):
    _name = 'nutrete.dieta'
    _description = 'Modelo para dietas'

    #Un cliente tiene muchas dietas
    cliente_id = fields.Many2one('nutrete.cliente', string='Cliente', required=True)
    #un nutricionista puede tener muchas dietas para los clientes
    nutricionista_id = fields.Many2one('nutrete.nutricionista', string='Nutricionista')
    #un dietista tiene muchas dietas
    dietista_id = fields.Many2one('nutrete.dietista', string='Dietista')
    #Una dieta puede tener muchas revisiones
    revision_ids = fields.One2many('nutrete.revision', 'dieta_id', string='Revisiones')

class Revision(models.Model):
    _name = 'nutrete.revision'
    _description = 'Modelo para revisiones'

    fecha = fields.Date(string='Fecha', default=fields.Date.today)
    hora = fields.Float(string='Hora')    
    peso = fields.Float(string='Peso')
    comentarios = fields.Text(string='Comentarios del paciente')
    tipo_evolucion = fields.Selection([
        ('positiva', 'Positiva'),
        ('neutra', 'Neutra'),
        ('negativa', 'Negativa'),
    ], string='Tipo de Evolución')
    #una dieta puede tener muchas revisiones
    dieta_id = fields.Many2one('nutrete.dieta', string='Dieta', required=True)

class Taller(models.Model):
    _name = 'nutrete.taller'
    _description = 'Modelo para talleres'

    #Un nutricionista puede tener muchos talleres
    nutricionista_id = fields.Many2one('nutrete.nutricionista', string='Nutricionista', required=True)
    #lo mismo con un dietista
    dietista_id = fields.Many2one('nutrete.dietista', string='Dietista')
    fecha = fields.Date(string='Fecha')
    hora = fields.Float(string='Hora')
    tema = fields.Char(string='Tema')
    link_telematico = fields.Char(string='Link Telemático')
    #Un cliente puede tener muchos talleres, al igual que un taller puede tener muchos clientes
    clientes_asistentes = fields.Many2many('nutrete.cliente', string='Clientes')