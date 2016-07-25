import kwant
from math import sqrt
from matplotlib import pyplot

from garn.geometry import rectangle
from garn.system_wide import Wire


class Wire2D(Wire):
    """Wire2D facilitates the modelling of nanowire contact geometries in
    Kwant by actings as a help in constructing a 2D projection of a
    nanowire and attaching customizabel contacts in each end.
    """
    
    
    
    def __init__(self, base=3, wire_length=30, lead_length=5,
        identifier="unnamed", file_name="", step_length=1,
        start_right=True, start_left=True, end_right=True,
        end_left=True):
                 
        """A Instance of Wire2D describes the properties of a 2D nanowire

        Wire2D facilitates the modelling of nanowires with a numerical
        effective mass method using Kwant by serving as a the nanowire
        object.

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
        Wire.__init__(self, base=base, wire_length=wire_length,
                      lead_length=lead_length, identifier=identifier,
                      file_name=file_name, step_length=step_length,
                      start_top=False, start_right=start_right,
                      start_left=start_left,
                      start_bottom=False, end_top=False,
                      end_right=end_right, end_left=end_left,
                      end_bottom=False)

        # Set lattice vectors for lattice object
        basis_vectors = ((self.a, 0), (0, self.a))
        self.lattice = kwant.lattice.Monatomic(basis_vectors)
        
        self._make_
        
    def _attach_leads(self, lead_start, lead_end):
        """Attaches leads to system according to the self.leads list
        
        Parameters
        ----------
        lead_top : `Builder <http://kwant-project.org/doc/1.0/reference/generated/kwant.builder.Builder#kwant.builder.Builder>`_ with 1D translational symmetry in y-direction
            Builder of the lead which is to be attached in the beginning.
        lead_side : `Builder <http://kwant-project.org/doc/1.0/reference/generated/kwant.builder.Builder#kwant.builder.Builder>`_ with 1D translational symmetry in y-direction
            Builder of the lead which is to be attached in the end.

        """
        
        if self.leads[2]:
            self.sys.attach_lead(lead_start)

        if self.leads[1]: 
            self.sys.attach_lead(lead_start.reversed())

        if self.leads[6]:
            self.sys.attach_lead(lead_end)

        if self.leads[5]:
            self.sys.attach_lead(lead_end.reversed())
        
                 
                 
    def _make_system(self):
        """Construct the wire.sys (kwant.Builder) attribute. 

        This is were the sites in the scattering region are added to
        the kwant.Builder object and functions to create leads and
        attach them are called. Welcome to the heart of
        :class:`garn.Wire3D`.
        
        """
        
        # Fill a rectange with sites
        self.sys[self.lattice.shape(
            self._rectangle_wire, (0, 0))] = self._onsite
                 
        # Set hoppings between those sites.
        self.sys[self.lattice.neighbors()] = -self.t

        lead_start, lead_end = self._create_leads()

        self._attach_leads(lead_start, lead_end)

        self.sys = self.sys.finalized()
                 
    def _rectangle_wire(self, pos):
        """ find out if the position is inside the scattering region"""
        
        x, y = pos
        if (rectangle(pos, self.base, self.wire_length)):
            return True
        else:
            return False         
                         
    def _onsite(self, args):
        """ Retrive onsite value of sites"""
        return 4 * self.t
                 
    def _create_leads(self):
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
