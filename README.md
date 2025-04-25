
# 🛡️ Insurance Policy Information Chatbot

An AI-powered chatbot built with **Streamlit** that provides instant responses to user queries about various insurance policies. It supports **Health**, **Life**, **Auto**, and **Home** insurance types using a simple yet effective **rule-based NLP engine**.

This project aims to automate customer support interactions, reduce wait times, and enhance user satisfaction by providing fast and reliable information about premiums, coverage, claims, and deductibles.



## 💡 Features

- ✅ Supports 4 types of insurance queries:
  - Health Insurance 🏥
  - Life Insurance 👨‍👩‍👧‍👦
  - Auto Insurance 🚗
  - Home Insurance 🏡
- ✅ Responds to user questions related to:
  - Premiums
  - Coverage
  - Claims
  - Deductibles
- ✅ Escalation message for contacting a human agent
- ✅ Modular codebase (future support for LLMs/embeddings)
- ✅ Clean, interactive UI with background image
- ✅ Works offline (no external APIs required)

---

## 🏗️ Architecture

```text
User Input (Streamlit Chat UI)
        ↓
Session State Handler
        ↓
Intent & Insurance Type Classifier
        ↓
Rule-Based Response Engine
        ↓
Relevant Information Retrieved from Tagged Document Chunks
        ↓
Response Displayed in Chat UI
```

---

## ⚙️ Tech Stack

| Layer            | Tool/Framework         |
|------------------|------------------------|
| Frontend         | Streamlit              |
| Backend Logic    | Python + Rule-based NLP|
| Document Handling| Custom Parser (`.txt`) |
| Future Ready     | LLM + Langchain Ready  |
| UI               | CSS for Chat + Styling |

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Manu270/Insurance-chatbot.git
   cd Insurance-chatbot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

## 💬 How It Works

- The app loads pre-written `.txt` documents with information about different insurance policies.
- When the user types a query, the system:
  1. Detects the insurance type (e.g., Health, Life)
  2. Identifies the intent (e.g., premium, claim)
  3. Returns the most relevant text snippet
- A fallback response is shown for unsupported queries or escalation to a human agent.


## 📈 Future Enhancements

- 🔍 Integration with GPT-4 or vector-based document retrieval
- 🌐 Multilingual support
- 📱 Responsive layout for mobile devices
- 📂 Admin dashboard to upload custom policy documents

https://docs.google.com/presentation/d/1ucCyOMFzew9A-YJnDG8Pw_EHXfl8ELGa/edit?usp=sharing&ouid=113937723499997475790&rtpof=true&sd=true
https://drive.google.com/file/d/1HjgNPT52vnMP9HTI-pSqFKnQ_-UAJdtj/view?usp=sharing

