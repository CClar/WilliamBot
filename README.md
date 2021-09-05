# WilliamBot
William, also known as Bill, used to split bills on discord

## Prerequisites 
* Download and install python3 - https://www.python.org/downloads/
* pip install -U discord.py
* pip install -U python-dotenv

## Setup
Go to https://discord.com/developers/applications and create a new application

1. Create the new app and give it a name
<img src="https://github.com/CClar/WilliamBot/blob/master/README%20images/1-Make%20Application.png?raw=true?sanitize=true">
2. Next, go to the Bot page and create a bot to use within your server 
<img src="https://github.com/CClar/WilliamBot/blob/master/README%20images/2-Make%20Bot%20.png?raw=true?raw=true?sanitize=true">
3. Then generate a link that will help us add the bot to your server (Note: We grant Administrator permissions here, but less permissions can be granted)
<img src="https://github.com/CClar/WilliamBot/blob/master/README%20images/3-GetBotUrl.png?raw=true?raw=true?sanitize=true">
4. Now we will add it to our server, follow the link, choose your server from the drop downbox and click continue
<img src="https://github.com/CClar/WilliamBot/blob/master/README%20images/4-InviteBot.png?raw=true?raw=true?sanitize=true">
5. After, go back to the bot page and copy the bot token that we will use for our application
<img src="https://github.com/CClar/WilliamBot/blob/master/README%20images/5-CopyToken.png?raw=true?raw=true?sanitize=true">
6. Create a .env file with a `DISCORD_TOKEN=${token}` in the same directory as your python script, where ${token} is your discord bot token
7. Lastly, open a commandline in the directory where the python script is located and run the command `python WilliamBot.py`

## Using the bot
Run !help to find out how to use the commands
React under each item according to who is splitting the item


## Improvements that have been considered but not done:
* Use an extra db to keep track of data, right now the bot only supports a single server because of this
* Validations around arguments, message existing, data existing, previous bill existing

