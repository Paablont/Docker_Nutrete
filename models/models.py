# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError



class Cliente(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
   
    dni = fields.Char(string='DNI')    
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
    talleres_apuntados = fields.Many2many(comodel_name="nutrete.taller",
                                           relation="taller_clientes",
                                           colum1="cliente_id",
                                           colum2="taller_id")
    
    #Restriccion para que el DNI tenga que ser válido y UNICO en SQL
    @api.constrains('dni')
    def _check_code(self):
       regex = re.compile('^[0-9]{8}[a-z]', re.I)
       for cl in self:
            if not regex.match(cl.dni):
                raise ValidationError('Formato de DNI incorrecto. Formato de DNI: 8 números y 1 letra')               
            
    _sql_constraints = [('dni_unique', 'unique(dni)', 'DNI ya existente.')]      

class Dietista(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    dni = fields.Char(string='DNI')
    
    especialidad = fields.Selection([
        ('vegetariana', 'Dieta vegetariana'),
        ('paleo', 'Dieta paleo'),
        ('detox', 'Dieta detox'),
        ('hipocalorica', 'Dieta hipocalórica'),
        ('proteica', 'Dieta proteica'),
    ], string='Especialidad')

    #Restriccion para que el DNI tenga que ser válido y UNICO en SQL
    @api.constrains('dni')
    def _check_code(self):
        regex = re.compile('^[0-9]{8}[a-z]', re.I)
        for diet in self:
            if not regex.match(diet.dni):
                raise ValidationError('Formato de DNI incorrecto. Formato de DNI: 8 números y 1 letra')               
            
    _sql_constraints = [('dni_unique', 'unique(dni)', 'DNI ya existente.')] 

class Nutricionista(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    
    dni = fields.Char(string='DNI')
    especialidad = fields.Selection([
        ('deportiva', 'Nutrición deportiva'),
        ('pediatrica', 'Nutrición pediátrica'),
        ('clinica', 'Nutrición clínica'),
        ('otros', 'Otros'),
    ], string='Especialidad')

    #Restriccion para que el DNI tenga que ser válido y UNICO en SQL
    @api.constrains('dni')
    def _check_code(self):
        regex = re.compile('^[0-9]{8}[a-z]', re.I)
        for diet in self:
            if not regex.match(diet.dni):
                raise ValidationError('Formato de DNI incorrecto. Formato de DNI: 8 números y 1 letra')               
            
    _sql_constraints = [('dni_unique', 'unique(dni)', 'DNI ya existente.')] 

class Dieta(models.Model):
    _name = 'nutrete.dieta'
    _description = 'Modelo para dietas'
    #Campo computado para calcular el peso promedio de todas las revisiones que tiene esa dieta
    peso_promedio_revisiones = fields.Float(string='Peso Promedio de Revisiones', compute='_compute_peso_promedio_revisiones')

    #Un cliente tiene muchas dietas
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    #un nutricionista puede tener muchas dietas para los clientes
    nutricionista_id = fields.Many2one('res.partner', string='Nutricionista')
    #un dietista tiene muchas dietas
    dietista_id = fields.Many2one('res.partner', string='Dietista')
    #Una dieta puede tener muchas revisiones
    revision_ids = fields.One2many('nutrete.revision', 'dieta_id', string='Revisiones')
    
    @api.depends('revision_ids.peso')
    def _compute_peso_promedio_revisiones(self):
        for dieta in self:
            try:
                if dieta.revision_ids:
                    peso_total = sum(rev.peso for rev in dieta.revision_ids)
                    dieta.peso_promedio_revisiones = peso_total / len(dieta.revision_ids)
                else:
                    dieta.peso_promedio_revisiones = 0.0
            except ZeroDivisionError:
                dieta.peso_promedio_revisiones = 0.0


class Revision(models.Model):
    _name = 'nutrete.revision'
    _description = 'Modelo para revisiones'

    fecha = fields.Date(string='Fecha')
    #Campo computado (Proxima revision, en 1 mes)
    proxima_revision = fields.Date(string='Proxima revision', compute="_prox_revision", store=True)
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
    #Una revision puede tener 1 cliente:
    cliente_id = fields.Many2one('res.partner', string='Cliente', store=True)
    
    @api.depends('fecha')
    def _prox_revision(self):
        for rev in self:
            try:
                if rev.fecha:
                    rev.proxima_revision = rev.fecha + datetime.timedelta(days=31)
            except Exception as e:
                raise ValidationError(f"Error al calcular la próxima revisión: {e}")
            
    #Restriccion para no poder poner peso negativo
    @api.constrains('peso')
    def _check_peso(self):
        for rev in self:
            if rev.peso < 0:
                raise ValidationError("El peso no puede ser negativo.")

    


class Taller(models.Model):
    _name = 'nutrete.taller'
    _description = 'Modelo para talleres'

    #Un nutricionista puede tener muchos talleres
    nutricionista_id = fields.Many2one('res.partner', string='Nutricionista', required=True)
    #lo mismo con un dietista
    dietista_id = fields.Many2one('res.partner', string='Dietista')
    fecha = fields.Date(string='Fecha')
    hora = fields.Float(string='Hora')
    tema = fields.Char(string='Tema')
    link_telematico = fields.Char(string='Link Telemático')
    #Un cliente puede tener muchos talleres, al igual que un taller puede tener muchos clientes
    clientes_asistentes = fields.Many2many(comodel_name="res.partner",
                                           relation="taller_clientes",
                                           colum1="taller_id",
                                           colum2="cliente_id")