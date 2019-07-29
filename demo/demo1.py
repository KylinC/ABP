#!/usr/bin/env python
#encoding=utf-8

import sys
from flask import Blueprint, render_template, session, redirect, url_for, request, \
    Response, flash, g, jsonify, abort
import json

mod1 = Blueprint('demo1', __name__)
@mod1.route("/demo1")
def home1():
    return render_template('demo1.html')
