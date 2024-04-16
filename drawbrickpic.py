from PIL import Image, ImageDraw, ImageFont
import numpy as np

SIDE_LENGTH = 48

class LegoArtPic:
    def __init__(self, pillSize, pilsX, pilsY):
        self.pillSize = pillSize
        self.pilsX = pilsX
        self.pilsY = pilsY
        self.palette = []

    def pixelLength(self):
        return self.pilsX * self.pillSize
    
    def pixelHeight(self):
        return self.pilsY * self.pillSize
    
  
paletteTest = [0,0,0,
               255,255,255,
               0,200,0]

lego31197Pallette = [0,0,0,
                     51,51,51,
                     20,184,217,
                     206,212,32,
                     173,109,168,
                     138,51,130,
                     92,9,85]
    
cutboxes = np.array([[0,0,1,1], [1,0,2,1], [2,0,3,1],
                     [0,1,1,2], [1,1,2,2], [2,1,3,2],
                     [0,2,1,3], [1,2,2,3], [2,2,3,3]])

def adjustImagePalette(legoArtPic, inputImage):
    if len(legoArtPic.palette) == 0:
        return inputImage.convert(mode="P", palette=1, colors=16, dither=3).resize([legoArtPic.pilsX, legoArtPic.pilsY])
    else:
        t_palImage = Image.new('P', (16, 16))
        t_palImage.putpalette(legoArtPic.palette)
        return inputImage.quantize(palette=t_palImage, dither=1).resize([legoArtPic.pilsX, legoArtPic.pilsY])

def generateColorLegend(pillSize, inputImage):
    colorAdjustedImage = inputImage.convert(mode="P", palette=1, colors=16, dither=3).resize([48, 48])
    colorsUsed = colorAdjustedImage.getcolors()
    palette = colorAdjustedImage.getpalette()
    xStart = 30
    yPadding = 10
    fontOffset = int(pillSize / 2)
    legendImage = Image.new("RGB", (500, len(colorsUsed) * (pillSize + yPadding)), "#000000")
    legendDraw = ImageDraw.Draw(legendImage)
    #legendDraw.font = ImageFont.truetype("FreeMono.ttf", size=30)
    for colNumber in colorsUsed:
        paletteIndex = colNumber[1] * 3
        fillColor = (palette[paletteIndex], palette[paletteIndex + 1], palette[paletteIndex +2])
        outlineColor = (fillColor[0] + 25, fillColor[1] + 25, fillColor[2] + 25)
        x1 = xStart
        y1 = colNumber[1] * pillSize + (colNumber[1] * yPadding)
        x2 = xStart + pillSize
        y2 = (colNumber[1] * pillSize ) + (colNumber[1] * yPadding) + pillSize
        points = [(x1, y1), (x2, y2)]
        legendDraw.ellipse(points, fill=fillColor, outline=outlineColor, width=3)
        legendDraw.text((x1 + fontOffset, y1 + fontOffset), str(colNumber[1]), fill='white', anchor='mm', font_size=25)
        legendDraw.text((xStart + 70, y1 + fontOffset), 'x {cnt}'.format(cnt = colNumber[0]), fill='white', anchor='lm', font_size=25)
    return legendImage
    

def generatePillArt(legoArtPic, inputImage):
    #colorAdjustedImage = inputImage.convert(mode="P", palette=1, colors=16, dither=3).resize([legoArtPic.pilsX, legoArtPic.pilsY])
    colorAdjustedImage = adjustImagePalette(legoArtPic, inputImage)
    inputPixelMap = colorAdjustedImage.load()
    inputPalette = colorAdjustedImage.getpalette()
    fontOffset = int(legoArtPic.pillSize / 2)

    image = Image.new("RGB", (legoArtPic.pixelLength(), legoArtPic.pixelHeight()), "#000012")
    draw = ImageDraw.Draw(image)
    #draw.font = ImageFont.truetype("FreeMono.ttf", size=30)
    for x in range(legoArtPic.pilsX):
        for y in range(legoArtPic.pilsY):
            px = x * legoArtPic.pillSize
            py = y * legoArtPic.pillSize
            paletteIndex = inputPixelMap[x, y] * 3
            fillColor = (inputPalette[paletteIndex], inputPalette[paletteIndex + 1], inputPalette[paletteIndex +2])
            outlineColor = (fillColor[0] + 25, fillColor[1] + 25, fillColor[2] + 25)
            points = [(px, py), (px + legoArtPic.pillSize, py + legoArtPic.pillSize)]
            draw.ellipse(points, fill=fillColor, width=3, outline=outlineColor)
            draw.text((px + fontOffset, py + fontOffset), str(int(paletteIndex / 3)),fill=(200, 200, 200), anchor="mm", font_size=25)
    return image

def splitImage(inputImage, legoArtPic):
    xStep = int(legoArtPic.pilsX / 3) * legoArtPic.pillSize
    yStep = int(legoArtPic.pilsY / 3) * legoArtPic.pillSize
    splitImages = []
    boxNum = 0
    for box in cutboxes:
        boxNum += 1
        splitImages.append(inputImage.crop((box[0] * xStep, box[1] * yStep, box[2] * xStep, box[3] * yStep)))
    return splitImages


def doExperiment():
    exp = LegoArtPic(50, SIDE_LENGTH, SIDE_LENGTH)
    exp.palette = lego31197Pallette
    inputImage =  Image.open("Boerneef.jpg")
    outputImage = generatePillArt(exp, inputImage)
    #t_palImage = Image.new('P', (16, 16))
    #t_palImage.putpalette(paletteTest)
    #converted = outputImage.quantize(palette=t_palImage, dither=0)
    outputImage.save("2024-04-16_4.gif")
    #splitImage(outputImage, exp)
    #cropped.save("B-cropped.gif")
    #legendImage = generateColorLegend(exp.pillSize, inputImage)
    #legendImage.save("Kas2-legend.gif")

#doExperiment()


