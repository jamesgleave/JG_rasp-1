import led_matrix_interface as Jworld


def test_all():
    pass


def physics_test():
    world = Jworld.PWorld()
    for _ in range(25):
        world.add_pixel()

    for time in range(600):
        world.update()
        Jworld.time.sleep(0.0166666)

    world.empty()

    world.add_circle(r=5, points=20, pos=)

def




