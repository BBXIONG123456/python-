from ursina import *
from ursina import Default, camera
from ursina.prefabs.first_person_controller import FirstPersonController
#柏林噪声
from perlin_noise import PerlinNoise
seed = int(input('请输入种子(数字):'))
app = Ursina()


grass_texture = load_texture('grass_block.png')
stone_texture = load_texture('stone_block.png')
brick_texture = load_texture('brick_block.png')
dirt_texture = load_texture('dirt_block.png')
sky_texture = load_texture('skybox.png')
arm_texture = load_texture('arm_texture.png')
TNT_texture = load_texture('TNT.png')
cao_texture =load_texture('cao.png')
shi_texture=load_texture('shi.png')
ni_texture=load_texture('ni.png')
punch_sound=Audio('punch_sound',loop=False,autoplay=False)
window.exit_button.visible = False
block_pick = 6
scene.fog_color=color.white
scene.fog_density = 0.04

def input(key):
    if key =='q' or key == 'escape':
        quit()

def update():
    global block_pick
    if held_keys['1']:block_pick = 1
    if held_keys['2']:block_pick = 2
    if held_keys['3']:block_pick = 3
    if held_keys['4']:block_pick = 4
    if held_keys['5']:block_pick = 5
    if held_keys['6']:block_pick = 6
    if held_keys['7']:block_pick = 7
    if held_keys['8']:block_pick = 8

    if held_keys['right mouse'] or held_keys['left mouse']:
        hand.active()
    else:
        hand.passive()


class Block(Button):
    def __init__(self,position = (0,0,0),texture = cao_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            #highlight_color = color.gray
            scale = 0.5
        )


    def input(self,key):
        if self.hovered:
            if key =='right mouse down':
                punch_sound.play()
                if block_pick==1:block = Block(position=self.position+mouse.normal,texture = grass_texture)
                if block_pick==2:block = Block(position=self.position+mouse.normal,texture = stone_texture)
                if block_pick==3:block = Block(position=self.position+mouse.normal,texture = brick_texture)
                if block_pick==4:block = Block(position=self.position+mouse.normal,texture = dirt_texture)
                if block_pick==5:block = Block(position=self.position+mouse.normal,texture = TNT_texture)
                if block_pick==6:block = Block(position=self.position+mouse.normal,texture = cao_texture)
                if block_pick==7:block = Block(position=self.position+mouse.normal,texture = shi_texture)
                if block_pick==8:block = Block(position=self.position+mouse.normal,texture = ni_texture)
            if key =='left mouse down':
                punch_sound.play()
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model = 'sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model = 'arm',
            texture=arm_texture,
            scale=0.2,
            double_sided=True,
            rotation=Vec3(150,-10,0),
            position=Vec2(0.9,-0.6)
        )
    
    def active(self):
        self.position=Vec2(0.8,-0.5)
    def passive(self):
        self.position=Vec2(0.9,-0.6)
noise=PerlinNoise(octaves=4,seed=seed)
scale=24

for z in range(30):
    for x in range(30):
        block = Block(position=(x,0,z))
        block.y=floor(noise([x/scale,z/scale])*8)

player = FirstPersonController()
sky = Sky()
hand=Hand()

app.run()