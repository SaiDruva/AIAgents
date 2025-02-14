# Voice-to-JIRA Ticket Agent

This agent captures your voice, transcribes it, uses OpenAI (via LangChain) to generate JIRA ticket details, and creates a ticket in JIRA.

## Features

- Real-time voice transcription
- Natural language processing to extract ticket details
- Automated JIRA ticket creation using Atlassian Document Format

## Prerequisites

- Python 3.7+
- An OpenAI API key
- JIRA account credentials

## Setup

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
