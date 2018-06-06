import sys
import pygame
import json
import matplotlib.colors as colors



#funkcja do odczytu pliku .json
def readFile(filename):
    data={}
    try:
        with open(filename) as file:
            data=json.load(file)
    except FileNotFoundError:
        print("There is no such input file!")
        sys.exit(1)
    except IOError:
        print("Error while loading input file!")
        sys.exit(1)
    except:
        print("Unexpected exception!")
        sys.exit(1)

    return data



#funkcja do otrzymania kodu RGB dla domyslnego tla(koloru) figur, jesli nie jest on okreslony dla danej figury
#albo nie wystepuje w zbiorze dostepnych kolorow
def getForeground(palette, color):
    for col in palette:
        if col==color:
            hex = colors.hex2color(color)
            return tuple([int(255 * c) for c in hex])

#funkcja do konwersji kodowania kolorow na RGB,
def convertToRGB(dict , color, fgcol):


    #jesli color byl juz zapisany w rgb
    if color[0]== "(" and color[len(color)-1]== ")":
        color = color.strip('(')
        color = color.strip(')')
        color = color.split(',')
        return tuple([(int(c)) for c in color])


    #jesli kolor byl zapisany w notacji html
    if color[0]=="#":
        #color = color.strip('#')
        hex = colors.hex2color(color)
        return tuple([int(255*c) for c in hex])

    #jesli kolor byl w postaci slownej
    palette = dict['Palette']

    for col in palette:
        if col == color:
            hex = colors.hex2color(color)
            return tuple([int(255 * c) for c in hex])

    print("Danego koloru nie ma w podanej gamie kolorow: " + color)
    return fgcol





#glowna funkcja do obslugi biblioteki pygame i wykonania zadania programu
def parse(toSave,inputfile,arg=""):
    try:
        pygame.init()
        data = readFile(inputfile) #odczyt i parsowanie pliku .json
        screenParams = data["Screen"] #rozmiary dla wyswietlanego ekranu
        size = [screenParams["width"], screenParams["height"]]
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Drawing figures ")

        fgcol = getForeground(data["Palette"], data["Screen"]["fg_color"]) #uzyskanie kodu RGB dla domyslnego koloru figury
        bg_color = convertToRGB(data , screenParams["bg_color"], fgcol) #uzyskanie koloru tla ekranu
        screen.fill(bg_color)
        Figs = data["Figures"]
        flag=True

        while True:
            if flag:
                for figure in Figs : #przechodze po figurach w pliku
                    pygame.display.update()
                    if figure['type'] == 'point':
                        x=figure['x']
                        y=figure['y']
                        if len(figure)==3:
                            pygame.draw.line(screen,fgcol,[x,y],[x+1,y+1],10)
                        elif len(figure)==4:
                            col = convertToRGB(data, figure['color'], fgcol)
                            pygame.draw.line(screen, col, [x, y], [x , y ], 10)
                        pygame.display.update()

                    elif figure['type']=='rectangle':
                        x = figure['x'] - (figure['width']/2)
                        y = figure['y'] - (figure['height']/2)
                        if len(figure) == 5:
                            pygame.draw.rect(screen, fgcol, [x, y, figure['width'], figure['height']])
                        elif len(figure) == 6:
                            col = convertToRGB(data, figure['color'], fgcol)
                            pygame.draw.rect(screen , col, [x , y , figure['width'] , figure['height'] ])
                        pygame.display.update()

                    elif figure['type']=='polygon':
                        pointlist=figure['points']
                        if len(figure) == 2:
                            pygame.draw.polygon(screen,fgcol,pointlist)
                        elif len(figure) == 3:
                            col = convertToRGB(data, figure['color'], fgcol)
                            pygame.draw.polygon(screen, col, pointlist)
                        pygame.display.update()

                    elif figure['type']=='square':
                        x = figure['x'] - (figure['size'] / 2)
                        y = figure['y'] - (figure['size'] / 2)
                        size = figure['size']
                        if len(figure) == 4:
                            pygame.draw.rect(screen, fgcol, [x, y, size, size])
                        elif len(figure) == 5:
                            col = convertToRGB(data, figure['color'],fgcol)
                            pygame.draw.rect(screen, col, [x, y , size, size])
                        pygame.display.update()

                    elif figure['type']=='circle':
                        x = figure['x']
                        y = figure['y']
                        radius= figure['radius']
                        if len(figure) == 4:
                            pygame.draw.circle(screen, fgcol, [x, y], radius)
                        elif len(figure) == 5:
                            col = convertToRGB(data, figure['color'], fgcol)
                            pygame.draw.circle(screen, col, [x, y], radius)
                        pygame.display.update()



            flag=False
            pygame.display.update()
            # okno wyswietla sie dopoki uzytkownik go nie zamknie
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    if toSave:
                        pygame.image.save(screen,arg)
                    pygame.quit()
                    sys.exit()
    except pygame.error:
        print("Error while using pygame library")
        sys.exit(1)

def main(argv): #obsluga linii komend

    if len(argv)== 2 and argv[1]=="-h" :
        print(" python filename.py inputfile -o [--output] outfile")
        sys.exit()

    elif len(argv)==2:
        print("Display only ")
        parse(False,argv[1])

    elif len(argv)==4 and (argv[2]=="-o" or argv[2]=="--output"):
        outfile = argv[3]
        print("Outfile = ", outfile)
        parse(True,argv[1], outfile)

    else:
        print("Wrong arguments")
        print(" python filename.py inputfile -o [--output] outfile")
        sys.exit()



if __name__=="__main__":
    main(sys.argv[0:])
