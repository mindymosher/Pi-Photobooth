import time
import picamera
import pygame
import os
import glob

real_path = os.path.dirname(os.path.realpath(__file__))

#####  break out pygame.init into it's own thing
#####  and fix it so that every method doesn't reinit 

def init_pygame():
	pygame.init()
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	pygame.display.set_caption('Photo Booth!')
	pygame.mouse.set_visible(False)
	newScreen = pygame.display.set_mode(size, pygame.FULLSCREEN)
	background = pygame.Surface(newScreen.get_size())
	background = background.convert()
	background.fill((255, 255, 255))
	newScreen.blit(background, (0, 0))
	return newScreen

def show_image(image_path):
	screen = init_pygame()
	img=pygame.image.load(image_path)
	screen.blit(img,((screen.get_rect().centerx - (img.get_rect().centerx)), (screen.get_rect().centery - (img.get_rect().centery))))
	pygame.display.flip()

def show_all_images(current_time):
	screen = init_pygame()
	font = pygame.font.Font(None, 100)
	text = font.render("Processing photos!", 1, (0,0,0))
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery
	screen.blit(text, textpos)

	pygame.display.flip()
	
	images = glob.glob('photoBooth/image_' + str(current_time) + '*.jpg')

	for i in range(0, 4):
		images[i] = pygame.image.load(images[i]).convert()
		images[i] = pygame.transform.scale(images[i], (640, 480))
		
	screen = init_pygame()
	screen.blit(images[0], (5, 5))
	screen.blit(images[1], (650, 5))
	screen.blit(images[2], (5, 490))
	screen.blit(images[3], (650, 490))
	pygame.display.flip()
	pygame.image.save(screen, "photoBooth/contact_" + str(current_time) + ".jpg")
	time.sleep(7)


def intro():
	screen = init_pygame()
	font = pygame.font.Font(None, 100)
	text = font.render("Welcome to the Photo Booth!", 1, (0,0,0))
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery
	screen.blit(text, textpos)

	pygame.display.flip()
	time.sleep(5)

def countdown():
	screen = init_pygame()
	font = pygame.font.Font(None,600)
	for i in range(3, 0, -1):
		text = font.render(str(i), 1, (0,0,0), (255, 255, 255))
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx
		textpos.centery = screen.get_rect().centery
		screen.blit(text, textpos)
		pygame.display.flip()
		time.sleep(1)

def print_photo(filename):
	os.system("lp " + filename)

def toggle_fullscreen():
	pygame.event.pump()
	for e in pygame.event.get():
		if e.type == pygame.KEYDOWN:
			print e.key
		if (e.type == pygame.KEYDOWN and e.key==pygame.K_ESCAPE):
			quit()
		if (e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN):
			if booth.get_flags() & pygame.FULLSCREEN:
				pygame.display.set_mode(size)
			else:
				pygame.display.set_mode(size, pygame.FULLSCREEN)


def photobooth(): 
	current_time = time.time()
	################# Countdown #######################
	show_image(real_path + "/blank.png")
	intro()
	print "Get Ready"
	camera = picamera.PiCamera()
	camera.vflip = True
	camera.hflip = False

	countdown()
	show_image(real_path + "/blank.png")
	camera.start_preview()
	time.sleep(3)

	############### Take pics ##########################
	try:
		print "Taking Photos"
		for i, filename in enumerate(camera.capture_continuous('photoBooth/image_' + str(current_time) + '_{counter:02d}.jpg')):
			print(filename)
			if i==3:
				break
			time.sleep(2)
			
	finally: 
		camera.stop_preview()

	############## Show pics ##########################

	show_all_images(current_time)

booth = init_pygame()
clock = pygame.time.Clock()
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
while True:
	images = glob.glob("photoBooth/image*.jpg")
	for image in images:
		show_image(image)
		toggle_fullscreen()	
		clock.tick()
		pygame.time.delay(3000)	

# photobooth()