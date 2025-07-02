import pathlib
import requests
import os
from urllib.parse import urlparse
import re


# Get the rquest url from the response
def get_request_url(provided_url: str) -> str:
    return requests.get(url=provided_url).url


# Get the file extension
def get_file_extension(system_path: str) -> str:
    return pathlib.Path(system_path).suffix


# Check if a file exists
def check_file_exists(system_path: str) -> bool:
    return os.path.isfile(path=system_path)


def download_pdf(url: str, download_dir: str) -> None:
    """
    Downloads a PDF file from the given URL into the specified directory.
    Skips the download if the file already exists or the URL does not return a PDF.
    Sanitizes the filename and prints all status messages to the console.

    Args:
        url (str): The URL of the PDF file to download.
        download_dir (str): The directory where the file should be saved.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "application/pdf" not in content_type.lower():
            print(f"❌ Skipped (not a PDF): {url}")
            return

        # Extract filename from Content-Disposition
        content_disposition = response.headers.get("Content-Disposition", "")
        filename = ""

        match = re.search(
            r"filename\*\s*=\s*[^']*''([^;\r\n]+)", content_disposition, re.IGNORECASE
        )
        if match:
            filename = match.group(1).strip('"')
        else:
            match = re.search(
                r"filename\s*=\s*\"?([^\";\r\n]+)\"?",
                content_disposition,
                re.IGNORECASE,
            )
            if match:
                filename = match.group(1).strip('"')
            else:
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename.endswith(".pdf"):
                    filename += ".pdf"

        # Sanitize filename
        name_part, ext = os.path.splitext(filename)
        name_part = name_part.lower()
        name_part = re.sub(r"[^a-z0-9]", "_", name_part)  # Replace non a-z0-9 with _
        name_part = re.sub(r"_+", "_", name_part)  # Collapse multiple __ to _
        name_part = name_part.strip("_")  # Remove leading/trailing _
        filename = f"{name_part}{ext.lower()}"  # Final filename

        # Directory setup
        os.makedirs(download_dir, exist_ok=True)
        file_path = os.path.join(download_dir, filename)

        if os.path.exists(file_path):
            print(f"⚠️ File already exists: {filename}")
            return

        # Write file
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"✅ Downloaded: {filename}")

    except requests.exceptions.RequestException as error:
        print(f"❌ Request failed: {error}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def main() -> None:
    # The remote URL Location
    remote_url: list[str] = [
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=204459&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=204476&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=204478&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=204470&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=131881&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=204465&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=131882&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=450531&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=204462&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=169252&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=169253&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=169250&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=169254&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=169251&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=286143&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=131879&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=131876&ft=1",
        "https://www.revbase.com/TagTeam/link.asp?id=E8CA47",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=204460&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=1791539&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=286141&ft=1",
        "https://www.quincycompressor.com/wp-content/uploads/2012/01/qsorb.pdf",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&dataid=204471&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=286142&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=2100877&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=521786&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=286142&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=5154021&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=482730&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=286142&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=5344686&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=286142&ft=1",
        "https://www.revbase.com/tt/sl.ashx?z=12b3cd59&DataID=9034787&ft=1",
    ]
    # Target directory
    download_dir = "PDFs"

    # Loop over the URLs and download them
    for url in remote_url:
        download_pdf(url, download_dir=download_dir)


main()
