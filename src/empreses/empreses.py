from src.empreses.empreses_scraputils import crawl_business_web
import os
from annoy import AnnoyIndex
import json
from tqdm import tqdm

#from sentence_transformers import SentenceTransformer
#GLOBAL_SBERT_CAT = SentenceTransformer("projecte-aina/ST-NLI-ca_paraphrase-multilingual-mpnet-base")

import src.local_calls as calls

class Empresa:
    def __init__(self, url, name, depth, vdbpath = '../../data/vdb.ann', metadata_path = '../../data/data.json'):
        self.url = url
        self.name = name
        self.depth = depth

        if not os.path.exists(vdbpath):
            self.load_vdb_and_data(vdbpath, metadata_path)
        else:
            self.vdb = AnnoyIndex(768, 'angular')
            self.vdb.load(vdbpath)
            self.chunks = json.load(open(metadata_path))

    # @staticmethod
    # def produce_sbert_embedding_cat(query):
    #     # TODO: Cridar al codi del pau
    #     return GLOBAL_SBERT_CAT.encode(query).tolist()
    def load_vdb_and_data(self, vdpath, metadata_path):
        data = crawl_business_web(self.url, self.depth)
        print(f"Data scrapped with {len(data)} chunks.")
        ann_index = AnnoyIndex(768, 'angular')
        self.chunks = []

        for n, chunk in tqdm(enumerate(data), total = len(data)):

            chunk_data = vars(chunk)
            chunk_data['idx'] = n

            ann_index.add_item(n, self.produce_sbert_embedding_cat(chunk_data['text']))
            self.chunks.append(chunk_data)
        ann_index.build(10)
        ann_index.save(vdpath)
        json.dump({'chunks': self.chunks}, open(metadata_path, 'w'))

        self.vdb = ann_index
        self.chunks = {'chunks': self.chunks}

    def query_vdb(self, query, min_len=10, max_len=250, num_results=800):
        return set([self.chunks['chunks'][i]['text'] for i in self.vdb.get_nns_by_vector(calls.call_embedding_model(query)['output'], num_results) if len(self.chunks['chunks'][i]['text'].split(" ")) > min_len and len(self.chunks['chunks'][i]['text'].split(" ")) < max_len])

if __name__ == '__main__':
    empresa = Empresa('https://www.allread.ai/ca/', None, 20, vdbpath='../../data/allread.vdb', metadata_path='../../data/allread.json')
    print(empresa.query_vdb('Marçal'))