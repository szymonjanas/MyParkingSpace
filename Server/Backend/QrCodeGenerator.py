import qrcode
from io import BytesIO

def generateQrCode(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=12,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    qrImgReservationId = qr.make_image(fill_color="black", back_color="white")

    byteBuffer = BytesIO()
    qrImgReservationId.save(byteBuffer)
    byteBuffer.seek(0)
    
    return byteBuffer
