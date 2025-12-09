from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import random
import math

#var
player_pos = [0, 0, 0] 
player_angle = 0
player_life = 5
game_score = 0 
bullets_missed = 0
game_over = False
player_fallen = False  

camera_pos = [0, 500, 500]
camera_angle = 0
camera_height = 500
camera_mode = "third"

cheat_mode = False   
cheat_vision = False
cheat_shot_cooldown = 0 

bullets = []
bullet_speed = 15 

enemies = [] 
enemy_speed = 0.1
num_enemies = 5
enemy_pulse = 0    

fovY = 120     
GRID_LENGTH = 600    
BOUNDARY_HEIGHT = 100  
CHEAT_SHOT_DELAY = 30 

class Bullet:
    def __init__(self, x, y, z, angle):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.size = 15
        self.lifetime = 1000
    
    def update(self):
        angle_rad = math.radians(self.angle)
        self.x += bullet_speed * math.cos(angle_rad)
        self.y += bullet_speed * math.sin(angle_rad)
        self.lifetime -= 1
        if abs(self.x) > GRID_LENGTH or abs(self.y) > GRID_LENGTH or self.lifetime <= 0:
            return False
        return True
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(1, 0.5, 0)
        glutSolidCube(self.size)
        glPopMatrix()


class Enemy:
    def __init__(self):
        self.respawn()
        self.size = 40
        self.head_size = 20
    
    def respawn(self):
        # Spawn at a random position on the grid
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(GRID_LENGTH/2, GRID_LENGTH*0.9)
        self.x = distance * math.cos(angle)
        self.y = distance * math.sin(angle)
        self.z = 0
    
    def update(self):
        global player_life, game_over, player_fallen
        
        # Move towards player
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 0:
            self.x += (dx/dist) * enemy_speed
            self.y += (dy/dist) * enemy_speed
        
        # Check collision with player
        if dist < 60 and not game_over:  # If enemy touches player
            player_life -= 1
            self.respawn()
            
            if player_life <= 0:
                game_over = True
                player_fallen = True
    
    def draw(self):
        pulse_factor = 0.8 + 0.2 * math.sin(enemy_pulse * 0.1)
        
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)       
        #body
        glColor3f(0.8, 0.2, 0.2)
        gluSphere(gluNewQuadric(), self.size * pulse_factor, 16, 16)        
        #matha
        glTranslatef(0, 0, self.size + self.head_size / 2)
        glColor3f(0.2, 0.2, 0.8)
        gluSphere(gluNewQuadric(), self.head_size * pulse_factor, 16, 16)
        glPopMatrix()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, 1000, 0, 800) 
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_player():
    if game_over and player_fallen:
        draw_fallen_player()
    else:
        draw_standing_player()
def draw_standing_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 0, 1)
    
    glPushMatrix()
    glColor3f(0.0, 0.8, 0.0)  
    glTranslatef(0, 0, 50) 
    glRotatef(90, 0, 0, 1) 
    glScalef(30, 20, 60)  
    glutSolidCube(1)
    glPopMatrix()
    
    #matha
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(0, 0, 100)
    gluSphere(gluNewQuadric(), 15, 16, 16)  # Head
    glPopMatrix()
    
    #legs
    glColor3f(1.0, 0.8, 0.6)  # Green
    
    glPushMatrix()
    glTranslatef(0, -10, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 50, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 10, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 50, 10, 10)
    glPopMatrix()
    
    #hand
    glColor3f(1.0, 0.8, 0.6)

    glPushMatrix()
    glTranslatef(0, -20, 70) 
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 4, 4, 25, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 20, 70)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 4, 4, 25, 10, 10)
    glPopMatrix()

    glPushMatrix()
    
    #Gun
    glTranslatef(0, 0, 70)
    glColor3f(0.3, 0.3, 0.3)
    glutSolidCube(15)
    
    #barrel
    glTranslatef(0, 0, 0)
    glRotatef(90, 1, 0, 0)
    glRotatef(90, 0, 1, 0)
    glColor3f(0.5, 0.5, 0.5)
    gluCylinder(gluNewQuadric(), 4, 4, 35, 10, 10)
    
    glPopMatrix()
    glPopMatrix()


def draw_fallen_player():
    glPushMatrix()

    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 0, 1)

    glRotatef(90, 1, 0, 0)

    glColor3f(0.5, 0.5, 0.5) 
    gluSphere(gluNewQuadric(), 30, 16, 16) 

    glPushMatrix()
 
    glTranslatef(0, 40, 0)
    glColor3f(0.3, 0.3, 0.3)
    glutSolidCube(20)

    glTranslatef(0, 0, 35)
    glColor3f(0.5, 0.5, 0.5)
    gluCylinder(gluNewQuadric(), 5, 5, 70, 10, 10)
    glPopMatrix()
    glPopMatrix()


def draw_grid():

    glBegin(GL_QUADS)

    grid_divisions = 12
    square_size = 2 * GRID_LENGTH / grid_divisions
    
    for i in range(grid_divisions):
        for j in range(grid_divisions):
            x1 = -GRID_LENGTH + i * square_size
            y1 = -GRID_LENGTH + j * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1) 
            else:
                glColor3f(0.7, 0.5, 0.95) 

            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    glEnd()
    draw_boundary()


def draw_boundary():
    glPushMatrix()
    wall_height = BOUNDARY_HEIGHT
    
    glColor3f(0.5, 0.5, 0.8)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glEnd()

    glColor3f(0.8, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glEnd()

    glColor3f(0.5, 0.8, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glEnd()
    
    glColor3f(0.8, 0.8, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glEnd()
    
    glPopMatrix()

def fire_bullet():
    global bullets
    gun_height = 30 
    gun_length = 0 
    
    angle_rad = math.radians(player_angle)
    
    bullet_x = player_pos[0]
    bullet_y = player_pos[1]
    bullet_z = player_pos[2] + gun_height  
    
    bullet_y -= gun_length * math.cos(angle_rad)
    bullet_x += gun_length * math.sin(angle_rad)
    
    shooting_angle = (player_angle ) % 360
    
    bullets.append(Bullet(bullet_x, bullet_y, bullet_z, shooting_angle))


def update_bullets():
    global bullets, bullets_missed, game_over, game_score
    
    i = 0
    while i < len(bullets):
        if not bullets[i].update():
            bullets.pop(i)
            if not cheat_mode:  
                bullets_missed += 1
                
                if bullets_missed >= 10:
                    game_over = True
                    player_fallen = True
        else:
            for enemy in enemies:
                dx = bullets[i].x - enemy.x
                dy = bullets[i].y - enemy.y
                dz = bullets[i].z - (enemy.z + enemy.size)
                dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                if dist < enemy.size: 

                    bullets.pop(i)
                    enemy.respawn()
                    game_score += 1
                    i -= 1 
                    break
            i += 1


def init_enemies():
    global enemies
    enemies = []
    for _ in range(num_enemies):
        enemies.append(Enemy())


def update_enemies():
    global enemy_pulse
    
    enemy_pulse += 1
    
    for enemy in enemies:
        enemy.update()


def update_cheat_mode():
    global player_angle, cheat_shot_cooldown
    
    if cheat_mode:
        if cheat_shot_cooldown > 0:
            cheat_shot_cooldown -= 1
            return
        
        closest_dist = float('inf')
        closest_enemy = None
        
        for enemy in enemies:
            dx = enemy.x - player_pos[0]
            dy = enemy.y - player_pos[1]
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < closest_dist:
                closest_dist = dist
                closest_enemy = enemy
        
        if closest_enemy:
            angle_to_enemy = math.degrees(math.atan2(
                closest_enemy.y - player_pos[1],
                closest_enemy.x - player_pos[0])) % 360
            
            player_angle = angle_to_enemy
            
            if closest_dist < GRID_LENGTH * 0.8:
                fire_bullet()
                cheat_shot_cooldown = CHEAT_SHOT_DELAY


def reset_game():
    global player_pos, player_angle, player_life, game_score, bullets_missed
    global game_over, player_fallen, bullets, enemies
    
    player_pos = [0, 0, 0]
    player_angle = 0
    player_life = 5
    
    game_score = 0
    bullets_missed = 0
    game_over = False
    player_fallen = False
    
    bullets = []
    init_enemies()


def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, cheat_vision, game_over
    
    if game_over:
        if key == b'r':
            reset_game()
        return
    move_speed = 10
    
    if key == b'w':
        player_pos[0] += move_speed * math.cos(math.radians(player_angle))
        player_pos[1] += move_speed * math.sin(math.radians(player_angle))
        
        player_pos[0] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[0]))
        player_pos[1] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[1]))

    if key == b's':
        player_pos[0] -= move_speed * math.cos(math.radians(player_angle))
        player_pos[1] -= move_speed * math.sin(math.radians(player_angle))
        
        player_pos[0] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[0]))
        player_pos[1] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[1]))
    if key == b'a':
        player_angle = (player_angle + 5) % 360
    if key == b'd':
        player_angle = (player_angle - 5) % 360
    if key == b'c':
        cheat_mode = not cheat_mode
    if key == b'v':
        cheat_vision = not cheat_vision
        
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global camera_angle, camera_height, camera_pos
    
    if key == GLUT_KEY_UP:
        camera_height += 20
        camera_pos[2] = camera_height 
        radius = math.sqrt(camera_pos[0]**2 + camera_pos[1]**2)
        camera_pos[0] = radius * math.sin(math.radians(camera_angle))
        camera_pos[1] = radius * math.cos(math.radians(camera_angle))

    if key == GLUT_KEY_DOWN:
        camera_height = max(100, camera_height - 20)
        camera_pos[2] = camera_height 
        radius = math.sqrt(camera_pos[0]**2 + camera_pos[1]**2)
        camera_pos[0] = radius * math.sin(math.radians(camera_angle))
        camera_pos[1] = radius * math.cos(math.radians(camera_angle))

    if key == GLUT_KEY_LEFT:
        camera_angle = (camera_angle + 5) % 360
        radius = math.sqrt(camera_pos[0]**2 + camera_pos[1]**2)
        camera_pos[0] = radius * math.sin(math.radians(camera_angle))
        camera_pos[1] = radius * math.cos(math.radians(camera_angle))

    if key == GLUT_KEY_RIGHT:
        camera_angle = (camera_angle - 5) % 360
        radius = math.sqrt(camera_pos[0]**2 + camera_pos[1]**2)
        camera_pos[0] = radius * math.sin(math.radians(camera_angle))
        camera_pos[1] = radius * math.cos(math.radians(camera_angle))

    glutPostRedisplay()


def mouseListener(button, state, x, y):

    global camera_mode, game_over
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        fire_bullet()

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if camera_mode == "third":
            camera_mode = "first"
        else:
            camera_mode = "third"

    glutPostRedisplay()


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if camera_mode == "first" or (cheat_mode and cheat_vision):
        gluPerspective(90, 1.25, 0.1, 1500)
    else:
        gluPerspective(fovY, 1.25, 0.1, 1500)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if camera_mode == "first" or (cheat_mode and cheat_vision):

        eye_height = 100  
        gun_offset = 35 

        angle_rad = math.radians(player_angle)
        eye_x = player_pos[0]
        eye_y = player_pos[1] + 0  
        eye_z = player_pos[2] + eye_height+20
        
        look_dist = 50.0 
        look_x = eye_x + look_dist * math.cos(math.radians(player_angle))
        look_y = eye_y + look_dist * math.sin(math.radians(player_angle))
        look_z = eye_z  
        
        gluLookAt(eye_x, eye_y, eye_z,
                  look_x, look_y, look_z,
                  0, 0, 1)
    else:
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                  0, 0, 0,
                  0, 0, 1)


def idle():
    if not game_over:
        update_bullets()
        update_enemies()
        
        if cheat_mode:
            update_cheat_mode()
    
    glutPostRedisplay()


def showScreen():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800) 
    
    glEnable(GL_DEPTH_TEST)
    
    setupCamera()
    
    draw_grid()
    
    draw_player()
    
    for enemy in enemies:
        enemy.draw()
    
    for bullet in bullets:
        bullet.draw()
    
    if game_over:
        draw_text(400, 400, "GAME OVER")
        draw_text(400, 370, "Press R to restart")
    
    draw_text(10, 770, f"Life: {player_life}")
    draw_text(10, 740, f"Score: {game_score}")
    draw_text(10, 710, f"Player Bullets Missed: {bullets_missed}/10")
    
    if cheat_mode:
        draw_text(800, 770, "CHEAT MODE ON")
    
    glutSwapBuffers()

def main():
    init_enemies()
    
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  
    glutInitWindowSize(1000, 800)  
    glutInitWindowPosition(0, 0)  
    glutCreateWindow(b"Bullet Frenzy - 3D Game")
    
    glutDisplayFunc(showScreen)  
    glutKeyboardFunc(keyboardListener)  
    glutSpecialFunc(specialKeyListener)  
    glutMouseFunc(mouseListener)  
    glutIdleFunc(idle)  
    
    glutMainLoop()

if __name__ == "__main__":
    main()