from context import garn

from garn.system_wide import truncate_list 

def equal_files(file_name_1, file_name_2):
    """Test if files are identical, return bool"""
    
    with open(file_name_1) as file_1:
        with open(file_name_2) as file_2:
            for x in file_1:
                if x != file_2.readline():
                    return False
    return True


### Initialize from arguments, calculate transmission, write test###
# 3D 
test_wire_3d = garn.Wire3D(base=3, wire_length=30, lead_length=5,
                           identifier="simple-test-3D", step_length=1,
                           start_top=True, start_right=True,
                           start_left=True, start_bottom=False,
                           end_top=True, end_right=True,
                           end_left=True, end_bottom=False)
#garn.system_plot(test_wire_3d)
test_wire_3d.transmission(0, 1, 10, print_to_commandline=False)
          
if equal_files("data-simple-test-3D", "data-ref-3D"):        
    print("3D transmission and write test... Passed")
else:
    print("3D transmission and write test... Failed")
    
#2D 
test_wire_2d = garn.Wire2D(base=3, wire_length=30, lead_length=5,
                           identifier="simple-test-2D", step_length=1,
                           start_right=True, start_left=True,
                           end_right=True, end_left=True)
#garn.system_plot(test_wire_2d)
test_wire_2d.transmission(0, 1, 10, print_to_commandline=False)

if equal_files("data-simple-test-2D", "data-ref-2D"):        
    print("2D transmission and write test... Passed")
else:
    print("2D transmission and write test... Failed")


### Initialize from file###
#3D
test_wire_from_file_3d = garn.Wire3D(file_name="data-simple-test-3D")
if test_wire_3d == test_wire_from_file_3d:
    print("3D initialize from file test... Passed")
else:
    print("3D initialize from file test... Failed")

    # Loosing precision when writing to file
    if truncate_list(test_wire_3d.transmission_data, 3) == truncate_list(test_wire_from_file_3d.transmission_data, 3):
       print("    Transmission_data... OK")
    else:
        print("    Transmission_data... Wrong")
        
    if test_wire_3d.base == test_wire_from_file_3d.base:
       print("    base... OK")
    else:
        print("    base... Wrong")

    if test_wire_3d.wire_length == test_wire_from_file_3d.wire_length:
       print("    Wire_length... OK")
    else:
        print("    Wire_length... Wrong")

    if test_wire_3d.lead_length == test_wire_from_file_3d.lead_length:
       print("    lead_length... OK")
    else:
        print("    lead_length... Wrong")

    if test_wire_3d.t == test_wire_from_file_3d.t:
       print("    t... OK")
    else:
        print("    t... Wrong")

#2D
test_wire_from_file_2d = garn.Wire2D(file_name="data-simple-test-2D")
if test_wire_2d == test_wire_from_file_2d:
    print("2D initialize from file test... Passed")
else:
    print("2D initialize from file test... Failed")
    # Further diagnosis (note precision is lost when writing to file)
    if truncate_list(test_wire_2d.transmission_data, 3) == truncate_list(test_wire_from_file_2d.transmission_data, 3):
       print("    Transmission_data... OK")
    else:
        print("    Transmission_data... Wrong")
        
    if test_wire_2d.base == test_wire_from_file_2d.base:
       print("    base... OK")
    else:
        print("    base... Wrong")

    if test_wire_2d.wire_length == test_wire_from_file_2d.wire_length:
       print("    Wire_length... OK")
    else:
        print("    Wire_length... Wrong")

    if test_wire_2d.lead_length == test_wire_from_file_2d.lead_length:
       print("    lead_length... OK")
    else:
        print("    lead_length... Wrong")

    if test_wire_2d.t == test_wire_from_file_2d.t:
       print("    t... OK")
    else:
        print("    t... Wrong")

