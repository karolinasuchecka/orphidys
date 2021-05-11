
            var auteurs_graphe = 
            {
            "data": [],
            "directed": false,
            "multigraph": false,
            "elements":
                {
                    "nodes": 
                    [
                    {"data": {"id" : "duchemin1837", "weight" : 5}},
            
                    {"data": {"id" : "rat1932", "weight" : 2}},
                
                    {"data": {"id" : "heguin1827", "weight" : 1}},
                
                    {"data": {"id" : "desportes1846_prose", "weight" : 1}},
                
                    {"data": {"id" : "nisard1868", "weight" : 1}},
                
               ],
               "edges":
               [
               
                       {"data": {"id" : "rat1932_duchemin1837", "source": "duchemin1837", "target" : "rat1932", "weight" : 2}},
                   
                       {"data": {"id" : "heguin1827_duchemin1837", "source": "duchemin1837", "target" : "heguin1827", "weight" : 1}},
                   
                       {"data": {"id" : "desportes1846_prose_duchemin1837", "source": "duchemin1837", "target" : "desportes1846_prose", "weight" : 1}},
                   
                       {"data": {"id" : "nisard1868_duchemin1837", "source": "duchemin1837", "target" : "nisard1868", "weight" : 1}},
                   
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
            
                    {"data": {"id" : "1600023", "auteur" : "duchemin1837", "weight" : 2}},
                
                    {"data": {"id" : "0200018", "auteur" : "rat1932", "weight" : 1}},
                    
                    {"data": {"id" : "0700026", "auteur" : "heguin1827", "weight" : 1}},
                    
                    {"data": {"id" : "2500027", "auteur" : "desportes1846_prose", "weight" : 1}},
                    
                    {"data": {"id" : "1600027", "auteur" : "duchemin1837", "weight" : 2}},
                
                    {"data": {"id" : "0200020", "auteur" : "rat1932", "weight" : 1}},
                    
                    {"data": {"id" : "1600005", "auteur" : "duchemin1837", "weight" : 2}},
                
                    {"data": {"id" : "2600005", "auteur" : "nisard1868", "weight" : 1}},
                    
            ],
            "edges":
            [
                        {"data": {"id" : "0200018_1600023", "source": "1600023", "target" : "0200018", "weight" : 3, "auteur_source" : "duchemin1837", "auteur_target" : "rat1932"}},
                    
                        {"data": {"id" : "0700026_1600023", "source": "1600023", "target" : "0700026", "weight" : 3, "auteur_source" : "duchemin1837", "auteur_target" : "heguin1827"}},
                    
                        {"data": {"id" : "2500027_1600023", "source": "1600023", "target" : "2500027", "weight" : 3, "auteur_source" : "duchemin1837", "auteur_target" : "desportes1846_prose"}},
                    
                        {"data": {"id" : "0200020_1600027", "source": "1600027", "target" : "0200020", "weight" : 16, "auteur_source" : "duchemin1837", "auteur_target" : "rat1932"}},
                    
                        {"data": {"id" : "2600005_1600005", "source": "1600005", "target" : "2600005", "weight" : 9, "auteur_source" : "duchemin1837", "auteur_target" : "nisard1868"}},
                    
            ]
            }};
            
                    