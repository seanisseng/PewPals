from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import requests

TOKEN: Final = '7231994891:AAHwgOQCgE1jWVDbkZKo8HeS_LVV04H1eMs'
BOT_USERNAME: Final = '@pewpalsbot'

type1 = [
    "\"How long have you been attending our church?\"",
    "\"Rice, Noodles, Bread Potatoes. Rank them from best to worst and explain.\"",
    "\"If you feel cold in a room, would you increase the temperature or put on a sweater? Why?\"",
    "\"What's your go-to comfort food?\"",
    "\"Some say everyone either looks like a Rat or Frog. Which category do you think I belong to?\"",
    "\"What line of work are you in? Do you find it fulfilling?\"",
    "\"What's the dumbest thing you ever did growing up?\"",
    "\"What have you been up to in the past week and how has that made you feel?\"",
    "\"What would you like to be known/remembered for?\"",
    "\"What activity do you take the most joy in doing?\"",
    "\"What is your idea of a restful day?\"",
    "\"How long have you been attending our church?\"",
]

type2 = [
    "\"What do you enjoy most about the sermons here?\"",
    "\"Have you been involved in any church activities recently?\"",
    "\"Which talk in the sermon series has been your favourite so far and why?\"",
    "\"What do you think is one thing we can be doing better as a church?\"",
    "\"How did you become a Christian?\"",
    "\"What have you been finding especially encouraging?\"",
    "\"What have you been finding especially discouraging?\"",
    "\"Have you been able to find ways to apply what you learn in church to your daily life?\"",
    "\"How can I pray for you?\"",
    "\"How is your Christian life going at the moment?\"",
    "\"Which aspect of God is most dear to you? Why do you hold closely to that?\"",
    "\"What aspect of God is hardest for you to grapple with? Why has it been a struggle?\"",
    "\"How has following Jesus been challenging for you?\"",
    "\"What has been occupying your head space recently?\"",
]

type3 = [
    "\"Who has been a role model / an influential person for you in your Christian faith and why?\"",
    "\"What's something you've been praying / thinking about from sermons / Bible studies / devotions?\"",
    "\"Can you tell me about a significant moment of spiritual growth or transformation in your life?\"",
    "\"How do you prioritise your spiritual life amidst your other responsibilities?\"",
    "\"Are there any aspects of your faith that you're currently questioning or exploring?\"",
    "\"Can you share a time when you experienced doubt or went through a crisis of faith?\"",
    "\"What role does prayer play in your life, and how do you maintain a consistent prayer life?\"",
    "\"What has been something you've been struggling to give up for the sake of the gospel?\"",
    "\"Has Christian living been feeling heavy? Why or Why not?\"",
    "\"Has your motivation for living been wholly the Gospel?\"",
    "\"Faith in Jesus must be a constant choice we make. Have you been placing your faith in the Gospel?\"",

]

def auto_forward(text: str):
    base_url = 'https://api.telegram.org/bot7231994891:AAHwgOQCgE1jWVDbkZKo8HeS_LVV04H1eMs/sendMessage?chat_id=-4245807653&text={}'.format(text)
    requests.get(base_url)

# Commmands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('All members working well')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('The Pew Pal Bot supplements our conversations with fellow believers by providing helpful questions. The goal is facilitate deeper spiritual friendships through Gospel centred convos.'
                                    '\n=== Pick a category of question ==='
                                    '\n\n/type1 - Ice Breakers. Simple fun and lighthearted questions that get the conversation going'
                                    '\n\n/type2 - Going Deeper. Questions to kickstart your Gospel conversations, not that intense'
                                    '\n\n/type3 - Getting Personal. The hard hitting questions that make you think and allow you to share your heart out'
                                    '\n\n/why - A short blurb unveiling the heart behind pew pals'
                                    '\n\n/feedback - This command is used for suggesting questions & providing feedback. Type the command followed by your feedback and enter')

async def tier1_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(type1))

async def tier2_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(type2))

async def tier3_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(type3))

async def why_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pew Pals was born from the firm conviction that the Church is built up to maturity through the ministry of the Pew, not a select few. A large bulk of this ministry is made up of the informal yet intentional gospel conversations that take place between members of the local body."
                                    "\n\nAccording to Paul, a properly functioning body looks like Jew, Greek, slave and free, having the same care for one another, seeking to love and build up one another (1 Cor 12). People who would otherwise never be caught in the same room together from the world's standpoint. That means that ministry of the pew is especially important between unlikely friends in the local body. We need them and they need us. It's this kind of body that displays the supernatural logic-defying power of the gospel for the world to see."
                                    "\n\nPew Pals was born to help facilitate these pew conversations. One of the pals behind this is an introvert that honestly finds these conversations hard. The other pal is an extrovert that enjoys putting people into awkward situations with difficult questions. But both pals pray this would be a useful tool in making many many more Pew Pals - for His glory and our good!")

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    new_text: str = text.replace("/feedback", '').strip()
    if new_text != '':
        auto_forward(new_text)
        await update.message.reply_text('Feedback received')
    else:
        await update.message.reply_text('No feedback received')

# Responses


def handle_response(text: str):
    processed: str = text.lower()

    if 'hello' in processed or 'hi' in processed or 'hey' in processed:
        return "Chat with others, not me!"

    if 'type1' in processed or 'type 1' in processed:
        return random.choice(type1)
    
    if 'type2' in processed or 'type 2' in processed:
        return random.choice(type2)
    
    if 'type3' in processed  or 'type 2' in processed:
        return random.choice(type3)
    
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
    app.add_handler(CommandHandler('type1', tier1_command))
    app.add_handler(CommandHandler('type2', tier2_command))
    app.add_handler(CommandHandler('type3', tier3_command))
    app.add_handler(CommandHandler('why', why_command))
    app.add_handler(CommandHandler('feedback', feedback_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=1)
