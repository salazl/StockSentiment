from StockSentiment_paired import paired_general_search, paired_username_search
from StockSentiment_unpaired import unpaired_general_search, unpaired_username_search

pair_function_picker = ['paired', 'unpaired']
pair_function_choice = None

#asking the user which search type they want to perform
while pair_function_choice not in pair_function_picker:
        pair_function_choice = input('Would you like to perform a '+"'"+'paired'+"'"+' or '+"'"+'unpaired'+"'"+' search?')

if pair_function_choice == 'paired':
    type_function_picker = ['general', 'username']
    type_function_choice = None
    
    while type_function_choice not in type_function_picker:
        type_function_choice = input('Would you like to perform a '+"'"+'general'+"'"+' or a '+"'"+'username'+"'"+' search?')
        
    if type_function_choice == 'general':
        paired_general_search()
        
    elif type_function_choice == 'username':
        paired_username_search()

elif pair_function_choice == 'unpaired':
    type_function_picker = ['general', 'username']
    type_function_choice = None
    
    while type_function_choice not in type_function_picker:
        type_function_choice = input('Would you like to perform a '+"'"+'general'+"'"+' or a '+"'"+'username'+"'"+' search?')
        
    if type_function_choice == 'general':
        unpaired_general_search()
        
    elif type_function_choice == 'username':
        unpaired_username_search()
