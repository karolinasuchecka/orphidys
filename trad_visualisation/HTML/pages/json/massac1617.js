
            var auteurs_graphe = 
            {
            "data": [],
            "directed": false,
            "multigraph": false,
            "elements":
                {
                    "nodes": 
                    [
                    {"data": {"id" : "massac1617", "weight" : 2}},
            
                    {"data": {"id" : "banier1732", "weight" : 1}},
                
                    {"data": {"id" : "villenave1806", "weight" : 1}},
                
               ],
               "edges":
               [
               
                       {"data": {"id" : "banier1732_massac1617", "source": "massac1617", "target" : "banier1732", "weight" : 1}},
                   
                       {"data": {"id" : "villenave1806_massac1617", "source": "massac1617", "target" : "villenave1806", "weight" : 1}},
                   
                ]
                }
               };
            var liens_phrases =  {"data": [],
            "directed": false,
            "multigraph": true,
            "elements":
            {
            "nodes":
            [
            
                    {"data": {"id" : "2400017", "auteur" : "massac1617", "weight" : 2}},
                
                    {"data": {"id" : "0500024", "auteur" : "banier1732", "weight" : 1}},
                    
                    {"data": {"id" : "2400009", "auteur" : "massac1617", "weight" : 2}},
                
                    {"data": {"id" : "1800018", "auteur" : "villenave1806", "weight" : 1}},
                    
            ],
            "edges":
            [
                        {"data": {"id" : "0500024_2400017", "source": "2400017", "target" : "0500024", "weight" : 7, "auteur_source" : "massac1617", "auteur_target" : "banier1732"}},
                    
                        {"data": {"id" : "1800018_2400009", "source": "2400009", "target" : "1800018", "weight" : 13, "auteur_source" : "massac1617", "auteur_target" : "villenave1806"}},
                    
            ]
            }};
            
                    