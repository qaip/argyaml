from argyaml import BaseHandler


def run(command: str | None = None) -> None:
    """
    Run argyaml cli tool
    """
    import os
    from sys import argv
    BaseHandler(
        args=[command] + argv[1:] if command else None,
        config_path=os.path.join(os.path.dirname(__file__), 'cli-config.yaml'),
        handlers_dir='argyaml.handlers').run()


if __name__ == '__main__':
    run()
