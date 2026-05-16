#!/usr/bin/env python3
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Based on the echobot example program.
"""

import logging
import datetime

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import csv

from telegram_token import MELLO_TOKEN
from stats import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    print(user)
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help! I need somebody")

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    if(user.username == "mell_o_tron"):
        args = context.args
        # args are: exercise, reps, weight
        if(len(args) == 3):
            with open('mell-o-tron.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows([
                    [args[0], args[1], args[2], datetime.datetime.now()]
                ])
                await update.message.reply_text("Added")
        else:
            await update.message.reply_text("Format is: exercise name (no spaces), reps, weight")
    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")

async def rm_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    if(user.username == "mell_o_tron"):
        args = context.args
        # args are: exercise, reps, weight
        with open('mell-o-tron.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if len(rows) > 0:
            with open('mell-o-tron.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows[:-1])  # [:-1] excludes the last row
                await update.message.reply_text("Removed")
        else:
            await update.message.reply_text("Nothing to remove")
    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    if(user.username == "mell_o_tron"):
        res = ""
        with open('mell-o-tron.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
               res += f"• <b>{row[3]}</b>: {row[0]} - {row[1]} x {row[2]} kg\n\n"
        await update.message.reply_text(res, parse_mode="HTML")
    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")

async def csv_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    if(user.username == "mell_o_tron"):
        await update.message.reply_document(
            document="./mell-o-tron.csv"
        )
    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    if(user.username == "mell_o_tron"):
        args = context.args
        # args are: exercise, reps, weight
        with open('mell-o-tron.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        categories, values = compute_volume_per_muscle_group(rows)

        argmin = values[:-1].index(min(values[:-1]))

        if values[-1] == 0:
            make_star_plot(categories[:-1], values[:-1])
        else:
            make_star_plot(categories, values)

        await update.message.reply_photo(
            photo="plot.png",
            caption=f"Here's your volume stats! Gotta work on your {categories[argmin]} some more..."
        )

    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(MELLO_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("rm", rm_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("csv", csv_command))
    application.add_handler(CommandHandler("stats", stats_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
