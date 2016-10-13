# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.update(
  DEBUG=True,
  SECRET_KEY='topsecret'
)
toolbar = DebugToolbarExtension(app)

@app.route('/')
def home(keywords=None):
    return render_template('home.html')
