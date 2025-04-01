# PaulGrahamAI

PaulGrahamAI is a project designed to scrape, preprocess, and analyze Paul Graham's essays, Twitter posts, and Hacker News discussions to fine-tune an AI model. The project includes data collection, cleaning, training, and deployment components, making it a comprehensive pipeline for working with textual AI models.

---

## 📂 Project Structure

```
PaulGrahamAI
│── 📂 data
│   ├── essays.json          # ✅ Scraped essays
│   ├── twitter.json         # ⏳ In Progress
│   ├── hackernews.json      # 🚀 Future
│
│── 📂 scraping
│   ├── scrape_essays.py     # ✅ Done
│   ├── scrape_twitter.py    # ⏳ Using snscrape
│   ├── scrape_hn.py         # 🚀 Future
│
│── 📂 preprocessing
│   ├── clean_text.py        # Cleans raw data
│   ├── format_data.py       # Converts to structured JSON
│
│── 📂 training
│   ├── fine_tune_gpt.py     # AI training script
│   ├── model_evaluation.py  # Tests AI accuracy
│
│── 📂 deployment
│   ├── web_ui.py            # Flask / FastAPI web app
│   ├── slack_bot.py         # Slack bot integration
│
│── requirements.txt         # All dependencies
│── README.md                # Project documentation
```

---

## 🚀 Features

- **Scraping:** Extract essays, tweets, and Hacker News posts related to Paul Graham.
- **Preprocessing:** Clean and format the scraped text for AI training.
- **Fine-Tuning:** Train an AI model using GPT on the collected data.
- **Evaluation:** Assess the model’s performance on various NLP tasks.
- **Deployment:** Integrate the model into a web UI and Slack bot for easy interaction.

---

## 📥 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/PaulGrahamAI.git
cd PaulGrahamAI
```

### 2️⃣ Install dependencies

Ensure you have Python 3.7+ installed, then run:

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables (if needed)

If any API keys are required (e.g., Slack, OpenAI API), create a `.env` file:

```bash
OPENAI_API_KEY=your_api_key
SLACK_BOT_TOKEN=your_token
```

---

## 🔄 Usage

### Scraping Data

- **Essays:**

```bash
python scraping/scrape_essays.py
```

- **Twitter:**

```bash
python scraping/scrape_twitter.py
```

- **Hacker News:** _(Future implementation)_

```bash
python scraping/scrape_hn.py
```

### Preprocessing Data

```bash
python preprocessing/clean_text.py
python preprocessing/format_data.py
```

### Training the AI Model

```bash
python training/fine_tune_gpt.py
```

### Evaluating the Model

```bash
python training/model_evaluation.py
```

### Deploying the AI Model

- **Web UI (FastAPI)**

```bash
uvicorn deployment.web_ui:app --host 0.0.0.0 --port 8000
```

- **Slack Bot Integration**

```bash
python deployment/slack_bot.py
```

---

## 📚 Dependencies

The project uses the following Python libraries:

```plaintext
snscrape
pandas
requests
beautifulsoup4
tqdm
transformers
fastapi
uvicorn
slack_sdk
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a Pull Request

---

## 📬 Contact

For any questions or suggestions, reach out via email or create an issue in the repository.

Happy coding! 🚀
