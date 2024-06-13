from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN: Final = '7231994891:AAH9pciH-qGymwo0WL5eBT0fzdm-OSl1CRI'
BOT_USERNAME: Final = '@pewpalsbot'

tier1 = [
    'How long have you been attending our church?',
    'What do you enjoy most about the sermons here?',
    "Have you been involved in any church activities recently?",
    "Which talk in the sermon series has been your favourite so far and why?",
    "How has your week been going?",
    "How did you become a Christian?", 
    "What have you been learning from God's Word?",
    'What have you been finding especially encouraging?',
    'How can I pray for you?'
]

tier2 = [
    'How is your Christian life going at the moment?',
    "What's a spiritual struggle you've been wrestling with lately?",
    "Have you been able to find ways to apply what you learn in church to your daily life?",
    "Are there any specific areas of your life where you're seeking God's guidance right now?",
    "What have you been finding especially discouraging?",
    "Which aspect of God is most dear to you?",
    "What aspect of God is hardest for you to grapple with?",
    "How has following Jesus been challenging for you?",
    "What's something you've been praying / thinking about from sermons / Bible studies / devotions?",
    "Who has been a role model / an influential person for you in your Christian faith and why?",
    "What is one thing do you think we can be doing better as church?"
]

tier3 = [
    "Can you tell me about a significant moment of spiritual growth or transformation in your life?",
    "How do you prioritize your spiritual life amidst your other responsibilities?",
    "Are there any aspects of your faith that you're currently questioning or exploring?",
    "Can you share a time when you experienced doubt or went through a crisis of faith?",
    "What role does prayer play in your life, and how do you maintain a consistent prayer life?",
    "What has been something you've been struggling to give up for the sake of the gospel?"
]


# Commmands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I provide questions to Choose a question tier')

async def tier1_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(tier1))

async def tier2_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(tier2))

async def tier3_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(tier3))


# Responses
def handle_response(text: str):
    processed: str = text.lower();

    if 'tier 1' in processed:
        return 'Hey there!'
    
    if 'tier 2' in processed:
        return 'Hey there!'
    
    if 'tier 3' in processed:
        return 'Hey there!'
    
    return 'I do not understand what you wrote'


async def handle_message(update: Update, context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('tier 1', tier1_command))
    app.add_handler(CommandHandler('tier 2', tier2_command))
    app.add_handler(CommandHandler('tier 3', tier3_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
