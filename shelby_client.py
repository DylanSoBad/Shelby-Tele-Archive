import os
import json
import subprocess
import tempfile
import uuid

def upload_to_shelby(content: bytes, metadata_summary: str, content_type: str = "text/plain") -> dict:
    """

    """

    temp_dir = tempfile.gettempdir()
    file_name = f"shelby_upload_{uuid.uuid4().hex}"
    temp_file_path = os.path.join(temp_dir, file_name)
    
    with open(temp_file_path, "wb") as f:
        f.write(content)
    
    try:

        node_script_path = os.path.join(os.path.dirname(__file__), "shelby_uploader.mjs")
        

        blob_name = f"blob_{uuid.uuid4().hex[:8]}"
        

        result = subprocess.run(
            ["node", node_script_path, temp_file_path, blob_name],
            capture_output=True,
            text=True,
            check=True # Sẽ raise exception nếu non-zero exit code
        )
        

        output_data = json.loads(result.stdout)
        return output_data
        
    except subprocess.CalledProcessError as e:

        try:
            error_msg = json.loads(e.stderr).get("error", "Unknown Node Error")
        except:
            error_msg = e.stderr or e.stdout or str(e)
            
        return {
            "success": False,
            "blob_id": None,
            "url": None,
            "error": f"Node.js Bridge Error: {error_msg[:1000]}"
        }
    except Exception as e:
        return {
            "success": False,
            "blob_id": None,
            "url": None,
            "error": f"Python Bridge Exception: {str(e)[:1000]}"
        }
    finally:

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def list_blobs() -> dict:
    """Lấy danh sách các blobs của người dùng từ Shelby."""
    try:
        node_script_path = os.path.join(os.path.dirname(__file__), "shelby_lister.mjs")
        result = subprocess.run(
            ["node", node_script_path],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        try:
            error_msg = json.loads(e.stderr).get("error", "Unknown Node Error")
        except:
            error_msg = e.stderr or e.stdout or str(e)
        return {"success": False, "error": f"Node.js Lister Error: {error_msg[:1000]}"}
    except Exception as e:
        return {"success": False, "error": f"Python Bridge Error: {str(e)[:1000]}"}

def download_from_shelby(blob_name: str) -> dict:
    """Tải một file từ Shelby bằng Node.js script."""
    temp_dir = tempfile.gettempdir()
    file_name = f"shelby_download_{blob_name}_{uuid.uuid4().hex}"
    temp_file_path = os.path.join(temp_dir, file_name)
    
    try:
        node_script_path = os.path.join(os.path.dirname(__file__), "shelby_downloader.mjs")
        result = subprocess.run(
            ["node", node_script_path, blob_name, temp_file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        try:
            error_msg = json.loads(e.stderr).get("error", "Unknown Node Error")
        except:
            error_msg = e.stderr or e.stdout or str(e)
        return {"success": False, "path": None, "error": f"Node.js Downloader Error: {error_msg[:1000]}"}
    except Exception as e:
        return {"success": False, "path": None, "error": f"Python Bridge Error: {str(e)[:1000]}"}
