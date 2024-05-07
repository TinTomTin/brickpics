from PIL import Image, ImageDraw, ImageColor
import numpy as np
from enum import Enum

SIDE_LENGTH = 48

class PicPaletteEnum(Enum):
    BEST16 = 0
    LEGO = 1
    MONROE = 2

class LegoArtPic:
    def __init__(self, pillSize: int, pilsX: int, pilsY: int):
        self.pillSize = pillSize
        self.pilsX = pilsX
        self.pilsY = pilsY
        self.palette = []
        self.name = "NoName"

    def pixelLength(self):
        return self.pilsX * self.pillSize
    
    def pixelHeight(self):
        return self.pilsY * self.pillSize
    
    def configure(self, paletteType: PicPaletteEnum, name: str):
        self.name = name
        if paletteType is PicPaletteEnum.BEST16:
            self.palette = []
        elif paletteType is PicPaletteEnum.MONROE:
            self.palette = lego31197Pallette
        elif paletteType is PicPaletteEnum.LEGO:
            self.palette = legoPalette
    
def buildLegoPalette():
    stringPalette = '#F4F4F4,#CCB98D,#BB805A,#B40000,#1E5AA8,#FAC80A,#000000,#00852B,#58AB41,#91501C,#7396C8,#D67923,#069D9F,#A5CA18,#901F76,#70819A,#897D62,#19325A,#00451A,#708E7C,#720012,#FCAC00,#5F3109,#969696,#646464,#9DC3F7,#C8509B,#FF9ECD,#FFEC6C,#441A91,#E1BEA1,#352100,#AA7D55,#469BC3,#68C3E2,#D3F2EA,#A06EB9,#CDA4DE,#E2F99A,#8B844F,#FD5F84,#F5F500,#755945,#CCA373,#CA4C0B,#915C3C,#543F33,#B80000,#ADDDED,#0085B8,#FFE622,#73B464,#FAF15B,#BBB29E,#FD8ECF,#6F7AA4,#E18D0A,#AFD246,#B9953B,#8C8C8C'
    colorList = stringPalette.split(',')
    outputPalette = []
    for col in colorList:
        outputPalette += ImageColor.getrgb(col)
    return outputPalette
  
legoPalette = buildLegoPalette()

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

def adjustImagePalette(legoArtPic: LegoArtPic, inputImage: Image):
    if len(legoArtPic.palette) == 0:
        return inputImage.convert(mode="P", palette=1, colors=16, dither=3).resize([legoArtPic.pilsX, legoArtPic.pilsY])
    else:
        t_palImage = Image.new('P', (16, 16))
        t_palImage.putpalette(legoArtPic.palette)
        return inputImage.quantize(palette=t_palImage, dither=0).resize([legoArtPic.pilsX, legoArtPic.pilsY])

def generateColorLegend(lpic: LegoArtPic, inputImage: Image):
    colorAdjustedImage = adjustImagePalette(lpic, inputImage)
    colorsUsed = colorAdjustedImage.getcolors()
    palette = colorAdjustedImage.getpalette()
    xStart = 30
    yPadding = 10
    fontOffset = int(lpic.pillSize / 2)
    legendImage = Image.new("RGB", (500, len(colorsUsed) * (lpic.pillSize + yPadding)), "#000000")
    legendDraw = ImageDraw.Draw(legendImage)
    #legendDraw.font = ImageFont.truetype("FreeMono.ttf", size=30)
    for colNumber in colorsUsed:
        paletteIndex = colNumber[1] * 3
        fillColor = (palette[paletteIndex], palette[paletteIndex + 1], palette[paletteIndex +2])
        outlineColor = (fillColor[0] + 25, fillColor[1] + 25, fillColor[2] + 25)
        x1 = xStart
        y1 = colNumber[1] * lpic.pillSize + (colNumber[1] * yPadding)
        x2 = xStart + lpic.pillSize
        y2 = (colNumber[1] * lpic.pillSize ) + (colNumber[1] * yPadding) + lpic.pillSize
        points = [(x1, y1), (x2, y2)]
        legendDraw.ellipse(points, fill=fillColor, outline=outlineColor, width=3)
        legendDraw.text((x1 + fontOffset, y1 + fontOffset), str(colNumber[1]), fill='white', anchor='mm', font_size=25)
        legendDraw.text((xStart + 70, y1 + fontOffset), 'x {cnt}'.format(cnt = colNumber[0]), fill='white', anchor='lm', font_size=25)
    return legendImage
    

def generatePillArt(legoArtPic, inputImage) -> Image:
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

def splitImage(imageToSplit: Image, legoArtPic: LegoArtPic):
    xStep = int(legoArtPic.pilsX / 3) * legoArtPic.pillSize
    yStep = int(legoArtPic.pilsY / 3) * legoArtPic.pillSize
    splitImages = []
    for box in cutboxes:
        splitImages.append(imageToSplit.crop((box[0] * xStep, box[1] * yStep, box[2] * xStep, box[3] * yStep)))
    return splitImages


def doExperiment():
    print(buildLegoPalette())
    #exp = LegoArtPic(50, SIDE_LENGTH, SIDE_LENGTH)
    #exp.palette = lego31197Pallette
    #inputImage =  Image.open("Boerneef.jpg")
    #outputImage = generatePillArt(exp, inputImage)
    #t_palImage = Image.new('P', (16, 16))
    #t_palImage.putpalette(paletteTest)
    #converted = outputImage.quantize(palette=t_palImage, dither=0)
    #outputImage.save("2024-04-16_4.gif")
    #splitImage(outputImage, exp)
    #cropped.save("B-cropped.gif")
    #legendImage = generateColorLegend(exp.pillSize, inputImage)
    #legendImage.save("Kas2-legend.gif")

#doExperiment()


