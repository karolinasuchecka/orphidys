
            var auteurs_graphe = 
            {
            "data": [],
            "directed": false,
            "multigraph": false,
            "elements":
                {
                    "nodes": 
                    [
                    {"data": {"id" : "cogolin1750", "weight" : 4}},
            
                    {"data": {"id" : "desfontaines1810", "weight" : 2}},
                
                    {"data": {"id" : "desportes1846_prose", "weight" : 2}},
                
               ],
               "edges":
               [
               
                       {"data": {"id" : "desfontaines1810_cogolin1750", "source": "cogolin1750", "target" : "desfontaines1810", "weight" : 2}},
                   
                       {"data": {"id" : "desportes1846_prose_cogolin1750", "source": "cogolin1750", "target" : "desportes1846_prose", "weight" : 2}},
                   
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
            
                    {"data": {"id" : "3100034", "auteur" : "cogolin1750", "weight" : 2}},
                
                    {"data": {"id" : "2100025", "auteur" : "desfontaines1810", "weight" : 1}},
                    
                    {"data": {"id" : "3100051", "auteur" : "cogolin1750", "weight" : 2}},
                
                    {"data": {"id" : "2100038", "auteur" : "desfontaines1810", "weight" : 1}},
                    
                    {"data": {"id" : "3100004", "auteur" : "cogolin1750", "weight" : 2}},
                
                    {"data": {"id" : "2500005", "auteur" : "desportes1846_prose", "weight" : 1}},
                    
                    {"data": {"id" : "3100005", "auteur" : "cogolin1750", "weight" : 2}},
                
                    {"data": {"id" : "2500006", "auteur" : "desportes1846_prose", "weight" : 1}},
                    
            ],
            "edges":
            [
                        {"data": {"id" : "2100025_3100034", "source": "3100034", "target" : "2100025", "weight" : 3, "auteur_source" : "cogolin1750", "auteur_target" : "desfontaines1810"}},
                    
                        {"data": {"id" : "2100038_3100051", "source": "3100051", "target" : "2100038", "weight" : 6, "auteur_source" : "cogolin1750", "auteur_target" : "desfontaines1810"}},
                    
                        {"data": {"id" : "2500005_3100004", "source": "3100004", "target" : "2500005", "weight" : 5, "auteur_source" : "cogolin1750", "auteur_target" : "desportes1846_prose"}},
                    
                        {"data": {"id" : "2500006_3100005", "source": "3100005", "target" : "2500006", "weight" : 2, "auteur_source" : "cogolin1750", "auteur_target" : "desportes1846_prose"}},
                    
            ]
            }};
            
                    