# 🧠 AI-Based Mismatch Analyzer (Car's Dashboard Image Validation)

## 📘 Problem Statement
In the automotive industry, validating dashboard and infotainment display images for multiple vehicle variants is crucial. Each test cycle generates a **Global Test Report** containing thousands of image comparisons between the *Reference (Expected)* and *To-Check (Actual)* images.  
Manual verification of mismatching pairs is time-consuming and error-prone.

The goal of this project is to **automate the semantic and visual comparison** of image pairs to classify them into one of four categories:
- ✅ **OK** – Images match perfectly or with negligible difference  
- ⚠️ **Investigate** – Slight differences detected; human review recommended  
- ❌ **NOK** – Major visual/semantic mismatch detected  
- 🛑 **Faulty** – Missing or dimension-mismatched images

The output is an **AI-Annotated HTML Report** grouping results by status with a clickable summary table and an integrated feedback system.

---

## ⚙️ Approach
The project leverages both **cloud and local AI models** to analyze mismatched image pairs extracted from `globalTestReport.html`.

1. **Input Parsing**  
   - Reads `globalTestReport.html` and extracts mismatched image pairs.  
   - Handles missing images and malformed HTML gracefully.

2. **AI-Based Comparison**  
   - If an API key for **Mistral** is available, sends both images for cloud-based semantic comparison.  
   - If not, falls back to a **local model** using pixel-level, color-difference, and cluster-based analysis.

3. **Super-Resolution Enhancement**  
   - Low-resolution images are enhanced using **Real-ESRGAN** (based on RRDBNet from BasicSR).  
   - This improves small-text or icon visibility before comparison.

4. **Difference Highlighting & Classification**  
   - Uses pixel-wise difference masks and connected component analysis to classify shifts as *global* or *localized*.

5. **Report Generation**  
   - Annotates the original HTML report with:  
     - Highlighted difference images  
     - AI verdicts and status tags  
     - Interactive feedback dropdowns  
     - Summary table with clickable links  
     - KO Check section for failed test conditions

6. **Output**  
   - Generates `aiAnalysisV2Report_<variant>.html` inside the `/output` folder.

---

## 🧩 Folder Structure
```
📦 Project Root
│
├── 📂 input/                    # Contains variant-specific folders with HTML + images
├── 📂 output/                   # AI-annotated HTML reports are saved here
│
├── api_handler.py               # Handles Mistral API requests for cloud-based comparison
├── local_model.py               # Local fallback image analysis model
├── main.ipynb                   # Primary Jupyter notebook orchestrating the workflow
│
├── api_key.txt                  # Stores your Mistral API key (if available)
├── config_path.txt              # Stores variant and directory path templates
├── requirements.txt             # Python dependencies
│
└── pkg_instl_files/             # (Create manually) to store external models like Real-ESRGAN & BasicSR
```

---

## 🧠 Key Libraries and Why They’re Used

| Library | Purpose |
|----------|----------|
| **BeautifulSoup (bs4)** | Parse and modify HTML reports for annotation |
| **OpenCV (cv2)** | Image difference detection, clustering, and mask generation |
| **Pillow (PIL)** | Image handling and compositing |
| **NumPy** | Numerical computations and mask operations |
| **Torch** | Runs Real-ESRGAN and local models |
| **Real-ESRGAN** | Super-resolution enhancement for small or low-quality screenshots |
| **BasicSR** | Provides RRDBNet backbone architecture used by Real-ESRGAN |
| **Requests** | Handles API communication with Mistral cloud model |
| **Mistral API** | Performs semantic-level image difference reasoning when API key is provided |

---

## 🌐 External Libraries to Download Manually

Some dependencies are **not available on PyPI** and must be cloned manually.

1. **Real-ESRGAN**
   ```bash
   git clone https://github.com/xinntao/Real-ESRGAN.git
   ```
   **Model Weights Path:**  
   `Path_to/Real-ESRGAN-master/realesrgan/weights/RealESRGAN_x4plus.pth`

2. **BasicSR v1.4.2**
   ```bash
   git clone -b v1.4.2 https://github.com/xinntao/BasicSR.git
   ```

> ⚠️ After downloading these repositories, update their paths in your code as needed.

---

## 🧭 Instructions to Run the Project

### 1. Clone the Repository
```bash
git clone <your_repo_url>
cd <your_repo_name>
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Also ensure **Real-ESRGAN** and **BasicSR v1.4.2** are manually cloned as described above.

### 3. Configure Paths
Edit `config_path.txt` to set up your variant name and directory structure. Example:
```
variant = Captur_Regression_Tests_globalTestReport
report_path_template = ./input/{variant}/globalTestReport.html
image_dir_template = ./input/{variant}/images
output_dir = ./output
relative_image_path_template = ../input/{variant}/images
```

### 4. (Optional) Add Mistral API Key
Add your API key to `api_key.txt` (keep this file private):
```
sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

If `api_key.txt` is missing or empty, the code automatically falls back to the **local model**.

### 5. Run the Notebook
Open `main.ipynb` in Jupyter Notebook or VSCode and run all cells.

### 6. Output
- The annotated HTML report will be saved inside `/output` as:  
  `aiAnalysisV2Report_<variant>.html`
- Open it in your browser to explore:
  - **Clickable summary table**
  - **Grouped status sections**
  - **KO checks**
  - **Interactive feedback panel**

---

## 💾 Example Output
- `aiAnalysisV2Report_Captur.html`
- `/output/img/` → Difference-highlighted images

---

## 🚀 Future Improvements
- Integrate multilingual OCR-based checks using PaddleOCR  
- Add CLIP-based local semantic comparison  
- Enable cloud-based batch parallelization for large test suites  
- Add web dashboard view for analytics

---

## 👨‍💻 Author
**Kanishk Mishra**  
*Former* AI Intern @ RNTBCI  
Focused on visual difference detection and semantic validation in automotive test automation.

