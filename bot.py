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
newplan - To add a plan with an estimated amount.
viewplans - To view all the plans.
plan - To view a particular plan.
delplan - To delete a plan.
exp - To add an expense out of planned event.
viewexp - To view all the expenses out of the plan.
"""

@bot.message_handler(commands=["start"])
def startMsg(message):
    try:
        users_collection.insert_one({"_id": message.from_user.id, "plans":[], "expenses":[]})
    except Exception:
        return bot.reply_to(message, f"""Hello {message.from_user.first_name}! You know me already! Use /help to know me more""")
    return bot.reply_to(message,f"""Hello {message.from_user.first_name}! My name is Dollar, Your virtual pocket diary.\nI can maintain your expenses and calculate your expenses.\nI can help you\nI'm Testing my bot""")

@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message,"Hello! I'm Growing")

@bot.message_handler(commands=["newplan"])
def newplan(message):
    msg = message.text.split("/newplan ")
    try:
        msg = msg[1].split(' -')
    except IndexError:
        return bot.reply_to(message, """Please use the format\n```/newplan {plan name} -c {keyword for the plan (2 letters recommended)} -d {optional description} -a {Amount}```""")
    newPlan = msg.pop(0)
    if newPlan == "":
        return bot.reply_to(message, (
        "Plan name not added!"
        "\nTry using,"
        "\n```/newplan {Plan name} -c {keyword for the plan (2 letters recommended)} -d {optional description} -a {amount in numbers}```"
        "\n/// Remember to add spaces before flags ' -c', ' -d' and ' -a'///"
        ))
    desc, code, amt = None, None, 0
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
    if amt == 0:
        return bot.reply_to(message, (
        "Estimated Amount not added! Please use -a flag to add amount."
        "\nTry using,"
        "\n```/newplan {Plan name} -c {keyword for the plan (2 letters recommended)} -d {optional description} -a {amount in numbers}```"
        "\n/// Remember to add spaces before flags ' -d' and ' -a'///"
        ))
    plans = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0, "plans" : 1})
    plans = plans["plans"]
    for plan in plans:
        if plan["code"] == code:
            return bot.reply_to(message, (
                f"Hey! It seems like you've already added `{code}` as the short code for {plan['plan']}.\n"
                "Try adding another code for the same plan!"))
    data = {
        "code": code, 
        "plan": newPlan,
        "desc": desc,
        "amt" : amt
        }
    users_collection.update_one({"_id": message.from_user.id},{"$push":{"plans":data}})
    return bot.reply_to(message,f"{newPlan} - Plan added successfully with an estimated expense of {amt}")

@bot.message_handler(commands=["viewplans"])
def getPlans(message):
    plans = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0, "plans" : 1})
    plans = plans["plans"]
    if plans == []:
        return bot.reply_to(message, "No plans added yet!. Try /newplan to create a plan!")
    retmsg = "Your plans are \n"
    i = 1
    for plan in plans:
        retmsg += f"{i}. {plan['plan']} - {plan['code']}\n"
        i += 1
    return bot.reply_to(message, retmsg)

@bot.message_handler(commands=["plan"])
def getOnePlan(message):
    try:
        code = message.text.split("/plan ")[1]
    except:
        return bot.reply_to(message, "Use /plan {code} to view about the plan.\nUse /viewplans to get the codes.")
    plans = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0, "plans" : 1})
    plans = plans["plans"]
    for plan in plans:
        if plan["code"] == code:
            desc = "" 
            if plan['desc'] != None:
                desc = f"Description - {plan['desc']}\n"
            retMsg = (f"Code - {plan['code']}\n"
                    f"Plan - {plan['plan']}\n"
                    +desc+
                    f"Estimated amount - {plan['amt']}")        
            return bot.reply_to(message, retMsg)
    return bot.reply_to(message, "No such event is found!\nTry /viewplans to get the code or use /newplan to create a plan.")

@bot.message_handler(commands=["delplan"])
def deletePlan(message):
    try:
        code = message.text.split("/delplan ")[1]
    except:
        return bot.reply_to(message, f"Hey {message.from_user.first_name}, Try using /delplan "+"{shortcode} to delete a plan!")
    plans = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0, "plans" : 1})
    plans,i = plans["plans"], 0
    for plan in plans:
        if plan["code"] == code:
            plan = plans.pop(i)
            users_collection.update_one({"_id": message.from_user.id},{"$set":{"plans":plans}})
            desc = "" 
            if plan['desc'] != None:
                desc = f"Description - {plan['desc']}\n"
            retMsg = (f"Code - {plan['code']}\n"
                    f"Plan - {plan['plan']}\n"
                    +desc+
                    f"Estimated amount - {plan['amt']}\n"
                    "The above plan has been deleted successfully.")        
            return bot.reply_to(message, retMsg)
        i += 1
    return bot.reply_to(message, "No such plan found!\nTry /viewplans to get your plans.")

@bot.message_handler(commands = ["exp"])
def addExpense(message):
    if message.text == "/exp":
        return bot.reply_to(message, "To add an expense try the format,\n`/exp {detail} -a {amount}`\n"
                                        "To add an expense to the existing plan, try `/expplan`")
    try:
        msg = message.text.split("/exp ")[1]
    except:
        return bot.reply_to(message, (f"Hello {message.from_user.first_name}!\nTo add an expense try the format,\n`/exp"+" {detail} -a {amount}`\n"
                                        "To add an expense to the existing plan, try `/expplan`"))
    try:
        msg = msg.split(" -a ")
        desc = msg[0]
        amt = float(msg[1])
    except:
        return bot.reply_to(message, (f"Hello {message.from_user.first_name}!\nTo add an expense, try the format,\n`/exp"
                                       " {detail} -a {amount}`\n"))
    data = {
        "desc" : desc,
        "amt" : amt
    }
    users_collection.update_one({"_id": message.from_user.id}, {"$push":{"expenses": data}})
    return bot.reply_to(message, f"Your expense {desc} has been added.\nAnd the expense is {amt}")

@bot.message_handler(commands = ["viewexp"])
def getExpenses(message):
    expenses = users_collection.find_one({"_id" : message.from_user.id},{"_id" : 0,"expenses" : 1})
    expenses = expenses["expenses"]
    if expenses == []:
        return bot.reply_to(message, f"Hey {message.from_user.first_name}, You haven't added any expense. Use `/exp` to add an expense.")
    retMsg = "Your expenses are,\n"
    for expense in expenses:
        retMsg += (expense["desc"] + " - " + str(expense["amt"]) + "\n")
    return bot.reply_to(message, retMsg)
    

bot.polling()