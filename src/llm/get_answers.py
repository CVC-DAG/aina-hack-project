from src.empreses.empreses import Empresa
from src.ciencia.scimatcher import SciMatcher

import src.model_calls as calls

def get_answers(empresa: Empresa, scimatcher: SciMatcher, nom_convocatoria: str):
    # Get the relevant papers
    relevant_papers = scimatcher.get_match(empresa)

    convocatoria = convocatoria[nom_convocatoria]['slots']
    for slot in convocatoria:
        if slot['needs_science']
    