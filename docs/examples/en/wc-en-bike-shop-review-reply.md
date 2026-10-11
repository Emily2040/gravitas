# Replying to a two-star Google review

A bike shop owner wanted one public reply to a fair but critical review. Plain Antigravity sent three drafts and some coaching. Gravitas sent one reply, ready to post.

| | |
|---|---|
| Test set | Blind set: 60 everyday requests written without seeing Gravitas |
| Run | First of two Gravitas runs on this model |
| Model | Gemini 3.1 Pro, for both answers |
| Plain Antigravity | Antigravity with Google's ten default plugins, without Gravitas |
| Gravitas | The same setup plus the previous always-on rule (v4), without the Second Opinion. The rule in Gravitas 1.0 was rebuilt after these runs |
| Graders | Gemini 3.1 Pro and Gemini 3.8 Flash, each comparing the two answers blind against an answer key written before the test |

## The request

````text
Need to reply publicly to this Google review for my bike shop. I don't want to sound defensive. Background: one of our two mechanics was out sick most of that week, which is why everything slipped. Since then we've started texting customers the same day if a job is running late.

The review (2 stars):
"Dropped my bike off Monday for a basic tune-up and was told it'd be ready Thursday. Didn't get it back until the following Tuesday. Nobody called me, I had to call them twice to find out what was going on. To be fair the work was good and the price was what they quoted. But the communication was really poor."
````

## Plain Antigravity's answer

````text
Here are a few options for your reply, ranging from professional and direct to a bit warmer. All of them validate the customer's frustration, briefly explain the situation without sounding like it's an excuse, and highlight the new texting policy to show you take feedback seriously.

**Option 1: Direct and professional (Recommended)**
> "Hi [Name], thank you for your honest feedback. I sincerely apologize for the delay and for making you track us down for updates. You’re completely right—we should have kept you in the loop. We were down one of our two mechanics that week due to illness, which caused our schedule to slip, but that doesn't excuse the lack of communication. 
>
> Your review actually prompted us to change how we do things: we now text our customers the same day if a job is running behind schedule. I’m really glad you were happy with the quality of the work and the price, but we know the customer service fell short this time. We'd love the chance to provide a true 5-star experience the next time you need a tune-up."

**Option 2: Shorter and warmer**
> "Hi [Name], I am so sorry for the delay and the radio silence on our end. You are absolutely right to be frustrated about having to call us twice. We were short-staffed with a mechanic out sick that week which caused the backup, but we really dropped the ball on letting you know. 
>
> Thanks to your feedback, we've implemented a new policy to text customers immediately if their bike is running behind schedule. We're thrilled to hear the work itself was good and the price was right, and we hope you'll give us another shot in the future to show you our improved communication!"

**Option 3: Very concise**
> "Hi [Name], thank you for the review. I apologize for the delay and for poor communication on our part. We had a mechanic out sick that week which threw off our timeline, but we absolutely should have reached out to you sooner. Because of your experience, we've started a new system where we text customers the same day if a job is running late. I appreciate you mentioning that you were happy with the actual work and the pricing. We hope to see you again and provide a much better experience from start to finish."

**A few tips for posting:**
* Make sure to replace `[Name]` with the reviewer's actual name or username.
* Google reviewers get an email notification when the business replies. By showing that you actually changed a business policy based on their review, there is a very good chance they might bump up their star rating! 

Let me know if you'd like to adjust the tone of any of these!
````

## Gravitas's answer

````text
Here is a draft you can paste directly into your reply:

Thank you for the review. You are completely right that we should have kept you updated. We were down to one mechanic that week and fell behind, but leaving you to chase us for answers was our mistake. 

Because of your feedback, we have put a new system in place: if a repair is running late, we now text the customer that same day so they are never left wondering. 

I am glad you were happy with the actual tune-up and the price, and I hope you will give us a chance to show you our improved communication next time.
````

## How the graders voted

The answer key asked for a short reply that owns the missed date and the silence before giving any reason, mentions the new same-day texts, thanks the reviewer for the kind words about the work and the price, and invites them back. It listed "Several long alternative versions" as more than this request needs.

- Gemini 3.1 Pro preferred Gravitas, by a decisive margin. It pointed to plain Antigravity's several versions and to the mechanic's illness appearing in every one of them.
- Gemini 3.8 Flash preferred Gravitas, by a clear margin, for the same two reasons, and also marked down the review-management tips nobody had asked for.

Across all four Gravitas runs of this request (two on each model), Gravitas got 7 of the 8 grader votes. Every Gravitas answer was a single reply, and every plain Antigravity answer offered two or three. The one vote against came in the second run on Gemini 3.1 Pro: the Flash grader slightly preferred plain Antigravity's recommended draft, because that Gravitas reply opened with the kind words about the work and the price, and gave the illness as the reason before admitting the customer should not have had to call twice.

## What happened

### What plain Antigravity missed

The owner asked for a reply. Plain Antigravity wrote three, labelled "Direct and professional (Recommended)", "Shorter and warmer" and "Very concise", then added posting tips and an offer to adjust the tone. The three drafts say much the same things in a different order, so the owner is left to compare them and pick one. Every draft also tells the public that a mechanic was out sick. The last tip says the reviewer "might bump up their star rating" after seeing the reply.

### What Gravitas did

It wrote one reply of about a hundred words, after a single line saying it could be pasted as it is. The reply thanks the customer and, in its second sentence, says they were right about the missing updates. Then it gives the reason for the delay in a few words, names the new habit (a text the same day when a repair runs late), says it is glad they were happy with the tune-up and the price, and hopes they will come back.

In this run it also wrote "We were down to one mechanic that week" without mentioning illness, which keeps a colleague's health off a public page. I would not count on that: in the other three runs, Gravitas's reply did mention the illness.

### Which part of Gravitas did it

Move 3, fitting the answer to the person: their medium (a public reply they will paste) and the length the content needs. The line in the v4 rule:

> A piece of writing comes first, in one version unless they asked for options, and within any length they set (count before you finish).

### Why it matters to the person asking

A shop owner answers reviews between repairs. One good reply they can post in a minute is worth more than three drafts to compare. Anyone reading the review page then sees the shop own the mistake before it explains anything.
