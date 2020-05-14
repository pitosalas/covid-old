echo "[Running covid reports]"
python3 covid.py graph1 --states "USA"  "New York" "Massachusetts" --vars "casesr"  "deathsr"
python3 covid.py graph2 --states "Florida" "California"  "District of Columbia" "USA"  "New York" "Massachusetts" "South Carolina" "New Hampshire"  "Washington" --vars "casesr"  "deathsr"
python3 covid.py graph3 --states "Massachusetts" "Florida" "California"  "District of Columbia" --vars "casesr"  "deathsr"
python3 covid.py graph4 --states "South Carolina" "New Hampshire"  "Washington" --vars "casesr"  "deathsr"

