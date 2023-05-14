import sys
from PIL import Image
from PIL.ExifTags import TAGS

def Banner():
    print(""" 
        .<==+.
             \)
__  /*-----._//
>_)='-[[[[---'
_______________
coded by KHASEY               
        """)

# Fonction affiche les métadonnées EXIF
def display_exif_metadata(image_path):
    try:
        with Image.open(image_path) as image:
            # Récupération des métadonnées EXIF
            exif_data = image._getexif()
            if exif_data:
                print(f"Metadata for {image_path}:")
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    print(f"{tag:25}: {value}")
            else:
                print(f"No EXIF metadata found in {image_path}")
    except IOError as e:
        print(f"Error opening {image_path}: {e}")

# Fonction principale
def main():
    Banner()
    # Vérification du nombre d'arguments passés au programme
    if len(sys.argv) < 2:
        print("Usage: scorpion FILE1 [FILE2 ...]")
        return

    # Liste des extensions d'images à traiter
    valid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

    # Parcours des fichiers passés en paramètre
    for file_path in sys.argv[1:]:
        # Vérification que le fichier est une image
        if file_path.endswith(valid_extensions):
            display_exif_metadata(file_path)
        else:
            print(f"{file_path} is not a valid image file.")

# Appel de la fonction principale
if __name__ == '__main__':
    main()
