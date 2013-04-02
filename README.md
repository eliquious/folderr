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

###### Folder / File classes

The Folder and File classes are used as conditions to verify a folder structure. Their constructors have the following arguments.

*  **relpath**: *(str)* 
    * Relative path to the root directory given to the ``verify`` function
    * `required=True`
*  **shouldExist**: *(bool)* 
    * Sets whether or not the directory should exist at the time of evaluation
    * `default=True`
*  **deleteIfExists**: *(bool)* 
    *  contingency action if the path exists and shouldn't (shouldExist=False)
    * `default=False`
*  **error** *(bool)* 
    *  raises Exception if True, otherwise reports a warning
    * `default=True`
*  **createIfNotExists**: *(bool)* 
    *  contingency action if the path should exist and doesn't (shouldExist=True)
    * `default=False`
*  **desc** *(str)* 
    *  customize error/warning text - can be used to instruct user to run previous step, etc.
    * `default=None`


###### *function* **verify**(root, *paths)

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

* Creates ``root/date`` if it doesn't exist
* By default, ``folderr`` raises an error unless ``error=False``
    * However, for the config file, ``error`` is not set and will raise an Exception if config.json doesn't exist
* The 'reduce' folder should not exist at runtime and will be deleted if it exists.
    * If the ``deleteIfExists`` kwarg was not set to True, an error would be raised because the folder should not have existed.
