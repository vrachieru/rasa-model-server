from flask import Flask, render_template, send_from_directory
from os import sep
from os.path import isdir, dirname, basename, relpath, join, exists

from config import models_dir, server_port
from filesystem import Scaner


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return list_dir(models_dir)
 
@app.route('/<path:path>', methods=['GET'])
def serve(path):
    fetch_latest = '@latest' in path
    real_path = join(models_dir, path.replace('@latest', ''))
    
    if not exists(real_path):
        return 'Not Found', 404

    if isdir(real_path):
        if fetch_latest:
            latest_entry = Scaner(real_path).latest_entry
            if not latest_entry:
                return 'No Models Found', 404
            return download_file(latest_entry.path)
        else:
            return list_dir(real_path)
    else:
        return download_file(real_path)


def list_dir(path):
    rel_path = relpath(path, models_dir)
    parent_path = dirname(rel_path)
    return render_template('index.html', sep=sep, parent_path=parent_path, path=rel_path, entries=Scaner(path).entries)

def download_file(path):
    return send_from_directory(dirname(path), basename(path), as_attachment=True, attachment_filename=basename(path))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)