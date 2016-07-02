import kwant

import saving

def system_plot(wire):
    """Illustrative plot of wire sites and hoppings.

    Basic plot of all the sites and hopping is the
    system. Semi-infinite contacts are plotted in read.

    Parameters
    ----------
    wire : :class:`~garn.Wire2D` or :class:`~garn.Wire3D`
         System to be plotted.

    Notes
    -----
    For more advanced settings pass wire.sys to the `kwant.plotter.plot
    <http://kwant-project.org/doc/1/reference/generated/kwant.plotter.plot#kwant.plotter.plot>`_.
    method.
    
    """

    kwant.plot(wire.sys)  # site_size=0.18, site_lw=0.01, hop_lw=0.01)



def range_float(start, stop, step=1):
    x = start
    res = []
    while True:
        if x < stop:
            res.append(x)
            x += step
        else:
            return res


def in_out_nums(leads):
    if len(leads) != 8:
        print("error in system_wide.in_out_leads")
        return
    
    start = [leads[0], leads[1], leads[2], leads[3]]
    end = [leads[4], leads[5], leads[6], leads[7]]

    in_leads = []
    i = 0
    for lead in start:
        if lead:
            in_leads.append(i)
            i = i + 1

    out_leads = []
    for lead in end:
        if lead:
            out_leads.append(i)
            i = i + 1
    return tuple(in_leads), tuple(out_leads)

#:math: `t = \frac{\hbar^2}{2 m_e^* wire.step_length}`.
    
def transmission(wire, start_energy, end_energy, number_of_points=500,
                 print_to_commandline=True):
    """Calculate transmission through system.

    Calculates the transmission in `number_of_points` equidistant points
    on the intervall [`start_energy`, `end_energy`).

    
    Parameters
    ----------
    wire : :class:`~garn.Wire2D` or :class:`~garn.Wire3D`
        The wire model for with the transmission is calculated and
        energy and transmission attributes are changed.
    start_energy : float
    end_energy : float, optional
    number_of_points : int, optional
    print_to_commandline : bool
        If true the resulting transmission energy pairs are printed
        in the terminal. (Default Ture beacuse good for monitoring progress)

    Notes
    -----
    The energy is given in units of :math:`t`. 

    .. math::

        t = \dfrac{\hbar^2}{2 m_e^* step\_length^2}

    :math:`m_e^*` is the effective mass of the semiconduction and step_length
    is the discretization step that is set on initialization of
    :class:`~garn.Wire2D` and :class:`~garn.Wire3D` instanses.

    The transmission is given in units of :math:`\dfrac{e^2}{\hbar}`. 

    The function changes the attributes energy and transmission of
    *wire* and saves to the file "data-" + `wire.identifier`. 

    """

    # handel case when the wire has calculated before
    if wire.energies != []:
        if (not energy_exist_dialog()):
            return

    intervall_length = end_energy - start_energy
    stepsize = intervall_length / float(number_of_points)
    start_step = int(start_energy / float(stepsize))
    end_step = int(end_energy / float(stepsize))

    wire.energies = [stepsize * i for i in range(start_step, end_step)]
    wire.transmission = []
        
    in_leads, out_leads = in_out_nums(wire.leads)

    if print_to_commandline:
        print("Transmission calculated for energies [t]: ")
        
    for en in wire.energies:
        smatrix = kwant.smatrix(wire.sys, en, in_leads=in_leads,
                                    out_leads=out_leads) 
        con_tot = 0
        for i in range(0,len(in_leads)):
            for j in range(len(in_leads), len(in_leads) +
                           len(out_leads)):
                con = smatrix.transmission(j, i)
                con_tot = con_tot + con
                #print(str(i) + "-" + str(j) + "= " + str(con)) 
        wire.transmission.append(con_tot)
        saving.save_to_file(wire, en, con_tot)

        if print_to_commandline:
            print(str(en) + " " + str(con_tot))


def energy_exist_dialog():
    """returns True if user whant to continiue and delete old energies
    else False
    """
    print("ERROR: Wire already have saved energies, do you want to delete old energies and continiue? y / n: ")
    ans = raw_input()
    if ("y" == ans):
        print("Call of method Transmission continiued")
        return True
    else:
        print("Call of method Transmission aborted")
        return False

 
def transmission_energy_plot(wire, title="", save=False, file_type=".eps"):
    """ Plot of energy on x - axis against transmission on y - axis
     REQUIRED ATTRIBUTES:
        energies, transmission and identifier
    """
    print(wire.energies)
    print(wire.transmission)
    pyplot.plot(wire.energies, wire.transmission)
    pyplot.ylabel("Transmission [$e * e / h$]")

    pyplot.xlabel("Energy[$hbar squared / 2 m a*a$]")
    pyplot.title(title)
    if save:
        pyplot.savefig("figure-" + wire.identifier + file_type)
    pyplot.show()
