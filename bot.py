from telebot import TeleBot
import telebot

from config import DATABASE, TOKEN
from logic import TaskManager


if not TOKEN:
    raise ValueError(
        "Bitte tragen Sie den Bot-Token in der Datei config.py ein."
    )

bot = TeleBot(TOKEN)

task_manager = TaskManager(DATABASE)
task_manager.create_table()


@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Hallo! 👋\n\n"
        "Ich bin ein einfacher Task-Manager-Bot. "
        "Ich kann deine Aufgaben speichern, anzeigen und löschen.\n\n"
        "Verfügbare Befehle:\n"
        "/add_task – neue Aufgabe hinzufügen\n"
        "/delete_task – Aufgabe löschen\n"
        "/show – alle Aufgaben anzeigen\n"
        "/show <Anzahl> – eine bestimmte Anzahl von Aufgaben anzeigen"
    )


@bot.message_handler(commands=["add_task"])
def add_task_command(message):
    bot.send_message(message.chat.id, "Bitte gib den Namen der Aufgabe ein:")
    bot.register_next_step_handler(message, save_task)


def save_task(message):
    name = (message.text or "").strip()

    if not name:
        bot.send_message(message.chat.id, "Der Aufgabenname darf nicht leer sein.")
        bot.register_next_step_handler(message, save_task)
        return

    task_manager.add_task(message.from_user.id, name, "")
    bot.send_message(message.chat.id, f"✅ Aufgabe „{name}“ wurde hinzugefügt.")


@bot.message_handler(commands=["delete_task"])
def delete_task_command(message):
    bot.send_message(
        message.chat.id,
        "Bitte gib den Namen der Aufgabe ein, die du löschen möchtest:"
    )
    bot.register_next_step_handler(message, delete_task_by_name)


def delete_task_by_name(message):
    task_name = (message.text or "").strip()

    if not task_name:
        bot.send_message(message.chat.id, "Der Aufgabenname darf nicht leer sein.")
        bot.register_next_step_handler(message, delete_task_by_name)
        return

    deleted = task_manager.delete_task(task_name, message.from_user.id)

    if deleted:
        bot.send_message(message.chat.id, f"🗑 Aufgabe „{task_name}“ wurde gelöscht.")
    else:
        bot.send_message(message.chat.id, "Diese Aufgabe wurde nicht gefunden.")


@bot.message_handler(commands=["show"])
def show_tasks(message):
    user_id = message.from_user.id
    argument = telebot.util.extract_arguments(message.text).strip()

    if argument:
        try:
            amount = int(argument)
            if amount <= 0:
                raise ValueError
            tasks = task_manager.show_task_many(user_id, amount)
        except ValueError:
            bot.send_message(
                message.chat.id,
                "Bitte verwende zum Beispiel: /show 5"
            )
            return
    else:
        tasks = task_manager.show_task_all(user_id)

    if not tasks:
        bot.send_message(message.chat.id, "Du hast noch keine Aufgaben.")
        return

    text = "\n".join(
        f"{index}. {task[0]}"
        for index, task in enumerate(tasks, start=1)
    )

    bot.send_message(
        message.chat.id,
        f"📋 Deine Aufgaben:\n\n{text}"
    )


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
