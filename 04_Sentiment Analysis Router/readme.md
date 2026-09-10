## ✅ Workflow details

This workflow is an AI-powered sentiment router. It receives customer text through a webhook, classifies the sentiment with ChatGPT, parses the result, routes it into one of three branches, and returns a final response with the appropriate action.

---

## 🔄 End-to-end flow

### 1) Webhook
- Type: Webhook
- Method: POST
- Path: sentiment
- Purpose: accepts a payload like:
  - text
  - context

Example:
{
  "text": "I absolutely love this product, it changed my life!",
  "context": "product review"
}

This is the entry point for the workflow.

### 2) Classify Sentiment
- Type: LangChain LLM Chain
- Input:
  - context
  - text
- Prompt asks the model to return only valid JSON with:
  - sentiment: positive / neutral / negative
  - confidence: float from 0.0 to 1.0
  - emotions: array up to 3 emotions
  - reason: one sentence explanation

This is the main AI classification step.

### 3) OpenAI Chat Model
- Type: OpenAI Chat Model
- Model used: gpt-3.5-turbo
- Settings:
  - maxTokens: 300
  - temperature: 0.1
- Purpose: performs the actual sentiment classification

### 4) Parse Classification
- Type: Code node
- It extracts the model output from various possible fields:
  - output
  - text
  - response
  - message.content
  - content
- It removes code fences if present
- It JSON.parse()s the result
- If parsing fails, it falls back to a neutral default:
  - sentiment: neutral
  - confidence: 0.5
  - emotions: []
  - reason: "Parse error"

It also adds:
- original_text
- analyzed_at

This ensures downstream routing still works even if the model output is messy.

### 5) Route by Sentiment
- Type: Switch node
- Checks the value of $json.sentiment
- Splits into three routes:
  - positive
  - neutral
  - negative

This is the decision logic of the workflow.

### 6) Handle Positive
- Type: Set node
- Adds fields:
  - action = escalate_to_success_team
  - priority = low
  - message = “Great feedback! Consider requesting a testimonial.”

This branch handles positive feedback.

### 7) Handle Neutral
- Type: Set node
- Adds fields:
  - action = log_for_review
  - priority = low
  - message = “Neutral feedback logged. No immediate action required.”

This branch handles neutral feedback.

### 8) Handle Negative
- Type: Set node
- Adds fields:
  - action = alert_support_team
  - priority = high
  - message = “Negative feedback detected! Requires immediate follow-up.”

This branch handles bad reviews or complaints.

### 9) Respond to Webhook
- Type: Respond to Webhook
- Returns JSON including:
  - success
  - sentiment
  - confidence
  - emotions
  - reason
  - action
  - priority
  - message

This is the final response returned to the caller.

---

## 📦 What the model returns

For a request like:
“I absolutely love this product, it changed my life!”

The model might return something like:

{
  "sentiment": "positive",
  "confidence": 0.97,
  "emotions": ["joy", "satisfaction"],
  "reason": "The text expresses strong enthusiasm and satisfaction with the product."
}

Then the workflow routes it to the positive branch.

---

## 🧠 Why this workflow matters

This is a classic example of:
- AI classification
- conditional logic
- multi-branch automation
- API response routing

Use cases:
- customer feedback triage
- social media monitoring
- review classification
- support ticket prioritization

---

## 🔍 Business logic

The workflow is effectively doing:

- If sentiment is positive → success team
- If sentiment is neutral → log for review
- If sentiment is negative → support alert

So it transforms raw text into an operational action.

---

## ✅ Summary

This workflow does three main things:

1. Receives incoming text
2. Uses AI to classify sentiment and confidence
3. Routes the result into different actions based on sentiment