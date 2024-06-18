from flask import Flask, render_template, request, jsonify, abort, send_file, redirect
import os
import random
import string

app = Flask(__name__)

DIRECTORY = "Storage"

def get_file_path_by_number(directory, prefix):
    txt_files = [file for file in os.listdir(directory) if file.endswith('.txt')]
    for filename in txt_files:
        if filename.startswith(prefix):
            return os.path.join(directory, filename)
    return None

def count_txt_files(directory):
    if not os.path.exists(directory):
        return 0, []
    txt_files = [file for file in os.listdir(directory) if file.endswith('.txt')]
    return len(txt_files), sorted(txt_files)

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/count')
def count_files():
    total_files, _ = count_txt_files(DIRECTORY)
    return f"There are {total_files} .txt files in the directory {DIRECTORY}"

def find_name(directory):
    while True:
        name = ''.join(random.choices(string.ascii_uppercase, k=random.randrange(5, 7)))
        filename_check = name + '.txt'
        if not os.path.isfile(os.path.join(directory, filename_check)):
            return name

@app.route('/Submit', methods=["POST"])
def submit():
    data = request.json  # Assuming JSON data is sent from JavaScript
    value_box = data.get('value_box')
    
    directory = DIRECTORY
    Name = find_name(directory) 
    filename = f"{Name}.txt"
    file_path = os.path.join(directory, filename)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(value_box)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"counter": Name})  # Sending JSON response

@app.route('/<string:file_prefix>')
def display_file(file_prefix):
    file_path = get_file_path_by_number(DIRECTORY, file_prefix)
    if file_path is None:
        return redirect('/')
    
    try:
        return send_file(file_path, as_attachment=False)
    except Exception as e:
        return abort(500, description=str(e))

if __name__ == '__main__':
    app.run(debug=True)
