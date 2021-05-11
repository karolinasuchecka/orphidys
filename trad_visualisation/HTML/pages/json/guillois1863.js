
            var auteurs_graphe = 
            {
            "data": [],
            "directed": false,
            "multigraph": false,
            "elements":
                {
                    "nodes": 
                    [
                    {"data": {"id" : "guillois1863", "weight" : 5}},
            
                    {"data": {"id" : "fournier1876", "weight" : 3}},
                
                    {"data": {"id" : "cabaret-dupaty1897", "weight" : 1}},
                
                    {"data": {"id" : "cournand1805", "weight" : 1}},
                
               ],
               "edges":
               [
               
                       {"data": {"id" : "fournier1876_guillois1863", "source": "guillois1863", "target" : "fournier1876", "weight" : 3}},
                   
                       {"data": {"id" : "cabaret-dupaty1897_guillois1863", "source": "guillois1863", "target" : "cabaret-dupaty1897", "weight" : 1}},
                   
                       {"data": {"id" : "cournand1805_guillois1863", "source": "guillois1863", "target" : "cournand1805", "weight" : 1}},
                   
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
            
                    {"data": {"id" : "1500001", "auteur" : "guillois1863", "weight" : 2}},
                
                    {"data": {"id" : "3000001", "auteur" : "fournier1876", "weight" : 1}},
                    
                    {"data": {"id" : "1500017", "auteur" : "guillois1863", "weight" : 2}},
                
                    {"data": {"id" : "3000016", "auteur" : "fournier1876", "weight" : 1}},
                    
                    {"data": {"id" : "1500019", "auteur" : "guillois1863", "weight" : 2}},
                
                    {"data": {"id" : "3000018", "auteur" : "fournier1876", "weight" : 1}},
                    
                    {"data": {"id" : "1500028", "auteur" : "guillois1863", "weight" : 2}},
                
                    {"data": {"id" : "2300023", "auteur" : "cabaret-dupaty1897", "weight" : 1}},
                    
                    {"data": {"id" : "1500035", "auteur" : "guillois1863", "weight" : 2}},
                
                    {"data": {"id" : "2200004", "auteur" : "cournand1805", "weight" : 1}},
                    
            ],
            "edges":
            [
                        {"data": {"id" : "3000001_1500001", "source": "1500001", "target" : "3000001", "weight" : 1, "auteur_source" : "guillois1863", "auteur_target" : "fournier1876"}},
                    
                        {"data": {"id" : "3000016_1500017", "source": "1500017", "target" : "3000016", "weight" : 3, "auteur_source" : "guillois1863", "auteur_target" : "fournier1876"}},
                    
                        {"data": {"id" : "3000018_1500019", "source": "1500019", "target" : "3000018", "weight" : 9, "auteur_source" : "guillois1863", "auteur_target" : "fournier1876"}},
                    
                        {"data": {"id" : "2300023_1500028", "source": "1500028", "target" : "2300023", "weight" : 5, "auteur_source" : "guillois1863", "auteur_target" : "cabaret-dupaty1897"}},
                    
                        {"data": {"id" : "2200004_1500035", "source": "1500035", "target" : "2200004", "weight" : 1, "auteur_source" : "guillois1863", "auteur_target" : "cournand1805"}},
                    
            ]
            }};
            
                    