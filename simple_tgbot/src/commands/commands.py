from simple_tgbot.src.commands.ban import ban_command
from simple_tgbot.src.commands.ban_add import ban_add_command
from simple_tgbot.src.commands.help import help_command

bot_commands = {
    "ban": ban_command,
    "ban_add": ban_add_command,
    tuple(["help", "info"]): help_command,
}
