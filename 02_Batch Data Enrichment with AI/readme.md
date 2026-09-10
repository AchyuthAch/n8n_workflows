## ✅ Workflow breakdown

This workflow is a batch company enrichment pipeline powered by AI. It takes a list of companies, asks OpenAI to infer business details, merges the results back into each record, and emails a final report.

---

## 🔄 End-to-end flow

### 1) Manual Trigger
- Type: Manual Trigger
- Purpose: starts the workflow when you click “Test workflow”
- This is a one-off trigger instead of a scheduled or webhook-based trigger

### 2) Sample Company List
- Type: Code node
- It creates a list of companies with:
  - name
  - website
  - founded year

Example companies included:
- Stripe
- Notion
- Vercel
- Supabase
- Hugging Face

The node returns each company as a separate item in JSON form, so the LLM node can process them individually.

### 3) Enrich Company with AI
- Type: LangChain LLM Chain
- Purpose: sends each company record to GPT-3.5-turbo
- Prompt includes:
  - company name
  - website
  - founded year

It asks the model to return JSON with:
- description
- industry
- likely_tech_stack
- business_model
- estimated_employees

Important detail:
- The prompt explicitly says “Return ONLY valid JSON. No markdown.”
- That is done so the next node can parse the output reliably

### 4) OpenAI Chat Model
- Type: OpenAI Chat Model
- This is the actual language model connection
- Model used: gpt-3.5-turbo
- It is connected to the LLM Chain through the ai_languageModel connection

### 5) Extract Enrichment
- Type: Code node
- Purpose: cleans and parses the model output and merges it with the original company data
- Logic:
  - reads the LLM output from fields such as output, text, response, message.content, or content
  - strips markdown code fences if present
  - JSON.parse() to convert the text into an object
  - if parsing fails, it stores an error object instead
  - merges each company’s original fields with the AI-enriched fields
  - adds enriched_at timestamp

Final output shape per company:
- name
- website
- founded
- description
- industry
- likely_tech_stack
- business_model
- estimated_employees
- enriched_at

### 6) Compile Final Report
- Type: Code node
- Purpose: combines all processed company results into one final JSON report
- Output includes:
  - total_companies
  - processed_at
  - companies array

This is where the workflow prepares a single final object for email delivery

### 7) Send a message
- Type: Gmail node
- Recipient:
  - [arunachaleswara369@gmail.com](mailto:arunachaleswara369@gmail.com)
- Subject:
  - “Reg: Company Info for [X] Companies”
- Email body:
  - a styled HTML table/section for each company
  - includes:
    - website
    - industry
    - founded year
    - employee range
    - business model
    - description
    - tech stack badges

This turns the structured JSON into a readable analyst-style report

---

## 📦 What the AI generates per company

For each company, the model tries to infer:
- description: what the company does
- industry: e.g. FinTech, DevTools, AI/ML
- likely_tech_stack: 3–5 technologies likely used
- business_model: B2B, B2C, B2B2C, Marketplace
- estimated_employees: range such as 100-500 or 1000-5000

This is basically AI-powered enrichment from minimal input data.

---

## 🔍 Why this workflow is useful

This pattern is commonly used for:
- lead enrichment
- CRM data prep
- market research
- startup/company profiling
- internal reporting

It is useful because you can feed in a list of names/websites and get structured business intelligence automatically.

---

## 💡 Key technical design feature

The important part is that the workflow processes all items in the company list automatically:
- It doesn’t need a manual loop
- n8n handles each item through the LLM chain one by one
- Then the final step aggregates everything into one report

That is exactly why this is called a “batch” workflow.

---

## 🧠 In plain English

This workflow says:

“Take a list of companies, ask AI to enrich each one with what it likely does and how it operates, then send me a polished summary email.”