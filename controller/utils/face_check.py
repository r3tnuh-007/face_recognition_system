import face_recognition
import asyncio


async def check_face(image_path: str) -> bool:
	# Carrega as imagens
	img = face_recognition.load_image_file(image_path)
	print(image_path)
	# Extrai os encodings (representações numéricas dos rostos)
	encoding = face_recognition.face_encodings(img)
	# Verifica se encontrou rostos
	if len(encoding) == 0:
		print(f"🚫 Nenhum rosto encontrado em {image_path}")
		return False
	print("🟢 Face detected")
	return True

