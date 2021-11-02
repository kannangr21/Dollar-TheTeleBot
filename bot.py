import telebot
from decouple import config
from database import get_database

API_TOKEN = config('API_KEY')
bot = telebot.TeleBot(API_TOKEN)
telebot.apihelper.SESSION_TIME_TO_LIVE = 5*60

db = get_database()
users_collection = db['Users']

"""
Commands :
-------------------- 
start - Dollar knows about you.
help - To help you.
reset - Reset all the lists.
newplan - To add a plan with an estimated amount.
viewplans - To view all the plans.
expplan - To add an expense under a plan.
plan - To view a particular plan.
delplan - To delete a plan.
exp - To add an expense out of planned event.
viewexp - To view all the expenses out of the plan.
delexp - To delete an expense.
note - To add a note.
viewnotes - To see the notes list.
delnote - To delete a note.
"""

# -------------- /start ------------------------

@bot.message_handler(commands = ["start"])
def startMsg(message):
    try:
        try:
            users_collection.insert_one({"_id": message.from_user.id, "plans":[], "expenses":[], "notes":[]})
        except Exception:
            return bot.reply_to(message, (f"Hello {message.from_user.first_name},\n" 
                                        "You know me already! Use /help to know me more"))
        return bot.reply_to(message,(f"Hello {message.from_user.first_name} 👋!\n" 
                                    "My name is Dollar💸, Your virtual pocket diary.\n"
                                    "I can maintain and calculate your expenses.\n"
                                    "Also, I can hold your notes in my memory🧠.\n"
                                    "Use /help to know more about me."))
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /reset --------------------------

@bot.message_handler(commands = ["reset"])
def resetData(message):
    try:
        users_collection.update_one({"_id": message.from_user.id}, {"$set":{"plans":[], "expenses":[], "notes":[]}}, upsert = True)
        return bot.reply_to(message, "Everything is reset. All your lists are empty now.")
    except:
        return bot.reply_to(message, "Sorry for the inconvenience, Something is not good in me.")

# -------------- /help ------------------------

@bot.message_handler(commands = ["help"])
def help(message):
    try:
        bot.reply_to(message,(
            "User guide to use *Dollar* 💸, your virtual pocket dairy to plan and maintain the expenses.\n"
            "\n*What's my work???*\n"
            "\n1️⃣ I can remember your plans."
            "\n2️⃣ I can remember the amount you've spent under any plan."
            "\n3️⃣ You can even tell me the expenses outside of a plan."
            "\n4️⃣ I have a good memory power to remember your notes."
            "\n\n*How to use me???*"
            "\n\n_---Plans and Expenses---_"
            "\n1️⃣ /newplan - To *create* a new plan with a budget.\n"
            "Format to use: `/newplan {Plan name} -c {plan code} -d {Optional description} -a {budget}`"
            "\n2️⃣ /viewplans - To *view* the plans and plan code.\n"
            "Format to use: `/viewplans`"
            "\n3️⃣ /expplan - To *add* an expense under a plan, this will be calculated from estimated budget.\n"
            "Format to use: `/expplan {plan code} -e {expense} -a {amount}`"
            "\n4️⃣ /plan - To view a plan in *detail* with expenses.\n"
            "Format to use: `/plan {plan code}`"
            "\n5️⃣ /delplan - To *delete* a plan and all the details related to a plan.\n"
            "Format to use: `/delplan {plan code}`\n\n"
            "_---Expenses out of plan---_"
            "\n1️⃣ /exp - To *add* an expense that is not in a plan.\n"
            "Format to use: `/exp {expense} -a {amount}`"
            "\n2️⃣ /viewexp - To *view* all the expenses out of any plan.\n"
            "Format to use: `/viewexp`"
            "\n3️⃣ /delexp - To *delete* a particular expense from the list.\n"
            "Format to use: `/delexp {exp number}`\n\n"
            "_---Notes---_"
            "\n1️⃣ /note - To *add* a note.\n"
            "Format to use: `/note {detail}`"
            "\n2️⃣ /viewnotes - To *view* all the notes.\n"
            "Format to use: `/viewnotes`"
            "\n3️⃣ /delnote - To *delete* a note\n"
            "Format to use: `/delnote {note number}`\n\n"
            "_---Codes---_\n"
            "`Plan name`: Name given to a plan, _can be a title_\n"
            "`Plan code`: A short code defined by you while adding a plan, _can be one or two letters_.\n"
            "`Description` (Optional): About the plan in detail, _can be long sentences_.\n"
            "`Budget`: Estimated amount for the plan.\n"
            "`Expense`: Expense title.\n"
            "`Amount`: Amount spent.\n"
            "`ExpNumber`: Expense number.(used to delete expense)\n"
            "\n_---Resetting---_\n"
            "/reset - To reset all the data.\n"
            "This will erase all plans, expenses, notes.\n"
            "\n*Contact my developer:*\n"
            "[Kannan G R](https://t.me/kannangr21)"
            ), parse_mode = "MarkDown")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /newplan ------------------------

@bot.message_handler(commands = ["newplan"])
def newplan(message):
    try:
        msg = message.text.split("/newplan ")
        try:
            msg = msg[1].split(' -')
        except IndexError:
            return bot.reply_to(message, ("Please use the format,"
            "\n`/newplan {Plan name} -c {Plan code} -d {Optional description} -a {budget}`"), 
            parse_mode = "MarkDown")
        newPlan = msg.pop(0)
        desc, code, amt = None, "", 0
        for element in msg:
            if element[0] == "c":
                try:
                    code = element.split("c ",1)[1]
                except:
                    code = element.split("c",1)[1]
            if element[0] == "d":
                try:
                    desc = element.split("d ",1)[1]
                except:
                    desc = element.split("d",1)[1]
            if element[0] == "a":
                try:
                    amt = float(element.split("a ",1)[1])
                except:
                    amt = float(element.split("a",1)[1])
        if amt == 0 or code == "":
            return bot.reply_to(message, (
            "*Format not recognized*"
            "\nTry using,"
            "\n`/newplan {Plan name} -c {Plan code} -d {Optional description} -a {budget}`"
            ),parse_mode = "MarkDown")
        plans = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0, "plans" : 1})
        plans = plans["plans"]
        for plan in plans:
            if plan["code"] == code:
                return bot.reply_to(message, (
                    f"Hey! It seems like you've already added *{code}* as the short code for *{plan['plan']}*.\n"
                    "Try adding another code for the new plan!"),
                    parse_mode = "MarkDown")
        data = {
            "code": code, 
            "plan": newPlan,
            "desc": desc,
            "amt" : amt,
            "spent" : 0,
            "expenses" : []
            }
        users_collection.update_one({"_id": message.from_user.id},{"$push":{"plans":data}})
        return bot.reply_to(message,f"*{newPlan}* - Plan added successfully with an estimated expense of *{amt}*",
                            parse_mode = "MarkDown")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /viewplans ------------------------

@bot.message_handler(commands = ["viewplans"])
def getPlans(message):
    try:
        plans = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0, "plans" : 1})
        plans = plans["plans"]
        if plans == []:
            return bot.reply_to(message, "No plans added yet!. Try /newplan to create a plan!")
        retmsg = "Your plans are,\n  *Plans* - *Codes*\n"
        i = 1
        for plan in plans:
            retmsg += f"{i}. {plan['plan']} - {plan['code']}\n"
            i += 1
        return bot.reply_to(message, retmsg, parse_mode="MarkDown")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /plan ------------------------

@bot.message_handler(commands = ["plan"])
def getOnePlan(message):
    try:
        try:
            code = message.text.split("/plan ")[1]
        except:
            return bot.reply_to(message, "Use `/plan {Plan code}` to view about a plan.\nUse /viewplans to get the codes.", 
            parse_mode = "MarkDown")
        plans = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0, "plans" : 1})
        plans = plans["plans"]
        for plan in plans:
            if plan["code"] == code:
                desc = "" 
                if plan['desc'] != None:
                    desc = f"*Description* - {plan['desc']}\n"
                retMsg = (f"*Code* - {plan['code']}\n"
                        f"*Plan* - {plan['plan']}\n"
                        +desc+
                        f"*Estimated amount* - {plan['amt']}\n"
                        "Expenses under this plan : ")
                i = 1  
                for exp in plan["expenses"]:
                    retMsg += f"\n{i}. {exp['desc']} - {exp['amt']}"
                    i += 1
                if i == 1:
                    retMsg += "\nNo amount has been spent for this plan.\nUse /expplan to add expenses on this plan."
                else:
                    retMsg += f"\n*Amount spent* - {plan['spent']}"
                    retMsg += f"\n*Balance* - {plan['amt']-plan['spent']}"
                return bot.reply_to(message, retMsg, parse_mode = "MarkDown")
        return bot.reply_to(message, "No such event is found!\nTry /viewplans to get the code or use /newplan to create a plan.")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /expplan ------------------------

@bot.message_handler(commands = ["expplan"])
def addExpPlan(message):
    try:
        try:
            msg = message.text.split("/expplan ")[1]
        except:
            return bot.reply_to(message, "Hey there, To add an expense use \n`/expplan {Plan code} -e {expense} -a {amount}`", 
            parse_mode = "MarkDown")
        msg = msg.split(" -")
        code = msg.pop(0)
        plans = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0, "plans" : 1})
        plans = plans["plans"]
        for x in plans:
            if code == x["code"]:
                exp, amt = "", 0
                for data in msg:
                    if data[0] == "e":
                        try:
                            exp = data.split("e ",1)[1]
                        except IndexError:
                            return bot.reply_to(message, ("*Format not recognized*"
                                                    "\nTry using,"
                                                    "\n`/expplan {Plan code} -e {expense} -a {amount}`"),
                                                    parse_mode = "MarkDown")        
                    if data[0] == "a":
                        try:
                            amt = data.split("a ",1)[1]
                        except IndexError:
                            return bot.reply_to(message, ("*Format not recognized*"
                                                    "\nTry using,"
                                                    "\n`/expplan {Plan code} -e {expense} -a {amount}`"), 
                                                    parse_mode = "MarkDown")
                if amt == 0 or exp == "":
                    return bot.reply_to(message, ("*Format not recognized*"
                                                    "\nTry using,"
                                                    "\n`/expplan {Plan code} -e {expense} -a {amount}`"), 
                                                    parse_mode = "MarkDown")
                expense = {
                    "desc" : exp,
                    "amt" : amt
                }
                x["spent"] += float(amt)
                x["expenses"].append(expense)
                users_collection.update_one({"_id": message.from_user.id},{"$set":{"plans":plans}})
                return bot.reply_to(message, "Expenses updated!")

        else:
            return bot.reply_to(message, (f"No plan named as *{code}* found!"
                                        "\nUse /viewplans to know the codes."), parse_mode = "MarkDown")    
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")        
    
# -------------- /delplan ------------------------

@bot.message_handler(commands = ["delplan"])
def deletePlan(message):
    try:
        try:
            code = message.text.split("/delplan ")[1]
        except:
            return bot.reply_to(message, (f"Hey {message.from_user.first_name},\n"
            "Try using `/delplan {Plan code}` to delete a plan!"), parse_mode="MarkDown")
        plans = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0, "plans" : 1})
        plans, i = plans["plans"], 0
        for plan in plans:
            if plan["code"] == code:
                plan = plans.pop(i)
                users_collection.update_one({"_id": message.from_user.id},{"$set":{"plans":plans}})
                desc = ""
                if plan['desc'] != None:
                    desc = f"*Description* - {plan['desc']}\n"
                retMsg = (f"*Code* - {plan['code']}\n"
                        f"*Plan* - {plan['plan']}\n"
                        +desc+
                        f"*Estimated amount* - {plan['amt']}\n"
                        f"*Amount spent* - {plan['spent']}\n"
                        "\nThe above plan has been deleted successfully.")        
                return bot.reply_to(message, retMsg, parse_mode = "MarkDown")
            i += 1
        return bot.reply_to(message, "No such plan found!\nTry /viewplans to get your plans.")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /exp ------------------------

@bot.message_handler(commands = ["exp"])
def addExpense(message):
    try:
        if message.text == "/exp":
            return bot.reply_to(message, ("To add an expense try the format,\n`/exp {expense} -a {amount}`\n"
                                        "To add an expense to the existing plan, try `/expplan`"), 
                                        parse_mode = "MarkDown")
        try:
            msg = message.text.split("/exp ")[1]
        except:
            return bot.reply_to(message, (f"Hello {message.from_user.first_name}!\n"
                                        "To add an expense try the format,\n`/exp {expense} -a {amount}`\n"
                                        "To add an expense to the existing plan, try /expplan"), parse_mode = "MarkDown")
        try:
            msg = msg.split(" -a ")
            desc = msg[0]
            amt = float(msg[1])
        except:
            return bot.reply_to(message, (f"Hello {message.from_user.first_name}!\n"
                                        "To add an expense, try the format,\n"
                                        "`/exp {expense} -a {amount}`"),parse_mode = "MarkDown")
        data = {
            "desc" : desc,
            "amt" : amt
        }
        users_collection.update_one({"_id": message.from_user.id}, {"$push":{"expenses": data}})
        return bot.reply_to(message, f"Your expense *{desc}* has been added.\nAnd the amount is *{amt}*",
                        parse_mode = "MarkDown")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /viewexp ------------------------

@bot.message_handler(commands = ["viewexp"])
def getExpenses(message):
    try:
        expenses = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0,"expenses" : 1})
        expenses = expenses["expenses"]
        if expenses == []:
            return bot.reply_to(message, (f"Hey {message.from_user.first_name},\n"
            "You haven't added any expense. Use /exp to add an expense that is not in a plan."))
        retMsg = "Your expenses are,\n"
        total, i = 0, 1
        for expense in expenses:
            total += expense['amt']
            retMsg += (f"{i}. {expense['desc']} - {str(expense['amt'])}\n")
            i += 1
        retMsg += f"\n*Total : {total}*"
        return bot.reply_to(message, retMsg, parse_mode = "MarkDown")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /delexp ------------------------

@bot.message_handler(commands = ["delexp"])
def delExpense(message):
    try:
        try:
            num = message.text.split("/delexp ")[1]
        except:
            return bot.reply_to(message, ("Try using the format,"
                                "\n`/delexp {expense number}`\n"
                                "Use /viewexp to know the expense number."),
                                parse_mode = "MarkDown")
        user_exp = users_collection.find_one({"_id": message.from_user.id},{"_id":0,"expenses": 1})
        user_exp = user_exp["expenses"]
        try:
            exp = user_exp.pop(int(num) - 1)
            users_collection.update_one({"_id":message.from_user.id},{"$set":{"expenses": user_exp}})
            return bot.reply_to(message, f"*{exp['desc']}* has been removed from the list", parse_mode = "MarkDown")
        except:
            return bot.reply_to(message, "No expense found!\nTry using /viewexp to get the expense number.")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /note ------------------------

@bot.message_handler(commands = ["note"])
def addNotes(message):
    try:
        try:
            msg = message.text.split("/note ")[1]
        except:
            return bot.reply_to(message,("Hey Buddy,"
            "\nTry using `/note {detail}` to add a note."),
            parse_mode = "MarkDown")
        users_collection.update_one({"_id": message.from_user.id}, {"$push":{"notes": msg}})
        return bot.reply_to(message, "Notes list has been updated.\nUse /viewnotes to see the list.")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /viewnotes ------------------------

@bot.message_handler(commands = ["viewnotes"])
def viewNotes(message):
    try:
        notes = users_collection.find_one({"_id": message.from_user.id}, {"_id":0, "notes":1})
        notes = notes["notes"]
        retMsg, i = "Here are your notes,\n", 1
        if notes == []:
            return bot.reply_to(message, ("Notes list is empty!\nUse /note to add notes."))
        for note in notes:
            retMsg += (f"*{i}*. {note}\n")
            i += 1
        return bot.reply_to(message, retMsg, parse_mode = "MarkDown")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

# -------------- /delnote ------------------------

@bot.message_handler(commands = ["delnote"])
def delNote(message):
    try:
        try:
            num = int(message.text.split("/delnote ")[1])
        except:
            return bot.reply_to(message, ("Kindly use,\n`/delnote {note number}` to delete a note."
                                        "\nUse /viewnotes to know the note number."), parse_mode = "MarkDown")
        user_notes = users_collection.find_one({"_id" : message.from_user.id},{"_id": 0,"notes": 1})
        user_notes = user_notes["notes"]
        try:
            delnote = user_notes.pop(num - 1)
            users_collection.update_one({"_id":message.from_user.id},{"$set":{"notes": user_notes}})
            return bot.reply_to(message, f"*{delnote}* has been removed from the Notes list.", parse_mode = "MarkDown")
        except:
            return bot.reply_to(message, "No note found in the given value.\nPlease use /viewnotes to know the number.")
    except:
        return bot.reply_to(message,(f"Sorry for the inconvenience, Something is not good in me.\n"
                                    "Trying /reset might help.\n"
                                    "*BUT REMEMBER:* _Reset will erase all your data (plans, expenses, notes)_"), 
                                    parse_mode = "MarkDown")

bot.infinity_polling()