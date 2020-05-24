echo "[Running covid reports]"

python3 covid.py graph1 --states usa ny --vars casesr  deathsr 
python3 covid.py  graph2 --states ma nj ny --vars casesr  deathsr 
python3 covid.py  graph3 --states tx fl --vars casesr  deathsr 
python3 covid.py  graph4 --states dc sc wv tx --vars casesr  deathsr 
python3 covid.py graph5 --states ca wa --vars casesr  deaths
python3 covid.py xx --states ca nh --vars deaths deathsr