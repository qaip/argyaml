# Argyaml
Argyaml is a small module for creating _powerful_ and _scalable_ __CLI applications__ based on a _simple_ and _user-friendly_ yaml __configuration file__.

### Motivation
Argyaml is built over the [argparse](https://docs.python.org/3/library/argparse.html) module, which is a part of python standard library starting python 3.2. While it works well for tiny projects that need to quickly access a few arguments and provide automatically generated help and usage messages for user, it gets very complicated and painful when it comes to large projects or your application grows in complexity.

### Features
- Independent specification of CLI commands and arguments.
- No boilerplate code.
- Ability to set default options for commands, groups, and arguments.
- Automatic and optimized invocation of command handlers.
- Handler template files generator.

## Install

```bash
# pip
pip install argyaml

# poetry
poetry add argyaml
```

## Getting started
```yaml
# cli-config.yaml
prog: todo
description: My beautiful todo app
next:
  - command: new
    next:
      - command: task
        description: Create a new task
        next:
          - argument: [name]
            help: the name of task
  - command: list
    next:
      - argument: [-t, --task]
        help: display tasks only
        action: 'store_true'
```

```python
from argyaml import BaseHandler

base = BaseHandler()
base.args # <-- parsed and ready-to-use arguments
```

__Learn more about [config file](./wiki#Config).__


### Using Handlers
Generate template files using `argyaml generate`:
```bash
# pip
argyaml generate

# poetry
poetry run argyaml generate
```
This will generate the following files:
```new
handlers/
  _new_task.py
  _list.py
```
Now, whenever `new task` command is called, the corresponding handler init function will be invoked with all additional aruments stored in the `self.args` object.

```python
# _new_task.py
from argyaml import BaseHandler

class Handler(BaseHandler.meta()):
    def __init__(self):
        print(f"Successfully created task '{self.args['name']}'!")
```
Modify the main file to run the base handler:
```python
from argyaml import BaseHandler

base = BaseHandler()
base.run()
```

__Learn more about [BaseHandler](./wiki#BaseHandler) and [argyaml generator](./wiki#Generator).__

## Contributing
Feel free to open issues. Pull requests are welcome.

## License
This project is licensed under the [MIT License](./LICENSE).
