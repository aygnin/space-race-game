from setup import *

class Asteroid:

    width, height = 8, 8
    speed = 0.3
    min_possible_height = SCREEN_HEIGHT / 5

    colour = (255, 255, 255)

    def __init__(self):
        self.is_on_screen = True
        self.velocity = pygame.Vector2(random.choice((-1, 1)) * self.speed, 0)
        self.position = pygame.Vector2(0, random.random() * (SCREEN_HEIGHT - self.min_possible_height))

        if self.velocity.x < 0:
            self.position.x = SCREEN_WIDTH + self.width / 2
        else:
            self.position.x = -self.width / 2
            
    def update(self, delta_time):
        self.position += self.velocity * delta_time
        if self.position.x > SCREEN_WIDTH + self.width / 2 or self.position.x < -self.width / 2:
            self.is_on_screen = False

    def draw(self, screen):
        r = pygame.Rect(
            self.position.x - self.width/2,
            self.position.y - self.height/2,
            self.width,
            self.height)
        pygame.draw.rect(screen, self.colour, r)

class Player:

    width, height = 75, 75
    speed = 0.3

    def __init__(self, position_x, position_y, file_name):
        self.position = pygame.Vector2(position_x, position_y)
        self.texture = pygame.transform.scale(pygame.image.load(file_name), (self.width, self.height))
        self.score = 0
        self.penalty_cooldown = 0
        
    def move_forward(self, delta_time):
        if self.penalty_cooldown == 0:
            self.position.y -= self.speed * delta_time

    def move_backward(self, delta_time):
        if self.penalty_cooldown == 0:
            if self.position.y < SCREEN_HEIGHT - self.height/2:
                self.position.y += self.speed * delta_time

    def is_colliding(self, asteroids):
        player_left = self.position.x - self.width / 2
        player_right = self.position.x + self.width / 2
        player_top = self.position.y - self.height / 2
        player_bottom = self.position.y + self.height / 2

        for asteroid in asteroids:
            asteroid_left = asteroid.position.x - asteroid.width / 2
            asteroid_right = asteroid.position.x + asteroid.width / 2
            asteroid_top = asteroid.position.y - asteroid.width / 2
            asteroid_bottom = asteroid.position.y + asteroid.width / 2

            if ((player_left < asteroid_right) and
                    (player_right > asteroid_left) and
                    (player_top < asteroid_bottom) and
                    (player_bottom > asteroid_top)):
                return True

        return False

    def update(self, delta_time):
        if self.position.y < -self.height/2:
            self.position.y = SCREEN_HEIGHT + self.height/2
            self.score += 1
        self.penalty_cooldown = max(self.penalty_cooldown - delta_time, 0) 

    def draw(self, screen):
        if self.penalty_cooldown // 200 % 2 == 0:
            top_left = (self.position.x - self.width/2, self.position.y - self.width/2)
            screen.blit(self.texture, top_left)

class Splash:
    
    title_text = "SPACE RACE"
    instruction_text = "PRESS SPACE TO PLAY"
    
    def update(self, delta_time):
         pressed = pygame.key.get_pressed()

         if pressed[pygame.K_SPACE]:
            SOUND_SELECT.play()
            return 0

    def draw(self, screen):
        
        text_surface = TITLE_FONT.render(self.title_text, True, (255, 255, 255))
        top_left = (SCREEN_WIDTH/2 - text_surface.get_width()/2, SCREEN_HEIGHT * 0.25 - text_surface.get_height()/2)
        screen.blit(text_surface, top_left)

        if pygame.time.get_ticks() // 500 % 2 == 0:
            text_surface = SMALL_FONT.render(self.instruction_text, True, (255, 255, 255))
            top_left = (SCREEN_WIDTH/2 - text_surface.get_width()/2, SCREEN_HEIGHT / 2 - text_surface.get_height()/2)
            screen.blit(text_surface, top_left)


class GameOver():

    duration = 4000

    def __init__(self, status):
        self.text = None
        if status == 0:
            self.text = "TIE"
        elif status == 1:
            self.text = "PLAYER ONE WINS!"
        elif status == 2:
            self.text = "PLAYER TWO WINS"
        self.current_time = 0

    def update(self, delta_time):
        if self.current_time > self.duration:
            return 0
        self.current_time += delta_time

    def draw(self, screen):
        text_surface = SMALL_FONT.render(self.text, True, (255, 255, 255))
        top_left = (SCREEN_WIDTH/2 - text_surface.get_width()/2, SCREEN_HEIGHT/2 - text_surface.get_height()/2)
        screen.blit(text_surface, top_left)

class SpaceRace:

    game_duration = 60000
    asteroid_population = 15
    player_start_height = SCREEN_HEIGHT -75
    player_collision_penalty = 1500

    def __init__(self):
        self.asteroids = []
        self.player_one = Player(SCREEN_WIDTH * 0.25, self.player_start_height, "ship.png")
        self.player_two = Player(SCREEN_WIDTH * 0.75, self.player_start_height, "ship.png")
        self.current_time = 0
        for _ in range(self.asteroid_population):
            a=Asteroid()
            a.position.x = random.random() * SCREEN_WIDTH
            self.asteroids.append(a)

    def update(self, delta_time):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_w]:
            self.player_one.move_forward(delta_time)
        if pressed[pygame.K_s]:
            self.player_one.move_backward(delta_time)
        if pressed[pygame.K_UP]:
            self.player_two.move_forward(delta_time)
        if pressed[pygame.K_DOWN]:
            self.player_two.move_backward(delta_time)

        self.player_one.update(delta_time)
        self.player_two.update(delta_time)

        if self.player_one.is_colliding(self.asteroids):
            self.player_one.position.y = self.player_start_height
            self.player_one.penalty_cooldown = self.player_collision_penalty
            SOUND_EXPLOSION.play()

        if self.player_two.is_colliding(self.asteroids):
            self.player_two.position.y = self.player_start_height
            self.player_two.penalty_cooldown = self.player_collision_penalty
            SOUND_EXPLOSION.play()
            
        for asteroid in self.asteroids:
            asteroid.update(delta_time)
            if not asteroid.is_on_screen:
                self.asteroids.remove(asteroid)
                self.asteroids.append(Asteroid())

        if self.current_time > self.game_duration:

            if self.player_one.score > self.player_two.score:
                return 1
            elif self.player_one.score < self.player_two.score:
                return 2
            elif self.player_one.score == self.player_two.score:
                return 0

        self.current_time += delta_time
        
    def draw(self, screen):
        self.player_one.draw(screen)
        self.player_two.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

        self.draw_score(screen, self.player_one, SCREEN_WIDTH * 0.25, 75, DEFAULT_FONT)
        self.draw_score(screen, self.player_two, SCREEN_WIDTH * 0.75, 75, DEFAULT_FONT)

        self.draw_timer(screen, SCREEN_WIDTH / 2, 75, SMALL_FONT)

    def draw_score(self, screen, player, position_x, position_y, font):
        text_surface = font.render(str(player.score), True, (255, 255, 255))
        top_left = (position_x - text_surface.get_width()/2, position_y - text_surface.get_height()/2)
        screen.blit(text_surface, top_left)

    def draw_timer(self, screen, position_x, position_y, font):
        time_text = str((self.game_duration - self.current_time)//1000+1)
        text_surface = font.render(time_text, True, (255, 255, 255))
        top_left = (position_x - text_surface.get_width()/2, position_y - text_surface.get_height()/2)
        screen.blit(text_surface, top_left)
