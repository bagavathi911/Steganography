# Intelligent Pixel Selection Steganography

A robust Flask-based web application designed to hide confidential text messages within digital images. This system elevates traditional steganography by incorporating heuristic, rule-based adaptive pixel selection—utilizing edge detection, variance, and entropy analysis—alongside password protection to ensure data remains both invisible and secure.

---

## Project Objectives

* **Secure Embedding:** Conceal secret messages within images using advanced LSB techniques.
* **Authentication:** Protect hidden data via password-based encryption and decryption.
* **Visual Fidelity:** Minimize image distortion by selecting the most complex pixels that naturally mask changes.
* **Accessibility:** Provide an intuitive, user-friendly web interface for users.

---

## Key Features

* **Heuristic AI Pixel Selection:** Uses weighted scoring to identify the safest pixels for data embedding.
* **LSB Steganography:** Utilizes the Least Significant Bit of pixel values for minimal visual impact.
* **Password Protection:** Ensures only authorized users with the correct key can extract the hidden message.
* **Security Analytics:** Displays image capacity and security-related statistics in real-time.
* **Cross-Platform:** Runs on any modern web browser via a Python Flask backend.

---

## Heuristic AI Approach

Instead of traditional linear embedding, this project employs a rule-based AI approach to enhance security. The system relies on expert-defined metrics to make intelligent decisions about where to hide data.

### Decision Strategy

The system computes a security score for each pixel based on:

1. **Edge Detection:** Identifies high-frequency regions where changes are less noticeable to the human eye.
2. **Local Variance Analysis:** Detects textured areas that can absorb noise better than flat, smooth areas.
3. **Entropy Measurement:** Evaluates the randomness within image regions using Shannon Entropy.

> Only pixels exceeding a predefined threshold are selected for embedding, ensuring the stego-image remains indistinguishable from the original.

---

## Technologies Used

| Category | Tools / Techniques |
| --- | --- |
| **Backend** | Python 3.x, Flask |
| **Image Processing** | OpenCV, NumPy |
| **Frontend** | HTML5, CSS3, JavaScript |
| **AI Technique** | Heuristic, Rule-Based Decision System |
| **Algorithms** | LSB Steganography, Canny Edge Detection, Shannon Entropy |

---

## Project Structure


Sem-project/
├── app.py                # Main Flask application & routing
├── stegano_utils.py      # Core steganography and heuristic AI logic
├── requirements.txt      # Project dependencies
└── templates/
    ├── index.html        # Homepage
    ├── encrypt.html      # Message embedding interface
    └── decrypt.html      # Message extraction interface
    

## Usage

### 1. Encryption

* **Upload** a carrier image (PNG or BMP is recommended to avoid compression loss).
* **Enter** your secret message.
* **Set** a security password.
* **Download** the generated stego-image.

### 2. Decryption

* **Upload** the stego-image.
* **Enter** the correct password used during encryption.
* **Retrieve** your hidden message.

---

## Limitations and Notes

* **Capacity:** The amount of text you can hide is limited by the image dimensions and the number of safe (high-complexity) pixels identified.
* **Lossless Formats:** Always use PNG or BMP. JPEG compression uses lossy algorithms that will destroy the bits where your message is hidden.
* **Text Only:** The current version is optimized specifically for UTF-8 text strings.

