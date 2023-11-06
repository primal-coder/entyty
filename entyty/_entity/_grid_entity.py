from __future__ import annotations

import math

import pyglet

from ._entity import *
from typing import Optional as _Optional, Union as _Union

_DIRECTION_MAP = {'south_west': 'down_left', 'west': 'left', 'north_west': 'up_left', 'north': 'up', 'north_east': 'up_right',  'east': 'right', 'south_east': 'down_right', 'south': 'down'}

def throw_exception(exception_type, message):
    """Throws an exception of the specified type with the specified message."""
    raise exception_type(message)

class AbstractGridEntity(LogicalEntity):
    _parent = None
    _grid = None
    _cell = None
    _cell_history = None
    _last_cell = None
    _width =  None
    _height = None
    _path = None
    _speed = None
    _movements = None
    _movements_remaining = None
    _movement_queue = None
    _move_energy = None
    _actions = None
    _is_turn = None
    _vision = None
    _facing = None

    @property
    def speed(self):
        return self._speed

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path):
        self._path = path
        
    @property
    def grid(self):
        return self._grid
    
    @grid.setter
    def grid(self, grid):
        self._grid = grid

    @property
    def cell(self):
        return self._cell
    
    @cell.setter
    def cell(self, cell):
        if cell is not None:
            if self.cell is not None:
                return
            self._cell = cell
        elif self.cell is not None:
            self.last_cell = self.cell
            self._cell = None
            self.cell_history.append(self.last_cell)
            self._pop_handlers()
            

    @property
    def cell_name(self):
        if self.cell is not None:
            return self.cell.designation
        
    @property
    def cell_history(self):
        return self._cell_history
    
    @cell_history.setter
    def cell_history(self, cell_history):
        self._cell_history = cell_history

    @property
    def last_cell(self):
        return self._last_cell
    
    @last_cell.setter
    def last_cell(self, last_cell):
        self._last_cell = last_cell

    @property
    def movements(self):
        if self.speed is not None:
            self._movements = self.speed // 5
        return self._movements if self._movements is not None else 1
    
    @movements.setter
    def movements(self, movements):
        self._movements_remaining = movements
        
    @property
    def movements_remaining(self):
        return self._movements_remaining
    
    @movements_remaining.setter
    def movements_remaining(self, movements_remaining):
        self._movements_remaining = movements_remaining
        
    @property
    def movement_queue(self):
        if self._movement_queue is None:
            self._movement_queue = []
        return self._movement_queue
    
    @movement_queue.setter
    def movement_queue(self, movement_queue):
        if movement_queue is None:
            movement_queue = []
        self._movement_queue = movement_queue
        
    @property
    def move_energy(self):
        if self._move_energy is None:
            self._move_energy = self.speed
        return self._move_energy
    
    @move_energy.setter
    def move_energy(self, move_energy):
        self._move_energy = move_energy

    @property
    def position(self):
        return self.cell.coordinates

    @property
    def x(self):
        return self.cell.coordinates[0] + 2

    @property
    def y(self):
        return self.cell.coordinates[1] + 2    

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def actions(self):
        return self._actions
    
    @actions.setter
    def actions(self, actions):
        self._actions = actions

    @property
    def is_turn(self):
        return self._is_turn
    
    @is_turn.setter
    def is_turn(self, is_turn):
        self._is_turn = is_turn

    @property
    def facing(self):
        """Returns the facing direction in degrees."""
        return self._facing
    
    @facing.setter
    def facing(self, facing: _Optional[_Union[float, int, str]]):
        """Sets the facing direction in degrees."""
        cardinal_directions = {
                "E":  range(337, 360) or range(23),
                "NE": range(23, 68),
                "N":  range(68, 113),
                "NW": range(113, 158),
                "W":  range(158, 203),
                "SW": range(203, 248),
                "S":  range(248, 293),
                "SE": range(293, 338)
        }
        if isinstance(facing, (float)):
            facing = math.degrees(facing)
        elif isinstance(facing, str) and facing in cardinal_directions:
            self._facing = facing
            return
        self._facing = next(
                (
                        direction
                        for direction, angle_range in cardinal_directions.items()
                        if facing in angle_range
                ),
                "Invalid angle",
        )
        

class GridEntity(AbstractGridEntity):
    _base_move_action = {None: {'direction': None, 'from': None, 'to': None}}
    """A class for an The GridEntity is a subclass of LogicalEntity and is assumed to exist on a grid, and
    has a position, a name, and a scale. The scale is used to determine the size of the entity
    when it is drawn on the screen. The scale is a tuple of two integers, the first being the
    width, and the second being the height. The position is a tuple of two integers, the first
    being the x coordinate, and the second being the y coordinate. The name is a string that
    identifies the entity. The grid is a reference to the grid that the entity exists on. The
    cell is a reference to the cell that the entity is currently occupying. The cell_history is
    a list of all cells that the entity has occupied. The last_cell is a reference to the last
    cell that the entity occupied. 
        
    The GridEntity class has the following methods:
    
        set_path_to: Returns a path from the entity's current cell to the destination cell.
        The destination cell can be specified as a string, which is the designation of the
        Cell, or as a Cell object.
        
        vacate: Vacates the cell that the entity is currently occupying. The entity will
        no longer be occupying a cell after this method is called.
        
        occupy: Occupies the cell that is specified. The cell can be specified as a string,
        which is the designation of the cell, or as a Cell object. The entity will be
        occupying the cell after this method is called.
        
        move: Moves the entity to the next cell in its path. The entity will be occupying
        the next cell in its path after this method is called.
        
        set_destination: Sets the destination of the entity to the next cell in its path.
        The entity will be traveling to the next cell in its path after this method is
        called.
        
        update: Updates the entity. This method should be called every frame. The entity
        will be updated after this method is called.
        
        draw: Draws the entity. This method should be called every frame. The entity will
        be drawn after this method is called.
        
        reflect: Reflects the entity's _position on the screen. This method should be called
        every frame. The entity's _position on the screen will be reflected after this method
        is called.   
    """
    def __init__(
            self,
            grid: _Optional[Grid] = None,
            name: _Optional[str] = None,
            parent: _Optional[object] = None,
            *arg, **kwargs
    ):
        super(GridEntity, self).__init__(name)
        self.parent = parent
        self.grid = grid
        init_cell = self.grid.random_cell(attr=('passable', True))
        self.cell = init_cell
        self.cell_history = []
        self.last_cell = None
        self._width =  self.grid.cell_size*0.8
        self._height = self.grid.cell_size*0.8
        self._path = []
        self._speed = parent.speed if parent is not None else 5
        self._movements_remaining = self.speed // 5
        self._actions = {'move': {None:{}}}
        self._action_history = []
        self.traveling = False
        self.occupy(self.cell)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
        self._move_energy = value
        
    def end_turn(self):
        self._action_history.append(self.actions)
        self.move_energy = self.speed - abs(self.move_energy) if self.move_energy < 0 else self.speed
        self.actions = {'move': {None:{}}}

    def get_path_to(self, destination: object):
        return self.grid.get_path(self.cell_name, destination)

    def slice_path(self, path):
        return [path[i:i + self.movements] for i in range(0, len(path), self.movements)]
        
    def set_path_to(self, destination: object):
        self.path = self.get_path_to(destination)
        if len(self.path) > self.movements:
            self.movement_queue = list(self.slice_path(self.path))
        else:
            self.movement_queue = list(self.path)
        self.traveling = True
    
    def vacate(self):
        self.cell.recv_occupant(self)
        self.cell = None

    def occupy(self, cell_to_occupy: object = None):
        if self.cell is None and not cell_to_occupy.occupied or self.last_cell is not None:
            self.cell = cell_to_occupy
        self.cell.recv_occupant(self)
        self._push_handlers(on_vacate=self.cell.recv_occupant, on_occupy=self.cell.recv_occupant)

    def check_destination(self, cell_to_move_to: object = None):
        if cell_to_move_to is not None:
            return bool(cell_to_move_to.passable)

    def move(self, cell_to_move_to: object = None):
        if self.move_energy <= 0:
            print('No energy remaining.')
            return None
        # idx = self.cell.adjacent.index([getattr(self.cell, f'{direction}') for direction in list(_DIRECTION_MAP.values()) if getattr(self.cell, f'{direction}') is cell_to_move_to][0].designation)
        if cell_to_move_to in [self.grid[cell] for cell in self.cell.adjacent]:
            if list(self.actions['move'].keys()) == [None]:
                mvmnt_index = 0
                self.actions['move'].update({0: {'direction': f'{list(_DIRECTION_MAP.keys())[self.cell.adjacent.index(cell_to_move_to.designation)]}', 'from': f'{self.cell.designation}', 'to': f'{cell_to_move_to.designation}'}})
                del self.actions['move'][None]
            else:
                mvmnt_index = len(list(self.actions['move'].keys()))
                self.actions['move'].update({mvmnt_index: {'direction': f'{list(_DIRECTION_MAP.keys())[self.cell.adjacent.index(cell_to_move_to.designation)]}', 'from': f'{self.cell.designation}', 'to': f'{cell_to_move_to.designation}'}})
        elif not cell_to_move_to.passable:
            print('Cell impassable')
            return
        else:
            print('Invalid move')
            return
        energy = self.move_energy
        cost = self.cell.cost_out
        self.vacate()
        self.occupy(cell_to_move_to)
        cost += self.cell.cost_in
        self.move_energy -= cost
        print(f'Energy: {energy} - {cost} = {self.move_energy}')
        return mvmnt_index

    def move_in_path(self, steps = None):
        if self.movement_queue != [] and self.traveling:
            cells = self.movement_queue.pop(0)
            self.path = self.path[len(cells):]
        elif steps is not None:
            if steps <= self._movements_remaining:
                cells = self.path[:steps]
                self.path = self.path[steps:]
            elif steps < len(self.path):
                cells = self.path[:self._movements_remaining]
                self.path = self.path[self._movements_remaining:]
                self.movement_queue = [self.path[i:i + self.movements] for i in range(0, len(self.path), self.movements)][:steps]
                self.traveling = True

            
        for cell in cells:
            self.move(cell)               

    def move_in_direction(self, direction):
        direction = _DIRECTION_MAP[direction] if direction not in _DIRECTION_MAP.values() else direction
        destination = getattr(self.cell, direction)
        if destination is not None:
            return self.move(destination)

    def refresh(self, dt):
        if self._movements_remaining > 0 and self.traveling:
            self.move_in_path()
        elif not self.path:
            self.traveling = False
            self.movement_queue = []
                        
    def draw(self):
        pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, color=(255, 0, 0), batch=self.scene.main_batch)
 