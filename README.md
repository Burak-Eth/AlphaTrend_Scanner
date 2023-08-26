# AlphaTrend_Scanner
 The provided Python script serves as a cryptocurrency trading strategy automation tool. It leverages the Alpha Trend (AT) indicator to make trading decisions based on buy and sell signals. The script collects trading data from the Binance Futures API, calculates the AT values for various trading pairs, and optimizes the DCA strategy for each pair. The DCA strategy involves buying and selling a cryptocurrency based on the AT signals, aiming to achieve a certain minimum profit percentage. The script continuously scans the trading pairs, detects buy and sell signals, and sends notifications through the Telegram Bot API to keep the trader informed about potential trading opportunities. This code provides a comprehensive framework to automate cryptocurrency trading based on technical indicators and predefined profit criteria.

---
<b> To install the necessary dependencies using the requirements.txt file, follow these instructions: </b>

  1. Open a terminal or command prompt on your system.
  2. Navigate to the directory where your Python script and requirements.txt file are located. You can use the cd command to change directories.
  3. Run the following command to install the required packages using pip:
     
     ```

     pip install -r requirements.txt

     ```

---

<b> You can follow the steps below to learn your Telegram user ID </b> 

  1. Open the Telegram application.
  2. In the top right corner, type @userinfobot in the search bar. This represents Telegram's official user information bot.
  3. Select @userinfobot and start interacting with the bot by clicking the 'Start' button.
  4. The bot will provide you with your user ID. This is usually in the form of a numerical sequence.

---

**To create a Telegram bot and obtain its token, follow these instructions:**

  1. *BotFather Interaction:* Open the Telegram app and search for "BotFather." This is the official bot provided by Telegram for creating and managing bots.
  2. *Start a Chat with BotFather:* Start a chat with BotFather by sending a message to it. You can say something like "Hi" or "/start."
  3. *Create a New Bot:* To create a new bot, send the command `/newbot`. BotFather will guide you through the process. You'll need to provide a name and a username for your bot. The username should end with "_bot." For example, "MyAwesomeBot_bot."
  4. *Receive Token:* After creating the bot, BotFather will provide you with a token for your bot. This token is a long alphanumeric string that you'll need to access the Telegram Bot API. Copy and securely store this token.
  5. *Privacy Mode:* You can configure privacy mode for your bot by interacting with BotFather. Privacy mode prevents your bot from receiving messages sent in groups unless the message starts with a command (i.e., "/"). This is useful to avoid unintended interactions.

Please note that you should keep your bot token confidential and never share it publicly. It's used as an authentication key to access the Telegram Bot API on behalf of your bot. If someone gains access to your bot token, they can control your bot.

Remember that this is a general overview of the process. The exact steps might slightly differ based on updates to the Telegram app or platform. Always refer to the official Telegram documentation or resources for the most accurate and up-to-date information.
