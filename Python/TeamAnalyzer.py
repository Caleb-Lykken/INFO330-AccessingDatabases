import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters


# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    print("Analyzing " + arg + " ...")
    # connect to pokemon.sqlite
    conn = sqlite3.connect("pokemon.sqlite")
    # get a cursor
    cursor = conn.cursor()
    # get the pokemon name, pokedex_number
    # extra credit** flexible input:
    # if the user inputs the pokemon's name or pokedex number, the program will still work
    if(arg.isdigit()):
        cursor.execute("SELECT pokedex_number, name FROM pokemon WHERE pokedex_number = " + arg )
    else:
        cursor.execute("SELECT pokedex_number, name FROM pokemon WHERE name = '" + arg + "'" )
    # put pokemon name into a variable
    name = cursor.fetchone()
    # get the pokemon's type1 and type2
    cursor.execute("SELECT type1, type2 FROM pokemon_types_view WHERE name = '" + name[1] + "'" )
    # put pokemon's type1 and type2 into a variable
    type_name = cursor.fetchone()
    # get the pokemon's against_XXX values
    cursor.execute("SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM battle WHERE type1name = '" + type_name[0] + "'" + " AND type2name = " + "'" + type_name[1] + "'" )
    # put the against_XXX values into a variable
    against = cursor.fetchone()
    # create loop to print the types that the pokemon is strong against
    counter = 0
    strong_against = []
    weak_against = []
    for n in against:
        if n > 1:
            strong_against.append(types[counter])
        elif n < 1:
            weak_against.append(types[counter])
        counter += 1
    
    # print the results
    print(name[1] + "(" + type_name[0] + " " + type_name[1] +")" +" is strong against:" + str(strong_against) + " but weak against:" + str(weak_against))
    # close the connection
    conn.close()
    # add the pokemon to the team list
    team.append(name[1])

    
    
# Ask the user if they want to save the team

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

