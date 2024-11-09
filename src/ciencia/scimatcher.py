from src.empreses.empreses import Empresa
from src.local_calls import call_embedding_model

import os
import json

from annoy import AnnoyIndex
import pickle
from typing import *
import numpy as np
import networkx as nx

import pdb

class SciMatcher:
    def __init__(self,  path_title: Tuple[str, str] = ("./", "./"),# type: ignore
                        path_abstract: Tuple[str, str] = ("./", "./"), # type: ignore
                        path_key_words: Tuple[str, str] = ("./", "./"),# type: ignore
                        path_graph: str = "./",
                        scimatcher_db = '../../data.json'):
        
        self.embeddings_path_title, self._look_up_table_path_title = path_title
        self.embeddings_path_abstract, self._look_up_table_path_abstract = path_abstract
        self.embeddings_path_key_words, self._look_up_table_path_key_words = path_key_words
        
        
        self.title_look_up_table = self.read_pickle(self._look_up_table_path_title)
        self.abstract_look_up_table = self.read_pickle(self._look_up_table_path_abstract)
        self.key_word_look_up_table = self.read_pickle(self._look_up_table_path_key_words)

        self.graph  = nx.read_graphml(path=path_graph)
        
        self.vdb_title = AnnoyIndex(768, 'angular')
        self.vdb_abstract = AnnoyIndex(768, 'angular')
        self.vdb_key_words = AnnoyIndex(768, 'angular')
            
        self.vdb_title.load(self.embeddings_path_title)
        self.vdb_key_words.load(self.embeddings_path_key_words)
        self.vdb_abstract.load(self.embeddings_path_abstract)

        self.path = scimatcher_db
        if os.path.exists(scimatcher_db):
            self.db = json.load(open(scimatcher_db))

        else:
            self.db = {}
            
    def read_pickle(self, filepath:str) -> Any:
        
        with open(filepath, "rb") as file:
            obj = pickle.load(file=file)
            
        return obj
    
    
         
    def compute_match(self, empresa: Empresa):
        # WHATEVER MATCHING IS DONE HERE FOR RELEVANT PAPERS AND AUTHORS
        retrieval_title = []
        retrieval_abstract = []
        retrieval_key_words = []
        
        query_results = empresa.query_vdb("resultats esperats", num_results=150)
        
        embeddings_to_search = [call_embedding_model(text)["output"] for text in query_results]
        
        for qemb in embeddings_to_search:
            title_best_matches, distances_title = self.vdb_title.get_nns_by_vector(qemb, 10, include_distances=True) 
            title_best_matches = self.title_look_up_table[title_best_matches]
            retrieval_title.extend(list(zip(title_best_matches, distances_title)))
            
            abstract_best_matches, distances_abstract = self.vdb_abstract.get_nns_by_vector(qemb, 10, include_distances=True)
            abstract_best_matches = self.abstract_look_up_table[abstract_best_matches]
            retrieval_abstract.extend(list(zip(abstract_best_matches, distances_abstract)))
            
            key_words_best_matches, distances_key_words = self.vdb_key_words.get_nns_by_vector(qemb, 10, include_distances=True)
            key_words_best_matches = self.key_word_look_up_table[key_words_best_matches]
            retrieval_key_words.extend(list(zip(key_words_best_matches, distances_key_words)))
            
        retrieval_abstract = sorted(retrieval_abstract, key= lambda x: x[1])
        retrieval_key_words = sorted(retrieval_key_words, key=lambda x: x[1])
        retrieval_title = sorted(retrieval_title, key=lambda x: x[1])
        
        final_retrieve = retrieval_abstract + retrieval_title + retrieval_key_words
        final_retrieve = sorted(final_retrieve, key=lambda x: x[1])
        
        best_match = final_retrieve[0][0]
        
        title_best_match = self.get_target_nodes_by_edge_type(str(best_match), 'title')[0]
        value_title = self.graph.nodes[title_best_match]["content"]
        
        best_abstract = self.get_target_nodes_by_edge_type(str(best_match), 'contain')[0]
        value_abstract = self.graph.nodes[best_abstract]["content"]
        
        best_context_match = f"The best context has been written by: {', '.join(self.get_target_nodes_by_edge_type(str(best_match), 'author'))} and the title is {value_title}\n"
        if len(self.get_target_nodes_by_edge_type(str(best_match), "has")) != 0:
            best_context_match += f"The publication contain the following keywords: {self.get_target_nodes_by_edge_type(str(best_match), 'has')}\n"
        
        if len(self.get_target_nodes_by_edge_type(str(best_match), 'contain')) != 0:
            best_context_match += f"And the abstract is:\n {value_abstract}"
        
        
        #self.db[empresa.url] = best_context_match
        #json.dump(self.db, open(self.path, 'w'))
        return best_context_match, self.get_target_nodes_by_edge_type(str(best_match), 'author')[0]
    
    
    def get_target_nodes_by_edge_type(self, node, edge_type):
        """
        Get target nodes connected to a given node with a specific type of edge.
        
        Parameters:
        - G (networkx.Graph): The graph containing the nodes and edges.
        - node: The node from which we want to get the target nodes.
        - edge_type (str): The type of edge to filter by (stored as an attribute on each edge).
        
        Returns:
        - List of target nodes connected to the given node by the specified edge type.
        """
        target_nodes = [
            neighbor for neighbor in self.graph.neighbors(node)
            if self.graph.edges[node, neighbor].get('relationship') == edge_type
        ]
        return target_nodes

    def get_match(self, empresa: Empresa):
        if empresa.vdb in self.db:
            return self.db['url']

        return self.compute_match(empresa)



