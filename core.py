import json
import uuid

from src.llm.get_answers import get_answers
from src.ciencia.scimatcher import SciMatcher
from src.empreses.empreses import Empresa
from src.common import *

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, template_folder=TEMPLATES, static_folder=STATIC)
scimatcher = SciMatcher(SCIMATCHER_PATH)
record_empreses = pd.read_csv(EMPRESES_RECORD, names=['url', 'vdb', 'metadata'])
print(record_empreses)


def load_empreses():
    return {url: Empresa(url, None, None, vdb, meta)
                for (url, vdb, meta) in zip(
                    record_empreses['url'],
                    record_empreses['vdb'],
                    record_empreses['metadata'])
                }
empreses = load_empreses()
print(empreses)
@app.route("/upload_business/")
def upload_business_page():
    return render_template("upload_business.html")

@app.route("/submit_upload_business", methods=["POST"])
def process_upload_business():
    print("Requested upload of a business")
    print(request.form["url"])
    upload_business(request.form["url"])

    return show_project_calls()

def upload_business(business_url):
    global record_empreses
    global empreses

    record_empreses = pd.read_csv(EMPRESES_RECORD, names=['url', 'vdb', 'metadata'])
    empreses = load_empreses()

    if (record_empreses['url'] == business_url).any():
        return None
    vdb_path = f"data/{str(uuid.uuid4())}" + '.ann'
    metapath = f"data/{str(uuid.uuid4())}" + '.json'
    empresa_nova = Empresa(business_url, None, 10, vdbpath=vdb_path, metadata_path=metapath)

    with open(EMPRESES_RECORD, 'a+') as handler:
        handler.write(','.join([business_url, vdb_path, metapath]) + "\n")

    empreses[business_url] = empresa_nova

    return empreses[-1]

@app.route("/fill_selected_call", methods=["POST"])
def process_fill_call():
    print("FILL CALL PROCESS")

    answers, author = get_answers(empreses[request.form["url"]], scimatcher,  request.form["selected_form"])
    output = show_filled_form(answers)
    return output

def show_filled_form(answers):
    output = ""
    for slot in answers:
        output += f"<h3> {slot['name']} </h3>"
        output += f"<h4> {slot['explain']} </h4>"
        output += f'<textarea class="responseText" rows=10>{slot["answer"]}<textarea/>'
    return output


REQUIRED_FIELDS = [
    "obertura",
    "tancament",
    "convoca",
    "tipus",
    "pressupost",
]

def show_project_calls():
    with open("src/convocatories/convocatories_data.json", "r") as f_convocatories:
        data = json.load(f_convocatories)
    output = "<table>"
    output += create_call_header()

    output += "<tbody>"
    for ii, (name, call) in enumerate(data.items()):
        metadata = call["metadata"]
        output += create_call_row(name, metadata, ii==0)
    output += "</tbody></table>"
    output += '<button type="button" onClick="javascript:submitWhichCall()">Emplena sol·licitud</button>'
    return output

def create_call_header():
    output = """<thead><tr>"""
    output += f"<th scope='col'>Selecció</th>"
    output += f"<th scope='col'>Nom</th>"
    for field in REQUIRED_FIELDS:
        capitalised = field[0].upper() + field[1:]
        output += f"<th scope='col'>{capitalised}</th>"
    output += """</tr></thead>"""
    return output

def create_call_row(nom, metadata, checked):
    output = """<tr>"""
    output += f'<td><input type="radio" id="conv_select_{nom}" name="conv_select" value="{nom}" {"checked" if checked else ""}/></td>'
    output += f"<td>{nom}</td>"
    for field in REQUIRED_FIELDS:
        output += f"<td>{metadata[field]}</td>"
    output += """</tr></thead>"""
    return output


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)



