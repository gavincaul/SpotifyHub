from CLIController import CLIController
import readline
import inspect


def get_command_docs(controller):
    """Returns a dict mapping command names to docstrings."""
    return {
        name[4:]: (method.__doc__ or "").strip()
        for name, method in inspect.getmembers(controller, predicate=callable)
        if name.startswith("cmd_")
    }

def main():
    controller = CLIController()
    command_docs = get_command_docs(controller)
    COMMANDS = list(command_docs.keys())

    def completer(text, state):
        matches = [cmd for cmd in COMMANDS if cmd.startswith(text)]
        return matches[state] if state < len(matches) else None

    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    print("SpotifyHub CLI (type 'help' or 'exit')")
    while True:
        try:
            line = input(">> ").strip()
            if not line:
                continue
            if line in ("exit", "quit", "q"):
                print("Exiting SpotifyHub CLI.")
                break

            parts = line.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd == "help":
                print("Hit Tab to see all available commands")
                continue

            method_name = f"cmd_{cmd}"
            if hasattr(controller, method_name):
                method = getattr(controller, method_name)
                method(*args)
            else:
                print(f"Unknown command: {cmd}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
