### Pylint doc:

* Structure:
    * my_project:
        * module1/
            * __init__.py
            * file1.py
        * module2/
            * __init__.py
            * file2.py
* Usage for a single script: ```pylint path/to/my_script.py```
* Usage for entire of target project: ```pylint my_project/```

* More information in : https://www.linode.com/docs/guides/install-and-use-pylint-for-python-3/

### Black doc:

* Usage for a single script: ```black path/to/my_script.py```
* Usage for entire of target project: ```black my_project/```
* Check which python file(s) can be formatted in the target folder : ```black --check traget_folder/```
* Stop emitting all non-critical output(Error messages will still be emitted): ```black my_project/ -q```
* More information
  in: https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#configuration-via-a-file

### How Ignore a file?
comment this in target file:

```python
# pylint: skip-file
```

### Generate pyling configuration file:
```shell
pylint --generate-rcfile > .pylintrc
```