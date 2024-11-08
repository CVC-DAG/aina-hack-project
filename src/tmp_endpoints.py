from sentence_transformers import SentenceTransformer

GLOBAL_SBERT_CAT = SentenceTransformer("projecte-aina/ST-NLI-ca_paraphrase-multilingual-mpnet-base")
def produce_sbert_embedding_cat(query):
    return  GLOBAL_SBERT_CAT.encode(query).tolist()


