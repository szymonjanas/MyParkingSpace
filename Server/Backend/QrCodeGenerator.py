import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

class QrCodeGenerator:
    def __init__(self):
        self.text = None

        self.version = 1
        self.box_size = 8
        self.border = 2
        self.qr = None

        self.color = "black"
        self.bgColor = "white"
        self.imgQrCode = None

        self.byteBufferQrCode = None

    def __initQRCode__(self):
        self.qr = qrcode.QRCode(
                    version=self.version,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=self.box_size,
                    border=self.border)

    def __generateImage__(self):
        self.qr.add_data(self.text)
        self.qr.make(fit=True)
        self.imgQrCode = self.qr.make_image(
                                    fill_color=self.color,
                                    back_color=self.bgColor)
        
        width = self.imgQrCode.width + 180
        descriptionImage = Image.new("RGB", (width, self.imgQrCode.height + 50), "white")
        descriptionDraw = ImageDraw.Draw(descriptionImage)

        descriptionImage.paste(self.imgQrCode, (0, 0))

        descriptionDraw.text(
            (40, self.imgQrCode.height-10), 
            self.text, 
            font=ImageFont.truetype("Backend/fonts/Lato-Bold.ttf", 42), 
            fill="black")
    
        self.imgQrCode = descriptionImage

    def __packIntoBuffer__(self):
        self.byteBufferQrCode = BytesIO()
        self.imgQrCode.save(self.byteBufferQrCode, format="PNG")
        self.byteBufferQrCode.seek(0)

    def generateBytes(self, text):
        self.text = text
        self.__initQRCode__()
        self.__generateImage__()
        self.__packIntoBuffer__()
        return self.byteBufferQrCode
    
    def genereateImg(self, text):
        self.text = text
        self.__initQRCode__()
        self.__generateImage__()
        return self.imgQrCode
