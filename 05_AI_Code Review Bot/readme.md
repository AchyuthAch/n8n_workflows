## ✅ Workflow details

This workflow is an AI code review API. It accepts a code snippet and context, asks OpenAI to review it for quality/security issues, scores it, applies a pass/fail threshold, and returns a decision with review details.

---

## 🔄 End-to-end flow

### 1) Webhook
- Type: Webhook
- Method: POST
- Path: code-review
- Purpose: receives code review requests

Example request body:
{
  "code": "def get_user(id): ...",
  "language": "python",
  "context": "User lookup function for REST API",
  "pass_threshold": 7
}

This is the trigger for the workflow.

### 2) Extract Input
- Type: Set node
- Reads the incoming request fields:
  - code
  - language
  - context
  - pass_threshold
- Sets default values when missing:
  - language defaults to “unknown”
  - pass_threshold defaults to 7

This standardizes the input before AI processing.

### 3) Review Code with LLM
- Type: LangChain LLM Chain
- Uses a prompt that includes:
  - language
  - context
  - code snippet
- It asks the model to return a JSON object with:
  - overall_score
  - security_issues
  - quality_issues
  - best_practice_violations
  - positive_aspects
  - refactored_snippet
  - summary

Important constraint:
- “Return ONLY valid JSON. No markdown.”
- This makes the downstream parsing step easier and more reliable

### 4) OpenAI Chat Model
- Type: OpenAI Chat Model
- Model: gpt-3.5-turbo
- Settings:
  - maxTokens: 1500
  - temperature: 0.2
- Purpose: performs the actual code review

### 5) Parse Review & Score
- Type: Code node
- It extracts the LLM output from likely fields like:
  - output
  - text
  - response
  - message.content
  - content
- It strips Markdown fences
- It parses JSON
- If parsing fails, it sets a fallback object with a lower score so the workflow still behaves safely

Then it calculates:
- critical_security_count
- high_security_count
- passes:
  - review.overall_score >= pass_threshold
  - and no critical security issues

It also keeps:
- original_code
- language
- context
- reviewed_at

So the workflow can decide both on score and on security risk.

### 6) Pass Threshold?
- Type: IF node
- Checks:
  - whether passes is true
- This is the decision gate
- True branch goes to approved
- False branch goes to needs changes

### 7) Mark Approved
- Type: Set node
- Sets:
  - status = APPROVED
  - badge = ✅
  - message = “Code passes review with score X/10. Ready for merge.”

This means the code is accepted.

### 8) Mark Needs Changes
- Type: Set node
- Sets:
  - status = NEEDS_CHANGES
  - badge = ❌
  - message = “Code requires changes. Score: X/10. Critical issues: Y. Address security and quality issues before merging.”

This means the code is rejected or sent back for revision.

### 9) Return Review
- Type: Respond to Webhook
- Returns a JSON response including:
  - status
  - badge
  - decision_message
  - score
  - threshold
  - security_issues
  - quality_issues
  - positive_aspects
  - refactored_snippet
  - summary
  - reviewed_at

This is the final output to the API caller.

---

## 📦 What the AI review includes

For each code snippet, the model is asked to produce:
- overall_score: 1–10
- security_issues: list of issues with severity and fix
- quality_issues: list of issues with severity and fix
- best_practice_violations: list of rule violations
- positive_aspects: what is good
- refactored_snippet: improved version of the code
- summary: 2–3 sentence review

This makes it more than just “pass/fail”; it gives actionable developer feedback.

---

## 🔍 Decision rule

A code review passes only if:
- score is above or equal to threshold
- and there are zero critical security issues

That means the workflow enforces both:
- quality threshold
- security gate

This is a strong production pattern.

---

## 💡 Example business logic

If someone sends this Python snippet:

def get_user(id):
  return db.execute(f'SELECT * FROM users WHERE id={id}')

The AI may flag:
- SQL injection risk
- lack of parameterization
- unsafe dynamic query construction

Then the workflow would likely route it to NEEDS_CHANGES if:
- score is low
- or critical security issue exists

---

## 🧠 In plain English

This workflow acts like a code-review bot:

- accept a code snippet
- have AI inspect it
- detect security and quality problems
- score it
- decide whether it’s acceptable
- return a structured result and fix suggestions