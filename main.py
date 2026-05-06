import face_recognition

def verificar_faces(imagem1_path: str, imagem2_path: str) -> bool:
    # Carrega as imagens
    img1 = face_recognition.load_image_file(imagem1_path)
    img2 = face_recognition.load_image_file(imagem2_path)

    # Extrai os encodings (representações numéricas dos rostos)
    encoding1 = face_recognition.face_encodings(img1)
    encoding2 = face_recognition.face_encodings(img2)

    # Verifica se encontrou rostos
    if len(encoding1) == 0:
        print(f"❌ Nenhum rosto encontrado em {imagem1_path}")
        return False

    if len(encoding2) == 0:
        print(f"❌ Nenhum rosto encontrado em {imagem2_path}")
        return False

    # Compara os rostos
    resultado = face_recognition.compare_faces([encoding1[0]], encoding2[0])

    if resultado[0]:
        print("✅ As fotos são da mesma pessoa!")
        return True
    else:
        print("❌ As fotos são de pessoas diferentes!")
        return False

# Usa a função
verificar_faces("./a.jpeg", "./a.jpeg")
