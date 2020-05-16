echo "[Running covid reports]"

python3 covid.py graph1 --states USA  "New York"  --vars casesr  deathsr
python3 covid.py graph2 --states Massachusetts "New Jersey" "New York" --vars casesr  deathsr
python3 covid.py graph3 --states  "District of Columbia" Florida --vars casesr  deathsr
python3 covid.py graph4 --states "South Carolina" "West Virginia" Texas --vars casesr  deathsr
python3 covid.py graph5 --states California Washington --vars casesr  deathsr
