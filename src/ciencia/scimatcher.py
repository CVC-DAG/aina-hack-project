import os
import json
from src.empreses.empreses import Empresa
class SciMatcher:
    def __init__(self, scimatcher_db = '../../data.json'):

        self.path = scimatcher_db
        if os.path.exists(scimatcher_db):
            self.db = json.load(open(scimatcher_db))

        else:
            self.db = {}

    def compute_match(self, empresa: Empresa):
        # WHATEVER MATCHING IS DONE HERE FOR RELEVANT PAPERS AND AUTHORS
        best_context_match = ''
        self.db[empresa.url] = best_context_match
        json.dump(self.db, open(self.path, 'w'))
        return best_context_match
    def get_match(self, empresa: Empresa):
        if empresa.vdb in self.db:
            return self.db['url']

        return self.compute_match(empresa)



