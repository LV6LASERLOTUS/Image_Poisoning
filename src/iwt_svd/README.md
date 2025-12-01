# IWT–SVD Watermarking (Minimal Reproduction)

This folder/notebook contains a minimal, notebook-first reproduction of an **IWT–SVD** watermarking pipeline, aligned with the paper’s idea of using a **2-level integer wavelet transform (5/3 lifting)** and embedding in the **HH₂** subband.

We focus on getting a clean, auditable end-to-end run:
**cover → embed → stego → extract → metrics + evidence images**.

---

## What we implemented

### Core method
- **2-level Integer Wavelet Transform (IWT), 5/3 lifting**
- **SVD watermark embedding in HH₂**
- A stable variant: **quadrant-SVD on HH₂**
  - HH₂ is split into 4 quadrants (spatial blocks)
  - each quadrant uses its own SVD
  - we embed only **top-k** singular values (stable indexing)

### Why quadrant-SVD
Directly embedding multiple blocks into disjoint *segments* of one singular-value vector can break extraction because SVD returns singular values **sorted by magnitude**, so indices can shift between embed/extract. Quadrant-SVD avoids that by keeping each quadrant’s SVD independent and index-stable.

---

## Configuration (reproduction settings)

- **Method:** 2-level IWT (5/3 lifting) + HH₂ quadrant-SVD
- **Parameters:** `alpha = 0.01`, `k = 32`
- **Cover image:** `512×512`, grayscale `uint8`
- **Watermark image:** `256×256`, grayscale `uint8`
  - internal working size is `128×128` (because HH₂ is `128×128` in a 2-level decomposition)

### Validation points we checked
- **IWT reversibility:** exact reconstruction (PSNR = inf)
- **Extraction quality at 128×128:** `NCC(128) ≈ 0.9998` (near-perfect)
- **256×256 NCC upper bound:** because embedding is on HH₂ (128×128), the recovered watermark at 256×256 is limited by resizing loss.
  - We computed a baseline: `NCC(wm256, resize(256→128→256)) ≈ 0.7405`
  - The extracted watermark at 256×256 matches this ceiling (≈ 0.74), as expected.

---

## Dataset (for cover images)

We used **HFO-5000 (Human Faces and Objects Dataset)** to sample cover images:
- 1500 male faces
- 1500 female faces
- 2000 objects
- Includes a CSV manifest with file paths/labels

In the notebook, we sample a small set of images into a local `samples/` directory and write a `manifest.csv`.

---

## Outputs / Evidence

All evidence files are saved under:

`samples/_previews/`

Key deliverables:
- `evidence_cover_512.png` — cover image
- `evidence_stego_512.png` — stego image (after embedding)
- `evidence_wm_hat_128.png` — extracted watermark at 128×128
- `evidence_wm_hat_256.png` — extracted watermark upsampled to 256×256
- `evidence_wm256_baseline.png` — baseline (256→128→256) for the NCC upper-bound argument
- (optional) panel images, if generated:
  - `evidence_panel_v4.png`
  - `evidence_panel_wm256_upperbound.png`

---

## How to run (notebook workflow)

1. **Load utilities / metrics**
   - Grayscale I/O, PSNR / SSIM / NCC

2. **Data sampling**
   - Read HFO-5000 CSV
   - Write a small `samples/manifest.csv`
   - Copy a few face/object images into `samples/`

3. **Single-image reproduction**
   - Pick one cover image (512×512)
   - Pick one watermark image (256×256)
   - Run: embed → extract
   - Compute metrics (PSNR/SSIM on cover; NCC on watermark)

4. **Save evidence images**
   - Save the 3 required evidence images + the baseline reference

---

## Notes for collaboration

- This reproduction validates the IWT–SVD component independently.
- Another group member is responsible for CMUA/FOUND.
- After both pipelines are stable, the team should agree on a shared evaluation protocol:
  - same cover sets
  - same attacks (JPEG, noise, blur, etc.)
  - same metrics + reporting format

---

## Dependencies

Typical environment (not strict):
- Python 3.x
- numpy
- opencv-python (cv2)
- scikit-image (for PSNR/SSIM)
- matplotlib (optional, for panels)
- pandas (for manifest)

---

## File naming (recommended)

- Notebook: `iwt_svd_minimal_repro.ipynb`
- Evidence directory: `samples/_previews/`

---

## Status

✅ IWT (5/3) is reversible  
✅ IWT–SVD embedding/extraction on HH₂ works  
✅ Quadrant-SVD variant yields near-perfect `NCC(128)`  
✅ Evidence images exported for reproducible review