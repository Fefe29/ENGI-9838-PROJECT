import cv2
from ultralytics import YOLO
import torch
torch.cuda.is_available()
#import tensorflowjs as tfjs


def train_yolo():
    # Paths to the dataset and configuration file
    #dataset_path = r'C:/Users/mohse/Desktop/Project/Face Anti-spoofing/Dataset2/data.yaml' 
    dataset_path = r"C:/Users/mohse/Desktop/Project/Face Anti-spoofing/Dataset3_CelebA_Spoof/data.yaml"
    # Initialize YOLO model
    model = YOLO('yolo11n.pt')  # Replace 'yolov8n.pt' with the desired pre-trained model version (n/s/m/l/x).

    # Train the model using GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.train(
        data=dataset_path,  # Path to dataset configuration
        epochs=50,  # Train for sufficient epochs
        imgsz=640,  # Standard input size for YOLO
        batch=16,  # Reduce batch size for RTX 3050 Ti if necessary
        project='YOLO11_Training',  # Project name for logging
        name='experiment_name',  # Experiment name
        half=True,  # Enable mixed precision
        cache=True,  # Cache dataset in memory
        augment=True
        
    )
 
    print("Training completed. Check the runs folder for results.")



def live_prediction():
    import cv2
    from ultralytics import YOLO

    # Load the YOLO model
    # model = YOLO(r'C:/Users/mohse/Desktop/Project/Face Anti-spoofing/YOLO11_Training/experiment_name/weights/best.pt')
    model = YOLO(r'C:/Users/mohse/Desktop/Project/Face Anti-spoofing/YOLO11_Training/Last_Training_Over_CelebA_Spoof/weights/best.pt')


    # Initialize video capture for live prediction
    cap = cv2.VideoCapture(0)  # 0 for the default camera

    # Set video capture properties (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Perform prediction using YOLO
        results = model.predict(source=frame, conf=0.50, iou=0.6, show=False)  # Adjust confidence and IoU thresholds

        # Display the YOLO layout
        results_img = results[0].plot()  # Use YOLO's built-in plotting method

        # Show the annotated frame
        cv2.imshow('Live Face Anti-Spoofing Detection', results_img)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    


def export_yolo_model():
    model_path = 'C:/Users/mohse/Desktop/Project/Face Anti-spoofing/YOLO11_Training/experiment_name4/weights/best.pt'
    #model_path = r"C:\Users\mohse\Desktop\Project\Face Anti-spoofing\yolo11n.pt"
    # Initialize the YOLO model
    model = YOLO(model_path)

    # Export to TensorFlow SavedModel format
    model.export(format='tfjs') #tfjs
    print(f"Model exported to TensorFlow format saved")

#export_yolo_model()
#train_yolo()
live_prediction()


"""live: 10730
spoof: 18537
The training dataset is not balanced."""





