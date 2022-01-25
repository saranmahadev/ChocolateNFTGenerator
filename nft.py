from PIL import Image
from uuid import uuid4
import os
import random
import hashlib
from io import BytesIO
import base64
import datetime

class Creator:
    def __init__(self) -> None:
        self.layer_foler = 'static/images/layers'        
        self.bgs = [ f'static/images/layers/bgs/{x}' for x in os.listdir('static/images/layers/bgs') if x.endswith('.png') ]
        self.faces = [ f'static/images/layers/faces/{x}' for x in os.listdir('static/images/layers/faces') if x.endswith('.png') ]
        self.eyes = [ f'static/images/layers/eyes/{x}' for x in os.listdir('static/images/layers/eyes') if x.endswith('.png') ] 
        self.mouths = [ f'static/images/layers/mouths/{x}' for x in os.listdir('static/images/layers/mouths') if x.endswith('.png') ]
        self.hats = [ f'static/images/layers/hats/{x}' for x in os.listdir('static/images/layers/hats') if x.endswith('.png') ]       

    def __enter__(self) -> None:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def get_layers(self) -> list:
        return [
            {'name': 'bgs','items': self.bgs},  
            {'name': 'faces','items': self.faces}, 
            {'name': 'eyes','items': self.eyes}, 
            {'name': 'mouths','items': self.mouths}, 
            {'name': 'hats','items': self.hats}
        ]       
    
    def upload_layer(self,form,file) -> dict:              
        file['image'].save(f'{self.layer_foler}/{form["layer"]}/{uuid4().hex}.png')
        return {'success': True}

    def delete_layer(self,location) -> dict:
        os.remove(f'{location.get("image")}')        
        return {'success': True}

    def generate_nft(self):
        bg = random.choice(self.bgs)
        face = random.choice(self.faces)
        eye = random.choice(self.eyes)
        mouth = random.choice(self.mouths)
        hat = random.choice(self.hats)

        bg_img = Image.open(bg).convert('RGBA')
        face_img = Image.open(face).convert('RGBA')
        eye_img = Image.open(eye).convert('RGBA')
        mouth_img = Image.open(mouth).convert('RGBA')
        hat_img = Image.open(hat).convert('RGBA')

        com1 = Image.alpha_composite(bg_img, face_img)  
        com2 = Image.alpha_composite(com1, eye_img)
        com3 = Image.alpha_composite(com2, mouth_img)
        com4 = Image.alpha_composite(com3, hat_img)

        return com4

    def generate_base64(self, nft) -> str:
        buffer = BytesIO()
        nft.save(buffer, format='PNG')
        return f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    
    def generate_hash(self, img) -> str:
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
        