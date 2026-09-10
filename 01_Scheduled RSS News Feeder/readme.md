## ✅ Workflow overview

This is a scheduled daily tech-news email pipeline. It:

1. Triggers every weekday at 8:00 AM
2. Fetches an RSS feed from NLM General Announcements
3. Keeps only the first 5 articles
4. Summarizes each article with OpenAI
5. Combines them into a styled HTML email
6. Sends the email to a Gmail address

---

## 🔄 Step-by-step flow

### 1) Every Weekday 8am
- Type: Schedule Trigger
- Cron expression: 0 8 * * 1-5
- Meaning: runs at 8:00 AM on Monday through Friday
- This is the start of the automation

### 2) Fetch Tech News RSS
- Type: RSS Feed Read
- URL:
  https://www.nlm.nih.gov/rss/auto/NLMGeneralAnnouncements.rss
- Purpose: pulls the latest feed items from the source
- Each item contains fields like:
  - title
  - link
  - pubDate
  - contentSnippet / summary / content

### 3) Limit to 5 Articles
- Type: Code node
- Logic:
  - takes the first 5 items from the RSS feed
  - reshapes each item into a cleaner JSON object with:
    - title
    - link
    - pubDate
    - contentSnippet
- This keeps the digest concise and prevents email overload

### 4) Summarize with LLM
- Type: LangChain LLM Chain
- Prompt:
  - “Summarize this news article in 2–3 clear sentences”
  - Uses article title + content snippet
- Model used:
  - GPT-4o-mini
- Purpose:
  - turns long article text into a short, readable summary
- It runs once for each article item automatically

### 5) OpenAI Chat Model
- Type: OpenAI Chat Model
- Connected to the summarization node
- Credential:
  - OpenAI API key attached
- Purpose:
  - provides the actual LLM inference for summaries

### 6) Extract Summary
- Type: Code node
- Logic:
  - reads the LLM output from a few possible fields like output, text, response, message.content, etc.
  - grabs the original article data from the same indexed item
  - returns a clean object with:
    - title
    - link
    - pubDate
    - summary
- This normalizes the result before formatting the email

### 7) Build Email HTML
- Type: Code node
- Purpose:
  - turns all summaries into a formatted HTML email
- It creates:
  - a heading with today’s date
  - one section per article
  - clickable article title links
  - each summary
  - publication date
  - a footer notice showing article count
- Output includes:
  - html
  - article_count
  - date

### 8) Send a message
- Type: Gmail node
- Recipient:
  - Arun’s Gmail address
- Subject:
  - “Tech News Digest - [date] ([count] articles)”
- Message:
  - uses the HTML generated in the previous step
- Purpose:
  - emails the digest to the configured inbox

---

## 📦 Data structure flow

Each article is transformed like this:

- RSS item:
  - title
  - link
  - pubDate
  - contentSnippet

Then becomes:

- processed article:
  - title
  - link
  - pubDate
  - summary

Then becomes:

- email payload:
  - html
  - article_count
  - date

---

## 💡 Important behavior in this workflow

- No loop node was needed.
- n8n automatically processes each RSS item through downstream nodes one-by-one.
- This means the 5 selected articles are each summarized independently, then combined into one email.

---

## ⚙️ What you should check in n8n

- Gmail credentials are valid
- OpenAI credential is connected
- RSS feed is reachable
- The email address is correct
- The schedule is set to the desired timezone and time

---

## 🧠 Summary

This workflow is a “scheduled AI-powered news digest”:
- RSS feed source
- 5-item filter
- OpenAI summarization
- HTML email formatting
- Gmail delivery
