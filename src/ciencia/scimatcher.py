from src.empreses.empreses import Empresa
from src.local_calls import call_embedding_model

import os
import json

from annoy import AnnoyIndex
import pickle
from typing import *
import numpy as np
import networkx as nx
import numpy as np
from collections import defaultdict
import random
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
        
        query_results = empresa.query_vdb("Tecnologies que busqueu desenvolupar", min_len=10, max_len=150, num_results=2000)
        
        if len(query_results) == 0:
            query_results = ["res"]
        
        embeddings_to_search = [call_embedding_model(text)["output"] for text in query_results]
        
        for qemb in embeddings_to_search:
            title_best_matches, distances_title = self.vdb_title.get_nns_by_vector(qemb, 20, include_distances=True) 
            title_best_matches = self.title_look_up_table[title_best_matches]
            retrieval_title.extend(list(zip(title_best_matches, distances_title)))
            
        retrieval_title = sorted(retrieval_title, key=lambda x: x[1])
        
        
        final_retrieve = self.merge_index_lists(retrieval_title)#retrieval_abstract + retrieval_title + retrieval_key_words
        final_retrieve = sorted(final_retrieve, key=lambda x: x[1])
        
        best_match = final_retrieve[0][0]
        similar_context = self.get_similar_titles(str(best_match))
        
        
        title_best_match = self.get_target_nodes_by_edge_type(str(best_match), 'title')
        if len(title_best_match) != 0:
            value_title = self.graph.nodes[title_best_match[0]]["content"]
        else:
            value_title = " "
            
        
        best_abstract = self.get_target_nodes_by_edge_type(str(best_match), 'contain')
        if len(best_abstract) != 0:
            value_abstract = self.graph.nodes[best_abstract[0]]["content"]
        else:
            value_abstract = " "
        
        best_context_match = f"L'article que més s'apropa al que busques ha estat escrit per : {', '.join(self.get_target_nodes_by_edge_type(str(best_match), 'author'))} i el seu títol és {value_title}\n"
        if len(self.get_target_nodes_by_edge_type(str(best_match), "has")) != 0:
            best_context_match += f"La publicació conté les següents paraules claus: {self.get_target_nodes_by_edge_type(str(best_match), 'has')}\n"
        
        if len(self.get_target_nodes_by_edge_type(str(best_match), 'contain')) != 0:
            best_context_match += f"i el seu abstract és:\n {value_abstract}"
        
        self.write_response(final_retrieve)
        
#        self.db[empresa.url] = best_context_match
#        json.dump(self.db, open(self.path, 'w'))
        
        return best_context_match, self.get_target_nodes_by_edge_type(str(best_match), 'author')[0]
    

    def get_similar_titles(self, publication_id, top_n=5):
        """
        Retrieve the top N titles similar to the title of the given publication.
        
        Parameters:
        - graph: A NetworkX graph where nodes represent publications and authors.
        - publication_id: The node ID of the publication to compare.
        - top_n: The number of similar titles to retrieve.
        
        Returns:
        - List of tuples (title, similarity_score) of the top N most similar titles.
        """
        # Step 1: Retrieve the title of the target publication
        target_title = self.extract_respose(publication_id, "title") #seself.get_target_nodes_by_edge_type() self.graph.nodes[publication_id].get('title', '')
        print(target_title)


        # Step 2: Navigate to connected authors and their other publications
        related_publications = set()
        for u, v, content in self.graph.edges(publication_id, data=True):
            if content["relationship"] == "author":
                for uu, vv, contentt in self.graph.edges(str(v),data=True):
                    if contentt["relationship"] == "author" and (vv != u):
                        related_publications.add(vv)
                        
        
        return random.sample(list(related_publications), top_n)
    

    def extract_respose(self, response, edge):
        title_best_match = self.get_target_nodes_by_edge_type(str(response), edge)
        if isinstance(title_best_match, list) and len(title_best_match) > 1:
            return title_best_match

        elif isinstance(title_best_match, list) and len(title_best_match) != 0:
            value_title = self.graph.nodes[title_best_match[0]]
            value_title = value_title.get("content")
            return value_title

        else:
            return "res"

    def write_response(self, list_reponses):
        

            
        top_responses = list_reponses[:10]
        json_response =  []
        for response in top_responses:
            sub_response = {
                
            }
            index_match = response[0]
            
            sub_response["title"] = self.extract_respose(index_match, "title")
            sub_response["keys"] = self.extract_respose(index_match, "has")
            sub_response["authors"] = self.extract_respose(index_match, "author")
            json_response.append(sub_response)
        
        self.write_json(data=json_response, filename="response.json")  
            
            
        
    def write_json(self, data, filename):
        """
        Write data to a JSON file.
        
        Parameters:
        - data: The data to write (can be a dictionary, list, etc.).
        - filename: The name of the file to write to, including the `.json` extension.
        """
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)  # `indent=4` for pretty-printing
            print(f"Data successfully written to {filename}")
        except Exception as e:
            print(f"An error occurred while writing JSON to {filename}: {e}")
            
    def merge_index_lists(self, *lists):
        # Step 1: Flatten all distances and compute softmax
        all_distances = [dist for lst in lists for _, dist in lst]
        softmax_distances = all_distances# np.exp(-np.array(all_distances)) / np.sum(np.exp(-np.array(all_distances))) # type: ignore
        
        # Step 2: Reassign normalized distances back to the (index, distance) pairs
        flattened_list = [pair for lst in lists for pair in lst]
        normalized_list = [(index, softmax_distances[i]) for i, (index, _) in enumerate(flattened_list)]
        
        # Step 3: Aggregate distances by index, multiplying for duplicates
        combined_distances = defaultdict(float)
        for idx, dist in normalized_list:
            if idx in combined_distances:
                combined_distances[idx] = (combined_distances[idx] * dist)/2  # Multiply for duplicates
            else:
                combined_distances[idx] = dist  # Set for the first occurrence
        
        # Step 4: Sort combined results by distance in ascending order and return
        sorted_combined = sorted(combined_distances.items(), key=lambda x: x[1])
        return sorted_combined
    
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



