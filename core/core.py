#############################################
#############################################
##
##  Import modules
##
#############################################
#############################################

from . import command
import logger_app
import threading
import os

#############################################
#############################################
##
##  Prepare logger
##
#############################################
#############################################

logger = logger_app.prepareLogger(__name__)

#############################################
#############################################
##
##  Exceptions
##
#############################################
#############################################



#############################################
#############################################
##
##  Main classes and functions
##
#############################################
#############################################

class Core:
    def __init__(self, command: command.CommandTable):
        self.commands = command
    
    def add_command(self, command: command.Command) -> None:
        try:
            self.commands.add_command(command)
        except Exception as e:
            logger.error(f"Catched exception while adding command <{command}>! {e}")
    
    def __call__(self, command: str, **kwargs) -> None:
        try:
            self.commands.get_command(command)(**kwargs)
        except Exception as e:
            logger.error(f"Catched exception while calling command <{command}> with kwargs={kwargs}! {e}")


class Console(Core):
    def __init__(self, commands: list[command.Command] = []):
        commands.extend([
            command.Command("help", "Get help menu", self._help, {}),
            command.Command("exit", "Close console", self._exit, {}),
            command.Command("test", "test args", self._test, {"r_a": str})
            #command.Command("thread", "Start a command in other thread", thread, {"command": str})
        ])
        super().__init__(command.CommandTable(commands))
        self.status = False
    
    def loop(self) -> None:
        self.status = True
        while self.status:
            try:
                command, *args = input("test > ").split()
                self.__call__(command, **self._args_to_kwargs(*args))
            except KeyboardInterrupt:
                logger.info("User close console!")
                return
            except Exception as e:
                logger.critical(f"Critical error: {e}")
    
    def _args_to_kwargs(self, *args) -> dict[str, any]:
        kwargs = {}
        for arg in args:
            arg = arg.replace(" ", "")
            key, value = arg.split("=")
            arg, _type = value.split(":")
            
            match _type:
                case "int":
                    kwargs[key] = int(arg)
                case _:
                    kwargs[key] = arg
        return kwargs
    
    def _test(self, r_a: str) -> None:
        print(f"Success: {r_a}")
    
    def _help(self) -> None:
        print("You called help menu for console.core...")
        print("If argument must be int, you would write it like: [command] [name]=[argument]:int")
        for i, command in enumerate(self.commands.commands.values()):
            print(f"{i}) {command.name}")
    
    def _exit(self) -> None:
        self.status = False