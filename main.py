from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder, CallbackQueryHandler
import random
import requests
import urllib.parse
import os

def load_env_file(file_path: str = ".env"):
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


load_env_file()

TOKEN: Final = os.getenv("API_KEY", "")
BOT_USERNAME: Final = '@pewpalsbot'
Group = "-4245807653"
AWAITING_FEEDBACK_KEY: Final = "awaiting_feedback"

intro = [
    "Rice, Noodles, Bread, Potatoes. Rank them from best to worst and explain.",
    "Some say that everyone either looks like a Rat or a Frog. Which category do you think I belong to?",
    "If you feel cold in a room, would you increase the temperature or put on a sweater? Why?",
    "What's your go-to comfort food?",
    "What's the dumbest thing you ever did growing up?",
    "What have you been up to in the past week and how has that made you feel?",
    "What would you like to be known/remembered for?",
    "What activity do you take the most joy in doing?",
    "What is your idea of a restful day?",
    "How long have you been attending our church?",
    "What are some of your fondest childhood memories?",
    "What book or movie left a lasting impression on you? Why?",
    "What's a secret talent that you have or a skill you're proud of?",
    "Guess if I'm an only child, older, younger, or a middle child?",
    "Exercise. Love it or hate it?",
    "What would you describe as your 'perfect day'?",
    "If you could take a week off from your regular life to immerse yourself in learning something new, what would it be?",
    "What are you excited about most in your life right now?"
]


church = [
    "What do you enjoy most about the sermons here?",
    "Have you been involved in any church activities recently?",
    "Which talk in the sermon series has been your favourite so far and why?",
    "What do you think is one thing we can be doing better as a church?",
    "How have you been actively living out church family?",
    "How has church family been an encouragement to you?",
    "How can I pray for you?",
    "How did you become a Christian?",
    "How would you describe your relationship with God?",
    "How are you finding church/small group? Anything you’re particularly excited or concerned about?",
    "How are your Christian friendships?",
    "How are your non-Christian friendships?",
    "Share a memory when you felt especially encouraged by someone/something in church.",]


christian = [
    "How did you become a Christian?",
    "How has your joy in the Lord been? Any thanksgiving in the past week?",
    "What have you been finding especially encouraging?",
    "What have you been finding especially discouraging?",
    "Have you been able to find ways to apply what you learn in church to your daily life?",
    "How has your faith inspired a decision you've made in the past week/month?",
    "What Bible story has had the most impact on you and why?",
    "Which aspect of God is most dear to you? Why do you hold closely to that?",
    "What aspect of God is hardest for you to grapple with? Why has it been a struggle?",
    "How has following Jesus been challenging for you?",
    "Who has been a role model / an influential person for you in your Christian faith and why?",
    "What's something you've been praying / thinking about from sermons / Bible studies / devotions?",
    "Can you tell me about a significant moment of spiritual growth or transformation in your life?",
    "Are there any aspects of your faith that you're currently questioning or exploring?",
    "Can you share a time when you experienced doubt or had your faith challenged? In what ways did it help you grow?",
    "What role does prayer play in your life, and how do you maintain a consistent prayer life? What have you been praying about?",
    "Has Christian living been feeling heavy?",
    "Has your motivation for living been wholly set in the Gospel?",
    "Faith in Jesus must be a constant choice we make. Have you been actively placing your faith in the Gospel?",
    "What have you been reading lately? What have you been learning from that?"
]

work = [
    "What line of work are you in? Do you find it fulfilling?",
    "How did you get into this line of work? Has there been anything you have especially enjoyed or struggled with?",
    "What has been occupying your head space recently?",
    "To what extent is career/studies an idol?",
    "Have you thought about what you might do in 1/5/10 years? What attracts you to this?",
    "When working, do you tend to be idle (undervaluing work) or an idolator (overvaluing work)?",
    "How do you prioritise your spiritual life amidst your other responsibilities?",
    "What has been something you've been struggling to give up for the sake of the gospel?",
    "What have you been excited about lately?",
    "What has been the highlight/low point of your week? What has been especially hard?"
]

all = intro + church + christian + work

def auto_forward(text: str):
    encoded_text = urllib.parse.quote(text)
    chat_id = '-4245807653' 
    base_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={encoded_text}'
    response = requests.get(base_url)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Intro", callback_data='option_1'), InlineKeyboardButton("Work/Life", callback_data='option_2')],
        [InlineKeyboardButton("Church", callback_data='option_3'), InlineKeyboardButton("Christian Living", callback_data='option_4')],
        [InlineKeyboardButton("Surprise Me!", callback_data='option_5')]
    ]

    # Create the markup with the buttons
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the menu
    await update.message.reply_text(
        'Select a category of Question 🤩:',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Grab a friend, pick a category of question and start chatting away 😁')
    
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 

    if query.data == 'option_1':
        response = random.choice(intro)
        await query.message.reply_text(response)
    elif query.data == 'option_2':
        response = random.choice(work)
        await query.message.reply_text(response)
    elif query.data == 'option_3':
        response = random.choice(church)
        await query.message.reply_text(response)
    elif query.data == 'option_4':
        response = random.choice(christian)
        await query.message.reply_text(response)
    elif query.data == 'option_5':
        response = random.choice(all)
        await query.message.reply_text(response)

async def lore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pew Pals was born from the firm conviction that the Church is built up to maturity through the ministry of the Pew, not a select few. A large bulk of this ministry is made up of the informal yet intentional gospel conversations that take place between members of the local body."
                                    "\n\nAccording to Paul, a properly functioning body looks like Jew, Greek, slave and free, having the same care for one another, seeking to love and build up one another (1 Cor 12). People who would otherwise never be caught in the same room together from the world's standpoint. That means that ministry of the pew is especially important between unlikely friends in the local body. We need them and they need us. It's this kind of body that displays the supernatural logic-defying power of the gospel for the world to see."
                                    "\n\nPew Pals was born to help facilitate these pew conversations. One of the pals behind this is an introvert that honestly finds these conversations hard. The other pal is an extrovert that enjoys putting people into awkward situations with difficult questions. But both pals pray this would be a useful tool in making many many more Pew Pals - for His glory and our good!")

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_waiting = context.user_data.get(AWAITING_FEEDBACK_KEY, False)

    if is_waiting:
        context.user_data[AWAITING_FEEDBACK_KEY] = False
        await update.message.reply_text('Feedback mode turned off. \nPlease type /feedback again if you want to provide feedback')
        return

    context.user_data[AWAITING_FEEDBACK_KEY] = True
    await update.message.reply_text(
        'Please type your question or suggestion in your next message'
    )

async def sean_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("How have you been struggling for the gospel?\n" + (" " * 26) + "🫵👁👅👁")

async def dezree_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You have summoned the beautiful Dezree! \n\nDezree is a legendary figure in the world of Pew Pals, known for being Sean's favourite. Her beauty is said to be so radiant that it can brighten even the darkest of days 😍😍😍")
# Responses


def handle_response(text: str):
    processed: str = text.lower()

    if 'hello' in processed or 'hi' in processed or 'hey' in processed:
        return "Chat with others, not me!"

    return 'I do not understand what you wrote'

async def handle_message(update: Update, context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if context.user_data.get(AWAITING_FEEDBACK_KEY, False):
        context.user_data[AWAITING_FEEDBACK_KEY] = False

        sender_name = update.effective_user.full_name if update.effective_user else "Unknown"
        sender_id = update.effective_user.id if update.effective_user else "Unknown"
        feedback_payload = f"Feedback from {sender_name} ({sender_id}) in {message_type}: {text}"

        auto_forward(feedback_payload)
        await update.message.reply_text('Feedback received. Thank you!')
        return

    if message_type == 'group'  or message_type == 'supergroup':
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

    if not TOKEN:
        raise RuntimeError(
            "Missing API_KEY. Set it in environment or add API_KEY=<token> to a .env file."
        )

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('lore', lore_command))
    app.add_handler(CommandHandler('feedback', feedback_command))
    app.add_handler(CommandHandler('Sean', sean_command))
    app.add_handler(CommandHandler('Dezree', dezree_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=1)
