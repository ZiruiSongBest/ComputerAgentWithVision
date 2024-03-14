from __future__ import annotations
import sys
sys.dont_write_bytecode = True
from typing import Union, Optional
from subprocess import run, PIPE
import get_os_version

class Output:
    def __init__(self, stdout: str, stderr: str):
        self.stdout = stdout
        self.stderr = stderr

    def observe(self):
        if self.stdout == "" and self.stderr != "":
            raise RuntimeError(self.stderr)
        else:
            return self.stdout

    def __str__(self):
        print([self.stdout, self.stderr])
        return self.stdout + self.stderr

class Command:
    def __init__(self, cmd: str, stdin: Optional[str]=None):
        self.cmd = cmd
        self.stdin = stdin

    def __call__(self, *arg) -> str:
        if get_os_version.get_os_name() == "windows":
            result = run(
                [self.cmd, *arg],
                input=self.stdin,
                capture_output=True,
                text=True,
                shell=True
            )
        else:
            result = run(
                [self.cmd, *arg],
                input=self.stdin,
                capture_output=True,
                text=True
            )
        return Output(result.stdout, result.stderr)

class Promise():
    def __init__(self, stdin: Optional[str]=None):
        self.stdin = stdin
        self.stash = None
        self.stdout = None

    def then(self, cmd: Union[str, Command], *arg) -> Promise:
        if type(cmd) == str:
            cmd = Command(cmd)
        self.stash = cmd
        self.stash.stdin = self.stdout if self.stdout != None else self.stdin
        return self.__call__(*arg) if len(arg) > 0 else self

    def observe(self) -> str:
        return self.stdout.strip("\n")

    def __call__(self, *arg) -> Promise:
        if self.stash != None:
            self.stdout = self.stash(*arg).observe()
            self.stash = None
            return self
        else:
            return self.observe()

if get_os_version.get_os_name() in ["macos", "linux"]:
    Pkexec = \
        lambda cmd: \
        lambda *arg: \
            Command("pkexec")(cmd, *arg)

    Pkexec_GUI = \
        lambda cmd: \
        lambda *arg: \
            Command("pkexec")(
                "env",
                "DISPLAY=$DISPLAY",
                "XAUTHORITY=$XAUTHORITY",
                cmd,
                *arg
            )