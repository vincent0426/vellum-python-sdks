"""
    Extension for the python ``click`` module
    to provide a group or command with aliases.
    From https://github.com/click-contrib/click-aliases
"""

import typing as t

import click

_click7 = click.__version__[0] >= "7"


class ClickAliasedGroup(click.Group):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self._commands: t.Dict[str, list[str]] = {}
        self._aliases: t.Dict[str, str] = {}

    def add_command(self, *args: t.Any, **kwargs: t.Any) -> None:
        aliases = kwargs.pop("aliases", [])
        super().add_command(*args, **kwargs)
        if aliases:
            cmd = args[0]
            name = args[1] if len(args) > 1 else None
            name = name or cmd.name
            if name is None:
                raise TypeError("Command has no name.")

            self._commands[name] = aliases
            for alias in aliases:
                self._aliases[alias] = name

    def command(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        aliases = kwargs.pop("aliases", [])
        decorator = super().command(*args, **kwargs)
        if not aliases:
            return decorator

        def _decorator(f: t.Any) -> t.Any:
            cmd = decorator(f)
            if aliases:
                self._commands[cmd.name] = aliases
                for alias in aliases:
                    self._aliases[alias] = cmd.name
            return cmd

        return _decorator

    def group(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        aliases = kwargs.pop("aliases", [])
        decorator = super().group(*args, **kwargs)
        if not aliases:
            return decorator

        def _decorator(f: t.Any) -> t.Any:
            cmd = decorator(f)
            if aliases:
                self._commands[cmd.name] = aliases
                for alias in aliases:
                    self._aliases[alias] = cmd.name
            return cmd

        return _decorator

    def resolve_alias(self, cmd_name: str) -> str:
        if cmd_name in self._aliases:
            return self._aliases[cmd_name]
        return cmd_name

    def get_command(self, ctx: click.Context, cmd_name: str) -> t.Optional[click.Command]:
        cmd_name = self.resolve_alias(cmd_name)
        command = super().get_command(ctx, cmd_name)
        if command:
            return command
        return None

    def format_commands(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        rows = []

        sub_commands = self.list_commands(ctx)

        max_len = 0
        if len(sub_commands) > 0:
            max_len = max(len(cmd) for cmd in sub_commands)

        limit = formatter.width - 6 - max_len

        for sub_command in sub_commands:
            cmd = self.get_command(ctx, sub_command)
            if cmd is None:
                continue
            if hasattr(cmd, "hidden") and cmd.hidden:
                continue
            if sub_command in self._commands:
                aliases = ",".join(sorted(self._commands[sub_command]))
                sub_command = f"{sub_command} ({aliases})"
            cmd_help = cmd.get_short_help_str(limit) if _click7 else cmd.short_help or ""
            rows.append((sub_command, cmd_help))

        if rows:
            with formatter.section("Commands"):
                formatter.write_dl(rows)
