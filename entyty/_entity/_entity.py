from ._base_entity import BaseEntity as _BaseEntity, Scene
from .__log__ import log
from typing import Optional as _Optional

class Entity(_BaseEntity):
    log('Initializing entity class.')
    def __init__(
        self,
        name: _Optional[str] = None,
        *args, **kwargs
    ):
        log(f'Instantiating entity {name}.')
        super().__init__(None, None, name, *args, **kwargs)
        if self.name is None:
            self.name = self.__class__.__name__.lower()
        


class LogicalEntity(_BaseEntity):
    """A base class for logical entities."""
    log(f'Initializing logical entity class.')

    def __init__(
            self,
            scene: _Optional[Scene] = None,
            name: _Optional[str] = None,
    ):
        log(f'Instantiating logical entity {name}.')
        super().__init__(scene, None, name)
        if self.name is None:
            self.name = self.__class__.__name__.lower()


class VisualEntity(_BaseEntity):
    """A base class for visual entities."""
    log(f'Initializing visual entity class.')

    def __init__(
            self,
            name: _Optional[str] = None,
            scene: _Optional[Scene] = None,
            position: _Optional[tuple] = None
    ):
        log(f'Instantiating visual entity {name}.')
        super().__init__(scene, None, name)
        if self.name is None:
            self.name = self.__class__.__name__.lower()
        self._position = position
        self._element = None

    @property
    def element(self):
        """Return the element of the entity."""
        return self._element

    @element.setter
    def element(self, value: _Optional[AbstractElement]):
        """Set the element of the entity."""
        self._element = value

    def set_element(self, elem):
        """Set the element of the entity."""
        self.element = elem

    @property
    def position(self):
        """Return the position of the entity."""
        return self._position

    @position.setter
    def position(self, value: tuple):
        """Set the position of the entity"""
        if value is not None:
            self._position = value
            self.x = value[1]
            self.y = value[0]
        else:
            self._position = None
            self.x = None
            self.y = None

    @property
    def x(self):
        """Return the x coordinate of the entity."""
        return self._x

    @x.setter
    def x(self, value):
        """Set the x coordinate of the entity."""
        self._x = value

    @property
    def y(self):
        """Return the y coordinate of the entity."""
        return self._y

    @y.setter
    def y(self, value):
        """Set the y coordinate of the entity."""
        self._y = value

    def update(self, dt):
        super().update(dt)