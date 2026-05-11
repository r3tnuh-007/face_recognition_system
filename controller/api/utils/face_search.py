import face_recognition
import asyncio


async def verificar_faces(imagem1_path: str, imagem2_path: str):
	# Carrega as imagens
	try:
		img1 = face_recognition.load_image_file(imagem1_path)
		img2 = face_recognition.load_image_file(imagem2_path)
	except:
		print("🚫 caminho invalido!!")
		return [False]
	# Extrai os encodings (representações numéricas dos rostos)
	encoding1 = face_recognition.face_encodings(img1)
	encoding2 = face_recognition.face_encodings(img2)
	# Verifica se encontrou rostos
	if len(encoding1) == 0:
		print(f"🚫 Nenhum rosto encontrado em {imagem1_path}")
		return [False]
	if len(encoding2) == 0:
		print(f"🚫 Nenhum rosto encontrado em {imagem2_path}")
		return [False]
	# Compara os rostos
	resultado = face_recognition.compare_faces([encoding1[0]], encoding2[0])
	if resultado[0]:
		print("🟢 As fotos são da mesma pessoa!")
		return [True, imagem2_path.split('/')[-1]]
	else:
		print("🚫 As fotos são de pessoas diferentes!")
		return [False]


#Chamar funcao para criar a lista de tarefas
async def task_builder(img1, imgs):
	tasks = []
	for img2 in imgs:
		tasks.append(verificar_faces(img1, img2))
	results = await asyncio.gather(*tasks)
	print(results)
	return results

# Usa a função
