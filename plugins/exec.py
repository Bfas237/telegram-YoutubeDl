from pyrogram import Filters
import config
import os

app = config.app
user_id = config.user_id


if config.language == "english":
    from languages.english import eval_running_text, eval_error_text, eval_success_text, eval_result_text

RUNNING = "**Exec Code:**\n```{}```\n**Running...**"
ERROR = "**Exec Code:**\n```{}```\n**Error:**\n```{}```"
SUCCESS = "**Exec Code:**\n```{}```\n**Success**"
RESULT = "**Exec Code:**\n```{}```\n**Result:**\n```{}```"


@app.on_message(Filters.user("197005208") & Filters.command("exec", prefix="-"))
def exec_expression(c, m):
    execution = " ".join(m.command[1:])

    if execution:
        m = m.reply(RUNNING.format(execution))

        try:
            exec('def __ex(c, m): ' + ''.join('\n ' + l for l in execution.split('\n')))
            result = locals()['__ex'](c, m)
        except Exception as error:
            c.edit_message_text(
                m.chat.id,
                m.message_id,
                ERROR.format(execution, error)
            )
        else:
            if result is None:
                c.edit_message_text(
                    m.chat.id,
                    m.message_id,
                    SUCCESS.format(execution)
                )
            else:
                client.edit_message_text(
                    m.chat.id,
                    m.message_id,
                    RESULT.format(execution, result)
                )
