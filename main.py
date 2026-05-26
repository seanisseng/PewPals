from typing import Final
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    KeyboardButtonRequestChat,
)
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
PRAYER_REQUESTS_KEY: Final = "prayer_requests"
PENDING_PRAYERLIST_SELECTION_KEY: Final = "pending_prayerlist_selection"
AWAITING_PRAYERLIST_CHAT_SHARE_KEY: Final = "awaiting_prayerlist_chat_share"
PRAYERLIST_CHAT_REQUEST_ID_KEY: Final = "prayerlist_chat_request_id"
PRAYERLIST_CHAT_REQUEST_ID: Final = 1
PRAYER_PREFIXES: Final = (
    "prayer request:",
    "prayer request -",
    "prayer request",
    "prayer:",
    "prayer -",
)
CHAT_TITLES_KEY: Final = "chat_titles"
USER_GROUPS_KEY: Final = "user_groups"

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
        '<b>Welcome to Pew Pals!</b>\n'
        'Use the buttons below to generate a conversation question for your group.\n\n'
        'If you want to collect prayer requests instead,\n'
        '1. Add this bot to your group chat.\n'
        '2. Use /pray &lt;request&gt; to add your prayer request.\n'
        '3. In private chat, use /prayerlist then tap Choose a Group 👥 to select the group and view its list.',
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start: Opens the question menu (buttons for Intro, Work/Life, Church, Christian Living, Surprise Me!) and shows short onboarding. Clicking a button sends a random question from that category.\n\n"
        "/pray or /prayer: Adds or updates the current user’s prayer request for the current chat (one request per user).\n"
        " - NOTE: these commands only work inside group or supergroup chats. Add the bot to your group and run /pray or /prayer there.\n\n"
        "/prayerlist: Shows prayer requests depending on where you run it:\n"
        " - In a group/supergroup: run /prayerlist to see the prayer requests collected for that chat.\n"
        " - In a private DM with the bot: run /prayerlist, tap Choose a Group 👥, then pick the group. The selected group ID is used to fetch that group's prayer list.\n\n"
        "/clear_prayers: Clears the prayer request list for the current chat. NOTE: this command only works inside group or supergroup chats.\n\n"
        "/lore: Provides the bot’s about/mission text.\n\n"
        "/feedback: Toggles feedback mode for the user; when active the next message is forwarded to the owners and acknowledged.\n\n"
    )


def get_prayer_requests(context: ContextTypes.DEFAULT_TYPE):
    return context.chat_data.setdefault(PRAYER_REQUESTS_KEY, {})


def store_prayer_request(context: ContextTypes.DEFAULT_TYPE, update: Update, prayer_text: str):
    prayer_requests = get_prayer_requests(context)
    sender = update.effective_user
    sender_name = sender.full_name if sender else "Unknown"
    sender_id = str(sender.id) if sender else "unknown"

    prayer_requests[sender_id] = {"name": sender_name, "text": prayer_text}


def extract_prayer_request(text: str):
    lowered = text.strip().lower()

    for prefix in PRAYER_PREFIXES:
        if lowered.startswith(prefix):
            return text[len(prefix):].strip(" :-")

    return ""


def normalize_lookup_text(value: str):
    return " ".join(value.lower().split())


def track_user_group(context: ContextTypes.DEFAULT_TYPE, user_id: int, chat_id: int, title: str = ""):
    user_groups = context.application.bot_data.setdefault(USER_GROUPS_KEY, {})
    user_groups.setdefault(str(user_id), {})[str(chat_id)] = title


async def get_known_prayerlist_choices(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, query_text: str = ""):
    titles = context.application.bot_data.get(CHAT_TITLES_KEY, {})
    user_groups = context.application.bot_data.get(USER_GROUPS_KEY, {})
    scoped_groups = user_groups.get(str(user_id), {})
    normalized_query = normalize_lookup_text(query_text) if query_text else ""
    choices = []

    for chat_id_text, scoped_title in scoped_groups.items():
        try:
            chat_id = int(chat_id_text)
        except Exception:
            continue

        # Titles may be stored with int or str keys; try both
        title = scoped_title or titles.get(chat_id) or titles.get(str(chat_id)) or f"Group {chat_id}"
        if normalized_query and normalized_query not in normalize_lookup_text(title):
            continue

        choices.append((chat_id, title))

    choices.sort(key=lambda item: item[1].lower())
    return choices


async def show_prayerlist_choice_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, choices):
    context.user_data[PENDING_PRAYERLIST_SELECTION_KEY] = {str(chat_id): title for chat_id, title in choices}

    keyboard = []
    for chat_id, title in choices[:12]:
        keyboard.append([InlineKeyboardButton(title, callback_data=f"prayerlist_pick:{chat_id}")])

    keyboard.append([InlineKeyboardButton("Cancel", callback_data="prayerlist_cancel")])

    await update.message.reply_text(
        "Select a group to view its prayer list:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def build_prayerlist_chat_picker_markup() -> ReplyKeyboardMarkup:
    group_button = KeyboardButton(
        text="Choose a Group 👥",
        request_chat=KeyboardButtonRequestChat(
            request_id=PRAYERLIST_CHAT_REQUEST_ID,
            chat_is_channel=False,
        ),
    )

    return ReplyKeyboardMarkup(
        [[group_button]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def send_prayerlist_for_chat(update: Update, context: ContextTypes.DEFAULT_TYPE, target_chat_id: int):
    reply_target = update.effective_message
    if not reply_target:
        return

    chat_store = context.application.chat_data.get(target_chat_id)
    if not chat_store:
        await reply_target.reply_text('No prayer requests found for that group.')
        return

    prayers = chat_store.get(PRAYER_REQUESTS_KEY)
    if not prayers:
        await reply_target.reply_text('No prayer requests found for that group.')
        return

    await send_long_message(update, format_prayer_requests(prayers))


def format_prayer_requests(requests):
    lines = ["Prayer Requests List🙏🏻:"]

    for index, request in enumerate(requests.values(), start=1):
        lines.append(f"{index}. {request['name']}: {request['text']}")

    return "\n".join(lines)


async def send_long_message(update: Update, text: str):
    reply_target = update.effective_message
    if not reply_target:
        return

    max_length = 3800

    if len(text) <= max_length:
        await reply_target.reply_text(text)
        return

    current_chunk = []
    current_length = 0

    for line in text.splitlines():
        line_length = len(line) + 1
        if current_chunk and current_length + line_length > max_length:
            await reply_target.reply_text("\n".join(current_chunk))
            current_chunk = []
            current_length = 0

        current_chunk.append(line)
        current_length += line_length

    if current_chunk:
        await reply_target.reply_text("\n".join(current_chunk))


async def prayer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Allow this command only in group chats
    if update.effective_chat.type not in ("group", "supergroup"):
        await update.message.reply_text(
            'The /pray command is for group chats only.\n'
            'Add me to a group and use /pray <request>'
        )
        return

    prayer_text = " ".join(context.args).strip()

    if not prayer_text:
        await update.message.reply_text(
            'Add a prayer request like /pray For my faith and love in God to grow.'
        )
        return

    if update.effective_user and update.effective_chat:
        chat_title = getattr(update.effective_chat, "title", "") or f"Group {update.effective_chat.id}"
        track_user_group(context, update.effective_user.id, update.effective_chat.id, chat_title)

    store_prayer_request(context, update, prayer_text)

    await update.message.reply_text('Prayer request captured or updated.\n'
    'Use /prayerlist to see the running list.')


# Note: the old `prayers_command` was removed. Use `prayerlist_command` instead.


async def prayerlist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # If invoked inside a group, show that group's prayer list
    if update.effective_chat.type in ("group", "supergroup"):
        prayer_requests = get_prayer_requests(context)
        if not prayer_requests:
            await update.message.reply_text('No prayer requests have been captured yet in this chat.')
            return

        await send_long_message(update, format_prayer_requests(prayer_requests))
        return

    # Otherwise, private chat: allow lookup by forwarded message, chat id or group name
    if update.effective_chat.type != 'private':
        await update.message.reply_text('Please DM me this command or forward a group message to me.')
        return

    # In private chat, use Telegram's native group picker to select a chat and share its id.
    context.user_data[AWAITING_PRAYERLIST_CHAT_SHARE_KEY] = True
    context.user_data[PRAYERLIST_CHAT_REQUEST_ID_KEY] = PRAYERLIST_CHAT_REQUEST_ID
    await update.message.reply_text(
        "Tap the button below and select a group. I'll use that group ID to fetch its prayer list.",
        reply_markup=build_prayerlist_chat_picker_markup(),
    )


async def handle_shared_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message:
        return

    shared_chat = getattr(message, "chat_shared", None)
    if not shared_chat:
        return

    is_awaiting = context.user_data.get(AWAITING_PRAYERLIST_CHAT_SHARE_KEY, False)
    expected_request_id = context.user_data.get(PRAYERLIST_CHAT_REQUEST_ID_KEY)
    received_request_id = getattr(shared_chat, "request_id", None)

    if not is_awaiting:
        await message.reply_text(
            "Group received. Send /prayerlist when you want to fetch prayer requests.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    if expected_request_id is not None and received_request_id is not None and received_request_id != expected_request_id:
        await message.reply_text(
            "That group selection doesn't match the latest request. Send /prayerlist and try again.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    context.user_data.pop(AWAITING_PRAYERLIST_CHAT_SHARE_KEY, None)
    context.user_data.pop(PRAYERLIST_CHAT_REQUEST_ID_KEY, None)

    selected_chat_id = shared_chat.chat_id

        # Prefer a cached title (from when the bot saw the group) over the shared payload.
        # Be resilient to int vs str keys and use the user's known-groups mapping as a fallback.
        titles_cache = context.application.bot_data.get(CHAT_TITLES_KEY, {})
        shared_title = getattr(shared_chat, "title", None)
        selected_chat_key = str(selected_chat_id)

        # Check user-scoped known groups for a title
        user_groups = context.application.bot_data.get(USER_GROUPS_KEY, {})
        user_known_title = None
        if update.effective_user:
            user_known_title = user_groups.get(str(update.effective_user.id), {}).get(selected_chat_key)

        # Try int-keyed cache, then str-keyed cache, then user-known title, then shared payload
        selected_title = (
            titles_cache.get(selected_chat_id)
            or titles_cache.get(selected_chat_key)
            or user_known_title
            or shared_title
            or f"Group {selected_chat_id}"
        )

        # Store under a string key for consistent future lookups
        context.application.bot_data.setdefault(CHAT_TITLES_KEY, {})[selected_chat_key] = selected_title
    if update.effective_user:
        track_user_group(context, update.effective_user.id, selected_chat_id, selected_title)

    await message.reply_text(
        f"Fetching prayer list for {selected_title}...",
        reply_markup=ReplyKeyboardRemove(),
    )

    await send_prayerlist_for_chat(update, context, selected_chat_id)


async def clear_prayers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Allow clearing only in group chats
    if update.effective_chat.type not in ("group", "supergroup"):
        await update.message.reply_text('The /clear_prayers command can only be used in a group or supergroup chat.')
        return

    context.chat_data[PRAYER_REQUESTS_KEY] = {}
    await update.message.reply_text('Prayer request list cleared for this chat.')
    
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 

    if query.data == 'prayerlist_cancel':
        context.user_data.pop(PENDING_PRAYERLIST_SELECTION_KEY, None)
        await query.message.reply_text('Prayer list selection canceled.')
        return

    if query.data.startswith('prayerlist_pick:'):
        selected_chat_id = query.data.split(':', 1)[1]
        pending_choices = context.user_data.get(PENDING_PRAYERLIST_SELECTION_KEY, {})

        if selected_chat_id not in pending_choices:
            await query.message.reply_text('That prayer list selection is no longer available. Please send /prayerlist again.')
            return

        context.user_data.pop(PENDING_PRAYERLIST_SELECTION_KEY, None)
        await send_prayerlist_for_chat(update, context, int(selected_chat_id))
        return

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
    await update.message.reply_text("Pew Pals was born to help believers keep conversations going with thoughtful questions and shared prayer requests. It gives groups an easy way to spark deeper gospel-centered discussion and to collect requests they can pray through together."
                                    "\n\nAccording to Paul, a properly functioning body looks like Jew, Greek, slave and free, having the same care for one another, seeking to love and build up one another (1 Cor 12). People who would otherwise never be caught in the same room together from the world's standpoint. That means that ministry of the pew is especially important between unlikely friends in the local body. We need them and they need us. It's this kind of body that displays the supernatural logic-defying power of the gospel for the world to see."
                                    "\n\nPew Pals was born to help facilitate those conversations and prayers. One of the pals behind this is an introvert that honestly finds these conversations hard. The other pal is an extrovert that enjoys putting people into awkward situations with difficult questions. But both pals pray this would be a useful tool in making many many more Pew Pals - for His glory and our good!")

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
    await update.message.reply_text("How have you been struggling for the gospel? 🫵👁👅👁")
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
        # Cache the group's title so users can refer to it later from a private chat
        chat = update.message.chat
        if getattr(chat, 'title', None):
            # Store under string keys for consistency
            context.application.bot_data.setdefault(CHAT_TITLES_KEY, {})[str(chat.id)] = chat.title

        if update.effective_user:
            track_user_group(
                context,
                update.effective_user.id,
                chat.id,
                getattr(chat, 'title', None) or f"Group {chat.id}",
            )

        prayer_request = extract_prayer_request(text)

        if prayer_request:
            store_prayer_request(context, update, prayer_request)
            await update.message.reply_text('Prayer request captured or updated.\nUse /prayerlist to see the running list.')
            return

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
    app.add_handler(CommandHandler('pray', prayer_command))
    # Alias: allow /prayer to behave the same as /pray
    app.add_handler(CommandHandler('prayer', prayer_command))
    # Note: /prayers command has been removed. Use /prayerlist for viewing prayer lists.
    app.add_handler(CommandHandler('clear_prayers', clear_prayers_command))
    app.add_handler(CommandHandler('prayerlist', prayerlist_command))
    app.add_handler(CommandHandler('Sean', sean_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.StatusUpdate.CHAT_SHARED, handle_shared_chat))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=1)
