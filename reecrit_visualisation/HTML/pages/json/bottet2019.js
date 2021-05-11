
            var auteurs_graphe = 
            {
            "data": [],
            "directed": false,
            "multigraph": false,
            "elements":
                {
                    "nodes": 
                    [
                    {"data": {"id" : "bottet2019", "weight" : 3}},
            
                    {"data": {"id" : "bouchet1987", "weight" : 1}},
                
                    {"data": {"id" : "york1470", "weight" : 1}},
                
                    {"data": {"id" : "walleys1493", "weight" : 1}},
                
               ],
               "edges":
               [
               
                       {"data": {"id" : "bouchet1987_bottet2019", "source": "bottet2019", "target" : "bouchet1987", "weight" : 1}},
                   
                       {"data": {"id" : "york1470_bottet2019", "source": "bottet2019", "target" : "york1470", "weight" : 1}},
                   
                       {"data": {"id" : "walleys1493_bottet2019", "source": "bottet2019", "target" : "walleys1493", "weight" : 1}},
                   
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
            
                    {"data": {"id" : "2700026", "auteur" : "bottet2019", "weight" : 2}},
                
                    {"data": {"id" : "6900016", "auteur" : "bouchet1987", "weight" : 1}},
                    
                    {"data": {"id" : "2700039", "auteur" : "bottet2019", "weight" : 2}},
                
                    {"data": {"id" : "4300028", "auteur" : "york1470", "weight" : 1}},
                    
                    {"data": {"id" : "7400027", "auteur" : "walleys1493", "weight" : 1}},
                    
            ],
            "edges":
            [
                        {"data": {"id" : "6900016_2700026", "source": "2700026", "target" : "6900016", "weight" : 2, "auteur_source" : "bottet2019", "auteur_target" : "bouchet1987"}},
                    
                        {"data": {"id" : "4300028_2700039", "source": "2700039", "target" : "4300028", "weight" : 5, "auteur_source" : "bottet2019", "auteur_target" : "york1470"}},
                    
                        {"data": {"id" : "7400027_2700039", "source": "2700039", "target" : "7400027", "weight" : 5, "auteur_source" : "bottet2019", "auteur_target" : "walleys1493"}},
                    
            ]
            }};
            
                    