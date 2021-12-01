import pygame
from random import randint

# game config
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 25
FPS = 15

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI snek")


class Direction:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Food:
    COLOR = (170, 0, 0)
    SIZE = (TILE_SIZE, TILE_SIZE)

    def genereteRandomPosition(self):
        return Position(TILE_SIZE*randint(0, int(SCREEN_WIDTH/TILE_SIZE)-1), TILE_SIZE*randint(0, int(SCREEN_HEIGHT/TILE_SIZE)-1))

    def __init__(self):
        self.position = self.genereteRandomPosition()

    def draw(self):
        food_rect = pygame.Rect(
            (self.position.x,
             self.position.y),
            self.SIZE)
        pygame.draw.rect(WINDOW, self.COLOR, food_rect)

    def changePosition(self):
        self.position = self.genereteRandomPosition()


class Snake:
    COLOR = (0, 150, 0)
    DIRECTION = Direction.RIGHT
    CHANGE_DIRECTION_TO = DIRECTION
    HAD_EATEN = False

    def __init__(self):
        self.body = [Position(SCREEN_WIDTH/2, SCREEN_HEIGHT/2),
                     Position(SCREEN_WIDTH/2-TILE_SIZE, SCREEN_HEIGHT/2),
                     Position(SCREEN_WIDTH/2-2*TILE_SIZE, SCREEN_HEIGHT/2)]

    def draw(self):
        for bodyPart in self.body:
            bodyPartRect = pygame.Rect(
                (bodyPart.x, bodyPart.y), (TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(WINDOW, self.COLOR, bodyPartRect)

    def move(self):
        new_body = self.body[:] if self.HAD_EATEN else self.body[:-1]
        if self.DIRECTION == Direction.RIGHT:
            new_body.insert(0, Position(
                self.body[0].x+TILE_SIZE, self.body[0].y))
            self.body = new_body
        elif self.DIRECTION == Direction.LEFT:
            new_body.insert(0, Position(
                self.body[0].x-TILE_SIZE, self.body[0].y))
            self.body = new_body
        elif self.DIRECTION == Direction.UP:
            new_body.insert(0, Position(
                self.body[0].x, self.body[0].y-TILE_SIZE))
            self.body = new_body
        elif self.DIRECTION == Direction.DOWN:
            new_body.insert(0, Position(
                self.body[0].x, self.body[0].y+TILE_SIZE))
            self.body = new_body

    def updateDirection(self):
        if self.CHANGE_DIRECTION_TO == Direction.UP and self.DIRECTION != Direction.DOWN:
            self.DIRECTION = Direction.UP
        elif self.CHANGE_DIRECTION_TO == Direction.DOWN and self.DIRECTION != Direction.UP:
            self.DIRECTION = Direction.DOWN
        elif self.CHANGE_DIRECTION_TO == Direction.LEFT and self.DIRECTION != Direction.RIGHT:
            self.DIRECTION = Direction.LEFT
        elif self.CHANGE_DIRECTION_TO == Direction.RIGHT and self.DIRECTION != Direction.LEFT:
            self.DIRECTION = Direction.RIGHT


class Game:
    def __init__(self):
        self.SNAKE = Snake()
        self.FOOD = Food()
        self.GAME_OVER = False
        self.SCORE = 0

    def draw_board(self):
        # COLOR1 = (65, 65, 65)
        # COLOR2 = (70, 70, 70)
        # for i in range(int(SCREEN_WIDTH/TILE_SIZE)):
        #     for j in range(int(SCREEN_HEIGHT/TILE_SIZE)):
        #         tile = pygame.Rect((i*TILE_SIZE, j*TILE_SIZE),
        #                            (TILE_SIZE, TILE_SIZE))
        #         pygame.draw.rect(WINDOW, COLOR1 if (i+j) %
        #                          2 == 0 else COLOR2, tile)
        WINDOW.fill((0, 0, 0))

    def checkColision(self):
        if self.SNAKE.body[0].x >= SCREEN_WIDTH or self.SNAKE.body[0].x < 0 or self.SNAKE.body[0].y >= SCREEN_HEIGHT or self.SNAKE.body[0].y < 0:  # wall coliision
            self.GAME_OVER = True
        elif self.SNAKE.body[0] in self.SNAKE.body[1:]:  # hit itself
            self.GAME_OVER = True

    def render(self):
        self.draw_board()
        self.FOOD.draw()
        self.SNAKE.updateDirection()
        self.SNAKE.move()
        self.SNAKE.draw()
        self.drawScore()

    def drawEndScreen(self):
        WINDOW.fill((0, 0, 0))
        font = pygame.font.SysFont("times new roman", 100)
        text = font.render("YOU DIED", True, (255, 0, 0))
        WINDOW.blit(text, (SCREEN_WIDTH/2-text.get_width()/2, SCREEN_HEIGHT/3))

        font = pygame.font.SysFont("times new roman", 30)
        text = font.render(f"Score: {self.SCORE}", True, (255, 0, 0))
        WINDOW.blit(text, (SCREEN_WIDTH/2-text.get_width() /
                    2, SCREEN_HEIGHT/2-text.get_height()/3+50))

        font = pygame.font.SysFont("times new roman", 30)
        text = font.render(
            "Press R to restart     Press Q to quit", True, (255, 255, 0))
        WINDOW.blit(text, (SCREEN_WIDTH/2-text.get_width() /
                    2, SCREEN_HEIGHT/2-text.get_height()/3+100))

    def checkIfAte(self):
        if self.SNAKE.body[0] == self.FOOD.position:
            self.SNAKE.HAD_EATEN = True
            self.FOOD.changePosition()
            self.SCORE += 10
        else:
            self.SNAKE.HAD_EATEN = False

    def drawScore(self):
        pygame.font.init()
        font = pygame.font.SysFont("comicsansms", 16)
        text = font.render(f"Score: {self.SCORE}", True, (255, 255, 255))
        WINDOW.blit(text, (10, 10))

    def restart(self):
        self.SNAKE = Snake()
        self.FOOD = Food()
        self.GAME_OVER = False
        self.SCORE = 0


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.SNAKE.CHANGE_DIRECTION_TO = Direction.UP
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.SNAKE.CHANGE_DIRECTION_TO = Direction.DOWN
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.SNAKE.CHANGE_DIRECTION_TO = Direction.LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.SNAKE.CHANGE_DIRECTION_TO = Direction.RIGHT
                elif event.key == pygame.K_q and game.GAME_OVER:
                    run = False
                elif event.key == pygame.K_r and game.GAME_OVER:
                    game.restart()

        if game.GAME_OVER:
            game.drawEndScreen()
        else:
            game.render()

        game.checkColision()
        game.checkIfAte()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
