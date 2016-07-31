from app import app
from flask import Flask, render_template, redirect, request, url_for, session

@app.route('/')
def home():
  return render_template("index.html", title="Homepage")

