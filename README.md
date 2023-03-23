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

__Learn more about [config file](#configuration-file).__


### Using Handlers
Generate template files using `argyaml generate`:
```bash
# pip
argyaml generate

# poetry
poetry run argyaml generate
```
This will generate the following files:
```
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

__Learn more about [BaseHandler](#base-handler) and [argyaml generator](#generator).__



## Basic concepts

Imagine that you have several commands, each containing its own sub-commands that have their own set of arguments:
```
add city <name>
add building --city CITY_NAME

remove city <name> [--force]
remove building --id ID

list cities
list buildings --city CITY_NAME
```

A minimal implementation using __argparser__ would be the following:
```python
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_add = subparsers.add_parser('add')
parser_remove = subparsers.add_parser('remove')
parser_list = subparsers.add_parser('list')

subparsers_add = parser_add.add_subparsers()
subparsers_remove = parser_remove.add_subparsers()
subparsers_list = parser_list.add_subparsers()

# 'add' sub-commands
parser_add_city = subparsers_add.add_parser('city')
parser_add_city.add_argument('name', type=str)

parser_add_building = subparsers_add.add_parser('building')
parser_add_building.add_argument('--city', dest='city_name',
                                 required=True, type=str)

# 'remove' sub-commands
parser_remove_city = subparsers_remove.add_parser('city')
parser_remove_city.add_argument('name', type=str)
parser_remove_city.add_argument('--force', action='store_true')

parser_remove_building = subparsers_remove.add_parser('building')
parser_remove_building.add_argument('--id', required=True, type=int)

# 'list' sub-commands
parser_list_cities = subparsers_list.add_parser('cities')

parser_list_buildings = subparsers_list.add_parser('buildings')
parser_list_buildings.add_argument('--city', dest='city_name', 
                                   required=True, type=str)

# parse the arguments and transform to dict
parser.parse_args()
vars(parser.parse_args())
```

Lots of boilerplate code that is not easy to read.  Here is an equivanet using __argyaml__:

```yaml
# cli-config.yaml
next:
  - command: add
    next:
      - command: city
        next:
          - argument: ['name']
            type: str
      - command: building
        next:
          - argument: ['--city']
            dest: 'city_name'
            required: true
            type: str

  - command: remove
    next:
      - command: city
        next:
          - argument: ['name']
            type: str
          - argument: ['--force']
            action: store_true
      - command: building
        next:
          - argument: ['--id']
            required: true
            type: int

  - command: list
    next:
      - command: cities
      - command: buildings
        next:
          - argument: ['--city']
            dest: 'city_name'
            required: true
            type: str
```
```python
from argyaml import BaseHandler

base = BaseHandler()
base.args
```

### Configuration file
The structure of yaml configuration file is defined as follows:
```yaml
<parser-options>
group:
  <subcommands-options>
next:
  - command: name
    <parser-options>
    group: ...
    next: ...
  - argument: [positional]
    <argument-options>
  - argument: [short-flag, long-flag, ...]
    <argument-options>

default: 
  group:
    <subcommands-options>
  command:
    <parser-options>
  argument:
    <argument-options>

handlers:

```

#### Next keyword
The `next` field is used to define a hierarchy of commands. It's a list of objects, where each object can start with either a `command` key, which defines a command (subcommand), or an `argument` key, which defines an argument (a positional argument or an option, flag) of the command. The `next` field can be used recursively to define subcommands and arguments within commands (subcommands).

#### Parser options
In the context of the above configuration file structure, `<parser-options>` represent the options that are specified for the top-level [ArgumentParser](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser) class:
- `prog` — The name of the program or a subcommand (default for program: `os.path.basename(sys.argv[0])`; default for subcommand: name of parent command).
- `usage` — The string describing the program or a subcommand usage (by default: generated from arguments added to parser).
- `description` — Text to display before the argument help (by default, no text).
- `epilog` — Text to display after the argument help (by default, no text)
- `prefix_chars` — The set of characters that prefix optional arguments (default: ‘-‘).
- `fromfile_prefix_chars` — The set of characters that prefix files from which additional arguments should be read (default: None).
- `argument_default` — The global default value for arguments (default: None).
- `add_help` — Determines whether or not to add -h/--help option (default: True).
- `allow_abbrev` — Allows long options to be abbreviated if the abbreviation is unambiguous (default: True).
- `exit_on_error` — Determines whether or not ArgumentParser exits with error info when an error occurs (default: True).


#### Subcommands options
The `<subcommands-options>` are the same options for the [add_subparsers](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers) method:
- `title` — Title for the sub-parser group in help output; by default “subcommands” if description is provided, otherwise uses title for positional arguments.
- `description` — Description for the sub-parser group in help output, by default None.
- `prog` — Usage information that will be displayed with sub-command help, by default the name of the program and any positional arguments before the subparser argument.
- `action` — The basic type of action to be taken when this argument is encountered at the command line.
- `dest` — Name of the attribute under which sub-command name will be stored; by default is parent command.
- `required` — Whether or not a subcommand must be provided, by default False (added in 3.7).
- `help` — Help for sub-parser group in help output, by default None.
- `metavar` — String presenting available sub-commands in help; by default it is None and presents sub-commands in form {cmd1, cmd2, ..}.

#### Argument options
`argument-options` are the same options for the [add_argument](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument) method, except for `name or flags` being specified under the `argument` field:
- `action` — The basic type of action to be taken when this argument is encountered at the command line.
- `nargs` — The number of command-line arguments that should be consumed.
- `const` — A constant value required by some action and nargs selections.
- `default` — The value produced if the argument is absent from the command line and if it is absent from the namespace object.
- `type` — The type to which the command-line argument should be converted.
- `choices` — A sequence of the allowable values for the argument.
- `required` — Whether or not the command-line option may be omitted (optionals only).
- `help` — A brief description of what the argument does.
- `metavar` — A name for the argument in usage messages.
- `dest` — The name of the attribute to be added to the object returned by parse_args().

#### Custom defaults
The `default` section of the configuration file allows you to define default values for each type of option. Note that these defaults can be overridden by values inside specific commands, groups, or arguments.


### Base Handler
The base handler should not necessarily be used once and only once. You can instantiate as many base handlers as you need. To create multiple base handlers, you must specify custom names that will used in further handler registration and access.

You may also want to use a different configuration file and argument list.

The `BaseHandler` class accepts the following options:
- `name` — the custom name of base handler.
- `args` — the list of arguments (by default, `sys.argv[1:]` is used).
- `config_path` — path to configuration file.
- `handlers_dir` — path to handlers directory.

#### Example
```python
BaseHandler(name='Sea', handlers_dir='sea-handlers').run()
BaseHandler(name='Land', handlers_dir='land-handlers').run()
```
```python
# sea-handlers/_default.py
class Handler(BaseHandler.meta('Sea')):
  print('This handler is invoked by Sea')
```
```python
# land-handlers/_default.py
class Handler(BaseHandler.meta('Land')):
  print('This handler is invoked by Land')
```

### Generator
Handler template files generator can be called with the following arguments:
- `--name NAME` — the custom name of base handler.
- `--config CONFIG` — path to configuration file.
- `--handlers_dir DIR` — path to handlers directory.
- `--force` — overwrite existing files.

#### Example
``` yaml
# sea-cli.yaml
next:
  - command: swim
```
```bash
# pip
argyaml generate --name Sea --dir sea-handlers --config sea-cli.yaml

# poetry
poetry run argyaml generate --name Sea --dir sea-handlers --config sea-cli.yaml
```
The command above will generate the following file:
```python
from argyaml import BaseHandler

class Handler(BaseHandler.meta('Sea')):
  pass
```
```
sea-handlers/
  _swim.py
```

### Advanced configuration
Argyaml configuration file may include an additional field `handlers`:
- `root` — the name of handler file to be invoked if no commands specified (default: "default")
- `internal` — whether to mark files as internal by adding an underscore before the name (default: true)
```yaml
handlers
  root: init
  internal: false
```


## Contributing
Feel free to open issues. Pull requests are welcome!

## License
This project is licensed under the [MIT License](./LICENSE).
