import os
import json
import platform

from sublime import status_message, load_settings
from sublime_plugin import TextCommand


class EnvirunCommand(TextCommand):

    def run(self, edit, open_file='$file'):
        current_file = self.view.file_name()
        if not current_file:
            return

        current_path = os.path.dirname(current_file)

        root = self.get_project_root(current_path)
        if not root:
            status_message('Current file is not in opened projects')
            return

        filename = self.get_config_filename()
        config_file = self.find_config_file(root, current_path, filename)
        if not config_file:
            status_message('Config file not found')
            return

        project = os.path.dirname(config_file)

        try:
            with open(config_file) as file:
                config = json.load(file)
        except Exception as e:
            status_message('Failed to parse config file')
            return

        if 'env' not in config or not isinstance(config['env'], str):
            status_message('Failed to parse env name')
            return

        environ = os.path.join(project, config['env'])
        if not os.path.isdir(environ):
            status_message('Environment "{}" not found'.format(config['env']))
            return

        interpreter = self.get_platform_interpreter(project, config['env'])
        if not os.path.isfile(interpreter):
            status_message('Python not found in "{}"'.format(config['env']))
            return

        commands = [interpreter, '-u']

        run = config.get('run', None)
        if not run or not isinstance(run, list):
            status_message('Failed to parse run list, use current file')
            commands.append(open_file)
        else:
            commands.extend(config['run'])

        self.repl_open(commands, project)

    def get_config_filename(self):
        settings = load_settings('Envirun.sublime-settings')
        return settings.get('file', '.envirun')

    def get_platform_interpreter(self, path, env):
        system = platform.system()
        if system == 'Windows':
            return os.path.join(path, env, 'Scripts', 'python.exe')
        else:
            return os.path.join(path, env, 'bin', 'python')

    def get_project_root(self, current_path):
        project_root = str()

        for folder in self.view.window().project_data()['folders']:
            current_root = folder['path']

            if not current_path.startswith(current_root):
                continue

            if current_root > project_root:
                project_root = current_root

        return project_root or None

    def find_config_file(self, root, current_path, filename):
        if current_path < root:
            return None

        fullpath = os.path.join(current_path, filename)
        if os.path.isfile(fullpath):
            return fullpath

        parent = os.path.abspath(os.path.join(current_path, os.pardir))
        return self.find_config_file(root, parent, filename)

    def repl_open(self, commands, cwd):
        params = {
            'encoding': 'utf8',
            'type': 'subprocess',
            'cmd': commands,
            'cwd': cwd or '$file_path'
        }
        self.view.window().run_command('repl_open', params)
