# 💵🤖 Kofin - Financial Education & Management Assistant

> An intelligent virtual assistant built with Python, Streamlit, and the Google Gemini API, designed to help beginners organize their personal finances in a straightforward and practical manner.

> 🇧🇷 **Read this in Portuguese:** [README_PT.md](./README_PT.md)

---

## 📌 Overview

**Kofin** is an interactive financial education chatbot created to simplify personal finance management. It analyzes user financial profiles (or simulated data) to offer tailored guidance using the **50/30/20 rule**, calculates emergency fund targets, and integrates real-time economic indicators—such as Brazil's official interest rate (**Selic Rate**) fetched via Central Bank REST APIs.

---

## 🛠️ Tech Stack

* **Language:** [Python 3.10+](https://www.python.org/)
* **Web Framework:** [Streamlit](https://streamlit.io/)
* **AI Model:** Google Gemini API (`google-genai` SDK)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
* **API Integration:** [Requests](https://requests.readthedocs.io/)
* **Version Control:** Git & GitHub

---

## ⚙️ Key Features

* **Custom or Simulated Financial Profiles:** Users can manually input income and expenses via the sidebar or switch to pre-configured profiles for quick testing.
* **Central Bank API Integration:** Automated fetching of updated macroeconomic indicators via the Central Bank of Brazil REST API.
* **Interactive Conversational AI:** Real-time chat guided by custom *System Prompts* engineered to deliver educational, empathetic, and risk-aware advice.
* **Data Security & Secrets Management:** Credentials secured using Streamlit `secrets.toml` and strict `.gitignore` rules.

---

## 📁 Repository Structure

```text
kofin_bot/
├── .streamlit/
│   └── secrets.toml          # API credentials management (ignored in Git)
├── data/
│   └── infos_ed_financeira.md # Markdown financial knowledge base
├── docs/
│   └── documentacao.md        # Agent documentation & prompt engineering specs
├── src/
│   └── app.py                 # Main Streamlit web application source code
├── .gitignore                 # Version control ignore rules
├── README.md                  # Project documentation
└── requirements.txt           # Python dependency manifest

```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher installed.
* Google Gemini API Key (obtained from [Google AI Studio](https://aistudio.google.com/)).

### Installation & Setup

1. **Clone the repository:**

```bash
git clone [https://github.com/MatheusKoppN/dio-lab-bia-do-futuro.git](https://github.com/MatheusKoppN/dio-lab-bia-do-futuro.git)
cd dio-lab-bia-do-futuro

```

2. **Create and activate a virtual environment:**

* **Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\activate

```

* **Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate

```

3. **Install dependencies:**

```bash
pip install -r requirements.txt

```

4. **Configure API Key:**
Create a `.streamlit` folder at the project root and add a `secrets.toml` file:

```toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

```

5. **Run the application:**

```bash
python -m streamlit run src/app.py

```

---

## 📜 License

Distributed under the MIT License. Developed for educational and personal portfolio purposes.

---

## 📬 Contact

**Matheus Kopp do Nascimento**

* **Email:** [matheuskoppn@gmail.com](https://www.google.com/search?q=mailto%3Amatheuskoppn%40gmail.com)
* **LinkedIn:** [linkedin.com/in/matheus-kopp-do-nascimento-426a783b5](https://www.linkedin.com/in/matheus-kopp-do-nascimento-426a783b5/)
* **GitHub:** [github.com/MatheusKoppN](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/MatheusKoppN)
