## ✅ Workflow details

This workflow is a webhook-based webpage analyzer that accepts a URL, fetches the page content, strips HTML, sends the cleaned text to OpenAI, and returns a structured JSON analysis.

---

## 🔄 Step-by-step flow

### 1) Webhook
- Type: Webhook
- HTTP method: POST
- Path: analyze
- Response mode: responseNode
- Purpose: receives a request like:
  - POST http://localhost:5678/webhook/analyze
  - with JSON body like:
    { "url": "https://en.wikipedia.org/wiki/Artificial_intelligence" }

This is the entry point for the workflow.

### 2) Set Target URL
- Type: Set
- Takes the incoming URL from:
  - $json.body.url
- Stores it as:
  - target_url
- This makes the value easier to reuse later in the workflow

### 3) Fetch Webpage
- Type: HTTP Request
- URL:
  - ={{ $json.target_url }}
- Uses custom headers:
  - User-Agent
  - Accept
  - Accept-Language
- Why this matters:
  - many sites block requests without a browser-like User-Agent header
  - this helps avoid scraping issues

It fetches the raw HTML from the page.

### 4) Strip HTML to Text
- Type: Code node
- It takes the HTML response and removes:
  - script tags
  - style tags
  - HTML tags
  - HTML entities like &nbsp;, &amp;, etc.
  - extra whitespace
- It then truncates the content to 3000 characters

Output fields:
- page_text
- source_url
- char_count

This is important because:
- the LLM has token limits
- long webpage content can be bulky and expensive

### 5) Analyze with LLM
- Type: LangChain LLM Chain
- Prompt instructs the model to analyze the webpage and return a JSON object with:
  - topic
  - summary
  - key_points
  - sentiment
  - reading_time_minutes

Prompt structure:
- source URL
- content text
- strict instruction: “Return ONLY valid JSON, no markdown, no explanation.”

This is where AI performs semantic analysis.

### 6) OpenAI Chat Model
- Type: OpenAI Chat Model
- Model used: gpt-3.5-turbo
- Settings:
  - maxTokens: 800
  - temperature: 0.2
- Purpose: generates the structured analysis result from the scraped text

### 7) Parse JSON Output
- Type: Code node
- Handles the LLM output:
  - tries several possible output keys:
    - output
    - text
    - response
    - message.content
    - content
  - strips markdown fences if present
  - parses the result as JSON using JSON.parse()
  - if parsing fails, it returns an error payload

Output:
- source_url
- analysis
- analyzed_at

This is a safety step to make the result consistent and usable.

### 8) Return Analysis
- Type: Respond to Webhook
- Response mode: JSON
- It returns the results to the caller as a JSON response

This is the final output of the workflow.

---

## 📦 Example output shape

The final response is structured like:

{
  "source_url": "...",
  "analysis": {
    "topic": "Artificial intelligence",
    "summary": "3 sentence summary",
    "key_points": ["...", "...", "..."],
    "sentiment": "neutral",
    "reading_time_minutes": 5
  },
  "analyzed_at": "2026-09-10T..."
}

---

## 🔍 What this workflow is actually doing

It is a content analysis microservice:

- Accepts a URL
- Downloads the webpage
- Cleans the text
- Summarizes it
- Extracts key points
- Detects sentiment
- Estimates reading time
- Returns structured JSON

This is useful for:
- content summarization
- article analysis
- SEO content review
- research automation
- AI-based web scraping tools

---

## ⚠️ Important notes

- Some sites block requests without a browser-like User-Agent
- The workflow only takes the first 3000 characters of the page text to keep calls compact
- It expects valid JSON from the model and has a parse fallback

---

## 🧠 In plain English

This workflow acts like a mini “AI web content analyzer”:
- give it a webpage URL
- it fetches the page
- removes noise
- asks GPT to understand it
- returns a clean summary and structure