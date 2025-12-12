import cv2
import os

#Konfiguracia
image_folder = "D:/temp_training_folder/for_labeling"  # Priecinok pre obrazky
label_folder = "D:/temp_training_folder/for_labeling"  # Priecinok pre text subory anotacia
num_classes = 5          # Pocet tried

os.makedirs(label_folder, exist_ok=True)

# konvertovanie bbox do YOLO formatu
def bbox_to_yolo(x1, y1, x2, y2, img_w, img_h, cls):
    x_center = (x1 + x2) / 2 / img_w
    y_center = (y1 + y2) / 2 / img_h
    width = abs(x2 - x1) / img_w
    height = abs(y2 - y1) / img_h
    return f"{cls} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"

# Hlavny cyklus pre pouzitie program pre vsetky obrazky
for filename in os.listdir(image_folder):
    if not filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        continue

    img_path = os.path.join(image_folder, filename)
    img = cv2.imread(img_path)
    img_h, img_w = img.shape[:2]
    bboxes = []
    # Zaciatok kreslenia mysou
    state = {'drawing': False, 'x_start': -1, 'y_start': -1, 'current_class': 0}
    def draw_rectangle(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            state['drawing'] = True
            state['x_start'], state['y_start'] = x, y
            # Vyziadanie ID triedy
            while True:
                try:
                    cls = int(input(f"Enter class ID (0-{num_classes-1}) for this box: "))
                    if 0 <= cls < num_classes:
                        state['current_class'] = cls
                        break
                    else:
                        print(f"Invalid class ID. Must be 0-{num_classes-1}.")
                except:
                    print("Enter a valid integer.")
        elif event == cv2.EVENT_MOUSEMOVE and state['drawing']:
            temp_img = img.copy()
            cv2.rectangle(temp_img, (state['x_start'], state['y_start']), (x, y), (0, 255, 0), 2)
            cv2.imshow("Image", temp_img)
        elif event == cv2.EVENT_LBUTTONUP:
            state['drawing'] = False
            bboxes.append((state['x_start'], state['y_start'], x, y, state['current_class']))
            cv2.rectangle(img, (state['x_start'], state['y_start']), (x, y), (0, 255, 0), 2)
            cv2.imshow("Image", img)
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", draw_rectangle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Ulozenie
    label_file = os.path.join(label_folder, os.path.splitext(filename)[0] + ".txt")
    with open(label_file, "w") as f:
        for x1, y1, x2, y2, cls in bboxes:
            f.write(bbox_to_yolo(x1, y1, x2, y2, img_w, img_h, cls) + "\n")
print("Labeling complete!")