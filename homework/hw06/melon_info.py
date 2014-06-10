"""
melon_info.py - Prints out all the melons in our inventory
"""

def print_melon(name, seedless, price, flesh, rind, ave_wt):

    hasseed = 'have'
    if seedless:
        hasseed = 'do not have'
    
    print "%ss %s seeds and are $%0.2f" % ( name, hasseed, price)

def main():

    from melons import (melon_name, melon_seedless, melon_price, flesh_color, 
                    rind_color, average_weight)

    for i in melon_name.keys():
        print_melon(melon_name[i], melon_seedless[i], melon_price[i], flesh_color[i], 
                    rind_color[i], average_weight[i])

if __name__ == '__main__':
    main()
