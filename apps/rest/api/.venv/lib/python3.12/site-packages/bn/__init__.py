"""\
BareNeccessities contains functions and classes I use so frequently I wish 
they were in the standard library (in fact one of them is as of Python 2.6!).

These all work with Python 2.4 and above and may work with earlier versions 
too.
"""

import imp
import logging
import os
import sys

try:
    from collections import OrderedDict
except:
    from bn.ordereddict import OrderedDict

log = logging.getLogger(__name__)

class MarbleLike(object):
    def __init__(
        self, 
        bag, 
        name, 
        aliases=None, 
    ):
        self.__dict__['bag'] = bag
        self.__dict__['name'] = name
        self.__dict__['aliases'] = aliases

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        if not self.__dict__.has_key('aliases'):
            raise AttributeError('Attempted to access the %r attribute, but the class is not initialised yet so no aliases are present'%name)
        if name in self.aliases:
            if not name in self.__dict__:
                alias = self.aliases[name]
                if not self.bag.has_key(alias):
                    self.bag.enter(alias)
                return self.bag[alias]
        log.debug(
            'Couldn\'t find the pipe %r in %r with aliases %r', 
            name, 
            self.__class__.__name__,
            self.aliases,
        )
        raise AttributeError('No such attribute %r'%name)

#
# AttributeDict
#

def day_of_month_in_english(day):
    day = int(str(day).lstrip('0'))
    if day in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30]:
        return '%sth'%day
    elif day in [1,21,31]:
        return '%sst'%day
    elif day in [2,22]:
        return '%snd'%day
    elif day in [3,23]:
        return '%srd'%day
    else: 
        raise Exception('Unknown day %r'%day)

class AttributeDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError('No such attribute %r'%name)

    def __setattr__(self, name, value):
        raise AttributeError(
            'You cannot set attributes of this object directly'
        )

class NestedAttributeDict(AttributeDict):
    """\
    Like an ``AttributeDict`` but also allows setting and getting
    of keys containing ``.`` characters.
    """
    def __getitem__(self, name):
        start = self
        for part in name.split('.'):
            start = dict.__getitem__(start, part)
        return start

    def __setitem__(self, name, value):
        """\
        Updates a nested ``AttributeDict()`` based on ``name``. eg this:
    
        ::
    
            service['boot.cmd'] = some_object
    
        Would result in an ``some_object`` being accessible as 
        ``service.boot.cmd`` as long as ``service.boot`` already existed.
        """
        start = self
        parts = name.split('.')
        used = []
        for part in parts[:-1]:
            if not start.has_key(part):
                if not used:
                    raise KeyError(
                        'Cannot set key %r because AttributeDict has no '
                        'key %r'%(
                            name,
                            part,
                        )
                    )
                raise KeyError(
                    'AttributeDict %r has no such key %r'%(
                        '.'.join(used), 
                        part
                    )
                )
            else:
                used.append(part)
                start = start[part]
        dict.__setitem__(start, parts[-1], value)


#
# Path Functions
#

# relpath path import (available in Python 2.6 and above)
try:
    import posixpath
    relpath = posixpath.relpath
except (NameError, AttributeError):
    from posixpath import curdir, sep, pardir, join
    def relpath(path, start=curdir):
        """Return a relative version of a path"""
        if not path:
            raise ValueError("no path specified")
        start_list = posixpath.abspath(start).split(sep)
        path_list = posixpath.abspath(path).split(sep)
        # Work out how much of the filepath is shared by start and path.
        i = len(posixpath.commonprefix([start_list, path_list]))
        rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return curdir
        return join(*rel_list)
except (ImportError):
    # We are in the wrong platform
    def relpath(path, start=curdir):
        raise NotImplementedError(
            'The relpath() function is only implemented on posix platforms'
        )

def walk(top, topdown=True, onerror=None, followlinks=False):

    from os.path import join, isdir, islink
    from os import error, listdir

    # We may not have read permission for top, in which case we can't
    # get a list of the files the directory contains.  os.path.walk
    # always suppressed the exception then, rather than blow up for a
    # minor reason when (say) a thousand readable directories are still
    # left to visit.  That logic is copied here.
    try:
        # Note that listdir and error are globals in this module due
        # to earlier import-*.
        names = listdir(top)
    except error, err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = join(top, name)
        if followlinks or not islink(path):
            for x in walk(path, topdown, onerror, followlinks):
                yield x
    if not topdown:
        yield top, dirs, nondirs


def uniform_path(path):
    return os.path.abspath(os.path.normcase(os.path.normpath(path)).replace('\\', '/'))

#
# Import functions
#

class RelativeImportError(Exception):
    pass

def relimport(module_path, current_module_filename, path_to_package, from_=None):
    log.debug(
        "Requesting module path: %r, "
        "current file: %r, path to package root: %r",
        module_path,
        current_module_filename,
        path_to_package
    )
    if not module_path.startswith('.'):
        raise ValueError('The module path %r is not a relative path'%module_path)
    if not path_to_package.startswith('.'):
        raise ValueError('The path to package %r is not a relative path from the importing file'%path_to_package)
    if '/' in module_path:
        raise ValueError("Shouldn't have a / character in the module path")
    if '\\' in module_path:
        raise ValueError("Shouldn't have a \ character in the module path")

    # Find the module path of the module to import
    up, new_rel_mod_path =  how_many_levels_up(module_path)
    if up == 1 and new_rel_mod_path == '':
        path_to_package = path_to_package.strip('/')[:-2]
    package_directory = dir_containing_package_root(path_to_package, current_module_filename)
    up, current_abs_module_path = module_path_of_current_module(current_module_filename, package_directory, up)
    new_abs_mod_path = abs_mod_path(current_abs_module_path, up, new_rel_mod_path)
    module_to_import, directory_containing_module = adjust_path_for_imp(new_abs_mod_path, package_directory)

    __import__(new_abs_mod_path, {}, {})
    mod = sys.modules[new_abs_mod_path]
    return handle_from_clause(mod, from_)
    ##try:
    ##    __import__(new_abs_mod_path, {}, {})
    ##except ImportError:
    ##    try:
    ##        fp, pathname, description = imp.find_module(new_abs_mod_path)
    ##    except ImportError:
    ##        log.error('No such module %r import relative to %r (%r)'%(module_path, current_module_filename, new_abs_mod_path))
    ##        raise RelativeImportError('No such module %r import relative to %r (%r)'%(module_path, current_module_filename, new_abs_mod_path))
    ##    else:
    ##        raise
    ##else:
    ##    mod = sys.modules[new_abs_mod_path]
    ##    return handle_from_clause(mod, from_)

def handle_from_clause(module, from_):
    """\
    Takes care of parsing the ``from_`` string and finding the objects in
    ``module``. If one object is imported it is returned, otherwise a tuple of the
    requested objects is returned.
    """
    if from_ is None:
        return module
    results = []
    for name in from_.split(','):
        n = name.strip()
        if not hasattr(module, n):
            raise ImportError('Cannot import name %s'%n)
        results.append(getattr(module, n))
    if len(results) == 1:
        return results[0]
    return tuple(results)

def how_many_levels_up(module_path):
    """\
    Calculates how many directories up the relative import starts and returns:

    * the number of directories up as an integer
    * the module path from the directory where the import starts
    """
    up = 0
    rel_module_path = module_path
    while rel_module_path.startswith('.'):
        up += 1
        rel_module_path = rel_module_path[1:]
    log.debug("Want to import %r, %r up from current module", rel_module_path, up)
    return up, rel_module_path

def dir_containing_package_root(path_to_package, current_module_filename):
    """\
    Returns the directory path containing the package's top ``__init__.py``
    file based on the value provided for the path to the package and the path and
    filename of the module the import is occurring from.
    """
    package_directory = uniform_path(os.path.join(current_module_filename, path_to_package, '../../'))
    log.debug("Package directory: %r", package_directory)
    return package_directory

def module_path_of_current_module(current_module_filename, package_directory, up):
    """\
    Calculate the absoulte module path of the current module and adjust the
    value of the ``up`` variable if the module filename ends with ``__init__.py``
    as the module path should be one lower than other files in the same directory.
    """
    new_up = up
    current_module_path = uniform_path(current_module_filename)[len(package_directory)+1:]
    # Ignore the extension
    current_module_path = '.'.join(current_module_path.split('.')[:-1])
    if current_module_path.endswith('/__init__'):
        current_module_path = current_module_path[:-9]
        new_up -= 1
    current_module_path = current_module_path.replace('/', '.')
    log.debug("Module path of current module: %r", current_module_path)
    return new_up, current_module_path

def abs_mod_path(current_abs_module_path, up, new_rel_mod_path):
    """\
    Calculate the absolute module path of the new import from the absolute module
    path of the current module the number of steps up to where the relatvie path
    begins and the relative module import path from that directory.
    """
    # Get the full module path
    full_mod_path = current_abs_module_path
    if up:
        parts = full_mod_path.split('.')
        parts = parts[:-up]
        full_mod_path = '.'.join(parts)
    if full_mod_path:
        full_mod_path = full_mod_path + '.' + new_rel_mod_path
    else:
        full_mod_path = new_rel_mod_path
    if full_mod_path.endswith('.'):
        full_mod_path = full_mod_path[:-1]
    log.debug("New abs module path: %r", full_mod_path)
    return full_mod_path

def adjust_path_for_imp(new_abs_mod_path, package_directory):
    """\
    Adjust the path so that imp doesn't need to deal with sub-modules
    """
    end_mod_path = new_abs_mod_path
    directory = package_directory
    parts = end_mod_path.split('.')
    for part in parts[:-1]:
        directory += '/'+part
    end_mod_path = parts[-1]
    log.debug("Importing %r from %r", end_mod_path, directory)
    return end_mod_path, directory

def absimport(mod_path, from_=None):
    """\
    Perform an absolute import of ``mod_path`` and return the last module
    """
    if from_ == '':
        raise Exception("The from_ argument cannot be ''")
    mod = __import__(mod_path)
    parts = mod_path.split('.')
    so_far = parts[0]
    for part in parts[1:]:
        so_far+='.'+part
        if not hasattr(mod, part):
            raise ImportError('No such module or object %r'%(so_far,))
        mod = getattr(mod, part)
    return handle_from_clause(mod, from_)

#
# String keys
#

def str_dict(dictionary):
    new_dict = {}
    for k, v in dictionary.items():
        if not isinstance(k, unicode):
            raise TypeError('Expected the key %r to be a Unicode string'*k)
        new_dict[str(k)] = v
    return new_dict

#
# HTMLFragment
#

class HTMLFragment(object):
    """\
    Build up a correctly-escaped HTML string.

    ::

        >>> fragment=HTMLFragment()
        >>> fragment.safe(u'<p>')
        >>> fragment.write(u'Hello, my name is <b>James</b>.')
        >>> fragment.safe(u'</p>')
        >>> print fragment.output
        <p>Hello, my name is &lt;b&gt;James &lt;/b&gt;.

    Notice that the unsafe characters passed to ``write()`` were escaped 
    whereas those passed to ``safe()`` were not.

    The idea is that you can use ``HTMLFragment`` to very efficiently generate
    fragements of code to be inserted into templates and in doing so avoid
    a dependency on a full templating language or its associated overheads
    whilst still generating safe HTML.
    """
    output = u''
    def __str__(self):
        return self.output

    def write(self, string):
        self.output += string.replace(u'&',u'&amp;')\
           .replace(u'<', u'&lt;')\
           .replace(u'>', u'&gt;')\
           .replace("'", '&#39;')\
           .replace('"', '&#34;')

    def safe(self, string):
        self.output += string

    def getvalue(self):
        return self.output



