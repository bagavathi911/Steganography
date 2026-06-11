import numpy as np
import cv2

DELIMITER = "<<END>>"

# ---------------- PASSWORD ENCODE / DECODE ----------------
def encode_msg(message, password):
    return password + "::" + message + DELIMITER

def decode_msg(data, password):
    if "::" in data:
        pw, msg_with_delim = data.split("::", 1)
        if pw == password and DELIMITER in msg_with_delim:
            msg = msg_with_delim.split(DELIMITER)[0]
            return msg
    return None

# ---------------- BIT CONVERSIONS ----------------
def message_to_bits(msg):
    return ''.join(format(ord(c), '08b') for c in msg)

def bits_to_message(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
        if ''.join(chars).endswith(DELIMITER):
            break
    return ''.join(chars)

# ---------------- SAFE PIXEL SELECTION ----------------
def get_safe_pixel_indices(image: np.ndarray) -> np.ndarray:
    """
    Deterministic safe pixel selection.
    Independent of embedded data.
    """
    img = image.astype(np.uint8)
    img_clean = img & 0xFE
    gray = cv2.cvtColor(img_clean, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 120, 250)
    edges_norm = edges / 255.0

    # Local variance
    kernel = np.ones((3, 3), np.float32) / 9
    gray_f = gray.astype(np.float32)
    mean = cv2.filter2D(gray_f, -1, kernel)
    variance = cv2.filter2D((gray_f - mean) ** 2, -1, kernel)
    variance_norm = cv2.normalize(variance, None, 0, 1, cv2.NORM_MINMAX)

    # Entropy map
    def entropy(block):
        hist = np.histogram(block, bins=256, range=(0, 255))[0]
        prob = hist / np.sum(hist)
        prob = prob[prob > 0]
        return -np.sum(prob * np.log2(prob))

    block_size = 8
    entropy_map = np.zeros_like(gray_f)

    for i in range(0, gray.shape[0], block_size):
        for j in range(0, gray.shape[1], block_size):
            block = gray[i:i+block_size, j:j+block_size]
            h, w = block.shape
            entropy_map[i:i+h, j:j+w] = entropy(block)

    entropy_norm = cv2.normalize(entropy_map, None, 0, 1, cv2.NORM_MINMAX)

    # Weighted security score
    security_score = (
        0.5 * edges_norm +
        0.3 * variance_norm +
        0.2 * entropy_norm
    )

    threshold = 0.6
    safe_mask = security_score > threshold

    return np.where(safe_mask.flatten())[0]

# ---------------- CAPACITY CALCULATION ----------------
def calculate_capacity(image: np.ndarray, password: str):
    safe_indices = get_safe_pixel_indices(image)

    total_bits = len(safe_indices) * 3  # RGB channels

    overhead_str = password + "::" + DELIMITER
    overhead_bits = len(overhead_str) * 8

    usable_bits = max(0, total_bits - overhead_bits)
    max_chars = usable_bits // 8

    return {
        "safe_pixels": len(safe_indices),
        "total_bits": total_bits,
        "usable_bits": usable_bits,
        "max_chars": max_chars
    }

# ---------------- HIDE MESSAGE ----------------
def hide_message(image: np.ndarray, message: str, password: str) -> np.ndarray:
    data = image.copy()
    flat_pixels = data.reshape(-1, 3)

    safe_indices = get_safe_pixel_indices(image)
    full_message = encode_msg(message, password)
    bits = message_to_bits(full_message)

    if len(bits) > len(safe_indices) * 3:
        raise ValueError("Message too large for this image.")

    bit_idx = 0
    for idx in safe_indices:
        for channel in range(3):
            if bit_idx < len(bits):
                flat_pixels[idx][channel] = (
                    flat_pixels[idx][channel] & 0xFE
                ) | int(bits[bit_idx])
                bit_idx += 1

    return flat_pixels.reshape(data.shape)

# ---------------- REVEAL MESSAGE ----------------
def reveal_message(image: np.ndarray, password: str) -> str:
    data = image.copy()
    flat_pixels = data.reshape(-1, 3)

    safe_indices = get_safe_pixel_indices(image)

    bits = ""
    for idx in safe_indices:
        for channel in range(3):
            bits += str(flat_pixels[idx][channel] & 1)

    raw_message = bits_to_message(bits)
    return decode_msg(raw_message, password)
