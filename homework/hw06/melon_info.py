"""
melon_info.py - Prints out all the melons in our inventory
"""

def get_melon_attrib():

#initialize dictionaries for each attribute 
#append to this section when new attributes are added
    from melons import (
        melon_name, 
        melon_seedless, 
        melon_price, 
        flesh_color, 
        rind_color, 
        average_weight
        )

#create a dictionary with key = label, value = attribute dictionary initialized above
#append to this section when new attributes are added
    melon_attrib_dict = {
        'name': melon_name, 
        'seedless': melon_seedless, 
        'price':melon_price, 
        'flesh': flesh_color, 
        'rind': rind_color, 
        'ave_wt': average_weight, 
    }

    return melon_attrib_dict

def print_melon(name, seedless, price, flesh, rind, ave_wt):

    hasseed = 'have'
    if seedless:
        hasseed = 'do not have'
    
    print "%ss %s seeds and are $%0.2f" % ( name, hasseed, price)

def main():

    melon_attrib_dict = get_melon_attrib()
    melon_attrib_label = melon_attrib_dict.keys()      #generate a list of the keys

    for i in melon_attrib_dict['name'].keys():
        print_melon(
            melon_attrib_dict['name'][i],
            melon_attrib_dict['seedless'][i],
            melon_attrib_dict['price'][i],
            melon_attrib_dict['flesh'][i],
            melon_attrib_dict['rind'][i],
            melon_attrib_dict['ave_wt'][i],
        )

if __name__ == '__main__':
    main()
