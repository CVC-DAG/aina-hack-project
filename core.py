from src.ciencia.scimatcher import SciMatcher
from src.empreses.empreses import Empresa
from src.common import *

from flask import Flask, render_template, request
import pandas as pd

import uuid

app = Flask(__name__, template_folder=TEMPLATES, static_folder=STATIC)
scimatcher = SciMatcher(SCIMATCHER_PATH)
record_empreses = pd.read_csv(EMPRESES_RECORD, names=['url', 'vdb', 'metadata'])
print(record_empreses)

empreses = [Empresa(url, None, None, vdb, meta) for (url, vdb, meta) in zip(record_empreses['url'],
                                                                            record_empreses['vdb'],
                                                                            record_empreses['metadata'])]
print(empreses)
@app.route("/upload_business/")
def upload_business_page():
    return render_template("upload_business.html")

@app.route("/submit_upload_business", methods=["POST"])
def process_upload_business():
    print("Requested upload of a business")
    print(request.form["url"])
    upload_business(request.form["url"])


    return "Success!"

def upload_business(business_url):
    global record_empreses
    record_empreses = pd.read_csv(EMPRESES_RECORD, names=['url', 'vdb', 'metadata'])

    if (record_empreses['url'] == business_url).any():
        return None
    vdb_path = f"data/{str(uuid.uuid4())}" + '.ann'
    metapath = f"data/{str(uuid.uuid4())}" + '.json'
    empresa_nova = Empresa(business_url, None, 10, vdbpath=vdb_path, metadata_path=metapath)

    with open(EMPRESES_RECORD, 'a+') as handler:
        handler.write(','.join([business_url, vdb_path, metapath]) + "\n")

    empreses.append(empresa_nova)

    return empreses[-1]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)



