# -*- coding: utf-8 -*-
# from odoo import http


# class InternBridge(http.Controller):
#     @http.route('/intern_bridge/intern_bridge', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/intern_bridge/intern_bridge/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('intern_bridge.listing', {
#             'root': '/intern_bridge/intern_bridge',
#             'objects': http.request.env['intern_bridge.intern_bridge'].search([]),
#         })

#     @http.route('/intern_bridge/intern_bridge/objects/<model("intern_bridge.intern_bridge"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('intern_bridge.object', {
#             'object': obj
#         })

