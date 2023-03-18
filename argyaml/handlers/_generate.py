from argyaml import BaseHandler
from yaml import safe_load
import os


class Handler(BaseHandler.meta('Default')):
    def __init__(self):
        config_path = self.args.get('config')
        if not config_path:
            config_path = 'cli-config.yaml'
        config = BaseHandler._load_config(config_path)
        rules = config.get('next', [])
        handlers_config = config.get('handlers', {})
        handlers_root = handlers_config.get('root', 'default')
        handlers_internal = handlers_config.get('internal', True)
        handler_name = self.args.get('name')
        handler_meta = f"'{handler_name}'" if handler_name else ''
        handlers_dir = self.args.get('dir') or 'handlers'
        print(f'Generating handlers into {handlers_dir}/')
        for file in self.__get_handlers('', rules):
            if not file:
                file = handlers_root
            if not handlers_internal:
                file = file[1:]
            try:
                if not os.path.exists(handlers_dir):
                    os.makedirs(handlers_dir)
                flag = 'w' if self.args.get('force', False) else 'x'
                with open(f'{handlers_dir}/{file}.py', flag,
                          encoding='UTF-8') as stream:
                    stream.writelines(
                        f"from argyaml import BaseHandler\n\n\n"
                        f"class Handler(BaseHandler.meta({handler_meta})):\n"
                        f"    def __init__(self):\n"
                        f"        pass\n")
                    print('created:', f'{file}.py')
            except FileExistsError:
                print('skipped:', f'{file}.py')

    def __get_handlers(self, base: str, rules: list):
        subcommand = False
        for rule in rules:
            if 'command' in rule:
                subcommand = True
                subrules = rule.get('next', [])
                yield from self.__get_handlers(
                    base + '_' + rule['command'], subrules)
        if not subcommand:
            yield base
