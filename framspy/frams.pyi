# Type stub file for the ``frams`` module (accessing Framsticks objects from Python).
# Place this ``frams.pyi`` file in the same directory as ``frams.py``
# to enable documentation, static type checking, and IDE autocomplete support.

"""
Framsticks as a Python module.

Static FramScript objects are available inside this module under their well-known names
(frams.Simulator, frams.GenePools, etc.)

These objects and all values passed to and from Framsticks are instances of ``frams_extvalue.ExtValue`` class.
Python values are automatically converted to Framsticks data types.
Use ExtValue._makeInt()/_makeDouble()/_makeString()/_makeNull() for explicit conversions.
Simple values returned from Framsticks can be converted to their natural Python
counterparts using ``_value()``, or forced to a specific type with ``_int()``/``_double()``/``_string()``.

All non-Framsticks Python attributes start with '_' to avoid conflicts with Framsticks attributes.
Framsticks names that are Python reserved words are prefixed with 'x' (currently just Simulator.ximport).

For sample usage, see ``frams-test.py`` and ``FramsticksLib.py``.

If you want to run many independent instances of this class in parallel, use the "multiprocessing" module and then each process
that uses this module will initialize it and get access to a separate instance of the Framsticks library.

If you want to use this module from multiple threads concurrently, use the "-t" option for ``init()``.
This will make concurrent calls from different threads sequential, thus making them safe.
However, this will likely degrade performance (due to required locking) compared to the single-threaded use.

For interfaces in other languages (e.g., using the Framsticks library in your C++ code), see ``../cpp/frams/frams-objects.h``
"""



from typing import Any, Type, Iterator, overload  #, type_check_only
from typing import Any as Object  # Framsticks occasionally uses Object as a type (besides "untyped") - check what is the difference
from warnings import deprecated
from frams_extvalue import ExtValue



# More complete type hinting - (meta)classes to facilitate access via indexing [i] equivalent to get(i) and iteration "value in Class":
# This could be automated for all iterable and indexable classes in Framsticks (vectors, dictionaries, etc.).
# Unfortunately, simpler approaches like __getitem__ = get or __class_getitem__ = get or avoiding metaclasses and defining these access methods in the actual classes did not work.

class GenePoolsIndexer(type):
    def __getitem__(cls, index: int) -> Type[GenePool]: ...
    def __iter__(cls) -> Iterator[Type[GenePool]]: ...

class PopulationsIndexer(type):
    def __getitem__(cls, index: int) -> Type[Population]: ...
    def __iter__(cls) -> Iterator[Type[Population]]: ...

class GenePoolIndexer(type):
    def __getitem__(cls, index: int) -> Type[Genotype]: ...
    def __iter__(cls) -> Iterator[Type[Genotype]]: ...

class PopulationIndexer(type):
    def __getitem__(cls, index: int) -> Type[Creature]: ...
    def __iter__(cls) -> Iterator[Type[Creature]]: ...

class NeuroProperties(ExtValue): ...  # the only class that is used once (Neuro.neuroproperties) in global context, but not defined in that context (and not really useful unless defining new *.neuro script neurons). This class is defined in "Neuron definitions" context, but let's not include that entire context, just provide a placeholder for this single class.

# auto-generated (from "framscript.xml") class declarations follow:


class CheckpointEvent(ExtValue):
    """ Used in onSlaveCheckpoint() which is called when a Slave Simulator checkpoint is reached. """

    index: int|ExtValue[int]
    """ **Slave index** """
    slave: Simulator
    ticks: int|ExtValue[int]
    """ **Simulator ticks** """
    data: Any|ExtValue[Any]
    """ **Checkpoint data** """

class Collision(ExtValue):
    """ Used in collision handlers (On___Collision). Contains the detailed information about the colliding parts (Part1,Part2 and their associated MechParts and Creatures). See the onFoodCollision() function in standard.expdef """

    Part1: Object
    Part2: Object
    MechPart1: Object
    MechPart2: Object
    Creature1: Object
    Creature2: Object

class CrCollision(ExtValue):
    """ Used in creature collision handlers (On___CrCollision). """

    Creature1: Object
    Creature2: Object

class Creature(ExtValue):
    """
    The object inside the simulated world, including its physical structure, neural network and performance data. Food pieces, obstacles and other movable objects can be implemented as Creatures even though they are not "alive".\n
    Before version 4.0rc4, the static Creature object was used in event handlers and in functions operating on the "selected" creature. This is now deprecated as all operations can be performed using the more convenient direct access (see GenePools). For event handlers, the creature object will be passed as argument, like this:\n
    function onDied(cr) {Simulator.print("Creature "+cr.name+" has died");}\n
    See also: Population.
    """

    name: str|ExtValue[str]
    genotype: str|ExtValue[str]
    info: str|ExtValue[str]
    """ Additional info or comments """
    group: Any|ExtValue[Any]
    """
    **creature's Population**
    
    Deprecated. Use population instead.
    """
    population: Population
    """ **creature's population** """
    index: int|ExtValue[int]
    """
    **current index in population**
    
    Note that the index changes depending on the current creature position in the population. Use Creature.uid if you need a permanent identifier that persists through the entire object lifetime.
    """
    num: int|ExtValue[int]
    """
    **Ordinal number**
    
    Acts as a unique identifier, but less strict than "uid". Unlike "uid", "num" can be changed and therefore can be saved and restored, providing persistence and continuity beyond a single application run. "num" is only guaranteed to be unique if it is autogenerated and not changed by the user, otherwise it is user's responsibility to manage the proper values of "num". Autogenerated "num" is always equal to the largest previously used "num" + 1. The largest previously used value is stored in Simulator.last_creature_num and can be changed as well (and is automatically saved and restored as a part of the Simulator state). Limitation: being a 32-bit integer, "num" overflows at about 2 billion counts.\n
    See also: uid
    """
    gnum: int|ExtValue[int]
    """ **Generation** """
    buildproblems: int|ExtValue[int]
    """ **Build problems** """
    energ0: float|ExtValue[float]
    """ **Starting energy** """
    energy0: float|ExtValue[float]
    """ **Starting energy** """
    idleen: float|ExtValue[float]
    """
    **Idle energy consumption**
    
    The amount of energy subtracted from the energy of this creature in each simulation step, as in: cr.energy-=cr.idleen;
    """
    energy: float|ExtValue[float]
    perf: int|ExtValue[int]
    """
    **Performance calculation**
    
    Replaced by perf_measuring
    """
    perf_measuring: int|ExtValue[int]
    """
    **Performance calculation**
    
    The initial value of this property is taken from Population.initial_perf_measuring
    """
    nnenabled: int|ExtValue[int]
    """
    **NN enabled**
    
    Replaced by nn_active
    """
    nn_active: int|ExtValue[int]
    """
    **NN active**
    
    The initial value of this property is taken from Population.nn_active
    """
    bodysim: int|ExtValue[int]
    """
    **Body simulation**
    
    Replaced by physics_active
    """
    physics_active: int|ExtValue[int]
    """
    **Body simulation**
    
    (Physical) body simulation can be disabled for individual objects which makes them immovable. Disabled objects can still participate in collisions depending on their collisions masks. The initial value of this property is taken from Population.initial_physics_active.
    
    Bugs: the standard collision handler does not work for disabled objects when ODE simulation is used. It means that these objects won't physically interact with other objects. The custom (scripting) handlers work as expected.
    """
    selfcol: int|ExtValue[int]
    """
    **Self-collisions**
    
    Replaced by self_collisions
    """
    self_collisions: int|ExtValue[int]
    """
    **Self-collisions**
    
    Enable/disable detection of self-collisions (within a creature body). They can only occur when using the ODE simulation engine. If enabled, the creature will have its sticks collide during lifespan.  The initial value of this property is taken from Population.initial_self_collisions.
    """
    @staticmethod
    @deprecated
    def selfcolstate() -> int|ExtValue[int]:
        """
        **Self-collisions**
        
        Replaced by selfCollisionsCount()
        """
        ...

    @staticmethod
    def selfCollisionsCount() -> int|ExtValue[int]:
        """
        **Current self-collisions state**
        
        Returns the number of self-collisions detected in the creature.
        """
        ...

    lifespan: int|ExtValue[int]
    """ While the creature's performance measurement is enabled, the creature's lifespan is incremented in "performance sampling period" intervals. """
    steps_after_birth: int|ExtValue[int]
    """
    **Simulation steps after birth**
    
    "Birth" is the moment when the simulation of a creature starts.
    """
    steps_in_lifespan: int|ExtValue[int]
    """
    **Simulation steps in lifespan**
    
    "Lifespan" is the period during simulation of a creature when its performance measurement is enabled.
    """
    distance: float|ExtValue[float]
    """ See https://www.framsticks.com/a/al_params.html#exper-perfcalc """
    c_velocity: float|ExtValue[float]
    """
    **Recent period velocity**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    c_vertvelocity: float|ExtValue[float]
    """
    **Recent period vertical velocity**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    c_vertpos: float|ExtValue[float]
    """
    **Recent period vertical position**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    velocity: float|ExtValue[float]
    """
    **Average velocity**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    vertpos: float|ExtValue[float]
    """
    **Average vertical position**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    vertvel: float|ExtValue[float]
    """
    **Average vertical velocity**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    pos_x: float|ExtValue[float]
    """
    **Position x**
    
    (pos_x,pos_y,pos_z) is the point of minimal coordinates ("bottom left corner") of the creature, including imaginary Part sizes (Part.s, usually 1.0). See also: Creature.moveAbs
    """
    pos_y: float|ExtValue[float]
    """
    **Position y**
    
    See Creature.pos_x
    """
    pos_z: float|ExtValue[float]
    """
    **Position z**
    
    See Creature.pos_x
    """
    size_x: float|ExtValue[float]
    """
    **Bounding box x size**
    
    (size_x,size_y,size_z) are dimensions of the axis-aligned bounding box of the creature, including the imaginary part sizes (Part.s, usually 1.0). A creature consisting of a single default Part has the size of (2.0,2.0,2.0) - twice the Part.s value (like a sphere diameter is twice its radius).\n
    See also: Creature.moveAbs
    """
    size_y: float|ExtValue[float]
    """
    **Bounding box y size**
    
    See Creature.size_x
    """
    size_z: float|ExtValue[float]
    """
    **Bounding box z size**
    
    See Creature.size_x
    """
    center_x: float|ExtValue[float]
    """
    **center.x**
    
    Center of gravity
    """
    center_y: float|ExtValue[float]
    """
    **center.y**
    
    Center of gravity
    """
    center_z: float|ExtValue[float]
    """
    **center.z**
    
    Center of gravity
    """
    bboxLow: XYZ
    """ **Bounding box 'low' corner** """
    bboxHigh: XYZ
    """ **Bounding box 'high' corner** """
    bboxCenter: XYZ
    """ **Bounding box center** """
    bboxSize: XYZ
    """ **Bounding box size** """
    bboxGroundOffset: float|ExtValue[float]
    """
    **Bounding box ground offset**
    
    Due to multiple modes of simulation and Part shapes, you need to add this value to the intended creature bottom elevation to get the 'z' coordinate of the bboxLow that places the creature exactly on the specific height level.\n
    Example:\n
    creature.locationSetBboxLow(10,10,0+creature.bboxGroundOffset); //bottom of the crearture will be at level 0 on a flat ground
    """
    centerOfGravity: XYZ
    """
    **Center of gravity**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    numparts: int|ExtValue[int]
    """ **Number of body Parts** """
    numjoints: int|ExtValue[int]
    """ **Number of body Joints** """
    numneurons: int|ExtValue[int]
    """ **Number of neurons** """
    numconnections: int|ExtValue[int]
    """ **Number of neural connections** """
    data: Dictionary
    """ **Custom fields dictionary** """
    user1: Any|ExtValue[Any]
    """ **User field 1** """
    user2: Any|ExtValue[Any]
    """ **User field 2** """
    user3: Any|ExtValue[Any]
    """ **User field 3** """
    @staticmethod
    @deprecated
    def move(dx: float|ExtValue[float], dy: float|ExtValue[float], dz: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **Move by a vector**
        
        Replaced by locationMoveBy().
        """
        ...

    @staticmethod
    def locationMoveBy(dx: float|ExtValue[float], dy: float|ExtValue[float], dz: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **Move by a vector**
        
        Shift the creature by a given vector (in world coordinates).
        """
        ...

    @staticmethod
    @deprecated
    def moveAbs(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **Move to absolute location**
        
        Replaced by locationSetBboxLow().
        """
        ...

    @staticmethod
    def locationSetBboxLow(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **Move bounding box corner to absolute location**
        
        Moves the creature as determined by the "low" corner (the one with the lower coordinate values) of the bounding box of a creature.
        """
        ...

    @staticmethod
    def locationSetBboxCenter(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **Move bounding box center to absolute location**
        
        Moves the creature as determined by the center of the bounding box of a creature.
        """
        ...

    @staticmethod
    @deprecated
    def moveLocal(dx: float|ExtValue[float], dy: float|ExtValue[float], dz: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **Move by a vector in local coordinates**
        
        Replaced by locationMoveLocalBy
        """
        ...

    @staticmethod
    def locationMoveLocalBy(dx: float|ExtValue[float], dy: float|ExtValue[float], dz: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **Move by a vector in local coordinates**
        
        Local coordinates are measured with respect to the position and orientation of the first Part.
        """
        ...

    @staticmethod
    def localToWorld(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> XYZ:
        """
        **Return world coordinates**
        
        Local coordinates are measured with respect to the position and orientation of the first Part.
        """
        ...

    @staticmethod
    def worldToLocal(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> XYZ:
        """
        **Return local coordinates**
        
        Local coordinates are measured with respect to the position and orientation of the first Part.
        """
        ...

    orient: Orient
    """
    **Orientation**
    
    By convention, the orientation of the creature is equal to the orientation of its first Part.
    """
    @staticmethod
    def rotate(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> None|ExtValue[None]:
        """ Rotate the creature around X, Y and Z axes. Should only be used immediately after creating a new creature (before the first simulation step is performed for this creature), otherwise further simulation can be disturbed. """
        ...

    @staticmethod
    def rotateLocal(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **Rotate in local coordinates**
        
        Rotate the creature around (local) X, Y and Z axes. Should only be used immediately after creating a new creature (before the first simulation step is performed for this creature), otherwise further simulation can be disturbed.
        """
        ...

    drive: XYZ
    """
    **Enforce constant speed**
    
    Measured in global coordinates.
    """
    driveLocal: XYZ
    """
    **Enforce local constant speed**
    
    Measured in local coordinates, that is, with respect to the current orientation of the creature.\n
    See also: Creature.orient
    """
    localDrive: XYZ
    """
    **Enforce constant speed**
    
    This field is now called driveLocal.
    """
    @staticmethod
    def getPart(index: int|ExtValue[int]) -> Part:
        """ **Get Part (static Model information)** """
        ...

    @staticmethod
    def getJoint(index: int|ExtValue[int]) -> Joint:
        """ **Get Joint (static Model information)** """
        ...

    @staticmethod
    def getNeuroDef(index: int|ExtValue[int]) -> NeuroDef:
        """ **Get NeuroDef** """
        ...

    @staticmethod
    def getMechPart(index: int|ExtValue[int]) -> MechPart:
        """ **Get MechPart (current properties)** """
        ...

    @staticmethod
    def getMechJoint(index: int|ExtValue[int]) -> MechJoint:
        """ **Get MechJoint (current properties)** """
        ...

    @staticmethod
    def getNeuro(index: int|ExtValue[int]) -> Neuro:
        """ **Get Neuro** """
        ...

    outdated_neuro_classes: Any|ExtValue[Any]
    """
    **Outdated neuro classes**
    
    Names of the neuron classes that have been modified after this creature was built
    """
    selfmask: int|ExtValue[int]
    """
    **Collision mask (self)**
    
    Creature's selfmask is set according to the Creature's Population.selfmask. See Population.selfmask for detailed information about collision handling.
    """
    othermask: int|ExtValue[int]
    """
    **Collision mask (other)**
    
    Creature's othermask is set according to the Creature's Population.othermask. See Population.selfmask for detailed information about collision handling.
    """
    geno: Geno
    """
    **Genotype**
    
    Source genotype for this creature
    """
    model: Model
    """
    **Source Model**
    
    Source Model for this creature
    """
    liveModel: Model
    """
    **Current Model**
    
    A Model object that is a copy of the current (temporary) geometry of this creature
    """
    uid: str|ExtValue[str]
    """
    **#**
    
    Unique identifier that is generated on object creation. "uid" is only unique during a single application run. Subsequent runs generate the same sequence of uid values.\n
    See also: num
    """
    signals: CreatureSignals
    """ **Signal sources** """
    @staticmethod
    def boundingBoxCollisions(mask: int|ExtValue[int]) -> int|ExtValue[int]:
        """
        **Check bounding box collisions**
        
        Checks approximate collisions for the selected creature.\n
        Returns the collision mask calculated as ( mask & colliding_creatures.othermask ). Usually called with mask=0, which has the special meaning of using the current creature.selmask instead of 0, so that it detects the same type of collisions as the current experiment configuration.\n
        Passing non-zero mask value uses it instead of creature.selfmask, allowing you to include or exclude other colliding populations, as if creature.selfmask were modified temporarily.
        """
        ...

    @staticmethod
    def checkCollisions(mask: int|ExtValue[int], accuracy: int|ExtValue[int]) -> Any|ExtValue[Any]:
        """
        **Check collisions**
        
        Returns zero if the creature does not collide with other creatures.\n
        Arguments:\n
        - mask: if not zero, temporarily replaces creature.selfmask. For details see boundingBoxCollisions()\n
        - accuracy:
         0 = testing creature bounding boxes\n
         1 = testing creature elements
        """
        ...

    @staticmethod
    def transferEnergyTo(recipient: Creature, requested_amount_of_energy: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **Transfer energy**
        
        Transfers at most the requested_amount_of_energy from this creature to the recipient. Returns the amount of energy actually transferred.\n
        The function will only transfer positive amounts and will not transfer more energy than this creature has, so the function is equivalent to:\n
        if (this.energy>0 && requested_amount_of_energy>0)\n
        {
          var amount = Math.min(requested_amount_of_energy, this.energy);\n
          recipient.energy += amount;\n
          this.energy -= amount;
        }
        
        Calling this function from inside the collision handler to transfer energy between colliding parts automatically adds the relevant MechPart references, as if transferEnergyToPart was called, i.e.
        	Collision.Creature1.transferEnergyTo(Collision.Creature2, e);
        is equivalent to:
        	Collision.Creature1.transferEnergyToPart(Collision.Part1, Collision.Creature2, Collision.Part2, e);
        When this behavior is not intended, explicit nulls in transferEnergyToPart() can be used to avoid associating the energy transfer with the currently colliding parts, like this:
        	Collision.Creature1.transferEnergyToPart(null, Collision.Creature2, null, e);
        """
        ...

    @staticmethod
    def transferEnergyToPart(source_part: MechPart, recipient_creature: Creature, recipient_part: MechPart, requested_amount_of_energy: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **Transfer energy**
        
        Transfer energy between specific parts of two creatures. Part arguments are only used for visualization and can be null, which would mean "the entire creature".\n
        See also: transferEnergyTo()
        """
        ...


class CreatureSettings(ExtValue):
    """ Creature building parameters """

    minjoint: float|ExtValue[float]
    """ **Minimal joint length** """
    maxjoint: float|ExtValue[float]
    """ **Maximal joint length** """
    randinit: float|ExtValue[float]
    """
    **Random initialization**
    
    Allowed range for initializing all neuron states with uniform distribution random numbers and zero mean. Set to 0 for deterministic initialization.
    """
    nnoise: float|ExtValue[float]
    """
    **Noise**
    
    Gaussian neural noise: a random value is added to each neural output in each simulation step. Set standard deviation here to add random noise, or 0 for deterministic simulation.
    """
    touchrange: float|ExtValue[float]
    """ **T receptor range** """
    bnoise_struct: float|ExtValue[float]
    """
    **Body disturbance**
    
    When >0, body constructs of creatures (position of Parts) will be randomly disturbed when they are created.
    """
    bnoise_vel: float|ExtValue[float]
    """
    **Initial movement**
    
    Random velocities will be applied to all body Parts (in MechaStick) or rigid segments (in ODE) of newly created creatures.
    """

class CreatureSignals(ExtValue):
    """ Signal sources associated with a creature. See also: Signal, WorldSignals, NeuroSignals. """

    @staticmethod
    def add(channel: str|ExtValue[str]) -> Signal:
        """ **Create a new signal** """
        ...

    @staticmethod
    def addProperty(channel: str|ExtValue[str], property: Any|ExtValue[Any]) -> Signal:
        """
        **Create property-based signal**
        
        Create a signal that automatically reflects one of the creature's properties (i.e. its power is equal to the property value).\n
        Example:\n
        Creature.signals.addProperty("energy","energy"); //then, Neuro.signals.receive("energy") in a custom neuron would work similarly to a built-in smell sensor.
        """
        ...

    @staticmethod
    def receive(channel: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **Receive signal in channel**
        
        Receive the aggregated signal power in a given channel.
        """
        ...

    @staticmethod
    def receiveSet(channel: str|ExtValue[str], max_distance: float|ExtValue[float]) -> Vector:
        """
        **Receive signals in range**
        
        Get all signals in the specified range. Returns a read-only vector object containing Signal objects - individual signals can be accessed as result[0], .., result[result.size-1].
        """
        ...

    @staticmethod
    def receiveFilter(channel: str|ExtValue[str], max_distance: float|ExtValue[float], flavor: float|ExtValue[float], flavorfilter: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **Receive filtered signal**
        
        Receive the aggregated signal power in a given channel.
        
        Additional filtering options:\n
        - Max distance only receives the neighbor signals (based on their physical location)\n
        - Flavor filtering: only signals having the flavor similar to the specified value will be received. The flavorfilter value is the difference of flavor that reduces the received signal to 0. The "flavor attenuation" is linear, i.e., signals differing by (filter/2) in flavor will be reduced to 50%.
        """
        ...

    @staticmethod
    def receiveSingle(channel: str|ExtValue[str], max_distance: float|ExtValue[float]) -> Signal:
        """
        **Receive strongest**
        
        Find the signal source that has the highest signal power (taking into account distance).
        """
        ...

    @staticmethod
    def get(index: int|ExtValue[int]) -> Signal:
        """ **Access individual signals (index = 0 .. size-1)** """
        ...

    size: int|ExtValue[int]
    """ **Number of signals in this set** """
    @staticmethod
    def clear() -> None|ExtValue[None]:
        """ **Delete all signals** """
        ...


class CreatureSnapshot(ExtValue):
    """
    A data object consisting of the same fields as the serialized Creature. Typically used for reading a Creature back from a file; Population.add(snapshot_object) recreates the Creature object from the snapshot. When the creature is added to a population and it happens to collide with the terrain, the creature will be automatically moved upwards just enough to avoid the collision.\n
    Serialized Creature preserves most of its data fields (including the 'data' dictionary) but only keeps aggregated information about its physical state, which is body orientation and location of the bounding box center. Individual physical body parts' locations, states and neuron states are lost.\n
    Restoring the state of a formerly living, serialized creature using its CreatureSnapshot is not perfect. Apart from losing information about individual body and brain parts and their states, the usual flow of calculating performance may be disturbed, which is related to the 'performance sampling period' being interrupted as well as the specifics of the 'freezing period' mechanism. In consequence, the intended behavior of 'lifespan', 'steps_in_lifespan', and performance fields may be broken. For example, when period=100, after every 100 'steps_in_lifespan', the 'lifespan' increases by 100 and the new performance data is calculated. When the period is interrupted by saving/restoring, 'steps_in_lifespan' continues to increase from the saved value, but performance counters will be waiting another full 100 steps before the next update, losing the information from the unfinished period. The resulting 'lifespan' will be lower than it would have been without interruptions, and will be inconsistent with 'steps_in_lifespan'. Because of these issues, it is strongly advised to thoroughly inspect and test the behavior of the restored Creatures in various moments in their lifepspan, and use CreatureSnapshot only when necessary.\n
    See also: scripts/standard_exploadsave.inc\n
    See also: Population.add()
    """

    @staticmethod
    def new() -> Creature:
        """ **create new object** """
        ...

    name: str|ExtValue[str]
    genotype: str|ExtValue[str]
    info: str|ExtValue[str]
    """ Additional info or comments """
    num: int|ExtValue[int]
    """
    **Ordinal number**
    
    Acts as a unique identifier, but less strict than "uid". Unlike "uid", "num" can be changed and therefore can be saved and restored, providing persistence and continuity beyond a single application run. "num" is only guaranteed to be unique if it is autogenerated and not changed by the user, otherwise it is user's responsibility to manage the proper values of "num". Autogenerated "num" is always equal to the largest previously used "num" + 1. The largest previously used value is stored in Simulator.last_creature_num and can be changed as well (and is automatically saved and restored as a part of the Simulator state). Limitation: being a 32-bit integer, "num" overflows at about 2 billion counts.\n
    See also: uid
    """
    gnum: int|ExtValue[int]
    """ **Generation** """
    energy0: float|ExtValue[float]
    """ **Starting energy** """
    idleen: float|ExtValue[float]
    """
    **Idle energy consumption**
    
    The amount of energy subtracted from the energy of this creature in each simulation step, as in: cr.energy-=cr.idleen;
    """
    energy: float|ExtValue[float]
    perf_measuring: int|ExtValue[int]
    """
    **Performance calculation**
    
    The initial value of this property is taken from Population.initial_perf_measuring
    """
    nn_active: int|ExtValue[int]
    """
    **NN active**
    
    The initial value of this property is taken from Population.nn_active
    """
    physics_active: int|ExtValue[int]
    """
    **Body simulation**
    
    (Physical) body simulation can be disabled for individual objects which makes them immovable. Disabled objects can still participate in collisions depending on their collisions masks. The initial value of this property is taken from Population.initial_physics_active.
    
    Bugs: the standard collision handler does not work for disabled objects when ODE simulation is used. It means that these objects won't physically interact with other objects. The custom (scripting) handlers work as expected.
    """
    self_collisions: int|ExtValue[int]
    """
    **Self-collisions**
    
    Enable/disable detection of self-collisions (within a creature body). They can only occur when using the ODE simulation engine. If enabled, the creature will have its sticks collide during lifespan.  The initial value of this property is taken from Population.initial_self_collisions.
    """
    lifespan: int|ExtValue[int]
    """ While the creature's performance measurement is enabled, the creature's lifespan is incremented in "performance sampling period" intervals. """
    steps_after_birth: int|ExtValue[int]
    """
    **Simulation steps after birth**
    
    "Birth" is the moment when the simulation of a creature starts.
    """
    steps_in_lifespan: int|ExtValue[int]
    """
    **Simulation steps in lifespan**
    
    "Lifespan" is the period during simulation of a creature when its performance measurement is enabled.
    """
    distance: float|ExtValue[float]
    """ See https://www.framsticks.com/a/al_params.html#exper-perfcalc """
    c_velocity: float|ExtValue[float]
    """
    **Recent period velocity**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    c_vertvelocity: float|ExtValue[float]
    """
    **Recent period vertical velocity**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    c_vertpos: float|ExtValue[float]
    """
    **Recent period vertical position**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    velocity: float|ExtValue[float]
    """
    **Average velocity**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    vertpos: float|ExtValue[float]
    """
    **Average vertical position**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    vertvel: float|ExtValue[float]
    """
    **Average vertical velocity**
    
    See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    center_x: float|ExtValue[float]
    """
    **center.x**
    
    Center of gravity
    """
    center_y: float|ExtValue[float]
    """
    **center.y**
    
    Center of gravity
    """
    center_z: float|ExtValue[float]
    """
    **center.z**
    
    Center of gravity
    """
    bboxCenter: XYZ
    """ **Bounding box center** """
    data: Dictionary
    """ **Custom fields dictionary** """
    user1: Any|ExtValue[Any]
    """ **User field 1** """
    user2: Any|ExtValue[Any]
    """ **User field 2** """
    user3: Any|ExtValue[Any]
    """ **User field 3** """
    orient: Orient
    """
    **Orientation**
    
    By convention, the orientation of the creature is equal to the orientation of its first Part.
    """
    selfmask: int|ExtValue[int]
    """
    **Collision mask (self)**
    
    Creature's selfmask is set according to the Creature's Population.selfmask. See Population.selfmask for detailed information about collision handling.
    """
    othermask: int|ExtValue[int]
    """
    **Collision mask (other)**
    
    Creature's othermask is set according to the Creature's Population.othermask. See Population.selfmask for detailed information about collision handling.
    """
    uid: str|ExtValue[str]
    """
    **#**
    
    Unique identifier that is generated on object creation. "uid" is only unique during a single application run. Subsequent runs generate the same sequence of uid values.\n
    See also: num
    """

class Dictionary(ExtValue):
    """
    Dictionary associates stored values with string keys ("key" is the first argument in get/set/remove functions). Integer key can be used to enumerate all elements (note that while iterating, the elements are returned in no particular order).\n
    Examples:
    	var d;\n
    	d=Dictionary.new();\n
    	d.set("name","John");\n
    	d.set("age",44);
    Another way of doing the same:
    	d={};\n
    	d["name"]="John";\n
    	d["age"]=44;
    And the most concise way:
    	d={ "name":"John", "age":44 };
    Iterating:
    	for(var v in d) Simulator.print(v); //values\n
    	for(var k in d.keys) Simulator.print(k+" is "+d[k]); //keys\n
    	for(var i=0;i<d.size;i++) Simulator.print(d.getKey(i)+" is "+d.get(i)); //by index
    """

    @staticmethod
    def clear() -> None|ExtValue[None]:
        """ **Clear data** """
        ...

    size: int|ExtValue[int]
    """ **Element count** """
    @staticmethod
    def remove(key: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ Removes the named or indexed element (depending on the argument type: string or int). """
        ...

    @staticmethod
    def get(key: Any|ExtValue[Any]) -> Any|ExtValue[Any]:
        """
        **Get element**
        
        Retrieves the named or indexed element (depending on the argument type: string or int). Accessing nonexistent keys is an error (use hasKey() if necessary).\n
        object.get(key) can be shortened to object[key].
        """
        ...

    @staticmethod
    def getKey(index: int|ExtValue[int]) -> str|ExtValue[str]:
        """
        **Get a key**
        
        Returns the key of the indexed element (0 <= index < size).
        """
        ...

    @staticmethod
    def hasKey(key: str|ExtValue[str]) -> int|ExtValue[int]:
        """
        **Check if key exists**
        
        Returns 1 (interpreted as true) if dictionary contains the supplied key, or 0 (false) otherwise.\n
        Example:
           if (obj.hasKey("a"))
              x = obj->a;
        """
        ...

    @staticmethod
    def set(key: Any|ExtValue[Any], value: Any|ExtValue[Any]) -> Any|ExtValue[Any]:
        """
        **Set element**
        
        Set element value for the specified key or index (depending on the argument type: string or int).\n
        Returns the value previously associated with the given key (or index).\n
        object.set(key,value) can be shortened to object[key]=value. Literal string keys can use even shorter notation: object->key=value instead of object.set("key",value)\n
        Note the difference in the returned value:
          var old_value=object.set("key",new_value); //'old_value' gets the value previously associated with "key"\n
          var x=object["key"]=new_value; //'x' becomes 'new_value', consistently with the semantics of the assignment operator. The value previously associated with "key" is lost.
        """
        ...

    @staticmethod
    def find(value: Any|ExtValue[Any]) -> Any|ExtValue[Any]:
        """ Returns the element key or null if not found. """
        ...

    @staticmethod
    def new() -> Dictionary:
        """
        **Create a Dictionary**
        
        Empty directory can be also created using the {} expression.
        """
        ...

    toString: str|ExtValue[str]
    """ **Textual form** """
    @staticmethod
    def clone() -> Dictionary:
        """
        **Create a clone**
        
        The resulting clone is a shallow copy (contains the same object references as the original). A deep copy can be obtained through serialization: String.deserialize(String.serialize(object));
        """
        ...

    @staticmethod
    def assign(arg1: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """
        **Assign from another object**
        
        Replaces current dictionary with dictionary contents from another object.
        """
        ...

    iterator: Object
    keys: Object
    """ Iterate over this object to get all keys: for(k in dict.keys) ... """

class EnergyParticles(ExtValue):


    enpa_lifespan_min: int|ExtValue[int]
    """
    **Lifespan minimum**
    
    Particle's lifespan is a random number taken from the specified range [min,max]
    """
    enpa_lifespan_max: int|ExtValue[int]
    """
    **Lifespan maximum**
    
    Particle's lifespan is a random number taken from the specified range [min,max]
    """
    enpa_amount_min: float|ExtValue[float]
    """
    **Particle energy minimum**
    
    A particle is emitted if the amount of energy transferred in a single step exceeds this threshold
    """
    enpa_amount_max: float|ExtValue[float]
    """
    **Particle energy maximum**
    
    A maximum amount of energy a single particle can represent. If energy transferred in a single simulation step exceeds this amount, more particles are created.
    """
    enpa_step_maxparticles: int|ExtValue[int]
    """
    **Max particles per step**
    
    Limit the number of particles created in a single step for each energy transfer
    """
    enpa_random_pos: float|ExtValue[float]
    """
    **Randomize positions**
    
    The amount of random shift used for individual particles (uniform distribution)
    """
    enpa_turn: float|ExtValue[float]
    """
    **Turn towards target**
    
    Ignore (0) or directly follow (1) the potentially moving target of a particle. Intermediate values create momentum effect as if the target was gradually adjusted.
    """
    enpa_speedup: float|ExtValue[float]
    """
    **Particle speedup**
    
    Increase particle speed by this factor in each simulation step. This can help reach moving targets (along with "Turn towards target").
    """
    enpa_fade: float|ExtValue[float]
    """
    **Fade out orphans**
    
    Gradually decrease particle size before it disappears when its energy transfer has ended while the particle was on its way. The remaining energy amount is multiplied by this factor in each step. 0 means: disappear immediately, 1 means: don't decrease the size at all. Note that these parameters only concern visualization and the actual energy was already transferred.
    """
    enpa_total_limit: int|ExtValue[int]
    """
    **Total particle limit**
    
    Limit the total number of existing energy particles (to save performance)
    """
    enpa_display_min: float|ExtValue[float]
    """
    **Min particle size**
    
    Visible particle size at minimum energy
    """
    enpa_display_max: float|ExtValue[float]
    """
    **Max particle size**
    
    Visible particle size at maximum energy
    """

class File(ExtValue):
    """ Provides read/write access to the filesystem. Can be used in the experiment definition to save the experiment state (onExpSave) or any other information. Files are created in the "data/scripts_output" subdirectory, which is either near the Framsticks executable (if this subdirectory is writable) or in your user Documents directory. """

    name: str|ExtValue[str]
    path: str|ExtValue[str]
    """ **Full path** """
    info: str|ExtValue[str]
    """ **Information** """
    @staticmethod
    def writeNameObject(name: str|ExtValue[str], arg2: Object) -> None|ExtValue[None]:
        """ **Write object with an alternative name** """
        ...

    @staticmethod
    def writeObject(arg1: Object) -> None|ExtValue[None]:
        """ **Write object** """
        ...

    @staticmethod
    def writeObjectBegin(arg1: Object) -> None|ExtValue[None]:
        """ **Write object header** """
        ...

    @staticmethod
    def writeObjectField(arg1: Object, field_index_or_name: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ **Write single field** """
        ...

    @staticmethod
    def writeObjectFields(arg1: Object) -> None|ExtValue[None]:
        """ **Write all fields** """
        ...

    @staticmethod
    def writeObjectFieldForce(arg1: Object, field_index_or_name: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ **Write single field** """
        ...

    @staticmethod
    def writeObjectFieldsForce(arg1: Object) -> None|ExtValue[None]:
        """ **Write all fields** """
        ...

    @staticmethod
    def writeObjectEnd() -> None|ExtValue[None]:
        """ **Finish object** """
        ...

    @staticmethod
    def writeString(anything: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ **Write anything** """
        ...

    @staticmethod
    def writeComment(anything: str|ExtValue[str]) -> None|ExtValue[None]:
        """ **Write comment string** """
        ...

    @staticmethod
    def readLine() -> str|ExtValue[str]:
        """
        **Read line**
        
        Returns the next line read from file or null when there are no more lines.
        """
        ...

    @staticmethod
    def readObject(arg1: Object) -> None|ExtValue[None]:
        """ **Read object** """
        ...

    EOF: int|ExtValue[int]
    """ **End Of File?** """
    @staticmethod
    def readUntilEOF() -> str|ExtValue[str]:
        """ **Read everything** """
        ...

    @staticmethod
    def getContents(filename: str|ExtValue[str]) -> str|ExtValue[str]:
        """
        **Get file contents**
        
        Shortcut to: var f=File.open(filename); c=f.readUntilEOF(); f.close(); return c;
        """
        ...

    @staticmethod
    def create(filename: str|ExtValue[str], description: str|ExtValue[str]) -> File:
        """ **Create a new buffered file** """
        ...

    @staticmethod
    def createDirect(filename: str|ExtValue[str], description: str|ExtValue[str]) -> File:
        """
        **Create a new unbuffered disk file**
        
        Returns null if the file can't be created
        """
        ...

    @staticmethod
    def append(filename: str|ExtValue[str], description: str|ExtValue[str]) -> File:
        """ **Append buffered to the file** """
        ...

    @staticmethod
    def appendDirect(filename: str|ExtValue[str], description: str|ExtValue[str]) -> File:
        """
        **Append unbuffered to the disk file**
        
        Returns null if the file can't be appended
        """
        ...

    @staticmethod
    def flush() -> None|ExtValue[None]:
        """ Useful for unbuffered disk files only (openDirect, appendDirect) """
        ...

    @staticmethod
    def open(filename: str|ExtValue[str]) -> File:
        """
        **Open existing file for reading**
        
        Returns null if the file can't be read
        """
        ...

    stdin: File
    """ **Standard input** """
    stdout: File
    """ **Standard output** """
    @staticmethod
    def new() -> File:
        """ **Create a new memory file** """
        ...

    @staticmethod
    def newFromString(text: str|ExtValue[str]) -> File:
        """ **Create a new memory file with string contents** """
        ...

    @staticmethod
    def close() -> str|ExtValue[str]:
        """
        **Close the file**
        
        Returns file contents if it has been buffered.
        """
        ...

    @staticmethod
    def exists() -> int|ExtValue[int]:
        """
        **Test if a file exists**
        
        Example:\n
        File.exists("walking.gen") -> returns 0 or 1.
        """
        ...

    pathseparator: str|ExtValue[str]
    """ **Path separator: / or \\\\** """
    @staticmethod
    def callURL(url: str|ExtValue[str], post_data_or_null: Any|ExtValue[Any], callback_or_null: FunctionReference) -> Dictionary:

        ...


class FunctionReference(ExtValue):
    """
    Function reference objects are created using the 'function' operator. The referenced function can be called using the 'call' operator:
    
    	function abc(a,b)\n
    	{ return a+b; }
    
    	var f=function abc;\n
    	Simulator.print(typeof(f)); //"FunctionReference"\n
    	Simulator.print(call(f)(123,321)); //444
    """


class GenePool(metaclass=GenePoolIndexer):
    """
    GenePool objects are accessed by GenePools[index], or Genotype.genepool and created by GenePools.addGroup(). Usage of the static GenePool object is not recommended.\n
    You can iterate directly over Genotypes in the GenePool using for(...in...) loops:
    	for(var genotype in GenePools[0]) Simulator.print(genotype.name);
    
    See also: GenePools
    """

    name: str|ExtValue[str]
    """ **Group name** """
    index: int|ExtValue[int]
    """ **gene pool index** """
    size: int|ExtValue[int]
    """
    **Number of genotypes**
    
    In standard.expdef, this is equivalent to the number of unique genotypes. Standard experiment definition uses the Genotype.instances field to indicate that some genotypes exist in multiple instances despite having only one item in the group. Other experiment definitions may create multiple copies of the same genotype.
    """
    genotype_instances: int|ExtValue[int]
    """
    **Total number of genotype instances**
    
    A sum of Genotype.instances values of all Genotypes in this gene pool.
    """
    totalpop: int|ExtValue[int]
    """
    **Total number of genotype instances**
    
    Please use 'genotype_instances' instead of this field.
    """
    fitness: str|ExtValue[str]
    """
    **Fitness formula**
    
    (For advanced users)
    """
    fitness_is_valid: int|ExtValue[int]
    """
    **Fitness formula is valid**
    
    (valid means can be compiled)
    """
    fitness_step_limit: int|ExtValue[int]
    """
    **Fitness formula step limit**
    
    (For advanced users)
    """
    fitness_time_limit: float|ExtValue[float]
    """
    **Fitness formula time limit**
    
    (For advanced users)
    """
    fitness_allowed_objs: str|ExtValue[str]
    """
    **Fitness formula allowed objects**
    
    For advanced users: a list of comma-separated names of object classes allowed in the fitness formula. Empty list means that there are no restrictions and all object classes are allowed.
    """
    fitfun: int|ExtValue[int]
    """
    **Scale fitness?**
    
    Enables fitness scaling.
    """
    fitm: float|ExtValue[float]
    """
    **Shift coefficient**
    
    Lower threshold: how many standard deviations below average?\n
    (avg - n * stddev) - used for fitness shifting
    """
    fitma: float|ExtValue[float]
    """
    **Scaling coefficient**
    
    The best genotype is as many times\n
    better than the average one.
    """
    @staticmethod
    def get(index: int|ExtValue[int]) -> Genotype:
        """ **Get a Genotype object** """
        ...

    @staticmethod
    @deprecated
    def findGeno(arg1: Geno) -> int|ExtValue[int]:
        """
        **Find a Genotype index**
        
        Finds the Genotype whose genes are identical to the supplied Geno object.\n
        Returns the Genotype index or -1 if not found.\n
        Deprecated. Use the more versatile GenePool.findGenotype() instead of this function.
        """
        ...

    @staticmethod
    def findGenotype(Genotype_object_or_Geno_object_or_string_genotype: Any|ExtValue[Any]) -> Genotype:
        """
        **Find a Genotype**
        
        Finds the Genotype whose genes are identical to the supplied Genotype object, Geno object, or genotype string.\n
        Returns the Genotype object or null if not found.
        """
        ...

    @staticmethod
    def findUID(uid: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Find a Genotype by UID** """
        ...

    @staticmethod
    @deprecated
    def addGeno(arg1: Geno) -> Genotype:
        """
        **Make a Genotype from Geno**
        
        Creates a new Genotype from the supplied Geno object.\n
        Returns the created Genotype.\n
        Deprecated. Use the more versatile GenePool.add() instead of this function.
        """
        ...

    @staticmethod
    @deprecated
    def createFromGeno(arg1: Geno) -> Genotype:
        """
        same as addGeno (to comply with createFrom... convention)\n
        Deprecated. Use the more versatile GenePool.add() instead of this function.
        """
        ...

    @staticmethod
    @deprecated
    def createFromString(genotype: str|ExtValue[str]) -> Genotype:
        """
        Uses the supplied string argument.\n
        Deprecated. Use the more versatile GenePool.add() instead of this function.
        """
        ...

    @staticmethod
    def add(Geno_object_or_string_genotype: Any|ExtValue[Any]) -> Genotype:
        """
        **Add a genotype**
        
        Creates a new Genotype from the supplied Geno or string.\n
        Returns the created Genotype.
        """
        ...

    @staticmethod
    def worst() -> Genotype:
        """ Returns the genotype object having the lowest fitness. Unrated genotypes (with instances=0) are ranked lower than those having at least one instance. """
        ...

    @staticmethod
    def best() -> Genotype:
        """ Returns the genotype object having the highest fitness. Unrated genotypes (with instances=0) are ranked lower than those having at least one instance. """
        ...

    @staticmethod
    def random() -> Genotype:
        """ Returns a random genotype object disregarding fitness value, but taking into account 'instances'. Unrated genotypes (with instances=0) are treated as if they had instances=1. """
        ...

    @staticmethod
    def roulette() -> Genotype:
        """ Returns a randomly selected, fitness-proportional genotype object. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. """
        ...

    @staticmethod
    def revroulette() -> Genotype:
        """ Returns a randomly selected, reverse fitness-proportional genotype object. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. """
        ...

    @staticmethod
    def tournament(genotypes_in_tournament: int|ExtValue[int]) -> Genotype:
        """ Returns a tournament winner genotype object. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. """
        ...

    @staticmethod
    def randomLikeGeno(minimum_similarity: float|ExtValue[float], target: Geno) -> Genotype:
        """
        Returns a random genotype index similar to the target genotype. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. Read about details:\n
        https://www.framsticks.com/bib/Komosinski-et-al-2001\n
        https://www.framsticks.com/bib/Komosinski-and-Kubiak-2011\n
        https://www.framsticks.com/bib/Komosinski-2016
        """
        ...

    @staticmethod
    def rouletteLikeGeno(minimum_similarity: float|ExtValue[float], target: Geno) -> Genotype:
        """
        Returns a random genotype similar to the target genotype, fitness-proportional. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. Read about details:\n
        https://www.framsticks.com/bib/Komosinski-et-al-2001\n
        https://www.framsticks.com/bib/Komosinski-and-Kubiak-2011\n
        https://www.framsticks.com/bib/Komosinski-2016
        """
        ...

    @staticmethod
    def delete(genotype_object_or_index: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ Deletes a genotype. """
        ...

    @staticmethod
    def deleteOne(genotype_object_or_index: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ Deletes one individual, i.e. decreases its 'instances' and deletes the genotype if the 'instances' goes to 0. """
        ...

    @staticmethod
    def clear() -> None|ExtValue[None]:
        """ Delete all genotypes. GenePools[group].clear() is equivalent to GenePools.clearGroup(group) """
        ...

    @staticmethod
    def mergeInstances() -> None|ExtValue[None]:
        """
        **Merge instances**
        
        Merges instances of the same genotype.
        """
        ...

    @staticmethod
    def splitInstances() -> None|ExtValue[None]:
        """
        **Split instances**
        
        Splits genotype instances.
        """
        ...

    iterator: Object
    @staticmethod
    def getStatsMin(field_name: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **get stats minimum**
        
        Retrieves data from stats.* object. Can only be used for fields covered by stats.* (subset of Genotype fields).
        """
        ...

    @staticmethod
    def getStatsAvg(field_name: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **get stats average**
        
        Retrieves data from stats.* object. Can only be used for fields covered by stats.* (subset of Genotype fields).
        """
        ...

    @staticmethod
    def getStatsMax(field_name: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **get stats maximum**
        
        Retrieves data from stats.* object. Can only be used for fields covered by stats.* (subset of Genotype fields).
        """
        ...

    @staticmethod
    def refreshGUI() -> None|ExtValue[None]:
        """
        **Refresh GUI**
        
        Notify list content changed
        """
        ...


class GenePools(metaclass=GenePoolsIndexer):
    """
    Manages all genotypes in the experiment, organized in one or more groups.\n
    You can iterate directly over GenePool objects in the GenePools collection using for(...in...) loops:
    	for(var pool in GenePools) Simulator.print(pool.name);
    
    Before version 4.0rc4, some operations could only be performed on the "selected" genotype (the one pointed to by group/genotype fields in GenePools). Currently, the more convenient and recommended way is to call Genotype's or GenePool's functions that operate directly on the passed objects.
    
    The old way:
    	GenePools.newGenotype("X");\n
    	GenePools.mutateSelected();\n
    	Genotype.info="my favorite genotype";\n
    	GenePools.copySelected(0);
    
    Doing the same the new way:
    	var g=Genotype.newFromGeno(GenMan.mutate(Geno.newFromString("X")));\n
    	g.info="my favorite genotype";\n
    	g.moveTo(GenePools[0]);
    """

    group: int|ExtValue[int]
    """
    **selected group**
    
    Index of the currently selected group (GenePool).
    """
    size: int|ExtValue[int]
    """ **Number of groups** """
    genotype: int|ExtValue[int]
    """
    **selected genotype**
    
    Index of the currently selected genotype or -1 if no genotype is selected.
    """
    @staticmethod
    @deprecated
    def newGenotype(genotype: str|ExtValue[str]) -> None|ExtValue[None]:
        """ Makes a new genotype from the supplied string and select the genotype. The resulting genotype is stored in the static Genotype object detached from the genotype group. After calling this function GenePools.genotype is -1 indicating that no genotype from the group is selected. (call "copySelected" if you want to add this gentype to the genotype group). """
        ...

    @staticmethod
    @deprecated
    def deleteSelected() -> None|ExtValue[None]:
        """ Deletes selected genotype from the gene pool (uses the selected genotype object). """
        ...

    @staticmethod
    @deprecated
    def deleteOne(genotype_index: int|ExtValue[int]) -> None|ExtValue[None]:
        """ Deletes one individual from the gene pool = decreases 'instances' and deletes the genotype if the 'instances' goes to 0. """
        ...

    @staticmethod
    @deprecated
    def copySelected(groupindex: int|ExtValue[int]) -> None|ExtValue[None]:
        """ Copies the selected genotype to another group. """
        ...

    @staticmethod
    @deprecated
    def getFromCreature() -> None|ExtValue[None]:
        """ Copies a genotype from the selected creature. The resulting genotype is stored in the static Genotype object detached from the genotype group. """
        ...

    @staticmethod
    @deprecated
    def getFromCreatureObject(arg1: Creature) -> None|ExtValue[None]:
        """ Copies a genotype from the creature object passed in argument. The resulting genotype is stored in the static Genotype object detached from the genotype group. """
        ...

    @staticmethod
    @deprecated
    def addPerformanceFromCreature() -> None|ExtValue[None]:
        """ Updates the current Genotype's performance values merging them with the current Creture's performance. It assumes the Genotype.instances has a reasonable value and performs the proper weighting. Use your own function instead if these conditions are not met in your experiment. """
        ...

    @staticmethod
    @deprecated
    def mutateSelected() -> None|ExtValue[None]:
        """ Mutates the selected genotype. The resulting genotype is stored in the static Genotype object detached from the genotype group. After calling this function GenePools.genotype is -1 indicating that no genotype from the group is selected. """
        ...

    @staticmethod
    @deprecated
    def crossoverSelected(other_index: int|ExtValue[int]) -> None|ExtValue[None]:
        """ Crossovers the selected genotype with another one (from the genotype group). The resulting genotype is stored in the static Genotype object detached from the genotype group. After calling this function GenePools.genotype is -1 indicating that no genotype from the group is selected. """
        ...

    @staticmethod
    @deprecated
    def worst() -> int|ExtValue[int]:
        """ Gets the worst (lowest fitness) genotype index. Unrated genotypes (instances=0) are ranked lower than those having at least one instance. """
        ...

    @staticmethod
    @deprecated
    def random() -> int|ExtValue[int]:
        """ Gets random genotype index. """
        ...

    @staticmethod
    @deprecated
    def roulette() -> int|ExtValue[int]:
        """ Gets a randomly selected, fitness-proportional genotype index. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. """
        ...

    @staticmethod
    @deprecated
    def revroulette() -> int|ExtValue[int]:
        """ Gets a randomly selected, reverse fitness-proportional genotype index. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. """
        ...

    @staticmethod
    @deprecated
    def tournament(genotypes_in_tournament: int|ExtValue[int]) -> int|ExtValue[int]:
        """ Gets tournament winner genotype. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. """
        ...

    @staticmethod
    @deprecated
    def randomLikeThis(minimum_similarity: float|ExtValue[float]) -> int|ExtValue[int]:
        """ Gets a random genotype index similar to the selected one. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. """
        ...

    @staticmethod
    @deprecated
    def likeThisRoulette(minimum_similarity: float|ExtValue[float]) -> int|ExtValue[int]:
        """ Gets a random genotype similar to the selected one, fitness-proportional. Unrated genotypes (with instances=0) are treated as if they had instances=1 and average fitness. """
        ...

    @staticmethod
    @deprecated
    def findGenotype() -> int|ExtValue[int]:
        """
        Finds a genotype identical to the currently selected genotype. It is only useful when the currently selected genotype is not on the list of genotypes (for example it is a result of a genetic operator)\n
        Deprecated. Use the more versatile GenePool.findGenotype() instead of this function.
        """
        ...

    @staticmethod
    @deprecated
    def findGenotypeForCreature() -> int|ExtValue[int]:
        """
        Finds a genotype identical to the genotype of the selected Creature.\n
        Deprecated. Use the more versatile GenePool.findGenotype() instead of this function.
        """
        ...

    @staticmethod
    def addGroup(name: str|ExtValue[str]) -> GenePool:
        """ Adds a new gene pool. """
        ...

    @staticmethod
    def deleteGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """ Removes a gene pool. """
        ...

    @staticmethod
    def clear() -> None|ExtValue[None]:
        """ Removes all gene pools except the first one. """
        ...

    @staticmethod
    @deprecated
    def clearGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """ GenePools[group].clear() is more "object-oriented" than GenePools.clearGroup(group) """
        ...

    @staticmethod
    def get(index: int|ExtValue[int]) -> GenePool:

        ...

    iterator: Object

class GenMan(ExtValue):
    """ Manages various genetic operations, using appropriate operators for the argument genotype format. """

    gen_hist: int|ExtValue[int]
    """
    **Remember history of genetic operations**
    
    Required for phylogenetic analysis
    """
    gen_hilite: int|ExtValue[int]
    """
    **Use syntax highlighting**
    
    Use colors for genes?\n
    (slows down viewing/editing of huge genotypes)
    """
    gen_extmutinfo: int|ExtValue[int]
    """
    **Extended mutation info**
    
    If active, information about employed mutation method will be stored in the 'info' field of each mutated genotype.
    """
    @staticmethod
    def operReport() -> None|ExtValue[None]:
        """
        **Operators report**
        
        Show available genetic operators
        """
        ...

    @staticmethod
    def toHTML(genotype: str|ExtValue[str]) -> str|ExtValue[str]:
        """
        **HTMLize a genotype**
        
        returns genotype expressed as colored HTML
        """
        ...

    @staticmethod
    def toHTMLshort(genotype: str|ExtValue[str]) -> str|ExtValue[str]:
        """
        **HTMLize a genotype, shorten if needed**
        
        returns genotype (abbreviated if needed) in colored HTML format
        """
        ...

    @staticmethod
    def toLaTeX(genotype: str|ExtValue[str]) -> str|ExtValue[str]:
        """
        **LaTeXize a genotype**
        
        returns genotype in colored LaTeX format
        """
        ...

    @staticmethod
    def validate(genotype: Geno) -> Geno:
        """ returns validated (if possible) Geno object from supplied Geno """
        ...

    @staticmethod
    def mutate(genotype: Geno) -> Geno:
        """ returns mutated Geno object from supplied Geno """
        ...

    @staticmethod
    def crossOver(genotype1: Geno, genotype2: Geno) -> Geno:
        """ returns crossed over genotype """
        ...

    @staticmethod
    def getSimplest(format: str|ExtValue[str]) -> Geno:
        """
        **Get the simplest genotype**
        
        returns the simplest genotype for a given encoding (format). "0" means f0, "4" means f4, etc.
        """
        ...

    @staticmethod
    def _propertyClear() -> None|ExtValue[None]:
        """
        **Remove all properties**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAdd(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property (id,type,name,help)**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemove(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyChange(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Change property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAddGroup(name: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemoveGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyExists(name: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Check for property existence** """
        ...

    _property_changed_index: int|ExtValue[int]
    """ **Last changed property index** """
    _property_changed_id: str|ExtValue[str]
    """ **Last changed property id** """
    genoper_f0: int|ExtValue[int]
    """ **Operators for f0** """
    genoper_f0s: int|ExtValue[int]
    """ **Operators for f0s** """
    genoper_f1: int|ExtValue[int]
    """ **Operators for f1** """
    genoper_f4: int|ExtValue[int]
    """ **Operators for f4** """
    genoper_f8: int|ExtValue[int]
    """ **Operators for f8** """
    genoper_f9: int|ExtValue[int]
    """ **Operators for f9** """
    genoper_fF: int|ExtValue[int]
    """ **Operators for fF** """
    genoper_fn: int|ExtValue[int]
    """ **Operators for fn** """
    genoper_fB: int|ExtValue[int]
    """ **Operators for fB** """
    genoper_fH: int|ExtValue[int]
    """ **Operators for fH** """
    genoper_fL: int|ExtValue[int]
    """ **Operators for fL** """
    genoper_fS: int|ExtValue[int]
    """ **Operators for fS** """
    neuadd_N: int|ExtValue[int]
    """
    **Neuron (N)**
    
    Standard neuron
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       Inertia (in) float 0..1 (default 0.8)\n
       Force (fo) float 0..999 (default 0.04)\n
       Sigmoid (si) float -99999..99999 (default 2)\n
       State (s) float -1..1 (default 0)
    """
    neuadd_Nu: int|ExtValue[int]
    """
    **Unipolar neuron [EXPERIMENTAL!] (Nu)**
    
    Works like standard neuron (N) but the output value is scaled to 0...+1 instead of -1...+1.\n
    Having 0 as one of the saturation states should help in "gate circuits", where input signal is passed through or blocked depending on the other singal.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       Inertia (in) float 0..1 (default 0.8)\n
       Force (fo) float 0..999 (default 0.04)\n
       Sigmoid (si) float -99999..99999 (default 2)\n
       State (s) float -1..1 (default 0)
    """
    neuadd_G: int|ExtValue[int]
    """
    **Gyroscope (G)**
    
    Tilt sensor.\n
    Signal is proportional to sin(angle) = most sensitive in horizontal orientation.\n
    0=the stick is horizontal\n
    +1/-1=the stick is vertical
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Joint
    """
    neuadd_Gpart: int|ExtValue[int]
    """
    **Part Gyroscope (Gpart)**
    
    Tilt sensor. Signal is directly proportional to the tilt angle.\n
    0=the part X axis is horizontal\n
    +1/-1=the axis is vertical
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    neuadd_T: int|ExtValue[int]
    """
    **Touch (T)**
    
    Touch and proximity sensor (Tcontact and Tproximity combined)\n
    -1=no contact\n
    0=just touching\n
    >0=pressing, value depends on the force applied (not implemented in ODE mode)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       Range (r) float 0..1 (default 1)\n
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    neuadd_Tcontact: int|ExtValue[int]
    """
    **Touch contact (Tcontact)**
    
    Touch sensor.\n
    -1=no contact\n
    0=the Part is touching the obstacle\n
    >0=pressing, value depends on the force applied (not implemented in ODE mode)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    neuadd_Tproximity: int|ExtValue[int]
    """
    **Touch proximity (Tproximity)**
    
    Proximity sensor detecting obstacles along the X axis.\n
    -1=distance is "r" or more\n
    0=zero distance
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       Range (r) float 0..1 (default 1)\n
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    neuadd_S: int|ExtValue[int]
    """
    **Smell (S)**
    
    Smell sensor. Aggregated "smell of energy" experienced from all energy objects (creatures and food pieces).\n
    Close objects have bigger influence than the distant ones: for each energy source, its partial feeling is proportional to its energy/(distance^2)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    neuadd_Constant: int|ExtValue[int]
    """
    **Constant (*)**
    
    Constant value
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_Bend_muscle: int|ExtValue[int]
    """
    **Bend muscle (|)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 0.25)\n
       bending range (r) float 0..1 (default 1)
    """
    neuadd_Rotation_muscle: int|ExtValue[int]
    """
    **Rotation muscle (@)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 1)
    """
    neuadd_M: int|ExtValue[int]
    """
    **Muscle for solids (M)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 1)\n
       axis (a) integer 0..1 (default 0)
    """
    neuadd_D: int|ExtValue[int]
    """
    **Differentiate (D)**
    
    Calculate the difference between the current and previous input value. Multiple inputs are aggregated with respect to their weights
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_Fuzzy: int|ExtValue[int]
    """
    **Fuzzy system [EXPERIMENTAL!] (Fuzzy)**
    
    Refer to publications to learn more about this neuron.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       number of fuzzy sets (ns) integer\n
       number of rules (nr) integer\n
       fuzzy sets (fs) string (default "")\n
       fuzzy rules (fr) string (default "")
    """
    neuadd_VEye: int|ExtValue[int]
    """
    **Vector Eye [EXPERIMENTAL!] (VEye)**
    
    Refer to publications to learn more about this neuron.
    
    Characteristics:
       uses single input\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       target.x (tx) float\n
       target.y (ty) float\n
       target.z (tz) float\n
       target shape (ts) string (default "")\n
       perspective (p) float 0.1..10 (default 1)\n
       scale (s) float 0.1..100 (default 1)\n
       show hidden lines (h) integer 0..1 (default 0)\n
       output lines count (each line needs four channels) (o) integer 0..99 (default 0)\n
       debug (d) integer 0..1 (default 0)
    """
    neuadd_VMotor: int|ExtValue[int]
    """
    **Visual-Motor Cortex [EXPERIMENTAL!] (VMotor)**
    
    Must be connected to the VEye and properly set up. Refer to publications to learn more about this neuron.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       number of basic features (noIF) integer\n
       number of degrees of freedom (noDim) integer\n
       parameters (params) string
    """
    neuadd_Sti: int|ExtValue[int]
    """
    **Sticky [EXPERIMENTAL!] (Sti)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Part
    """
    neuadd_LMu: int|ExtValue[int]
    """
    **Linear muscle [EXPERIMENTAL!] (LMu)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0.01..1 (default 1)
    """
    neuadd_Water: int|ExtValue[int]
    """
    **Water detector (Water)**
    
    Output signal:\n
    0=on or above water surface\n
    1=under water (deeper than 1)\n
    0..1=in the transient area just below water surface
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    neuadd_Energy: int|ExtValue[int]
    """
    **Energy level (Energy)**
    
    The current energy level divided by the initial energy level.\n
    Usually falls from initial 1.0 down to 0.0 and then the creature dies. It can rise above 1.0 if enough food is ingested
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_Ch: int|ExtValue[int]
    """
    **Channelize (Ch)**
    
    Combines all input signals into a single multichannel output; Note: ChSel and ChMux are the only neurons which support multiple channels. Other neurons discard everything except the first channel.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_ChMux: int|ExtValue[int]
    """
    **Channel multiplexer (ChMux)**
    
    Outputs the selected channel from the second (multichannel) input. The first input is used as the selector value (-1=select first channel, .., 1=last channel)
    
    Characteristics:
       uses 2 inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_ChSel: int|ExtValue[int]
    """
    **Channel selector (ChSel)**
    
    Outputs a single channel (selected by the "ch" parameter) from multichannel input
    
    Characteristics:
       uses single input\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       channel (ch) integer
    """
    neuadd_Rnd: int|ExtValue[int]
    """
    **Random noise (Rnd)**
    
    Generates random noise (subsequent random values in the range of -1..+1)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_Sin: int|ExtValue[int]
    """
    **Sinus generator (Sin)**
    
    Output frequency = f0+input
    
    Characteristics:
       uses single input\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       base frequency (f0) float -1..1 (default 0.0628319)\n
       time (t) float 0..6.28319 (default 0)
    """
    f0_nodel_tag: int|ExtValue[int]
    """
    **Respect the 'delete inhibit' tag**
    
    You can tag elements using their 'i' field and the i="mi=d" tag.\n
    Mutations will not delete such elements.\n
    The i="mi=dm" combination is allowed.
    """
    f0_nomod_tag: int|ExtValue[int]
    """
    **Respect the 'modify inhibit' tag**
    
    You can tag elements using their 'i' field and the i="mi=m" tag.\n
    Mutations will not modify properties of such elements.\n
    The i="mi=md" combination is allowed.
    """
    f0_p_new: float|ExtValue[float]
    """ **New part** """
    f0_p_del: float|ExtValue[float]
    """ **Delete part** """
    f0_p_swp: float|ExtValue[float]
    """ **Swap parts** """
    f0_p_pos: float|ExtValue[float]
    """ **Position** """
    f0_p_den: float|ExtValue[float]
    """
    **Density**
    
    Density only has an influence under water
    """
    f0_p_frc: float|ExtValue[float]
    """ **Friction** """
    f0_p_ing: float|ExtValue[float]
    """ **Ingestion** """
    f0_p_asm: float|ExtValue[float]
    """
    **Assimilation**
    
    The interpretation and influence of this property must be implemented by the experiment definition
    """
    f0_p_color: float|ExtValue[float]
    """
    **Visual only: color**
    
    If this value is above zero, apart from this mutation occurring, the color of every newly created gray Part will be mutated on creation
    """
    f0_j_new: float|ExtValue[float]
    """ **New joint** """
    f0_j_del: float|ExtValue[float]
    """ **Delete joint** """
    f0_j_stm: float|ExtValue[float]
    """
    **Stamina**
    
    The interpretation and influence of this property must be implemented by the experiment definition
    """
    f0_j_stf: float|ExtValue[float]
    """ **Stiffness** """
    f0_j_rsf: float|ExtValue[float]
    """ **Rotational stiffness** """
    f0_j_color: float|ExtValue[float]
    """
    **Visual only: color**
    
    If this value is above zero, apart from this mutation occurring, every newly created Joint will be assigned a color that is the average color of both joined Parts
    """
    f0_n_new: float|ExtValue[float]
    """ **New neuron** """
    f0_n_del: float|ExtValue[float]
    """ **Delete neuron** """
    f0_n_prp: float|ExtValue[float]
    """ **Change properties** """
    f0_c_new: float|ExtValue[float]
    """ **New connection** """
    f0_c_del: float|ExtValue[float]
    """ **Delete connection** """
    f0_c_wei: float|ExtValue[float]
    """ **Change weight** """
    f0s_nodel_tag: int|ExtValue[int]
    """
    **Respect the 'delete inhibit' tag**
    
    You can tag elements using their 'i' field and the i="mi=d" tag.\n
    Mutations will not delete such elements.\n
    The i="mi=dm" combination is allowed.
    """
    f0s_nomod_tag: int|ExtValue[int]
    """
    **Respect the 'modify inhibit' tag**
    
    You can tag elements using their 'i' field and the i="mi=m" tag.\n
    Mutations will not modify properties of such elements.\n
    The i="mi=md" combination is allowed.
    """
    f0s_circle_section: int|ExtValue[int]
    """
    **Ensure circle section**
    
    Ensure that ellipsoids and cylinders have circle cross-section
    """
    f0s_use_elli: int|ExtValue[int]
    """ **Use ellipsoids in mutations** """
    f0s_use_cub: int|ExtValue[int]
    """ **Use cuboids in mutations** """
    f0s_use_cyl: int|ExtValue[int]
    """ **Use cylinders in mutations** """
    f0s_p_new: float|ExtValue[float]
    """ **New part** """
    f0s_p_del: float|ExtValue[float]
    """ **Delete part** """
    f0s_p_swp: float|ExtValue[float]
    """ **Swap parts** """
    f0s_p_pos: float|ExtValue[float]
    """ **Position** """
    f0s_p_rot: float|ExtValue[float]
    """ **Rotation** """
    f0s_p_scale: float|ExtValue[float]
    """ **Size (precisely, 'scale')** """
    f0s_p_frc: float|ExtValue[float]
    """ **Friction** """
    f0s_p_ing: float|ExtValue[float]
    """ **Ingestion** """
    f0s_p_asm: float|ExtValue[float]
    """
    **Assimilation**
    
    The interpretation and influence of this property must be implemented by the experiment definition
    """
    f0s_p_color: float|ExtValue[float]
    """
    **Visual only: color**
    
    If this value is above zero, apart from this mutation occurring, the color of every newly created gray Part will be mutated on creation
    """
    f0s_j_new: float|ExtValue[float]
    """ **New joint** """
    f0s_j_del: float|ExtValue[float]
    """ **Delete joint** """
    f0s_j_stm: float|ExtValue[float]
    """
    **Stamina**
    
    The interpretation and influence of this property must be implemented by the experiment definition
    """
    f0s_j_color: float|ExtValue[float]
    """
    **Visual only: color**
    
    If this value is above zero, apart from this mutation occurring, every newly created Joint will be assigned a color that is the average color of both joined Parts
    """
    f0s_n_new: float|ExtValue[float]
    """ **New neuron** """
    f0s_n_del: float|ExtValue[float]
    """ **Delete neuron** """
    f0s_n_prp: float|ExtValue[float]
    """ **Change properties** """
    f0s_c_new: float|ExtValue[float]
    """ **New connection** """
    f0s_c_del: float|ExtValue[float]
    """ **Delete connection** """
    f0s_c_wei: float|ExtValue[float]
    """ **Change weight** """
    f1_xo_propor: int|ExtValue[int]
    """
    **Proportional crossover**
    
    Cross over (exchange) corresponding segments of the two parent genotypes?
    
    f1 uses a two-point crossing over.\n
    If this option is turned on, cut points will be selected proportionally to neural genes in both parents, and a similar number of characters will be exchanged if possible.\n
    Thus, if both parents have the same number of neurons, then this will be preserved in their children.
    """
    f1_smX: float|ExtValue[float]
    """ **Add/remove a stick X** """
    f1_smJunct: float|ExtValue[float]
    """ **Add/remove a branch ( )** """
    f1_smComma: float|ExtValue[float]
    """ **Add/remove a comma ,** """
    f1_smModif: float|ExtValue[float]
    """
    **Add/remove a modifier**
    
    Modifiers: LlRrCcQqFfMmEeWwSsAaIiDdGgBb
    """
    f1_smModifiers: str|ExtValue[str]
    """
    **Allowed modifiers**
    
    Modifier symbols that will be added or deleted during mutation\n
    (from the full set: LlRrCcQqFfMmEeWwSsAaIiDdGgBb).
    
    You may use the extended syntax: after every allowed symbol, you may include its probability value in parentheses.\n
    Without parentheses, all allowed symbols behave as if they had (1.0) appended.\n
    If you include (0.0) after a symbol, this bans that symbol as if it was not present in this string.
    """
    f1_nmNeu: float|ExtValue[float]
    """
    **Add/remove a neuron**
    
    Adds a (connected) neuron or removes a neuron
    """
    f1_nmConn: float|ExtValue[float]
    """ **Add/remove neural connection** """
    f1_nmProp: float|ExtValue[float]
    """ **Add/remove neuron property setting** """
    f1_nmWei: float|ExtValue[float]
    """ **Change connection weight** """
    f1_nmVal: float|ExtValue[float]
    """ **Change property value** """
    f4_mut_add: float|ExtValue[float]
    """
    **Add node**
    
    Mutation: probability of adding a node
    """
    f4_mut_add_div: float|ExtValue[float]
    """
    **- add division**
    
    Add node mutation: probability of adding a division
    """
    f4_mut_add_conn: float|ExtValue[float]
    """
    **- add connection**
    
    Add node mutation: probability of adding a neural connection
    """
    f4_mut_add_neupar: float|ExtValue[float]
    """
    **- add neuron property**
    
    Add node mutation: probability of adding a neuron property/modifier
    """
    f4_mut_add_rep: float|ExtValue[float]
    """
    **- add repetition '#'**
    
    Add node mutation: probability of adding the '#' repetition gene
    """
    f4_mut_add_simp: float|ExtValue[float]
    """
    **- add simple node**
    
    Add node mutation: probability of adding a random, simple gene
    """
    f4_mut_del: float|ExtValue[float]
    """
    **Delete node**
    
    Mutation: probability of deleting a node
    """
    f4_mut_mod: float|ExtValue[float]
    """
    **Modify node**
    
    Mutation: probability of changing a node
    """
    f4_mut_modneu_conn: float|ExtValue[float]
    """
    **- neuron input: modify source**
    
    Neuron input mutation: probability of changing its source neuron
    """
    f4_mut_modneu_weight: float|ExtValue[float]
    """
    **- neuron input: modify weight**
    
    Neuron input mutation: probability of changing its weight
    """
    f4_mut_max_rep: int|ExtValue[int]
    """
    **Maximum number for '#' repetitions**
    
    Maximum allowed number of repetitions for the '#' repetition gene
    """
    f4_mut_modifiers: str|ExtValue[str]
    """
    **Allowed modifiers**
    
    Modifier symbols that will be added or deleted during mutation\n
    (from the full set: LlRrCcQqFfMmEeWwSsAaIiDdGgBb).
    
    You may use the extended syntax: after every allowed symbol, you may include its probability value in parentheses.\n
    Without parentheses, all allowed symbols behave as if they had (1.0) appended.\n
    If you include (0.0) after a symbol, this bans that symbol as if it was not present in this string.
    """
    f8_mut_chg_begin_arg: float|ExtValue[float]
    """
    **Change beginning argument**
    
    mutation: probability of changing a beginning argument
    """
    f8_mut_chg_arg: float|ExtValue[float]
    """
    **Change argument**
    
    mutation: probability of changing a production's argument
    """
    f8_mut_del_comm: float|ExtValue[float]
    """
    **Delete command**
    
    mutation: probability of deleting a command
    """
    f8_mut_insert_comm: float|ExtValue[float]
    """
    **Insert commands**
    
    mutation: probability of inserting commands
    """
    f8_mut_enc: float|ExtValue[float]
    """
    **Encapsulate commands**
    
    mutation: probability of encapsulating commands
    """
    f8_mut_chg_cond_sign: float|ExtValue[float]
    """
    **Change condition sign**
    
    mutation: probability of changing a condition sign
    """
    f8_mut_add_param: float|ExtValue[float]
    """
    **Add parameter**
    
    mutation: probability of adding a parameter to the production
    """
    f8_mut_add_cond: float|ExtValue[float]
    """
    **Add condition**
    
    mutation: probability of adding a condition to the subproduction
    """
    f8_mut_add_subprod: float|ExtValue[float]
    """
    **Add subproduction**
    
    mutation: probability of adding a subproduction
    """
    f8_mut_chg_iter_number: float|ExtValue[float]
    """
    **Change iteration number**
    
    mutation: probability of changing a number of iterations
    """
    f8_mut_del_param: float|ExtValue[float]
    """
    **Delete parameter**
    
    mutation: probability of deleting a parameter
    """
    f8_mut_del_cond: float|ExtValue[float]
    """
    **Delete condition**
    
    mutation: probability of deleting a condition
    """
    f8_mut_add_loop: float|ExtValue[float]
    """
    **Add loop**
    
    mutation: probability of adding a loop
    """
    f8_mut_del_loop: float|ExtValue[float]
    """
    **Delete loop**
    
    mutation: probability of deleting a loop
    """
    f8_mut_del_prod: float|ExtValue[float]
    """
    **Delete production**
    
    mutation: probability of deleting a production
    """
    f9_mut: float|ExtValue[float]
    """
    **Mutation intensity**
    
    How many genes (letters) should be changed during a single genotype mutation (1=all genes, 0.1=ten percent, 0=one gene)
    """
    fF_xover: float|ExtValue[float]
    """
    **Inherited in linear mix crossover**
    
    0.5 => children are averaged parents.\n
    0.8 => children are only 20% different from parents.\n
    1.0 => each child is identical to one parent (no crossover).
    """
    fn_xover: float|ExtValue[float]
    """
    **Fraction inherited in linear mix crossover**
    
    0.5 => children are averaged parents.\n
    0.8 => children are only 20% different from parents.\n
    1.0 => each child is identical to one parent (no crossover).
    """
    fn_xover_random: int|ExtValue[int]
    """
    **Random fraction inherited in crossover**
    
    If active, the amount of linear mix is random in each crossover operation, so the "Fraction inherited in linear mix crossover" parameter is ignored.
    """
    fn_mut_bound_low: str|ExtValue[str]
    """
    **Lower bounds for mutation**
    
    A vector of lower bounds (one real value for each variable)
    """
    fn_mut_bound_high: str|ExtValue[str]
    """
    **Higher bounds for mutation**
    
    A vector of higher bounds (one real value for each variable)
    """
    fn_mut_stddev: str|ExtValue[str]
    """
    **Standard deviations for mutation**
    
    A vector of standard deviations (one real value for each variable)
    """
    fn_mut_single_var: int|ExtValue[int]
    """
    **Mutate only a single variable**
    
    If active, only a single randomly selected variable will be mutated in each mutation operation. Otherwise all variables will be mutated.
    """
    fB_mut_substitute: float|ExtValue[float]
    """
    **Substitution**
    
    Relative probability of changing a single random character (or a neuron) in the genotype
    """
    fB_mut_insert: float|ExtValue[float]
    """
    **Insertion**
    
    Relative probability of inserting a random character in a random place of the genotype
    """
    fB_mut_insert_neuron: float|ExtValue[float]
    """
    **Insertion of a neuron**
    
    Relative probability of inserting a neuron in a random place of genotype
    """
    fB_mut_delete: float|ExtValue[float]
    """
    **Deletion**
    
    Relative probability of deleting a random character (or a neuron) in the genotype
    """
    fB_mut_duplicate: float|ExtValue[float]
    """
    **Duplication**
    
    Relative probability of copying a single *gene* of the genotype and appending it to the beginning of this genotype
    """
    fB_mut_translocate: float|ExtValue[float]
    """
    **Translocation**
    
    Relative probability of swapping two substrings in the genotype
    """
    fB_cross_gene_transfer: float|ExtValue[float]
    """
    **Horizontal gene transfer**
    
    Relative probability of crossing over by copying a single random gene from each parent to the beginning of the other parent
    """
    fB_cross_crossover: float|ExtValue[float]
    """
    **Crossing over**
    
    Relative probability of crossing over by a random distribution of genes from both parents to both children
    """
    fH_mut_addition: float|ExtValue[float]
    """
    **Add element**
    
    Probability of adding a new element
    """
    fH_mut_add_joint: float|ExtValue[float]
    """
    **- add joint**
    
    Probability of adding a new stick handle
    """
    fH_mut_add_neuron: float|ExtValue[float]
    """
    **- add neuron**
    
    Probability of adding a new neuron handle
    """
    fH_mut_add_connection: float|ExtValue[float]
    """
    **- add neural connection**
    
    Probability of adding a new neuron connection handle
    """
    fH_mut_deletion: float|ExtValue[float]
    """
    **Delete element**
    
    Probability of removing an element
    """
    fH_mut_handle: float|ExtValue[float]
    """
    **Modify vectors of handles**
    
    Probability of changing values in vectors of a handle
    """
    fH_mut_property: float|ExtValue[float]
    """
    **Modify properties of handles**
    
    Probability of changing properties of handles
    """
    fL_maxdefinedwords: int|ExtValue[int]
    """
    **Maximum number of defined words**
    
    Maximum number of words that can be defined in the L-System
    """
    fL_axm_mut_prob: float|ExtValue[float]
    """
    **Axiom mutation**
    
    Probability of performing mutation operations on axiom
    """
    fL_rul_mut_prob: float|ExtValue[float]
    """
    **Rule's successor mutation**
    
    Probability of performing mutation operations on the successor of a random rule
    """
    fL_mut_addition: float|ExtValue[float]
    """
    **Addition of a word to a sequence**
    
    Probability of adding a random existing word to the axiom or to one of successors
    """
    fL_mut_add_stick: float|ExtValue[float]
    """
    **- addition of a stick**
    
    Probability of adding a stick
    """
    fL_mut_add_neuro: float|ExtValue[float]
    """
    **- addition of a neuron**
    
    Probability of adding a neuron
    """
    fL_mut_add_conn: float|ExtValue[float]
    """
    **- addition of a neuron connection**
    
    Probability of adding a neuron connection
    """
    fL_mut_add_rot: float|ExtValue[float]
    """
    **- addition of rotation words**
    
    Probability of adding one of rotation words
    """
    fL_mut_add_branch: float|ExtValue[float]
    """
    **- addition of a branched stick**
    
    Probability of adding a branch with a rotation and a stick
    """
    fL_mut_add_other: float|ExtValue[float]
    """
    **- addition of defined words**
    
    Probability of adding another word defined in the genotype
    """
    fL_mut_worddefaddition: float|ExtValue[float]
    """
    **Addition of a new word definition**
    
    Probability of adding a new word definition to the genotype
    """
    fL_mut_ruleaddition: float|ExtValue[float]
    """
    **Addition of a new rule definition**
    
    Probability of adding a new rule definition for an existing word
    """
    fL_mut_rulecond: float|ExtValue[float]
    """
    **Modification of a rule condition**
    
    Probability of modifying a random rule condition
    """
    fL_mut_changeword: float|ExtValue[float]
    """
    **Change a random word**
    
    Probability of changing a word name or a formula of a random word from an axiom or one of successors
    """
    fL_mut_changeword_formula: float|ExtValue[float]
    """
    **- change of a formula**
    
    Probability of changing a formula in a word
    """
    fL_mut_changeword_name: float|ExtValue[float]
    """
    **- change of a name**
    
    Probability of changing a name in a word
    """
    fL_mut_changeiter: float|ExtValue[float]
    """
    **Change the number of iterations**
    
    Probability of changing the number of iterations of the L-System
    """
    fL_mut_changeiter_step: float|ExtValue[float]
    """
    **Step of the iteration change**
    
    The minimal step that should be used for changing iterations in the L-System
    """
    fL_mut_deletion: float|ExtValue[float]
    """
    **Deletion of a random word**
    
    Probability of deleting a random word from an axiom or a random successor (also deletes the rule if there is only one word in the successor)
    """
    fS_mut_add_part: float|ExtValue[float]
    """
    **Add part**
    
    mutation: probability of adding a part
    """
    fS_mut_rem_part: float|ExtValue[float]
    """
    **Remove part**
    
    mutation: probability of deleting a part
    """
    fS_mut_mod_part: float|ExtValue[float]
    """
    **Modify part**
    
    mutation: probability of changing the part type
    """
    fS_mut_change_joint: float|ExtValue[float]
    """
    **Change joint**
    
    mutation: probability of changing a joint
    """
    fS_mut_add_param: float|ExtValue[float]
    """
    **Add param**
    
    mutation: probability of adding a parameter
    """
    fS_mut_rem_param: float|ExtValue[float]
    """
    **Remove param**
    
    mutation: probability of removing a parameter
    """
    fS_mut_mod_param: float|ExtValue[float]
    """
    **Modify param**
    
    mutation: probability of modifying a parameter
    """
    fS_mut_mod_mod: float|ExtValue[float]
    """
    **Modify modifier**
    
    mutation: probability of modifying a modifier
    """
    fS_mut_add_neuro: float|ExtValue[float]
    """
    **Add neuron**
    
    mutation: probability of adding a neuron
    """
    fS_mut_rem_neuro: float|ExtValue[float]
    """
    **Remove neuron**
    
    mutation: probability of removing a neuron
    """
    fS_mut_mod_neuro_conn: float|ExtValue[float]
    """
    **Modify neuron connection**
    
    mutation: probability of changing a neuron connection
    """
    fS_mut_add_neuro_conn: float|ExtValue[float]
    """
    **Add neuron connection**
    
    mutation: probability of adding a neuron connection
    """
    fS_mut_rem_neuro_conn: float|ExtValue[float]
    """
    **Remove neuron connection**
    
    mutation: probability of removing a neuron connection
    """
    fS_mut_mod_neuro_params: float|ExtValue[float]
    """
    **Modify neuron params**
    
    mutation: probability of changing a neuron param
    """
    fS_circle_section: int|ExtValue[int]
    """
    **Ensure circle section**
    
    Ensure that ellipsoids and cylinders have circle cross-section
    """
    fS_use_elli: int|ExtValue[int]
    """
    **Use ellipsoids in mutations**
    
    Use ellipsoids in mutations
    """
    fS_use_cub: int|ExtValue[int]
    """
    **Use cuboids in mutations**
    
    Use cuboids in mutations
    """
    fS_use_cyl: int|ExtValue[int]
    """
    **Use cylinders in mutations**
    
    Use cylinders in mutations
    """
    fS_mut_add_part_strong: int|ExtValue[int]
    """
    **Strong add part mutation**
    
    Add part mutation will produce more parametrized parts
    """

class GenManStats(ExtValue):
    """ Statistics for genetic operations. """

    gen_count: int|ExtValue[int]
    """ **Number of genetic operations so far** """
    gen_mvalid: int|ExtValue[int]
    """ **Mutations valid** """
    gen_mvalidated: int|ExtValue[int]
    """ **Mutations validated** """
    gen_minvalid: int|ExtValue[int]
    """
    **Mutations invalid**
    
    couldn't be repaired
    """
    gen_mfailed: int|ExtValue[int]
    """
    **Mutations failed**
    
    couldn't be performed
    """
    gen_xovalid: int|ExtValue[int]
    """ **Crossovers valid** """
    gen_xovalidated: int|ExtValue[int]
    """ **Crossovers validated** """
    gen_xoinvalid: int|ExtValue[int]
    """
    **Crossovers invalid**
    
    couldn't be repaired
    """
    gen_xofailed: int|ExtValue[int]
    """
    **Crossovers failed**
    
    couldn't be performed
    """
    gen_mutimpr: float|ExtValue[float]
    """
    **Mutations total effect**
    
    total cumulative mutation change
    """
    gen_xoimpr: float|ExtValue[float]
    """
    **Crossovers total effect**
    
    total cumulative crossover change
    """
    @staticmethod
    def clrstats() -> None|ExtValue[None]:
        """ **Clear stats and history** """
        ...


class Geno(ExtValue):
    """
    All information about a single genotype.\n
    This is a genetics-only object which does not contain any performance data. See also: Genotype class
    """

    name: str|ExtValue[str]
    rawgenotype: str|ExtValue[str]
    """
    **Raw genotype**
    
    Genotype, excluding the format specifier
    """
    info: str|ExtValue[str]
    """ Additional information or comments """
    format: str|ExtValue[str]
    """ Genotype format """
    genotype: str|ExtValue[str]
    """ Genes as a string of characters """
    isValid: int|ExtValue[int]
    """
    **Valid**
    
    Use 'is_valid' instead of 'isValid'.
    """
    is_valid: int|ExtValue[int]
    """
    **Validity**
    
    0 = invalid genotype\n
    1 = valid genotype\n
    -1 = validity is not known. This is a transient state. The value of "is_valid" will never be -1 when read. It is safe to treat is_valid as boolean in statements like "if (g.is_valid) ...". Setting "is_valid=-1" will make it 0 or 1 again. This third state (-1) is only needed for loading Genotype objects from files where the "is_valid" field might not be present.
    """
    @staticmethod
    def getConverted(format: str|ExtValue[str]) -> Geno:
        """ **Get converted genotype** """
        ...

    @staticmethod
    def getConvertedWithCheckpoints(format: str|ExtValue[str]) -> Geno:
        """
        **Get converted genotype**
        
        See also Model.newWithCheckpoints()
        """
        ...

    f0genotype: str|ExtValue[str]
    """
    **f0 genotype**
    
    converted to f0 genotype
    """
    @staticmethod
    def new() -> Geno:
        """ **create new empty object** """
        ...

    @staticmethod
    def newFromString(genotype: str|ExtValue[str]) -> Geno:
        """ **create new object from supplied string argument** """
        ...

    @staticmethod
    def newFrom(genotype: str|ExtValue[str], format: str|ExtValue[str], name: str|ExtValue[str], description: str|ExtValue[str]) -> Geno:
        """ **create new object** """
        ...

    autoname: str|ExtValue[str]
    """ **Autogenerated name** """
    toVector: Vector
    """ **serialization support** """
    @staticmethod
    def newFromVector(arg1: Vector) -> Geno:
        """ **serialization support** """
        ...


class GenoConverters(ExtValue):
    """ Converters between genetic formats """

    genoconv_f1_f0: int|ExtValue[int]
    """ **f1 --> f0  :  Recursive encoding** """
    genoconv_f4_f0: int|ExtValue[int]
    """ **f4 --> f0  :  Developmental encoding** """
    genoconv_f8_f1: int|ExtValue[int]
    """ **f8 --> f1  :  (Old) generative encoding** """
    genoconv_f9_f0: int|ExtValue[int]
    """ **f9 --> f0  :  Turtle3D-ortho encoding** """
    genoconv_fF_f0s: int|ExtValue[int]
    """ **fF --> f0s  :  10-parameter Foraminifera encoding** """
    genoconv_fn_f0: int|ExtValue[int]
    """ **fn --> f0  :  Vector of real values, no phenotype** """
    genoconv_fB_fH: int|ExtValue[int]
    """ **fB --> fH  :  Biological encoding** """
    genoconv_fH_f0: int|ExtValue[int]
    """ **fH --> f0  :  Similarity encoding** """
    genoconv_fL_f0: int|ExtValue[int]
    """ **fL --> f0  :  L-System encoding** """
    genoconv_fS_f0s: int|ExtValue[int]
    """ **fS --> f0s  :  Solids tree-structure encoding** """
    conv_f1_f0_modcompat: int|ExtValue[int]
    """
    **Modifier compatibility**
    
    The modern implementation makes the influence of modifiers more consistent and uniform, and the extreme property values are easier to reach with a lower number of characters, which improves the topology for evolutionary search.\n
    Previous implementation can be enabled for compatibility, for example when you want to test old genotypes.
    """
    conv_f1_f0_cq_influence: int|ExtValue[int]
    """
    **'C' and 'Q' modifier influence**
    
    'C' and 'Q' modifier semantics was changed in June 2023. Previously they did not affect the stick immediately following the current sequence of modifiers. In the modern implementation, all modifiers consistently start their influence at the very next stick that is being created in the current branch.\n
    Example:\n
    In the old interpretation of 'XcXX', only the last stick is rotated, because 'c' starts its influence at the stick that occurs after the current stick. In the modern implementation, the same effect is achieved with 'XXcX', where 'c' immediately bends the first 'X' that appears after it.\n
    Previous implementation can be enabled for compatibility, for example when you want to test old genotypes.
    """
    conv_f1_f0_branch_muscle_range: int|ExtValue[int]
    """
    **Bending muscle default range**
    
    Determines how the bending muscle default turning range is limited when the muscle is controlling a stick growing from a branching point that has 'NumberOfBranches' sticks separated by commas. The motivation of the limited range is to keep the neighboring sticks from intersecting when they are bent by muscles. This constraint may degrade the performance (e.g. velocity) of creatures, but this default value can be overridden by providing a specific range property value for the '|' muscle neuron in the genotype.\n
    - Full/NumberOfBranches - a compromise between the two other settings.\n
    - Full/(NumberOfBranches+1) - because the originating stick also counts as a branch. This setting guarantees that in the worst case, when at least two neighboring branches have sticks controlled by bending muscles and their controlling signals are at extreme values, the sticks can touch and overlap, but will not intersect. This setting is in most cases too strict because (1) all branches are very rarely controlled by muscles, (2) there are often 'empty' branches - multiple commas with no sticks in-between, and (3) the share of the originating stick is effectively wasted because this stick itself has no muscle at the branching point so it will not bend; the muscle bending range is symmetrical and the default range is equal for all muscles in a branching, but the sticks equipped with muscles in a branching are rarely evenly spaced.\n
    - Full: always the complete angle - because we do not have to care about the physical plausibility and avoid intersecting sticks, and other genetic representations do not impose such constraints, so this full angle setting can be useful as the default bending range when comparing the performance of various genetic encodings.
    """
    conv_f8_f1_maxlen: int|ExtValue[int]
    """
    **Maximal genotype length**
    
    Maximal length of the resulting f1 genotype, in characters. If the f8 L-system produces longer f1 genotype, it will be considered invalid.
    """

class Genotype(ExtValue):
    """ A Genotype with the associated performance information. Adding genotypes to GenePool makes them accessible in Framsticks GUI and enables the use of GenePool selection methods. See also GenePools. """

    name: str|ExtValue[str]
    genotype: str|ExtValue[str]
    """ Genes as a string of characters. """
    info_timestamp: float|ExtValue[float]
    """ **Last modified** """
    info_author: str|ExtValue[str]
    """ **Author name** """
    info_author_ispublic: int|ExtValue[int]
    """ **Author name is public** """
    info_email: str|ExtValue[str]
    """ **Author email** """
    info_email_ispublic: int|ExtValue[int]
    """ **Author email is public** """
    info: str|ExtValue[str]
    """
    **Description**
    
    Short description of key features of this creature.
    """
    info_origin: int|ExtValue[int]
    """
    **Origin**
    
    Declaration of how this genotype originated.
    """
    info_how_created: str|ExtValue[str]
    """
    **How created**
    
    Description of the process of designing and/or evolving this genotype.
    """
    info_performance: str|ExtValue[str]
    """
    **Performance notes**
    
    Description of why this genotype is special/interesting and how it performs.
    """
    simi: float|ExtValue[float]
    """
    **Similarity**
    
    Average of 'dissimilarity(thisgeno,othergeno)' calculated for all other Genotype instances. This property is meant as fitness multiplier, included in the fitness function when similarity speciation (ExpProperties.cr_simi) is enabled.\n
    Read about details of dissimilarity calculation and its applications:\n
    https://www.framsticks.com/bib/Komosinski-et-al-2001\n
    https://www.framsticks.com/bib/Komosinski-and-Kubiak-2011\n
    https://www.framsticks.com/bib/Komosinski-2016
    """
    energ0: float|ExtValue[float]
    """ **Starting energy** """
    energy0: float|ExtValue[float]
    """ **Starting energy** """
    strsiz: int|ExtValue[int]
    """ **Body parts (deprecated; use numparts)** """
    strjoints: int|ExtValue[int]
    """ **Body joints (deprecated; use numjoints)** """
    nnsiz: int|ExtValue[int]
    """ **Brain size (deprecated; use numneurons)** """
    nncon: int|ExtValue[int]
    """ **Brain connections (deprecated; use numconnections)** """
    numparts: int|ExtValue[int]
    """ **Number of body Parts** """
    numjoints: int|ExtValue[int]
    """ **Number of body Joints** """
    numneurons: int|ExtValue[int]
    """ **Number of neurons** """
    numconnections: int|ExtValue[int]
    """ **Number of neural connections** """
    num: int|ExtValue[int]
    """
    **Ordinal number**
    
    Acts as a unique identifier, but less strict than "uid". Unlike "uid", "num" can be changed and therefore can be saved and restored, providing persistence and continuity beyond a single application run. "num" is only guaranteed to be unique if it is autogenerated and not changed by the user, otherwise it is user's responsibility to manage the proper values of "num". "Genotype.num" is generated on adding a Genotype object to a group, unless it already has a non-zero "num" (previously autogenerated or user-assigned). Autogenerated "num" is always equal to the largest previously used "num" + 1. The largest previously used value is stored in Simulator.last_genotype_num and can be changed as well (and is automatically saved and restored as a part of the Simulator state). Limitation: being a 32-bit integer, "num" overflows at about 2 billion counts.\n
    See also: uid
    """
    gnum: int|ExtValue[int]
    """ **Generation** """
    popsiz: int|ExtValue[int]
    """
    **Population size**
    
    Please use 'instances' instead of 'popsiz'.
    """
    instances: int|ExtValue[int]
    """ Copies of this genotype """
    lifespan: float|ExtValue[float]
    """
    **Life span**
    
    See Creature.lifespan
    """
    velocity: float|ExtValue[float]
    """ See Creature.velocity """
    distance: float|ExtValue[float]
    """ See Creature.distance """
    vertvel: float|ExtValue[float]
    """
    **Vertical velocity**
    
    See Creature.vertvel
    """
    vertpos: float|ExtValue[float]
    """
    **Vertical position**
    
    See Creature.vertpos
    """
    fit: float|ExtValue[float]
    """ **Fitness** """
    fit2: float|ExtValue[float]
    """
    **Final fitness**
    
    Fitness shifted by (avg-n*stddev)
    """
    f0genotype: str|ExtValue[str]
    """
    **f0 genotype**
    
    converted to f0 genotype
    """
    convtrace1: str|ExtValue[str]
    """ **Conversion backtrace [1]** """
    data: Dictionary
    """ **Custom fields dictionary** """
    user1: Any|ExtValue[Any]
    """ **User field 1** """
    user2: Any|ExtValue[Any]
    """ **User field 2** """
    user3: Any|ExtValue[Any]
    """ **User field 3** """
    @staticmethod
    def mutate() -> None|ExtValue[None]:

        ...

    isValid: int|ExtValue[int]
    """
    **Valid**
    
    Use 'is_valid' instead of 'isValid'.
    """
    is_valid: int|ExtValue[int]
    """
    **Validity**
    
    0 = invalid genotype\n
    1 = valid genotype\n
    -1 = validity is not known. This is a transient state. The value of "is_valid" will never be -1 when read. It is safe to treat is_valid as boolean in statements like "if (g.is_valid) ...". Setting "is_valid=-1" will make it 0 or 1 again. This third state (-1) is only needed for loading Genotype objects from files where the "is_valid" field might not be present.
    """
    @staticmethod
    def getNormalized(property_name_or_index: Any|ExtValue[Any]) -> float|ExtValue[float]:
        """ **get normalized property** """
        ...

    geno: Geno
    """ A Geno object for this Genotype """
    uid: str|ExtValue[str]
    """
    **#**
    
    Unique identifier that is generated on object creation. "uid" is only unique during a single application run. Subsequent runs generate the same sequence of uid values.\n
    See also: num
    """
    @staticmethod
    def getModel() -> Model:
        """ **Model object** """
        ...

    @staticmethod
    def splitInstances() -> None|ExtValue[None]:
        """ **split instances** """
        ...

    @staticmethod
    def newFromString(genotype: str|ExtValue[str]) -> Genotype:
        """ **create new object** """
        ...

    @staticmethod
    def newFromGeno(arg1: Geno) -> Genotype:
        """ **create new object** """
        ...

    @staticmethod
    def newFromCreature(arg1: Creature) -> Genotype:
        """ **create new object** """
        ...

    @staticmethod
    def addPerformanceFromCreature(arg1: Creature) -> None|ExtValue[None]:
        """ Updates the Genotype's performance values merging them with the supplied Creture's performance. It assumes the Genotype.instances has a reasonable value and performs the proper weighting. Use your own function instead if these conditions are not met in your experiment. """
        ...

    @staticmethod
    def moveTo(pool: GenePool) -> None|ExtValue[None]:
        """
        **move to another gene pool**
        
        the genotype is removed from its current pool when pool=null
        """
        ...

    @staticmethod
    def clone() -> Genotype:
        """
        **create a copy of the genotype**
        
        Returns a duplicated genotype, not attached to any gene pool. All genotype fields are copied including 'data' (for which Dictionary.clone() produces a shallow copy).
        """
        ...

    @staticmethod
    def delete() -> None|ExtValue[None]:
        """ **remove from the pool** """
        ...

    @staticmethod
    def deleteOne() -> None|ExtValue[None]:
        """ **delete single instance from the pool** """
        ...

    genepool: GenePool
    """
    **gene pool**
    
    GenePool object or null when not in pool
    """
    index: int|ExtValue[int]
    """
    **current index in gene pool**
    
    -1 when not in pool.\n
    Note that the index changes depending on the current genotype position in the pool. Use Genotype.uid if you need a permanent identifier that persists through the entire object lifetime.
    """
    @staticmethod
    def beforeLoad() -> None|ExtValue[None]:
        """ **Before loading** """
        ...

    @staticmethod
    def afterLoad() -> None|ExtValue[None]:
        """ **After loading** """
        ...


class Interface(ExtValue):
    """
    Used to query for object member descriptions. Examples:
      Simulator.print(Interface.makeFrom(Populations[0]).getType("perfperiod"));\n
      Simulator.print(Interface.makeFrom(Populations[0]).getMin("perfperiod"));\n
      Simulator.print(Interface.makeFrom(Populations[0]).getMax("perfperiod"));\n
      Simulator.print(Interface.makeFrom(Populations[0]).getDefault("perfperiod"));\n
      Simulator.print(Interface.makeFrom(Joint.*).getMax("dx"));\n
      Simulator.print(Interface.makeFrom(Part.*).getName("x"));\n
      Simulator.print(Interface.makeFrom(Creature.*).getHelp("idleen"));\n
      var iface=Interface.makeFrom(someobject); var description="This object has "+iface.size+" properties, first property is "+iface.getId(0);
    """

    name: str|ExtValue[str]
    """ **object name** """
    size: int|ExtValue[int]
    """ **property count** """
    groups: int|ExtValue[int]
    """ **group count** """
    @staticmethod
    def get(index_or_id: Any|ExtValue[Any]) -> Any|ExtValue[Any]:
        """ **value of item** """
        ...

    @staticmethod
    def getId(index_or_id: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """ **id for item** """
        ...

    @staticmethod
    def getName(index_or_id: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """ **name for item** """
        ...

    @staticmethod
    def getGroup(index_or_id: Any|ExtValue[Any]) -> int|ExtValue[int]:
        """ **group index for item** """
        ...

    @staticmethod
    def getGroupName(index: int|ExtValue[int]) -> str|ExtValue[str]:
        """ **group name for group index** """
        ...

    @staticmethod
    def getType(index_or_id: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """ **type for item** """
        ...

    @staticmethod
    def getMin(index_or_id: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """ **min value for item** """
        ...

    @staticmethod
    def getMax(index_or_id: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """ **max value for item** """
        ...

    @staticmethod
    def getDefault(index_or_id: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """ **default value for item** """
        ...

    @staticmethod
    def getFlags(index_or_id: Any|ExtValue[Any]) -> int|ExtValue[int]:
        """ **flags for item** """
        ...

    @staticmethod
    def getHelp(index_or_id: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """ **help for item** """
        ...

    @staticmethod
    def findId(name: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **item index having id** """
        ...

    @staticmethod
    def findGroupId(name: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **group index for group name** """
        ...

    @staticmethod
    def findIdInGroup(name: str|ExtValue[str], group_name_or_index: Any|ExtValue[Any]) -> int|ExtValue[int]:
        """ **item index for id in group** """
        ...

    @staticmethod
    def makeFrom(arg1: Object) -> Interface:
        """ **get interface object** """
        ...

    @staticmethod
    def set(index_or_id: Any|ExtValue[Any], value: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ **set value of item** """
        ...

    @staticmethod
    def setDefault(index_or_id: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ **set default value for item** """
        ...

    @staticmethod
    def setAllDefault() -> None|ExtValue[None]:
        """ **set default values for all items** """
        ...

    @staticmethod
    def invoke(function_name_or_index: Any|ExtValue[Any], arguments: Vector) -> None|ExtValue[None]:
        """ **invoke action** """
        ...

    readonly: int|ExtValue[int]
    """ **d 0 1** """
    @staticmethod
    def isReadonly(arg1: Object) -> int|ExtValue[int]:
        """ **test if object is readonly** """
        ...

    @staticmethod
    def makeReadonly(arg1: Object) -> Object:
        """ **make any object readonly** """
        ...


class Joint(ExtValue):


    p1: int|ExtValue[int]
    """ **part1 ref#** """
    p2: int|ExtValue[int]
    """ **part2 ref#** """
    rx: float|ExtValue[float]
    """ **rotation.x** """
    ry: float|ExtValue[float]
    """ **rotation.y** """
    rz: float|ExtValue[float]
    """ **rotation.z** """
    dx: float|ExtValue[float]
    """ **delta.x** """
    dy: float|ExtValue[float]
    """ **delta.y** """
    dz: float|ExtValue[float]
    """ **delta.z** """
    sh: int|ExtValue[int]
    """ **shape** """
    hx: float|ExtValue[float]
    """ **hinge position.x** """
    hy: float|ExtValue[float]
    """ **hinge position.y** """
    hz: float|ExtValue[float]
    """ **hinge position.z** """
    hrx: float|ExtValue[float]
    """ **hinge rotation.x** """
    hry: float|ExtValue[float]
    """ **hinge rotation.y** """
    hrz: float|ExtValue[float]
    """ **hinge rotation.z** """
    hxn: float|ExtValue[float]
    """ **hinge x negative limit** """
    hxp: float|ExtValue[float]
    """ **hinge x positive limit** """
    hyn: float|ExtValue[float]
    """ **hinge y negative limit** """
    hyp: float|ExtValue[float]
    """ **hinge y positive limit** """
    stif: float|ExtValue[float]
    """ **stiffness** """
    rotstif: float|ExtValue[float]
    """ **rotation stiffness** """
    stam: float|ExtValue[float]
    """ **stamina** """
    i: str|ExtValue[str]
    """ **info** """
    Vstyle: str|ExtValue[str]
    """
    **Visual style**
    
    See the "Visual style definition" context for more information
    """
    vr: float|ExtValue[float]
    """ **red component** """
    vg: float|ExtValue[float]
    """ **green component** """
    vb: float|ExtValue[float]
    """ **blue component** """

class Loader(ExtValue):
    """ Support for loading files in the Framsticks format. Used in the experiment definition to retrieve experiment state (see OnExpLoad function in standard.expdef). Registered objects (addClass) are handled automaticaly. Loader can call user functions defined by setBreakLabel. """

    @staticmethod
    def addClass(arg1: Object) -> None|ExtValue[None]:
        """ **add class definition** """
        ...

    @staticmethod
    def removeClass(arg1: Object) -> None|ExtValue[None]:
        """ **remove class definition** """
        ...

    @staticmethod
    def clearClasses() -> None|ExtValue[None]:
        """ **remove all definitions** """
        ...

    @staticmethod
    def go() -> int|ExtValue[int]:
        """ **load until next break** """
        ...

    @staticmethod
    def run() -> int|ExtValue[int]:
        """ **continue loading** """
        ...

    status: int|ExtValue[int]
    """ **loader status** """
    comment: str|ExtValue[str]
    """ **last comment** """
    @staticmethod
    def setBreak(break_conditions: int|ExtValue[int]) -> None|ExtValue[None]:
        """ **define break condition** """
        ...

    @staticmethod
    def setBreakLabel(break_condition: int|ExtValue[int], label: str|ExtValue[str]) -> None|ExtValue[None]:
        """ **associate code label with the break condition** """
        ...

    @staticmethod
    def abort() -> None|ExtValue[None]:
        """ **abort loading** """
        ...

    currentObject: Object
    """ **current object** """
    objectName: str|ExtValue[str]
    """ **current object's class name** """
    @staticmethod
    def loadObject() -> None|ExtValue[None]:
        """ **load current object** """
        ...

    @staticmethod
    def skipObject() -> None|ExtValue[None]:
        """ **skip current object** """
        ...

    firstComment: int|ExtValue[int]
    """ **first comment** """
    BeforeObject: int|ExtValue[int]
    """ **BeforeObject break condition** """
    AfterObject: int|ExtValue[int]
    """ **AfterObject break condition** """
    BeforeUnknown: int|ExtValue[int]
    """ **BeforeUnknown break condition** """
    OnComment: int|ExtValue[int]
    """ **OnComment break condition** """
    OnError: int|ExtValue[int]
    """ **OnError break condition** """

class Math(ExtValue):
    """ Mathematical functions library. """

    pi: float|ExtValue[float]
    """ **pi ~ 3.14** """
    twopi: float|ExtValue[float]
    """ **2*pi ~ 6.28** """
    pi2: float|ExtValue[float]
    """ **pi/2 ~ 1.57** """
    pi4: float|ExtValue[float]
    """ **pi/4 ~ 0.78** """
    @staticmethod
    def random(num: int|ExtValue[int]) -> int|ExtValue[int]:
        """
        **integer random number**
        
        0..num-1
        """
        ...

    rnd01: float|ExtValue[float]
    """ **random number [0..1)** """
    @staticmethod
    def rndUni(begin: float|ExtValue[float], end: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **random number (uniform distribution)**
        
        [begin..end)
        """
        ...

    rndGaussStd: float|ExtValue[float]
    """ **random number (normal distribution)** """
    @staticmethod
    def rndGauss(mean: float|ExtValue[float], standard_deviation: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **random number (selectable std.dev.)**
        
        rndGaussStd is rndGauss(0,1)
        """
        ...

    @staticmethod
    def rndCustom(arg1: Vector) -> float|ExtValue[float]:
        """
        **random number**
        
        the parameter describes the desired random distribution that is a sum of uniform distributions, e.g., rndCustom([-10,-1, -1,1, 1,10]) defines 3 uniform distribution intervals [-1,10) [-1,1), [1,10)
        """
        ...

    seed: int|ExtValue[int]
    """
    **random seed**
    
    Random number generator seed.\n
    Note: Math.seed influences all further random activity in the simulator, not just the results of functions in this class.\n
    Note #2: When read, the value behaves just like a regular variable that stores the previously assigned value. It does NOT reflect the internal random generator seed that changes every time a random number has been generated.
    """
    @staticmethod
    def randomize():
        """
        **set random seed**
        
        Set random seed for the random number generator.
        """
        ...

    time: float|ExtValue[float]
    """
    **current time**
    
    Number of seconds since the Epoch (00:00:00 UTC/GMT, January 1, 1970)
    """
    @staticmethod
    def abs(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **absolute value** """
        ...

    @staticmethod
    def sign(arg1: float|ExtValue[float]) -> int|ExtValue[int]:
        """ **sign (-1, 0 or 1)** """
        ...

    @staticmethod
    def sin(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **sinus** """
        ...

    @staticmethod
    def cos(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **cosinus** """
        ...

    @staticmethod
    def tan(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **tangent** """
        ...

    @staticmethod
    def asin(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **arc sinus** """
        ...

    @staticmethod
    def acos(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **arc cosinus** """
        ...

    @staticmethod
    def atan(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **arc tangent** """
        ...

    @staticmethod
    def atan2(y: float|ExtValue[float], x: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **arc tangent of y/x** """
        ...

    @staticmethod
    def pow(a: float|ExtValue[float], b: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **power, a^b** """
        ...

    @staticmethod
    def exp(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **exponent** """
        ...

    @staticmethod
    def log(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **logarithm; base = e** """
        ...

    @staticmethod
    def sqrt(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **square root** """
        ...

    @staticmethod
    def sigmoid(arg1: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **sigmoid function = 2/(1+exp(-x))-1** """
        ...

    @staticmethod
    def min(arg1: Any|ExtValue[Any], arg2: Any|ExtValue[Any]) -> Any|ExtValue[Any]:
        """ **minimum** """
        ...

    @staticmethod
    def max(arg1: Any|ExtValue[Any], arg2: Any|ExtValue[Any]) -> Any|ExtValue[Any]:
        """ **maximum** """
        ...


class MechJoint(ExtValue):


    rx: float|ExtValue[float]
    """ **rotation.x** """
    ry: float|ExtValue[float]
    """ **rotation.y** """
    rz: float|ExtValue[float]
    """ **rotation.z** """
    dx: float|ExtValue[float]
    """ **delta.x** """
    dy: float|ExtValue[float]
    """ **delta.y** """
    dz: float|ExtValue[float]
    """ **delta.z** """
    stif: float|ExtValue[float]
    """ **stiffness** """
    rotstif: float|ExtValue[float]
    """ **rotation stiffness** """
    part1: MechPart
    """ **first part** """
    part2: MechPart
    """ **second part** """
    stress: float|ExtValue[float]
    rotstress: float|ExtValue[float]
    joint: Joint
    """ corresponding Joint object """

class MechPart(ExtValue):


    x: float|ExtValue[float]
    """ **position.x** """
    y: float|ExtValue[float]
    """ **position.y** """
    z: float|ExtValue[float]
    """ **position.z** """
    pos: XYZ
    """ **position** """
    m: float|ExtValue[float]
    """
    **mass**
    
    The mass of a MechPart is the same as the mass of its corresponding Part and cannot be changed. For f0, the mass of each Part is calculated as the number of its incident Joints. For f0s, the mass of each Part is calculated internally as its density*volume.
    """
    s: float|ExtValue[float]
    """ **size** """
    vol: float|ExtValue[float]
    """ **volume** """
    fr: float|ExtValue[float]
    """ **friction** """
    vx: float|ExtValue[float]
    """ **velocity.x** """
    vy: float|ExtValue[float]
    """ **velocity.y** """
    vz: float|ExtValue[float]
    """ **velocity.z** """
    v: XYZ
    """ **velocity** """
    orient: Orient
    """ **orientation** """
    oxx: float|ExtValue[float]
    """ **orientation.x.x** """
    oxy: float|ExtValue[float]
    """ **orientation.x.y** """
    oxz: float|ExtValue[float]
    """ **orientation.x.z** """
    oyx: float|ExtValue[float]
    """ **orientation.y.x** """
    oyy: float|ExtValue[float]
    """ **orientation.y.y** """
    oyz: float|ExtValue[float]
    """ **orientation.y.z** """
    ozx: float|ExtValue[float]
    """ **orientation.z.x** """
    ozy: float|ExtValue[float]
    """ **orientation.z.y** """
    ozz: float|ExtValue[float]
    """ **orientation.z.z** """
    @staticmethod
    def applyForce(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> None|ExtValue[None]:
        """ **apply force** """
        ...

    part: Part
    """ corresponding Part object """

class MessageCatcher(ExtValue):
    """ Capture error messages. """

    @staticmethod
    def new() -> MessageCatcher:
        """ **create and deploy the new MessageCatcher** """
        ...

    @staticmethod
    def close() -> None|ExtValue[None]:
        """ **stop using this MessageCatcher** """
        ...

    store: int|ExtValue[int]
    """ **message storing options** """
    error_count: int|ExtValue[int]
    """ **error count** """
    error_warning_count: int|ExtValue[int]
    """ **error+warning count** """
    error_warning_info_count: int|ExtValue[int]
    """ **error+warning+info count** """
    warning_count: int|ExtValue[int]
    """ **warning count** """
    info_count: int|ExtValue[int]
    """ **info count** """
    stored_count: int|ExtValue[int]
    """ **number of stored messages** """
    messages: str|ExtValue[str]
    """ **stored messages** """
    summary: str|ExtValue[str]
    """ **error summary** """

class Model(ExtValue):


    se: float|ExtValue[float]
    """ **startenergy** """
    Vstyle: str|ExtValue[str]
    """
    **Visual style**
    
    See the "Visual style definition" context for more information
    """
    geno: Geno
    @staticmethod
    def newFromString(genotype: str|ExtValue[str]) -> Model:
        """ **Create a new object** """
        ...

    @staticmethod
    def newFromGeno(arg1: Geno) -> Model:
        """ **Create a new object** """
        ...

    @staticmethod
    def newWithCheckpoints(Geno_object_or_string_genotype: Any|ExtValue[Any]) -> Model:
        """
        **Create a new object**
        
        Creates a Model with the "Checkpoints" option enabled. Genotype converters supporting Checkpoints provide a sequence of Models that reflects development stages of the creature (this sequence is used purely for debugging and visualization of phenotype growth/development). Checkpoint Models can be accessed using getCheckpoint(i) for i ranging from 0 to numcheckpoints-1. Models created without the Checkpoint option and Models coming from unsupported converters have numcheckpoints=0.
        """
        ...

    numparts: int|ExtValue[int]
    """ **Number of parts** """
    numjoints: int|ExtValue[int]
    """ **Number of joints** """
    numneurons: int|ExtValue[int]
    """ **Number of neurons** """
    numconnections: int|ExtValue[int]
    """ **Number of neuron connections** """
    is_valid: int|ExtValue[int]
    """ **Validity** """
    @staticmethod
    def getPart(index: int|ExtValue[int]) -> Part:
        """ **getPart (static model information)** """
        ...

    @staticmethod
    def getJoint(index: int|ExtValue[int]) -> Joint:
        """ **getJoint (static model information)** """
        ...

    @staticmethod
    def getNeuroDef(index: int|ExtValue[int]) -> NeuroDef:

        ...

    size_x: float|ExtValue[float]
    """
    **Bounding box x size**
    
    (size_x,size_y,size_z) are dimensions of the axis-aligned bounding box of the creature, including imaginary Part sizes (Part.s, usually 1.0). A creature consisting of a single default part has the size of (2.0,2.0,2.0) - twice the Part.s value (like a sphere diameter is twice its radius).\n
    See also: Creature.moveAbs
    """
    size_y: float|ExtValue[float]
    """
    **Bounding box y size**
    
    See Model.size_x
    """
    size_z: float|ExtValue[float]
    """
    **Bounding box z size**
    
    See Model.size_x
    """
    bboxSize: XYZ
    """ **Bounding box size** """
    numcheckpoints: int|ExtValue[int]
    """ **Number of checkpoints** """
    @staticmethod
    def getCheckpoint(index: int|ExtValue[int]) -> Model:
        """
        Checkpoint Model objects are only valid as long as the parent Model object exists.\n
        See also: Model.newWithCheckpoints()
        
        // incorrect usage - calling getCheckpoint() on a temporary object:\n
        var c=Model.newWithCheckpoints("XXX").getCheckpoint(1).genotype.geno;
        
        // correct usage - keeping the parent Model reference in 'm':\n
        var m=Model.newWithCheckpoints("XXX");\n
        var c=m.getCheckpoint(1).genotype.geno;
        """
        ...

    shape_type: int|ExtValue[int]
    """ **Shape type** """
    solid_model: Model
    """
    **Solid shapes model**
    
    Conversion of this Model to solid shapes. Note! Only available when this Model has shape_type==2 (Ball-and-stick).
    """

class ModelGeometry(ExtValue):
    """
    Approximately estimates sizes, volume, and area of a Model based on the geometry of its parts.\n
    Example usage:\n
    Simulator.print(ModelGeometry.forModel(Model.newFromString("//0\\\\np:sh=1\\\\n")).area());
    
    ModelGeometry.geom_density refers to the global simulator parameter (also available in GUI).\n
    To set geom_density for individual ModelGeometry objects:\n
    var mg=ModelGeometry.forModel(GenePools[0][0].getModel()); mg.geom_density=2; GenePools[0][0].data->area=mg.area();
    """

    geom_density: float|ExtValue[float]
    """
    **Density**
    
    The number of samples (per unit length in one dimension) that affects the precision of estimation of geometrical properties.
    """
    @staticmethod
    def forModel(arg1: Model) -> ModelGeometry:
        """ The returned ModelGeometry object can be used to calculate geometric properties (volume, area, sizes) of the associated model. The density is copied from the current global ModelGeometry.geom_density on object creation. """
        ...

    @staticmethod
    def volume() -> float|ExtValue[float]:

        ...

    @staticmethod
    def area() -> float|ExtValue[float]:

        ...

    @staticmethod
    def voxels() -> Vector:
        """ Returns a Vector of Pt3D objects from a regular 3D grid (sampled according to ModelGeometry.geom_density) that are inside the Model body (Parts and Joints). """
        ...

    @staticmethod
    def sizesAndAxes() -> Vector:
        """ The returned vector contains XYZ (sizes) and Orient (axes) objects. """
        ...


class ModelSymmetry(ExtValue):
    """ Calculates bilateral symmetry. Details are described in https://www.framsticks.com/bib/Jaskowski-and-Komosinski-2008 """

    @staticmethod
    def calculateSymmetry(model: Model) -> float|ExtValue[float]:
        """
        **Calculate symmetry**
        
        Returns bilateral symmetry (0.0 .. 1.0) for a given Model using default precision parameters (symPosSteps,symAlphaSteps,symBetaSteps). Returns the symmetry plane, too (sets symResultA,B,C,D).\n
        Note: may take a long time for large creatures.
        """
        ...

    @staticmethod
    def calculateSymmetry2(model: Model, posSteps: int|ExtValue[int], alphaSteps: int|ExtValue[int], betaSteps: int|ExtValue[int]) -> float|ExtValue[float]:
        """
        **Calculate symmetry**
        
        Returns bilateral symmetry (0.0 .. 1.0) for a given Model using specified precision parameters. Returns the symmetry plane, too (sets symResultA,B,C,D).\n
        Note: may take a long time for large creatures.
        """
        ...

    @staticmethod
    def calculateSymmetryForPlane(model: Model, A: float|ExtValue[float], B: float|ExtValue[float], C: float|ExtValue[float], D: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **Calculate symmetry**
        
        Returns bilateral symmetry (0.0 .. 1.0) for a given Model and given a specific plane defined by coefficients A, B, C, D.
        """
        ...

    symPosSteps: int|ExtValue[int]
    """
    **Position sampling**
    
    Default number of samples per stick length
    """
    symAlphaSteps: int|ExtValue[int]
    """
    **Angular sampling (1)**
    
    Default number of samples per full angle (#1)
    """
    symBetaSteps: int|ExtValue[int]
    """
    **Angular sampling (2)**
    
    Default number of samples per full angle (#2)
    """
    symResultA: float|ExtValue[float]
    """ **resulting symmetry plane, coeff. A (set by calculateSymmetry)** """
    symResultB: float|ExtValue[float]
    """ **resulting symmetry plane, coeff. B (set by calculateSymmetry)** """
    symResultC: float|ExtValue[float]
    """ **resulting symmetry plane, coeff. C (set by calculateSymmetry)** """
    symResultD: float|ExtValue[float]
    """ **resulting symmetry plane, coeff. D (set by calculateSymmetry)** """

class Neuro(ExtValue):
    """ Live Neuron object. """

    @staticmethod
    def getInputState(input: int|ExtValue[int]) -> float|ExtValue[float]:
        """ **Get input signal** """
        ...

    @staticmethod
    def getInputWeight(input: int|ExtValue[int]) -> float|ExtValue[float]:
        """ **Get input weight** """
        ...

    @staticmethod
    def getWeightedInputState(input: int|ExtValue[int]) -> float|ExtValue[float]:
        """ **Get weighted input signal** """
        ...

    @staticmethod
    def getInputSum(input: int|ExtValue[int]) -> float|ExtValue[float]:
        """ **Get signal sum** """
        ...

    @staticmethod
    def getWeightedInputSum(input: int|ExtValue[int]) -> float|ExtValue[float]:
        """
        **Get weighted signal sum**
        
        Uses any number of inputs starting with the specified input. getWeightedInputSum(0)=weightedInputSum
        """
        ...

    getInputCount: int|ExtValue[int]
    """ **Get input count** """
    inputSum: float|ExtValue[float]
    """ **Full signal sum** """
    weightedInputSum: float|ExtValue[float]
    """ **Full weighted signal sum** """
    @staticmethod
    def getInputChannelCount(input: int|ExtValue[int]) -> int|ExtValue[int]:
        """ **Get channel count for input** """
        ...

    @staticmethod
    def getInputStateChannel(input: int|ExtValue[int], channel: int|ExtValue[int]) -> float|ExtValue[float]:
        """ **Get input signal from channel** """
        ...

    @staticmethod
    def getWeightedInputStateChannel(input: int|ExtValue[int], channel: int|ExtValue[int]) -> float|ExtValue[float]:
        """ **Get weighted input signal from channel** """
        ...

    state: float|ExtValue[float]
    """
    **Neuron state (channel 0)**
    
    When read, returns the current neuron state.\n
    When written, sets the 'internal' neuron state that will become current in the next step.\n
    Typically you should use this field, and not currState.
    """
    channelCount: int|ExtValue[int]
    """ **Number of output channels** """
    @staticmethod
    def getStateChannel(channel: int|ExtValue[int]) -> float|ExtValue[float]:
        """ **Get state for channel** """
        ...

    @staticmethod
    def setStateChannel(channel: int|ExtValue[int], value: float|ExtValue[float]) -> None|ExtValue[None]:
        """ **Set state for channel** """
        ...

    hold: int|ExtValue[int]
    """
    **Hold state**
    
    "Holding" means keeping the neuron state as is, blocking the regular neuron operation. This is useful when your script needs to inject some control signals into the NN. Without "holding", live neurons would be constantly overwriting your changes, and the rest of the NN could see inconsistent states, depending on the connections. Setting hold=1 ensures the neuron state will be only set by you, and not by the neuron. The enforced signal value can be set using Neuro.currState before or after setting hold=1. Set hold=0 to resume normal operation.
    """
    currState: float|ExtValue[float]
    """
    **Current neuron state (channel 0)**
    
    When read, it behaves just like the 'state' field.\n
    When written, changes the current neuron state immediately, which disturbs the regular synchronous NN operation.\n
    This feature should only be used while controlling the neuron 'from outside' (like a neuro probe) and not in the neuron definition. See also: Neuro.hold
    """
    @staticmethod
    def setCurrStateChannel(channel: int|ExtValue[int], value: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **Set current neuron state for channel**
        
        Analogous to "currState".
        """
        ...

    position_x: float|ExtValue[float]
    """ **Position x** """
    position_y: float|ExtValue[float]
    """ **Position y** """
    position_z: float|ExtValue[float]
    """ **Position z** """
    relative_pos: XYZ
    """ **Relative position** """
    relative_orient: Orient
    """ **Relative orientation** """
    creature: Creature
    """ **Gets owner creature** """
    mechpart: MechPart
    """ The MechPart object where this neuron is located """
    mechjoint: MechJoint
    """ The MechJoint object where this neuron is located """
    neuroproperties: NeuroProperties
    """
    **Custom neuron fields**
    
    Neurons can have different fields depending on their class. Script neurons have their fields defined using the "property:" syntax. If you develop a custom neuron script you should use the NeuroProperties object for accessing your own neuron fields. The Neuro.neuroproperties property is meant for accessing the neuron fields from the outside script.\n
    Examples:\n
    var c=Populations.createFromString("X[N]");\n
    Simulator.print("standard neuron inertia="+c.getNeuro(0).neuroproperties.in);\n
    c=Populations.createFromString("X[Nn,e:0.1]");\n
    Simulator.print("noisy neuron error rate="+c.getNeuro(0).neuroproperties.e);
    
    The Interface object can be used to discover which fields are available for a certain neuron object:\n
    c=Populations.createFromString("X[N]");\n
    var iobj=Interface.makeFrom(c.getNeuro(0).neuroproperties);\n
    var i;\n
    for(i=0;i<iobj.size;i++)
     Simulator.print(iobj.getId(i)+" ("+iobj.getName(i)+")");
    """
    def_: NeuroDef
    """ **Neuron definition from which this live neuron was built** """
    classObject: NeuroClass
    """ **Neuron class for this neuron** """
    signals: NeuroSignals

class NeuroClass(ExtValue):
    """ The static NeuroClass object refers to the class selected in the NeuroClassLibrary. Most, but not all, properties have direct counterparts in *.neuro files that define custom neuron classes. """

    name: str|ExtValue[str]
    """
    **Class name**
    
    Used in genotypes
    """
    longname: str|ExtValue[str]
    """
    **Long, human readable name**
    
    Used in hints
    """
    description: str|ExtValue[str]
    """ **Long description** """
    prefinputs: int|ExtValue[int]
    """
    **Preferred number of inputs**
    
    -1 means "any number of inputs is OK"
    """
    prefoutput: int|ExtValue[int]
    """
    **Provides output**
    
    Should be 1 if the neuron provides meaningful output value, 0 otherwise
    """
    preflocation: int|ExtValue[int]
    """ **Preferred body location** """
    shape_types: int|ExtValue[int]
    """
    **Supported model shape types**
    
    Bit mask of supported (1<<Model::ShapeType) values, default 3=all shape types supported
    """
    joint_shapes: int|ExtValue[int]
    """
    **Supported joint shapes**
    
    Bit mask of supported (1<<Joint::Shape) values, default 15=all joint shapes supported
    """
    visualhints: int|ExtValue[int]
    """
    **Visual hints**
    
    This is a bitfield. Compute the value by adding the following bits:\n
    1 = Invisible - don't draw neurons of this class\n
    2 = No label - don't draw classname label (below the neuron symbol) for this neuron class\n
    4 = First Part - draw the neuron at the first part when attached to a joint (default is in the middle)\n
    8 = Second Part - draw the neuron at the second part when attached to a joint (default is in the middle)\n
    16 = Effector - use muscle color when drawing this neuron\n
    32 = Sensor - use receptor color when drawing this neuron\n
    Compatiblity: visualhints is called "vhints" in *.neuro files.
    """
    glyph: str|ExtValue[str]
    """
    **Glyph vector data**
    
    <html>The neuron icon for use in NN diagrams, encoded as a comma-separated sequence of integer numbers.<ul>\n
    <li>N = the total number of all numbers following this one\n
    <li>NS = the number of line sequences<br>\n
    <ul>repeated NS times:\n
    <li>NL = number of line segments (creating a polyline)\n
    <li><span style="background-color:#fcc;">X,Y</span> (repeated NL+1 times) - subsequent line segment coordinates, each line should fit in a 100x100 square<br>\n
    - neuron input connections will be drawn at X=25 (varying Y for multiple inputs, Y=50 for a single input)<br>\n
    - neuron output connection will be drawn at (X=75,Y=50)\n
    </ul></ul>\n
    <p>Example:\n
    <table border=1>\n
    <tr><th>16,</th><th>2,</th><th>3,</th><th><span style="background-color:#fcc;">25,50</span>, <span style="background-color:#fcc;">40,30</span>, <span style="background-color:#fcc;">60,30</span>, <span style="background-color:#fcc;">75,50</span>,</th><th>1,</th><th><span style="background-color:#fcc;">40,50</span>, <span style="background-color:#fcc;">60,50</span></th></tr>\n
    <tr><td>N = 16 numbers following this one</td><td>NS = 2 line sequences</td><td>NL = the first sequence has 3 segments</td><td>coordinates for 3 line segments = 4 endpoints = 8 numbers</td><td>NL = the second sequence has 1 segment</td><td>coordinates for 1 line segment</td></tr>\n
    </table>\n
    <p>See also: <a href="https://www.framsticks.com/files/apps-devel/inkscape-to-icon.html">a script for creating *.neuro icon from SVG</a><br>\n
    Compatibility: this field is called "icon" in *.neuro files.
    """
    properties: Interface
    """
    **Interface object connected with neuron class properties**
    
    Compatibility: not preset in *.neuro files.
    """
    summary: str|ExtValue[str]
    """
    Textual summary of all features.\n
    Compatibility: not preset in *.neuro files.
    """

class NeuroClassLibrary(ExtValue):
    """ Set of Neuron classes. You can access the selected class in the static NeuroClass object. """

    count: int|ExtValue[int]
    """ **class count** """
    class_: int|ExtValue[int]
    """
    **current class**
    
    0 ... count-1
    """
    @staticmethod
    def findClass(class_name: str|ExtValue[str]) -> None|ExtValue[None]:
        """ **select class by name** """
        ...

    @staticmethod
    def getClass(class_name: str|ExtValue[str]) -> NeuroClass:
        """ **get class object by name** """
        ...


class NeuroDef(ExtValue):


    p: int|ExtValue[int]
    """ **part ref#** """
    j: int|ExtValue[int]
    """ **joint ref#** """
    d: str|ExtValue[str]
    """ **details** """
    i: str|ExtValue[str]
    """ **info** """
    Vstyle: str|ExtValue[str]
    """
    **Visual style**
    
    See the "Visual style definition" context for more information
    """
    getInputCount: int|ExtValue[int]
    """ **input count** """
    @staticmethod
    def getInputNeuroDef(arg1: int|ExtValue[int]) -> NeuroDef:
        """ **get input neuron** """
        ...

    @staticmethod
    def getInputNeuroIndex(arg1: int|ExtValue[int]) -> int|ExtValue[int]:
        """ **get input neuron index** """
        ...

    @staticmethod
    def getInputWeight(arg1: int|ExtValue[int]) -> float|ExtValue[float]:
        """ **get input weight** """
        ...

    classObject: NeuroClass
    """ **neuron class** """

class NeuronsSimEnabled(ExtValue):


    ncl_N: int|ExtValue[int]
    """
    **Neuron (N)**
    
    Standard neuron
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       Inertia (in) float 0..1 (default 0.8)\n
       Force (fo) float 0..999 (default 0.04)\n
       Sigmoid (si) float -99999..99999 (default 2)\n
       State (s) float -1..1 (default 0)
    """
    ncl_Nu: int|ExtValue[int]
    """
    **Unipolar neuron [EXPERIMENTAL!] (Nu)**
    
    Works like standard neuron (N) but the output value is scaled to 0...+1 instead of -1...+1.\n
    Having 0 as one of the saturation states should help in "gate circuits", where input signal is passed through or blocked depending on the other singal.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       Inertia (in) float 0..1 (default 0.8)\n
       Force (fo) float 0..999 (default 0.04)\n
       Sigmoid (si) float -99999..99999 (default 2)\n
       State (s) float -1..1 (default 0)
    """
    ncl_G: int|ExtValue[int]
    """
    **Gyroscope (G)**
    
    Tilt sensor.\n
    Signal is proportional to sin(angle) = most sensitive in horizontal orientation.\n
    0=the stick is horizontal\n
    +1/-1=the stick is vertical
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Joint
    """
    ncl_Gpart: int|ExtValue[int]
    """
    **Part Gyroscope (Gpart)**
    
    Tilt sensor. Signal is directly proportional to the tilt angle.\n
    0=the part X axis is horizontal\n
    +1/-1=the axis is vertical
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    ncl_T: int|ExtValue[int]
    """
    **Touch (T)**
    
    Touch and proximity sensor (Tcontact and Tproximity combined)\n
    -1=no contact\n
    0=just touching\n
    >0=pressing, value depends on the force applied (not implemented in ODE mode)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       Range (r) float 0..1 (default 1)\n
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    ncl_Tcontact: int|ExtValue[int]
    """
    **Touch contact (Tcontact)**
    
    Touch sensor.\n
    -1=no contact\n
    0=the Part is touching the obstacle\n
    >0=pressing, value depends on the force applied (not implemented in ODE mode)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    ncl_Tproximity: int|ExtValue[int]
    """
    **Touch proximity (Tproximity)**
    
    Proximity sensor detecting obstacles along the X axis.\n
    -1=distance is "r" or more\n
    0=zero distance
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       Range (r) float 0..1 (default 1)\n
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    ncl_S: int|ExtValue[int]
    """
    **Smell (S)**
    
    Smell sensor. Aggregated "smell of energy" experienced from all energy objects (creatures and food pieces).\n
    Close objects have bigger influence than the distant ones: for each energy source, its partial feeling is proportional to its energy/(distance^2)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    ncl_Constant: int|ExtValue[int]
    """
    **Constant (*)**
    
    Constant value
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_Bend_muscle: int|ExtValue[int]
    """
    **Bend muscle (|)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 0.25)\n
       bending range (r) float 0..1 (default 1)
    """
    ncl_Rotation_muscle: int|ExtValue[int]
    """
    **Rotation muscle (@)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 1)
    """
    ncl_M: int|ExtValue[int]
    """
    **Muscle for solids (M)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 1)\n
       axis (a) integer 0..1 (default 0)
    """
    ncl_D: int|ExtValue[int]
    """
    **Differentiate (D)**
    
    Calculate the difference between the current and previous input value. Multiple inputs are aggregated with respect to their weights
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_Fuzzy: int|ExtValue[int]
    """
    **Fuzzy system [EXPERIMENTAL!] (Fuzzy)**
    
    Refer to publications to learn more about this neuron.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       number of fuzzy sets (ns) integer\n
       number of rules (nr) integer\n
       fuzzy sets (fs) string (default "")\n
       fuzzy rules (fr) string (default "")
    """
    ncl_VEye: int|ExtValue[int]
    """
    **Vector Eye [EXPERIMENTAL!] (VEye)**
    
    Refer to publications to learn more about this neuron.
    
    Characteristics:
       uses single input\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       target.x (tx) float\n
       target.y (ty) float\n
       target.z (tz) float\n
       target shape (ts) string (default "")\n
       perspective (p) float 0.1..10 (default 1)\n
       scale (s) float 0.1..100 (default 1)\n
       show hidden lines (h) integer 0..1 (default 0)\n
       output lines count (each line needs four channels) (o) integer 0..99 (default 0)\n
       debug (d) integer 0..1 (default 0)
    """
    ncl_VMotor: int|ExtValue[int]
    """
    **Visual-Motor Cortex [EXPERIMENTAL!] (VMotor)**
    
    Must be connected to the VEye and properly set up. Refer to publications to learn more about this neuron.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       number of basic features (noIF) integer\n
       number of degrees of freedom (noDim) integer\n
       parameters (params) string
    """
    ncl_Sti: int|ExtValue[int]
    """
    **Sticky [EXPERIMENTAL!] (Sti)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Part
    """
    ncl_LMu: int|ExtValue[int]
    """
    **Linear muscle [EXPERIMENTAL!] (LMu)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0.01..1 (default 1)
    """
    ncl_Water: int|ExtValue[int]
    """
    **Water detector (Water)**
    
    Output signal:\n
    0=on or above water surface\n
    1=under water (deeper than 1)\n
    0..1=in the transient area just below water surface
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    ncl_Energy: int|ExtValue[int]
    """
    **Energy level (Energy)**
    
    The current energy level divided by the initial energy level.\n
    Usually falls from initial 1.0 down to 0.0 and then the creature dies. It can rise above 1.0 if enough food is ingested
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_Ch: int|ExtValue[int]
    """
    **Channelize (Ch)**
    
    Combines all input signals into a single multichannel output; Note: ChSel and ChMux are the only neurons which support multiple channels. Other neurons discard everything except the first channel.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_ChMux: int|ExtValue[int]
    """
    **Channel multiplexer (ChMux)**
    
    Outputs the selected channel from the second (multichannel) input. The first input is used as the selector value (-1=select first channel, .., 1=last channel)
    
    Characteristics:
       uses 2 inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_ChSel: int|ExtValue[int]
    """
    **Channel selector (ChSel)**
    
    Outputs a single channel (selected by the "ch" parameter) from multichannel input
    
    Characteristics:
       uses single input\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       channel (ch) integer
    """
    ncl_Rnd: int|ExtValue[int]
    """
    **Random noise (Rnd)**
    
    Generates random noise (subsequent random values in the range of -1..+1)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_Sin: int|ExtValue[int]
    """
    **Sinus generator (Sin)**
    
    Output frequency = f0+input
    
    Characteristics:
       uses single input\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       base frequency (f0) float -1..1 (default 0.0628319)\n
       time (t) float 0..6.28319 (default 0)
    """

class NeuroSignals(ExtValue):
    """
    Signals attached to a neuron.\n
    See also: Signal, WorldSignals, CreatureSignals.\n
    scripts/light.neuro and scripts/seelight.neuro are simple custom neuron examples demonstrating how to send/receive signals between creatures.
    """

    @staticmethod
    def add(channel: str|ExtValue[str]) -> Signal:
        """ **Create a new signal** """
        ...

    @staticmethod
    def receive(channel: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **Receive signal in channel**
        
        Receive the aggregated signal power in a given channel.
        """
        ...

    @staticmethod
    def receiveSet(channel: str|ExtValue[str], max_distance: float|ExtValue[float]) -> Vector:
        """
        **Receive signals in range**
        
        Get all signals in the specified range. Returns a read-only vector object containing Signal objects - individual signals can be accessed as result[0], .., result[result.size-1].
        """
        ...

    @staticmethod
    def receiveFilter(channel: str|ExtValue[str], max_distance: float|ExtValue[float], flavor: float|ExtValue[float], flavorfilter: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **Receive filtered signal**
        
        Receive the aggregated signal power in a given channel.
        
        Additional filtering options:\n
        - Max distance only receives the neighbor signals (based on their physical location)\n
        - Flavor filtering: only signals having the flavor similar to the specified value will be received. The flavorfilter value is the difference of flavor that reduces the received signal to 0. The "flavor attenuation" is linear, i.e., signals differing by (filter/2) in flavor will be reduced to 50%.
        """
        ...

    @staticmethod
    def receiveSingle(channel: str|ExtValue[str], max_distance: float|ExtValue[float]) -> Signal:
        """
        **Receive strongest**
        
        Find the signal source that has the highest signal power (taking into account distance).
        """
        ...

    @staticmethod
    def get(index: int|ExtValue[int]) -> Signal:
        """ **Access individual signals (index = 0 .. size-1)** """
        ...

    size: int|ExtValue[int]
    """ **Number of signals in this set** """
    @staticmethod
    def clear() -> None|ExtValue[None]:
        """ **Delete all signals** """
        ...


class ODE(ExtValue):
    """ ODE Parameters. """

    odeshape: int|ExtValue[int]
    """ **Stick shape for ball-and-stick models** """
    odestep: float|ExtValue[float]
    """ **Simulation step** """
    odemusclemin: float|ExtValue[float]
    """
    **Muscle min power**
    
    i.e. "mmmmm" in f1
    """
    odemusclemax: float|ExtValue[float]
    """
    **Muscle max power**
    
    i.e. "MMMMM" if f1
    """
    odemusclespeed: float|ExtValue[float]
    """
    **Muscle speed limit**
    
    Muscle state cannot change faster than the supplied value
    """
    odeairdrag: float|ExtValue[float]
    """
    **Drag**
    
    A drag force ("air drag") proportional to the velocity of mass centers of moving parts (ODE's "linear damping")
    """
    oderotdrag: float|ExtValue[float]
    """
    **Rotation drag**
    
    Drag momentum acting on rotating bodies (ODE's "angular damping")
    """
    odewaterdrag: float|ExtValue[float]
    """ **Water drag** """
    odewaterbuoy: float|ExtValue[float]
    """ **Water buoyancy** """
    odeseed: int|ExtValue[int]
    """
    **Randomness**
    
    Affects collisions.\n
    - 'Truly random' is closest to the standard ODE operation. Use Math.seed to influence randomness in ODE collisions.\n
    - 'Deterministic' automatically calculates random seed in each step based on the current simulation (world) state, which makes the simulation repeatable but more random than 'Fixed'.\n
    - 'Fixed' is completely deterministic and does not depend on Math.seed - the same seed value is set before each step. This might negatively affect ODE accuracy.
    """
    odesepsticks: int|ExtValue[int]
    """
    **Separate sticks**
    
    Each stick gets a separate ODE body (like in MechaStick)
    """
    odeworlderp: float|ExtValue[float]
    """
    **ERP**
    
    World ERP (error reduction parameter)
    """
    odeworldcfm: float|ExtValue[float]
    """
    **CFM**
    
    World CFM (constraint force mixing)
    """
    odecolmumin: float|ExtValue[float]
    """
    **Min. friction**
    
    Mu coefficient for Parts with minimal friction (i.e. "fffff" in f1)
    """
    odecolmumax: float|ExtValue[float]
    """
    **Max. friction**
    
    Mu coefficient for Parts with maximal friction (i.e. "FFFFF" in f1)
    """
    odecolbounce: float|ExtValue[float]
    """ **Bounce** """
    odecolbouncevel: float|ExtValue[float]
    """ **Bounce velocity** """
    odecolsoftcfm: float|ExtValue[float]
    """ **Soft CFM** """
    odecolsofterp: float|ExtValue[float]
    """ **Soft ERP** """
    odecol2mumin: float|ExtValue[float]
    """
    **Min. friction**
    
    Mu coefficient for Parts with minimal friction (i.e. "fffff" in f1)
    """
    odecol2mumax: float|ExtValue[float]
    """
    **Max. friction**
    
    Mu coefficient for Parts with maximal friction (i.e. "FFFFF" in f1)
    """
    odecol2bounce: float|ExtValue[float]
    """ **Bounce** """
    odecol2bouncevel: float|ExtValue[float]
    """ **Bounce velocity** """
    odecol2softcfm: float|ExtValue[float]
    """ **Soft CFM** """
    odecol2softerp: float|ExtValue[float]
    """ **Soft ERP** """
    @staticmethod
    def rayIntersection(position_x: float|ExtValue[float], position_y: float|ExtValue[float], position_z: float|ExtValue[float], direction_x: float|ExtValue[float], direction_y: float|ExtValue[float], direction_z: float|ExtValue[float], max_distance: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **ray intersection** """
        ...


class Orient(ExtValue):
    """ 3D orientation, stored as 3x3 matrix. """

    xx: float|ExtValue[float]
    """ **orientation.x.x** """
    xy: float|ExtValue[float]
    """ **orientation.x.y** """
    xz: float|ExtValue[float]
    """ **orientation.x.z** """
    yx: float|ExtValue[float]
    """ **orientation.y.x** """
    yy: float|ExtValue[float]
    """ **orientation.y.y** """
    yz: float|ExtValue[float]
    """ **orientation.y.z** """
    zx: float|ExtValue[float]
    """ **orientation.z.x** """
    zy: float|ExtValue[float]
    """ **orientation.z.y** """
    zz: float|ExtValue[float]
    """ **orientation.z.z** """
    x: XYZ
    """ **x vector** """
    y: XYZ
    """ **y vector** """
    z: XYZ
    """ **z vector** """
    @staticmethod
    def new() -> Orient:
        """ **create new Orient object** """
        ...

    @staticmethod
    def newFromVector(arg1: Vector) -> Orient:
        """ **create new Orient object** """
        ...

    toVector: Vector
    """
    **vector representation**
    
    for serialization
    """
    @staticmethod
    def clone() -> Orient:
        """ **create new Orient object** """
        ...

    @staticmethod
    def set(arg1: Orient) -> None|ExtValue[None]:
        """ **copy from another Orient object** """
        ...

    @staticmethod
    def reset() -> None|ExtValue[None]:
        """ **set identity matrix** """
        ...

    @staticmethod
    def rotate3(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> None|ExtValue[None]:
        """ **rotate around 3 axes** """
        ...

    @staticmethod
    def rotate(arg1: Orient) -> None|ExtValue[None]:
        """ **rotate using Orient object** """
        ...

    @staticmethod
    def revRotate(arg1: Orient) -> None|ExtValue[None]:
        """ **reverse rotate using Orient object** """
        ...

    @staticmethod
    def lookAt(direction: XYZ, up: XYZ) -> None|ExtValue[None]:
        """ **calculate rotation from 2 vectors** """
        ...

    @staticmethod
    def normalize() -> None|ExtValue[None]:

        ...

    @staticmethod
    def between2(arg1: Orient, arg2: Orient, amount: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **interpolate orientation**
        
        The calling Orient receives the orientation interpolated from 2 input orientations.\n
        Example:\n
        var o1=Orient.new(), o2=Orient.new(), o3=Orient.new();\n
        o2.rotate3(0,Math.pi/2,0);\n
        o3.between2(o1,o2,0); // o3 equals o2\n
        o3.between2(o1,o2,1); // o3 equals o1\n
        o3.between2(o1,o2,0.5); // o3 is halfway between o1 and o2
        """
        ...

    @staticmethod
    def betweenOV(arg1: Orient, arg2: XYZ, amount: float|ExtValue[float]) -> None|ExtValue[None]:
        """
        **interpolate orientation**
        
        Like between2(), but the second Orient is composed of the supplied XYZ vector (X component) and Y Z vectors from the calling object.\n
        Example:\n
        var o=Orient.new();\n
        o.betweenOV(o,(0,1,0),1); //no change, o remains 100 010 001\n
        o.betweenOV(o,(0,1,0),0.9); //o is slightly rotated towards (0,1,0)\n
        o.betweenOV(o,(0,1,0),0); //o is completely transformed, o.x=(0,1,0)
        """
        ...

    @staticmethod
    def localToWorld(point: XYZ, center: XYZ) -> XYZ:
        """ **transform coordinates** """
        ...

    @staticmethod
    def worldToLocal(point: XYZ, center: XYZ) -> XYZ:
        """ **transform coordinates** """
        ...

    angles: XYZ
    """ **Euler angles representation** """
    toString: str|ExtValue[str]
    """ **textual form** """

class Part(ExtValue):


    x: float|ExtValue[float]
    """ **position.x** """
    y: float|ExtValue[float]
    """ **position.y** """
    z: float|ExtValue[float]
    """ **position.z** """
    sh: int|ExtValue[int]
    """ **shape** """
    s: float|ExtValue[float]
    """ **size** """
    sx: float|ExtValue[float]
    """ **scale.x** """
    sy: float|ExtValue[float]
    """ **scale.y** """
    sz: float|ExtValue[float]
    """ **scale.z** """
    h: float|ExtValue[float]
    """ **hollow** """
    dn: float|ExtValue[float]
    """ **density** """
    fr: float|ExtValue[float]
    """ **friction** """
    ing: float|ExtValue[float]
    """ **ingestion** """
    as_: float|ExtValue[float]
    """ **assimilation** """
    rx: float|ExtValue[float]
    """ **rot.x** """
    ry: float|ExtValue[float]
    """ **rot.y** """
    rz: float|ExtValue[float]
    """ **rot.z** """
    i: str|ExtValue[str]
    """ **info** """
    Vstyle: str|ExtValue[str]
    """
    **Visual style**
    
    See the "Visual style definition" context for more information
    """
    vr: float|ExtValue[float]
    """ **red component** """
    vg: float|ExtValue[float]
    """ **green component** """
    vb: float|ExtValue[float]
    """ **blue component** """

class Population(metaclass=PopulationIndexer):
    """
    A set of Creature objects, sharing some high level simulation properties (performance calculation, NN simulation, collision detection, event handling). The groups usually have different roles in the experiment (e.g. Creatures groups and Food group in standard.expdef).\n
    You can iterate directly over Creatures in a Population using for(...in...) loops:
    	for(var c in Populations[0]) Simulator.print(c.name);
    """

    index: int|ExtValue[int]
    """ **population index** """
    name: str|ExtValue[str]
    """ **Group name** """
    size: int|ExtValue[int]
    """ **Number of creatures** """
    energy: int|ExtValue[int]
    """
    **Energy calculation**
    
    If turned off, creature's energy will be constant.
    """
    death: int|ExtValue[int]
    """ Do creatures die when no energy? """
    nnsim: int|ExtValue[int]
    """
    **Neural net simulation**
    
    Replaced by initial_nn_active
    """
    initial_nn_active: int|ExtValue[int]
    """
    **Neural net simulation**
    
    Stabilization means no significant movement during a specified period of time. See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    nn_paused: int|ExtValue[int]
    """
    **Neural net paused**
    
    Disables NN simulation for all creatures in the population
    """
    perfperiod: int|ExtValue[int]
    """
    **Performance sampling period**
    
    Defines how often onUpdate() events are called and how often the built-in performance counters (distance, speed, etc.) are calculated. See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    stabilperiod: int|ExtValue[int]
    """
    **Sampling period while waiting**
    
    "Performance sampling period" for the stabilization phase.
    """
    killnostable: int|ExtValue[int]
    """
    **Kill if no stabilization after**
    
    Creatures that fail to stabilize after the specified waiting period (e.g. because they are continuously rolling) will be killed. 0 disables this feature.
    """
    stabledist: float|ExtValue[float]
    """
    **Allowed distance to be stable**
    
    A creature is considered stabilized when its center of gravity stays within the specified distance after the "Sampling period while waiting" has elapsed.
    """
    enableperf: int|ExtValue[int]
    """
    **Performance calculation**
    
    Replaced by initial_perf_measuring
    """
    initial_perf_measuring: int|ExtValue[int]
    """
    **Performance calculation**
    
    Stabilization means no significant movement during a specified period of time. See https://www.framsticks.com/a/al_params.html#exper-perfcalc
    """
    colmask: int|ExtValue[int]
    """
    **Collision mask**
    
    You should use selfmask and othermask instead of colmask (these masks are also much easier to understand than the old colmask field).
    """
    selfmask: int|ExtValue[int]
    """
    **Collision mask (self)**
    
    Collisions between objects can be handled in two ways:
     - standard 'mechanical' collision handler (simple 'rebound' effect)\n
     - special script handler (On[GROUPNAME]Collision function)
    
    In the script handler function, use the Collision object to access the two colliding parts of two creatures.\n
    The first part in the Collision object (i.e. Collision.Creature1) always concerns the creature that belongs to [GROUPNAME].\n
    The handler is called once for each creature that collides with the creature from [GROUPNAME].
    
    Collision masks that you set determine which handler will be used (none and both are also possible). On each collision, selfmask and othermask of the colliding objects are logically ANDed.\n
    If the resulting non-zero value falls into 16 lower bits (0x0000ffff), the standard handler is enabled.\n
    If the resulting non-zero value falls into 16 higher bits (0xffff0000), the custom handler is enabled.
    
    Examples:
    
    1.With one group, all possible combinations of the collision handlers are as follows:
    	- ignore collisions (e.g. selfmask=othermask=0)\n
    	- use standard handling (e.g. selfmask=othermask=1)\n
    	- use custom handling (e.g. selfmask=othermask=0x10000)\n
    	- use standard and custom handling (e.g. selfmask=othermask=0x10001)
    
    2.Two groups yield more interesting cases. Let us consider the 'standard.expdef' setting:
    	Creatures: selfmask=0x10001, othermask=0x20001\n
    	Food: selfmask=0x20002, othermask=0x10002
    There are three possible scenarios:
    	- creature and creature: collision value = 0x10001 & 0x20001 = 1 -> Standard handling will be used (1 is one of the lower 16 bits)\n
    	- food and food: collision value = 0x20002 & 0x10002 = 2 -> As above.\n
    	- creature and food: collision value = (0x10001 & 0x10002) or (0x20002 & 0x20001) = 0x10000 or 0x20000 -> Custom handling will be used (the result falls into higher 16 bits).
    
    
    Instead of manually calculating mask values, you can use this interactive graphical helper: https://www.framsticks.com/files/apps/js/population-mask-helper/index.html
    """
    othermask: int|ExtValue[int]
    """
    **Collision mask (other)**
    
    See selfmask.
    """
    bodysim: int|ExtValue[int]
    """
    **Body simulation**
    
    Replaced by initial_physics_active
    """
    initial_physics_active: int|ExtValue[int]
    """
    **Body simulation**
    
    Enable/disable physical body simulation. This is the initial value of Creature.physics_active for all objects created in this group. For details, see the documentation of Creature.physics_active.
    """
    selfcol: int|ExtValue[int]
    """
    **Detect self-collisions**
    
    Replaced by initial_self_collisions
    """
    initial_self_collisions: int|ExtValue[int]
    """
    **Detect self-collisions**
    
    Detect collisions within creature bodies (only applicable for the ODE simulation engine). This is the initial value of Creature.self_collisions for all objects created in this group. If enabled, creatures with self-colliding genotypes are not born, and others will have their sticks collide during lifespan.
    """
    em_stat: float|ExtValue[float]
    """
    **Muscle static work**
    
    Energy consumption of a muscle resisting an external force (whether performing or not performing any physical work). Framsticks muscles cannot be "turned off", but they can stop consuming "static" energy when the body part keeps itself in the requested position without stressing the muscle, e.g. when floating in the water or resting freely on the ground.
    """
    em_dyn: float|ExtValue[float]
    """
    **Muscle dynamic work**
    
    Energy consumption of a muscle moving a stick, calculated from the actual work performed by the muscle. Muscles must move to consume this kind of energy.
    """
    en_assim: float|ExtValue[float]
    """
    **Assimilation productivity**
    
    Maximal energy gain produced by a vertical specialized stick.\n
    Horizontal specialized sticks get half of this value.
    """
    @staticmethod
    @deprecated
    def createFromGenotype() -> Creature:
        """
        Uses the selected Genotype object.\n
        Deprecated. Use the more universal add() function.
        """
        ...

    @staticmethod
    @deprecated
    def createFromString(genotype: str|ExtValue[str]) -> Creature:
        """
        Uses the supplied string argument.\n
        Deprecated. Use the more universal add() function.
        """
        ...

    @staticmethod
    @deprecated
    def createFromGeno(arg1: Geno) -> Creature:
        """
        Uses the supplied Geno object.\n
        Deprecated. Use the more universal add() function.
        """
        ...

    @staticmethod
    def add(Genotype_object_or_Geno_object_or_string_genotype_or_CreatureSnapshot_object: Any|ExtValue[Any]) -> Creature:
        """
        Adding CreatureSnapshot object automatically copies the CreatureSnapshot fields into the Creature, including creature location (the center of the bounding box is preserved) and orientation.\n
        See also: CreatureSnapshot
        """
        ...

    @staticmethod
    def canAdd(Genotype_object_or_Geno_object_or_string_genotype_or_CreatureSnapshot_object: Any|ExtValue[Any], treat_warnings_as_errors: int|ExtValue[int], mute: int|ExtValue[int]) -> int|ExtValue[int]:
        """
        Check if the creature could be built from the supplied argument, as if add() was called - this is equivalent to add()ing a creature and immediately removing it, but without the side effects of onBorn().\n
        The mandatory second argument means: -1=obey the current simulator setting for "Don't simulate genotypes with warnings", 0=warnings during creature building are acceptable, 1=treat such warnings as a build failure (cannot add).\n
        Errors/warnings are emitted like in add(), unless mute=1.
        """
        ...

    @staticmethod
    def findUID(uid: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Find a Creature by UID** """
        ...

    @staticmethod
    def get(index: int|ExtValue[int]) -> Creature:
        """ **get creature object** """
        ...

    @staticmethod
    def senseCreaturesProperty(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float], propertyname: str|ExtValue[str], exclude: Creature) -> float|ExtValue[float]:
        """
        Arguments:
         - x,y,z (sensor position)\n
         - property (name, data[key] or Class:id). "data[key]" can be used to access Creature's data field (Dictionary) containing named items\n
         - exclude (creature object)
        
        This function works like a smell sensor (but you can provide any property as the argument, not just "energy") for all creatures in this group except "exclude".\n
        The following is a sample function that reproduces the "S" sensor which smells creatures from all populations:
        	function smellEnergyAllPopulations(x, y, z, exclude)\n
        	{
        		var s=0;\n
        		for(var i=0; i<Populations.size; i++)
        			s += Populations[i].senseCreaturesProperty(x, y, z, "energy", exclude);
        		return s;
        	}
        """
        ...

    @staticmethod
    def findCreatureAt(point: Vector, vector: Vector) -> Creature:
        """
        **Find creature**
        
        Returns the first Creature object colliding with the line defined by the supplied starting point and the vector. For the purpose of this function, "collision" means "passing closer than 1.0 from any of the Creature's Parts".\n
        Note that a screen point corresponds to a 3D line going through the screen surface; if you want to identify the object under the mouse cursor, you can use this function because finding an object at a given screen coordinates can be a special case of finding the line-with-object collision.
        """
        ...

    @staticmethod
    def delete(Creature_object_or_index: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ Delete the creature (remove it without executing the onKill event). Removing creatures inside some event handlers (e.g. onCollision) might be unsafe. """
        ...

    @staticmethod
    def kill(Creature_object_or_index: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ Kill the creature (remove it and execute its onKill handler). Killing creatures inside some event handlers (e.g. onCollision) might be unsafe. The recommended and safe way of killing a creature is by setting its energy to 0. """
        ...

    @staticmethod
    def clear() -> None|ExtValue[None]:
        """ Delete all creatures """
        ...

    iterator: Object
    @staticmethod
    def getStatsMin(field_name: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **get stats minimum**
        
        Retrieves data from stats.* object. Can only be used for fields covered by stats.* (subset of Creature fields).
        """
        ...

    @staticmethod
    def getStatsAvg(field_name: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **get stats average**
        
        Retrieves data from stats.* object. Can only be used for fields covered by stats.* (subset of Creature fields).
        """
        ...

    @staticmethod
    def getStatsMax(field_name: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **get stats maximum**
        
        Retrieves data from stats.* object. Can only be used for fields covered by stats.* (subset of Creature fields).
        """
        ...

    @staticmethod
    def refreshGUI() -> None|ExtValue[None]:
        """
        **Refresh GUI**
        
        Notify list content changed
        """
        ...


class Populations(metaclass=PopulationsIndexer):
    """
    Manages all Creature objects in the experiment, organized in one or more groups.\n
    You can iterate directly over Population objects in the Populations collection using for(...in...) loops:
    	for(var pop in Populations) Simulator.print(pop.name);
    
    Before version 4.0rc4, some operations could only be performed on the "selected" creature (the one pointed to by group/creature fields in Populations). Currently, the more convenient and recommended way is to call Creatures's functions that operate directly on the passed objects.
    
    The old way:
    	Populations.group=0;\n
    	Populations.creature=0;\n
    	GenePools.getFromCreature();\n
    	GenePools.copyTo(0);
    
    Doing the same the new way:
    	Genotype.newFromCreature(Populations[0][0]).moveTo(GenePools[0]);
    
    See also: Creature, Population.
    """

    group: int|ExtValue[int]
    """
    **selected group**
    
    Index of the currently selected group (Population).\n
    Deprecated. Pass creature object to functions needing it, instead of the old "first select, then call" approach.
    """
    size: int|ExtValue[int]
    """ **Number of groups** """
    creature: int|ExtValue[int]
    """
    **selected creature**
    
    Deprecated. Pass creature object to functions needing it, instead of the old "first select, then call" approach.
    """
    @staticmethod
    @deprecated
    def createFromGenotype() -> Creature:
        """ Uses the selected Genotype object. """
        ...

    @staticmethod
    @deprecated
    def createFromString(genotype: str|ExtValue[str]) -> Creature:
        """ Uses the supplied string argument. """
        ...

    @staticmethod
    @deprecated
    def killSelected() -> None|ExtValue[None]:
        """ Applies to the selected Creature. """
        ...

    @staticmethod
    @deprecated
    def deleteSelected() -> None|ExtValue[None]:
        """ Applies to the selected Creature. """
        ...

    @staticmethod
    def addGroup(name: str|ExtValue[str]) -> Population:
        """ Adds a new population. """
        ...

    @staticmethod
    def deleteGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """ Removes a population. """
        ...

    @staticmethod
    def clear() -> None|ExtValue[None]:
        """ Removes all populations except the first one. """
        ...

    @staticmethod
    @deprecated
    def clearGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        Deprecated.\n
        Use Populations[pop_index].clear() instead of Populations.clearGroup(pop_index);
        """
        ...

    @staticmethod
    @deprecated
    def creatBBCollisions(mask: int|ExtValue[int]) -> int|ExtValue[int]:
        """
        Checks approximate collisions for the selected creature.\n
        Returns the collision mask calculated as ( creature.selfmask & other_creatures.othermask ).\n
        Passing non-zero argument is equivalent to setting a temporary selfmask for the current creature.
        
        Deprecated. Use Creature.boundingBoxCollisions()
        """
        ...

    @staticmethod
    def get(index: int|ExtValue[int]) -> Population:

        ...

    @staticmethod
    def findCreatureAt(point: Vector, vector: Vector) -> Creature:
        """
        **Find creature**
        
        Returns the first Creature object colliding with the line defined by the supplied starting point and the vector. For the purpose of this function, "collision" means "passing closer than 1.0 from any of the Creature's Parts".\n
        Note that a screen point corresponds to a 3D line going through the screen surface; if you want to identify the object under the mouse cursor, you can use this function because finding an object at a given screen coordinates can be a special case of finding the line-with-object collision.
        """
        ...

    iterator: Object

class POVExport(ExtValue):


    povex_outdir: str|ExtValue[str]
    """
    **Output directory**
    
    Directory name WITHOUT trailing '/' sign
    """
    povex_outfiles: str|ExtValue[str]
    """
    **Output files pattern**
    
    Frame number replaces %d (e.g., 'scene%03d.pov')
    """
    povex_skip: int|ExtValue[int]
    """
    **Skip frames**
    
    A scene file is generated each (n+1) simulation steps\n
    (a small value means more frames and smooth animation)
    """
    povex_startf: int|ExtValue[int]
    """
    **Starting frame#**
    
    Starting number
    """
    povex_maxframes: int|ExtValue[int]
    """
    **Maximum frames**
    
    How many frames are to be generated?
    """
    povex_dust: int|ExtValue[int]
    """ **Dust particles** """
    povex_energy: int|ExtValue[int]
    """ **Energy particles** """
    @staticmethod
    def povex_enable():
        """ **Enable export** """
        ...

    @staticmethod
    def povex_disable():
        """ **Disable export** """
        ...

    @staticmethod
    def povex_now():
        """ **Export current scene** """
        ...

    povex_currframe: int|ExtValue[int]
    """ **Next frame#** """
    povex_enabled: int|ExtValue[int]
    """ **Export enabled** """
    povex_lastfile: str|ExtValue[str]
    """ **Last filename** """

class Ref(ExtValue):
    """
    Reference objects. Useful for returning things from functions.
    
    Example:\n
    var x=111;\n
    square(&x);// '&' creates the Reference object\n
    Simulator.print(x);//x is now 12321
    
    function square(r)\n
    {r.value=r.value*r.value;}\n
    //square receives the Reference object and changes its 'value' field
    """

    value: Any|ExtValue[Any]
    @staticmethod
    def newO():
        """
        **create new reference**
        
        (for internal use only) use &variablename to create Ref objects.
        """
        ...

    @staticmethod
    def copyFrom(arg1: Ref) -> None|ExtValue[None]:
        """
        **copy the reference**
        
        make the reference point to the same target,
        """
        ...

    toString: str|ExtValue[str]
    """ **textual form** """

class Signal(ExtValue):
    """
    Signals broadcast information in a channel (being an abstract communication medium that could be imagined as sound, smell, vision or anything else). There are no sender-receiver associations, although the receiving party can filter out signals (two standard filtering methods are: physical neighborhood and one-dimensional attribute called flavor). Signals attached to neurons and creatures (created in Creature.signals and Neuro.signals) automatically follow the owner's location. Environmental signals (in World.signals) are stationary.
    
    Receiving: \n
    There are 2 kinds of data you can receive:\n
    1. aggregating functions (receive and receiveFilter) calculate the overall power of the received signal (based on the distance and the source power).\n
    2. receiveSet and receiveSingle fetch the individual Signal object(s) so it is possible to transmit something else than just a single number (by using Signal.value) and do more sophisticated processing.
    
    Creating: Use "add" in Creature.signals, Neuro.signals, or World.signals.
    """

    value: Any|ExtValue[Any]
    """ Signal value can be any type. On the receiver side it is only available by accessing the individual Signal objects, i.e. after calling receiveSet() or receiveSingle(). The aggregating functions receive() and receiveFilter() ignore this attribute. """
    power: float|ExtValue[float]
    """ Signal power affects the aggregated signal value returned from receive() and receiveFilter(). """
    flavor: float|ExtValue[float]
    """ Signal flavor can be used to differentiate between signals in a single channel. """
    channel: str|ExtValue[str]
    """
    **Channel name**
    
    Channel name, read-only.
    """
    pos: XYZ
    """
    **Position**
    
    Signal position, read-only.
    """
    @staticmethod
    def remove():
        """ Deletes the signal. """
        ...


class SignalView(ExtValue):
    """ This object can be used by an Experiment Definition or a Framsticks Theater show script to configure the preferred Signal visualization in the experiment. SignalView.mode and SignalView.label can also be adjusted in the Framsticks GUI (overriding the script-configured state). """

    @staticmethod
    def clear():
        """
        **Clear 'Custom' mode settings**
        
        Removes custom display settings that might have been defined by various scripts (expdef or show).
        """
        ...

    mode: int|ExtValue[int]
    """ "Automatic" labels all signal sources in all channels and shows the intensity map of the first channel. This is sufficient for many simple setups, but as the number of signals and channels grows, the display becomes cluttered. In such cases, the experiment definition can define "Custom" signal visualization tailored for the particular experiment. """
    labels: str|ExtValue[str]
    """
    The label formula should return text to be displayed over the signal source, presumably by reading some values from the supplied Signal object. It is especially useful for more sophisticated signal usage scenarios, when Signal.value keeps a reference to an object (the default signal label only shows <XXX Object at xxxxx> in such cases).
    
    Examples: (switch to "Automatic" mode to see labels, then remove the label formula and compare the effect)
    
    return "x";\n
    return "val="+Signal.value;\n
    return "power="+Signal.power;
    """
    @staticmethod
    def addMap(channel: str|ExtValue[str], color: int|ExtValue[int]) -> None|ExtValue[None]:
        """ **add channel** """
        ...

    @staticmethod
    def addSignals(channel: str|ExtValue[str], color: int|ExtValue[int], angle_x: int|ExtValue[int], angle_y: int|ExtValue[int], angle_z: int|ExtValue[int]) -> None|ExtValue[None]:
        """ **add channel** """
        ...

    @staticmethod
    def addSignalsFilter(channel: str|ExtValue[str], color: int|ExtValue[int], angle_x: int|ExtValue[int], angle_y: int|ExtValue[int], angle_z: int|ExtValue[int], flavor: int|ExtValue[int], filter: int|ExtValue[int]) -> None|ExtValue[None]:
        """ **add channel** """
        ...


class sim_params(ExtValue):
    """ This object groups all simulator parameters so they can be loaded or saved with a single call (see scripts/standard_loadsave.inc). For other purposes please use specific objects, like Simulator, World, Populations, etc. """

    @staticmethod
    def print(text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Print information message**
        
        One argument: message to be printed.
        """
        ...

    @staticmethod
    def message(text: str|ExtValue[str], level: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Print message**
        
        The second argument can be:
         -1 = debugging message\n
         0 = information\n
         1 = warning\n
         2 = error\n
         3 = critical error
        """
        ...

    @staticmethod
    def sleep(milliseconds: int|ExtValue[int]) -> None|ExtValue[None]:
        """ Suspends the execution for a specified interval. """
        ...

    @staticmethod
    def beep() -> None|ExtValue[None]:
        """ Plays the default system sound. """
        ...

    @staticmethod
    def sound(freqency_in_Hz: int|ExtValue[int], length_in_milliseconds: int|ExtValue[int]) -> None|ExtValue[None]:
        """ Generates a simple tone on the speaker """
        ...

    @staticmethod
    def eval(script_statement: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Evaluate a statement**
        
        The argument must be a complete statement, e.g. "return 2+2;" is valid, while "2+2" is not. The Error object is returned for invalid statements.\n
        Example:\n
        var statement="function fun(a) {return a*a;} return fun(Math.pi);";\n
        var result=Simulator.eval(statement);\n
        if (typeof result=="Error")
           Simulator.print("Error:"+result.message);
        else
           Simulator.print("Result:"+result);
        """
        ...

    @staticmethod
    def load(filename: str|ExtValue[str]) -> None|ExtValue[None]:
        """ Load experiment file (calls onExpLoad() in the current experiment definition). This function is intended to replace the simulator state; the old state is cleared by automatically calling "resetToDefaults()". Use "import" if you don't want to lose the old simulator state. Contents can also be loaded from string by using specifically formed filename: "string://string_contents_to_be_loaded". """
        ...

    @overload
    @staticmethod
    def import_(filename: str|ExtValue[str], options: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        Import some data from file. Contents can also be imported from string by using specifically formed filename: "string://string_contents_to_be_imported".\n
        The second optional argument selects what section(s) will be imported:
        	1 - experiment (works just like load(), all other bits are ignored, and can reset the simulator state!)\n
        	2 - genotypes\n
        	4 - simulator parameters\n
        	8 - genepool settings\n
        	16 - population settings\n
        	32 - new groups will be created for imported genepools and populations\n
        	64 - allow switching to a different expdef while importing parameters (4)\n
        	256 - creatures
        
        The standard behavior (without the second argument) is to import genotypes, parameters, and genepool and population settings (2+4+8+16). Note that "64" is not included by default, because the expdef change resets all simulator parameters, which contradicts the usual meaning of "import" in Framsticks ("add data", as opposed to "load" meaning "replace data"). Moreover, using the "64" option in scripts can be dangerous, especially all expdef and show scripts should always declare the proper expdef name in their header rather than change the expdef directly. Without the "64" option, it is always safe to "import" any file in a script regardless of the current simulator state.
        """
        ...

    @overload
    @staticmethod
    def import_(filename: str|ExtValue[str]) -> None|ExtValue[None]:
        """ Equivalent to import(filename,2+4+8+16) - imports genotypes, parameters, genepool and population settings. """
        ...

    @staticmethod
    def save(filename: str|ExtValue[str]) -> Any|ExtValue[Any]:
        """ Save experiment file (calls onExpSave() in the current experiment definition). Providing null filename makes save() return saved data as a text string instead of writing it to the file. """
        ...

    @staticmethod
    def export(filename: str|ExtValue[str], options: int|ExtValue[int], genepool: int|ExtValue[int], population: int|ExtValue[int]) -> Any|ExtValue[Any]:
        """
        Save some data to file. Arguments:\n
        - filename: can be null, which makes export() return saved data as a text string instead of writing it to the file.\n
        - options: composed of the following bit values:
        	1 - experiment (works just like save() and all other option bits are ignored)\n
        	2 - genotypes\n
        	4 - simulator parameters\n
        	8 - simulator stats\n
        	16 - genepool settings\n
        	32 - population settings\n
        	64 - do autosave\n
        	256 - creatures
        - selected genepool, -1 means all genepools\n
        - selected population, -1 means all populations
        """
        ...

    @staticmethod
    def start() -> None|ExtValue[None]:
        """
        **Start simulation**
        
        Called by the user interface.
        """
        ...

    @staticmethod
    def stop() -> None|ExtValue[None]:
        """
        **Stop simulation**
        
        The expdef script calls this function to stop simulation.
        """
        ...

    running: int|ExtValue[int]
    """
    **Is the simulation running?**
    
    Useful for synchronizing the user interface state.
    """
    stop_on: int|ExtValue[int]
    """
    **Error level to stop running simulation**
    
    If the simulation is running and a message is emitted with at least the selected severity, the simulation will be stopped.
    """
    @staticmethod
    def step() -> None|ExtValue[None]:
        """ **Do a single simulation step** """
        ...

    time: int|ExtValue[int]
    """
    **Number of steps**
    
    Simulator.time will be removed because of its misleading name, please use Simulator.stepNumber instead.
    """
    last_genotype_num: int|ExtValue[int]
    """
    **Largest previously used Genotype.num**
    
    See: Genotype.num
    """
    last_creature_num: int|ExtValue[int]
    """
    **Largest previously used Creature.num**
    
    See: Creature.num
    """
    stepNumber: int|ExtValue[int]
    """ **Number of simulation steps** """
    simspeed: int|ExtValue[int]
    """
    **Simulation speed**
    
    steps/second
    """
    expdef: str|ExtValue[str]
    """
    **Experiment definition**
    
    Choose the experiment framework\n
    (in Windows GUI, confirm by pressing 'Apply')
    
    Stop the simulation before selecting another experiment definition.\n
    It is a good practice to initialize the experiment before running the simulation.
    """
    expdef_title: str|ExtValue[str]
    """ **Title** """
    expdef_info: str|ExtValue[str]
    """ **Description** """
    @staticmethod
    def init() -> None|ExtValue[None]:
        """
        **Initialize experiment**
        
        Prepares the experiment for running - usually performs initialization procedures such as resetting counters, states, gene pools, etc.\n
        These actions are defined in the onInit() function of this experiment definition.
        """
        ...

    @staticmethod
    def loadexpdef() -> None|ExtValue[None]:
        """
        **Reload experiment definition**
        
        Resets the simulator to its default state, resets all parameters to default values and then loads this experiment definition.
        """
        ...

    usercode: str|ExtValue[str]
    """
    **Script override**
    
    You can override any function from the original experiment definition script. Use the same function names and provide alternative implementations.\n
    Example:
    
    function onBorn(cr)\n
    {
      Simulator.print("A creature is born: "+cr.name);\n
      super_onBorn(cr); //calls the original implementation
    }
    """
    autosaveperiod: int|ExtValue[int]
    """
    **Save backup**
    
    Save simulation state once every n-th event\n
    (events are defined by the script. For 'standard.expdef' it is after each death).\n
    Save EXPT file first to initialize name for autosave files.\n
    Slave simulators (in multithreaded experiments) ignore this setting and never create autosave files.
    """
    overwrite: int|ExtValue[int]
    """
    **Overwrite files?**
    
    Lets you choose what to do when a file is created with the same name as an already existing file: overwite the existing file or create its backup?
    """
    filecomm: int|ExtValue[int]
    """
    **Show file comments**
    
    Controls displaying comments encountered in opened files.
    """
    @staticmethod
    def checkpoint() -> None|ExtValue[None]:
        """
        **Notify that the experiment state was significantly updated.**
        
        This function was previously called "autosave".
        """
        ...

    @staticmethod
    def checkpointData(any_data: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """
        **Notify that the experiment state was significantly updated + pass data.**
        
        In the distributed/paralellized scenario the data passed as argument can be received by the controlling entity (onSlaveCheckpoint in multithreaded master experiment, /simulator/expevent in distributed network simulator).
        """
        ...

    lastCheckpoint: Any|ExtValue[Any]
    """
    **Last checkpoint**
    
    Most recently reported by the experiment definition script.
    """
    @staticmethod
    def resetToDefaults() -> None|ExtValue[None]:
        """
        **Reset the simulator state**
        
        Clears groups and loads default values for simulator parameters, then calls onExpDefLoad() of the current experiment definition.
        """
        ...

    createrr: int|ExtValue[int]
    """ **Object creation errors** """
    groupchk: int|ExtValue[int]
    """
    **Warn on adding invalid genotypes**
    
    Warnings will be printed when invalid genotypes are added to a gene pool.
    """
    creatwarnfail: int|ExtValue[int]
    """
    **Don't simulate genotypes with warnings**
    
    Creatures grown with warnings will not be simulated. This helps prevent the propagation of faulty genes, because genotypes that cause warnings when interpreted will not reproduce.
    """
    vmdebug: int|ExtValue[int]
    """ **VM debug** """
    vm_step_limit: int|ExtValue[int]
    """
    **VM step limit**
    
    Abort any script (expdef, fitness formula, user script) when it performs too many operations - which can take more or less time depending on your machine performance. This can protect against infinite loops or unbearably long runs of untested scripts that would otherwise force you to kill the whole application. Use Simulator.vm_..._warning if you only need information about what script takes too much time without aborting it.
    """
    vm_step_warning: int|ExtValue[int]
    """
    **VM step warning**
    
    Display a warning when any script (expdef, fitness formula, user script) performs too many operations - which can take more or less time depending on your machine performance. Use Simulator.vm_..._limit to prevent the application from becoming unresponsive by aborting misbehaving scripts.
    """
    vm_time_limit: float|ExtValue[float]
    """
    **VM time limit**
    
    Abort any script (expdef, fitness formula, user script) when it takes too much time - measured in seconds. The actual amount of work depends on your machine performance. This can protect against infinite loops or unbearably long runs of untested scripts that would otherwise force you to kill the whole application. Use Simulator.vm_..._warning if you only need information about what script takes too much time without aborting it.
    """
    vm_time_warning: float|ExtValue[float]
    """
    **VM time warning**
    
    Display a warning when any script (expdef, fitness formula, user script) takes too much time - measured in seconds. The actual amount of work depends on your machine performance. Use Simulator.vm_..._limit to prevent the application from becoming unresponsive by aborting misbehaving scripts.
    """
    @staticmethod
    def new() -> Simulator:
        """ **create new Simulator** """
        ...

    slaves: SlaveSimulators
    """ **Slave simulator objects** """
    cpus: int|ExtValue[int]
    """ **Number of detected CPUs ('cores') on this machine** """
    world: World
    populations: Populations
    genepools: GenePools
    """ **Gene pools object** """
    expproperties: ExpProperties
    expstate: ExpState
    genman: GenMan
    genoconverters: GenoConverters
    """ **Genotype converters object** """
    @staticmethod
    def reloadNeurons() -> None|ExtValue[None]:
        """ **Reload neuron definitions** """
        ...

    userdata: Any|ExtValue[Any]
    """ **User field** """
    identity: int|ExtValue[int]
    """ -1 for master simulator, 0...count-1 for slaves """
    @staticmethod
    def refreshGUI() -> None|ExtValue[None]:
        """
        **Refresh GUI**
        
        Notify that all populations and gene pools content changed.
        """
        ...

    version_string: str|ExtValue[str]
    """
    **Version string**
    
    Current application version as a string (human-friendly).
    """
    version_int: int|ExtValue[int]
    """
    **Version integer**
    
    Current application version as an integer.
    """
    @staticmethod
    def _propertyClear() -> None|ExtValue[None]:
        """
        **Remove all properties**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAdd(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property (id,type,name,help)**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemove(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyChange(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Change property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAddGroup(name: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemoveGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyExists(name: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Check for property existence** """
        ...

    _property_changed_index: int|ExtValue[int]
    """ **Last changed property index** """
    _property_changed_id: str|ExtValue[str]
    """ **Last changed property id** """
    wrldtyp: int|ExtValue[int]
    """ **Type** """
    wrldsiz: float|ExtValue[float]
    """
    **Size**
    
    Side length of the world
    """
    wrldmap: str|ExtValue[str]
    """
    **Map**
    
    Description of the world (only applies to world types: "Blocks" or "Heightfield").\n
    To generate a random landscape, use:
       r[scaling] <sizex> <sizey> [seed]
    To generate a custom landscape, provide height values:
       m[scaling] <sizex> <sizey> digits...
     or
       M[scaling] <sizex> <sizey> numbers...
    
    "digits..." is a sequence of integer values 0,1,2,..,9. You may also use '-' and '|' characters for smooth slides between blocks.\n
    "numbers..." is a sequence of floating point values, so the "M" option provides more freedom.\n
    [scaling] is an optional linear scaling expression in the form of *FACTOR+OFFSET or *FACTOR-OFFSET, for example "r*0.1-2 5 5" creates a 5x5 random map with a 10% amplitude, shifted down by 2.
    
    See also the WorldMap object.
    """
    wrldwat: float|ExtValue[float]
    """ **Water level** """
    wrldbnd: int|ExtValue[int]
    """
    **Boundaries**
    
    Teleporting a creature that is outside of the world area is attempted every 'performance sampling period' steps. Teleport succeeds only when the target location in the world is empty (there is no collision).
    """
    wrldg: float|ExtValue[float]
    """
    **Gravity**
    
    You can adjust gravity for your experiments.\n
    The "official" setting used to evaluate and compare creatures is 1.
    """
    @staticmethod
    def wrldchg() -> None|ExtValue[None]:
        """ **Trigger world update** """
        ...

    simtype: int|ExtValue[int]
    """
    **Simulation engine**
    
    MechaStick is a fast and simple primary Framsticks simulation engine.\n
    ODE is Open Dynamics Engine by Russel Smith et al.
    
    NOTE: switching between simulation engines causes removal of all objects in the world (e.g. creatures).
    """
    nnspeed: float|ExtValue[float]
    """
    **NN speed**
    
    Number of neural network simulation steps in each physics simulation step
    """
    rndcollisions: int|ExtValue[int]
    """
    **Random collision order**
    
    When enabled, custom collision handlers are invoked in random order. This can help remove unfair bias in some experiments - for example where the same collision order in each simulation step would cause some creatures colliding with food to consume energy while other colliding creatures would starve.
    """
    signals: WorldSignals
    """ **Signal sources** """
    odeshape: int|ExtValue[int]
    """ **Stick shape for ball-and-stick models** """
    odestep: float|ExtValue[float]
    """ **Simulation step** """
    odemusclemin: float|ExtValue[float]
    """
    **Muscle min power**
    
    i.e. "mmmmm" in f1
    """
    odemusclemax: float|ExtValue[float]
    """
    **Muscle max power**
    
    i.e. "MMMMM" if f1
    """
    odemusclespeed: float|ExtValue[float]
    """
    **Muscle speed limit**
    
    Muscle state cannot change faster than the supplied value
    """
    odeairdrag: float|ExtValue[float]
    """
    **Drag**
    
    A drag force ("air drag") proportional to the velocity of mass centers of moving parts (ODE's "linear damping")
    """
    oderotdrag: float|ExtValue[float]
    """
    **Rotation drag**
    
    Drag momentum acting on rotating bodies (ODE's "angular damping")
    """
    odewaterdrag: float|ExtValue[float]
    """ **Water drag** """
    odewaterbuoy: float|ExtValue[float]
    """ **Water buoyancy** """
    odeseed: int|ExtValue[int]
    """
    **Randomness**
    
    Affects collisions.\n
    - 'Truly random' is closest to the standard ODE operation. Use Math.seed to influence randomness in ODE collisions.\n
    - 'Deterministic' automatically calculates random seed in each step based on the current simulation (world) state, which makes the simulation repeatable but more random than 'Fixed'.\n
    - 'Fixed' is completely deterministic and does not depend on Math.seed - the same seed value is set before each step. This might negatively affect ODE accuracy.
    """
    odesepsticks: int|ExtValue[int]
    """
    **Separate sticks**
    
    Each stick gets a separate ODE body (like in MechaStick)
    """
    odeworlderp: float|ExtValue[float]
    """
    **ERP**
    
    World ERP (error reduction parameter)
    """
    odeworldcfm: float|ExtValue[float]
    """
    **CFM**
    
    World CFM (constraint force mixing)
    """
    odecolmumin: float|ExtValue[float]
    """
    **Min. friction**
    
    Mu coefficient for Parts with minimal friction (i.e. "fffff" in f1)
    """
    odecolmumax: float|ExtValue[float]
    """
    **Max. friction**
    
    Mu coefficient for Parts with maximal friction (i.e. "FFFFF" in f1)
    """
    odecolbounce: float|ExtValue[float]
    """ **Bounce** """
    odecolbouncevel: float|ExtValue[float]
    """ **Bounce velocity** """
    odecolsoftcfm: float|ExtValue[float]
    """ **Soft CFM** """
    odecolsofterp: float|ExtValue[float]
    """ **Soft ERP** """
    odecol2mumin: float|ExtValue[float]
    """
    **Min. friction**
    
    Mu coefficient for Parts with minimal friction (i.e. "fffff" in f1)
    """
    odecol2mumax: float|ExtValue[float]
    """
    **Max. friction**
    
    Mu coefficient for Parts with maximal friction (i.e. "FFFFF" in f1)
    """
    odecol2bounce: float|ExtValue[float]
    """ **Bounce** """
    odecol2bouncevel: float|ExtValue[float]
    """ **Bounce velocity** """
    odecol2softcfm: float|ExtValue[float]
    """ **Soft CFM** """
    odecol2softerp: float|ExtValue[float]
    """ **Soft ERP** """
    @staticmethod
    def rayIntersection(position_x: float|ExtValue[float], position_y: float|ExtValue[float], position_z: float|ExtValue[float], direction_x: float|ExtValue[float], direction_y: float|ExtValue[float], direction_z: float|ExtValue[float], max_distance: float|ExtValue[float]) -> float|ExtValue[float]:
        """ **ray intersection** """
        ...

    gen_hist: int|ExtValue[int]
    """
    **Remember history of genetic operations**
    
    Required for phylogenetic analysis
    """
    gen_hilite: int|ExtValue[int]
    """
    **Use syntax highlighting**
    
    Use colors for genes?\n
    (slows down viewing/editing of huge genotypes)
    """
    gen_extmutinfo: int|ExtValue[int]
    """
    **Extended mutation info**
    
    If active, information about employed mutation method will be stored in the 'info' field of each mutated genotype.
    """
    @staticmethod
    def operReport() -> None|ExtValue[None]:
        """
        **Operators report**
        
        Show available genetic operators
        """
        ...

    @staticmethod
    def toHTML(genotype: str|ExtValue[str]) -> str|ExtValue[str]:
        """
        **HTMLize a genotype**
        
        returns genotype expressed as colored HTML
        """
        ...

    @staticmethod
    def toHTMLshort(genotype: str|ExtValue[str]) -> str|ExtValue[str]:
        """
        **HTMLize a genotype, shorten if needed**
        
        returns genotype (abbreviated if needed) in colored HTML format
        """
        ...

    @staticmethod
    def toLaTeX(genotype: str|ExtValue[str]) -> str|ExtValue[str]:
        """
        **LaTeXize a genotype**
        
        returns genotype in colored LaTeX format
        """
        ...

    @staticmethod
    def validate(genotype: Geno) -> Geno:
        """ returns validated (if possible) Geno object from supplied Geno """
        ...

    @staticmethod
    def mutate(genotype: Geno) -> Geno:
        """ returns mutated Geno object from supplied Geno """
        ...

    @staticmethod
    def crossOver(genotype1: Geno, genotype2: Geno) -> Geno:
        """ returns crossed over genotype """
        ...

    @staticmethod
    def getSimplest(format: str|ExtValue[str]) -> Geno:
        """
        **Get the simplest genotype**
        
        returns the simplest genotype for a given encoding (format). "0" means f0, "4" means f4, etc.
        """
        ...

    genoper_f0: int|ExtValue[int]
    """ **Operators for f0** """
    genoper_f0s: int|ExtValue[int]
    """ **Operators for f0s** """
    genoper_f1: int|ExtValue[int]
    """ **Operators for f1** """
    genoper_f4: int|ExtValue[int]
    """ **Operators for f4** """
    genoper_f8: int|ExtValue[int]
    """ **Operators for f8** """
    genoper_f9: int|ExtValue[int]
    """ **Operators for f9** """
    genoper_fF: int|ExtValue[int]
    """ **Operators for fF** """
    genoper_fn: int|ExtValue[int]
    """ **Operators for fn** """
    genoper_fB: int|ExtValue[int]
    """ **Operators for fB** """
    genoper_fH: int|ExtValue[int]
    """ **Operators for fH** """
    genoper_fL: int|ExtValue[int]
    """ **Operators for fL** """
    genoper_fS: int|ExtValue[int]
    """ **Operators for fS** """
    neuadd_N: int|ExtValue[int]
    """
    **Neuron (N)**
    
    Standard neuron
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       Inertia (in) float 0..1 (default 0.8)\n
       Force (fo) float 0..999 (default 0.04)\n
       Sigmoid (si) float -99999..99999 (default 2)\n
       State (s) float -1..1 (default 0)
    """
    neuadd_Nu: int|ExtValue[int]
    """
    **Unipolar neuron [EXPERIMENTAL!] (Nu)**
    
    Works like standard neuron (N) but the output value is scaled to 0...+1 instead of -1...+1.\n
    Having 0 as one of the saturation states should help in "gate circuits", where input signal is passed through or blocked depending on the other singal.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       Inertia (in) float 0..1 (default 0.8)\n
       Force (fo) float 0..999 (default 0.04)\n
       Sigmoid (si) float -99999..99999 (default 2)\n
       State (s) float -1..1 (default 0)
    """
    neuadd_G: int|ExtValue[int]
    """
    **Gyroscope (G)**
    
    Tilt sensor.\n
    Signal is proportional to sin(angle) = most sensitive in horizontal orientation.\n
    0=the stick is horizontal\n
    +1/-1=the stick is vertical
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Joint
    """
    neuadd_Gpart: int|ExtValue[int]
    """
    **Part Gyroscope (Gpart)**
    
    Tilt sensor. Signal is directly proportional to the tilt angle.\n
    0=the part X axis is horizontal\n
    +1/-1=the axis is vertical
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    neuadd_T: int|ExtValue[int]
    """
    **Touch (T)**
    
    Touch and proximity sensor (Tcontact and Tproximity combined)\n
    -1=no contact\n
    0=just touching\n
    >0=pressing, value depends on the force applied (not implemented in ODE mode)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       Range (r) float 0..1 (default 1)\n
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    neuadd_Tcontact: int|ExtValue[int]
    """
    **Touch contact (Tcontact)**
    
    Touch sensor.\n
    -1=no contact\n
    0=the Part is touching the obstacle\n
    >0=pressing, value depends on the force applied (not implemented in ODE mode)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    neuadd_Tproximity: int|ExtValue[int]
    """
    **Touch proximity (Tproximity)**
    
    Proximity sensor detecting obstacles along the X axis.\n
    -1=distance is "r" or more\n
    0=zero distance
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       Range (r) float 0..1 (default 1)\n
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    neuadd_S: int|ExtValue[int]
    """
    **Smell (S)**
    
    Smell sensor. Aggregated "smell of energy" experienced from all energy objects (creatures and food pieces).\n
    Close objects have bigger influence than the distant ones: for each energy source, its partial feeling is proportional to its energy/(distance^2)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    neuadd_Constant: int|ExtValue[int]
    """
    **Constant (*)**
    
    Constant value
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_Bend_muscle: int|ExtValue[int]
    """
    **Bend muscle (|)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 0.25)\n
       bending range (r) float 0..1 (default 1)
    """
    neuadd_Rotation_muscle: int|ExtValue[int]
    """
    **Rotation muscle (@)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 1)
    """
    neuadd_M: int|ExtValue[int]
    """
    **Muscle for solids (M)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 1)\n
       axis (a) integer 0..1 (default 0)
    """
    neuadd_D: int|ExtValue[int]
    """
    **Differentiate (D)**
    
    Calculate the difference between the current and previous input value. Multiple inputs are aggregated with respect to their weights
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_Fuzzy: int|ExtValue[int]
    """
    **Fuzzy system [EXPERIMENTAL!] (Fuzzy)**
    
    Refer to publications to learn more about this neuron.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       number of fuzzy sets (ns) integer\n
       number of rules (nr) integer\n
       fuzzy sets (fs) string (default "")\n
       fuzzy rules (fr) string (default "")
    """
    neuadd_VEye: int|ExtValue[int]
    """
    **Vector Eye [EXPERIMENTAL!] (VEye)**
    
    Refer to publications to learn more about this neuron.
    
    Characteristics:
       uses single input\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       target.x (tx) float\n
       target.y (ty) float\n
       target.z (tz) float\n
       target shape (ts) string (default "")\n
       perspective (p) float 0.1..10 (default 1)\n
       scale (s) float 0.1..100 (default 1)\n
       show hidden lines (h) integer 0..1 (default 0)\n
       output lines count (each line needs four channels) (o) integer 0..99 (default 0)\n
       debug (d) integer 0..1 (default 0)
    """
    neuadd_VMotor: int|ExtValue[int]
    """
    **Visual-Motor Cortex [EXPERIMENTAL!] (VMotor)**
    
    Must be connected to the VEye and properly set up. Refer to publications to learn more about this neuron.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       number of basic features (noIF) integer\n
       number of degrees of freedom (noDim) integer\n
       parameters (params) string
    """
    neuadd_Sti: int|ExtValue[int]
    """
    **Sticky [EXPERIMENTAL!] (Sti)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Part
    """
    neuadd_LMu: int|ExtValue[int]
    """
    **Linear muscle [EXPERIMENTAL!] (LMu)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0.01..1 (default 1)
    """
    neuadd_Water: int|ExtValue[int]
    """
    **Water detector (Water)**
    
    Output signal:\n
    0=on or above water surface\n
    1=under water (deeper than 1)\n
    0..1=in the transient area just below water surface
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    neuadd_Energy: int|ExtValue[int]
    """
    **Energy level (Energy)**
    
    The current energy level divided by the initial energy level.\n
    Usually falls from initial 1.0 down to 0.0 and then the creature dies. It can rise above 1.0 if enough food is ingested
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_Ch: int|ExtValue[int]
    """
    **Channelize (Ch)**
    
    Combines all input signals into a single multichannel output; Note: ChSel and ChMux are the only neurons which support multiple channels. Other neurons discard everything except the first channel.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_ChMux: int|ExtValue[int]
    """
    **Channel multiplexer (ChMux)**
    
    Outputs the selected channel from the second (multichannel) input. The first input is used as the selector value (-1=select first channel, .., 1=last channel)
    
    Characteristics:
       uses 2 inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_ChSel: int|ExtValue[int]
    """
    **Channel selector (ChSel)**
    
    Outputs a single channel (selected by the "ch" parameter) from multichannel input
    
    Characteristics:
       uses single input\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       channel (ch) integer
    """
    neuadd_Rnd: int|ExtValue[int]
    """
    **Random noise (Rnd)**
    
    Generates random noise (subsequent random values in the range of -1..+1)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    neuadd_Sin: int|ExtValue[int]
    """
    **Sinus generator (Sin)**
    
    Output frequency = f0+input
    
    Characteristics:
       uses single input\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       base frequency (f0) float -1..1 (default 0.0628319)\n
       time (t) float 0..6.28319 (default 0)
    """
    f0_nodel_tag: int|ExtValue[int]
    """
    **Respect the 'delete inhibit' tag**
    
    You can tag elements using their 'i' field and the i="mi=d" tag.\n
    Mutations will not delete such elements.\n
    The i="mi=dm" combination is allowed.
    """
    f0_nomod_tag: int|ExtValue[int]
    """
    **Respect the 'modify inhibit' tag**
    
    You can tag elements using their 'i' field and the i="mi=m" tag.\n
    Mutations will not modify properties of such elements.\n
    The i="mi=md" combination is allowed.
    """
    f0_p_new: float|ExtValue[float]
    """ **New part** """
    f0_p_del: float|ExtValue[float]
    """ **Delete part** """
    f0_p_swp: float|ExtValue[float]
    """ **Swap parts** """
    f0_p_pos: float|ExtValue[float]
    """ **Position** """
    f0_p_den: float|ExtValue[float]
    """
    **Density**
    
    Density only has an influence under water
    """
    f0_p_frc: float|ExtValue[float]
    """ **Friction** """
    f0_p_ing: float|ExtValue[float]
    """ **Ingestion** """
    f0_p_asm: float|ExtValue[float]
    """
    **Assimilation**
    
    The interpretation and influence of this property must be implemented by the experiment definition
    """
    f0_p_color: float|ExtValue[float]
    """
    **Visual only: color**
    
    If this value is above zero, apart from this mutation occurring, the color of every newly created gray Part will be mutated on creation
    """
    f0_j_new: float|ExtValue[float]
    """ **New joint** """
    f0_j_del: float|ExtValue[float]
    """ **Delete joint** """
    f0_j_stm: float|ExtValue[float]
    """
    **Stamina**
    
    The interpretation and influence of this property must be implemented by the experiment definition
    """
    f0_j_stf: float|ExtValue[float]
    """ **Stiffness** """
    f0_j_rsf: float|ExtValue[float]
    """ **Rotational stiffness** """
    f0_j_color: float|ExtValue[float]
    """
    **Visual only: color**
    
    If this value is above zero, apart from this mutation occurring, every newly created Joint will be assigned a color that is the average color of both joined Parts
    """
    f0_n_new: float|ExtValue[float]
    """ **New neuron** """
    f0_n_del: float|ExtValue[float]
    """ **Delete neuron** """
    f0_n_prp: float|ExtValue[float]
    """ **Change properties** """
    f0_c_new: float|ExtValue[float]
    """ **New connection** """
    f0_c_del: float|ExtValue[float]
    """ **Delete connection** """
    f0_c_wei: float|ExtValue[float]
    """ **Change weight** """
    f0s_nodel_tag: int|ExtValue[int]
    """
    **Respect the 'delete inhibit' tag**
    
    You can tag elements using their 'i' field and the i="mi=d" tag.\n
    Mutations will not delete such elements.\n
    The i="mi=dm" combination is allowed.
    """
    f0s_nomod_tag: int|ExtValue[int]
    """
    **Respect the 'modify inhibit' tag**
    
    You can tag elements using their 'i' field and the i="mi=m" tag.\n
    Mutations will not modify properties of such elements.\n
    The i="mi=md" combination is allowed.
    """
    f0s_circle_section: int|ExtValue[int]
    """
    **Ensure circle section**
    
    Ensure that ellipsoids and cylinders have circle cross-section
    """
    f0s_use_elli: int|ExtValue[int]
    """ **Use ellipsoids in mutations** """
    f0s_use_cub: int|ExtValue[int]
    """ **Use cuboids in mutations** """
    f0s_use_cyl: int|ExtValue[int]
    """ **Use cylinders in mutations** """
    f0s_p_new: float|ExtValue[float]
    """ **New part** """
    f0s_p_del: float|ExtValue[float]
    """ **Delete part** """
    f0s_p_swp: float|ExtValue[float]
    """ **Swap parts** """
    f0s_p_pos: float|ExtValue[float]
    """ **Position** """
    f0s_p_rot: float|ExtValue[float]
    """ **Rotation** """
    f0s_p_scale: float|ExtValue[float]
    """ **Size (precisely, 'scale')** """
    f0s_p_frc: float|ExtValue[float]
    """ **Friction** """
    f0s_p_ing: float|ExtValue[float]
    """ **Ingestion** """
    f0s_p_asm: float|ExtValue[float]
    """
    **Assimilation**
    
    The interpretation and influence of this property must be implemented by the experiment definition
    """
    f0s_p_color: float|ExtValue[float]
    """
    **Visual only: color**
    
    If this value is above zero, apart from this mutation occurring, the color of every newly created gray Part will be mutated on creation
    """
    f0s_j_new: float|ExtValue[float]
    """ **New joint** """
    f0s_j_del: float|ExtValue[float]
    """ **Delete joint** """
    f0s_j_stm: float|ExtValue[float]
    """
    **Stamina**
    
    The interpretation and influence of this property must be implemented by the experiment definition
    """
    f0s_j_color: float|ExtValue[float]
    """
    **Visual only: color**
    
    If this value is above zero, apart from this mutation occurring, every newly created Joint will be assigned a color that is the average color of both joined Parts
    """
    f0s_n_new: float|ExtValue[float]
    """ **New neuron** """
    f0s_n_del: float|ExtValue[float]
    """ **Delete neuron** """
    f0s_n_prp: float|ExtValue[float]
    """ **Change properties** """
    f0s_c_new: float|ExtValue[float]
    """ **New connection** """
    f0s_c_del: float|ExtValue[float]
    """ **Delete connection** """
    f0s_c_wei: float|ExtValue[float]
    """ **Change weight** """
    f1_xo_propor: int|ExtValue[int]
    """
    **Proportional crossover**
    
    Cross over (exchange) corresponding segments of the two parent genotypes?
    
    f1 uses a two-point crossing over.\n
    If this option is turned on, cut points will be selected proportionally to neural genes in both parents, and a similar number of characters will be exchanged if possible.\n
    Thus, if both parents have the same number of neurons, then this will be preserved in their children.
    """
    f1_smX: float|ExtValue[float]
    """ **Add/remove a stick X** """
    f1_smJunct: float|ExtValue[float]
    """ **Add/remove a branch ( )** """
    f1_smComma: float|ExtValue[float]
    """ **Add/remove a comma ,** """
    f1_smModif: float|ExtValue[float]
    """
    **Add/remove a modifier**
    
    Modifiers: LlRrCcQqFfMmEeWwSsAaIiDdGgBb
    """
    f1_smModifiers: str|ExtValue[str]
    """
    **Allowed modifiers**
    
    Modifier symbols that will be added or deleted during mutation\n
    (from the full set: LlRrCcQqFfMmEeWwSsAaIiDdGgBb).
    
    You may use the extended syntax: after every allowed symbol, you may include its probability value in parentheses.\n
    Without parentheses, all allowed symbols behave as if they had (1.0) appended.\n
    If you include (0.0) after a symbol, this bans that symbol as if it was not present in this string.
    """
    f1_nmNeu: float|ExtValue[float]
    """
    **Add/remove a neuron**
    
    Adds a (connected) neuron or removes a neuron
    """
    f1_nmConn: float|ExtValue[float]
    """ **Add/remove neural connection** """
    f1_nmProp: float|ExtValue[float]
    """ **Add/remove neuron property setting** """
    f1_nmWei: float|ExtValue[float]
    """ **Change connection weight** """
    f1_nmVal: float|ExtValue[float]
    """ **Change property value** """
    f4_mut_add: float|ExtValue[float]
    """
    **Add node**
    
    Mutation: probability of adding a node
    """
    f4_mut_add_div: float|ExtValue[float]
    """
    **- add division**
    
    Add node mutation: probability of adding a division
    """
    f4_mut_add_conn: float|ExtValue[float]
    """
    **- add connection**
    
    Add node mutation: probability of adding a neural connection
    """
    f4_mut_add_neupar: float|ExtValue[float]
    """
    **- add neuron property**
    
    Add node mutation: probability of adding a neuron property/modifier
    """
    f4_mut_add_rep: float|ExtValue[float]
    """
    **- add repetition '#'**
    
    Add node mutation: probability of adding the '#' repetition gene
    """
    f4_mut_add_simp: float|ExtValue[float]
    """
    **- add simple node**
    
    Add node mutation: probability of adding a random, simple gene
    """
    f4_mut_del: float|ExtValue[float]
    """
    **Delete node**
    
    Mutation: probability of deleting a node
    """
    f4_mut_mod: float|ExtValue[float]
    """
    **Modify node**
    
    Mutation: probability of changing a node
    """
    f4_mut_modneu_conn: float|ExtValue[float]
    """
    **- neuron input: modify source**
    
    Neuron input mutation: probability of changing its source neuron
    """
    f4_mut_modneu_weight: float|ExtValue[float]
    """
    **- neuron input: modify weight**
    
    Neuron input mutation: probability of changing its weight
    """
    f4_mut_max_rep: int|ExtValue[int]
    """
    **Maximum number for '#' repetitions**
    
    Maximum allowed number of repetitions for the '#' repetition gene
    """
    f4_mut_modifiers: str|ExtValue[str]
    """
    **Allowed modifiers**
    
    Modifier symbols that will be added or deleted during mutation\n
    (from the full set: LlRrCcQqFfMmEeWwSsAaIiDdGgBb).
    
    You may use the extended syntax: after every allowed symbol, you may include its probability value in parentheses.\n
    Without parentheses, all allowed symbols behave as if they had (1.0) appended.\n
    If you include (0.0) after a symbol, this bans that symbol as if it was not present in this string.
    """
    f8_mut_chg_begin_arg: float|ExtValue[float]
    """
    **Change beginning argument**
    
    mutation: probability of changing a beginning argument
    """
    f8_mut_chg_arg: float|ExtValue[float]
    """
    **Change argument**
    
    mutation: probability of changing a production's argument
    """
    f8_mut_del_comm: float|ExtValue[float]
    """
    **Delete command**
    
    mutation: probability of deleting a command
    """
    f8_mut_insert_comm: float|ExtValue[float]
    """
    **Insert commands**
    
    mutation: probability of inserting commands
    """
    f8_mut_enc: float|ExtValue[float]
    """
    **Encapsulate commands**
    
    mutation: probability of encapsulating commands
    """
    f8_mut_chg_cond_sign: float|ExtValue[float]
    """
    **Change condition sign**
    
    mutation: probability of changing a condition sign
    """
    f8_mut_add_param: float|ExtValue[float]
    """
    **Add parameter**
    
    mutation: probability of adding a parameter to the production
    """
    f8_mut_add_cond: float|ExtValue[float]
    """
    **Add condition**
    
    mutation: probability of adding a condition to the subproduction
    """
    f8_mut_add_subprod: float|ExtValue[float]
    """
    **Add subproduction**
    
    mutation: probability of adding a subproduction
    """
    f8_mut_chg_iter_number: float|ExtValue[float]
    """
    **Change iteration number**
    
    mutation: probability of changing a number of iterations
    """
    f8_mut_del_param: float|ExtValue[float]
    """
    **Delete parameter**
    
    mutation: probability of deleting a parameter
    """
    f8_mut_del_cond: float|ExtValue[float]
    """
    **Delete condition**
    
    mutation: probability of deleting a condition
    """
    f8_mut_add_loop: float|ExtValue[float]
    """
    **Add loop**
    
    mutation: probability of adding a loop
    """
    f8_mut_del_loop: float|ExtValue[float]
    """
    **Delete loop**
    
    mutation: probability of deleting a loop
    """
    f8_mut_del_prod: float|ExtValue[float]
    """
    **Delete production**
    
    mutation: probability of deleting a production
    """
    f9_mut: float|ExtValue[float]
    """
    **Mutation intensity**
    
    How many genes (letters) should be changed during a single genotype mutation (1=all genes, 0.1=ten percent, 0=one gene)
    """
    fF_xover: float|ExtValue[float]
    """
    **Inherited in linear mix crossover**
    
    0.5 => children are averaged parents.\n
    0.8 => children are only 20% different from parents.\n
    1.0 => each child is identical to one parent (no crossover).
    """
    fn_xover: float|ExtValue[float]
    """
    **Fraction inherited in linear mix crossover**
    
    0.5 => children are averaged parents.\n
    0.8 => children are only 20% different from parents.\n
    1.0 => each child is identical to one parent (no crossover).
    """
    fn_xover_random: int|ExtValue[int]
    """
    **Random fraction inherited in crossover**
    
    If active, the amount of linear mix is random in each crossover operation, so the "Fraction inherited in linear mix crossover" parameter is ignored.
    """
    fn_mut_bound_low: str|ExtValue[str]
    """
    **Lower bounds for mutation**
    
    A vector of lower bounds (one real value for each variable)
    """
    fn_mut_bound_high: str|ExtValue[str]
    """
    **Higher bounds for mutation**
    
    A vector of higher bounds (one real value for each variable)
    """
    fn_mut_stddev: str|ExtValue[str]
    """
    **Standard deviations for mutation**
    
    A vector of standard deviations (one real value for each variable)
    """
    fn_mut_single_var: int|ExtValue[int]
    """
    **Mutate only a single variable**
    
    If active, only a single randomly selected variable will be mutated in each mutation operation. Otherwise all variables will be mutated.
    """
    fB_mut_substitute: float|ExtValue[float]
    """
    **Substitution**
    
    Relative probability of changing a single random character (or a neuron) in the genotype
    """
    fB_mut_insert: float|ExtValue[float]
    """
    **Insertion**
    
    Relative probability of inserting a random character in a random place of the genotype
    """
    fB_mut_insert_neuron: float|ExtValue[float]
    """
    **Insertion of a neuron**
    
    Relative probability of inserting a neuron in a random place of genotype
    """
    fB_mut_delete: float|ExtValue[float]
    """
    **Deletion**
    
    Relative probability of deleting a random character (or a neuron) in the genotype
    """
    fB_mut_duplicate: float|ExtValue[float]
    """
    **Duplication**
    
    Relative probability of copying a single *gene* of the genotype and appending it to the beginning of this genotype
    """
    fB_mut_translocate: float|ExtValue[float]
    """
    **Translocation**
    
    Relative probability of swapping two substrings in the genotype
    """
    fB_cross_gene_transfer: float|ExtValue[float]
    """
    **Horizontal gene transfer**
    
    Relative probability of crossing over by copying a single random gene from each parent to the beginning of the other parent
    """
    fB_cross_crossover: float|ExtValue[float]
    """
    **Crossing over**
    
    Relative probability of crossing over by a random distribution of genes from both parents to both children
    """
    fH_mut_addition: float|ExtValue[float]
    """
    **Add element**
    
    Probability of adding a new element
    """
    fH_mut_add_joint: float|ExtValue[float]
    """
    **- add joint**
    
    Probability of adding a new stick handle
    """
    fH_mut_add_neuron: float|ExtValue[float]
    """
    **- add neuron**
    
    Probability of adding a new neuron handle
    """
    fH_mut_add_connection: float|ExtValue[float]
    """
    **- add neural connection**
    
    Probability of adding a new neuron connection handle
    """
    fH_mut_deletion: float|ExtValue[float]
    """
    **Delete element**
    
    Probability of removing an element
    """
    fH_mut_handle: float|ExtValue[float]
    """
    **Modify vectors of handles**
    
    Probability of changing values in vectors of a handle
    """
    fH_mut_property: float|ExtValue[float]
    """
    **Modify properties of handles**
    
    Probability of changing properties of handles
    """
    fL_maxdefinedwords: int|ExtValue[int]
    """
    **Maximum number of defined words**
    
    Maximum number of words that can be defined in the L-System
    """
    fL_axm_mut_prob: float|ExtValue[float]
    """
    **Axiom mutation**
    
    Probability of performing mutation operations on axiom
    """
    fL_rul_mut_prob: float|ExtValue[float]
    """
    **Rule's successor mutation**
    
    Probability of performing mutation operations on the successor of a random rule
    """
    fL_mut_addition: float|ExtValue[float]
    """
    **Addition of a word to a sequence**
    
    Probability of adding a random existing word to the axiom or to one of successors
    """
    fL_mut_add_stick: float|ExtValue[float]
    """
    **- addition of a stick**
    
    Probability of adding a stick
    """
    fL_mut_add_neuro: float|ExtValue[float]
    """
    **- addition of a neuron**
    
    Probability of adding a neuron
    """
    fL_mut_add_conn: float|ExtValue[float]
    """
    **- addition of a neuron connection**
    
    Probability of adding a neuron connection
    """
    fL_mut_add_rot: float|ExtValue[float]
    """
    **- addition of rotation words**
    
    Probability of adding one of rotation words
    """
    fL_mut_add_branch: float|ExtValue[float]
    """
    **- addition of a branched stick**
    
    Probability of adding a branch with a rotation and a stick
    """
    fL_mut_add_other: float|ExtValue[float]
    """
    **- addition of defined words**
    
    Probability of adding another word defined in the genotype
    """
    fL_mut_worddefaddition: float|ExtValue[float]
    """
    **Addition of a new word definition**
    
    Probability of adding a new word definition to the genotype
    """
    fL_mut_ruleaddition: float|ExtValue[float]
    """
    **Addition of a new rule definition**
    
    Probability of adding a new rule definition for an existing word
    """
    fL_mut_rulecond: float|ExtValue[float]
    """
    **Modification of a rule condition**
    
    Probability of modifying a random rule condition
    """
    fL_mut_changeword: float|ExtValue[float]
    """
    **Change a random word**
    
    Probability of changing a word name or a formula of a random word from an axiom or one of successors
    """
    fL_mut_changeword_formula: float|ExtValue[float]
    """
    **- change of a formula**
    
    Probability of changing a formula in a word
    """
    fL_mut_changeword_name: float|ExtValue[float]
    """
    **- change of a name**
    
    Probability of changing a name in a word
    """
    fL_mut_changeiter: float|ExtValue[float]
    """
    **Change the number of iterations**
    
    Probability of changing the number of iterations of the L-System
    """
    fL_mut_changeiter_step: float|ExtValue[float]
    """
    **Step of the iteration change**
    
    The minimal step that should be used for changing iterations in the L-System
    """
    fL_mut_deletion: float|ExtValue[float]
    """
    **Deletion of a random word**
    
    Probability of deleting a random word from an axiom or a random successor (also deletes the rule if there is only one word in the successor)
    """
    fS_mut_add_part: float|ExtValue[float]
    """
    **Add part**
    
    mutation: probability of adding a part
    """
    fS_mut_rem_part: float|ExtValue[float]
    """
    **Remove part**
    
    mutation: probability of deleting a part
    """
    fS_mut_mod_part: float|ExtValue[float]
    """
    **Modify part**
    
    mutation: probability of changing the part type
    """
    fS_mut_change_joint: float|ExtValue[float]
    """
    **Change joint**
    
    mutation: probability of changing a joint
    """
    fS_mut_add_param: float|ExtValue[float]
    """
    **Add param**
    
    mutation: probability of adding a parameter
    """
    fS_mut_rem_param: float|ExtValue[float]
    """
    **Remove param**
    
    mutation: probability of removing a parameter
    """
    fS_mut_mod_param: float|ExtValue[float]
    """
    **Modify param**
    
    mutation: probability of modifying a parameter
    """
    fS_mut_mod_mod: float|ExtValue[float]
    """
    **Modify modifier**
    
    mutation: probability of modifying a modifier
    """
    fS_mut_add_neuro: float|ExtValue[float]
    """
    **Add neuron**
    
    mutation: probability of adding a neuron
    """
    fS_mut_rem_neuro: float|ExtValue[float]
    """
    **Remove neuron**
    
    mutation: probability of removing a neuron
    """
    fS_mut_mod_neuro_conn: float|ExtValue[float]
    """
    **Modify neuron connection**
    
    mutation: probability of changing a neuron connection
    """
    fS_mut_add_neuro_conn: float|ExtValue[float]
    """
    **Add neuron connection**
    
    mutation: probability of adding a neuron connection
    """
    fS_mut_rem_neuro_conn: float|ExtValue[float]
    """
    **Remove neuron connection**
    
    mutation: probability of removing a neuron connection
    """
    fS_mut_mod_neuro_params: float|ExtValue[float]
    """
    **Modify neuron params**
    
    mutation: probability of changing a neuron param
    """
    fS_circle_section: int|ExtValue[int]
    """
    **Ensure circle section**
    
    Ensure that ellipsoids and cylinders have circle cross-section
    """
    fS_use_elli: int|ExtValue[int]
    """
    **Use ellipsoids in mutations**
    
    Use ellipsoids in mutations
    """
    fS_use_cub: int|ExtValue[int]
    """
    **Use cuboids in mutations**
    
    Use cuboids in mutations
    """
    fS_use_cyl: int|ExtValue[int]
    """
    **Use cylinders in mutations**
    
    Use cylinders in mutations
    """
    fS_mut_add_part_strong: int|ExtValue[int]
    """
    **Strong add part mutation**
    
    Add part mutation will produce more parametrized parts
    """
    genoconv_f1_f0: int|ExtValue[int]
    """ **f1 --> f0  :  Recursive encoding** """
    genoconv_f4_f0: int|ExtValue[int]
    """ **f4 --> f0  :  Developmental encoding** """
    genoconv_f8_f1: int|ExtValue[int]
    """ **f8 --> f1  :  (Old) generative encoding** """
    genoconv_f9_f0: int|ExtValue[int]
    """ **f9 --> f0  :  Turtle3D-ortho encoding** """
    genoconv_fF_f0s: int|ExtValue[int]
    """ **fF --> f0s  :  10-parameter Foraminifera encoding** """
    genoconv_fn_f0: int|ExtValue[int]
    """ **fn --> f0  :  Vector of real values, no phenotype** """
    genoconv_fB_fH: int|ExtValue[int]
    """ **fB --> fH  :  Biological encoding** """
    genoconv_fH_f0: int|ExtValue[int]
    """ **fH --> f0  :  Similarity encoding** """
    genoconv_fL_f0: int|ExtValue[int]
    """ **fL --> f0  :  L-System encoding** """
    genoconv_fS_f0s: int|ExtValue[int]
    """ **fS --> f0s  :  Solids tree-structure encoding** """
    conv_f1_f0_modcompat: int|ExtValue[int]
    """
    **Modifier compatibility**
    
    The modern implementation makes the influence of modifiers more consistent and uniform, and the extreme property values are easier to reach with a lower number of characters, which improves the topology for evolutionary search.\n
    Previous implementation can be enabled for compatibility, for example when you want to test old genotypes.
    """
    conv_f1_f0_cq_influence: int|ExtValue[int]
    """
    **'C' and 'Q' modifier influence**
    
    'C' and 'Q' modifier semantics was changed in June 2023. Previously they did not affect the stick immediately following the current sequence of modifiers. In the modern implementation, all modifiers consistently start their influence at the very next stick that is being created in the current branch.\n
    Example:\n
    In the old interpretation of 'XcXX', only the last stick is rotated, because 'c' starts its influence at the stick that occurs after the current stick. In the modern implementation, the same effect is achieved with 'XXcX', where 'c' immediately bends the first 'X' that appears after it.\n
    Previous implementation can be enabled for compatibility, for example when you want to test old genotypes.
    """
    conv_f1_f0_branch_muscle_range: int|ExtValue[int]
    """
    **Bending muscle default range**
    
    Determines how the bending muscle default turning range is limited when the muscle is controlling a stick growing from a branching point that has 'NumberOfBranches' sticks separated by commas. The motivation of the limited range is to keep the neighboring sticks from intersecting when they are bent by muscles. This constraint may degrade the performance (e.g. velocity) of creatures, but this default value can be overridden by providing a specific range property value for the '|' muscle neuron in the genotype.\n
    - Full/NumberOfBranches - a compromise between the two other settings.\n
    - Full/(NumberOfBranches+1) - because the originating stick also counts as a branch. This setting guarantees that in the worst case, when at least two neighboring branches have sticks controlled by bending muscles and their controlling signals are at extreme values, the sticks can touch and overlap, but will not intersect. This setting is in most cases too strict because (1) all branches are very rarely controlled by muscles, (2) there are often 'empty' branches - multiple commas with no sticks in-between, and (3) the share of the originating stick is effectively wasted because this stick itself has no muscle at the branching point so it will not bend; the muscle bending range is symmetrical and the default range is equal for all muscles in a branching, but the sticks equipped with muscles in a branching are rarely evenly spaced.\n
    - Full: always the complete angle - because we do not have to care about the physical plausibility and avoid intersecting sticks, and other genetic representations do not impose such constraints, so this full angle setting can be useful as the default bending range when comparing the performance of various genetic encodings.
    """
    conv_f8_f1_maxlen: int|ExtValue[int]
    """
    **Maximal genotype length**
    
    Maximal length of the resulting f1 genotype, in characters. If the f8 L-system produces longer f1 genotype, it will be considered invalid.
    """
    randinit: float|ExtValue[float]
    """
    **Random initialization**
    
    Allowed range for initializing all neuron states with uniform distribution random numbers and zero mean. Set to 0 for deterministic initialization.
    """
    nnoise: float|ExtValue[float]
    """
    **Noise**
    
    Gaussian neural noise: a random value is added to each neural output in each simulation step. Set standard deviation here to add random noise, or 0 for deterministic simulation.
    """
    touchrange: float|ExtValue[float]
    """ **T receptor range** """
    bnoise_struct: float|ExtValue[float]
    """
    **Body disturbance**
    
    When >0, body constructs of creatures (position of Parts) will be randomly disturbed when they are created.
    """
    bnoise_vel: float|ExtValue[float]
    """
    **Initial movement**
    
    Random velocities will be applied to all body Parts (in MechaStick) or rigid segments (in ODE) of newly created creatures.
    """
    ncl_N: int|ExtValue[int]
    """
    **Neuron (N)**
    
    Standard neuron
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       Inertia (in) float 0..1 (default 0.8)\n
       Force (fo) float 0..999 (default 0.04)\n
       Sigmoid (si) float -99999..99999 (default 2)\n
       State (s) float -1..1 (default 0)
    """
    ncl_Nu: int|ExtValue[int]
    """
    **Unipolar neuron [EXPERIMENTAL!] (Nu)**
    
    Works like standard neuron (N) but the output value is scaled to 0...+1 instead of -1...+1.\n
    Having 0 as one of the saturation states should help in "gate circuits", where input signal is passed through or blocked depending on the other singal.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       Inertia (in) float 0..1 (default 0.8)\n
       Force (fo) float 0..999 (default 0.04)\n
       Sigmoid (si) float -99999..99999 (default 2)\n
       State (s) float -1..1 (default 0)
    """
    ncl_G: int|ExtValue[int]
    """
    **Gyroscope (G)**
    
    Tilt sensor.\n
    Signal is proportional to sin(angle) = most sensitive in horizontal orientation.\n
    0=the stick is horizontal\n
    +1/-1=the stick is vertical
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Joint
    """
    ncl_Gpart: int|ExtValue[int]
    """
    **Part Gyroscope (Gpart)**
    
    Tilt sensor. Signal is directly proportional to the tilt angle.\n
    0=the part X axis is horizontal\n
    +1/-1=the axis is vertical
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    ncl_T: int|ExtValue[int]
    """
    **Touch (T)**
    
    Touch and proximity sensor (Tcontact and Tproximity combined)\n
    -1=no contact\n
    0=just touching\n
    >0=pressing, value depends on the force applied (not implemented in ODE mode)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       Range (r) float 0..1 (default 1)\n
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    ncl_Tcontact: int|ExtValue[int]
    """
    **Touch contact (Tcontact)**
    
    Touch sensor.\n
    -1=no contact\n
    0=the Part is touching the obstacle\n
    >0=pressing, value depends on the force applied (not implemented in ODE mode)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    ncl_Tproximity: int|ExtValue[int]
    """
    **Touch proximity (Tproximity)**
    
    Proximity sensor detecting obstacles along the X axis.\n
    -1=distance is "r" or more\n
    0=zero distance
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       Range (r) float 0..1 (default 1)\n
       rotation.y (ry) float -6.282..6.282 (default 0)\n
       rotation.z (rz) float -6.282..6.282 (default 0)
    """
    ncl_S: int|ExtValue[int]
    """
    **Smell (S)**
    
    Smell sensor. Aggregated "smell of energy" experienced from all energy objects (creatures and food pieces).\n
    Close objects have bigger influence than the distant ones: for each energy source, its partial feeling is proportional to its energy/(distance^2)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    ncl_Constant: int|ExtValue[int]
    """
    **Constant (*)**
    
    Constant value
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_Bend_muscle: int|ExtValue[int]
    """
    **Bend muscle (|)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 0.25)\n
       bending range (r) float 0..1 (default 1)
    """
    ncl_Rotation_muscle: int|ExtValue[int]
    """
    **Rotation muscle (@)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 1)
    """
    ncl_M: int|ExtValue[int]
    """
    **Muscle for solids (M)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0..1 (default 1)\n
       axis (a) integer 0..1 (default 0)
    """
    ncl_D: int|ExtValue[int]
    """
    **Differentiate (D)**
    
    Calculate the difference between the current and previous input value. Multiple inputs are aggregated with respect to their weights
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_Fuzzy: int|ExtValue[int]
    """
    **Fuzzy system [EXPERIMENTAL!] (Fuzzy)**
    
    Refer to publications to learn more about this neuron.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       number of fuzzy sets (ns) integer\n
       number of rules (nr) integer\n
       fuzzy sets (fs) string (default "")\n
       fuzzy rules (fr) string (default "")
    """
    ncl_VEye: int|ExtValue[int]
    """
    **Vector Eye [EXPERIMENTAL!] (VEye)**
    
    Refer to publications to learn more about this neuron.
    
    Characteristics:
       uses single input\n
       provides output value\n
       should be located on a Part
    
    
    Properties:
       target.x (tx) float\n
       target.y (ty) float\n
       target.z (tz) float\n
       target shape (ts) string (default "")\n
       perspective (p) float 0.1..10 (default 1)\n
       scale (s) float 0.1..100 (default 1)\n
       show hidden lines (h) integer 0..1 (default 0)\n
       output lines count (each line needs four channels) (o) integer 0..99 (default 0)\n
       debug (d) integer 0..1 (default 0)
    """
    ncl_VMotor: int|ExtValue[int]
    """
    **Visual-Motor Cortex [EXPERIMENTAL!] (VMotor)**
    
    Must be connected to the VEye and properly set up. Refer to publications to learn more about this neuron.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       number of basic features (noIF) integer\n
       number of degrees of freedom (noDim) integer\n
       parameters (params) string
    """
    ncl_Sti: int|ExtValue[int]
    """
    **Sticky [EXPERIMENTAL!] (Sti)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Part
    """
    ncl_LMu: int|ExtValue[int]
    """
    **Linear muscle [EXPERIMENTAL!] (LMu)**
    
    Characteristics:
       uses single input\n
       does not provide output value\n
       should be located on a Joint
    
    
    Properties:
       power (p) float 0.01..1 (default 1)
    """
    ncl_Water: int|ExtValue[int]
    """
    **Water detector (Water)**
    
    Output signal:\n
    0=on or above water surface\n
    1=under water (deeper than 1)\n
    0..1=in the transient area just below water surface
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       should be located on a Part
    """
    ncl_Energy: int|ExtValue[int]
    """
    **Energy level (Energy)**
    
    The current energy level divided by the initial energy level.\n
    Usually falls from initial 1.0 down to 0.0 and then the creature dies. It can rise above 1.0 if enough food is ingested
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_Ch: int|ExtValue[int]
    """
    **Channelize (Ch)**
    
    Combines all input signals into a single multichannel output; Note: ChSel and ChMux are the only neurons which support multiple channels. Other neurons discard everything except the first channel.
    
    Characteristics:
       supports any number of inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_ChMux: int|ExtValue[int]
    """
    **Channel multiplexer (ChMux)**
    
    Outputs the selected channel from the second (multichannel) input. The first input is used as the selector value (-1=select first channel, .., 1=last channel)
    
    Characteristics:
       uses 2 inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_ChSel: int|ExtValue[int]
    """
    **Channel selector (ChSel)**
    
    Outputs a single channel (selected by the "ch" parameter) from multichannel input
    
    Characteristics:
       uses single input\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       channel (ch) integer
    """
    ncl_Rnd: int|ExtValue[int]
    """
    **Random noise (Rnd)**
    
    Generates random noise (subsequent random values in the range of -1..+1)
    
    Characteristics:
       does not use inputs\n
       provides output value\n
       does not require location in body
    """
    ncl_Sin: int|ExtValue[int]
    """
    **Sinus generator (Sin)**
    
    Output frequency = f0+input
    
    Characteristics:
       uses single input\n
       provides output value\n
       does not require location in body
    
    
    Properties:
       base frequency (f0) float -1..1 (default 0.0628319)\n
       time (t) float 0..6.28319 (default 0)
    """
    simil_type: int|ExtValue[int]
    """ **Type of similarity measure** """
    @staticmethod
    def evaluateDistance(arg1: Geno, arg2: Geno) -> float|ExtValue[float]:
        """
        **Evaluate model dissimilarity**
        
        Calculates dissimilarity between two models created from Geno objects.
        """
        ...

    simil_greedy_parts: float|ExtValue[float]
    """
    **Weight of parts count**
    
    Differing number of parts is also handled by the 'part degree' similarity component.
    """
    simil_greedy_partdeg: float|ExtValue[float]
    """ **Weight of parts' degree** """
    simil_greedy_neuro: float|ExtValue[float]
    """ **Weight of neurons count** """
    simil_greedy_partgeom: float|ExtValue[float]
    """ **Weight of parts' geometric distances** """
    simil_greedy_fixedZaxis: int|ExtValue[int]
    """ **Fix 'z' (vertical) axis?** """
    simil_greedy_weightedMDS: int|ExtValue[int]
    """
    **Should weighted MDS be used?**
    
    If activated, weighted MDS with vertex (i.e., Part) degrees as weights is used for 3D alignment of body structure.
    """
    simil_parts: float|ExtValue[float]
    """
    **Weight of parts count**
    
    Differing number of parts is also handled by the 'part degree' similarity component.
    """
    simil_partdeg: float|ExtValue[float]
    """ **Weight of parts' degree** """
    simil_neuro: float|ExtValue[float]
    """ **Weight of neurons count** """
    simil_partgeom: float|ExtValue[float]
    """ **Weight of parts' geometric distances** """
    simil_fixedZaxis: int|ExtValue[int]
    """ **Fix 'z' (vertical) axis?** """
    simil_weightedMDS: int|ExtValue[int]
    """
    **Should weighted MDS be used?**
    
    If activated, weighted MDS with vertex (i.e., Part) degrees as weights is used for 3D alignment of body structure.
    """
    simil_density: float|ExtValue[float]
    """ **Density of surface sampling** """
    simil_bin_num: int|ExtValue[int]
    """ **Number of bins** """
    simil_samples_num: int|ExtValue[int]
    """ **Number of samples** """
    @staticmethod
    def calculateSymmetry(model: Model) -> float|ExtValue[float]:
        """
        **Calculate symmetry**
        
        Returns bilateral symmetry (0.0 .. 1.0) for a given Model using default precision parameters (symPosSteps,symAlphaSteps,symBetaSteps). Returns the symmetry plane, too (sets symResultA,B,C,D).\n
        Note: may take a long time for large creatures.
        """
        ...

    @staticmethod
    def calculateSymmetry2(model: Model, posSteps: int|ExtValue[int], alphaSteps: int|ExtValue[int], betaSteps: int|ExtValue[int]) -> float|ExtValue[float]:
        """
        **Calculate symmetry**
        
        Returns bilateral symmetry (0.0 .. 1.0) for a given Model using specified precision parameters. Returns the symmetry plane, too (sets symResultA,B,C,D).\n
        Note: may take a long time for large creatures.
        """
        ...

    @staticmethod
    def calculateSymmetryForPlane(model: Model, A: float|ExtValue[float], B: float|ExtValue[float], C: float|ExtValue[float], D: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **Calculate symmetry**
        
        Returns bilateral symmetry (0.0 .. 1.0) for a given Model and given a specific plane defined by coefficients A, B, C, D.
        """
        ...

    symPosSteps: int|ExtValue[int]
    """
    **Position sampling**
    
    Default number of samples per stick length
    """
    symAlphaSteps: int|ExtValue[int]
    """
    **Angular sampling (1)**
    
    Default number of samples per full angle (#1)
    """
    symBetaSteps: int|ExtValue[int]
    """
    **Angular sampling (2)**
    
    Default number of samples per full angle (#2)
    """
    symResultA: float|ExtValue[float]
    """ **resulting symmetry plane, coeff. A (set by calculateSymmetry)** """
    symResultB: float|ExtValue[float]
    """ **resulting symmetry plane, coeff. B (set by calculateSymmetry)** """
    symResultC: float|ExtValue[float]
    """ **resulting symmetry plane, coeff. C (set by calculateSymmetry)** """
    symResultD: float|ExtValue[float]
    """ **resulting symmetry plane, coeff. D (set by calculateSymmetry)** """
    geom_density: float|ExtValue[float]
    """
    **Density**
    
    The number of samples (per unit length in one dimension) that affects the precision of estimation of geometrical properties.
    """
    @staticmethod
    def forModel(arg1: Model) -> ModelGeometry:
        """ The returned ModelGeometry object can be used to calculate geometric properties (volume, area, sizes) of the associated model. The density is copied from the current global ModelGeometry.geom_density on object creation. """
        ...

    @staticmethod
    def volume() -> float|ExtValue[float]:

        ...

    @staticmethod
    def area() -> float|ExtValue[float]:

        ...

    @staticmethod
    def voxels() -> Vector:
        """ Returns a Vector of Pt3D objects from a regular 3D grid (sampled according to ModelGeometry.geom_density) that are inside the Model body (Parts and Joints). """
        ...

    @staticmethod
    def sizesAndAxes() -> Vector:
        """ The returned vector contains XYZ (sizes) and Orient (axes) objects. """
        ...

    minjoint: float|ExtValue[float]
    """ **Minimal joint length** """
    maxjoint: float|ExtValue[float]
    """ **Maximal joint length** """

class SimilMeasure(ExtValue):
    """
    Evaluates morphological dissimilarity. More information:\n
    https://www.framsticks.com/bib/Komosinski-et-al-2001\n
    https://www.framsticks.com/bib/Komosinski-and-Kubiak-2011\n
    https://www.framsticks.com/bib/Komosinski-2016\n
    https://doi.org/10.1007/978-3-030-16692-2_8
    """

    simil_type: int|ExtValue[int]
    """ **Type of similarity measure** """
    @staticmethod
    def evaluateDistance(arg1: Geno, arg2: Geno) -> float|ExtValue[float]:
        """
        **Evaluate model dissimilarity**
        
        Calculates dissimilarity between two models created from Geno objects.
        """
        ...


class SimilMeasureDistribution(ExtValue):
    """ Evaluates morphological dissimilarity using the distribution measure. """

    simil_density: float|ExtValue[float]
    """ **Density of surface sampling** """
    simil_bin_num: int|ExtValue[int]
    """ **Number of bins** """
    simil_samples_num: int|ExtValue[int]
    """ **Number of samples** """
    @staticmethod
    def evaluateDistance(arg1: Geno, arg2: Geno) -> float|ExtValue[float]:
        """
        **Evaluate model dissimilarity**
        
        Calculates dissimilarity between two models created from Geno objects.
        """
        ...


class SimilMeasureGreedy(ExtValue):
    """
    Evaluates morphological dissimilarity using the greedy measure. More information:\n
    https://www.framsticks.com/bib/Komosinski-et-al-2001\n
    https://www.framsticks.com/bib/Komosinski-and-Kubiak-2011\n
    https://www.framsticks.com/bib/Komosinski-2016\n
    https://www.framsticks.com/bib/Komosinski-and-Mensfelt-2019
    """

    simil_greedy_parts: float|ExtValue[float]
    """
    **Weight of parts count**
    
    Differing number of parts is also handled by the 'part degree' similarity component.
    """
    simil_greedy_partdeg: float|ExtValue[float]
    """ **Weight of parts' degree** """
    simil_greedy_neuro: float|ExtValue[float]
    """ **Weight of neurons count** """
    simil_greedy_partgeom: float|ExtValue[float]
    """ **Weight of parts' geometric distances** """
    simil_greedy_fixedZaxis: int|ExtValue[int]
    """ **Fix 'z' (vertical) axis?** """
    simil_greedy_weightedMDS: int|ExtValue[int]
    """
    **Should weighted MDS be used?**
    
    If activated, weighted MDS with vertex (i.e., Part) degrees as weights is used for 3D alignment of body structure.
    """
    @staticmethod
    def evaluateDistance(arg1: Geno, arg2: Geno) -> float|ExtValue[float]:
        """
        **Evaluate model dissimilarity**
        
        Calculates dissimilarity between two models created from Geno objects.
        """
        ...


class SimilMeasureHungarian(ExtValue):
    """
    Evaluates morphological dissimilarity using the measure. More information:\n
    https://www.framsticks.com/bib/Komosinski-et-al-2001\n
    https://www.framsticks.com/bib/Komosinski-and-Kubiak-2011\n
    https://www.framsticks.com/bib/Komosinski-2016\n
    https://www.framsticks.com/bib/Komosinski-and-Mensfelt-2019
    """

    simil_parts: float|ExtValue[float]
    """
    **Weight of parts count**
    
    Differing number of parts is also handled by the 'part degree' similarity component.
    """
    simil_partdeg: float|ExtValue[float]
    """ **Weight of parts' degree** """
    simil_neuro: float|ExtValue[float]
    """ **Weight of neurons count** """
    simil_partgeom: float|ExtValue[float]
    """ **Weight of parts' geometric distances** """
    simil_fixedZaxis: int|ExtValue[int]
    """ **Fix 'z' (vertical) axis?** """
    simil_weightedMDS: int|ExtValue[int]
    """
    **Should weighted MDS be used?**
    
    If activated, weighted MDS with vertex (i.e., Part) degrees as weights is used for 3D alignment of body structure.
    """
    @staticmethod
    def evaluateDistance(arg1: Geno, arg2: Geno) -> float|ExtValue[float]:
        """
        **Evaluate model dissimilarity**
        
        Calculates dissimilarity between two models created from Geno objects.
        """
        ...


class Simulator(ExtValue):
    """ The Framsticks simulator. """

    @staticmethod
    def print(text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Print information message**
        
        One argument: message to be printed.
        """
        ...

    @staticmethod
    def message(text: str|ExtValue[str], level: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Print message**
        
        The second argument can be:
         -1 = debugging message\n
         0 = information\n
         1 = warning\n
         2 = error\n
         3 = critical error
        """
        ...

    @staticmethod
    def sleep(milliseconds: int|ExtValue[int]) -> None|ExtValue[None]:
        """ Suspends the execution for a specified interval. """
        ...

    @staticmethod
    def beep() -> None|ExtValue[None]:
        """ Plays the default system sound. """
        ...

    @staticmethod
    def sound(freqency_in_Hz: int|ExtValue[int], length_in_milliseconds: int|ExtValue[int]) -> None|ExtValue[None]:
        """ Generates a simple tone on the speaker """
        ...

    @staticmethod
    def eval(script_statement: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Evaluate a statement**
        
        The argument must be a complete statement, e.g. "return 2+2;" is valid, while "2+2" is not. The Error object is returned for invalid statements.\n
        Example:\n
        var statement="function fun(a) {return a*a;} return fun(Math.pi);";\n
        var result=Simulator.eval(statement);\n
        if (typeof result=="Error")
           Simulator.print("Error:"+result.message);
        else
           Simulator.print("Result:"+result);
        """
        ...

    @staticmethod
    def load(filename: str|ExtValue[str]) -> None|ExtValue[None]:
        """ Load experiment file (calls onExpLoad() in the current experiment definition). This function is intended to replace the simulator state; the old state is cleared by automatically calling "resetToDefaults()". Use "import" if you don't want to lose the old simulator state. Contents can also be loaded from string by using specifically formed filename: "string://string_contents_to_be_loaded". """
        ...

    @overload
    @staticmethod
    def import_(filename: str|ExtValue[str], options: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        Import some data from file. Contents can also be imported from string by using specifically formed filename: "string://string_contents_to_be_imported".\n
        The second optional argument selects what section(s) will be imported:
        	1 - experiment (works just like load(), all other bits are ignored, and can reset the simulator state!)\n
        	2 - genotypes\n
        	4 - simulator parameters\n
        	8 - genepool settings\n
        	16 - population settings\n
        	32 - new groups will be created for imported genepools and populations\n
        	64 - allow switching to a different expdef while importing parameters (4)\n
        	256 - creatures
        
        The standard behavior (without the second argument) is to import genotypes, parameters, and genepool and population settings (2+4+8+16). Note that "64" is not included by default, because the expdef change resets all simulator parameters, which contradicts the usual meaning of "import" in Framsticks ("add data", as opposed to "load" meaning "replace data"). Moreover, using the "64" option in scripts can be dangerous, especially all expdef and show scripts should always declare the proper expdef name in their header rather than change the expdef directly. Without the "64" option, it is always safe to "import" any file in a script regardless of the current simulator state.
        """
        ...

    @overload
    @staticmethod
    def import_(filename: str|ExtValue[str]) -> None|ExtValue[None]:
        """ Equivalent to import(filename,2+4+8+16) - imports genotypes, parameters, genepool and population settings. """
        ...

    @staticmethod
    def save(filename: str|ExtValue[str]) -> Any|ExtValue[Any]:
        """ Save experiment file (calls onExpSave() in the current experiment definition). Providing null filename makes save() return saved data as a text string instead of writing it to the file. """
        ...

    @staticmethod
    def export(filename: str|ExtValue[str], options: int|ExtValue[int], genepool: int|ExtValue[int], population: int|ExtValue[int]) -> Any|ExtValue[Any]:
        """
        Save some data to file. Arguments:\n
        - filename: can be null, which makes export() return saved data as a text string instead of writing it to the file.\n
        - options: composed of the following bit values:
        	1 - experiment (works just like save() and all other option bits are ignored)\n
        	2 - genotypes\n
        	4 - simulator parameters\n
        	8 - simulator stats\n
        	16 - genepool settings\n
        	32 - population settings\n
        	64 - do autosave\n
        	256 - creatures
        - selected genepool, -1 means all genepools\n
        - selected population, -1 means all populations
        """
        ...

    @staticmethod
    def start() -> None|ExtValue[None]:
        """
        **Start simulation**
        
        Called by the user interface.
        """
        ...

    @staticmethod
    def stop() -> None|ExtValue[None]:
        """
        **Stop simulation**
        
        The expdef script calls this function to stop simulation.
        """
        ...

    running: int|ExtValue[int]
    """
    **Is the simulation running?**
    
    Useful for synchronizing the user interface state.
    """
    stop_on: int|ExtValue[int]
    """
    **Error level to stop running simulation**
    
    If the simulation is running and a message is emitted with at least the selected severity, the simulation will be stopped.
    """
    @staticmethod
    def step() -> None|ExtValue[None]:
        """ **Do a single simulation step** """
        ...

    time: int|ExtValue[int]
    """
    **Number of steps**
    
    Simulator.time will be removed because of its misleading name, please use Simulator.stepNumber instead.
    """
    last_genotype_num: int|ExtValue[int]
    """
    **Largest previously used Genotype.num**
    
    See: Genotype.num
    """
    last_creature_num: int|ExtValue[int]
    """
    **Largest previously used Creature.num**
    
    See: Creature.num
    """
    stepNumber: int|ExtValue[int]
    """ **Number of simulation steps** """
    simspeed: int|ExtValue[int]
    """
    **Simulation speed**
    
    steps/second
    """
    expdef: str|ExtValue[str]
    """
    **Experiment definition**
    
    Choose the experiment framework\n
    (in Windows GUI, confirm by pressing 'Apply')
    
    Stop the simulation before selecting another experiment definition.\n
    It is a good practice to initialize the experiment before running the simulation.
    """
    expdef_title: str|ExtValue[str]
    """ **Title** """
    expdef_info: str|ExtValue[str]
    """ **Description** """
    @staticmethod
    def init() -> None|ExtValue[None]:
        """
        **Initialize experiment**
        
        Prepares the experiment for running - usually performs initialization procedures such as resetting counters, states, gene pools, etc.\n
        These actions are defined in the onInit() function of this experiment definition.
        """
        ...

    @staticmethod
    def loadexpdef() -> None|ExtValue[None]:
        """
        **Reload experiment definition**
        
        Resets the simulator to its default state, resets all parameters to default values and then loads this experiment definition.
        """
        ...

    usercode: str|ExtValue[str]
    """
    **Script override**
    
    You can override any function from the original experiment definition script. Use the same function names and provide alternative implementations.\n
    Example:
    
    function onBorn(cr)\n
    {
      Simulator.print("A creature is born: "+cr.name);\n
      super_onBorn(cr); //calls the original implementation
    }
    """
    autosaveperiod: int|ExtValue[int]
    """
    **Save backup**
    
    Save simulation state once every n-th event\n
    (events are defined by the script. For 'standard.expdef' it is after each death).\n
    Save EXPT file first to initialize name for autosave files.\n
    Slave simulators (in multithreaded experiments) ignore this setting and never create autosave files.
    """
    overwrite: int|ExtValue[int]
    """
    **Overwrite files?**
    
    Lets you choose what to do when a file is created with the same name as an already existing file: overwite the existing file or create its backup?
    """
    filecomm: int|ExtValue[int]
    """
    **Show file comments**
    
    Controls displaying comments encountered in opened files.
    """
    @staticmethod
    def checkpoint() -> None|ExtValue[None]:
        """
        **Notify that the experiment state was significantly updated.**
        
        This function was previously called "autosave".
        """
        ...

    @staticmethod
    def checkpointData(any_data: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """
        **Notify that the experiment state was significantly updated + pass data.**
        
        In the distributed/paralellized scenario the data passed as argument can be received by the controlling entity (onSlaveCheckpoint in multithreaded master experiment, /simulator/expevent in distributed network simulator).
        """
        ...

    lastCheckpoint: Any|ExtValue[Any]
    """
    **Last checkpoint**
    
    Most recently reported by the experiment definition script.
    """
    @staticmethod
    def resetToDefaults() -> None|ExtValue[None]:
        """
        **Reset the simulator state**
        
        Clears groups and loads default values for simulator parameters, then calls onExpDefLoad() of the current experiment definition.
        """
        ...

    createrr: int|ExtValue[int]
    """ **Object creation errors** """
    groupchk: int|ExtValue[int]
    """
    **Warn on adding invalid genotypes**
    
    Warnings will be printed when invalid genotypes are added to a gene pool.
    """
    creatwarnfail: int|ExtValue[int]
    """
    **Don't simulate genotypes with warnings**
    
    Creatures grown with warnings will not be simulated. This helps prevent the propagation of faulty genes, because genotypes that cause warnings when interpreted will not reproduce.
    """
    vmdebug: int|ExtValue[int]
    """ **VM debug** """
    vm_step_limit: int|ExtValue[int]
    """
    **VM step limit**
    
    Abort any script (expdef, fitness formula, user script) when it performs too many operations - which can take more or less time depending on your machine performance. This can protect against infinite loops or unbearably long runs of untested scripts that would otherwise force you to kill the whole application. Use Simulator.vm_..._warning if you only need information about what script takes too much time without aborting it.
    """
    vm_step_warning: int|ExtValue[int]
    """
    **VM step warning**
    
    Display a warning when any script (expdef, fitness formula, user script) performs too many operations - which can take more or less time depending on your machine performance. Use Simulator.vm_..._limit to prevent the application from becoming unresponsive by aborting misbehaving scripts.
    """
    vm_time_limit: float|ExtValue[float]
    """
    **VM time limit**
    
    Abort any script (expdef, fitness formula, user script) when it takes too much time - measured in seconds. The actual amount of work depends on your machine performance. This can protect against infinite loops or unbearably long runs of untested scripts that would otherwise force you to kill the whole application. Use Simulator.vm_..._warning if you only need information about what script takes too much time without aborting it.
    """
    vm_time_warning: float|ExtValue[float]
    """
    **VM time warning**
    
    Display a warning when any script (expdef, fitness formula, user script) takes too much time - measured in seconds. The actual amount of work depends on your machine performance. Use Simulator.vm_..._limit to prevent the application from becoming unresponsive by aborting misbehaving scripts.
    """
    @staticmethod
    def new() -> Simulator:
        """ **create new Simulator** """
        ...

    slaves: SlaveSimulators
    """ **Slave simulator objects** """
    cpus: int|ExtValue[int]
    """ **Number of detected CPUs ('cores') on this machine** """
    world: World
    populations: Populations
    genepools: GenePools
    """ **Gene pools object** """
    expproperties: ExpProperties
    expstate: ExpState
    genman: GenMan
    genoconverters: GenoConverters
    """ **Genotype converters object** """
    @staticmethod
    def reloadNeurons() -> None|ExtValue[None]:
        """ **Reload neuron definitions** """
        ...

    userdata: Any|ExtValue[Any]
    """ **User field** """
    identity: int|ExtValue[int]
    """ -1 for master simulator, 0...count-1 for slaves """
    @staticmethod
    def refreshGUI() -> None|ExtValue[None]:
        """
        **Refresh GUI**
        
        Notify that all populations and gene pools content changed.
        """
        ...

    version_string: str|ExtValue[str]
    """
    **Version string**
    
    Current application version as a string (human-friendly).
    """
    version_int: int|ExtValue[int]
    """
    **Version integer**
    
    Current application version as an integer.
    """

class SlaveSimulators(ExtValue):
    """
    This is a vector of slave Simulator objects. More details in:\n
    https://www.framsticks.com/bib/Komosinski-and-Ulatowski-2013r\n
    https://www.framsticks.com/bib/Komosinski-and-Ulatowski-2016
    """

    size: int|ExtValue[int]
    """
    **number of slaves**
    
    Changing this value will create/remove slave simulator objects as needed.
    """
    @staticmethod
    def get(index: int|ExtValue[int]) -> Simulator:
        """
        Access the slave simulator object (Simulator.slaves[index] works, too).\n
        Important: Do not operate on a simulator that is currently running, always stop() it first.
        """
        ...

    running: int|ExtValue[int]
    """
    **number of slaves running**
    
    Note that if running>0 then the number of running simulations can be outdated in the very moment you read this field, because the expdef can stop itself anytime. If running==0, then it is guaranteed to stay 0 until someone calls start() on some of the slave simulator objects.
    """
    @staticmethod
    def create() -> Simulator:
        """
        **create a slave**
        
        If you need to create AND store the reference to a newly created simulator object, then this function may be more readable than var s=Simulator.slaves[Simulator.slaves.size++];
        """
        ...

    @staticmethod
    def remove(slave_index_or_slave_Simulator_object_reference: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """
        **remove single slave**
        
        Also calls stop() if the simulator is running. Events assocated with the simulator being deleted are cancelled, so the expdef will not see the usual onSlaveStop.
        """
        ...

    @staticmethod
    def removeAll():
        """
        **remove all slaves**
        
        Same as Simulator.slaves=0;
        """
        ...

    @staticmethod
    def startAll():
        """ **start all slaves** """
        ...

    @staticmethod
    def stopAll():
        """ **stop all slaves** """
        ...

    @staticmethod
    def cancelEventsFromSlave(arg1: Simulator) -> None|ExtValue[None]:
        """ If the onSlaveStop() event is used to schedule work to a simulator, then you might want to cancel pending events when the experiment is aborted - otherwise it may be difficult to distinguish between self-stop events (called internally from the slave simulator to signal the job was completed) from abort-stop events (requested by the supervising simulator). Calling Simulator.slaves.stopAll(); Simulator.slaves.cancelAllEvents(); makes sure that no old events will be detected after that time point. Without cancelling, the old onSlaveStop() notification (the consequence of the abort-stop) might arrive after the next start() which may confuse the expdef code (slave events are asynchronous). """
        ...

    @staticmethod
    def cancelAllEvents():
        """ see cancelEventsFromSlave() """
        ...

    isolation: int|ExtValue[int]
    """
    **slave isolation**
    
    Slave simulator access is filtered to exclude object references across simulator boundaries and ensure a safe multithreaded operation.\n
    1. Slave simulations objects can't be accessed from master while the slave simulator is running (except for Simulator.stop/start/running).\n
    2. Master simulator objects can't be passed to slave simulators\n
    3. Data objects (Vectors and Dictionaries) are passed by value rather than by reference (to make sure that no simulator contains a reference to another simulator's data).\n
    Setting isolation=0 disables these restrictions, which can lead to unpredictable results or crashes, but is sometimes useful for inspecting true object relationships.
      Sample cases:
    Simulator.slaves[0].stop(); - always permitted\n
    Simulator.slaves[0].expdef="prime"; - permitted if the slave simulator is not running\n
    var vec=[1,2,3]; Simulator.slaves[0].user=vec; vec.clear(); - vec has changed, user field is still [1,2,3]\n
    var vec=[1,2,GenePools[0]]; Simulator.slaves[0].user=vec; - user field becomes [1,2,null] (because master's GenePool object can't be passed to the slave)\n
    var g=Simulator.slaves[0].genepools[0][0].genotype; - but the slave's GenePool can be accessed from master (if the slave is not running at the moment)
    """

class stats(ExtValue):


    gen_count: int|ExtValue[int]
    """ **Number of genetic operations so far** """
    gen_mvalid: int|ExtValue[int]
    """ **Mutations valid** """
    gen_mvalidated: int|ExtValue[int]
    """ **Mutations validated** """
    gen_minvalid: int|ExtValue[int]
    """
    **Mutations invalid**
    
    couldn't be repaired
    """
    gen_mfailed: int|ExtValue[int]
    """
    **Mutations failed**
    
    couldn't be performed
    """
    gen_xovalid: int|ExtValue[int]
    """ **Crossovers valid** """
    gen_xovalidated: int|ExtValue[int]
    """ **Crossovers validated** """
    gen_xoinvalid: int|ExtValue[int]
    """
    **Crossovers invalid**
    
    couldn't be repaired
    """
    gen_xofailed: int|ExtValue[int]
    """
    **Crossovers failed**
    
    couldn't be performed
    """
    gen_mutimpr: float|ExtValue[float]
    """
    **Mutations total effect**
    
    total cumulative mutation change
    """
    gen_xoimpr: float|ExtValue[float]
    """
    **Crossovers total effect**
    
    total cumulative crossover change
    """
    @staticmethod
    def clrstats() -> None|ExtValue[None]:
        """ **Clear stats and history** """
        ...

    @staticmethod
    def _propertyClear() -> None|ExtValue[None]:
        """
        **Remove all properties**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAdd(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property (id,type,name,help)**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemove(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyChange(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Change property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAddGroup(name: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemoveGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyExists(name: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Check for property existence** """
        ...

    _property_changed_index: int|ExtValue[int]
    """ **Last changed property index** """
    _property_changed_id: str|ExtValue[str]
    """ **Last changed property id** """
    st_count: int|ExtValue[int]
    """ **Count** """
    st_min_numparts: float|ExtValue[float]
    """ **Minimal Number of body Parts** """
    st_avg_numparts: float|ExtValue[float]
    """ **Average Number of body Parts** """
    st_max_numparts: float|ExtValue[float]
    """ **Maximal Number of body Parts** """
    st_min_numjoints: float|ExtValue[float]
    """ **Minimal Number of body Joints** """
    st_avg_numjoints: float|ExtValue[float]
    """ **Average Number of body Joints** """
    st_max_numjoints: float|ExtValue[float]
    """ **Maximal Number of body Joints** """
    st_min_numneurons: float|ExtValue[float]
    """ **Minimal Number of neurons** """
    st_avg_numneurons: float|ExtValue[float]
    """ **Average Number of neurons** """
    st_max_numneurons: float|ExtValue[float]
    """ **Maximal Number of neurons** """
    st_min_numconnections: float|ExtValue[float]
    """ **Minimal Number of neural connections** """
    st_avg_numconnections: float|ExtValue[float]
    """ **Average Number of neural connections** """
    st_max_numconnections: float|ExtValue[float]
    """ **Maximal Number of neural connections** """
    st_min_num: float|ExtValue[float]
    """ **Minimal Ordinal number** """
    st_avg_num: float|ExtValue[float]
    """ **Average Ordinal number** """
    st_max_num: float|ExtValue[float]
    """ **Maximal Ordinal number** """
    st_min_gnum: float|ExtValue[float]
    """ **Minimal Generation** """
    st_avg_gnum: float|ExtValue[float]
    """ **Average Generation** """
    st_max_gnum: float|ExtValue[float]
    """ **Maximal Generation** """
    st_min_instances: float|ExtValue[float]
    """ **Minimal Instances** """
    st_avg_instances: float|ExtValue[float]
    """ **Average Instances** """
    st_max_instances: float|ExtValue[float]
    """ **Maximal Instances** """
    st_min_lifespan: float|ExtValue[float]
    """ **Minimal Life span** """
    st_avg_lifespan: float|ExtValue[float]
    """ **Average Life span** """
    st_max_lifespan: float|ExtValue[float]
    """ **Maximal Life span** """
    st_min_velocity: float|ExtValue[float]
    """ **Minimal Velocity** """
    st_avg_velocity: float|ExtValue[float]
    """ **Average Velocity** """
    st_max_velocity: float|ExtValue[float]
    """ **Maximal Velocity** """
    st_min_distance: float|ExtValue[float]
    """ **Minimal Distance** """
    st_avg_distance: float|ExtValue[float]
    """ **Average Distance** """
    st_max_distance: float|ExtValue[float]
    """ **Maximal Distance** """
    st_min_vertvel: float|ExtValue[float]
    """ **Minimal Vertical velocity** """
    st_avg_vertvel: float|ExtValue[float]
    """ **Average Vertical velocity** """
    st_max_vertvel: float|ExtValue[float]
    """ **Maximal Vertical velocity** """
    st_min_vertpos: float|ExtValue[float]
    """ **Minimal Vertical position** """
    st_avg_vertpos: float|ExtValue[float]
    """ **Average Vertical position** """
    st_max_vertpos: float|ExtValue[float]
    """ **Maximal Vertical position** """
    st_min_fit: float|ExtValue[float]
    """ **Minimal Fitness** """
    st_avg_fit: float|ExtValue[float]
    """ **Average Fitness** """
    st_max_fit: float|ExtValue[float]
    """ **Maximal Fitness** """
    st_min_fit2: float|ExtValue[float]
    """ **Minimal Final fitness** """
    st_avg_fit2: float|ExtValue[float]
    """ **Average Final fitness** """
    st_max_fit2: float|ExtValue[float]
    """ **Maximal Final fitness** """
    st_min_c_velocity: float|ExtValue[float]
    """ **Minimal Recent period velocity** """
    st_avg_c_velocity: float|ExtValue[float]
    """ **Average Recent period velocity** """
    st_max_c_velocity: float|ExtValue[float]
    """ **Maximal Recent period velocity** """
    st_min_c_vertvelocity: float|ExtValue[float]
    """ **Minimal Recent period vertical velocity** """
    st_avg_c_vertvelocity: float|ExtValue[float]
    """ **Average Recent period vertical velocity** """
    st_max_c_vertvelocity: float|ExtValue[float]
    """ **Maximal Recent period vertical velocity** """
    st_min_c_vertpos: float|ExtValue[float]
    """ **Minimal Recent period vertical position** """
    st_avg_c_vertpos: float|ExtValue[float]
    """ **Average Recent period vertical position** """
    st_max_c_vertpos: float|ExtValue[float]
    """ **Maximal Recent period vertical position** """
    st_min_pos_x: float|ExtValue[float]
    """ **Minimal Position x** """
    st_avg_pos_x: float|ExtValue[float]
    """ **Average Position x** """
    st_max_pos_x: float|ExtValue[float]
    """ **Maximal Position x** """
    st_min_pos_y: float|ExtValue[float]
    """ **Minimal Position y** """
    st_avg_pos_y: float|ExtValue[float]
    """ **Average Position y** """
    st_max_pos_y: float|ExtValue[float]
    """ **Maximal Position y** """
    st_min_pos_z: float|ExtValue[float]
    """ **Minimal Position z** """
    st_avg_pos_z: float|ExtValue[float]
    """ **Average Position z** """
    st_max_pos_z: float|ExtValue[float]
    """ **Maximal Position z** """
    st_min_size_x: float|ExtValue[float]
    """ **Minimal Bounding box x size** """
    st_avg_size_x: float|ExtValue[float]
    """ **Average Bounding box x size** """
    st_max_size_x: float|ExtValue[float]
    """ **Maximal Bounding box x size** """
    st_min_size_y: float|ExtValue[float]
    """ **Minimal Bounding box y size** """
    st_avg_size_y: float|ExtValue[float]
    """ **Average Bounding box y size** """
    st_max_size_y: float|ExtValue[float]
    """ **Maximal Bounding box y size** """
    st_min_size_z: float|ExtValue[float]
    """ **Minimal Bounding box z size** """
    st_avg_size_z: float|ExtValue[float]
    """ **Average Bounding box z size** """
    st_max_size_z: float|ExtValue[float]
    """ **Maximal Bounding box z size** """
    st_min_center_x: float|ExtValue[float]
    """ **Minimal center.x** """
    st_avg_center_x: float|ExtValue[float]
    """ **Average center.x** """
    st_max_center_x: float|ExtValue[float]
    """ **Maximal center.x** """
    st_min_center_y: float|ExtValue[float]
    """ **Minimal center.y** """
    st_avg_center_y: float|ExtValue[float]
    """ **Average center.y** """
    st_max_center_y: float|ExtValue[float]
    """ **Maximal center.y** """
    st_min_center_z: float|ExtValue[float]
    """ **Minimal center.z** """
    st_avg_center_z: float|ExtValue[float]
    """ **Average center.z** """
    st_max_center_z: float|ExtValue[float]
    """ **Maximal center.z** """

class StopEvent(ExtValue):
    """ Used in onSlaveStop() which is called when a Slave Simulator is stopped. """

    index: int|ExtValue[int]
    """ **slave index** """
    slave: Simulator

class String(ExtValue):
    """ String functions library. """

    @staticmethod
    def len(arg1: str|ExtValue[str]) -> int|ExtValue[int]:
        """
        **String length**
        
        String.len("abcdef") == 6
        """
        ...

    @staticmethod
    def replace(input_string: str|ExtValue[str], search: str|ExtValue[str], substitute: str|ExtValue[str]) -> str|ExtValue[str]:
        """ String.replace("abcdef","cd","X") == "abXef" """
        ...

    @staticmethod
    def split(text_to_split: str|ExtValue[str], word_separator: str|ExtValue[str]) -> Vector:
        """
        return the vector of substrings, cut at separator positions.\n
        subsequent separators give empty words:\n
        split("word1---word2-word3","-") returns ["word1","","","word2","word3"]
        """
        ...

    @staticmethod
    def split2(text_to_split: str|ExtValue[str], word_separator: str|ExtValue[str]) -> Vector:
        """
        **Split, merging separators first**
        
        return the vector of substrings, cut at separator positions.\n
        subsequent separators are treated as one:\n
        split2("word1---word2-word3","-") returns ["word1","word2","word3"]
        """
        ...

    @staticmethod
    def indexOf(arg1: str|ExtValue[str], substring: str|ExtValue[str]) -> int|ExtValue[int]:
        """
        **Search for substring**
        
        String.indexOf("abcdef","cd") == 2\n
        String.indexOf("abcdef","dc") == -1
        """
        ...

    @staticmethod
    def indexOfStart(arg1: str|ExtValue[str], substring: str|ExtValue[str], start_index: int|ExtValue[int]) -> int|ExtValue[int]:
        """
        **Search for substring**
        
        String.indexOfStart("abcdef","cd",1) == 2\n
        String.indexOfStart("abcdef","cd",3) == -1
        """
        ...

    @overload
    @staticmethod
    def substr(arg1: str|ExtValue[str], first_character: int|ExtValue[int], number_of_characters: int|ExtValue[int]) -> str|ExtValue[str]:
        """
        **Substring**
        
        String.substr("abcdef",3,2) == "de"
        """
        ...

    @overload
    @staticmethod
    def substr(arg1: str|ExtValue[str], first_character: int|ExtValue[int]) -> str|ExtValue[str]:
        """
        **substring**
        
        String.substr("abcdef",3) == "def"
        """
        ...

    @staticmethod
    def left(arg1: str|ExtValue[str], number_of_characters: int|ExtValue[int]) -> str|ExtValue[str]:
        """
        **Left substring**
        
        String.left("abcdef",3) == "abc"
        """
        ...

    @staticmethod
    def right(arg1: str|ExtValue[str], number_of_characters: int|ExtValue[int]) -> str|ExtValue[str]:
        """
        **Right substring**
        
        String.right("abcdef",3) == "def"
        """
        ...

    @staticmethod
    def trim(arg1: str|ExtValue[str]) -> str|ExtValue[str]:
        """ **Removes whitespace from both sides of a string.** """
        ...

    @staticmethod
    def startsWith(string: str|ExtValue[str], substring: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Test if starts with substring** """
        ...

    @staticmethod
    def endsWith(string: str|ExtValue[str], substring: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Test if ends with substring** """
        ...

    @staticmethod
    def format(format_string: str|ExtValue[str], value_or_vector: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """
        **Formatted string conversion**
        
        Works like the standard C library "sprintf()". The '%' operator can be used as a shortcut, e.g. String.format("%x",123) is equivalent of "%x" % 123\n
        Character seqences beginning with % found in the format string are replaced by formatted values produced according to their corresponding format specifiers: %[-][+][0][width[.precision]]type
         -: left adjust (default is right adjust)\n
         +: place a sign (+ or -) before a number\n
         0: the value should be zero padded\n
         width: minimum field width\n
         precision: minimum number of decimal digits\n
         type: d=decimal integer, x/X=hexadecimal integer, f/g=floating point number, e="scientific" style floating point, c=character of a given ascii code, t=time, %=special case, outputs the literal % character
        Multiple values can be formatted in one call, by passing a vector as the second argument:\n
        String.format("a=%03d b=%.2f c=%s",[a,b,c]) or "a=%03d b=%.2f c=%s" % [a,b,c]\n
        Alternatively, if no % characters are required in the output string, the chained call can be used:\n
        "a=%03d b=%.2f c=%s" % a % b % c\n
        The above expression works as expected, because, unlike the regular sprintf, the formatting function preserves % characters left after using all input arguments:
         input:          "a=%03d b=%.2f c=%s" % a % b % c\n
         actual meaning: (("a=%03d b=%.2f c=%s" % a) % b) % c\n
         phase 1:        ("a=000 b=%.2f c=%s" % b) % c\n
         phase 2:        "a=000 b=0.00 c=%s" % c\n
         result:         "a=000 b=0.00 c=0"
        
        Examples:
         String.format("|%07.2f|",Math.pi) == "|0003.14|"\n
         String.format("|%04x|",255) == "|00ff|"\n
         String.format("|%7s|","text") == "|   text|"\n
         String.format("|%-7d|",12345) == "|12345  |"\n
         String.format("%t",Math.time) == "Sun Apr 29 19:22:02 2007"\n
         String.format("%T",Math.time) == "2007-05-29 19:22:02"\n
         String.format("x=%d%%",100) == "100%"
        """
        ...

    @staticmethod
    def parseInt(arg1: str|ExtValue[str]) -> int|ExtValue[int]:
        """
        **Parse integer**
        
        If the supplied string is not an integer, returns 0 and posts an error message.
        """
        ...

    @staticmethod
    def parseFloat(arg1: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **Parse floating point**
        
        If the supplied string is not a number, returns 0.0 and posts an error message.
        """
        ...

    @staticmethod
    def parseNumber(arg1: str|ExtValue[str]) -> Any|ExtValue[Any]:
        """
        **Parse integer or floating point**
        
        Returns an integer, a floating point, or null if the string cannot be parsed as a number.\n
        The 'typeof' operator can be used to distinguish between an integer and a floating point value:\n
        typeof(String.parseNumber("qwerty")) == "null"\n
        typeof(String.parseNumber("1234")) == "int"\n
        typeof(String.parseNumber("3.14")) == "float"
        """
        ...

    @staticmethod
    def code(arg1: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **ASCII code of the character** """
        ...

    @staticmethod
    def char(arg1: int|ExtValue[int]) -> str|ExtValue[str]:
        """ **Character from ASCII** """
        ...

    @staticmethod
    def toUpper(arg1: str|ExtValue[str]) -> str|ExtValue[str]:
        """ **Make uppercase version** """
        ...

    @staticmethod
    def toLower(arg1: str|ExtValue[str]) -> str|ExtValue[str]:
        """ **Make lowercase version** """
        ...

    @staticmethod
    def serialize(arg1: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """ Converts to textual representation, preserving object hierarchy. """
        ...

    @staticmethod
    def deserialize(arg1: str|ExtValue[str]) -> Any|ExtValue[Any]:
        """
        Extracts objects from textual representation. Error object is returned if deserialization fails.\n
        Example:\n
        var ret=String.deserialize(something);\n
        if (typeof(ret)=="Error") Simulator.print("something is wrong: "+ret.message);
        """
        ...

    @staticmethod
    def toJSON(arg1: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """
        **JSON serialization**
        
        Exports to JSON format, preserving object hierarchy (excluding recursion).
        """
        ...

    @staticmethod
    def hash(arg1: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Compute 32-bit hash** """
        ...

    @staticmethod
    def diff(arg1: str|ExtValue[str], arg2: str|ExtValue[str]) -> Vector:
        """
        **Calculate string difference**
        
        Returns the vector of minimal differences between two strings. The vector contains either 2-element subvectors with differing substrings ["text-1","text-2"] or strings "same".
        
        For example, String.diff("thisisatest", "testing123testing") returns [t,[hi,e],s,[,t],i,[sa,ng123],test,[,ing]].
        
        Use this function for short strings, as it requires 4*length(string1)*length(string2) bytes of memory.
        """
        ...

    @staticmethod
    def urlEncode(arg1: str|ExtValue[str]) -> str|ExtValue[str]:
        """ **URL encode** """
        ...

    @staticmethod
    def urlDecode(arg1: str|ExtValue[str]) -> str|ExtValue[str]:
        """ **URL decode** """
        ...

    @staticmethod
    def quoteEof(arg1: str|ExtValue[str]) -> str|ExtValue[str]:
        """
        **quote eof**
        
        Add leading backslash to lines containing just 'eof' (or previously quoted 'eof') (for use in the network protocol implementation)
        """
        ...

    @staticmethod
    def unquoteEof(arg1: str|ExtValue[str]) -> str|ExtValue[str]:
        """
        **unquote eof**
        
        Remove one level of backslash quoting from lines containing quoted 'eof' (for use in the network protocol implementation)
        """
        ...

    SERIALIZATION_PREFIX: str|ExtValue[str]
    """
    **Serialization prefix**
    
    String prefix used in the Framsticks file format to indicate object fields that contain serialized objects.
    """
    ESC: str|ExtValue[str]
    """ **Escape character** """
    NBSP: str|ExtValue[str]
    """ **Non-breaking space character** """

class UserScripts(ExtValue):


    @staticmethod
    def _propertyClear() -> None|ExtValue[None]:
        """
        **Remove all properties**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAdd(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property (id,type,name,help)**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemove(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyChange(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Change property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAddGroup(name: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemoveGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyExists(name: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Check for property existence** """
        ...

    _property_changed_index: int|ExtValue[int]
    """ **Last changed property index** """
    _property_changed_id: str|ExtValue[str]
    """ **Last changed property id** """

class Vector(ExtValue):
    """
    Vector is a 1-dimensional array indexed by an integer value (starting from 0). Multidimensional arrays can be simulated by putting other Vector objects into a Vector.\n
    Examples:
    	var v1=Vector.new();\n
    	v1.add(123);\n
    	v1.add("string");
    A short way of doing the same (square brackets create a vector):
    	var v2=[123,"string"];
    Simulate a 2D array:
    	var v3=[[1,2,3],[4,5],[6]];
    You can iterate directly over values of a Vector using for(...in...) loops:
    	for(var element in v3) Simulator.print(element);
    """

    @staticmethod
    def clear() -> None|ExtValue[None]:
        """ **Clear data** """
        ...

    size: int|ExtValue[int]
    """ **Element count** """
    @staticmethod
    def remove(position: int|ExtValue[int]) -> None|ExtValue[None]:
        """ **Remove at position** """
        ...

    @staticmethod
    def get(position: int|ExtValue[int]) -> Any|ExtValue[Any]:
        """
        **Get value at position**
        
        object[position] can be always used instead of object.get(position)
        """
        ...

    @staticmethod
    def set(position: int|ExtValue[int], value: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """
        **Set value at position**
        
        object[position]=value can be always used instead of object.set(position,value)
        """
        ...

    @staticmethod
    def insert(position: int|ExtValue[int], value: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ **Insert value at position** """
        ...

    @staticmethod
    def add(value: Any|ExtValue[Any]) -> None|ExtValue[None]:
        """ **Append at the end** """
        ...

    @staticmethod
    def find(value: Any|ExtValue[Any]) -> int|ExtValue[int]:
        """ returns the element index or -1 if not found """
        ...

    avg: Any|ExtValue[Any]
    """ **Average** """
    stdev: Any|ExtValue[Any]
    """
    **Standard deviation**
    
    =sqrt(sum((element[i]-avg)^2)/(size-1)) which is estimated population std.dev. from sample std.dev.
    """
    toString: str|ExtValue[str]
    """ **Textual form** """
    @staticmethod
    def new() -> Vector:
        """ **Create new Vector** """
        ...

    @staticmethod
    def sort(comparator: FunctionReference) -> None|ExtValue[None]:
        """
        **Sort elements (in place)**
        
        comparator can be null, giving the "natural" sorting order (depending on element type), otherwise it must be a function reference obtained from the 'function' operator.
        
        Example:\n
        function compareLastDigit(a,b) {return (a%10)<(b%10);}\n
        var v=[16,23,35,42,54,61];\n
        v.sort(function compareLastDigit);
        """
        ...

    iterator: Object
    @staticmethod
    def clone() -> Vector:
        """
        **Create a clone**
        
        The resulting clone is a shallow copy (contains the same object references as the original). A deep copy can be obtained through serialization: String.deserialize(String.serialize(object));
        """
        ...


class WireframeAppearance(ExtValue):
    """ This object defines appearance of the elements of creatures (applies to the 'wireframe' display mode). Default shape definitions make food's "p:" look like a sphere, and manipulator's "p:" look like a robot hand. The model's Vstyle property is the name of the shape. Developers of experiment definitions can introduce new Vstyle(s) for their expdef and provide appropriate shape definitions by calling WireframeAppearance.set(...) in the onExpDefLoad() function. """

    @staticmethod
    def set(id: str|ExtValue[str], definition: str|ExtValue[str], color: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Id**
        
        Arguments:
        
        - "id" - can be
          "1p_STYLENAME": affects a single-Part creature (without Joints)\n
          "p_STYLENAME": affects all normal Parts\n
          "j_STYLENAME": affects Joints
             (STYLENAME corresponds to the Model.Vstyle value, and it can be empty).
        
        - "definition" is a genotype describing the object shape
        
        - "color" can be 0xRRGGBB or one of the special values: -3 = default creature color, -4 = default food color, -5 = default manipulator color
        
        Examples:\n
        WireframeAppearance.set("j_predator","X",0xff0000);//make all predators (i.e. creatures with Vstyle=predator) red\n
        WireframeAppearance.set("1p_food","...some...genotype...",-4);//change food appearance\n
        WireframeAppearance.set("p_","//0\\\\np:0,0,0\\\\np:-0.1,0,0\\\\np:0.1,0,0\\\\np:0,-0.1,0\\\\np:0,0.1,0\\\\np:0,0,-0.1\\\\np:0,0,0.1\\\\nj:0,1\\\\nj:0,2\\\\nj:0,3\\\\nj:0,4\\\\nj:0,5\\\\nj:0,6\\\\n",0);//make Parts' orientation axes visible
        """
        ...

    @staticmethod
    def clear() -> None|ExtValue[None]:

        ...


class World(ExtValue):
    """ Environment properties. """

    wrldtyp: int|ExtValue[int]
    """ **Type** """
    wrldsiz: float|ExtValue[float]
    """
    **Size**
    
    Side length of the world
    """
    wrldmap: str|ExtValue[str]
    """
    **Map**
    
    Description of the world (only applies to world types: "Blocks" or "Heightfield").\n
    To generate a random landscape, use:
       r[scaling] <sizex> <sizey> [seed]
    To generate a custom landscape, provide height values:
       m[scaling] <sizex> <sizey> digits...
     or
       M[scaling] <sizex> <sizey> numbers...
    
    "digits..." is a sequence of integer values 0,1,2,..,9. You may also use '-' and '|' characters for smooth slides between blocks.\n
    "numbers..." is a sequence of floating point values, so the "M" option provides more freedom.\n
    [scaling] is an optional linear scaling expression in the form of *FACTOR+OFFSET or *FACTOR-OFFSET, for example "r*0.1-2 5 5" creates a 5x5 random map with a 10% amplitude, shifted down by 2.
    
    See also the WorldMap object.
    """
    wrldwat: float|ExtValue[float]
    """ **Water level** """
    wrldbnd: int|ExtValue[int]
    """
    **Boundaries**
    
    Teleporting a creature that is outside of the world area is attempted every 'performance sampling period' steps. Teleport succeeds only when the target location in the world is empty (there is no collision).
    """
    wrldg: float|ExtValue[float]
    """
    **Gravity**
    
    You can adjust gravity for your experiments.\n
    The "official" setting used to evaluate and compare creatures is 1.
    """
    @staticmethod
    def wrldchg() -> None|ExtValue[None]:
        """ **Trigger world update** """
        ...

    simtype: int|ExtValue[int]
    """
    **Simulation engine**
    
    MechaStick is a fast and simple primary Framsticks simulation engine.\n
    ODE is Open Dynamics Engine by Russel Smith et al.
    
    NOTE: switching between simulation engines causes removal of all objects in the world (e.g. creatures).
    """
    nnspeed: float|ExtValue[float]
    """
    **NN speed**
    
    Number of neural network simulation steps in each physics simulation step
    """
    rndcollisions: int|ExtValue[int]
    """
    **Random collision order**
    
    When enabled, custom collision handlers are invoked in random order. This can help remove unfair bias in some experiments - for example where the same collision order in each simulation step would cause some creatures colliding with food to consume energy while other colliding creatures would starve.
    """
    signals: WorldSignals
    """ **Signal sources** """

class WorldMap(ExtValue):
    """ Environment details for "Blocks" and "Heightfield" world type. The most important concept is a "Map", which is the array of Map elements. """

    xsize: int|ExtValue[int]
    """ **Map x size** """
    ysize: int|ExtValue[int]
    """ **Map y size** """
    @staticmethod
    def getAsString(alternate_script: str|ExtValue[str], special_arguments: Any|ExtValue[Any]) -> str|ExtValue[str]:
        """
        **String representation of the world surface**
        
        This function returns the universal polygonal description of the world surface (regardless of the world type). The data is provided in the following simple textual format with each line describing one vertex (3 floating point values) or one face (3 or 4 vertex indices - faces can be triangles or quads), which is a subset of the Wavefront .obj file format:
        
        v first vertex coordinates\n
        v second vertex coordinates\n
        v ...etc\n
        f first face indices\n
        f second face indices\n
        f ...etc
        
        For example, the default flat world consists of 4 vertices and 1 quad face:
        
        v 0 0 0\n
        v 20.0 0 0\n
        v 20.0 20.0 0\n
        v 0 20.0 0\n
        f 1 2 3 4
        
        Internaly, the data returned by this function is generated by the 'scripts/worldmap-faces.script' file, so you can refer to its source if needed.\n
        The first argument to getAsString() (if not null or empty string) selects an alternate userscript to be used instead of the default 'worldmap-faces.script', allowing for extension and customization.\n
        Examples:\n
        WorldMap.getAsString(null,null) //use the default script\n
        WorldMap.getAsString("myscript","myarg") //calls "WorldMap_myscript", passing "myarg" to its main_args() function.
        """
        ...

    @staticmethod
    def getHeight(x: float|ExtValue[float], y: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **Height**
        
        Height at any 2d coordinate
        """
        ...

    @staticmethod
    def getMap(x: int|ExtValue[int], y: int|ExtValue[int]) -> Object:
        """
        **get map element object**
        
        Retrieve the map element object for a given grid coordinates (x,y), where 0<=x<xsize, 0<=y<ysize.
        
        The obtained value type depends on the current world type.\n
        - Blocks world objects provide 'z' and 'type' values (z is the block height, type is 0=flat block, 1=west-east slope, 2=north-south slope).\n
        - Heightfield world objects provide just the 'z' value (which is the grid point height).
        
        See the 'scripts/worldmap_faces.script' file for a practical example on how to obtain the world geometry data using WorldMap.getMap().
        
        Quirks: Internally, maps have more elements than could be deduced from the user-supplied World.wrldmap, as additional rows of elements are added to provide smooth transitions to flat surroundings, which is reflected in 'xsize' and 'ysize'.\n
        WorldMap.getMap() arguments refer to this internal representation, so the object corresponding to the first map element is not (0,0), but (1,1) for Heightfield or (2,2) for Blocks world. Not starting from (0,0) can be convenient - for example, given any valid grid coordinates (x,y), all its neighbors are also valid and can be requested through getMap() without introducing any special cases in the code.
        """
        ...

    @overload
    @staticmethod
    def intersect(arg_3d_point: Vector, arg_3d_direction: Vector, range: float|ExtValue[float]) -> Vector:
        """
        Calculate the intersection point between the world surface and the ray projected from "3d point" towards the given direction. 3D points are actually 3-elements Vector objects. The resulting vector contains the additional fourth element - the intersection point distance. The function returns null if there is no intersection.
        
        See "standard_events.inc" file, which uses "intersect" for calculating the world coordinates corresponding to the user-clicked screen location.\n
        Bugs: This function does not currently handle the heightfield environment correctly (works as if it was flat)
        """
        ...

    @overload
    @staticmethod
    def intersect(arg_3d_point: Vector, arg_3d_direction: Vector) -> Vector:
        """ Works like intersect(3d point,3d direction,range) for inifinite range, that is without limiting the intersection distance """
        ...


class WorldSignals(ExtValue):
    """
    Use this object to create stationary signals (not associated with any moving object) and to receive signals from any location in the world. There are Creature-based and Neuro-based variants of this object that automatically operate from creature's or neuron's position.
    
    See also: Signal, CreatureSignals, NeuroSignals.
    """

    @staticmethod
    def add(position: XYZ, channel: str|ExtValue[str]) -> Signal:
        """ **Create a new signal** """
        ...

    @staticmethod
    def receive(position: XYZ, channel: str|ExtValue[str]) -> float|ExtValue[float]:
        """
        **Receive signal in channel**
        
        Receive the aggregated signal power in a given channel.
        """
        ...

    @staticmethod
    def receiveSet(position: XYZ, channel: str|ExtValue[str], max_distance: float|ExtValue[float]) -> Vector:
        """
        **Receive signals in range**
        
        Get all signals in the specified range. Returns a read-only vector object containing Signal objects - individual signals can be accessed as result[0], .., result[result.size-1].
        """
        ...

    @staticmethod
    def receiveFilter(position: XYZ, channel: str|ExtValue[str], max_distance: float|ExtValue[float], flavor: float|ExtValue[float], flavorfilter: float|ExtValue[float]) -> float|ExtValue[float]:
        """
        **Receive filtered signal**
        
        Receive the aggregated signal power in a given channel.
        
        Additional filtering options:\n
        - Max distance only receives the neighbor signals (based on their physical location)\n
        - Flavor filtering: only signals having the flavor similar to the specified value will be received. The flavorfilter value is the difference of flavor that reduces the received signal to 0. The "flavor attenuation" is linear, i.e., signals differing by (filter/2) in flavor will be reduced to 50%.
        """
        ...

    @staticmethod
    def receiveSingle(position: XYZ, channel: str|ExtValue[str], max_distance: float|ExtValue[float]) -> Signal:
        """
        **Receive strongest**
        
        Find the signal source that has the highest signal power (taking into account distance).
        """
        ...

    @staticmethod
    def get(index: int|ExtValue[int]) -> Signal:
        """ **Access individual signals (index = 0 .. size-1)** """
        ...

    size: int|ExtValue[int]
    """ **Number of signals in this set** """
    @staticmethod
    def clear() -> None|ExtValue[None]:
        """ **Delete all signals** """
        ...


class XYZ(ExtValue):
    """ 3D vector """

    x: float|ExtValue[float]
    y: float|ExtValue[float]
    z: float|ExtValue[float]
    @staticmethod
    def new(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> XYZ:
        """
        **create new XYZ object**
        
        3D vectors objects can be also created using the (x,y,z) notation, i.e. var v=(1,2,3) is the same as var v=XYZ.new(1,2,3);
        """
        ...

    @staticmethod
    def newFromVector(arg1: Vector) -> XYZ:
        """
        **create new XYZ object**
        
        used for deserialization
        """
        ...

    @staticmethod
    def clone() -> XYZ:
        """
        **create new XYZ object copying the coordinates**
        
        Note: copying object references does not create new objects. Use clone() if a new object is needed.
        
        Example:\n
        var o1=(1,2,3), o2=o1, o3=o1.clone();\n
        o1.y=9999;\n
        //o2 is now (1,9999,3) but o3 is still (1,2,3)
        """
        ...

    @staticmethod
    def set(arg1: XYZ) -> None|ExtValue[None]:
        """ **set (copy) coordinates from another XYZ object** """
        ...

    @staticmethod
    def set3(x: float|ExtValue[float], y: float|ExtValue[float], z: float|ExtValue[float]) -> None|ExtValue[None]:
        """ **set individual 3 coordinates** """
        ...

    @staticmethod
    def add(arg1: XYZ) -> None|ExtValue[None]:
        """ Note: it does not return a new object, just modifies the existing one """
        ...

    @staticmethod
    def sub(arg1: XYZ) -> None|ExtValue[None]:
        """
        **subtract**
        
        Note: it does not return a new object, just modifies the existing one
        """
        ...

    @staticmethod
    def scale(arg1: float|ExtValue[float]) -> None|ExtValue[None]:
        """ **multiply by scalar** """
        ...

    length: float|ExtValue[float]
    @staticmethod
    def normalize() -> None|ExtValue[None]:
        """ scales the vector length to 1.0 """
        ...

    toString: str|ExtValue[str]
    """ **textual form** """
    toVector: Vector
    """ **vector of [x,y,z]** """
    @staticmethod
    def rotate(arg1: Orient) -> None|ExtValue[None]:
        """ **rotate using Orient object** """
        ...

    @staticmethod
    def revRotate(arg1: Orient) -> None|ExtValue[None]:
        """ **reverse rotate using Orient object** """
        ...

    @staticmethod
    def get(index: int|ExtValue[int]) -> float|ExtValue[float]:
        """
        **get one of coordinates**
        
        this function makes the XYZ objects "indexable" (so you can use [] for accessing subsequent fields, like in Vector)
        """
        ...


class ExpProperties(ExtValue):


    @staticmethod
    def _propertyClear() -> None|ExtValue[None]:
        """
        **Remove all properties**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAdd(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property (id,type,name,help)**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemove(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyChange(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Change property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAddGroup(name: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemoveGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyExists(name: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Check for property existence** """
        ...

    _property_changed_index: int|ExtValue[int]
    """ **Last changed property index** """
    _property_changed_id: str|ExtValue[str]
    """ **Last changed property id** """

class ExpState(ExtValue):


    @staticmethod
    def _propertyClear() -> None|ExtValue[None]:
        """
        **Remove all properties**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAdd(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property (id,type,name,help)**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemove(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyChange(id: str|ExtValue[str], type_description: str|ExtValue[str], name: str|ExtValue[str], flags: int|ExtValue[int], help_text: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Change property**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyAddGroup(name: str|ExtValue[str]) -> None|ExtValue[None]:
        """
        **Add property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyRemoveGroup(index: int|ExtValue[int]) -> None|ExtValue[None]:
        """
        **Remove property group**
        
        Using most _property functions is restricted for internal purposes. Use "property:" or "state:" definitions in your script files to change object properties.
        """
        ...

    @staticmethod
    def _propertyExists(name: str|ExtValue[str]) -> int|ExtValue[int]:
        """ **Check for property existence** """
        ...

    _property_changed_index: int|ExtValue[int]
    """ **Last changed property index** """
    _property_changed_id: str|ExtValue[str]
    """ **Last changed property id** """


