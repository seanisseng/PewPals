## **Description**

In our busy lives, it's easy for conversations to stay surface-level. The Pew Pal Bot helps guide discussions toward deeper, more spiritually enriching topics. By suggesting relevant and reflective questions, it encourages believers to engage in gospel-centered conversations that build up and strengthen spiritual friendships.

[@PewPalsbot](https://t.me/PewPalsbot) on Telegram

---

## **Features**

- **Category Selection**: Users can choose specific categories like *Intro*, *Work/Life*, *Church*, and *Christian Living* to tailor their conversations.  
- **Surprise Me!**: Can’t decide? Use the *Surprise Me!* button to get a random question from any category.  
- **Feedback Support**: Users can share suggestions or feedback using the `/feedback` command, helping improve the bot's content and functionality.  
- **Prayer Request Capture**: In a group chat, users can submit prayer requests with `/pray <request>` or a message starting with `Prayer request:` and review them later with `/prayers`.  

---

Let me know if you'd like any further refinements!
---

## **Commands**

Here are the available commands for interacting with The Pew Pal Bot:

| **Command**          | **Description**                                                        |
|-----------------------|------------------------------------------------------------------------|
| `/start`             | Launches the question menu to explore categories and start interacting.|
| `/help`              | Provides instructions on how to use the bot.                          |
| `/lore`              | Shares a short blurb about the heart and purpose behind Pew Pals.     |
| `/feedback`          | Allows users to suggest questions and provide feedback. Type the command followed by your feedback message. |
| `/pray`              | Adds a prayer request to the current group chat's running list.        |
| `/prayers`           | Returns the prayer requests that have been captured in the current chat. |
| `/clear_prayers`     | Clears the stored prayer request list for the current chat.            |

---

## **Installation**

To set up The Pew Pal Bot for your Telegram group or personal use, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/pew-pal-bot.git
   cd pew-pal-bot
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add the following:
   ```plaintext
   API_KEY=your-telegram-bot-token
   ```

   Replace `your-telegram-bot-token` with the token you received from [BotFather](https://core.telegram.org/bots#botfather).

3. **Run the Bot**:
   Start the bot using:
   ```bash
   python main.py
   ```

4. **Add the Bot to Telegram**:
   Search for your bot on Telegram (using the bot username) and click **Start**.

---

## **Usage**

1. Add the bot to your group or start a direct conversation.
2. Use `/question` to receive a random question, or `/category [name]` to explore specific topics.
3. Use it during small group sessions, one-on-one conversations, or personal reflection to foster deeper connections.
4. In a group, collect prayer requests with `/pray <request>` or a message that starts with `Prayer request:`.
5. Use `/prayers` to print the collated requests for the chat.

Note:
- If you want the bot to pick up ordinary group messages instead of only commands and replies, make sure Telegram privacy mode is disabled for the bot in BotFather.

---

## **Deploy to Heroku**

This repository is configured to run on Heroku as a **worker** dyno using long polling.

1. **Create the app and login**:
   ```bash
   heroku login
   heroku create <your-app-name>
   ```

2. **Set required config vars**:
   ```bash
   heroku config:set API_KEY=<your-telegram-bot-token>
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```
   If your default branch is `master`, use:
   ```bash
   git push heroku master
   ```

4. **Start the worker dyno**:
   ```bash
   heroku ps:scale worker=1
   ```

5. **Check logs**:
   ```bash
   heroku logs --tail
   ```

Notes:
- `Procfile` starts the bot with `python main.py`.
- Do not commit `.env`; use Heroku config vars in production.

