import json
from src.empreses.empreses import Empresa
from src.ciencia.scimatcher import SciMatcher
from src.llm.get_answers import get_answers
from src.common import *

#empresa = Empresa('https://www.allread.ai/ca/', None, 20, vdbpath='data/allread.vdb', metadata_path='data/allread.json')
empresa = Empresa('https://www.lafoneria.com/ca/', None, 20, vdbpath='data/foneria.vdb', metadata_path='data/foneria.json')
scimatcher = SciMatcher(path_abstract=(EMBEDDINGS_ABSTRACTS, LOOK_UP_TABLE_ABSTRACTS),
                        path_title=(EMBEDDINGS_TITLE, LOOK_UP_TABLE_TITLE),
                        path_key_words=(EMBEDDINGS_KEY_WORDS, LOOK_UP_TABLE_KEY_WORDS),
                        path_graph=GRAPH_PATH,
                        scimatcher_db=SCIMATCHER_PATH)

nom_convocatoria = 'cupons' #'DiH4CAT'

save_path = f'{nom_convocatoria}_answers.json'
answers = get_answers(empresa, scimatcher, nom_convocatoria)
json.dump(answers, open(save_path, 'w'))
