import streamlit as st
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
from drawbrickpic import LegoArtPic
from drawbrickpic import generatePillArt, generateColorLegend, splitImage, PicPaletteEnum

defaultLegoArtPic = LegoArtPic(50, 48, 48)

st.set_page_config(
    page_title="Convert image to Lego Art",
    layout="wide",
    initial_sidebar_state="expanded"
)

def download_art(legoArtPic: LegoArtPic, mainImage: Image, legendImage: Image, splitImages):
    buffer = BytesIO()
    archive = BytesIO()
    mainFileName = "{n}_main.gif".format(n=legoArtPic.name.replace(" ", "_"))
    legendFileName = "{n}_legend.gif".format(n=legoArtPic.name.replace(" ", "_"))
    mainImage.save(buffer, format="GIF")
    with ZipFile(archive, 'w') as ziparch:
        with ziparch.open(mainFileName,'w') as mainFile:
            mainFile.write(buffer.getvalue())
        for i, tile in enumerate(splitImages):
            tileName = "{a}_tile_{n}.gif".format(a=legoArtPic.name, n=i)
            tileBuffer = BytesIO()
            tile.save(tileBuffer, format="GIF")
            with ziparch.open(tileName, 'w') as tile:
                tile.write(tileBuffer.getvalue())
        with ziparch.open(legendFileName, 'w') as legendFile:
            legendBuffer = BytesIO()
            legendImage.save(legendBuffer, format="GIF")
            legendFile.write(legendBuffer.getvalue())
    return archive.getvalue()

def makeFileName(artworkName):
    return "{n}_madeWithBrickPics.zip".format(n=artworkName.replace(" ", "_"))

def renderSplitImages(images, tab):
    row1 = tab.columns(3)
    row2 = tab.columns(3)
    row3 = tab.columns(3)
    for i, col in enumerate(row1 + row2 + row3):
        tile = col.container()
        tile.image(images[i], width=450)



st.title("BRICK PICS")

tabOriginal, tabBrickPick, tabLegend, tabSplit, tabAbout = st.tabs(["Original", "Brick Pick", "Legend", "Split","About"])

outputName = st.sidebar.text_input("Name of artwork", value="BrickPick1")
st.sidebar.markdown("For best results upload an image with 1:1 aspect ratio, or as close as possible")
inputFile = st.sidebar.file_uploader("Select an image", type=["jpg"], accept_multiple_files=False)
paletteChoice = st.sidebar.radio(":rainbow[Color Palette, not fully working]", [e.value for e in PicPaletteEnum], captions=["Best fitting 16 colors", "Official lego palette","Marylin Monroe Lego Art"])

tabAbout.markdown("Converts the uploaded image to a 48 x 48 block picture that can be built using round 48 x 48 tiles.")
tabAbout.markdown("It will generate instructions to build a 48 x 48 image such as [this set](https://www.lego.com/en-us/product/andy-warhol-s-marilyn-monroe-31197)")
tabAbout.subheader("Palettes:", divider=True)
tabAbout.markdown("**16 Colors** - This option will reduce the input image to the best 16 colors it can find.")
tabAbout.markdown("**Set 31197** - This option will try fit the image as best as it can to the colors used in [this set](https://www.lego.com/en-us/product/andy-warhol-s-marilyn-monroe-31197).")
tabAbout.markdown("**Lego palette** - This option will attempt to fit the image to the actual lego palette (solid colors only)")


if inputFile is not None:
    uploadedFile = Image.open(inputFile)
    tabOriginal.image(uploadedFile)
    defaultLegoArtPic.configure(PicPaletteEnum(paletteChoice), outputName)
    outputImage = generatePillArt(defaultLegoArtPic, uploadedFile)
    tabBrickPick.image(outputImage, outputName)
    legendImage = generateColorLegend(defaultLegoArtPic, uploadedFile)
    tabLegend.image(legendImage,'{fn}-legend'.format(fn=outputName))
    splitImages = splitImage(outputImage, defaultLegoArtPic)
    renderSplitImages(splitImages, tabSplit)
    st.sidebar.download_button("Download files",
                               download_art(defaultLegoArtPic, outputImage, legendImage, splitImages),
                               file_name=makeFileName(outputName),
                               mime="application/x-zip")