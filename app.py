from os import scandir, listdir, environ
from os.path import isfile, isdir, dirname, basename, relpath, join, exists, getsize
from datetime import datetime
from flask import Flask, render_template, send_from_directory


class Scaner:
    def __init__(self, path):
        self.entries = [Entry(entry) for entry in scandir(path.encode())]

class Entry:
    def __init__(self, entry):
        self.name = entry.name.decode()
        self.path = entry.path.decode()
        self.rel_path = relpath(self.path, models_dir)
        self.is_dir = entry.is_dir()
        self.created_time = datetime.fromtimestamp(entry.stat().st_ctime).ctime()
        self.modified_time = datetime.fromtimestamp(entry.stat().st_mtime).ctime()
        self.size = self._human_readable_size(self._get_size(entry.path))

    def _get_size(self, path):
        total_size = getsize(path)
        if isdir(path):
            for item in listdir(path):
                item_path = join(path, item)
                if isfile(item_path):
                    total_size += getsize(item_path)
                elif isdir(item_path):
                    total_size += self._get_size(item_path)
        return total_size

    def _human_readable_size(self, size):
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        human_fmt = '{0:.2f} {1}'
        human_radix = 1024.

        for unit in units[:-1]:
            if size < human_radix: 
                return human_fmt.format(size, unit)
            size /= humanradix

        return human_fmt.format(size, units[-1])


models_dir = environ.get('MODELS_DIR', 'models')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', path='/', entries=Scaner(models_dir).entries)
 
@app.route('/<path:path>', methods=['GET'])
def serve(path):
    real_path = join(models_dir, path)
    parent_path = relpath(dirname(real_path), models_dir)

    if not exists(real_path):
        return 'Not Found', 404

    if isdir(real_path):
        return render_template('index.html', parent_path=parent_path, path=path, entries=Scaner(real_path).entries)
    else:
        return send_from_directory(dirname(real_path), basename(real_path), as_attachment=True, attachment_filename=basename(real_path))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=environ.get('PORT', 8080))