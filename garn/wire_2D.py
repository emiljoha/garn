import kwant
from math import sqrt
from matplotlib import pyplot
from geometry import rectangle
from saving import read_file_to_wire


class Wire2D:
    """Wire2D facilitates the modelling of nanowire contact geometries in
    Kwant by actings as a help in constructing a 2D projection of a
    nanowire and attaching customizabel contacts in each end.

    """
    
    
    a = 1
    energies = []
    transmission = []
    sys = kwant.Builder()

    parameters_names = ["identifier", "t", "base", "wire_length",
                        "lead_length", "start_top", "start_right",
                        "start_left", "start_bottom", "end_top",
                        "end_right", "end_left", "end_bottom"]
    
    
    
    def __init__(self, base=3, wire_length=30, lead_length=5,
        identifier="unnamed", file_name="", step_length=1,
        start_right=True, start_left=True, end_right=True,
        end_left=True):
                 
        """A Instance of Wire2D describes the properties of a 2D nanowire

        Wire2D facilitates the modelling of nanowires by 

        .. warning:: If keyword parameter `file_name` is set to
                     anything else than "" all other parameters are
                     ignored. It is only to facilitate the use of
                     parameter `file_name` that `base`, `wire_length`
                     and, `lead_length` parameters are optional.
    
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
        start_right : bool, optional
            Boolian vaules of there should be a lead on the right side at
            the start of the wire (default True)
        start_left : bool, optional
            Boolian vaules of there should be a lead on the left side at
            the start of the wire (default True)
        end_right : bool, optional
            Boolian vaules of there should be a lead on the right side at
            the end of the wire (default True)
        end_left : bool, optional
            Boolian vaules of there should be a lead on the left side at
            the end of the wire (default True)
        file_name : str, optional
            Uses the data-file specified by the str to create a the instance

        """
                 
        if (file_name == ""):
            scaling_factor = step_length ** -1
            self.t = step_length ** -2
            self.no_file = True
            self.identifier = identifier
            self.base = int(scaling_factor * base)  # width of wire
            self.wire_length = int(scaling_factor * wire_length)
            self.lead_length = int(scaling_factor * lead_length)
            self.leads = [False, start_right, start_left,
                          False, False, end_right,
                          end_left, False]

        else:
            read_file_to_wire(self, file_name)
            self.no_file = False


        self.parameters_values = (self.identifier, self.t, self.base,
                             self.wire_length, self.lead_length,
                             self.leads[0], self.leads[1],
                             self.leads[2], self.leads[3],
                             self.leads[4], self.leads[5],
                             self.leads[6], self.leads[7])

        # Set lattice vectors for lattice object
        basis_vectors = ((self.a, 0), (0, self.a))
        self.lattice = kwant.lattice.Monatomic(basis_vectors)
        
        self.make_system()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self.transmission) == len(other.transmission):
                for i in range(len(self.transmission)):
                    if str(self.transmission[i]) != str(other.transmission[i]):
                        return False
                return True
        else:
            return False
                 
                 
    def make_system(self):
        """Fills the Builder object with all sites and hoppings.
                 
        Adds nodes to the graph(onsite hamiltonians) To change the onsite
        hamiltonian change the method onsite.
                 
        Adds hopping between sites. (hopping integral)
                 
        Also finalizes system.
        """
        
        # add nodes in graph
        self.sys[self.lattice.shape(
            self.rectangle_wire, (0, 0))] = self.onsite
                 
        # add hoppings between nodes
        self.sys[self.lattice.neighbors()] = -self.t
                 
        lead_start, lead_end = self.create_leads()

        if self.leads[2]:
            self.sys.attach_lead(lead_start)

        if self.leads[1]: 
            self.sys.attach_lead(lead_start.reversed())

        if self.leads[6]:
            self.sys.attach_lead(lead_end)

        if self.leads[5]:
            self.sys.attach_lead(lead_end.reversed())
                 
        self.sys = self.sys.finalized()
                 
    def rectangle_wire(self, pos):
        """ find out if the position is inside the scattering region"""
        
        x, y = pos
        if (rectangle(pos, self.base, self.wire_length)):
            return True
        else:
            return False         
                         
    def onsite(self, args):
        # + im * kwant.digest.gauss(str(site.pos))
        return 4 * self.t
                 
    def create_leads(self):
        """ Return leads of system ready to be attached"""
        # The lead builder object is created with a symetry object as argument that sets the symmetry of the lead.
        # Lead need to have a symmetry property to function.
        lead_start = kwant.Builder(
            kwant.TranslationalSymmetry((0, self.a)))
        lead_end = kwant.Builder(
            kwant.TranslationalSymmetry((0, self.a)))
                 
        start = int(self.wire_length - self.lead_length)
        for x in range(start, self.wire_length):
            lead_end[self.lattice(x, 0)] = 4 * self.t
        
        for x in range(self.lead_length):
            lead_start[self.lattice(x, 0)] = 4 * self.t
                 
        lead_start[self.lattice.neighbors()] = -self.t
        lead_end[self.lattice.neighbors()] = -self.t
                 
        return lead_start, lead_end
