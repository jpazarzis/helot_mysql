# helot_mysql
Adds a mysql wrapper library to helot library.
  
This library is favouring simplicity over comprehension while it allows the user

to easily build on top of it, in case that he wants to specialize its behaviour.

## Installation

#### Using pip
```
pip3 install helot_mysql
```

#### Source code
```
git clone https://github.com/jpazarzis/helot_mysql
sudo python3 setup.py install
```

The exposed components from common are the following: 

## Using the mysql library

#### Importing

To import the package you can use either style:

```python
from helot.mysql import execute_query
```

or

```python
import helot.mysql.execute_query as execute_query
```

The following syntax:
```python
import helot
helot.mysql
```

will not work and will produce the following exception:
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'helot' has no attribute 'mysql'
```
