try:
    from PIL import Image, ImageDraw
    import os

    # Crear directorio assets si no existe
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Crear icono (azul con una letra V blanca)
    img = Image.new('RGBA', (256, 256), color=(59, 130, 246, 255))
    draw = ImageDraw.Draw(img)
    
    # Dibujar un triángulo simple como logo (V)
    draw.polygon([(40, 40), (128, 220), (216, 40)], fill=(255, 255, 255, 255))
    
    img.save('assets/vectora.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("✅ assets/vectora.ico generado exitosamente")
except Exception as e:
    print(f"❌ Error generando icono: {e}")
