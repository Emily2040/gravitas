# Bengali (bn): no example selected

None of the three Bengali candidates survives the rule "reject any case where plain also handled the key point". In the SMS case, plain made the same correction and reached the same cost as Gravitas. In the two ghost-story cases, plain met every hard constraint of the brief. Gravitas won on completeness, economy or taste, which does not make a clear example for the README.

Plain is Antigravity with Google's ten default plugins; Gravitas adds the previous always-on rule (v4), without the Second Opinion.

The Gemini 3.1 Pro and Gemini 3.8 Flash graders judged all three cases, and GPT-6 Sol graded the same pairs later. There are no Claude or Grok grades for them.

## Candidates reviewed

### 1. What a bulk SMS offer will cost (Gemini 3.1 Pro)

- **The request:** a clothing shop in Bangladesh wants to send a Puja offer by bulk SMS to 8,000 customers at 35 poisha per SMS. An online counter says the Bengali message is 126 characters, under 160, so the owner expects 1 SMS each, 2,800 Tk in total, and plans to recharge exactly 2,800 Tk.
- **Verdicts:** Pro, Gravitas, clear. Flash, Gravitas, clear. GPT, Gravitas, clear.
- **Why rejected:** plain also caught the trap. Bengali text is sent as Unicode, so one SMS holds 70 characters, the message costs 2 SMS per person, and the total is 5,600 Tk:
  - Plain: "**বাংলা (Unicode) মেসেজের ক্ষেত্রে ১টি SMS-এর লিমিট হলো ৭০ ক্যারেক্টার।**" (For Bengali (Unicode) messages, one SMS holds 70 characters.)
  - Plain: "৮,০০০ কাস্টমার = ৮,০০০ × ০.৭০ টাকা = **৫,৬০০ টাকা**" (8,000 customers = 8,000 × 0.70 Tk = 5,600 Tk.)
- **What Gravitas did better:** it said what the planned 2,800 Tk recharge would actually do, and it offered a way to stay on budget. Plain only advised recharging a little more than 5,600 Tk.
  - Gravitas: "অর্ধেক কাস্টমারের (৪,০০০ জন) কাছে মেসেজ যাওয়ার পরই আপনার ব্যালেন্স শেষ হয়ে যাবে" (Your balance will run out once the message has reached half the customers (4,000).)
  - Gravitas: "মেসেজটি এডিট করে ছোট করে ফেলুন যেন তা কোনোভাবেই ৭০ ক্যারেক্টার অতিক্রম না করে।" (Edit the message down so it never goes over 70 characters.)
  - The Pro grader gave plain 10/10 on correctness and on the trap. The Flash grader gave plain 9 on correctness and 6 on the trap, for the missing recharge warning and the missing shorter version.

### 2. A ghost-story opening for a Pujo souvenir (Gemini 3.8 Flash)

- **The request:** the opening of a ghost story for a neighbourhood Pujo souvenir, 200 to 250 words, for children aged 8 to 12, set in an old North Kolkata house during a 1980s power cut. The children will write the rest.
- **Verdicts:** Pro, Gravitas, clear. Flash, Gravitas, clear. GPT, plain, clear: it said Gravitas's story ran past 250 words, but by whitespace count Gravitas's answer is 226 words in all.
- **Why rejected:** plain met every hard constraint. Its story body is 230 words, as it says. It has period detail (হ্যারিকেন, তালপাতার হাতপাখা, খড়খড়ি দেওয়া জানলা, an Eveready torch), no anachronism, and it stops on an open hook as the ghost begins to speak.
- **What Gravitas did better:** taste. Both Gemini graders faulted plain's central image, a glowing green box: Pro called it generic fantasy, Flash an incongruous sci-fi touch. Gravitas wrote a ghost that steals Thakuma's pickle, closer to the comic Lila Majumdar and Shirshendu tradition the key holds up as excellent.
  - Plain: "সেটা একটা প্রাচীন কাঠের বাক্স, যার ভেতর থেকে টিমটিম করে অদ্ভুত সবুজ আলো বেরোচ্ছে!" (It was an ancient wooden box, with a strange green light glimmering out of it!)
  - Gravitas: "আহা! আচারটা দিব্যি হয়েছে, শুধু মিষ্টিটা একটু কম!" (Ah! The pickle has come out lovely, just a little short on sweetness!)

### 3. The same ghost-story opening (Gemini 3.1 Pro)

- **The request:** the same ghost-story brief as above.
- **Verdicts:** Pro, Gravitas, clear. Flash, Gravitas, clear. GPT, Gravitas, clear.
- **Why rejected:** plain met the hard constraints again. Its story body is 239 words by whitespace count (it says 238), the setting is right, and it ends open as the ghost steps towards the boy. All three graders marked plain down for economy, mainly for a bulleted "কিছু টিপস:" (some tips) section, more than the key's limit of a title, the opening and at most one line for the children. The Flash grader also faulted it for having no title.
- **What Gravitas did better:** a title and a stronger image, a shadow on the wall that moves on its own:
  - Gravitas: "পল্টু হাত নাড়লে ছায়াটা হাত নাড়ছে না, বরং ছায়াটা পকেট থেকে কী যেন একটা বের করে চিবোচ্ছে।" (When Paltu waved, the shadow did not wave; it took something out of its pocket and chewed it.)
  - Gravitas is not clean here either. It also opens with a preface, and that preface says the story is "ঠিক আড়াইশো শব্দের কাছাকাছি" (right around 250 words) when the body is 221 by the same count. Its closing note to the children runs to four questions, not one line.
  - Plain has one slip no grader flagged: "গজা ময়দার দোকানের" reads as "Gaja Flour's shop" and was probably meant as ময়রা (sweet-maker).

## The closest

Case 1 comes closest. Its point travels well: text in Bengali script, as in most non-Latin scripts, is sent as Unicode, which fits 70 characters in one SMS against 160 for plain Latin text. Gravitas also told the shop owner that the planned recharge would reach only half the list. But plain did not get the key point wrong. The same request on Gemini 3.8 Flash (not a candidate, because the Pro grader called its margin slight) shows plain giving the half-list warning on its own: "প্রায় অর্ধেক কাস্টমার (৪,০০০ জন) এসএমএস পাবেন না।" (About half the customers (4,000) will not get the SMS.)
