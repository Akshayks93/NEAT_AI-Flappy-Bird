"""import all libs- pygame for game physics/ neat for evolving artificial neural networks with a genetic algorithm/   
time module provides many ways of representing time in code, such as objects, numbers, and strings/ OS module in 
python provides functions for creating and removing a directory (folder), fetching its contents, changing and identifying 
the current directory, etc/ Random module is an in-built module of Python which is used to generate random numbers"""

import pygame
import neat 																#neat module helps with the the AI programming Neuro evolution
import time
import os
import random
pygame.font.init()

#set the dimension of the screen
WIN_WIDTH = 550
WIN_HEIGHT = 800

GEN = 0
#ALL CAPITALS are for the variables that will always be constant

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


#scale2x makes the image bigger/load loads image from file.
#we will be programming the base and bg and pipe to be moving while the bird will standing still in essence

#first bird class to have multiple/diff birds each frame nad having them moving around base on their neural networks so we are defining all its characteistics for that object

class Bird:
	IMGS = BIRD_IMGS 														#easier to reference using self.IMGS
	MAX_ROTATION = 25 														#max tilt the bird takes
	ROT_VEL = 20 															#how much we rotate the bird each frame
	ANIMATION_TIME = 5 														#how fast the bird animation is showing and flapping its wings

	def __init__(self,x,y):
		self.x = x 															#starting position of the bird
		self.y = y 															#starting position of the bird
		self.tilt = 0 														#initial tild will be 0 since bird will be straight
		self.tick_count = 0 												#count to for figuring out the physics of the bird when we jump and fall down
		self.vel = 0 														#velocity 0 since its not moving
		self.height = self.y
		self.img_count = 0 													#count to keep track of the img of bird which is currently showing so we cna animate it
		self.img = self.IMGS[0]  											#referncing the first bird image the flat one which os [0] of the BIRD_IMGS

	def jump(self):  														#function whenever we need the
		self.vel = -10.5													#(0,0) coordinate for pygame left top corner so jump up is -ve along Y axis and moving down is +ve, similarly moving right is +ve and left is -ve
		self.tick_count = 0 												#keep track of when we last jumped; reset it to 0 bcz we need to know when its changig directions or velocities for the physics formulas in the game to work
		self.height = self.y 												#track where the point u originally started from 

	def move(self):															#fucntion to call every single frame to move our bird
		self.tick_count += 1 												#1 tick a frame went by, movement happened, keep track of how many times we moved from the last jump 

		#now we need to calculate displacement i.e. how many pixels where moving up or down during this one frame movement. this is what we end up moving when change the Y pos of the bird
		
		d = self.vel*self.tick_count + 1.5*self.tick_count**2

		"""	self.vel*self.tick_count = how much the bird is moving up or down
			self.tick_count = how many seconds the bird was moving for 
			every time the bird keeps moving up or stops moving the tick_count will keep going up up up ie count +1 every time
			based on this tick count we will understand whether the its moving op or if we have reached the top of the jump point 
			and now we are moving down.
			as soon as we jump we reset tick_count to 0, set the height as self.y and velocity as -10.5
			so 
				d = -10.5 * 1 + 1.5 * 1**2
				d = -10.5 + 1.5
				d = -9
			so in this frame we are moving 9 pixels upward, then next frame 7 , 5, 3, 1  upward till we to 0 and the displacement becomes
			+ve to 2, 4 , downward so on this results in an arc going from the jump going up and then going down."""
			
		if d >= 16:
			d = 16 															#so essentially if we are moving down more than 16 according to dispalcement, just move 16 pixels.

		if d < 0:
				d -= 2 														#if we are still moving upwards we can still let it move upwars till it becomes 0

		#now we have to chnage the the Y pos of the bird in according to this displacement

		self.y = self.y + d 												#adding the d calculated in line 53 to Y pos

		#we have to tilt the bird

		if d <0 or self.y < self.height + 50: 								#tilt up condition		
		
			"""d<0 if it is still moving up with ref to the start position/height +50 is still above the ref y point of start, keep the tilt up ward
			when it reaches below the point of Y ref beginning then tilt it downwards"""
		
			if self.tilt < self.MAX_ROTATION: 		
				self.tilt = self.MAX_ROTATION 								#so that the tilt is not over this value and rotate is backwards we immediately set the tilt to 25 as in MAX_ROTATION
		
		else: 																#tilt down
			if self.tilt > -90: 				
				self.tilt -= self.ROT_VEL 									#this help rotate the bird completely 90 deg during jump freefall


	def draw(self, win): 													#win is the window we are drawing the brird 
		self.img_count += 1 												#to animate our bird we need to keep track of how many ticks we have shown for our current image; tick ie. how many times has our main while loop as in out main game loop run and how many time we have shown that one image

		#now to animate the birds wings flapping looped through three images

		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0
		#this in essence make the frames toggle in the images order 1,2,3,2,1 to get the flapping animation

		if self.tilt <= -80:
			self.img = self.IMGS[1] 										#this is to keep the image 1 while free falling to not flap wings
			self.img_count = self.ANIMATION_TIME*2 							#this is so that when it jumps from free fall it doesnt skip a frame by returning to line 100 count 

		rotated_image = pygame.transform.rotate(self.img, self.tilt) 										# how to rotate an object on its in pygame but it will at topleft of x,y axis
		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center) 		#(from stack overflow)move pos of bird from top left to the center of the object
		win.blit(rotated_image,new_rect.topleft)															#drawing the bird image
		

	def get_mask(self):
		return pygame.mask.from_surface(self.img) 							#if any doubts regarding masks check pygame lib documentation for masks

class Pipe:
	GAP = 200 																#gap b/w top and bottom pipes
	VEL = 5																	#since the game in effect the bird is in center and the pipe and BG are moving +ve velocity

	def __init__(self, x):      											#we are using only x and not y bcz the height(y coordinate) will be random
		self.x = x
		self.height = 0

		self.top = 0														#pos for the pipes to be situated in the window
		self.bottom = 0														#pos for the pipes to be situated in the window
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) 		#the Top pipe  is inverted so using flip func in pygame
		self.PIPE_BOTTOM = PIPE_IMG											#original image for the bottom pipes

		self.passed = False													#for collision purposes, checking whether the bird has already passed by the pipe
		self.set_height() 													#his func will define where the base of top n bottom pipes are. how tall is top vs bottom/ where the gap is.

	def set_height(self):
		self.height = random.randrange(50, 450) 							#where we want the heads of the pipes to be 
		self.top = self.height - self.PIPE_TOP.get_height() 				#to find the pos where the base of the top pipe is and the head of top pipe i.e the pipes base is on the top end of the window and to calculate the head of the top pipe(ie inverted bottom pipe) we use the randome height generated and subtract the pipe base pos which we get using the get_height method 
		self.bottom = self.height + self.GAP 								#similar to 
	
	def move(self): 														#move function for the pipe according to the velocity
		self.x -= self.VEL

	def draw(self, win): 													#draw both top and bottom of the pipes at the same place moving along the same coordinate in the x axis
		win.blit(self.PIPE_TOP,(self.x, self.top))
		win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
	
	def collide(self, bird): 												#collide method
		bird_mask = bird.get_mask() 										#get the bird pixels
		top_mask = pygame.mask.from_surface(self.PIPE_TOP) 					#top pipe mpixels
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM) 			#bottom pipe pixels

		#now we need to calculate offset; an offset is how far away these masks are awawy from each other; built in pygame library MASK

		top_offset = (self.x - bird.x, self.top - round(bird.y))
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y)) 		#round funtion to remove decimals
		
		b_point = bird_mask.overlap(bottom_mask, bottom_offset) 			#this tells us the collision between the bird(bird_mask) and bottom pipe(bottom_mask using bottom_offset) by telling us if any overlap of pixels
		t_point = bird_mask.overlap(top_mask, top_offset) 					
		#these both return "None" incase no collision/overlap

		if t_point or b_point:
			return True 													#if any value is returns we can stop the game or pause the game
		
		return False 														#if returns "none" i.e. no collision the bird continues
	

class Base:
	VEL = 5  																#same as pipe velocity bcz otherwise the pipe and base move at different speeds
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH
	
	def move(self): 														#taking two bases images and cycling them one after the other without missing pixels and soona s after its out of the screen it comes back to the rear again 
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))
	
	

def draw_window(win, birds, pipes, base, score, gen): 							#draw window for the game
	
	win.blit(BG_IMG, (0,0)) 												#blit simply means draw BG to the window	 		
	
	for pipe in pipes:
		pipe.draw(win) 														#draw all pipes in window
	
	base.draw(win)										             		#draw base
	for bird in birds:
		bird.draw(win)														#draw the bird on top of the BG image, calls the draw fn and all the animation is taken care of tilting etc
	
	text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255)) 		#score display
	win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))		

	text = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255)) 		#score generation
	win.blit(text, (10, 10))											
	
	pygame.display.update() 												#keeps updating the window and refreshing it

def main(genomes, config): 													#main loop run all the bird running at the same time
	global GEN
	GEN += 1
	nets = []
	ge = []
	birds = []													

	#to chnage the fitness of the birds and find it for bird[0],ge[0]and nets[0]
	for _, g in genomes: 													#genoes is tuple so we iuse underscore
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		birds.append(Bird(230, 350))
		g.fitness = 0
		ge.append(g)

	base = Base(730) 														#base location in the screen
	pipes = [Pipe(600)] 													#pipes as list and starting pos @600
	
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) 					#python creates a window for display
	
	clock = pygame.time.Clock() 											#we set the frame rate to for the game to run so that it dopes not have to take the pc frame rate
	
	score = 0
	
	run = True 																#run = false can be used to stop the game
	
	while run: 																#for running the game 	
		clock.tick(30) 														#30clicks per second 30 fps
		for event in pygame.event.get(): 									#keep track of events like if user clicks on the window
			if event.type == pygame.QUIT: 									#red x on the top right stops the game 
				run = False
				pygame.quit()
				quit()
		
		#bird.move() 														#calling the move funtion for the brid animation
		
		pipe_ind = 0
		if len(birds) > 0:
			if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
				pipe_ind = 1
		else:
			run = False
			break

		for x, bird in enumerate(birds):
			bird.move()
			ge[x].fitness += 0.1

			output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))  #output is a list
			
			if output[0] > 0.5:
				bird.jump()

		add_pipe = False
		rem = [] 															#remove pipes
		
		for pipe in pipes: 													#for more than one pipe
			for x, bird in enumerate(birds): 								#for all 100 bids
				if pipe.collide(bird): 										#if all collide with pipe
					ge[x].fitness -= 1 										#since all birds move and the once that hit pipe should not be in fron and considered fit
					birds.pop(x) 											#the onces that hit the pipes are rmove from the genome list
					nets.pop(x)
					ge.pop(x)

				if not pipe.passed and pipe.x < bird.x: 					#check if the bird has passed the pipe, as soon as the bird pass the pipe generate a new pipe section
					pipe.passed = True
					add_pipe = True
			
			if pipe.x + pipe.PIPE_TOP.get_width() < 0: 						#this means pipe completely of the screen
				rem.append(pipe) 											#remove the pipe and put it in the remove list

			pipe.move() 													#moving the pipe in opp direction by calling function
		
		if add_pipe: 														#addingt next pipes
			score += 1 														#keep count of the number of pipes passed
			for g in ge:
				g.fitness += 5
			pipes.append(Pipe(600))

		for r in rem: 														#remove pipes that went of screen
			pipes.remove(r)  												

		for x, bird in enumerate(birds):
			if bird.y + bird.img.get_height() >= 730 or bird.y < 0:		#to notify that we hit the floor if each of out birds hits the ground
				birds.pop(x) 											#the onces that hit the pipes are rmove from the genome list
				nets.pop(x)
				ge.pop(x)

		base.move() 														#base movement
		draw_window(win, birds, pipes, base, score, GEN) 							#draws all the things we have called to the pygame window

	


def run(config_path):

	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	#we are caaling all the sub heading in the neat configuration file 

	p = neat.Population(config) 											#generate a population

	p.add_reporter(neat.StdOutReporter(True)) 								#detailed stats about the population and the best fitness
	stats = neat.StatisticsReporter() 										#gives us the out put in numbers
	p.add_reporter(stats)

	winner = p.run(main, 50) 													#set fitness(distance travelled in this game) function that will run 50 generations 

if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	run(config_path)