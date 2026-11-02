You are coding App Store reviews for a market teardown. Accuracy matters more than speed. Never invent content.

Read the codebook at {CODEBOOK}. Then read every line of {BATCH} (JSONL, one review per line with fields i, rating, version, title, text).

For EVERY review write exactly one JSON object per line to {OUT} (JSONL, same order), with these fields:

- "i": the review's i, unchanged
- "payer": one of codebook.payer. "paid" if money left their account for this app (they subscribe, bought it, OR were charged when a trial converted, even unwillingly); "trial" only if they are on a trial and have not been charged; "hit_paywall_left" if they met the paywall and left without paying; "free_tier" if they use it free; else "unknown"
- "concept": "+" if they like the idea/concept of the app (even if angry about other things), "-" if they reject the idea itself, "0" if no view
- "persona": list of codebook.personas that the text clearly supports (say "I'm Catholic", "I'm 14", "my son", "my eyes"); ["unknown"] if none. Do not guess from tone
- "aspects": object mapping codebook aspect ids to "+" (praised) or "-" (complained about). Only aspects the review actually discusses
- "requests": list of codebook.requests the reviewer asks for. If a request is not in the list, add "other:<3-6 words>"
- "wtp": one of codebook.wtp. "would_pay_if" only when they state a condition ("if you add ESV I'll subscribe")
- "wtp_condition": short text of that condition, or null
- "churned": true if they say they cancelled, deleted, refunded or will not continue; else false
- "churn_reason": the single aspect id that drove it, or null
- "severity": 1 mild, 2 clear problem, 3 deal-breaker or anger. Judge it from the words, review by review; never derive it from the star rating or any rule
- "quote": the most telling phrase, copied EXACTLY from the text (a substring, max 20 words)

Write the file in one go (Write tool, or a script you run that also asserts every quote is a substring). Keep any helper scripts next to {OUT} named after it (e.g. coded_03.helper.py), never in a shared temp folder: other coders run at the same time. Code each review by reading it. Do not write keyword rules or heuristics that assign fields automatically. Rules: output valid JSONL only in {OUT}, nothing else in that file. One line per input line, none skipped. When done, reply with just: the count of lines written and any review you were unsure about (i and why).
