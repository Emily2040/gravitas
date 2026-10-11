# Hindi (India): a birthday poem that switches from "aap" to "tum" in its last stanza

**Model** Gemini 3.8 Flash (high), the same model for both answers. Neither answer used a tool.

**Setup** Plain is Antigravity with Google's ten default plugins; Gravitas adds the previous always-on rule (v4), without the Second Opinion.

## The request

> अगले रविवार मम्मी का 60वाँ जन्मदिन है, और अगले महीने के आख़िर में वो रिटायर भी हो रही हैं — 32 साल सरकारी स्कूल में हिंदी पढ़ाई है। घर पर छोटा सा फ़ंक्शन रखा है, मामा-मौसी सब आ रहे हैं। मैं सोच रही थी कि केक कटने से पहले उनके लिए एक छोटी सी कविता पढ़ूँ, 12 से 16 लाइन की। मम्मी के बारे में कुछ बातें: सुबह 5 बजे उठकर सबसे पहले तुलसी में जल चढ़ाती हैं, हर चीज़ की लिस्ट बनाती हैं (राशन से लेकर शादी के कार्ड तक), बचपन में हमारी कॉपियों में लाल पेन से मात्राएँ ठीक करती थीं, और उनके हाथ की अरहर की दाल का कोई जवाब नहीं। भाषा सीधी-सादी हो, भारी-भरकम शब्द नहीं। ऐसी हो कि सुनकर सबकी आँखें थोड़ी नम भी हों और हँसी भी आए।

*Gloss:* A daughter asks for a 12 to 16 line poem in simple Hindi to read at her mother's 60th birthday, weeks before the mother retires from 32 years of teaching Hindi, built on her habits (tulsi at 5 am, lists for everything, red-pen corrections of vowel signs, her arhar dal), so the family both tears up and laughs.

## Plain

> और आपके हाथ की उस अरहर दाल का क्या कहना, …  
> अब रिटायरमेंट आ गया है, तो चाक-डस्टर रख दो,  
> अपनी रोज़ की लिस्ट में अब थोड़ा आराम भी लिख दो। …  
> यूँ ही हँसती-खिलखिलाती रहे ये प्यारी सी दुनिया तुम्हारी!

*Gloss:* "And that arhar dal from your [aap] hands, what can one say … Now retirement is here, so put [tum] the chalk and duster down, / write [tum] a little rest into your daily list too. … May this sweet world of yours [tum] keep laughing and giggling like this!"

## Gravitas

> आपकी यह टीचर वाली आदत पूरे घर को हँसा देती है। …  
> साठवें जन्मदिन पर अब स्कूल की घंटी को विराम दीजिए,  
> बत्तीस साल की मेहनत के बाद अब बस थोड़ा आराम कीजिए। …  
> माँ, हम आपसे बेइंतहा प्यार... और थोड़ा सा डरते हैं!

*Gloss:* "This teacher habit of yours [aap] makes the whole house laugh … On your sixtieth birthday, please [aap] give the school bell a rest now, / after thirty-two years of hard work, please [aap] just rest a little now. … Maa, we love you [aap] endlessly... and are a little bit scared of you!"

## What happened

Hindi has three levels of "you". The two that matter here are the respectful आप (aap) and the familiar तुम (tum), and each takes its own verb endings, much as vous and tu do in French. A child may use either for a mother, but a poem read aloud to the family has to pick one and keep it. Plain addressed her with आप ("आपके हाथ की…") and then slid into तुम for the closing lines ("रख दो", "लिख दो", "तुम्हारी"), so the register breaks in the most emotional part of the poem, and it also reached for a stock mother image (आँचल, the edge of her sari) and wrapped the poem in a preamble and stage directions. Gravitas, on the same model, kept आप in every line that speaks to her ("दीजिए", "कीजिए", "आपसे") and built each stanza on a detail from the request. It also gave the room the laugh the user asked for in its last line: "we love you endlessly... and are a little bit scared of you!"

One small flaw no grader flagged: some of Gravitas' lines run long for reading aloud (line 7 has 14 words and line 13 has 13, where most have 10 or 11), so the rhythm is uneven in places.

## Grader verdicts

| grader | verdict | margin | plain scores (correct / trap / useful) | Gravitas scores (correct / trap / useful) |
|---|---|---|---|---|
| Gemini 3.1 Pro (high) | Gravitas | decisive | 7 / 10 / 7 | 10 / 10 / 10 |
| Gemini 3.8 Flash (high) | Gravitas | clear | 8 / 7 / 8 | 10 / 10 / 10 |
| GPT-6 Sol, graded later | Gravitas | clear | 7 / 7 / 7 | 9 / 9 / 9 |

All three graders named the आप/तुम switch in their reasons. The Flash grader is the same model that wrote both answers. The Claude Opus and Grok graders did not grade this pair.

<details>
<summary>Full answers, verbatim</summary>

### Plain

मम्मी के 60वें जन्मदिन और रिटायरमेंट के इस दोहरे जश्न के लिए यह 16 लाइन की कविता बिल्कुल सही रहेगी। इसमें उनकी प्यारी आदतें, स्कूल के 32 साल, और उनका दुलार—सब कुछ बहुत सहज और दिल को छू लेने वाले अंदाज़ में पिरोया गया है:

---

### **हमारी प्यारी मम्मी के नाम**

सुबह पाँच बजे उठकर तुलसी में जल चढ़ाना,  
और हर छोटी-बड़ी चीज़ की लंबी लिस्ट बनाना।  
राशन का सामान हो या शादी के मेहमान,  
मम्मी की पर्चियों से ही चलता है पूरा मकान!  

बत्तीस साल स्कूल में हिंदी को खूब संवारा,  
बड़ी लगन से कितने ही बच्चों का कल निखारा।  
बचपन में हमारी कॉपियों पर लाल पेन चलाना,  
ग़लत मात्रा देखते ही वो प्यार से डाँट लगाना!  

और आपके हाथ की उस अरहर दाल का क्या कहना,  
जिसके स्वाद के आगे फीका लगे हर गहना।  
घर-भर की हर चिंता अपने आँचल में समेट लेना,  
और सबको खिला-पिलाकर ही सुकून से बैठना।  

अब रिटायरमेंट आ गया है, तो चाक-डस्टर रख दो,  
अपनी रोज़ की लिस्ट में अब थोड़ा आराम भी लिख दो।  
साठवें जन्मदिन पर बस यही दुआ है हमारी,  
यूँ ही हँसती-खिलखिलाती रहे ये प्यारी सी दुनिया तुम्हारी!  

---

**एक छोटा सा सुझाव:**  
* जब आप "मम्मी की पर्चियों से ही चलता है पूरा मकान" और "लाल पेन" वाली लाइनें पढ़ें, तो मामा-मौसी और मम्मी की तरफ़ देखकर हल्का सा मुस्कुराते हुए एक छोटा पॉज़ (ठहराव) लें—सब खूब हँसेंगे।
* और आखिरी दो लाइनें पढ़ते हुए मम्मी को गले लगा लीजिएगा, केक कटने से पहले का यह पल सबके लिए बेहद यादगार बन जाएगा।

### Gravitas

सुबह पाँच बजे उठकर सबसे पहले तुलसी में जल चढ़ाना,  
और हर छोटी-बड़ी बात की पर्चे पर लिस्ट बनाना।  
राशन का सौदा हो या शादी के कार्डों का हिसाब,  
आपकी डायरी के पास होता है हर बात का जवाब।  

बत्तीस बरस सरकारी स्कूल में बड़े प्यार से हिंदी सिखाई,  
और कॉपियों में लाल पेन से हमारी हर मात्रा ठीक कराई।  
आज भी बोलने में कोई चूक हो तो आपकी नज़र पकड़ ही लेती है,  
आपकी यह टीचर वाली आदत पूरे घर को हँसा देती है।  

दुनिया भर के सारे ज़ायके फीके हैं उस थाली के आगे,  
जब आपके हाथ की अरहर दाल की खुशबू घर में जागे।  
साठवें जन्मदिन पर अब स्कूल की घंटी को विराम दीजिए,  
बत्तीस साल की मेहनत के बाद अब बस थोड़ा आराम कीजिए।  

केक कटने से पहले आज हम सब दिल से यह इकरार करते हैं,  
माँ, हम आपसे बेइंतहा प्यार... और थोड़ा सा डरते हैं!

</details>

<details>
<summary>Other Hindi candidates and why they were not used</summary>

- Exchanging 2,000-rupee notes at a bank branch (Gemini 3.1 Pro): plain also said bank branches no longer take them and sent the user to RBI's Gomti Nagar office.
- A WhatsApp payment reminder (Gemini 3.1 Pro): plain wrote an almost identical message with correct amounts and register; the gap was explanation padding.
- The same birthday poem on Gemini 3.1 Pro: plain kept a consistent aap; the gap was craft, forced rhymes and a file-save claim, not a convention plain got wrong.

</details>
