import pygame, os, random

pygame.init()

# Variables
gameWidth = 840
gameHeight = 640
picSize = 128
gameCol = 5
gameRow = 4
padding = 10
leftMargin = (gameWidth - ((picSize + padding) * gameCol)) // 2
rightMargin = leftMargin  # =75
topMargin = (gameHeight - ((picSize + padding) * gameRow)) // 2
bottomMargin = topMargin  # =44
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
selection1 = None  # Slected Image. Can't be 0 as 0 indicates index in python
selection2 = None

"""SCREEN"""
screen = pygame.display.set_mode((gameWidth, gameHeight))  # width & height
pygame.display.set_caption("Memory Game")  # Heading on Top
gameIcon = pygame.image.load("Images/Apple.png")  # Loads Icon beside heading
pygame.display.set_icon(gameIcon)  # Sets Icon


""" background """
bgImage = pygame.image.load("Background.png")
bgImage = pygame.transform.scale(
    bgImage, (gameWidth, gameHeight)
)  # Change resolution to fit the game window
bgImageRect = bgImage.get_rect()  # get rect value


""" List of Pictures for the Game """
Pictures = []

for item in os.listdir("Images/"):
    # appends Apple instead of Apple.png
    Pictures.append(item.split(".")[0])

PicturesCopy = Pictures.copy()  # 2 pics of each item req for the game
# Add copied images to the list
# Doesn't append existing list thereby creating a nested List.
# eg: [Apple, ApplePie, Chicken,...,Steak, Straberry, Apple, ApplePie, Chicken,..,Steak, Straberry]
#  Instead of
#   [Apple, ApplePie, Chicken,....,Steak, Straberry, [Apple, ApplePie, Chicken,...,Steak, Straberry]]
Pictures.extend(PicturesCopy)
PicturesCopy.clear()  # Clearing the loaded images copy after extending
random.shuffle(Pictures)  # Randomizes Images


""" Loding PICTURES in Python memory"""

memPic = []
memPicRect = []
hiddenImages = []

for item in Pictures:
    Pic = pygame.image.load(f"Images/{item}.png")
    Pic = pygame.transform.scale(Pic, (picSize, picSize))
    memPic.append(Pic)
    PicRect = Pic.get_rect()
    memPicRect.append(PicRect)

"""
Setting correct co-ordinates for Images in the window
Default co-ordinates look like this: <rect(0, 0, 128, 128)> (for Fish diregarding copy & randomiztion)
128 is the picSize. Co-ordinates are (0,0)
We have to fetch x co-ordiante. selecting each number in <rect(351, 0, 128, 128)>. So that pictures (for x coordinate)
start from left margin
"""

for i in range(len(memPicRect)):
    # = 75 + ((128 + 10) * (i % 5))
    memPicRect[i][0] = leftMargin + ((picSize + padding) * (i % gameCol))
    # now it looks like <rect(75, 0, 128, 128)> <rect(213, 0, 128, 128)>, <rect(351, 0, 128, 128)>, <rect(489, 0, 128, 128)>, <rect(627, 0, 128, 128)>
    # & then starting again at left margin <rect(75, 0, 128, 128)>, <rect(213, 0, 128, 128)>....
    memPicRect[i][1] = topMargin + ((picSize + padding) * (i % gameRow))
    # <rect(75, 44, 128, 128)>, <rect(213, 182, 128, 128)>
    hiddenImages.append(False)  # False is tag to hide image

# Game Loop
gameLoop = True

while gameLoop:
    # Load Background Image in window replacing black screen
    screen.blit(bgImage, bgImageRect)

    # Input Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False

        # event.pos gives position of triggered event on screen. Here
        # mouseclick. Only trigger if clicked on item in image box, which
        # will be an item with position coordinates from memPicsRect
        # index func converts rect coordinates into
        # simple consective numbers 1-20 for 20 images

        # Selecting Images
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in memPicRect:
                if item.collidepoint(event.pos):
                    if hiddenImages[memPicRect.index(item)] != True:
                        # if a image has been selected already
                        if selection1 != None:
                            selection2 = memPicRect.index(item)
                            # Reveal image on click
                            hiddenImages[selection2] = True
                        else:
                            # Select first image for matching
                            selection1 = memPicRect.index(item)
                            hiddenImages[selection1] = True

    # Updating Display with Image after selection
    for i in range(len(Pictures)):
        if hiddenImages[i] == True:
            # Shows/Prints images in the apt memPicRect
            screen.blit(memPic[i], memPicRect[i])
        else:
            # Hide image under white colour
            # (screen, colour, (x position, y position, picSize for x, picSize for y))
            pygame.draw.rect(
                screen, WHITE, (memPicRect[i][0], memPicRect[i][1], picSize, picSize)
            )

    pygame.display.update()  # to update the screen with printed image

    # Matching
    if selection1 != None and selection2 != None:
        # Goes through list Chicken = Chicken
        if Pictures[selection1] == Pictures[selection2]:
            # Match success. None for further selection
            selection1, selection2 = None, None
        else:
            # Match fail. Hide image & None for further selection
            pygame.time.wait(1000)
            hiddenImages[selection1] = False
            hiddenImages[selection2] = False
            selection1, selection2 = None, None

    win = 1
    for number in range(len(hiddenImages)):
        win *= hiddenImages[number]

    if win == 1:
        gameLoop = False

    pygame.display.update()

pygame.quit()
