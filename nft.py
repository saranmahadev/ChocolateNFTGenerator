from PIL import Image
from PIL.Image import Image as PILImage
from uuid import uuid4
import os
import random
import hashlib
from io import BytesIO
import base64
import datetime

class Creator:
    def __init__(self) -> None:        
        with open('images/bg.png', 'rb') as f:
            self.bg = Image.open(f).convert('RGBA')       
        self.faces = [ f'images/faces/{x}' for x in os.listdir('images/faces') if x.endswith('.png') ]
        self.eyes = [ f'images/eyes/{x}' for x in os.listdir('images/eyes') if x.endswith('.png') ] 
        self.mouths = [ f'images/mouths/{x}' for x in os.listdir('images/mouths') if x.endswith('.png') ]
        self.hats = [ f'images/hats/{x}' for x in os.listdir('images/hats') if x.endswith('.png') ]       

    def __enter__(self) -> None:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def generate_nft(self) -> PILImage:
        face = random.choice(self.faces)
        eye = random.choice(self.eyes)
        mouth = random.choice(self.mouths)
        hat = random.choice(self.hats)

        face_img = Image.open(face).convert('RGBA')
        eye_img = Image.open(eye).convert('RGBA')
        mouth_img = Image.open(mouth).convert('RGBA')
        hat_img = Image.open(hat).convert('RGBA')

        com1 = Image.alpha_composite(self.bg, face_img)  
        com2 = Image.alpha_composite(com1, eye_img)
        com3 = Image.alpha_composite(com2, mouth_img)
        com4 = Image.alpha_composite(com3, hat_img)

        return com4

    def generate_base64(self, nft: PILImage) -> str:
        buffer = BytesIO()
        nft.save(buffer, format='PNG')
        return f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    
    def generate_hash(self, img: PILImage) -> str:
        img_bytes = img.tobytes()
        hash_object = hashlib.sha256(img_bytes)
        hex_dig = hash_object.hexdigest()
        return hex_dig  

    def mint_nft(self, count:int = 1) -> list:        
        nfts = []
        for _ in range(count):
            image = self.generate_nft()
            nfts.append({
                'image': self.generate_base64(image),
                'hash' : self.generate_hash(image),
                'id' : uuid4().hex,
                'created_at' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        return nfts
    
nfts = Creator().mint_nft(2)
print(nfts[0]["image"] == nfts[1]["image"])

        