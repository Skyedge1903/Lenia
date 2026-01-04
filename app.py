import time
import os
import cv2
import numpy as np
import flask
import matplotlib as plt

# =====================================================
# PARAMÈTRES
# =====================================================
N = M = 350
dt = np.float32(0.1)

FPS = 60
JPEG_QUALITY = 90

INIT_IMAGE = "lenia_save.png"

mu = np.array([0.156, 0.193, 0.342], dtype=np.float32)
sigma = np.array([0.0118, 0.049, 0.0891], dtype=np.float32)

# =====================================================
# OUTILS
# =====================================================
def random_grid():
    return np.random.rand(N, M).astype(np.float32)

def load_grid():
    if not os.path.exists(INIT_IMAGE):
        raise FileNotFoundError("Image initiale absente")
    img = cv2.imread(INIT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None or img.shape != (N, M):
        raise ValueError("Image invalide (350x350)")
    return img.astype(np.float32) / 255.0

def gauss(x, mu, sigma):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2, dtype=np.float32)

# =====================================================
# KERNELS FFT
# =====================================================
def build_kernels(R):
    bs = [
        [1, 5/12, 2/3],
        [1/12, 1],
        [1]
    ]

    y, x = np.ogrid[-N//2:N//2, -M//2:M//2]
    dist = np.sqrt(x*x + y*y).astype(np.float32)

    fKs = []

    for b in bs:
        K = np.zeros((N, M), np.float32)
        d = dist / R * len(b)

        for i, bi in enumerate(b):
            mask = (d.astype(np.int32) == i)
            K[mask] += bi * np.exp(
                -0.5 * ((d[mask] % 1 - 0.5) / 0.15) ** 2
            )

        K /= K.sum()
        fKs.append(np.fft.fft2(np.fft.fftshift(K)))

    return fKs

# =====================================================
# LENIA
# =====================================================
def evolve(X, FX, fKs):
    FX[:] = np.fft.fft2(X)
    G = 0.0

    for i in range(3):
        U = np.fft.ifft2(FX * fKs[i]).real
        G += 2 * gauss(U, mu[i], sigma[i]) - 1

    X += dt * (G / 3.0)
    np.clip(X, 0, 1, out=X)

# =====================================================
# COLORMAP
# =====================================================
def make_lut():
    cmap = plt.colormaps.get_cmap("nipy_spectral")
    return (cmap(np.arange(256))[:, :3] * 255).astype(np.uint8)

# =====================================================
# FLASK
# =====================================================
app = flask.Flask(__name__)
server = app

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Lenia</title>
<style>
html, body {{
    margin: 0;
    background: black;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}}
canvas {{
    background: black;
}}
</style>
</head>
<body>
<canvas id="c" width="1000" height="1000"></canvas>
<img id="src" src="{stream_url}" style="display:none">

<script>
const W = 350;
const H = 350;
const SCALE = 1000 / 350;
const canvas = document.getElementById("c");
const ctx = canvas.getContext("2d");
const img = document.getElementById("src");

ctx.imageSmoothingEnabled = false;

const STYLE = "circle"; // "circle" ou "star"

function drawStar(x, y, r, color) {{
    ctx.fillStyle = color;
    ctx.beginPath();
    for (let i = 0; i < 5; i++) {{
        let a = i * 2 * Math.PI / 5;
        ctx.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r);
        a += Math.PI / 5;
        ctx.lineTo(x + Math.cos(a) * r * 0.4, y + Math.sin(a) * r * 0.4);
    }}
    ctx.closePath();
    ctx.fill();
}}

img.onload = () => {{
    const off = document.createElement("canvas");
    off.width = W;
    off.height = H;
    const octx = off.getContext("2d");

    function render() {{
        octx.drawImage(img, 0, 0);
        const data = octx.getImageData(0, 0, W, H).data;

        ctx.clearRect(0, 0, 1000, 1000);

        for (let y = 0; y < H; y++) {{
            for (let x = 0; x < W; x++) {{
                const i = (y * W + x) * 4;
                const r = data[i];
                const g = data[i+1];
                const b = data[i+2];

                if (r + g + b < 5) continue;

                const cx = x * SCALE + SCALE / 2;
                const cy = y * SCALE + SCALE / 2;
                const color = `rgb(${{r}},${{g}},${{b}})`;

                if (STYLE === "circle") {{
                    ctx.fillStyle = color;
                    ctx.beginPath();
                    ctx.arc(cx, cy, SCALE*0.45, 0, Math.PI*2);
                    ctx.fill();
                }} else {{
                    drawStar(cx, cy, SCALE*0.5, color);
                }}
            }}
        }}
        requestAnimationFrame(render);
    }}
    render();
}};
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return HTML_TEMPLATE.format(stream_url="/stream")

@app.route("/random")
def random_page():
    return HTML_TEMPLATE.format(stream_url="/random_stream")

def stream_generator(mode):
    if mode == "random":
        X = random_grid()
        R = 10
    else:
        X = load_grid()
        R = 13

    FX = np.empty((N, M), np.complex64)
    fKs = build_kernels(R)
    lut = make_lut()

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]

    while True:
        t0 = time.time()
        evolve(X, FX, fKs)
        img = lut[(X * 255).astype(np.uint8)]
        _, jpeg = cv2.imencode(".jpg", img, encode_param)

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            jpeg.tobytes() +
            b"\r\n"
        )

        time.sleep(max(0.0, 1/FPS - (time.time() - t0)))

@app.route("/stream")
def stream():
    return flask.Response(
        stream_generator("loaded"),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/random_stream")
def random_stream():
    return flask.Response(
        stream_generator("random"),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# Route pour favicon
@app.route('/favicon.ico')
def favicon():
    try:
        return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
    except FileNotFoundError:
        print("favicon.ico non trouvé")
        return '', 204  # Réponse vide avec statut 204 (No Content)

# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
