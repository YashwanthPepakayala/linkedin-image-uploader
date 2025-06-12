from flask import Flask, request, jsonify
import base64, requests

app = Flask(__name__)

@app.route("/upload-only", methods=["POST"])
def upload_image_only():
    try:
        # 🔎 Step 1: Parse and validate incoming JSON
        data = request.get_json()
        if not data:
            print("🚫 No JSON received.")
            return jsonify({"error": "Missing or invalid JSON"}), 400

        upload_url = data.get("upload_url")
        base64_img = data.get("base64_image")
        content_type = data.get("content_type", "image/png")

        if not upload_url or not base64_img:
            print("🚫 upload_url or base64_image missing.")
            return jsonify({"error": "upload_url and base64_image are required"}), 400

        print("🔗 Upload URL (first 50 chars):", upload_url[:50] + "...")
        print("🧪 Content-Type:", content_type)
        print("🧪 Base64 length:", len(base64_img))

        # 🧪 Step 2: Decode image
        try:
            image_bytes = base64.b64decode(base64_img)
            print("📦 Decoded image byte size:", len(image_bytes))
        except Exception as decode_err:
            print("🚫 Base64 decoding failed:", str(decode_err))
            return jsonify({"error": "Base64 decode failed", "details": str(decode_err)}), 400

        # ⬆️ Step 3: Upload to LinkedIn via PUT
        headers = {
            "Content-Type": content_type
        }

        response = requests.put(upload_url, headers=headers, data=image_bytes)

        print("📡 PUT Response Code:", response.status_code)
        print("📡 PUT Response Text (first 200 chars):", response.text[:200])

        if response.status_code not in [200, 201]:
            return jsonify({
                "error": "Upload failed",
                "status": response.status_code,
                "details": response.text
            }), 500

        return jsonify({"message": "✅ Upload complete"}), 200

    except Exception as e:
        print("🚨 Unexpected exception:", str(e))
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# 🔌 Flask entry point for Render
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
