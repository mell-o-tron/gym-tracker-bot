#!/usr/bin/env python3
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Based on the echobot example program.
"""

import logging
import datetime

from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
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
        rf"Hi {user.mention_html()}! Use the /adb command to select an existing exercise, or the /add command to select one by hand! See /help for usage.",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "Available commands:\n\n"
        "/start - start the bot\n"
        "/help - show this help\n"
        "/add <exercise> <reps> <weight> - log an exercise entry\n"
        "/bw <weight> - save your bodyweight\n"
        "/rm - remove the last entry\n"
        "/history - show recent workout history\n"
        "/csv - download the workout CSV\n"
        "/stats - view your volume stats\n"
        "/target - view weekly target volume\n"
        "/adb - interactive exercise selector"
    )
    await update.message.reply_text(help_text)

async def add_with_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Chest", callback_data="chest"),
         InlineKeyboardButton("Biceps", callback_data="biceps")],
        [InlineKeyboardButton("Triceps", callback_data="triceps"),
         InlineKeyboardButton("Shoulders", callback_data="shoulders")],
        [InlineKeyboardButton("Back", callback_data="back"),
         InlineKeyboardButton("Legs", callback_data="legs")],
        [InlineKeyboardButton("Abs", callback_data="abs")],
    ]
    await update.message.reply_text(
        "Choose one:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO put these in a file at some point
    chest_exercises = [
        [InlineKeyboardButton("Chest Press", callback_data="chest_press")],
        [InlineKeyboardButton("Pushup", callback_data="pushup")]
    ]
    
    bicep_exercises = [
        [InlineKeyboardButton("Bicep Curl", callback_data="bicep_curl")]
    ]

    tricep_exercises = [
        [InlineKeyboardButton("Tricep Kickback", callback_data="tricep_kickback")],
        [InlineKeyboardButton("Tricep Pushdown", callback_data="tricep_pushdown")],

    ]

    shoulder_exercises = [
        [InlineKeyboardButton("Lateral Raises", callback_data="shoulder_lateral_raises")],
        [InlineKeyboardButton("Shoulder Press", callback_data="shoulder_press")]
    ]

    back_exercises = [
        [
            [InlineKeyboardButton("Pull-Ups", callback_data="lat_pull-ups")],
            [InlineKeyboardButton("Rows", callback_data="back_rows")]
        ],
    ]

    ab_exercises = [
        [InlineKeyboardButton("Ab Crunch", callback_data="ab_crunch")]
    ],

    leg_exercises = [
        [InlineKeyboardButton("Squat", callback_data="leg_squat")],
        [InlineKeyboardButton("Leg Press", callback_data="leg_press")],
        [InlineKeyboardButton("Calf Press", callback_data="leg_press_calves")]
    ]
    query = update.callback_query
    await query.answer()
    print(f"query is \"{query.data}\"")
    match query.data:
        case "chest":
            await query.edit_message_text(
                "Select chest exercise:",
                reply_markup=InlineKeyboardMarkup(chest_exercises),
            )
        case "biceps":
            await query.edit_message_text(
                "Select biceps exercise:",
                reply_markup=InlineKeyboardMarkup(bicep_exercises),
            )
        case "triceps":
            await query.edit_message_text(
                "Select triceps exercise:",
                reply_markup=InlineKeyboardMarkup(tricep_exercises),
            )
        case "shoulders":
            await query.edit_message_text(
                "Select shoulders exercise:",
                reply_markup=InlineKeyboardMarkup(shoulder_exercises),
            )
        case "back":
            await query.edit_message_text(
                "Select back exercise:",
                reply_markup=InlineKeyboardMarkup(back_exercises),
            )
        case "abs":
            await query.edit_message_text(
                "Select abs exercise:",
                reply_markup=InlineKeyboardMarkup(ab_exercises),
            )
        case "legs":
            await query.edit_message_text(
                "Select legs exercise:",
                reply_markup=InlineKeyboardMarkup(leg_exercises),
            )
        case _:
            context.user_data["awaiting_two_numbers"] = True
            context.user_data["selected_exercise"] = query.data
            await query.edit_message_text(
                f"You chose: {query.data}\nPlease send number of reps and weight, separated by a space. Use bw to indicate bodyweight."
            )


async def add_entry(update: Update, exercise_name: str, reps: str, weight: str) -> None:
    user = update.effective_user
    if user is not None and user.username == "mell_o_tron":
        if weight == "bw":
            with open('bw_mell-o-tron.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if len(rows) == 0:
                    await update.message.reply_text("No weight measurement found, using default of 65kg")
                    weight = "65"
                else:
                    weight = f"{rows[-1][0]}"

        with open('mell-o-tron.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([
                [exercise_name, reps, weight, datetime.datetime.now()]
            ])
            await update.message.reply_text("Added")
    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if(user.username == "mell_o_tron"):
        args = context.args
        # args are: exercise, reps, weight
        if len(args) == 3:
            await add_entry(update, args[0], args[1], args[2])
        else:
            await update.message.reply_text("Format is: exercise name (no spaces), reps, weight")
    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")


async def add_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if(user.username == "mell_o_tron"):
        args = context.args
        # args are: exercise, reps, weight
        if(len(args) == 1):

            with open('bw_mell-o-tron.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows([
                    [args[0], datetime.datetime.now()]
                ])
                await update.message.reply_text("Added")
        else:
            await update.message.reply_text("Format is: weight")
    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")

async def rm_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    user = update.effective_user
    if(user.username == "mell_o_tron"):
        await update.message.reply_document(
            document="./mell-o-tron.csv"
        )
    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

async def view_target(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if(user.username == "mell_o_tron"):
        args = context.args
        # args are: exercise, reps, weight
        with open('mell-o-tron.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        categories, target_values = compute_target_volume(rows)
        categories, week_values = compute_volume_per_muscle_group_week(rows)

        make_target_plot(categories, week_values, target_values)

        await update.message.reply_photo(
            photo="plot.png",
            caption=f"Here's your weekly volume stats!"
        )

    else:
        await update.message.reply_text("Sorry, this bot can currently only be used by mello :)")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Arbitrary message logic """
    if context.user_data.get("awaiting_two_numbers"):
        parts = update.message.text.strip().split()
        if len(parts) != 2:
            await update.message.reply_text(
                "Please send exactly two values separated by a space."
            )
            return

        first, second = parts
        if second.lower() != "bw":
            try:
                float(second)
            except ValueError:
                await update.message.reply_text(
                    "The second value must be a number or bw."
                )
                return

        exercise_name = context.user_data.get("selected_exercise", "unknown exercise")
        context.user_data["awaiting_two_numbers"] = False
        context.user_data["selected_exercise"] = None
        await add_entry(update, exercise_name, first, second)
        return

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
    application.add_handler(CommandHandler("bw", add_weight))
    application.add_handler(CommandHandler("target", view_target))
    application.add_handler(CommandHandler("adb", add_with_buttons))
    application.add_handler(CallbackQueryHandler(button))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
