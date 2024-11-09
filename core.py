import json
import uuid

from src.llm.get_answers import get_answers
from src.ciencia.scimatcher import SciMatcher
from src.empreses.empreses import Empresa
from src.common import *

from flask import Flask, render_template, request
import pandas as pd
import urllib.parse
from src.local_calls import call_salamandra

app = Flask(__name__, template_folder=TEMPLATES, static_folder=STATIC)
scimatcher = SciMatcher(path_abstract=(EMBEDDINGS_ABSTRACTS, LOOK_UP_TABLE_ABSTRACTS),
                        path_title=(EMBEDDINGS_TITLE, LOOK_UP_TABLE_TITLE),
                        path_key_words=(EMBEDDINGS_KEY_WORDS, LOOK_UP_TABLE_KEY_WORDS),
                        path_graph=GRAPH_PATH,
                        scimatcher_db=SCIMATCHER_PATH)
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
        handler.write("\n" + ','.join([business_url, vdb_path, metapath]))

    empreses[business_url] = empresa_nova

    return None

@app.route("/fill_selected_call", methods=["POST"])
def process_fill_call():
    print("FILL CALL PROCESS")

    answers, author = get_answers(empreses[request.form["url"]], scimatcher,  request.form["selected_form"])
    output = show_filled_form(answers, author)
    return output

def show_filled_form(answers, author):

    encoded_author = urllib.parse.quote(author)
    output =   f"""<section  id="graph_cerca">
        Cerca al Catàleg Científic:
      <iframe src="{GRAPH_NX_WEB}&n={encoded_author}"
              width="100%"
              height="400"
              style="border: none;">
      </iframe>
    </section>"""
    complete = True
    for ii, slot in enumerate(answers):
        output += f"<h3> {slot['name']} </h3>"
        output += f"<h4> {slot['explain']} </h4>"
        if "No puc".lower() in slot["answer"].lower():
            output += f'<textarea class="responseText" id="slot_{ii}" rows=10> Introdueixi més context </textarea>'
            complete = False
        else:
            output += f'<p class="fixedResponse" id="slot_{ii}"> {slot["answer"]} </p>'
    if not complete:
        print("NOT COMPLETE!")
        output += '<button type="button" onClick="javascript:submitRevision()" id="button_esmenes"> Envia Esmena amb context</button>'
    else:
        ...
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
    output += '<button type="button" onClick="javascript:submitWhichCall()" id="submit_button_ok">Emplena sol·licitud</button>'
    return output

def get_slot_index(slot_name):
    return int(slot_name.split("_")[-1])
@app.route('/esmenar/', methods=["POST"])
def process_esmenes():
    amendment_data = request.get_json()
    with open("src/convocatories/convocatories_data.json", "r") as f_convocatories:
        convs = json.load(f_convocatories)
        slots = convs[amendment_data["form"]]["slots"]

    answer = {}

    for slot_name, text in amendment_data["amendments"].items():
        slot_index = get_slot_index(slot_name)
        prompt = slots[slot_index]['system_prompt']
        generated = call_salamandra(f"Expandeix el text que s'adjunta a continuació amb text que s'adeqüi a la descripció següent: {prompt}", text, 0.0)["output"]["content"]
        slots[slot_index]["answer"] = generated

        answer[slot_name] = generated

    for slot_name, text in amendment_data["correct"].items():
        slot_index = get_slot_index(slot_name)
        slots[slot_index]["answer"] = text

    return answer

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



