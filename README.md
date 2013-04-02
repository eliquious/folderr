===========================================
folderr - simple dir structure verification
===========================================

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

Path is the base class for the File and Folder classes.

*class* **Path** (relpath[, shouldExist=True[, deleteIfExists=False[, error=True[, createIfNotExists=False[, desc=None]]]]])

*  **relpath**: *(str)* 
    * Relative path to the root directory given to the ``verify`` function
*  **shouldExist**: *(bool)* 
    * Sets whether or not the directory should exist at the time of evaluation
*  **deleteIfExists**: *(bool)* 
    *  contingency action if the path exists and shouldn't (shouldExist=False)
*  **error** *(bool)* 
    *  raises Exception if True, otherwise reports a warning
*  **createIfNotExists**: *(bool)* 
    *  contingency action if the path should exist and doesn't (shouldExist=True)
*  **desc** *(str)* 
    *  customize error/warning text - can be used to instruct user to run previous step, etc.


*class* **Folder**(Path)

  Path object for folders. Used to verify the existence of directories

*class* **File**(Path)

  Path object for files. Used to verify the existence of files

*function* **verify**(root, *paths)

  This is the main function of ``folderr`` which is used to verify the existing folder structure for correctness.

*  **root**: *(str)* 
    *  Root folder for verification
*  **paths**: *(list of Folder/File instances)* 
    *  conditions used to verify the folder structure

-------
Example
-------

    root = get_data_directory()
    date = ...

    verify(
        root,
        Folder(date, createIfNotExists=True),
        File("%%s/config.json" %% date, desc="Create configuration file")
        Folder("%%s/reduce" %% date, shouldExist=False, deleteIfExists=True),
    )

The ``verify`` function in the above code sample does the following:

* Creates ``datadir/date`` if it doesn't exist
* By default, ``folderr`` raises an error unless ``error=False``
    * However, for the config file, ``error`` is not set and will raise an Exception if config.json doesn't exist
* The 'reduce' folder should not exist at runtime and will be deleted if it exists.
    * If the ``deleteIfExists`` kwarg was not set to True, an error would be raised because the folder should not have existed.
