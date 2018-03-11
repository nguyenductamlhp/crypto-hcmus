# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons.website.models.website import slug
import string
from datetime import datetime

class EncryptDecrypt(models.Model):

    _name = 'encrypt.decrypt'

    name = fields.Char("Name", required=True)
    mode = fields.Selection(
        string="Mode",
        selection=[
            ('ecb', 'ECB'),
            ('cfb', 'CFB'),
            ('ofb', 'OFB'),
            ('cbc', 'CBC'),
            ('ctr', 'CTR'),
        ]
    )
    encypt_text = fields.Text("Encypt Text")
    decrypt_text = fields.Text("Decrypt Text")

    def compute_result(self):
        objs = self.env['statisticter.vi'].search([('id', '=', active_id)])
        attch_env = self.env['ir.attachment']
        for rec in objs:
            table = '''
            <table style="width:100%">
                <tr>
                    <th>Letter</th>
                    <th>Percent (%)</th> 
                </tr>
            '''
            # Init result
            file_name = ''
            result = {}
            for i in string.ascii_lowercase:
                result[i] = 0
            datas = attch_env.search(
                [('res_model', '=', 'statisticter.vi'),
                 ('res_id', '=', rec.id)])
            if not datas:
                continue
            for char in datas.index_content:
                if char in result.keys():
                    result[char] = result[char] + 1
                file_name = file_name + char.name
            # Compute total
            total = 0
            for k in result.keys():
                total = total + result[k]
            # Compute 
            for k in result.keys():
                result[k] = round(100.0 * result[k] / total, 2)
                row = '''
                <tr>
                    <td>%s</td>
                    <td>%s</td> 
                </tr>
                ''' % (k, result[k])
                table = table + row
            table = table + '</table>'
            rec.table = table
            rec.description = file_name
