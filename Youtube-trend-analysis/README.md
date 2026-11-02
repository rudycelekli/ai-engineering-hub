# YouTube Trend Analysis with CrewAI and BrightData

This project implements a YouTube Trend Analysis with CrewAI and BrightData.
- [Bright Data](https://brdta.com/dailydoseofds) is used to scrape YouTube videos.
- CrewAI is used to analyze the transcripts of the videos and generate a summary.
- Streamlit is used to create a web interface for the project.


---
## Setup and installations

**Get BrightData API Key**:
- Go to [Bright Data](https://brdta.com/dailydoseofds) and sign up for an account.
- Once you have an account, go to the API Key page and copy your API key.
- Paste your API key by creating a `.env` file as follows:

```
BRIGHT_DATA_API_KEY=your_api_key
OPENAI_API_KEY=your_openai_api_key
```

The agents run on OpenAI `gpt-4o` by default (see `load_llm()` in `app.py`), so `OPENAI_API_KEY` is required.

**Setup Ollama (optional, to run locally instead of OpenAI)**:
   To use a local model, set up Ollama as below and switch `load_llm()` in `app.py` to the commented-out `ollama/llama3.2` LLM.
   ```bash
   # setup ollama on linux 
   curl -fsSL https://ollama.com/install.sh | sh
   # pull llama 3.2 model
   ollama pull llama3.2 
   ```


**Install Dependencies**:
   Ensure you have Python 3.11 or later installed.
   ```bash
   pip install streamlit ollama crewai crewai-tools
   ```

---

## Run the project

Finally, run the project by running the following command:

```bash
streamlit run app.py
```



---

## 📬 Stay Updated with Our Newsletter!
**Get a FREE Data Science eBook** 📖 with 150+ essential lessons in Data Science when you subscribe to our newsletter! Stay in the loop with the latest tutorials, insights, and exclusive resources. [Subscribe now!](https://join.dailydoseofds.com)

[![Daily Dose of Data Science Newsletter](https://github.com/patchy631/ai-engineering/blob/main/resources/join_ddods.png)](https://join.dailydoseofds.com)

---

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.
