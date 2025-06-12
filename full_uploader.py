from flask import Flask, request, jsonify
import base64, requests

app = Flask(__name__)

@app.route("/linkedin/upload", methods=["POST"])
def upload_to_linkedin():
    data = request.get_json()

    try:
        img_b64 = data["base64_image"]
        content = data["content"]
        token = data["access_token"]
        person_urn = data["person_urn"]

        image_bytes = base64.b64decode(img_b64)

        # Register image upload
        reg_payload = {
            "registerUploadRequest": {
                "owner": person_urn,
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "serviceRelationships": [{
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }]
            }
        }

        reg_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        reg_res = requests.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            json=reg_payload, headers=reg_headers)

        if reg_res.status_code != 200:
            return jsonify({"error": "Register failed", "details": reg_res.text}), 500

        reg_data = reg_res.json()
        upload_url = reg_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset_urn = reg_data["value"]["asset"]

        # Upload image
        put_headers = {"Content-Type": "image/png"}
        put_res = requests.put(upload_url, headers=put_headers, data=image_bytes)

        if put_res.status_code not in [200, 201]:
            return jsonify({"error": "Upload failed", "status": put_res.status_code}), 500

        # Post to LinkedIn
        post_body = {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "IMAGE",
                    "media": [{
                        "status": "READY",
                        "media": asset_urn,
                        "title": {"text": "Posted from SN"},
                        "description": {"text": "Middleware Test"}
                    }]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        post_res = requests.post("https://api.linkedin.com/v2/ugcPosts",
                                 json=post_body, headers=reg_headers)

        if post_res.status_code != 201:
            return jsonify({"error": "Post failed", "details": post_res.text}), 500

        return jsonify({
            "message": "✅ Post Successful",
            "asset_urn": asset_urn,
            "linkedin_response": post_res.json()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run()
