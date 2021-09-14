from flask import Flask, render_template, request
from flask import Blueprint

contact = Blueprint("contact", __name__, url_prefix="/contact")

# contact
@contact.route("")
def index():
  return 'test'

