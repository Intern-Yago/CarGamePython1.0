from ursina import *
import random

app = Ursina()
camera.orthographic = True

camera.fov = 10

car = Entity(model='quad', texture='./car', collider='box', scale=(2,1), rotation_z=-90, y = -1, x=.7)

road1 = Entity(model='quad', texture='./road', scale=15, z=1)
road2= duplicate(road1, y=15)
pair = [road1, road2]

enemies = []
positionsM = [0.6, 3.2]
positionsCM = [-1.4, -3.7]

def newEnemy():
  val = random.uniform(-2,2)

  new = duplicate(car, texture='./enemy', x = random.choice(positionsCM) if val < 0 else random.choice(positionsM), y = 25, color=color.random_color(),
                  rotation_z = 90 if val < 0 else -90)
  enemies.append(new)
  invoke(newEnemy, delay=0.5)
newEnemy()

def update():
    status = time.dt if car.y > -5 else 0
    acel = status
    car.x -=held_keys['a']*5*acel
    car.x +=held_keys['d']*5*acel
    for road in pair:
      road.y -= 6*acel
      if road.y < -15:
        road.y += 30
    for enemy in enemies:
      if enemy.x < 0:
        enemy.y -= 10 * acel
      else:
        enemy.y -= 5 * acel
      if enemy.y < -10:
        enemies.remove(enemy)
        destroy(enemy)
    if car.intersects().hit:
      car.y -= 2 * acel
      car.shake(magnitude=.5 if acel > 0 else 0, direction=(1,1), duration=.1)

    if car.x <= -4.6 or car.x >= 4.1:
      car.y -= 1*acel
    else:
      if car.y < -1:
        car.y += .5*acel


input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')

app.run()