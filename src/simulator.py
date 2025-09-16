import pymunk

class Simulator:
    """
    Manages a 2D physics simulation using the Pymunk library.
    
    Each instance of this class represents a self-contained "world" with its
    own physics parameters (like gravity and friction).
    """
    def __init__(self, friction, gravity=(0, -900)):
        """
        Initializes a new simulation space.
        
        Args:
            friction (float): The coefficient of friction for objects in this world.
            gravity (tuple): A tuple (x, y) representing the gravitational force.
        """
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.friction = friction
        
        # We need a static floor for the object to slide on
        self._add_static_floor()
        
        # This will hold the dynamic object we want to track
        self.object_body = None

    def _add_static_floor(self):
        """Creates a static, immovable floor at the bottom of the space."""
        floor_body = self.space.static_body
        floor_shape = pymunk.Segment(floor_body, (-500, 10), (500, 10), 5)
        floor_shape.friction = 1.0  # High friction for the floor
        self.space.add(floor_shape)

    def add_dynamic_box(self, position=(0, 50), size=(50, 50), mass=10):
        """
        Adds a single dynamic box to the simulation. This will be the object
        we track and apply forces to.
        
        Args:
            position (tuple): The initial (x, y) position of the box.
            size (tuple): The (width, height) of the box.
            mass (int): The mass of the box.
            
        Returns:
            pymunk.Body: The body of the created box.
        """
        body = pymunk.Body(mass, pymunk.moment_for_box(mass, size))
        body.position = position
        
        shape = pymunk.Poly.create_box(body, size)
        shape.friction = self.friction # Apply the world-specific friction
        
        self.space.add(body, shape)
        self.object_body = body
        return body

    def apply_impulse(self, impulse=(5000, 0)):
        """
        Applies a one-time force (an impulse) to the dynamic object.
        
        Args:
            impulse (tuple): The (x, y) impulse vector to apply.
        """
        if self.object_body:
            self.object_body.apply_impulse_at_local_point(impulse)

    def step(self, dt=1/60.0):
        """
        Advances the simulation by one time step.
        
        Args:
            dt (float): The time delta for the physics step.
        """
        self.space.step(dt)

    def get_object_state(self):
        """
        Gets the current state (position) of the dynamic object.
        
        Returns:
            tuple: The (x, y) position of the object, or None if no object exists.
        """
        if self.object_body:
            return self.object_body.position.x, self.object_body.position.y
        return None
