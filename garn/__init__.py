"""
Garn is a small Kwant_ based package for doing effective mass
calculations on two models of contact geometry effects on
semiconductor nanowires.

This documentation is of the software and how it is used and will not
cover the physics behind the simulations. A formal introduction to the
project is publiched in `Numerical simulations of contact geometry
effects on transport properties of semiconductor nanowires <http://lup.lub.lu.se/student-papers/record/8878322>`_.

.. _Kwant: http://kwant-project.org/

Using Garn
----------

As any python package when the package is in your python path type

.. code-block:: Python

   import garn

to use it. 

Creating a wire system is done with a call to any of the two wire
classes :class:`~garn.Wire3D` or :class:`~garn.Wire2D`. In this case
:class:`~garn.Wire3D`.

.. code-block:: Python

   wire = garn.Wire2D(base=3, wire_length=30, lead_length=5,
                           identifier="test-2D", step_length=1)


Now you can plot the system with the :meth:`~garn.system_plot`
methodto see if it looks as you expect.

.. code-block:: Python

    garn.system_plot(wire)

In the end it is all about calculation the transmission through the
system. This is done with with the :meth: `~garn.transmission`
function. For example calculating the transmission from the start to
the end of the wire in 10 equidistant points in the intervall 0 to 1 [t]
can done with the command.

.. code-block:: Python

    garn.transmission(wire, start_energy=0, end_energy=1,
                      number_of_points=10)

The transmission data and information about the wire is saved in a
file named after the following principle

.. code-block:: Python

    "data-" + wire.identifier

In this case wire.identifier is set to "test-2D" so the filename will be
"data-test-2D". The resulting list of transmissions and energies can also be
accesed via the attributes wire.energies and wire.transmission.

A instance of the classes :class:`~garn.Wire2D` and :class:`~garn.Wire3D`
can also be made with the "file_name" parameter as only parameter.

.. code-block:: Python

     wire_from_file = garn.Wire2D(file_name="data-test-2D")

"""

import os
import sys
sys.path.insert(0,
                os.path.abspath('/home/emil/dip-work-emil/package/garn'))



from garn.wire_3d import Wire3D


from garn.wire_2D import Wire2D


