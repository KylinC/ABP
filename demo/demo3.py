#!/usr/bin/env python
#encoding=utf-8

import sys
from flask import Blueprint, render_template, session, redirect, url_for, request, \
    Response, flash, g, jsonify, abort
import json

mod3 = Blueprint('demo3', __name__)

@mod3.route("/demo3")
def home3():
    return render_template('demo3.html')