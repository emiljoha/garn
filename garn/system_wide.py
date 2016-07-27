import kwant
import garn
from numpy import sqrt

class Wire(object):
    
    a = 1
    energies = []
    transmission_data = []
    sys = kwant.Builder()

    parameters_names = ["identifier", "t", "base", "wire_length",
                        "lead_length", "start_top", "start_right",
                        "start_left", "start_bottom", "end_top",
                        "end_right", "end_left", "end_bottom"]

    def __init__(self, base=3, wire_length=30, lead_length=5,
                     identifier="unnamed", file_name="", step_length=1,
                     start_top=True, start_right=True, start_left=True,
                     start_bottom=False, end_top=True, end_right=True,
                     end_left=True, end_bottom=False ):
                 
        """A class inherrited by :class:`~garn.Wire2D` and
        :class:`~garn.Wire3D.
    
        Parameters
        ----------
        base : int or float, optional
            Width of wire.
        wire_length : int or float, optional
            Length of complete wire including leads.
        lead_length : int or float, optional
            Length of lead-wire interface in direction of the                      

        Other Parameters
        ----------------
        indentifier : str, optional
            Identifies the wire represented in plots and data files produced by garn.
        step_length : int or float, optional
            Discretization step.
        start_top : bool, optional
            Boolian vaules of there should be a lead on the top at
            the start of the wire
        start_right : bool, optional
            Boolian vaules of there should be a lead on the right side at
            the start of the wire.
        start_left : bool, optional
            Boolian vaules of there should be a lead on the left side at
            the start of the wire.
        start_bottom : bool, optional
            Boolian vaules of there should be a lead on the bottom at
            the start of the wire
        end_top : bool, optional
            Boolian vaules of there should be a lead on the top at
            the end of the wire.
        end_right : bool, optional
            Boolian vaules of there should be a lead on the right side at
            the end of the wire.
        end_left : bool, optional
            Boolian vaules of there should be a lead on the left side at
            the end of the wire.
        end_bottom : bool, optional
            Boolian vaules of there should be a lead on the bottom at
            the end of the wire.
        """
                 
        if (file_name == ""):
            scaling_factor = step_length ** -1
            self.t = step_length ** -2
            self.no_file = True
            self.identifier = identifier
            self.base = int(scaling_factor * base)  # width of wire
            self.wire_length = int(scaling_factor * wire_length)
            self.lead_length = int(scaling_factor * lead_length)
            self.leads = [start_top, start_right, start_left,
                          start_bottom, end_top, end_right, end_left,
                          end_bottom]

        else:
            self._read_file_to_wire(file_name)
            self.no_file = False


        self.parameters_values = (self.identifier, self.t, self.base,
                             self.wire_length, self.lead_length,
                             self.leads[0], self.leads[1],
                             self.leads[2], self.leads[3],
                             self.leads[4], self.leads[5],
                             self.leads[6], self.leads[7])

    
    def system_plot(self):
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

        kwant.plot(self.sys)  # site_size=0.18, site_lw=0.01, hop_lw=0.01)



    def _in_out_nums(self):
        """Transform attributeleads to input for kwant.smatrix.transmission

        Translate attribute leads from wire classes :class:`~garn.Wire2D`
        and :class:`~garn.Wire3D` to the keyword argument `in_leads` and
        `out_leads` of the `kwant.smatrix.transmission
        <http://kwant-project.org/doc/1/reference/generated/kwant.solvers.default.smatrix#kwant.solvers.default.smatrix>`_
        method.

        Parameters
        ----------
        leads : list of bool (length 8)
            A list of True of False value that specify if leads are present.
            order is [`start_top`, `start_right`, `start_left`, `start_bottom`,
            `end_top`, `end_right`, `end_left`, `end_bottom`]

        Returns
        -------
        (in_leads, out_leads) : touple of touples
            keyword argument `in_leads` and
            `out_leads` of the `kwant.smatrix.transmission
            <http://kwant-project.org/doc/1/reference/generated/kwant.solvers.default.smatrix#kwant.solvers.default.smatrix>`_
            method.
        
        """
        
        start = [self.leads[0], self.leads[1], self.leads[2],
                 self.leads[3]]
        end = [self.leads[4], self.leads[5], self.leads[6],
               self.leads[7]]

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


        
    def transmission(self, start_energy, end_energy, number_of_points=500,
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
        *wire* and saves to the file "data-" + `wire.identifier`. If the
        transmission function have been called before or the wire.energies
        attribute is non-empty the
        :meth:`~garn.system_wide._energy_exist_dialog` is called asking
        what to do.

        
        """

        # handel case when the wire has calculated before
        if self.energies != []:
            if (not _energy_exist_dialog()):
                return

        intervall_length = end_energy - start_energy
        stepsize = intervall_length / float(number_of_points)
        start_step = int(start_energy / float(stepsize))
        end_step = int(end_energy / float(stepsize))

        self.energies = [stepsize * i for i in range(start_step, end_step)]
        self.transmission_data = []
            
        in_leads, out_leads = self._in_out_nums()

        if print_to_commandline:
            print("Transmission_Data calculated for energies [t]: ")
            
        for en in self.energies:
            smatrix = kwant.smatrix(self.sys, en, in_leads=in_leads,
                                        out_leads=out_leads) 
            con_tot = 0
            for i in range(0,len(in_leads)):
                for j in range(len(in_leads), len(in_leads) +
                               len(out_leads)):
                    con = smatrix.transmission(j, i)
                    con_tot = con_tot + con
                    #print(str(i) + "-" + str(j) + "= " + str(con)) 
            self.transmission_data.append(con_tot)
            self._save_to_file(en, con_tot)

            if print_to_commandline:
                print(str(en) + " " + str(con_tot))


    def __eq__(self, other):
        """ Defentition of equality used in testing

        Compares transmission_data attributes element wise
        """
        if self.transmission_data == other.transmission_data:
            if self.base == other.base:
                if self.wire_length == other.wire_length:
                    if self.lead_length == other.lead_length:
                        if self.step_length == other.step_length:
                            return True

        return False
        
    def _energy_exist_dialog():
        """User desides if to overwrite earlier transmission data

        Ask user via terminal prompt if to delete old tranmsiosson and
        energies or aborth.

        Return
        ------
        Bool
            :code:`True` means user whant to continiue and overwrite old
            data. :code:`False` means user want to abort transmission
            function call.

        """
        print("ERROR: Wire already have saved energies, do you want to delete old energies and continiue? y / n: ")
        ans = raw_input()
        if ("y" == ans):
            print("Call of method Transmission continiued")
            return True
        else:
            print("Call of method Transmission aborted")
            return False

     
    def transmission_energy_plot(self, title="", save=False,
                                 file_type="png"):
        """Plot of energy on x - axis against transmission on y - axis

        Plots self.energies against self.transmission with some
        options.

        Parameters
        ----------
        title : str
           Title of the plot.
        save : bool
           Save the plot with name "figure-" + `self.identifier` + `file_type`
        file_type : str
            Choose file format to save the plot in

        """
        print(self.energies)
        print(self.transmission_data)
        pyplot.plot(self.energies, self.transmission_data)
        pyplot.ylabel("Transmission [$e * e / h$]")

        pyplot.xlabel("Energy[$hbar squared / 2 m a*a$]")
        pyplot.title(title)
        if save:
            pyplot.savefig("figure-" + self.identifier, format=file_type)
        pyplot.show()


    def _read_file_to_wire(self, file_name):
        """ Initialize variables for wire instance from data file.
        
        Internal function that gives the ´wire´ the same properties as the
        wire used to produce the file ´file_name´

        .. warning::
            This method will write over all prior attributes of `wire` with
            those specified in the `file_name` file. 
                     

        Parameters
        ----------
        file_name : str
        
        """
        
        f = open(file_name)

        
        # read wire information from file to list
        values = []                              
        for parameter in self.parameters_names:
            line = f.readline()
            line = line.split()
            if(line[0] == (parameter + "=")):
                values.append(line[1])
            else:
                print("File: " + file_name + "not correctly formatted")
                return

        self.identifier = values[0]
        self.t = float(values[1])
        # Not yet adjusted for steplength
        base  = float(values[2]) 
        wire_length = float(values[3])
        lead_length = float(values[4])

        self.leads = []
        for value in values[5:13]:
            self.leads.append(bool(value))

        # adjust spacial characteristics to the step_length
        step_length = self.t ** - sqrt(2)
        scaling_factor = step_length ** -1
        self.no_file = True # Not really shure about this parameter.
        self.base = int(scaling_factor * base)  # width of wire
        self.wire_length = int(scaling_factor * wire_length)
        self.lead_length = int(scaling_factor * lead_length)
                       
        for line in f:
            line2 = line.split()
            self.energies.append(float(line2[0]))
            self.transmission_data.append(float(line2[1]))


    def _save_to_file(self, energy, transmission):
        """Save result of calculation to file.

        Saves the `energy` and `transmission` to the file with name
        `self.file_name`.
        
        Parameters
        ----------
        energy : float
        transmission: float
        
        Notes
        -----
        If wire was initialized with the ´file_name´ parameter
        the function saves to the end of the old file. If the wire
        instance was initialised with the other parameters any old file with
        with the same name will be overwritten with the new data.

        """
                                                     
        if self.no_file == True: 
            f = open("data-" + self.identifier, "w")
            for i in range(len(self.parameters_values)):
                f.write(self.parameters_names[i] + "= " +
                        str(self.parameters_values[i]) + "\n")
            self.no_file = False

        else:
            f = open("data-" + self.identifier, "a")
            #open with "a" for append
               
        f.write(str(energy) + " " + str(transmission) + "\n")

        f.close()
