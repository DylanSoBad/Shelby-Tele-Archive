from google import genai
from config import Config

# Khởi tạo client mới với genai
client = genai.Client(api_key=Config.GEMINI_API_KEY)

# Sử dụng mô hình mới nhất
MODEL_NAME = 'gemini-2.5-flash'

def summarize_text(text: str) -> str:
    """
    Summarizes a block of text to generate metadata for the Shelby blob.
    """
    if len(text) < 100:
        return text # Do not summarize if it's already short enough
        
    prompt = (
        "Identify and summarize the main content of the following text to serve as brief metadata "
        "(max 2-3 sentences). Return only the summary text directly, with no greetings: \n\n"
        f"{text}"
    )
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return "Metadata: Unable to generate summary due to system error."

def generate_metadata_for_file(filename: str, file_size: int, extra_info: str = "") -> str:
    """
    Creates metadata based on file details.
    """
    prompt = (
        f"Generate a brief metadata summary (1-2 sentences) for an uploaded document.\n"
        f"Filename: {filename}\n"
        f"Size: {file_size} bytes\n"
        f"Additional Info: {extra_info}\n"
    )
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return f"File upload: {filename} (Size: {file_size} bytes)"
