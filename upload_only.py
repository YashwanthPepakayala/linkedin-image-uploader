from flask import Flask, request, jsonify
import base64, requests

app = Flask(__name__)

@app.route("/upload-only", methods=["POST"])
def upload_image_only():
    data = request.get_json()

    try:
        upload_url = data["upload_url"]
        base64_img = data["base64_image"]
        content_type = data.get("content_type", "image/png")

        # Convert base64 to binary
        image_bytes = base64.b64decode(base64_img)

        # Upload to LinkedIn
        headers = {"Content-Type": content_type}
        response = requests.put(upload_url, headers=headers, data=image_bytes)

        if response.status_code not in [200, 201]:
            return jsonify({
                "error": "Upload failed",
                "status": response.status_code,
                "details": response.text
            }), 500

        return jsonify({"message": "✅ Upload complete"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# if __name__ == "__main__":
#     app.run()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
