from PIL import Image, ExifTags

def correct_image_orientation(image_path, output_path):
    # Charger l'image
    image = Image.open(image_path)
    
    # Vérifier si l'image contient des métadonnées EXIF d'orientation
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        
        # Appliquer la rotation correcte en fonction des métadonnées EXIF
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
        
    except (AttributeError, KeyError, IndexError):
        # Les métadonnées EXIF n'existent pas ou ne sont pas lisibles
        pass
    
    # Enregistrer l'image avec l'orientation correcte
    image.save(output_path)
    print("L'image a été corrigée et enregistrée.")

# Utilisation de la fonction
image_path = "./photo.jpg"
output_path = "./image_corrigee.jpg"
correct_image_orientation(image_path, output_path)
