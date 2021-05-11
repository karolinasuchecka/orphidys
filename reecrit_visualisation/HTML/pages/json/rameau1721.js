
            var auteurs_graphe = 
            {
            "data": [],
            "directed": false,
            "multigraph": false,
            "elements":
                {
                    "nodes": 
                    [
                    {"data": {"id" : "rameau1721", "weight" : 2}},
            
                    {"data": {"id" : "nisard1869", "weight" : 1}},
                
                    {"data": {"id" : "chapoton1648", "weight" : 1}},
                
               ],
               "edges":
               [
               
                       {"data": {"id" : "nisard1869_rameau1721", "source": "rameau1721", "target" : "nisard1869", "weight" : 1}},
                   
                       {"data": {"id" : "chapoton1648_rameau1721", "source": "rameau1721", "target" : "chapoton1648", "weight" : 1}},
                   
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
            
                    {"data": {"id" : "3100027", "auteur" : "rameau1721", "weight" : 2}},
                
                    {"data": {"id" : "2000035", "auteur" : "nisard1869", "weight" : 1}},
                    
                    {"data": {"id" : "3100011", "auteur" : "rameau1721", "weight" : 2}},
                
                    {"data": {"id" : "3300542", "auteur" : "chapoton1648", "weight" : 1}},
                    
            ],
            "edges":
            [
                        {"data": {"id" : "2000035_3100027", "source": "3100027", "target" : "2000035", "weight" : 5, "auteur_source" : "rameau1721", "auteur_target" : "nisard1869"}},
                    
                        {"data": {"id" : "3300542_3100011", "source": "3100011", "target" : "3300542", "weight" : 3, "auteur_source" : "rameau1721", "auteur_target" : "chapoton1648"}},
                    
            ]
            }};
            
                    