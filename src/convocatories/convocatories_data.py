
CONVOCATORIES = {
    'cupons': {

        'explain': '',
        'bases_reguladores': '',
        'slots': [{
            'name': 'Empresa Beneficiària',
            'explain': "Nom de l'empresa que sol·licita la tranferència.",
            'system_prompt': '',
            'needs_science': False,
            'needs_business': True
        },
        {
            'name': "1.1 Descripció de l'empresa i de l'activitat de l'empresa",
            'explain': "Sector i activitat principal de l'empresa.",
            'system_prompt': '',
            'needs_science': False,
            'needs_business': True
        },
        {
            'name': "1.2 Web de l'Empresa",
            'explain': "Idem",
            'system_prompt': '',
            'needs_science': False,
            'needs_business': True
        },
        {
            'name': "Xifres de negoci de l’empresa (tenint en compte totes les Unitats de Negoci)",
            'explain': "Idem",
            'system_prompt': '',
            'needs_science': False,
            'needs_business': True
        },

        {
            'name': "1.4. Resultat del test d’Autorientació digital del DIH4CAT",
            'explain': "Resultat del test d'autoorientació de la plataorma externa proporcionada per DIH4CAT",
            'system_prompt': '',
            'needs_science': False,
            'needs_business': True,
            'choose': ['Explorant', 'Competent', 'Expert', 'Líder']
        },
            {
                'name': "2.1. Títol descriptiu del servei",
                'explain': "Títol de l'activitat que l'empresa planteja solucionar amb el centre científic.",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': True
            },
            {
                'name': "2.2. Indicar quines tecnologies digitals avançades es contemplen en el servei d’assessorament pel testatge, experimentació i validació de l’ús i aplicació de les tecnologies digitals avançades (es pot marcar més d’una opció): ",
                'explain': "Tipus de tecnologies que es faran servir per duur a terme la tasca.",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': True,
                'choose': ['Fabricació additiva/i3D Printing', 'Robòtica i manufactura avançada ( inclou realitat virtual i realitat augmentada o mixta,Cloud/Edge,Simulació i bessó digital)',
                           'Supercomputació i Quàntica', 'Supercomputació i Quàntica', 'Ciberseguretat', 'Intel·ligència artificial ( Inclou Big Data)']
            },
            {
                'name': "2.3 Indicar el tipus de servei vinculat a l’assessorament (es pot marcar més d’una opció):",
                'explain': "Tipus de servei que es demana.",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': True,
                'choose': ['Estudis de viabilitat tecnològica', 'Anàlisis de nous models de negoci basats en l’ús de tecnologies digitals avançades.', 'Serveis de prova de concepte i validació de resultats.', 'Desenvolupament de prototips i pilots (testatge del producte o servei).']
            },
            {
                'name': '2.4.1. Descriure en què consistirà el servei a realitzar i l’abast del mateix. (es recomana un mínim de 8 línies)',
                'explain': "Descripció del servei que es demana.",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': True
            },
            {
                'name': '2.4.2. Descriure el repte principal i reptes associats que pretén resoldre l’empresa amb el testatge, experimentació i validació de l’ús i aplicació de les tecnologies digitals avançades',
                'explain': "Repte principal i reptes associats que es volen resoldre.",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': True
            },
            {
                'name': '2.4.3. Descriure quin tipus de resultats s’esperen del servei ( Els resultats obtinguts han de ser algun dels que s’indiquen en l’apartat 6 del annex 2 )',
                'explain': "Resultats esperats del servei.",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': True
            },
            {
                'name': '2.4.4. Llistar i descriure el/s lliurable/s previstos',
                'explain': "Lliurables previstos.",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': True
            },
            {
                'name': 'NIF del proveïdor',
                'explain': "NIF del centre de recerca",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': False
            },
            {
                'name': 'Indicar el tipus de vinculació amb un EDIH',
                'explain': "",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': False,
                'choose_model': ["membre d'un EDIH", 'entitat vinculada a un EDIH'],
                'choose': ['Membre d’un European Digital Innovation Hub que hagi estat seleccionat per la Comissió Europea per rebre finançament del programa Europa Digital', 'Entitat formalment vinculada a un European Digital Innovation Hub que hagi estat seleccionat per la Comissió Europea per rebre finançament del programa Europa Digital.']
            },
            {
                'name': 'Nom del EDIH',
                'explain': "Nom del EDIH al que està vinculat.",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': False
            },
            {
                'name': 'Nom de l’Entitat representant de l’EDIH',
                'explain': "Nom de l'entitat representant de l'EDIH",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': False
            },
            {
                'name': 'NIF de l’Entitat representant de l’EDIH',
                'explain': "NIF de l'entitat representant de l'EDIH",
                'system_prompt': '',
                'needs_science': True,
                'needs_business': False
            },
            {
                'name': '3.2. Descripció de les competències i coneixements experts del proveïdor relacionats amb el servei de testatge, experimentació i validació de tecnologia a prestar a l’empresa sol·licitant de l’ajut.',
                'explain': 'Competencies i coneixements del centre d\'investigació.',
                'system_prompt': '',
                'needs_science': True,
                'needs_business': False
            },
            {
                'name': '3.3. Experiència prèvia en la prestació de serveis especialitzats de digitalització a les empreses relacionats amb el servei de testatge, experimentació i validació de tecnologia a prestar a l’empresa sol·licitant de l’ajut.',
                'explain': 'Experiencia prèvia del centre d\'investigació.',
                'system_prompt': '',
                'needs_science': True,
                'needs_business': False
            },
            {
                'name': '3.4. Nom del servei ofert a través del European Digital Innovation Hub',
                'explain': 'Nom del servei ofert a través del EDIH.',
                'system_prompt': '',
                'needs_science': True,
                'needs_business': False
            },
            {
                'name': '3.5. Relació de les infraestructures i equipaments propis del proveïdor oferts a través del European Digital Innovation Hub relacionats amb el servei a prestar a l’empresa sol·licitant de l’ajut',
                'explain': 'Infraestructures i equipaments del centre d\'investigació.',
                'system_prompt': '',
                'needs_science': True,
                'needs_business': False
            },
            {
                'name': 'El cost subvencionable que es presenta és igual o superior a 15.000 €? (Indicar amb X una de les opcions proposades):',
                'explain': 'Cost subvencionable igual o major que 15000€',
                'system_prompt': '',
                'needs_science': False,
                'needs_business': True,
                'choose': ['Sí', 'No']
            },
            {
                'name': '4.2. Detall del pressupost',
                'explain': 'Pressupost del servei.',
                'system_prompt': '',
                'needs_science': False,
                'needs_business': True
            },
            
        ]
    }
}