python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
find . -type d -name '__pycache__' -not -path './venv/*' -exec rm -r {} +
