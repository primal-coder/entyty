# entyty

**entyty** is a Python module that defines a framework for managing entities in a game or simulation environment. Entities are objects that can exist on a grid, occupy cells, and perform various actions within the system. The module provides base classes for creating and managing entities in a game or simulation. It also includes a set of subclasses that extend the framework to support grid-based entities. The module relies on the [pyglet](https://github.com/pyglet/pyglet) library for event dispatching/handling.

## Package Structure

The "entyty" package consists of the following classes:

- '_AbstractEntity'
- '_BaseEntity'

- 'Entity'
- 'LogicalEntity'
- 'VisualEntity'

- '_AbstractGridEntity'

- 'GridEntity'


## Entities

### Entity

- `Entity` is a subclass of `BaseEntity` representing general entities.

### LogicalEntity

- `LogicalEntity` is a subclass of `BaseEntity` representing logical entities.

### VisualEntity

- `VisualEntity` is a subclass of `BaseEntity` representing visual entities.
- It includes additional properties for managing an element and a position.

### GridEntity

- `GridEntity` is a concrete subclass of `AbstractGridEntity`.
- It represents grid-based entities and includes methods and properties for managing their movement and actions.
- Grid entities can occupy cells, move on a grid, and perform actions.

## Usage

To use the "entyty" package, you can create subclasses of the provided base classes to define specific entity types in your game or simulation. Customize the properties and methods to suit your needs.

Here's a simple example of how to create an entity:

```python
from entyty import LogicalEntity

class MyEntity(LogicalEntity):
    def __init__(self):
        super().__init__(name='MyEntity', **kwargs)

my_entity = MyEntity()
```
