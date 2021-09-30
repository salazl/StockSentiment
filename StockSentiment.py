
from StockSentiment_functions import general_search, username_search #import functions from other file

function_picker = ['general', 'username']
function_choice = None

#asking the user which search type they want to perform
while function_choice not in function_picker:
        function_choice = input('Would you like to perform a '+"'"+'general'+"'"+' or a '+"'"+'username'+"'"+' search?')

if function_choice == 'general':
    general_search()

elif function_choice == 'username':
    username_search()

