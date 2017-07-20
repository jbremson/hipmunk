Installing and running the weather chatbot.

7/19/17
Joel Bremson

To install:

pip install flask
pip install -U flask-cors

To configure:

Copy ./src/secrets.tmpl to ./src/secrets.py.
Edit ./src/secrets.py with the various key values.

To test:

python test_chatbot.py

To start webserver:

In src/:

export FLASK_APP=chatbot.py
flask run -p 9000