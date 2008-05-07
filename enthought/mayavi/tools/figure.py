"""
Functions related to creating the engine or the figures.

"""

# Author: Gael Varoquaux <gael.varoquaux@normalesup.org>
# Copyright (c) 2007, Enthought, Inc.
# License: BSD Style.

# Standard library imports.
import numpy
from types import IntType

# Enthought library imports.
from enthought.tvtk.api import tvtk

# Mayavi imports
from camera import view
from config import get_engine
from enthought.mayavi.preferences.api import preference_manager


options = preference_manager.mlab

######################################################################

def figure(name=None, background=None, foreground=None):
    """ Creates a new scene or retrieves an existing scene. If the mayavi
    engine is not running this also starts it.

    Parameters:
    -----------

    name -- A string specifying the name of the scene.

    background -- A 3-tuple of floats in the range [0,1] specifying the
    background color to use on the scene.

    foreground -- A 3-tuple of floats in the range [0,1] specifying the
    foreground color to use on the scene.

    """
    engine = get_engine()
    if type(name) == IntType:
        name = 'TVTK Scene %d' % name
    if name is not None:
        for scene in engine.scenes:
            if scene.name == name:
                engine.current_scene = scene
                break
        else:
            engine.new_scene()
            engine.current_scene.name = name
    else:
        engine.new_scene()
    view(40, 50)
    fig = engine.current_scene
    if background is None:
        background = options.background_color
    if foreground is None:
        foreground = options.foreground_color

    fig.scene.background = background
    fig.scene.foreground = foreground
    return fig

def gcf():
    """Return a handle to the current figure.
    """
    engine = get_engine()
    scene = engine.current_scene
    if scene is None:
        return figure()
    return scene

def clf():
    """Clear the current figure.
    """
    try:
        scene = gcf()
        scene.scene.disable_render = True
        scene.children[:] = []
        scene.scene.disable_render = False
    except AttributeError:
        pass

def draw():
    """ Forces a redraw of the current figure.
    """
    gcf().render()

def savefig(filename, size=None, **kwargs):
    """ Save the current scene.
        The output format are deduced by the extension to filename.
        Possibilities are png, jpg, bmp, tiff, ps, eps, pdf, rib (renderman),
        oogl (geomview), iv (OpenInventor), vrml, obj (wavefront)

        If an additional size (2-tuple) argument is passed the window
        is resized to the specified size in order to produce a
        suitably sized output image.  Please note that when the window
        is resized, the window may be obscured by other widgets and
        the camera zoom is not reset which is likely to produce an
        image that does not reflect what is seen on screen.

        Any extra keyword arguments are passed along to the respective
        image format's save method.
    """
    gcf().scene.save(filename, size=size, **kwargs)
