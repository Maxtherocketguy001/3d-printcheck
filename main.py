# pip install supabase --break-system-packages
from supabase import create_client, Client
# pip inference-sdk --break-system-packages
from inference_sdk import InferenceHTTPClient
# pip install opencv-python  --break-system-packages
import cv2

import time




# initialize the roboflow client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="dqVpz2N2VJeNGw8wQE3E"
)

# initialize the supabase client
url = "https://cnsyivsklaiwjgksrnug.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNuc3lpdnNrbGFpd2pna3NybnVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1OTU5NDMsImV4cCI6MjA0NjE3MTk0M30.VBh3MYdAPcPdpmDt13mv2wwVNW26d2gjELrpC84NfKc"
supabase: Client = create_client(url, key)

deviceID = "aaaaaab"



capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print("Camera Capture not Initiated. Check the Camera")
    exit()
    

while True:
    ret,frame=capture.read()
    if not ret:
        print("cant read frame")
        break
    cv2.imwrite("poop.png",frame)
    cv2.imshow("camera",frame)
    result = CLIENT.infer("poop.png", model_id="3d-print-failure-detection-efvsh-1kg6p/1")
    print(result)
    
    if len(result["predictions"]) > 0:
      status = result["predictions"][0]["class"]
      image_path = "poop.png"

      with open(image_path, 'rb') as f:
        timestamp = time.time()
        upload_path_name = f"public/{deviceID}_{timestamp}.png"

        response = supabase.storage.from_("poop_images").upload(
          file = f,
          path = upload_path_name,
          file_options = {"cache-control": "3600", "upsert": "false"},
        )

        image_path = response.full_path

        storage_path = f"https://cnsyivsklaiwjgksrnug.supabase.co/storage/v1/object/public/{image_path}"

        response = (
            supabase.table("device_images")
            .insert(
                {
                    "device_id": deviceID, 
                    "image_path": storage_path, 
                    "status": status
                }
            )
            .execute()
        )

    else:
      status = "Print is ok"
      image_path = "poop.png"

      with open(image_path, 'rb') as f:
        timestamp = time.time()
        upload_path_name = f"public/{deviceID}_{timestamp}.png"

        response = supabase.storage.from_("poop_images").upload(
          file = f,
          path = upload_path_name,
          file_options = {"cache-control": "3600", "upsert": "false"},
        )

        image_path = response.full_path

        storage_path = f"https://cnsyivsklaiwjgksrnug.supabase.co/storage/v1/object/public/{image_path}"

        response = (
            supabase.table("device_images")
            .insert(
                {
                    "device_id": deviceID, 
                    "image_path": storage_path, 
                    "status": status
                }
            )
            .execute()
        )
    
    if cv2.waitKey(5000)==ord("q"):
        break
capture.release()
cv2.destroyAllWindows()
