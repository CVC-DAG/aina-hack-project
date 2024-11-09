import json
from src.empreses.empreses import Empresa
from src.ciencia.scimatcher import SciMatcher

import src.local_calls as calls

def get_answers(empresa: Empresa, scimatcher: SciMatcher, nom_convocatoria: str, convocatories_data_path = 'src/convocatories/convocatories_data.json', max_context_length = 8000):
    # Get the relevant papers
    relevant_papers, author = scimatcher.get_match(empresa)
    # relevant_papers = ""
    # author = "Pau Torras"

    convocatoria = json.load(open(convocatories_data_path))
    convocatoria = convocatoria[nom_convocatoria]['slots']
    for slot in convocatoria:
        context = ""

        if slot['needs_business']:
            context += f"Dades de l'empresa:\nNom: {empresa.name}\n Pàgina Web: {empresa.url}\n\n" + " ".join(empresa.query_vdb(slot['search_query']))
        if slot['needs_science']:
            context += "Dades del centre d'investigació:\nNom: Centre de Visió per Computador\nNIF: Q5856375J\n\nArticles científics que has de tenir en compte (tradueix al català): " + relevant_papers
        if len(context) > max_context_length:
            context = context[:max_context_length]
        question = slot['system_prompt']
        model_prompt = f"Respon la pregunta amb la informació context que se't dona, si el context no te suficient informació per respondre digues 'no puc respondre'. Pregunta: {question}, Contexte: {context}"

        slot['answer'] = calls.call_salamandra(system_prompt="", prompt=model_prompt, temperature=0.0)['output']['content']
        #print(f"Answer for slot {slot['name']}: {slot['answer']}")

    return convocatoria, author
    

        