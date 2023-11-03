from __future__ import annotations as _annotations

from ..__log__ import log, log_method

from abc import ABC as _ABC, abstractmethod as _abstractmethod

from pyglet.event import EventDispatcher as _EventDispatcher

from typing import Optional as _Optional

from uuid import uuid4 as _uuid4, UUID as _UUID

import json


class Scene(_ABC):
    pass


class AbstractElement(_ABC):
    pass


class EntityMeta(type):
    dispatcher = _EventDispatcher()
    events = {
            'on_create': 'entity_created',
            'on_update': 'entity_updated',
            'on_delete': 'entity_deleted',
            'on_freeze': 'entity_frozen',
    }
    for event_name in events:
        dispatcher.register_event_type(event_name)
    
    """A metaclass for entity _objects."""

    def __new__(cls, name, bases, attrs):
        """Create a new entity class."""
        return super().__new__(cls, name, bases, attrs)


class AbstractEntity(metaclass=EntityMeta):
    log('Initializing abstract entity class.')
    _scene = None
    _name = None
    _entity_id = None
    _age = 0
    _labels = {'static': [], 'dynamic': []}
    _recvs_input = False
    _inputs = None
    _is_child = False
    _is_parent = False
    _children = None
    _siblings = None
    _parent = None
    """An abstract base class for entity _objects."""

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @name.setter
    def name(self, name):
        """Set the name of the entity."""
        if self._name is None or self.__class__.__name__ != 'BaseEntity':
            self._name = name
        else:
            raise AttributeError("Cannot change the name of an entity.")
        
    @property
    def scene(self):
        """Return the scene of the entity."""
        return self._scene

    @scene.setter
    def scene(self, scene):
        """Set the scene of the entity."""
        if hasattr(self, '_scene'):
            if self._scene is None and scene is not None:
                self._scene = scene
                scene.add_entity(self)
            elif self._scene is not None and scene is None:
                self._scene.remove_entity(self)
                self._scene = None
                del self._scene
            elif self._scene is not None:
                self._scene.remove_entity(self)
                self._scene = scene
                scene.add_entity(self)

    @scene.deleter
    def scene(self):
        if hasattr(self, '_scene') and self._scene is not None:
            self._scene.remove_entity(self)
            self._scene = None
            delattr(self, '_scene')
        else:
            return

    @property
    def entity_id(self):
        """Return the ID of the entity."""
        if self._entity_id is None:
            self._entity_id = _uuid4()
        return self._entity_id.hex

    @entity_id.setter
    def entity_id(self, entity_id):
        """Set the ID of the entity."""
        if isinstance(entity_id, _UUID):
            self._entity_id = entity_id

    @property
    def age(self):
        return self._age

    @classmethod
    def _add_handler(cls, event_type, handler):
        """Add an event handler to the entity."""
        cls.dispatcher.push_handlers(handler, event_type)

    @classmethod
    def _remove_handler(cls, event_type, handler):
        """Remove an event handler from the entity."""
        cls.dispatcher.remove_handlers(handler, event_type)

    @classmethod
    def _push_handlers(cls, *args, **kwargs):
        """Push event handlers to the entity."""
        cls.dispatcher.push_handlers(*args, **kwargs)

    @classmethod
    def _pop_handlers(cls):
        """Pop event handlers from the entity."""
        cls.dispatcher.pop_handlers()

    @classmethod
    def _register_event_type(cls, event_type):
        """Register an event type for the entity."""
        cls.dispatcher.register_event_type(event_type)

    def _dispatch_event(self, event_name, *args):
        """Dispatch an event for the entity."""
        if event_type := self.events.get(event_name):
            self.dispatcher.dispatch_event(event_type, self, *args)

    @_abstractmethod
    def _validate(self):
        """Validate the entity."""
        pass

    def _save(self, file_path: str) -> bool:
        """Save the entity's data to a file.

        Args:
            file_path (str): The path to the file where the data will be saved.

        Returns:
            bool: True if the save operation was successful, False otherwise.
        """
        try:
            data_to_save = {
                    "name":        self.name,
                    "entity_id":   str(self.entity_id),
                    "age":         self.age,
                    # Add more entity-specific data here as needed
            }

            with open(file_path, "w") as file:
                json.dump(data_to_save, file, indent=4)

            print(f"Entity data saved to {file_path}")
            return True
        except Exception as e:
            print(f"Failed to save entity data: {str(e)}")
            return False

    def _update_entity(self):
        pass

    def _adopt(self, child):
        """Adopt a child entity."""
        if not self.children:
            self.children = []
        self.children.append(child)
        self.is_parent = True
        child.parent = self
        child.is_child = True

    def _orphan(self, child):
        """Orphan a child entity."""
        if self._children:
            self._children.remove(child)
        if not self._children:
            self._children = None
            self._is_parent = False
        child._parent = None
        child._is_child = False

    def __eq__(self, other):
        """Check if the entity is equal to another entity."""
        if not isinstance(other, AbstractEntity):
            return False
        return self.entity_id == other.entity_id

    def __hash__(self):
        """Return a hash of the entity."""
        return hash(self.entity_id)


class BaseEntity(AbstractEntity):
    """A base class for entity _objects."""
    log('Initializing base entity class.')
    def __init__(
            self,
            scene: _Optional[Scene] = None,
            entity_id: _Optional[_UUID] = None,
            name: _Optional[str] = None,
            *args, **kwargs
    ):
        """Create a new entity object."""
        super(BaseEntity, self).__init__()
        self.name = name
        self.entity_id = entity_id if entity_id is not None else _uuid4()
        if scene is None:
            del self.scene
        else:
            self.scene = scene

    def _validate(self):
        pass

    def update(self, dt):
        self._age += 1
