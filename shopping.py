def adding(qty,item):
    filepath = "shopping_list\items.txt"
    try:
        with open(filepath,"a") as file:
            list_entry = item+","+qty+"\n"
            file.write(list_entry)
            return 1
    except IOError:
        return 0



def deleting(item):
    filepath = "shopping_list\items.txt"
    try:
        with open(filepath,'r') as file:
            lines = file.readlines()
            if len(lines)==0:
                return 2
            else:
                for line in lines:
                    if line.split(",")[0]==item:
                        lines.remove(line)
                        with open(filepath,'w') as file:
                            file.writelines(lines)
                            return 1
    except IOError:
        return 0


def editing(item,qty):
    filepath = "shopping_list\items.txt"
    try:
        with open(filepath,'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.split(",")[0]==item:
                    new_qty = qty
                    edited = item+','+new_qty+"\n"
                    lines[lines.index(line)] = edited
                    with open(filepath,'w') as file:
                        file.writelines(lines)
                        return 1
                
    except IOError:
        return 0



def recite():
    items = []
    filepath = "shopping_list\items.txt"
    try:
        with open(filepath,"r") as file:
            lines = file.readlines()
            if len(lines)!=0:
                for line in lines:
                    items.append(line.split(",")[1]+" of "+line.split(",")[0])
                return items
            else:
                return 2
    except IOError:
        return 0

def clearing():
    filepath = "shopping_list\items.txt"
    try:
        with open(filepath,"w") as file:
            file.write("")
            return 1
    
    except IOError:
        return 0