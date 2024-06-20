from flask import Flask, render_template, request, abort, send_file, jsonify, redirect, url_for
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

def find_password(id_to_find):
    file_path = 'passwords.txt'  # Assuming the file is named passwords.txt and located in the same directory as the script
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('-')
                if len(parts) == 2:
                    id_in_file, password = parts
                    if id_in_file == id_to_find:
                        return password
            return None  # If ID is not found
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def count_txt_files(directory):
    if not os.path.exists(directory):
        return 0, []
    txt_files = [file for file in os.listdir(directory) if file.endswith('.txt')]
    return len(txt_files), sorted(txt_files)

def find_name(directory):
    while True:
        name = ''.join(random.choices(string.ascii_uppercase, k=random.randrange(5, 7)))
        name_with_n = name + 'n'
        filename_check = name_with_n + '.txt'
        if not os.path.isfile(os.path.join(directory, filename_check)):
            return name_with_n

def find_name_password(directory):
    while True:
        name = ''.join(random.choices(string.ascii_uppercase, k=random.randrange(5, 7)))
        name_with_n = name + 'p'
        filename_check = name_with_n + '.txt'
        if not os.path.isfile(os.path.join(directory, filename_check)):
            return name_with_n

def write_to_empty_line(filename, variable):
    with open(filename, 'r+') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line.strip() == '':
                lines[i] = str(variable) + '\n'
                break
        else:
            lines.append(str(variable) + '\n')
        
        file.seek(0)
        file.writelines(lines)

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/count')
def count_files():
    total_files, _ = count_txt_files(DIRECTORY)
    return f"There are {total_files} .txt files in the directory {DIRECTORY}"

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

@app.route('/SubmitP', methods=["POST"])
def submit_password():
    data = request.json  # Assuming JSON data is sent from JavaScript
    value_box = data.get('value_box')
    password = data.get('password')
    
    directory = DIRECTORY
    Name = find_name_password(directory) 
    filename = f"{Name}.txt"
    file_path = os.path.join(directory, filename)
    password_join = Name + "-" + password

    write_to_empty_line("passwords.txt", password_join)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(value_box)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"counter": Name})  # Sending JSON response

@app.route('/<string:file_prefix>')
def display_file(file_prefix):
    file_path = get_file_path_by_number(DIRECTORY, file_prefix)
    if file_path is None or not os.path.exists(file_path):
        abort(404)  # File not found

    if file_prefix.endswith("n"):
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
            return render_template('file_display.html', file_content=file_content, id=file_prefix)
        except Exception as e:
            return abort(500, description=str(e))
    else:
        try:
            password = find_password(file_prefix)
            with open(file_path, 'r') as file:
                file_content = file.read()
            return render_template('file_display.html', file_content=file_content, id=file_prefix, password=password)
        except Exception as e:
            return abort(500, description=str(e))

@app.route('/<string:file_prefix>/raw')
def display_file_raw(file_prefix):
    file_path = get_file_path_by_number(DIRECTORY, file_prefix)
    if file_path is None or not os.path.exists(file_path):
        abort(404)  # File not found

    if file_prefix.endswith('p'):  # Check if file_prefix ends with 'p'
        # Example function to find password based on file_prefix
        password = find_password(file_prefix)
        if password is None:
            abort(403)  # File is password protected but no password found
        password_from_url = request.args.get('password')  # Extract password from query parameter
        if password_from_url == password:  # Replace with your actual password validation logic
            try:
                return send_file(file_path, as_attachment=False)
            except Exception as e:
                return abort(500, description=str(e))
        else:
            return redirect(url_for('main'))
    else:
        try:
            return send_file(file_path, as_attachment=False)
        except Exception as e:
            return redirect(url_for('main'))
                

if __name__ == '__main__':
    app.run(debug=True)
