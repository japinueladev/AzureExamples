from flask import Flask 

app = Flask(__name__)

@app.route('/')
def index():
    return "Hola, mundo"

@app.route('/profile/')
def profile(): 
    return {"name": "Juan A Piñuela", "profile_photo_url": "https://picsum.photos/200"} 

if __name__ == '__main__': 
    app.run(host="0.0.0.0", port=8080, debug=True)