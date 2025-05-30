async def open_camera(payload):
    # Simulated camera opening logic
    flash = payload.get("flash", "off")
    quality = payload.get("quality", "SD")
    print(f"📷 Opening camera with flash: {flash} and quality: {quality}")
    # Add real logic here, e.g. system calls or device APIs
