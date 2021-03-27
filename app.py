from flask import Flask
app = Flask(__name__)

@app.route('/')
def documentation():
    documentation = f"""
    <a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a>
    Hello
    """
    return documentation



if __name__ == '__main__':
    app.run(debug=True)