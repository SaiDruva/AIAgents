# Voice-to-JIRA Ticket AI Agent

This project is an AI Agent that creates JIRA tickets by capturing your voice, transcribing it, and processing the transcription using OpenAI to generate ticket details. The ticket is then created in JIRA via its REST API.

## Overview

The solution consists of three main components:
1. **Voice Transcription Agent:** Listens to your voice and converts it to text using Python's SpeechRecognition library.
2. **JIRA Details Generator Agent:** Uses LangChain with OpenAI (via the `langchain-openai` package) to generate a concise ticket title and detailed description.
3. **JIRA Ticket Creator Agent:** Creates a JIRA ticket using the generated details and JIRA's REST API, with the description formatted according to the Atlassian Document Format (ADF).

## Features

- **Real-time voice transcription:** Converts your spoken words into text.
- **Natural language processing:** Utilizes OpenAI's API to extract structured ticket details.
- **Automated JIRA integration:** Creates tickets in JIRA with proper formatting.
- **Modular design:** Easily extendable to add more features or integrations.

## Prerequisites

- Python 3.7 or later
- An OpenAI API key (set as an environment variable or in the code)
- JIRA account and API token with permissions to create tickets
- A JIRA instance (cloud or server) with API access

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/your-repository-name.git
   cd your-repository-name
