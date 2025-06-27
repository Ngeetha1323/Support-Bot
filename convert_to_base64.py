import base64

with open("assets/background.png.png", "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

# Save it to a text file
with open("background_base64.txt", "w") as output_file:
    output_file.write(encoded)

print("Base64 string saved to background_base64.txt")
