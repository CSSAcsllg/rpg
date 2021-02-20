import pygame
from pygame.locals import *
import sys
import random
from tkinter import messagebox
from tkinter import *
import numpy

pygame.init()  # Begin pygame
pygame.mixer.init()

# Declaring variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

EVENT_NULL = 100
EVENT_ATTACKING = 101
EVENT_KILL = 102
EVENT_DIED = 103
EVENT_GET = 104
EVENT_MOVING = 105

EVENT_HIT_COOLDOWN = pygame.USEREVENT + 1
EVENT_NEXT = pygame.USEREVENT + 4


# Create the display
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


# light shade of the button 
color_light = (170,170,170)
color_dark = (100,100,100)
color_white = (255,255,255) 
  
# defining a font
headingfont = pygame.font.SysFont("Verdana", 40)
regularfont = pygame.font.SysFont('Corbel',25)
smallerfont = pygame.font.SysFont('Corbel',16) 
text = regularfont.render('LOAD' , True , color_light)

pygame.mixer.music.load("Music/background.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops = -1)


# Run animation for the RIGHT
run_ani_R = [pygame.image.load("Images/Player/Player_Sprite_R.png"), pygame.image.load("Images/Player/Player_Sprite2_R.png"),
             pygame.image.load("Images/Player/Player_Sprite3_R.png"),pygame.image.load("Images/Player/Player_Sprite4_R.png"),
             pygame.image.load("Images/Player/Player_Sprite5_R.png"),pygame.image.load("Images/Player/Player_Sprite6_R.png"),
             pygame.image.load("Images/Player/Player_Sprite_R.png")]

# Run animation for the LEFT
run_ani_L = [pygame.image.load("Images/Player/Player_Sprite_L.png"), pygame.image.load("Images/Player/Player_Sprite2_L.png"),
             pygame.image.load("Images/Player/Player_Sprite3_L.png"),pygame.image.load("Images/Player/Player_Sprite4_L.png"),
             pygame.image.load("Images/Player/Player_Sprite5_L.png"),pygame.image.load("Images/Player/Player_Sprite6_L.png"),
             pygame.image.load("Images/Player/Player_Sprite_L.png")]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("Images/Player/Player_Sprite_R.png"), pygame.image.load("Images/Player/Player_Attack_R.png"),
                pygame.image.load("Images/Player/Player_Attack2_R.png"),pygame.image.load("Images/Player/Player_Attack2_R.png"),
                pygame.image.load("Images/Player/Player_Attack3_R.png"),pygame.image.load("Images/Player/Player_Attack3_R.png"),
                pygame.image.load("Images/Player/Player_Attack4_R.png"),pygame.image.load("Images/Player/Player_Attack4_R.png"),
                pygame.image.load("Images/Player/Player_Attack5_R.png"),pygame.image.load("Images/Player/Player_Attack5_R.png"),
                pygame.image.load("Images/Player/Player_Sprite_R.png")]

# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("Images/Player/Player_Sprite_L.png"), pygame.image.load("Images/Player/Player_Attack_L.png"),
                pygame.image.load("Images/Player/Player_Attack2_L.png"),pygame.image.load("Images/Player/Player_Attack2_L.png"),
                pygame.image.load("Images/Player/Player_Attack3_L.png"),pygame.image.load("Images/Player/Player_Attack3_L.png"),
                pygame.image.load("Images/Player/Player_Attack4_L.png"),pygame.image.load("Images/Player/Player_Attack4_L.png"),
                pygame.image.load("Images/Player/Player_Attack5_L.png"),pygame.image.load("Images/Player/Player_Attack5_L.png"),
                pygame.image.load("Images/Player/Player_Sprite_L.png")]

# Animations for the Health Bar
health_ani = [pygame.image.load("Images/heart/heart0.png"), pygame.image.load("Images/heart/heart.png"),
              pygame.image.load("Images/heart/heart2.png"), pygame.image.load("Images/heart/heart3.png"),
              pygame.image.load("Images/heart/heart4.png"), pygame.image.load("Images/heart/heart5.png")]


class Background(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.bgimage = pygame.image.load("Images/Items/Background.png")
            self.immune_image = pygame.image.load("Images/Items/Background_immune.png")
            self.image = self.bgimage
            self.rectBGimg = self.bgimage.get_rect()        
            self.bgY = 0
            self.bgX = 0

      def render(self):
            displaysurface.blit(self.image, (self.bgX, self.bgY))      


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Items/Ground.png")
        self.rect = self.image.get_rect(center = (350, 350))
        self.bgX1 = 0
        self.bgY1 = 285

    def render(self):
        displaysurface.blit(self.image, (self.bgX1, self.bgY1)) 

class Sound(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sounds = []
        for i in range(0,5):
            sound = pygame.mixer.Sound("Music/" + str(i + 100) + ".wav")
            self.sounds.append(sound)
            sound.set_volume(0.4)
    def play(self,event):
        self.sounds[event - 100].play()

class Item(pygame.sprite.Sprite):
      def __init__(self, itemtype):
            super().__init__()
            if itemtype == 1: self.image = pygame.image.load("Images/heart/heart.png")
            elif itemtype == 2: self.image = pygame.image.load("Images/Items/coin.png")
            self.rect = self.image.get_rect()
            self.type = itemtype
            self.posx = 0
            self.posy = 0
            
      def render(self):
            self.rect.x = self.posx
            self.rect.y = self.posy
            displaysurface.blit(self.image, self.rect)

      def update(self):
            hits = pygame.sprite.spritecollide(self, Playergroup, False)
            # Code to be activated if item comes in contact with player
            if hits:
                
                if player.health < 5 and self.type == 1:
                    sound.play(EVENT_GET)
                    player.health += 1
                    health.image = health_ani[player.health]
                    self.kill()
                if self.type == 2:
                    sound.play(EVENT_GET)
                    handler.money += 1
                    self.kill()
                        


class Player(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Player/Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "RIGHT"

        # Movement 
        self.jumping = False
        self.running = False
        self.move_frame = 0

        #Combat
        self.attacking = False
        self.cooldown = False
        self.immuned = False
        self.immune_timer = pygame.USEREVENT + 3
        self.special = False
        self.experiance = 0
        self.attack_frame = 0
        self.health = 5
        self.mana = 20


      def move(self):
          if cursor.wait == 1: return
          
          # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
          self.acc = vec(0,0.5)

          # Will set running to False if the player has slowed down to a certain extent
          if abs(self.vel.x) > 0.3:
                self.running = True
          else:
                self.running = False

          # Returns the current key presses
          pressed_keys = pygame.key.get_pressed()

          # Accelerates the player in the direction of the key press
          if pressed_keys[K_a]:
                self.acc.x = -ACC
          if pressed_keys[K_d]:
                self.acc.x = ACC 

          # Formulas to calculate velocity while accounting for friction
          self.acc.x += self.vel.x * FRIC
          self.vel += self.acc
          self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values

          # This causes character warping from one point of the screen to the other
          if self.pos.x > WIDTH:
                self.pos.x = 0
          if self.pos.x < 0:
                self.pos.x = WIDTH
        
          self.rect.midbottom = self.pos  # Update rect with new pos            

      def gravity_check(self):
          hits = pygame.sprite.spritecollide(player ,ground_group, False)
          if self.vel.y > 0:
              if hits:
                  lowest = hits[0]
                  if self.pos.y < lowest.rect.bottom:
                      self.pos.y = lowest.rect.top + 1
                      self.vel.y = 0
                      self.jumping = False


      def update(self):
          if cursor.wait == 1: return
          
          # Return to base frame if at end of movement sequence 
          if self.move_frame > 6:
                self.move_frame = 0
                return

          # Move the character to the next frame if conditions are met 
          if self.jumping == False and self.running == True:  
                if self.vel.x > 0:
                      self.image = run_ani_R[self.move_frame]
                      self.direction = "RIGHT"
                else:
                      self.image = run_ani_L[self.move_frame]
                      self.direction = "LEFT"
                self.move_frame += 1

          # Returns to base frame if standing still and incorrect frame is showing
          if abs(self.vel.x) < 0.2 and self.move_frame != 0:
                self.move_frame = 0
                if self.direction == "RIGHT":
                      self.image = run_ani_R[self.move_frame]
                elif self.direction == "LEFT":
                      self.image = run_ani_L[self.move_frame]

      def attack(self):  

          sound.play(EVENT_ATTACKING)      
          # If attack frame has reached end of sequence, return to base frame      
          if self.attack_frame > 10:
                self.attack_frame = 0
                self.attacking = False

          # Check direction for correct animation to display  
          if self.direction == "RIGHT":
                 self.image = attack_ani_R[self.attack_frame]
          elif self.direction == "LEFT":
                 self.correction()
                 self.image = attack_ani_L[self.attack_frame] 

          # Update the current attack frame  
          self.attack_frame += 1
          
      def immune(self):
            if self.mana >= 15 :
                  self.mana -= 15
                  self.immuned = True
                  background.image = background.immune_image
                  pygame.time.set_timer(self.immune_timer, 4000)

      def jump(self):
        self.rect.x += 1

        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        
        self.rect.x -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
           self.jumping = True 
           self.vel.y = -12

      def correction(self):
          # Function is used to correct an error
          # with character position on left attack frames
          if self.attack_frame == 1:
                self.pos.x -= 20
          if self.attack_frame == 10:
                self.pos.x += 20
                
      def player_hit(self):
        if self.cooldown == False and self.immuned == False:      
            self.cooldown = True # Enable the cooldown
            pygame.time.set_timer(EVENT_HIT_COOLDOWN, 1000) # Resets cooldown in 1 second

            sound.play(EVENT_DIED)
            self.health = self.health - 1
            health.image = health_ani[self.health]
            
            if self.health <= 0:
                self.kill()
                pygame.display.update()
      
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Items/Enemy.png")
        self.rect = self.image.get_rect()     
        self.pos = vec(0,0)
        self.vel = vec(0,0)

        self.direction = random.randint(0,1) # 0 for Right, 1 for Left
        self.vel.x = random.randint(2,6) / 2  # Randomised velocity of the generated enemy
        self.mana = random.randint(1, 3)  # Randomised mana amount obtained upon    

        # Sets the intial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235


      def move(self):
        if cursor.wait == 1: return
        
        # Causes the enemy to change directions upon reaching the end of screen    
        if self.pos.x >= (WIDTH-20):
              self.direction = 1
        elif self.pos.x <= 0:
              self.direction = 0

        # Updates positon with new values     
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
            
        self.rect.topleft = self.pos # Updates rect
               
      def update(self):
            # Checks for collision with the Player
            hits = pygame.sprite.spritecollide(self, Playergroup, False)

            # Activates upon either of the two expressions being true
            if hits and player.attacking == True:
                
                sound.play(EVENT_KILL)

                self.kill()
                handler.dead_enemy_count += 1
                  
                if player.mana < 30: player.mana += self.mana # Release mana
                player.experiance += 1   # Release expeiriance
                  
                rand_num = numpy.random.uniform(0, 100)
                item_no = 0
                if rand_num >= 0 and rand_num <= 5:  # 1 / 20 chance for an item (health) drop
                    item_no = 1
                elif rand_num > 5 and rand_num <= 15:
                    item_no = 2

                if item_no != 0:
                    # Add Item to Items group
                    item = Item(item_no)
                    Items.add(item)
                    # Sets the item location to the location of the killed enemy
                    item.posx = self.pos.x
                    item.posy = self.pos.y
                 

            # If collision has occured and player not attacking, call the "hit" func.            
            elif hits and player.attacking == False:
                  player.player_hit()
                  
      def render(self):
            # Displayed the enemy on screen
            displaysurface.blit(self.image, self.rect)


class Castle(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.hide = False
            self.image = pygame.image.load("Images/Items/castle.png")

      def update(self):
            if self.hide == False:
                  displaysurface.blit(self.image, (400, 80))

class Trader(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("Images/Items/trader.png")
        self.rect = self.image.get_rect()
        self.posx = 200
        self.posy = 235
        self.hit = False

    def update(self):
        if self.hide == False:
            hits = pygame.sprite.spritecollide(self, Playergroup,False)
            if hits:
                self.hit = True
            else: 
                self.hit = False
    def buy(self):
        self.root = Tk()
        self.root.geometry("200x200")

        button = Button(self.root, text = "BUY",width = 18,height = 2,
                        command = self.bought)
        button.place(x = 40 , y = 70)

        self.root.mainloop()
    def bought(self):
        if handler.money >= 2 and player.health < 5:
            handler.money -= 2
            player.health += 1
            health.image = health_ani[player.health]
            messagebox.showinfo("Info","Successfully!")
    def render(self):
        if self.hide == False:    
            self.rect.x = self.posx
            self.rect.y = self.posy
            displaysurface.blit(self.image, self.rect)            

class EventHandler():
    def __init__(self):
            self.enemy_count = 0
            self.dead_enemy_count = 0
            self.battle = False
            self.enemy_generation = pygame.USEREVENT + 2
            self.stage = 1
            self.money = 0
            self.world = 0
            self.next = True

            self.stage_enemies = []
            for x in range(1, 11):
                  self.stage_enemies.append(int((x ** 2 / 2) + 1))
            
    def stage_handler(self):
            # Code for the Tkinter stage selection window
            self.root = Tk()
            self.root.geometry('200x170')
            
            button1 = Button(self.root, text = "Twilight Dungeon", width = 18, height = 2,
                            command = self.world1)
            button2 = Button(self.root, text = "Skyward Dungeon", width = 18, height = 2,
                            command = self.world2)
            button3 = Button(self.root, text = "Hell Dungeon", width = 18, height = 2,
                            command = self.world3)
             
            button1.place(x = 40, y = 15)
            button2.place(x = 40, y = 65)
            button3.place(x = 40, y = 115)
            
            self.root.mainloop()

    def to_world(self):
        pygame.time.set_timer(self.enemy_generation, 2500 - self.world * 500)
        button.imgdisp = 1
        castle.hide = True
        trader.hide = True
        self.battle = True  

    def world1(self):
        self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 2000)
        button.imgdisp = 1
        castle.hide = True
        trader.hide = True
        self.battle = True  
        self.world = 1

    def world2(self):
        self.root.destroy()
        self.battle = True
        button.imgdisp = 1
        castle.hide = True
        trader.hide = True
        pygame.time.set_timer(self.enemy_generation, 1500)
        self.world = 2
            

    def world3(self):
        self.root.destroy()
        self.battle = True
        button.imgdisp = 1
        castle.hide = True
        trader.hide = True
        pygame.time.set_timer(self.enemy_generation, 1000)
        self.world = 3
 
    def next_stage(self):  # Code for when the next stage is clicked
            button.imgdisp = 1
            self.stage += 1
            print("Stage: "  + str(self.stage))
            self.enemy_count = 0
            self.dead_enemy_count = 0
            pygame.time.set_timer(self.enemy_generation, 2000 - self.world * 500 - (50 * self.stage))      

    def update(self):
            if self.dead_enemy_count == self.stage_enemies[self.stage - 1]:
                  self.dead_enemy_count = 0
                  stage_display.clear = True
                  stage_display.stage_clear()

    def home(self):
            # Reset Battle code
            pygame.time.set_timer(self.enemy_generation, 0)
            self.battle = False
            #self.enemy_count = 0
            #self.dead_enemy_count = 0

            # Destroy any enemies or items lying around
            for group in Enemies, Items:
                  for entity in group:
                        entity.kill()
            
            # Bring back normal backgrounds
            castle.hide = False
            trader.hide = False
            background.bgimage = pygame.image.load("Images/Items/Background.png")
            ground.image = pygame.image.load("Images/Items/Ground.png")
    def restart(self):
        player.experiance = 0
        player.mana = 20
        player.health = 5
        player.pos = vec((340, 240))
        self.money = 0
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 1
        self.world = 0
        health.image = health_ani[player.health]
        self.home()
        game_over_bar.game_over = False

class HealthBar(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("Images/heart/heart5.png")

      def render(self):
            displaysurface.blit(self.image, (10,10))

class GameOverBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((350,175))
        self.image = pygame.image.load("Images/Items/home_small.png")
        self.text = headingfont.render("Game Over",True,color_white)
        self.game_over = False
    def render(self):
        self.game_over = True
        displaysurface.blit(self.surf,(175,88))
        displaysurface.blit(self.text,(235,120))
        displaysurface.blit(self.image,(330,190))

class StageDisplay(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.text = headingfont.render("STAGE: " + str(handler.stage), True, color_dark)
            self.rect = self.text.get_rect()
            self.posx = -100
            self.posy = 100
            self.display = False
            self.clear = False

      def move_display(self):
            # Create the text to be displayed
            self.text = headingfont.render("STAGE: " + str(handler.stage), True, color_dark)
            if self.posx < 720:
                  self.posx += 6
                  displaysurface.blit(self.text, (self.posx, self.posy))
            else:
                  self.display = False
                  self.posx = -100
                  self.posy = 100


      def stage_clear(self):
            self.text = headingfont.render("STAGE CLEAR!", True , color_dark)
            button.imgdisp = 0
            
            if self.posx < 720:
                  self.posx += 10
                  displaysurface.blit(self.text, (self.posx, self.posy))
            else:
                  self.clear = False
                  self.posx = -100
                  self.posy = 100
                  
     
#显示角色状态
class StatusBar(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.surf = pygame.Surface((120, 96))
            self.rect = self.surf.get_rect(center = (480, 10))
            self.exp = player.experiance
            self.current_world = ""
            self.worlds = ("Home","Twilight","Skyward","Hell")
            
      def update_draw(self):
            
            self.current_world = self.worlds[handler.world]

            # Create the text to be displayed
            text0 = smallerfont.render("WORLD: "+ self.current_world, True, color_white)
            text1 = smallerfont.render("STAGE: " + str(handler.stage) , True , color_white)
            text2 = smallerfont.render("EXP: " + str(player.experiance) , True , color_white)
            text3 = smallerfont.render("MANA: " + str(player.mana) , True , color_white)
            text4 = smallerfont.render("MONEY: " + str(handler.money) , True , color_white)
            text5 = smallerfont.render("FPS: " + str(int(FPS_CLOCK.get_fps())) , True , color_white)
            self.exp = player.experiance

            # Draw the text to the status bar
            displaysurface.blit(text0, (575, 7))
            displaysurface.blit(text1, (575, 22))
            displaysurface.blit(text2, (575, 37))
            displaysurface.blit(text3, (575, 52))
            displaysurface.blit(text4, (575, 67))
            displaysurface.blit(text5, (575, 82))

class Cursor(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("Images/Items/cursor.png")
            self.rect = self.image.get_rect()
            self.wait = 0

      def pause(self):
            if self.wait == 1:
                  self.wait = 0
            else:
                  self.wait = 1

      def hover(self):
          if 620 <= mouse[0] <= 660 and 300 <= mouse[1] <= 345:
                pygame.mouse.set_visible(False)
                cursor.rect.center = pygame.mouse.get_pos()  # update position 
                displaysurface.blit(cursor.image, cursor.rect)
          else:
                pygame.mouse.set_visible(True)
                

class PButton(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.vec = vec(620, 300)
            self.imgdisp = 0

      def render(self, num):
            if (num == 0):
                  self.image = pygame.image.load("Images/Items/home_small.png")
            elif (num == 1):
                  if cursor.wait == 0:
                        self.image = pygame.image.load("Images/Items/pause_small.png")
                  else:
                        self.image = pygame.image.load("Images/Items/play_small.png")
                                    
            displaysurface.blit(self.image, self.vec)
                  
            


Enemies = pygame.sprite.Group()

trader = Trader()
NPCs = pygame.sprite.Group()
NPCs.add(trader)

player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)

background = Background()
button = PButton()
ground = Ground()
cursor = Cursor()
sound = Sound()

ground_group = pygame.sprite.Group()
ground_group.add(ground)

castle = Castle()
handler = EventHandler()
health = HealthBar()
stage_display = StageDisplay()
status_bar = StatusBar()
game_over_bar = GameOverBar()
Fireballs = pygame.sprite.Group()
Items = pygame.sprite.Group()



while True:
    player.gravity_check()
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == EVENT_HIT_COOLDOWN:
            player.cooldown = False
        # Will run when the close window button is clicked    
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == handler.enemy_generation and cursor.wait == 0:
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                  enemy = Enemy()
                  Enemies.add(enemy)
                  handler.enemy_count += 1
        if event.type == player.immune_timer :
              player.immuned = False
              background.image = background.bgimage
              pygame.time.set_timer(player.immune_timer,0)
        if event.type == EVENT_NEXT:
              handler.next = True
              pygame.time.set_timer(EVENT_NEXT,0)
        # For events that occur upon clicking the mouse (left click) 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 620 <= mouse[0] <= 660 and 300 <= mouse[1] <= 350:
                if button.imgdisp == 1:
                    cursor.pause()
                elif button.imgdisp == 0:
                    handler.home()
            if 330 <= mouse[0] <= 370 and 170 <= mouse[1] <= 210:
                if game_over_bar.game_over == True:
                    handler.restart()
                    cursor.wait = 0
                    Playergroup.add(player)
                


        # Event handling for a range of different key presses    
        if event.type == pygame.KEYDOWN and cursor.wait == 0:
            if event.key == pygame.K_n:
                  if handler.battle == True and len(Enemies) == 0 and handler.next == True:
                        handler.next_stage()
                        stage_display = StageDisplay()
                        stage_display.display = True
                        handler.next = False
                        pygame.time.set_timer(EVENT_NEXT,3000)

            if event.key == pygame.K_q and 450 < player.rect.x < 550 and castle.hide == False:
                if handler.world == 0 :
                    handler.stage_handler()
                else:
                    handler.to_world()
            if event.key == pygame.K_q and trader.hit == True:
                trader.buy()
            if event.key == pygame.K_i:
                  player.immune()
            if event.key == pygame.K_w or event.key == pygame.K_k:
                player.jump()
            if event.key == pygame.K_j:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True      


    # Player related functions
    player.update()
    if player.attacking == True:
          player.attack() 
    player.move()                

    # Display and Background related functions         
    background.render()
    ground.render()
    button.render(button.imgdisp)
    cursor.hover()


    # Render stage display
    if stage_display.display == True:
          stage_display.move_display()
    if stage_display.clear == True:
          stage_display.stage_clear()

    

    # Status bar update and render
    displaysurface.blit(status_bar.surf, (570, 5))
    status_bar.update_draw()
    handler.update()

    
    for i in Items:
          i.render()
          i.update() 
   
    for entity in Enemies:
          entity.update()
          entity.move()
          entity.render()
      
    # Rendering Sprite
    castle.update()
    trader.update()
    trader.render()
    if player.health > 0:
        displaysurface.blit(player.image, player.rect)
    else:
        cursor.wait = 1 
        game_over_bar.render()
    health.render()

    pygame.display.update()      
    FPS_CLOCK.tick(FPS)
