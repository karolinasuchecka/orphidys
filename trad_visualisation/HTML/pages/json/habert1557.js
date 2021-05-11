
            var auteurs_graphe = 
            {
            "data": [],
            "directed": false,
            "multigraph": false,
            "elements":
                {
                    "nodes": 
                    [
                    {"data": {"id" : "habert1557", "weight" : 2}},
            
                    {"data": {"id" : "fontanelle1789", "weight" : 1}},
                
                    {"data": {"id" : "martignac1697", "weight" : 1}},
                
               ],
               "edges":
               [
               
                       {"data": {"id" : "fontanelle1789_habert1557", "source": "habert1557", "target" : "fontanelle1789", "weight" : 1}},
                   
                       {"data": {"id" : "martignac1697_habert1557", "source": "habert1557", "target" : "martignac1697", "weight" : 1}},
                   
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
            
                    {"data": {"id" : "3500020", "auteur" : "habert1557", "weight" : 2}},
                
                    {"data": {"id" : "0300023", "auteur" : "fontanelle1789", "weight" : 1}},
                    
                    {"data": {"id" : "3500038", "auteur" : "habert1557", "weight" : 2}},
                
                    {"data": {"id" : "2900043", "auteur" : "martignac1697", "weight" : 1}},
                    
            ],
            "edges":
            [
                        {"data": {"id" : "0300023_3500020", "source": "3500020", "target" : "0300023", "weight" : 3, "auteur_source" : "habert1557", "auteur_target" : "fontanelle1789"}},
                    
                        {"data": {"id" : "2900043_3500038", "source": "3500038", "target" : "2900043", "weight" : 4, "auteur_source" : "habert1557", "auteur_target" : "martignac1697"}},
                    
            ]
            }};
            
                    