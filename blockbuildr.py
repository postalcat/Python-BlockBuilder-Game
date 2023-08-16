from ursina import * #code incomplete, will specify later.
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.mouse import * #code incomplete, will specify later.
from random import randint
from math import sqrt
def calculate_distance_3d(point1, point2):#cool distance calculator i made(uses a math formula we learnt last semester)
    # helps with stopping player from destroying blocks too far away from themselves.
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    distance = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return distance
class Tree(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__()
        self.position_y = position[1]
        self.position_x = position[0]
        self.position_z = position[2]
        # Create the trunk
        for i in range(3):
            Block(position=(position[0], position[1] + i, position[2]),texture="download.png")
        # Create the leaves
        for x_offset in range(-2, 3):
            for z_offset in range(-2, 3):
                if abs(x_offset) + abs(z_offset) <= 3:  # Only create leaves within the circular area
                    Block(position=(self.position_x + x_offset, self.position_y + 3, self.position_z + z_offset),texture="leave.png")
                    Block(position=(self.position_x - x_offset, self.position_y + 3, self.position_z + z_offset),texture="leave.png")
                    Block(position=(self.position_x + x_offset, self.position_y + 4, self.position_z + z_offset),texture="leave.png")
                    Block(position=(self.position_x - x_offset, self.position_y + 4, self.position_z + z_offset),texture="leave.png")
        for x_offset in range(-1, 2):
            for z_offset in range(-1, 2):
                if abs(x_offset) + abs(z_offset) <= 3:
                    Block(position=(self.position_x - x_offset, self.position_y + 5, self.position_z + z_offset),texture="leave.png")
def set_inventory():
    global blocks 
    textlist = ["grass", "dirt.png", "stone.png", "wood.png"]
    blocks = []
    Entity(parent=camera.ui, model="quad", texture="white_cube", scale=(0.45, 0.13), position=(-0.05, -0.45))
    for i in range(4):
        counter = float(i/10)
        x = Entity(
            parent=camera.ui, 
            model="quad",
            texture_scale=(1, 1),
            texture = textlist[i],
            scale=(0.1, 0.1),
            origin=(0, 0),
            position=(-0.2 + counter, -0.447),
            color=color.color(0, 0, 1, .9)
        )
        blocks.append(x)
    print(blocks)
    return blocks
class Block(Button):
    active_texture = "grass"
    def __init__(self, position=(0, 0, 0), texture="grass"):
        super().__init__(
            parent=scene,
            model="cube",
            position=position,
            texture=texture,
            color=color.white,
            highlight_color=color.light_gray
        )
    @classmethod
    def change_block(cls, key):
        if key == "1":
            cls.active_texture = "grass"
            reset_textures(0)
        elif key == "2": 
            cls.active_texture = "dirt.png"
            reset_textures(1)
        elif key == "3":
            cls.active_texture = "stone.png"
            reset_textures(2)
        elif key == "4":
            cls.active_texture = "wood.png"
            reset_textures(3)
    def input(self, key):
        player_position = player.position
        block_placement_position = self.position
        if calculate_distance_3d(player_position, block_placement_position)>=5:
            return 
        else:
            if self.hovered:
                if key == "left mouse down":
                    Block(position=self.position + mouse.normal, 
                        texture=self.active_texture
                        )
                elif key == "right mouse down":
                    destroy(self)
class Island(Entity):
    def __init__(self, position=(0, 0, 0)):#additional functionality- can place islands at specific locations
        super().__init__(
            position_y=position[1],
            position_x=position[0],
            position_z=position[2]
        )
        for x in range(-10, 10):
            for z in range(-10, 10):
                Block(position=(x + position[0], 
                                position[1], z + 
                                position[2]), 
                                texture="grass.png"
                                )
        for x in range(-10, 10):
            for z in range(-10, 10):
                Block(position=(x + position[0], 
                                position[1] - 1, 
                                z + position[2]), 
                                texture="dirt.png"
                                )
        for x in range(-9, 9):
            for z in range(-9, 9):
                Block(position=(x + position[0], 
                                position[1] - 2, 
                                z + position[2]), 
                                texture="stone"
                                )
        for x in range(-8, 8):
            for z in range(-8, 8):
                Block(position=(x + position[0], 
                                position[1] - 3,
                                z + position[2]), 
                                texture="stone"
                                )
        for x in range(-8, 8):
            for z in range(-8, 8):
                Block(position=(x + position[0], 
                                position[1] - 4, 
                                z + position[2]), 
                                texture="stone"
                                )
        for x in range(-7, 7):
            for z in range(-7, 7):
                Block(position=(x + position[0], 
                                position[1] - 5, 
                                z + position[2]), 
                                texture="stone"
                                )
        for i in range(4):
            Tree(position=
                (randint(-8, 8) + position[0], 
                position[1], 
                randint(-8, 8) + position[2]))
def reset_textures(exception):
    for i in range(4):
        blocks[i].color = color.white
    blocks[exception].color = color.dark_gray
if __name__ == "__main__":
    app = Ursina()
    skybox_image = load_texture("x.png")
    Sky(texture=skybox_image)
    player = FirstPersonController(y=2, origin=(0, 0, 0))
    spawn_position = player.position
    def update():
        if player.y < -50:
            player.position = (randint(0, 8), 0, randint(0, 8))
    def input(key):
        Block.change_block(key)
    island = Island((0,0,0))
    active_texture = "grass"
    set_inventory()
    app.run()
