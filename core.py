from src.ciencia.scimatcher import SciMatcher
from src.empreses.empreses import Empresa
from src.common import *

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder=TEMPLATES, static_folder=STATIC)
scimatcher = SciMatcher(SCIMATCHER_PATH)
record_empreses = pd.read_csv(EMPRESES_RECORD, names=['url', 'vdb', 'metadata'])
print(record_empreses)

empreses = [Empresa(url, None, None, vdb, meta) for (url, vdb, meta) in zip(record_empreses['url'],
                                                                            record_empreses['vdb'],
                                                                            record_empreses['metadata'])]
print(empreses)
@app.route("/upload_business/")
def upload_business():
    return render_template("upload_business.html")

def upload_business(business_url):
    vdb_path = business_url.split('.')[0] + '.ann'
    metapath = business_url.split('.')[0] + '.json'
    empresa_nova = Empresa(business_url, None, 10, vdbpath=vdb_path, metadata_path=metapath)

    with open(EMPRESES_RECORD, 'a+') as handler:
        handler.write(','.join([business_url, vdb_path, empresa_nova]))

    empreses.append(empresa_nova)

    return empreses[-1]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)



