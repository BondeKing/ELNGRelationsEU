




def make_new_d_point(data=[], str="", area=""):
    
    return {"data": data, "str":str, "area": area}



def sort_and_print_d_list(d_list):
    
    sorted_list = []
    sorted_list.append(d_list[0])
    
    for d_point in d_list[1:]:
        for i in range(len(sorted_list)):
            if sorted_list[i]["data"] < d_point["data"]:
                if i == 0:
                    sorted_list = [d_point] + sorted_list
                else:
                    sorted_list = sorted_list[:i] + [d_point] + sorted_list[i:]
                break
            elif i == len(sorted_list)-1:
                sorted_list.append(d_point)
                
    for d_point in sorted_list:
        print(d_point["str"])        

    return 