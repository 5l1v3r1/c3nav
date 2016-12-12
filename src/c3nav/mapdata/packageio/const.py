from c3nav.mapdata.models import AreaOfInterest, GroupOfInterest, Level, Package, Source
from c3nav.mapdata.models.collections import Elevator
from c3nav.mapdata.models.geometry import (Building, Door, ElevatorLevel, Hole, LevelConnector, LineObstacle, Obstacle,
                                           Outside, Room, Stair)

ordered_models = (Package, Level, LevelConnector, Source, Building, Room, Outside, Door, Obstacle, Hole)
ordered_models += (Elevator, ElevatorLevel, LineObstacle, Stair)
ordered_models += (GroupOfInterest, AreaOfInterest)
