
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
                'needs_business': True, # TODO: ARTEMIS M'HE QUEDAT AQUÍ
                'choose': ['Fabricació additiva/i3D Printing', 'Robòtica i manufactura avançada ( inclou realitat virtual i realitat augmentada o mixta,Cloud/Edge,Simulació i bessó digital)',
                           'Supercomputació i Quàntica', 'Supercomputació i Quàntica', 'Ciberseguretat', 'Intel·ligència artificial ( Inclou Big Data)']
            },
        ]
    }
}