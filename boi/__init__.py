#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_assets import Environment, Bundle
from flask_session import Session
from boi.views import mod as boi_main


app = Flask(__name__)
app.config.from_object('boi.config.FlaskConfig')
Session(app)

app.register_blueprint(boi_main)

assets = Environment(app)
assets.register('img_favicon',
                Bundle('images/favicon.png', output='gen/favicon.png'))
assets.register('js_app',
                Bundle('js/app/kersulis-scatter_skin.v1.js',
                       filters='jsmin',
                       output='gen/js_app.js'))
