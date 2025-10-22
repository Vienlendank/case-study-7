from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient
import os

CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=mxr9etsds;AccountKey=21zN841z3NDchKJtWEv11yDZ1djUFxTJqN+bSMqqYqazAheEwuRpPLt3pzKOdxrh5TuBSxDPHddh+ASt+WzgmA==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "lanternfly-images"

bsc = BlobServiceClient.from_connection_string(CONNECTION_STRING)## Create Blob Service Client
cc  = bsc.get_container_client(CONTAINER_NAME) # Replace with Container name cc.url will get you the url path to the container.  

app = Flask(__name__)

try:
    cc.create_container(public_access="container")  # makes it public-read for gallery
    print(f"Created container: {CONTAINER_NAME}")
except Exception:
    print(f"Container {CONTAINER_NAME} already exists or is accessible.")

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/v1/upload")
def upload():
    f = request.files["file"]
    filename = f.filename
    # Complete this section so that you can uplaod files
    blob_client = cc.get_blob_client(filename)
    blob_client.upload_blob(f, overwrite=True)

    return jsonify(ok=True, url=f"{cc.url}/{f.filename}")

## Add other API end points. (/api/v1/gallery)  and (/api/v1/health)
@app.get("/api/v1/gallery")
def gallery():
    blobs = [f"{cc.url}/{b.name}" for b in cc.list_blobs()]
    return jsonify(ok=True, gallery=blobs)

@app.get("/api/v1/health")
def health():
    return jsonify(ok=True, message="Healthy")

if __name__ == "__main__":
    app.run(debug=True)