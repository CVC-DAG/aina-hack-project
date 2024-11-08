from src.ciencia.scimatcher import SciMatcher
from src.empreses.empreses import Empresa
from src.common import *

from flask import Flask
import pandas as pd

app = Flask(__name__)
scimatcher = SciMatcher(SCIMATCHER_PATH)
record_empreses = pd.read_csv(EMPRESES_RECORD, names=['url', 'vdb', 'metadata'])
empreses = [Empresa(url, None, None, vdb, meta) for (url, vdb, meta) in []]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def upload_business():
    return None