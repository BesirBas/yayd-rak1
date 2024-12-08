import cv2
import numpy as np

def detect_objects():
    # Kamera bağlantısı
    cap = cv2.VideoCapture(0)  # 0 varsayılan kamera, gerekirse değiştirilebilir

    # YOLO nesne tespiti modelini yükle
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Renk atamaları
    colors = {
        "person": (255, 0, 0),      # Mavi
        "car": (0, 255, 0),         # Yeşil
        "bicycle": (0, 0, 255),     # Kırmızı
        "dog": (255, 255, 0),       # Sarı
        "cat": (255, 0, 255),       # Mor
        "traffic light": (0, 255, 255),  # Turkuaz
        "bus": (128, 0, 128),       # Mor ton
        "motorbike": (255, 165, 0), # Turuncu
        "aeroplane": (0, 128, 255), # Açık mavi
        "train": (128, 128, 0),     # Zeytin yeşili
        "default": (255, 255, 255)  # Beyaz (Diğer nesneler için)
    }

    while True:
        # Kameradan frame al
        ret, frame = cap.read()
        height, width, _ = frame.shape

        # Blob oluştur
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        
        # Çıktı katmanlarını al
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)

        # Tespit edilen nesnelerin bilgileri
        boxes = []
        confidences = []
        class_ids = []

        # Çıktıları işle
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > 0.5:
                    # Nesne koordinatları
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Dikdörtgen çizimi için koordinatlar
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Non-maximum suppression
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Nesneleri çiz
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]

                # Sınıf adına göre renk seçimi
                color = colors.get(label, colors["default"])  # Belirtilmemiş nesneler için varsayılan renk (beyaz)

                # Nesne bilgilerini ekrana yaz
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, f'{label} {confidence:.2f}', (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Frame'i göster
        cv2.imshow('Nesne Tespiti', frame)

        # Çıkış için 'q' tuşuna bas
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kaynakları temizle
    cap.release()
    cv2.destroyAllWindows()

# Script'i çalıştır
if __name__ == "__main__":
    detect_objects()
