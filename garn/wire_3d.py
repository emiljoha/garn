import kwant
from math import sqrt
from matplotlib import pyplot
import numpy as np

from garn.geometry import hexagon, extension
import garn.system_wide
import garn.saving


class Wire3D:
    """Wire3D facilitates the modelling of nanowire contact geometries in
    Kwant by actings as a help in constructing a hexagonal nanowire
    and attaching customizabel contacts in each end.

    """
    
    a = 1
    energies = []
    transmission = []

    parameters_names = ["identifier", "t", "base", "wire_length",
                        "lead_length", "start_top", "start_right",
                        "start_left", "start_bottom", "end_top",
                        "end_right", "end_left", "end_bottom"]

    
    def __init__(self, base=3, wire_length=30, lead_length=5,
                 identifier="unnamed", file_name="", step_length=1,
                 start_top=True, start_right=True, start_left=True,
                 start_bottom=False, end_top=True, end_right=True,
                 end_left=True, end_bottom=False):

        """A Instance of Wire3D describes the properties of a 3D nanowire
 

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
        file_name : str, optional
            Uses the data-file specified by the str to create a the
            instance.

        """

        if (file_name == ""):
            scaling_factor = step_length ** -1
            self.t = step_length ** -2
            self.no_file = True
            self.identifier = identifier
            self.base = int(scaling_factor * base)  # side of hexagon
            self.wire_length = int(scaling_factor * wire_length)
            self.lead_length = int(scaling_factor * lead_length)
        else:
            garn.saving._read_file_to_wire(self, file_name)
            self.no_file = False

        self.leads = [start_top, start_right, start_left,
                      start_bottom, end_top, end_right, end_left,
                      end_bottom]

        self.parameters_values = (self.identifier, self.t, self.base,
                             self.wire_length, self.lead_length,
                             self.leads[0], self.leads[1],
                             self.leads[2], self.leads[3],
                             self.leads[4], self.leads[5],
                             self.leads[6], self.leads[7])
    

        
        self.lattice = self._lattice()
        self._make_system()

    def __eq__(self, other):
        """ Defentition of equality used in testing

        Compares transmission attributes element wise

        """
        if isinstance(other, self.__class__):
            if len(self.transmission) == len(other.transmission):
                for i in range(len(self.transmission)):
                    if str(self.transmission[i]) != str(other.transmission[i]):
                        return False
                return True
        else:
            return False

#---------------------------------------------------------------------
# Internal functions
#---------------------------------------------------------------------
    def _attach_leads(self, lead_start_top, lead_start_side, lead_end_top,
                     lead_end_side):
        """Attaches leads to system according to the self.leads list

        Parameters
        ----------
        lead_start_top : Builder_ with 1D translational symmetry in z-direction
            Builder of the lead which is to be attached on the top of
            the beginning.
        lead_start_side : Builder_ with 1D translational symmetry in x-direction
            Builder of the lead which is to be attached on the side of
            the beginning.
        lead_end_top : Builder_ with 1D translational symmetry in z-direction
            Builder of the lead which is to be attached on the top of
            the end.
        lead_end_side : Builder_ with 1D translational symmetry in x-direction
            Builder of the lead which is to be attached on the side of
            the end.

        .. _Builder:: http://kwant-project.org/doc/1.0/reference/generated/kwant.builder.Builder#kwant.builder.Builder

        """
        
        if self.leads[0]:
            self.sys.attach_lead(lead_start_top)
            
        if self.leads[1]:
            self.sys.attach_lead(lead_start_side)

        if self.leads[2]:
            self.sys.attach_lead(lead_start_side.reversed())
      
        if self.leads[3]:
            self.sys.attach_lead(lead_start_top.reversed())

        if self.leads[4]:
            self.sys.attach_lead(lead_end_top)
            
        if self.leads[5]:
            self.sys.attach_lead(lead_end_side)

        if self.leads[6]:
            self.sys.attach_lead(lead_end_side.reversed())
      
        if self.leads[7]:
            self.sys.attach_lead(lead_end_top.reversed())

    def _make_system(self):
        """Fills the Builder object with sites and hoppings.

        This is were the sites in the scattering region are added to
        the kwant.Builder object and functions to create leads and
        attach them are called. Welcome to the heart of
        :class:`garn.Wire3D`.
        
        """

        self.sys = kwant.Builder()

        #add sites in scattering region
        self.sys[self.lattice.shape(
            self._hexagon_wire, (0, 0, 0))] = self._onsite

        
        self.sys[self.lattice.neighbors()] = - self.t
        
        lead_start_top, lead_end_top = self._create_leads((0, 0, self.a))
        lead_start_side, lead_end_side = self._create_leads((self.a, 0, 0))

        self._attach_leads(lead_start_top, lead_start_side,
                          lead_end_top, lead_end_side)

        self.sys = self.sys.finalized()


    def _hexagon_wire(self, pos):
        """ Find out if the position is inside a hexagonal wire."""
        x, y, z = pos
        if (hexagon((x, z), self.base) & (y >= 0) & (y < self.wire_length)):
            return True
        else:
            return False


    def _positions_of_leads(self):
        """Calculate positions from where to start fill leads

        Returns
        -------
        start_top_site: tuple of 3 floats
            Top left corner of rectange enclosing the hexagon of the
            beggining of the wire.
        end_top_site: tuple of 3 floats
            Top left corner of rectange enclosing the hexagon of the
            wire at a the begging of the lead at the end of the wire.

        Notes
        -----
        Explaining these positions are messy so here is
        some math instead.

        .. math::

            start_top_site = (-\dfrac{base}{2}, 0, \dfrac{\sqrt{3}base}{2}) \

            start_end_site = (-\dfrac{base}\2}, wire_length - lead_length, \dfrac{\sqrt{3}base}{2})

        """
        xs, ys, zs = self.lattice.closest(( - self.base / 2.0, 0,
                                            sqrt(3) / 2.0 *
                                            self.base))

        xe, ye, ze = self.lattice.closest( (- self.base / 2.0,
                                            self.wire_length -
                                            self.lead_length, sqrt(3)
                                            / 2.0 * self.base))

        start_top_site = (xs, ys, zs)
        end_top_site = (xe, ye, ze)

        return start_top_site, end_top_site

    def _lattice(self):
        # Set lattice vectors for lattice object
        basis_vectors = ((self.a, 0, 0), (0, self.a, 0), (0, 0, self.a))

        # return the lattice object
        return kwant.lattice.Monatomic(basis_vectors)

    def _onsite(self, args):
        # + im * kwant.digest.gauss(str(site.pos))
        return 6 * self.t

        
    def _fill_lead(self, lead, position, side=False):
        x, y, z = position
                
        start_x  = -self.base + 1
        if not side:
            lead[[self.lattice(i, j, 0) for i in range(-self.base+1,
                                                       self.base) for j in range(y, y +
                                                                                 self.lead_length)]] = 6 * self.t
            return lead

        if side:
            lead[[self.lattice(0, j, k) for j in
                  range(y, y + self.lead_length) for k in
                  range(int(-self.base * sqrt(3) / 2.0),
                        int(self.base * sqrt(3) / 2.0)+1)]] = 6 * self.t
            return lead
            


    def _create_leads(self, sym):
        """ Return lead at the start and end of wire with symetry sym"""
        
        if (sym == (self.a, 0, 0)):
            side = True
        else:
            side = False

        lead_start = kwant.Builder(
            kwant.TranslationalSymmetry(sym))
        lead_end = kwant.Builder(
            kwant.TranslationalSymmetry(sym))

        pos_start, pos_end = self._positions_of_leads()
        lead_end = self._fill_lead(lead_end, pos_end, side)
        lead_start = self._fill_lead(lead_start, pos_start, side)

        lead_end[self.lattice.neighbors()] = -self.t
        lead_start[self.lattice.neighbors()] = -self.t

        return lead_start, lead_end
