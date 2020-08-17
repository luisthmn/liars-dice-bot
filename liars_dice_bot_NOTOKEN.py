# This is the code for a bot that allows the game liars dice to be played on a discord server
import discord
import random
from itertools import cycle

# Bot methods
# --------------------------------------------------------------


# param: value of the dice to be drawn
def draw_dice(value):
    if value == 1:
        return 'images/one.png'
    elif value == 2:
        return 'images/two.png'
    elif value == 3:
        return 'images/three.png'
    elif value == 4:
        return 'images/four.png'
    elif value == 5:
        return 'images/five.png'
    elif value == 6:
        return 'images/six.png'


# Bot variables
# ----------------------------------------------------------------
help_string = """
!lobby - Set up a game lobby
!join  - Join the lobby
!quit  - End current game or quit started lobby
!start - Start game with players in lobby
!list  - List out players in turn order
!xdy   - Make a bid - x = Quantity of dice, y = Face of dice
!liar  - Accuse previous player of being a liar
!bid   - See current bid

Want to learn how to play?
"""
client = discord.Client()
client.loby_started = False
client.game_started = False
client.table = {
    "players": [],
    "quantity": [],
    "dice": []
}
client.bid_quantity = 0
client.bid_face = 0
client.turn = ""
client.previous = ""
aux_list = []
# -----------------------------------------------------------------


@ client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# List of programmed responses of the bot
@ client.event
async def on_message(message):

    # Ignore messages from bot itself
    if message.author == client.user:
        return

    # Print out the bot commands
    if message.content.startswith('!help'):
        await message.channel.send('Commands`{0}`'.format(help_string))
        await message.channel.send('https://www.wikihow.com/Play-Liar%27s-Dice')

    #!lobby command responses
    # --------------------------------------------------------------------------------------------------------------
    # Start lobby when lobby is started and game not started
    if message.content.startswith('!lobby') and not client.loby_started and not client.game_started:
        await message.channel.send('Hello! A new game lobby has been created, use the `!join` command to join it and `!start` to start the game!')
        client.loby_started = True

    # Start lobby when game is started
    elif message.content.startswith('!lobby') and client.game_started:
        await message.channel.send('Sorry, there is already a game started on this channel, wait for it to end or try another channel')

    # Start lobby when lobby is started and game not started
    elif message.content.startswith('!lobby') and client.loby_started and not client.game_started:
        await message.channel.send('There is already a lobby started! use the `!join` command to join it')

    # --------------------------------------------------------------------------------------------------------------

    #!join command responses
    # --------------------------------------------------------------------------------------------------------------
    if message.content.startswith('!join') and client.game_started:
        await message.channel.send('Sorry, there is already a game in progress, wait for it to end or try another channel')

    # join command when there is no lobby avaiable
    if message.content.startswith('!join') and not client.loby_started:
        await message.channel.send('There isn\'t a lobby to join! You can create one by using `!lobby`')

    # join command when player is in the game
    if message.content.startswith('!join') and client.loby_started and message.author in client.table["players"]:
        await message.channel.send('You are already in the lobby {0}! Use the `!list` command if you need to see the list of players'.format(message.author.name))

    # join command when there is a lobby avaiable
    if message.content.startswith('!join') and client.loby_started and message.author not in client.table["players"]:
        client.table["players"].append(message.author)
        client.table["quantity"].append(5)
        client.table["dice"].append([])
        await message.channel.send('Welcome to the lobby {0}! The game will start shortly'.format(message.author.name))
    # --------------------------------------------------------------------------------------------------------------

    #!quit command responses
    # --------------------------------------------------------------------------------------------------------------
    # Use quit command with no active game
    if message.content.startswith('!quit') and not client.loby_started and not client.game_started:
        await message.channel.send('There is no active game or lobby at the moment!')

    # Use quit command with active lobby
    if message.content.startswith('!quit') and client.loby_started:
        await message.channel.send('`Lobby has been terminated`')
        client.loby_started = False
        client.table = {
            "players": [],
            "quantity": [],
            "dice": []
        }
        client.bid_quantity = 0
        client.bid_face = 0

    # Use quit command with active game
    if message.content.startswith('!quit') and client.game_started:
        await message.channel.send('`Game has been terminated`')
        client.game_started = False
        client.table = {
            "players": [],
            "quantity": [],
            "dice": []
        }
        client.bid_quantity = 0
        client.bid_face = 0

    # --------------------------------------------------------------------------------------------------------------

    #!start command responses
    # --------------------------------------------------------------------------------------------------------------
    # Start command with game in progress
    if message.content.startswith('!start') and not client.loby_started and client.game_started:
        await message.channel.send('`There is already a game in progress!`')

    # Start command with no lobby
    if message.content.startswith('!start') and not client.loby_started and not client.game_started:
        await message.channel.send('`There is no lobby active! use the `!lobby` command to start one`')

    # Start command with lobby but not ebough players
    if message.content.startswith('!start') and client.loby_started and len(client.table["players"]) < 2:
        await message.channel.send('`There are not enough players in the lobby! use the `!join` command to join, at least 2 players are needed`')

    # All game rules are inside of this statement
    # Start command with lobby but not enough players
    if message.content.startswith('!start') and client.loby_started and len(client.table["players"]) >= 2:
        # while len(client.table["players"]) > 1:
        client.loby_started = False
        client.game_started = True
        client.player_cycle = cycle(client.table["players"])
        client.turn = next(client.player_cycle)

        await message.channel.send('`The game is on! Here are your dice (Check your DMs)`')
        # We send each player their dice values
        for i, x in enumerate(client.table["players"]):
            for y in range(client.table["quantity"][i]):
                dice_value = random.randint(1, 6)
                client.table["dice"][i].append(dice_value)
                await x.send(file=discord.File(draw_dice(dice_value)))
            await x.send("Dice values: {0}".format(client.table["dice"][i]))

        # Dice values have been sent, we print out table status
        await message.channel.send("`Dice have been rolled, here is the table status\n`")
        for i, x in enumerate(client.table["players"]):
            del aux_list[:]
            await message.channel.send("{0} dice:".format(x.name))
            for y in range(client.table["quantity"][i]):
                aux_list.append('?')
            await message.channel.send("{0}".format(aux_list) + " Total: " + str(len(aux_list)) + " dice")
        del aux_list[:]
        await message.channel.send("`{0} is the player in turn, make your move`".format(client.turn.name))
    # --------------------------------------------------------------------------------------------------------------

    # !xdy and !liar command respondes
    # --------------------------------------------------------------------------------------------------------------

    # xdy commands when game is on and player is in turn
    if message.content.startswith('!') and client.game_started and message.author == client.turn and message.content[1:].split("d")[0].isdigit() and message.content[1:].split("d")[1].isdigit():
        mensaje_separado = message.content[1:].split("d")

        if int(mensaje_separado[0]) <= int(client.bid_quantity) and int(mensaje_separado[1]) <= int(client.bid_face):
            await message.channel.send('`Invalid bid {0}, remember that your bid has to be higher in quantity of dice and/or face of dice, try that again`'.format(message.author.name))
        else:
            client.bid_quantity = mensaje_separado[0]
            client.bid_face = mensaje_separado[1]

            number_of_dice = 0
            for x in client.table["quantity"]:
                number_of_dice += x

            # for i, x in enumerate(client.table["players"]):
            #    if x == message.author:
            #        dados_jugador = client.table["dice"][i]

            if int(client.bid_quantity) < 1 or int(client.bid_face) < 1 or int(client.bid_face) > 6 or int(client.bid_quantity) > number_of_dice:
                await message.channel.send('`Invalid bid, try that again {0}`'.format(message.author.name))
            else:
                await message.channel.send('`Current bid:`')
                await message.channel.send('Quantity: {0}'.format(client.bid_quantity))
                await message.channel.send(file=discord.File(draw_dice(int(client.bid_face))))
                client.previous = client.turn
                client.turn = next(client.player_cycle)
                await message.channel.send('`{0} is the player in turn, make your move`'.format(client.turn.name))

    #!liar command with no bid when game is not on
    if message.content.startswith('!liar') and client.bid_quantity == 0 and client.bid_face == 0:
        await message.channel.send('There is no bid to accuse!')

    if message.content.startswith('!liar') and client.bid_quantity != 0 and client.bid_face != 0 and message.author == client.turn:
        await message.channel.send(str(client.turn.name) + ' has accused ' + str(client.previous.name) + " of being a liar!")
        await message.channel.send("\n`Table status`")
        for i, x in enumerate(client.table["players"]):
            await message.channel.send("{0} dice:".format(x.name))
            await message.channel.send("{0}".format(client.table["dice"][i]))

        real_quantity = 0
        for x in client.table["dice"]:
            real_quantity += x.count(int(client.bid_face))
        await message.channel.send('\n`Results`')
        await message.channel.send(file=discord.File(draw_dice(int(client.bid_face))))
        await message.channel.send('`Bid: {0}`'.format(client.bid_quantity))
        await message.channel.send('`Actual quantity: {0}`'.format(real_quantity))

        # We take a die away from the loser and check if the game is over
        if real_quantity >= int(client.bid_quantity):
            await message.channel.send("`The bid was correct! %s is not a liar and %s loses a dice`" % (client.previous.name, client.turn.name))
            client.bid_quantity = 0
            client.bid_face = 0
            for i, x in enumerate(client.table["players"]):
                if x.name == client.turn.name:
                    client.table["quantity"][i] -= 1
                    if client.table["quantity"][i] == 0:
                        client.turn = next(client.player_cycle)
                    break
        else:
            await message.channel.send("`The bid was NOT correct! %s is a liar and loses a dice`" % (client.previous.name))
            client.bid_quantity = 0
            client.bid_face = 0
            for i, x in enumerate(client.table["players"]):
                if x.name == client.previous.name:
                    client.table["quantity"][i] -= 1
                    client.turn = client.previous
                    if client.table["quantity"][i] == 0:
                        client.previous = next(client.player_cycle)
                    break

        # We check if any player has lost the game
        for i, x in enumerate(client.table["quantity"]):
            if x == 0:
                await message.channel.send('\n\n`{0} has been eliminated from the game!\n\n`'.format(client.table["players"][i].name))
                del client.table["players"][i]
                del client.table["quantity"][i]
                del client.table["dice"][i]
                client.player_cycle = cycle(client.table["players"])

        # We check if the game has ended
        if len(client.table["players"]) == 1:
            await message.channel.send('\n\n`{0} has won the game! The match is over`'.format(client.table["players"][0].name))
            client.game_started = False
            client.loby_started = False
            client.table = {
                "players": [],
                "quantity": [],
                "dice": []
            }
            client.bid_quantity = 0
            client.bid_face = 0
        else:
            await message.channel.send('\n\n`New round starting! Here are your dice (Check your DMs)`')

            for x in client.table["dice"]:
                del x[:]

            # We send each player their dice values
            for i, x in enumerate(client.table["players"]):
                for y in range(client.table["quantity"][i]):
                    dice_value = random.randint(1, 6)
                    client.table["dice"][i].append(dice_value)
                    await x.send(file=discord.File(draw_dice(dice_value)))
                await x.send("Dice values: {0}".format(client.table["dice"][i]))

            # Dice values have been sent, we print out table status
            await message.channel.send("`Dice have been rolled, here is the table status\n`")
            for i, x in enumerate(client.table["players"]):
                del aux_list[:]
                await message.channel.send("{0} dice:".format(x.name))
                for y in range(client.table["quantity"][i]):
                    aux_list.append('?')
                await message.channel.send("{0}".format(aux_list) + " Total: " + str(len(aux_list)) + " dice")
            del aux_list[:]
            await message.channel.send("`{0} is the player in turn, make your move`".format(client.turn.name))
    # --------------------------------------------------------------------------------------------------------------

    #!list command responses
    # --------------------------------------------------------------------------------------------------------------
    if message.content.startswith('!list') and client.game_started:
        await message.channel.send('`Players in the game`')
        await message.channel.send('`' + ''.join([(str(x.name) + "\n") for x in client.table["players"]]) + '`')

    if message.content.startswith('!list') and client.loby_started and len(client.table["players"]) > 0:
        await message.channel.send('`Players in the lobby`')
        await message.channel.send('`' + ''.join([(str(x.name) + "\n") for x in client.table["players"]]) + '`')

    if message.content.startswith('!list') and client.loby_started and len(client.table["players"]) == 0:
        await message.channel.send('`No players in lobby!`')

    if message.content.startswith('!list') and not client.loby_started and not client.game_started:
        await message.channel.send('`No game or lobby is active at the moment`')
    # --------------------------------------------------------------------------------------------------------------

    #!bid command responses
    # --------------------------------------------------------------------------------------------------------------
    if message.content.startswith('!bid') and (int(client.bid_quantity) == 0 or int(client.bid_face) == 0):
        await message.channel.send('`No current bid`')

    if message.content.startswith('!bid') and (int(client.bid_quantity) > 0 and int(client.bid_face) > 0):
        await message.channel.send('`Current bid:`')
        await message.channel.send('Quantity: {0}'.format(client.bid_quantity))
        await message.channel.send(file=discord.File(draw_dice(int(client.bid_face))))
    # --------------------------------------------------------------------------------------------------------------

    # Bot token
client.run('Insert your token here')
