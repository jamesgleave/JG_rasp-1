import led_matrix_interface as Jworld
import led_matrix_animator


class GameEngine(Jworld.physics_engine.Physics):
    def __init__(self, air_resistance=0.95, g=-.5, fps=60):
        super(GameEngine, self).__init__(air_resistance=air_resistance, g=g, fps=fps)
        self.player = None

    def check_collisions(self):
        collider = self.player.collider

        for o in self.object_list:
            obstacle = o.collider
            if collider.x < obstacle.x + obstacle.width \
                    and collider.x + collider.width > obstacle.x \
                    and collider.y < obstacle.y + obstacle.height \
                    and collider.y + collider.height > obstacle.y:
                return o.name

        return None

    def set_player(self, player):
        self.player = player

    def update_environment(self):
        self.check_collisions()
        for obj in self.object_list:
            obj.update()
        frame_sleep = 1 / self.fps
        Jworld.time.sleep(frame_sleep)


class Player(Jworld.physics_engine.PhysicsBody):
    def __init__(self, matrix, position, animator, controller, jump_force=100, size=(3, 3), game_engine=None,
                 mass=5, led_size=(64, 32), bounciness=0.1,
                 gravity_enabled=True):

        super(Player, self).__init__(position=position, environment=game_engine, mass=mass, matrix=matrix,
                                     led_size=led_size, bounciness=bounciness, gravity_enabled=gravity_enabled)

        self.animator = animator
        self.controller = controller
        self.size = size
        self.jump_force = jump_force
        self.name = "player"
        self.collider = self.set_collider_size()

    def check_bounds(self):
        x = self.position.x
        y = self.position.y

        if x + self.size[0] > self.led_size[0] or x - self.size[0] < 0:
            self.bounce(1)

        if y + self.size[1] > self.led_size[1] or y - self.size[1] < 1:
            self.bounce(2)

    def jump(self):
        self.add_force(Jworld.Vector2(0, self.jump_force))

    def set_collider_size(self):
        position = self.position
        x = position.x
        y = position.y
        w, l = self.size

        return {"x": x, "y": y, "width": w, "height": l}


class GameBody(Jworld.physics_engine.PhysicsBody):
    def __init__(self, matrix, position, name, animator=None, controller=None, jump_force=100, size=(3, 3), environment=None,
                 mass=5, led_size=(64, 32), bounciness=0.1,
                 gravity_enabled=True):

        super(GameBody, self).__init__(position=position, environment=environment, mass=mass, matrix=matrix,
                                       led_size=led_size, bounciness=bounciness, gravity_enabled=gravity_enabled)

        self.animator = animator
        self.controller = controller
        self.size = size
        self.jump_force = jump_force
        self.name = name
        self.collider = self.set_collider_size()

    def set_collider_size(self):
        position = self.position
        x = position.x
        y = position.y
        w, l = self.size

        return {"x": x, "y": y, "width": w, "height": l}




