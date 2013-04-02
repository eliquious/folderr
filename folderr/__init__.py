"""
``folderr`` is a small Python module which is used to verify folder structures.

This module allows a script to verify the existing folder structure before
continuing. Folders can be created if they don't already exist, deleted if
they shouldn't already exist or simple raise an exception if no contengency
action is selected. Files on the other hand can only be deleted or verified
that they already exist. Therefore, files cannot be created if they don't
exist simply because the needed contents of the files are not known.

---
API
---

"""
import os, warnings, shutil

__all__ = ["Path", "Folder", "File", "verify"]

def warn(message):
    warnings.warn(message, UserWarning, stacklevel=2)

class PathDoesNotExistException(Exception):
    """docstring for PathDoesNotExistException"""
    def __init__(self, path, desc):
        super(PathDoesNotExistException, self).__init__()
        self.path = path
        self.desc = desc

    def __str__(self):
        if self.desc is None:
            return "'%s' does not exist" % self.path
        else:
            return "'%s' does not exist; (Comment: %s)" % (self.path, self.desc)

class PathAlreadyExistsException(Exception):
    """docstring for PathAlreadyExistsException"""
    def __init__(self, path, desc):
        super(PathAlreadyExistsException, self).__init__()
        self.path = path
        self.desc = desc

    def __str__(self):
        if self.desc is not None:
            return "'%s' already exists; (Comment: %s)" % (self.path, self.desc)
        else:
            return "'%s' already exists" % (self.path)

class Path(object):
    """
    Path is the base class for the File and Folder classes.

    :param path: Relative path to the root directory given to the ``verify`` function
    :type path: str
    :param shouldExist: sets whether or not the directory should exist at the time of evaluation
    :type shouldExist: bool
    :param deleteIfExists: contingency action if the path exists and shouldn't (shouldExist=False)
    :type deleteIfExists: bool
    :param error: raises Exception if True, otherwise reports a warning
    :type error: bool
    :param createIfNotExists: contingency action if the path should exist and doesn't (shouldExist=True)
    :type createIfNotExists: bool
    :param desc: customize error/warning text - can be used to instruct user to run previous step, etc.
    :type desc: str
    """
    def __init__(self, path, shouldExist=True, deleteIfExists=False, error=True, createIfNotExists=False, desc=None):
        super(Path, self).__init__()
        self.path = path
        self.shouldExist = shouldExist
        self.deleteIfExists = deleteIfExists
        self.createIfNotExists = createIfNotExists
        self.error = error
        self.desc = desc

    def verify(self):
        raise Exception("'verify function must be overridden. Use File/Folder classes instead.")

class Folder(Path):
    """Path object for folders. Used to verify the existence of directories"""
    def __init__(self, path, **kwargs):
        super(Folder, self).__init__(path, **kwargs)

    def verify(self):
        # get absolute path from relative one
        abspath = os.path.abspath(self.path)

        # determine if the path already exists
        exists = os.path.exists(abspath)

        # if the path should already exist (as per args)
        if self.shouldExist:

            # and it doesn't already exist
            if not exists:

                # if folder and createIfNotExists=True, create dir
                if self.createIfNotExists:

                    # create dirs recursively
                    os.makedirs(abspath)

                    # exit function
                    return

                else:
                    if self.error:
                        raise PathDoesNotExistException(abspath, self.desc)
                    else:
                        warn("'%s' does not exist; (Comments: %s)" % (abspath, self.desc))

                        # exit function
                        return

        # if the path should not exist
        else:

            # if file exists
            if exists:

                # if file should be deleted if it exists
                if self.deleteIfExists:

                    # delete folder
                    shutil.rmtree(abspath)

                    # exit function
                    return

                # otherwise raise exception
                else:
                    if self.error:
                        raise PathAlreadyExistsException(abspath, self.desc)
                    else:
                        warn("'%s' already exists; (Comments: %s)" % (abspath, self.desc))

                        # exit function
                        return

class File(Path):
    """Path object for files. Used to verify the existence of files"""
    def __init__(self, path, **kwargs):
        super(File, self).__init__(path, **kwargs)

    def verify(self):
        # get absolute path from relative one
        abspath = os.path.abspath(self.path)

        # determine if the path already exists
        exists = os.path.exists(abspath)

        # if the path should already exist (as per args)
        if self.shouldExist:

            # and it doesn't already exist
            if not exists:

                # if folder and createIfNotExists=True, create dir
                # however, files cannot be created because the needed contents are not known to folderr
                if self.error:
                    raise PathDoesNotExistException(abspath, self.desc)
                else:
                    warn("'%s' does not exist; (Comments: %s)" % (abspath, self.desc))

                    # exit function
                    return

        # if the path should not exist
        else:

            # if file exists
            if exists:

                # if file should be deleted if it exists
                if self.deleteIfExists:
                    # delete file
                    os.remove(abspath)

                    # exit function
                    return

                # otherwise raise exception
                else:
                    if self.error:
                        raise PathAlreadyExistsException(abspath, self.desc)
                    else:
                        warn("'%s' already exists; (Comments: %s)" % (abspath, self.desc))

                        # exit function
                        return

def verify(root, *paths):
    """
    This is the main function of ``folderr`` which is used to verify the existing folder structure for correctness.

    :param root: Root folder for verification
    :type root: str
    :param paths: conditions used to verify the folder structure
    :type paths: list of Folder/File instances
    """
    cwd = os.getcwd()
    os.chdir(root)
    for path in paths:
        try:
            path.verify()
        except:
            os.chdir(cwd)
            raise

    os.chdir(cwd)

