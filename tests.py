import json
from src.empreses.empreses import Empresa
from src.ciencia.scimatcher import SciMatcher
from src.llm.get_answers import get_answers

empresa = Empresa('https://www.allread.ai/ca/', None, 20, vdbpath='data/allread.vdb', metadata_path='data/allread.json')
scimatcher = None

nom_convocatoria = 'DiH4CAT'

save_path = f'{nom_convocatoria}_answers.json'
answers = get_answers(empresa, scimatcher, nom_convocatoria)
json.dump(answers, open(save_path, 'w'))
