from flask import Flask, render_template, request, jsonify, abort, send_file
import os

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('Main.html')

DIRECTORY = "\\DropCloud\\Storage"

def count_txt_files(directory):
    if not os.path.exists(directory):
        return 0, []
    txt_files = [file for file in os.listdir(directory) if file.endswith('.txt')]
    return len(txt_files), sorted(txt_files)

@app.route('/count')
def count_files():
    total_files, _ = count_txt_files(DIRECTORY)
    return f"There are {total_files} .txt files in the directory {DIRECTORY}"

@app.route('/Submit', methods=["POST"])
def submit():
    data = request.json  # Assuming JSON data is sent from JavaScript
    value_box = data.get('value_box')
    
    print("uploading")
    print(value_box)
    print("uploading")

    directory = DIRECTORY

    txt_files_count = len([file for file in os.listdir(directory) if file.endswith('.txt')])
    counter = txt_files_count + 1  # Increment counter for new file

    filename = f"Storage{counter}.txt"
    file_path = os.path.join(directory, filename)

    with open(file_path, 'w') as f:
        f.write(value_box)
    
    return jsonify({"counter": counter})  # Sending JSON response

@app.route('/<int:file_number>')
def display_file(file_number):
    total_files, txt_files = count_txt_files(DIRECTORY)
    if file_number > total_files or file_number <= 0:
        return abort(404, description="File not found")
    
    file_path = os.path.join(DIRECTORY, txt_files[file_number - 1])
    try:
        return send_file(file_path, as_attachment=False)
    except Exception as e:
        return abort(500, description=str(e))

if __name__ == '__main__':
    app.run(debug=True)
