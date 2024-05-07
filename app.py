from flask import Flask, render_template, request, jsonify
from game import get_stuff

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stuff = get_stuff()
    labels = stuff[1][:4] + [stuff[0]] + stuff[1][4:]
    labels = [i.capitalize() for i in labels]
    assert(len(labels) == 9)
    
    if request.method == 'POST':
        data = request.get_json()
        textbox_id = list(data.keys())[0]  # Assuming only one textbox's data is sent at a time
        textbox_data = data[textbox_id]
        textbox_name = data['textBoxID']
        print(f"Textbox '{textbox_name}' data:", textbox_data)
        # You can process the data further here
        # For example, you can store it in a database or perform any other operation

        return jsonify({"message": "Data received successfully"})

    return render_template('index.html', labels=labels)

if __name__ == '__main__':
    app.run(debug=True)    

if __name__ == '__main__':
    app.run(debug=True)