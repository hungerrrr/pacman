import pygame
import random


black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow   = ( 255, 255,   0)
screen_width = 606
screen_height = 606


#墙壁
class Wall(pygame.sprite.Sprite):
    # 构造函数
    def __init__(self,x,y,width,height, color):
        # 先构造父类
        pygame.sprite.Sprite.__init__(self)
  
        # 制作颜色为color的墙
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # 将坐标传入top和left
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


# 豆子
class Block(pygame.sprite.Sprite):
     
     
    def __init__(self, color, width, height):
        # call父类构造
        pygame.sprite.Sprite.__init__(self) 
 
        # 制作豆子
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])

        self.rect = self.image.get_rect() 

#吃豆人
class Pacman(pygame.sprite.Sprite):
    #xy方向上变量
    dx = 0 
    dy = 0
    #速度
    speed = 15
    angle = 90 #实时图片朝向
    angle_base = 90 #基准朝向
    directions = {"left": (-speed, 0), "right": (speed, 0), "up": (0, -speed), "down": (0, speed)}

    #构造
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("pacman.png").convert()

        self.rect = self.image.get_rect()

        self.rect.top = y
        self.rect.left = x
        
    #设置吃豆人坐标
    def setxy(self, walls, gate):
        #记录原坐标
        old_x = self.rect.left
        old_y = self.rect.top
        #更新坐标
        self.rect.left += self.dx
        self.rect.top += self.dy


        #碰撞
        collide = pygame.sprite.spritecollide(self, walls, False)
        if collide:
            self.rect.top = old_y
            self.rect.left = old_x

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y

    #更新吃豆人的方向
    def update(self, walls):

        # 处理按键事件
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman_direction = "left"
            #翻转图像
            self.image = pygame.transform.rotate(self.image, self.angle - self.angle_base - 180)
            self.angle = 270
            Pacman.dx, Pacman.dy = Pacman.directions[pacman_direction]
        elif keys[pygame.K_RIGHT]:
            pacman_direction = "right"
            self.image = pygame.transform.rotate(self.image, self.angle - self.angle_base - 0)
            self.angle = 90
            Pacman.dx, Pacman.dy = Pacman.directions[pacman_direction]
        elif keys[pygame.K_UP]:
            pacman_direction = "up"
            self.image = pygame.transform.rotate(self.image, self.angle - self.angle_base + 90)
            self.angle = 0
            Pacman.dx, Pacman.dy = Pacman.directions[pacman_direction]
        elif keys[pygame.K_DOWN]:
            pacman_direction = "down"
            self.image = pygame.transform.rotate(self.image, self.angle - self.angle_base - 90)
            self.angle = 180
            Pacman.dx, Pacman.dy = Pacman.directions[pacman_direction]



#鬼
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__()
  
        self.image = pygame.image.load(filename).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = "left" # 初始移动方向为左侧
        self.speed = 10 # 移动速度为 10 像素/帧

    def update(self, walls):
        # 计算 ghost 应该朝向哪个方向移动
        if random.random() < 0.1: # 有 10% 的概率随机改变方向
            self.direction = random.choice(["left", "right", "up", "down"])

        # 在当前方向上移动 ghost
        old_position = self.rect.copy() # 存储移动前的位置，用于后面的碰撞检测
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # 检测 Ghost 是否与墙壁重叠，并进行修正
        ghostcollide = pygame.sprite.spritecollide(self, walls, False)
        if ghostcollide:
            for wall in walls:
                # 如果 Ghost 与墙壁重叠，则尝试在其他方向上移动
                if self.direction == "left":
                    self.rect.left = old_position.left
                    if self.rect.colliderect(wall.rect): # 如果仍然与墙壁重叠，则改变方向
                        self.direction = random.choice(["up", "down", "right"])
                elif self.direction == "right":
                    self.rect.right = old_position.right
                    if self.rect.colliderect(wall.rect):
                        self.direction = random.choice(["up", "down", "left"])
                elif self.direction == "up":
                    self.rect.top = old_position.top
                    if self.rect.colliderect(wall.rect):
                        self.direction = random.choice(["left", "right", "down"])
                elif self.direction == "down":
                    self.rect.bottom = old_position.bottom
                    if self.rect.colliderect(wall.rect):
                        self.direction = random.choice(["left", "right", "up"])
               



# 生成地图函数
def setupRoomOne(all_sprites_list):
    # 创建墙壁list (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.RenderPlain()
     
    # 所有墙壁的坐标以及宽高 [x, y, width, height]
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,300,126,6],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]
     
    # 循环创建墙壁并加入list
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],green)
        wall_list.add(wall)
        all_sprites_list.add(wall)
         
    return wall_list


#创建大门
def setupGate(all_sprites_list):
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282,242,42,2,white))
      all_sprites_list.add(gate)
      return gate


#初始化pygame
pygame.init()
  
# 创建窗口
screen = pygame.display.set_mode([606, 606])

#设置标题
pygame.display.set_caption('Pacman')

# 设置背景
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

#设置帧
clock = pygame.time.Clock()

#字体
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)


#设置鬼的初始位置
w = 303-16 
m_h = (4*60)+19 #Monster
b_h = (3*60)+19 #Binky
i_w = 303-16-32 #Inky
c_w = 303+(32-16) #Clyde


#添加音乐
pygame.mixer.init()
pygame.mixer.music.load('music\Ken Ishii - JOIN THE PAC (Original Mix - Official Theme Song for PAC-MAN 40th Anniversary).flac')
pygame.mixer.music.play(-1, 0.0)

def startGame():

    all_sprites_list = pygame.sprite.RenderPlain()

    block_list = pygame.sprite.RenderPlain()

    monsta_list = pygame.sprite.RenderPlain()

    pacman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)

    gate = setupGate(all_sprites_list)

    #初始化pacman，设置位置
    pacman = Pacman(303, 317)

    all_sprites_list.add(pacman)

    pacman_collide.add(pacman)

  # 创建鬼
    Blinky=Ghost( w, b_h, "images/Blinky.png" )
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky=Ghost( w, m_h, "images/Pinky.png" )
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)
    
    Inky=Ghost( i_w, m_h, "images/Inky.png" )
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)
   
    Clyde=Ghost( c_w, m_h, "images/Clyde.png" )
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

  # 绘制
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block(blue, 4, 4)

                # 设置豆子的位置
                block.rect.x = (30*column+6)+26
                block.rect.y = (30*row+6)+26

                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    block_list.add(block)
                    all_sprites_list.add(block)

    block_list_length = len(block_list)

    #得分
    score = 0

    done = False

    while done == False:
        #程序循环执行
        #设置pacman位置
        pacman.setxy(wall_list, gate)

        #处理键盘事件
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pacman.update(wall_list)

        #更新怪物  
        Pinky.update(wall_list)
        Blinky.update(wall_list)
        Inky.update(wall_list)
        Clyde.update(wall_list)
        

        # 吃到的豆子
        blocks_hit_list = pygame.sprite.spritecollide(pacman, block_list, True)
        
        # 计入得分
        if len(blocks_hit_list) > 0:
            score +=len(blocks_hit_list)    
    
        #绘图
        screen.fill(black)
        
        wall_list.draw(screen)

        gate.draw(screen)
        
        all_sprites_list.draw(screen)
        
        monsta_list.draw(screen)

        text=font.render("Score: "+str(score)+"/"+str(block_list_length), True, red)
        screen.blit(text, [10, 10])

        #作弊码
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_1]:
                    doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)
        #吃完所有豆子
        if score == block_list_length:
            doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)


        #被鬼抓住
        monsta_hit_list = pygame.sprite.spritecollide(pacman, monsta_list, False)
        if monsta_hit_list:
            doNext("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

        pygame.display.flip()
        
        clock.tick(20)#帧率

#游戏结束后操作
def doNext(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
    while True:
        #如果esc就退出，enter进行下一把
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del monsta_list
                    del pacman_collide
                    del wall_list
                    del gate
                    startGame()

        #提示界面
        w = pygame.Surface((400,200))  
        w.set_alpha(10)                # 设置alpha值
        w.fill((128,128,128))           
        screen.blit(w, (100,200))    

        #输赢词条
        text1=font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2=font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3=font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(60)

startGame()

pygame.quit()
