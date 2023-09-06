from app.main import main
from config import Config
from flask import Flask, render_template, request, redirect, url_for, send_from_directory


@main.route("/")
def home():
    return #render_template('index.html')

@main.route("/test")
def test_data():
    return render_template('index.html')
