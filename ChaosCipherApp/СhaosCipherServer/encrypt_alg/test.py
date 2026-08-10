from io import BytesIO


from strategies import ImageCryptor, TextCryptor
from generators import ChaosFactory
#import PIL.Image as Image
generator_factory = ChaosFactory()
dict = {"logisticXLorenz":0.3, "lorenzX":1, "lorenzY":2, "lorenzZ":3}
gen1= generator_factory.create_generator("lorenz", dict, "bytes" )
"""
image_strategy = ImageCryptor()
filename = "C:\\Users\\САША\\Desktop\\Диплом 25\\ExperimentalImages\\1024x768.png"
with open(filename, "rb") as f:
    img_bytes = f.read()
encrypted_img = image_strategy.process(img_bytes, gen1, "encrypt")
decrypted_img = image_strategy.process(encrypted_img, gen1, "decrypt")
"""
"""text_strategy = TextCryptor()
text = "Who tried to eat an elephant?"
encrypted_text = text_strategy.process(text, gen1, "encrypt", "bytes")
decrypted_text = text_strategy.process(encrypted_text, gen1, "decrypt", "bytes")
print(encrypted_text)
print(decrypted_text)
"""

"""text_strategy = TextCryptor()
text = "Who tried to eat an elephant?"
encrypted_text = text_strategy.process(text, gen1, "encrypt", "chars")
decrypted_text = text_strategy.process(encrypted_text, gen1, "decrypt", "chars")
print(encrypted_text)
print(decrypted_text)"""

