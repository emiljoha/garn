from math import sqrt

def _read_file_to_wire(wire, file_name):
    """ Initialize variables for wire instance from data file.
    
    Internal function that gives the ´wire´ the same properties as the
    wire used to produce the file ´file_name´

    .. warning::
        This method will write over all prior attributes of `wire` with
        those specified in the `file_name` file. 
                 

    Parameters
    ----------
    wire : :class:`garn.Wire3D` or :class:`garn.Wire2D`
    file_name : str
    
    """
    
    f = open(file_name)

    identifier = 0

    values = []
                          
    # read wire information from file
    for parameter in wire.parameters_names:
        line = f.readline()
        line = line.split()
        if(line[0] == (parameter + "=")):
            values.append(line[1])
        else:
            print("File: " + file_name + "not correctly formatted")
            return

    wire.identifier = values[0]
    wire.t = float(values[1])
    base  = float(values[2])
    wire_length = float(values[3])
    lead_length = float(values[4])

    wire.leads = []
    for value in values[5:13]:
        wire.leads.append(bool(value))

    step_length = wire.t ** - sqrt(2)
    scaling_factor = step_length ** -1
    wire.no_file = True
    wire.base = int(scaling_factor * base)  # width of wire
    wire.wire_length = int(scaling_factor * wire_length)
    wire.lead_length = int(scaling_factor * lead_length)
                   
    for line in f:
        line2 = line.split()
        wire.energies.append(float(line2[0]))
        wire.transmission.append(float(line2[1]))


def _save_to_file(wire, energy, transmission):
    """Save result of calculation to file.

    Saves the `energy` and `transmission` to the file with name
    `wire.file_name`.
    
    Parameters
    ----------
    wire : :class:`garn.Wire3D` or :class:`garn.Wire2D`
    energy : float
    transmission: float
    
    Notes
    -----
    If wire was initialized with the ´file_name´ parameter
    the function saves to the end of the old file. If the wire
    instance was initialised with the other parameters any old file with
    with the same name will be overwritten with the new data.

    """
                                                 
    if wire.no_file == True: 
        f = open("data-" + wire.identifier, "w")
        for i in range(len(wire.parameters_values)):
            f.write(wire.parameters_names[i] + "= " +
                    str(wire.parameters_values[i]) + "\n")
        wire.no_file = False

    else:
        f = open("data-" + wire.identifier, "a")
        #open with "a" for append
           
    f.write(str(energy) + " " + str(transmission) + "\n")

    f.close()
