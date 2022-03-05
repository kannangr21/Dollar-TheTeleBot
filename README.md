# Dollar-TheTeleBot

Dollar is a Telegram bot that simply maintains expenses and also can be used to list the tasks.

***
### <u>**Tech Used:**</u>

- *Language* &nbsp;&nbsp;: Python 3.5 or above 
- *Framework* : pyTelegramBotAPI
- *Database* &nbsp;&nbsp; : MongoDB Atlas

***
### <u>**Working:**</u>

 - `/start` plays a vital role in creating a collection with user telegram user id as a key.  
 - Every entry will be updated in the database with respective commands in the chat.
 - `/help` explains about the commands to be used and the formats to be used.  
 
 ***
 ### <u>**Note:**</u>

 **A particular format has been used in every command that to be followed to read the messages and store it in the database.  
 Data might not be stored in the database correctly if the format is not followed properly.  
 The format for respective commands are given in the `/help` command.**
 ***
### <u>**Troubleshooting:**</u>

- Try `/reset` command once.
- If issue still persists, raise an issue [here](https://github.com/kannangr21/Dollar-TheTeleBot/issues). 
- Contact details can be found in bot's `/help` command.
