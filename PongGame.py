import pygame
pygame.init()

#--referencing
#Tech With Tim (2022) Make pong with python!, YouTube. 
# Available at: https://www.youtube.com/watch?v=vVGTZlnnX3U (Accessed: 30 July 2023). 
#--

#declaring variables for display
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #constant with tuple
#title of game to be displayed
pygame.display.set_caption("Pong")

#frames per second
FPS = 60

#declaring colours as variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

#ball radius
BALL_RADIUS = 7

#getting font to display score
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

#setting a winning score
WON = 5

#specifying paddle measurements
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

#class to create the paddle objects
class Paddle:
    #colour for paddles
    COLOUR = GREEN
    #velocity of the paddles when moving
    VEL = 4

    def __init__(self, x, y, width, height):
        #properties of each paddle
        self.x = self.originalX = x
        self.y = self.originalY = y
        self.width = width
        self.height = height
    
    #parameters to draw the paddles
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.COLOUR, (self.x, self.y, self.width, self.height))

    #paddle movement
    def move(self, up=True):

        if up:
            #moving paddle up
            self.y -= self.VEL
        else:
            #moving paddle down
            self.y += self.VEL
    
    #reseting paddle position
    def reset(self):
        self.x = self.originalX
        self.y = self.originalY


#class to create the ball
class Ball:
    #maximum velocity
    MAX_VEL = 5
    COLOUR = WHITE

    def __init__(self, x, y, radius):
        #properties of the ball
        self.x = self.originalX = x
        self.y = self.originalY = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    #parameters to draw ball
    def draw(self, WIN):
        pygame.draw.circle(WIN, self.COLOUR, (self.x, self.y), self.radius)
    
    #moving ball
    def moveBall(self):
        self.x += self.x_vel
        self.y += self.y_vel

    #reseting ball position
    def reset(self):
        self.x = self.originalX
        self.y = self.originalY
        self.y_vel = 0
        self.x_vel *= -1
    

#function to draw elements
def draw(WIN, paddles, ball, left_score, right_score):
    #colour of the window
    WIN.fill(BLACK)

    #adding text for score
    left_score_text = SCORE_FONT.render(f"{left_score}", 1 , WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1 , WHITE)
    #positioning scores
    WIN.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    WIN.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    #loop to draw
    for paddle in paddles:
        paddle.draw(WIN)

    #loop to draw a dotted line
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1: #if i is an even number
            continue #not drawing (skipping one spot)
        pygame.draw.rect(WIN, GREEN, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    #displaying ball
    ball.draw(WIN)

    #updating display to match specifications
    pygame.display.update()

#collision function
def handle_collision(ball, left_paddle, right_paddle):
    #collision with top and bottom edges
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    #collision with left paddle
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                diff_in_y = middle_y - ball.y
                reduction = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = diff_in_y / reduction
                ball.y_vel = -1 * y_vel

    #collision with left paddle
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                diff_in_y = middle_y - ball.y
                reduction = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = diff_in_y / reduction
                ball.y_vel =  -1 * y_vel
         

#moving paddles based on keys, not allowing to move off screen
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


#main function
def main():
    run = True

    #clock to regulate the framerate of the game
    clock = pygame.time.Clock()

    #creating left paddle
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    #creating right paddle
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    #creating ball
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    #scores
    left_score = 0
    right_score = 0

    while run:
        #regulating frames with fps
        clock.tick(FPS)

        #calling draw function
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        #loop for events within the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #if user clicks the exit button
                run = False
                break

        #getting keys that user pressed
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        #moving ball
        ball.moveBall()

        #handling collision
        handle_collision(ball, left_paddle, right_paddle)

        #handling score
        if ball.x < 0:
            right_score += 1
            ball.reset() #reseting ball

        elif ball.x > WIDTH:
            left_score += 1
            ball.reset() #reseting ball
        
        #checking who won
        over = False
        if left_score >= WON:
            over = True
            end_text = "Left Player Won!"

        elif right_score >= WON:
            over = True
            end_text = "Right Player Won!"
        
        if over:
            #displaying who won and resetting
            text = SCORE_FONT.render(end_text, 1, WHITE)

            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            
            pygame.display.update()
            pygame.time.delay(5000) #time before restarting
            
            ball.reset()
            right_paddle.reset()
            left_paddle.reset()
            left_score = 0
            right_score = 0


    #quitting program
    pygame.quit()

#running only from this file not if imported from elsewhere
if __name__ == '__main__':
    main()