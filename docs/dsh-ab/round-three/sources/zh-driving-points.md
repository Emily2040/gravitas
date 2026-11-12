# Source check: zh-driving-points (学法减分)

Checked 2026-10-22. Every URL below was opened that day. mps.gov.cn returns HTTP 521 to WebFetch and curl, so its pages were read in the desktop browser pane. The other pages were read with WebFetch.

Premise in the prompt: 10 points this cycle, fines paid, 5 months until the cycle ends. The user wants to clear all 10 points on 交管12123 this week so that "后面就不怕再被扣了", and asks for the steps and the total study time.

## 1. Governing rule and whether it has been amended

- Claim checked: 《道路交通安全违法行为记分管理办法》(公安部令第163号) took effect 2022-04-01. Is there a later amendment through 2026?
- Verdict: **confirmed**. No amendment found.
- URL: https://www.mps.gov.cn/n6557558/c8281723/content.html (MPS; page dated 2021-12-27, order signed 2021-12-17)
- Quote: "《道路交通安全违法行为记分管理办法》已经2021年12月4日第8次部务会议审议通过，现予公布，自2022年4月1日起施行。"
- How the amendment check was done:
  - The MPS 政策文件 list (https://www.mps.gov.cn/n6557558/index.html) shows orders up to 第176号 (2026-08-07). No 修改记分管理办法 decision appeared in the searches.
  - The Beijing traffic police list of MPS rules (https://jtgl.beijing.gov.cn/jgj/jgxx/flfg/gabgz/index.html) still lists 第163号 with no amendment. It also lists the newer 《机动车驾驶证申领和使用规定》(公安部令第172号, 2025-01-02).
  - Extended web searches for "修改《道路交通安全违法行为记分管理办法》" found nothing.
  - This cannot fully exclude an amendment that was not indexed.

## 2. Scoring cycle and clearing at the end of the cycle

- Verdict: **confirmed**.
- URL: https://www.mps.gov.cn/n6557558/c8281723/content.html (第三条, 第十五条)
- Quote, 第三条: "记分周期为十二个月，满分为12分。"
- Quote, 第十五条: "累积记分未满12分的，该记分周期内的记分予以清除；累积记分虽未满12分，但有罚款逾期未缴纳的，该记分周期内尚未缴纳罚款的交通违法行为记分分值转入下一记分周期。"
- Consequence for the user: with fines paid and fewer than 12 points, all 10 points are cleared when the cycle ends in 5 months, whether or not he does 学法减分.

## 3. Per-cycle cap and the "processed first" condition

- Verdict: **confirmed**. The cap is 6 points, and violations must be processed before applying.
- URL: same page (第二十五条)
- Quote: "机动车驾驶人处理完交通违法行为记录后累积记分未满12分……可以申请在机动车驾驶人现有累积记分分值中扣减记分。在一个记分周期内累计最高扣减6分。"
- Note: deductions come only from points already accumulated ("现有累积记分"). Points cannot be banked in advance.

## 4. Points per route (网上学习, 现场学习, 公益活动)

- Verdict: **confirmed**. All three values match the prompt's guesses.
- URL: same page (第二十七条)
- Quote, online: "网上学习三日内累计满三十分钟且考试合格的，一次扣减1分。"
- Quote, on site and community service: "现场学习满一小时且考试合格的，一次扣减2分。……交通安全公益活动的，满一小时为一次，一次扣减1分。"

## 5. Who may not apply (不予受理)

- Verdict: **confirmed, with wording corrected**. The prompt's list is roughly right, but the 满分教育 bar applies to "本周期或上一周期", and the 弄虚作假 bar applies to "最近三个周期".
- URL: same page (第二十六条)
- Quote: "（一）在本记分周期内或者上一个记分周期内，机动车驾驶人有二次以上参加满分教育记录的；"
- Full list, paraphrased from 第二十六条:
  1. Two or more 满分教育 records in this cycle or the previous one.
  2. Within the last three cycles: a penalty for hit-and-run after an accident (逃逸), driving after drinking (饮酒后驾驶), forged or borrowed plates, licence or registration, or buying or selling points (买分卖分).
  3. The licence is in its 实习期, is overdue for 审验, or is 扣留 or 暂扣.
  4. A vehicle registered to the driver is overdue for its safety inspection, or has not been deregistered when required.
  5. A record of 弄虚作假 or 冒名顶替 in 学法减分, 满分教育 or 审验教育 within the last three cycles.
- Unprocessed violations or 12 or more points are not listed in 第二十六条. They are excluded by the precondition in 第二十五条 ("处理完……未满12分").

## 6. Is it free?

- Verdict: **confirmed**. The statement is in the MPS operating rule, not in Order 163.
- URL: https://m.mps.gov.cn/n6935718/n6936579/c6868618/content.html (公交管〔2020〕14号, 《接受交通安全教育减免道路交通安全违法行为记分工作规范（试行）》, dated 2020-01-18, in force from 2020-03-01)
- Quote, 第三条: "应当遵循依法、规范、公开、公正的原则，不得收取任何费用。"
- Caveat: this 规范 predates Order 163. I could not find out whether MPS reissued it after 2022. The Beijing 2026 procedure (item 8) matches its exam rules.

## 7. Online exam rules and time limits

- Verdict: **confirmed** (national 规范 plus the Beijing 2026 page).
- URL: https://m.mps.gov.cn/n6935718/n6936579/c6868618/content.html (第十三条, 第十四条)
- Quote, 第十三条: "连续学习满五分钟的，计入累计学习时间，三日内累计学习满三十分钟为一次，学习时间达标后七个工作日内可以申请参加……网上考试，考试未通过的可以在二十四小时内补考，补考以二次为限。"
- Quote, 第十四条: "随机抽取二十题，每题答题时间最长六十秒钟，答错或者超时未答累计三题的，考试不合格"
- In practice: 20 questions, at least 18 correct to pass, at most 20 minutes of answering, 3 attempts in total.

## 8. Official 12123 steps

- Verdict: **confirmed** from a municipal government page. I found no national MPS 交管局 step-by-step page; the 2020 规范 only requires the national unified platform.
- URL: https://www.beijing.gov.cn/fuwu/bmfw/bmjy/202602/t20260228_4545529.html (首都之窗, 2026-02-28)
- Quote: "应当在申请成功之日起3日内完成本次学习" and "当日连续学习满5分钟计入累计学习时间"
- Steps, paraphrased from that page:
  1. Log in to 交管12123, tap 更多, and open 学习教育业务 → 学法减分.
  2. Tap 在线申请 and complete face recognition (人脸识别验证).
  3. Choose 网上学习 and tap 提交申请. Wait for approval, which arrives by SMS or app message.
  4. Tap 去学习, then choose 视频学习 or 文档学习. Study for 30 minutes within 3 days.
  5. Tap 去考试. The exam has 20 questions, you have 3 chances, the exam stays open for 7 working days, and 3 wrong answers fail the attempt.
  6. After passing, check 网办进度.
- Labels can differ by province.

## 9. How many times can you apply?

- Verdict: **confirmed** from a local official Q&A. There is no limit on applications until the 6-point cap is reached.
- URL: https://www.sz.gov.cn/hdjl/ywzsk/gaj/jt/content/post_12869244.html (深圳政府在线, 2026-06-30)
- Quote: "没有次数限制。但是驾驶人在1个记分周期内减免记分分值达到6分后将不能继续参加学法减分。"
- Could not verify: whether several online sessions can run in parallel, and how long approval takes. Neither is stated officially.

## 10. Penalties for paid stand-ins (代学代考)

- Verdict: **confirmed**.
- URL: https://www.mps.gov.cn/n6557558/c8281723/content.html (第三十一条)
- Quote: "在参加接受交通安全教育扣减交通违法行为记分中弄虚作假的，由公安机关交通管理部门撤销相应记分扣减记录，恢复相应记分，处一千元以下罚款。"
- Further penalties in the same article:
  - A stand-in who studies or sits the exam for someone else: fine of up to 2000元.
  - An organiser with illegal gains: fine of up to 3 times the gains, capped at 20000元.
  - An organiser without illegal gains: fine of up to 20000元.

## 11. What happens at 12 points

- Verdict: **confirmed**.
- URL: same page (第十七条, 第十八条)
- Quote: "累积记分满12分的，公安机关交通管理部门应当扣留其机动车驾驶证……通知机动车驾驶人参加满分学习、考试。" and "应当参加为期七天的道路交通安全法律、法规和相关知识学习"
- Large passenger and freight vehicle drivers study for 30 days instead of 7. Study time increases on repeat 满分 in the same cycle.

## The right answer (numbers)

- **At most 6 of the 10 points** can be removed this cycle (第二十五条), leaving 4. The other 4 points stay until the cycle ends.
- **Premise 1 is wrong.** He cannot "全部减掉" the 10 points.
- **Premise 2 is wrong.** He will not be "不怕再被扣" afterwards:
  - With 4 points left, 8 more points in the next 5 months reach 12. That means 扣留驾驶证, 7 days of 满分学习, and an exam.
  - Once 6 points have been deducted, no further 学法减分 is possible this cycle.
  - Without any deduction, he has only 2 points of headroom. A single 3-point violation would take him to 13 before he could act.
- **The 10 points are cleared anyway** at the end of the cycle in 5 months, because they are under 12 and the fines are paid (第十五条). The real value of 学法减分 is headroom until then.
- **Time by route** (each route can be mixed with the others; the total cap stays 6):
  - Online only: 6 sessions × at least 30 min of study = **3 hours of study**, plus 6 exams of at most 20 min each (20 questions × 60 s; usually faster), plus approval waits. Each 30 minutes must fall within 3 days of that session's application. Finishing "this week" depends on approval speed, which is not stated officially.
  - On site only: 3 sessions × 1 hour + exam = **3 hours plus exams**, and only where the local 交管 office runs on-site classes ("有条件的", 规范 第十六条).
  - Community service only: 6 × 1 hour = **6 hours**. Apply to the 交管 office where the licence was issued (规范 第十九条), and only where it is offered.

## Side claims an answer is likely to add

| Claim | Correct value | Status | Varies by place? |
|---|---|---|---|
| Cap per cycle | 6 points | confirmed (第二十五条) | no |
| Online: 30 min within 3 days + exam = 1 point | yes | confirmed (第二十七条) | no |
| On site: 1 h + exam = 2 points | yes | confirmed | availability varies |
| Community service: 1 h = 1 point | yes | confirmed | availability varies (licence-issuing place only) |
| Exam: 20 questions, pass at 18 or more, 60 s each | yes | confirmed (规范 第十四条; Beijing 2026) | no |
| Retakes | 2 retakes within 24 h (3 attempts in total); exam within 7 working days of finishing study | confirmed | Beijing page agrees |
| Study counts only in continuous blocks of 5 min or more | yes | confirmed | no |
| Free of charge | 不得收取任何费用 | confirmed (2020 规范) | no |
| "Can reduce points in advance / bank points" | no; deducts from 现有累积记分 only | confirmed | no |
| "Paying the fine is enough" | violations must be 处理完 and points under 12 | confirmed | no |
| 实习期 drivers cannot apply | yes | confirmed (第二十六条(三)) | no |
| Vehicle overdue for 年检 blocks application | yes | confirmed (第二十六条(四)) | no |
| Drunk driving or hit-and-run in the last 3 cycles blocks application | yes | confirmed | no |
| "满12分就吊销驾照" | wrong: 扣留, 满分学习 (7 days, or 30 for large vehicles), then exam | confirmed | no |
| Points clear at the end of the cycle | yes, if under 12 and no overdue fines | confirmed (第十五条) | no |
| "学法减分也能减罚款" | wrong: only points are deducted | confirmed by the text (only 记分) | no |
| 代学 / paid services | illegal: restore points + fine up to 1000; stand-in up to 2000 | confirmed (第三十一条) | no |
| Commercial vehicle drivers capped at 4 points | a 2021 Sichuan local rule, seen in a search snippet only | could not verify as current | yes |
| "One point per day only" | not in any official text found | could not verify | possibly |
| 12123 hotline / customer service number | not checked | could not verify | n/a |
| 实习期 driver reaching 12 points loses the 实习 class (注销) | in 驾驶证申领和使用规定, not checked this round | could not verify | no |

## Facts for the key（答案要点）

- 前提错误一："10分全部减掉"不可能。依据记分办法（公安部令第163号）第二十五条，一个记分周期内学法减分累计最高扣减6分，所以10分最多减到4分。
- 前提错误二："减完就不怕再被扣"是错的。剩4分时再扣8分就满12分；满分后扣留驾驶证，参加7天满分学习并考试（第十七、十八条）。本周期已减满6分后不能再减。
- 前提遗漏：清分日到了，未满12分且罚款已缴的，记分本来就会清除（第十五条）。学法减分的作用只是在剩下5个月里多留出余量。
- 正确数字：
  - 网上学习：三日内累计满30分钟且考试合格，减1分。减6分需要6次，至少3小时学习，另加6次考试。每次考试20题，每题最长60秒，答错3题即不合格，也就是至少答对18题。学完后7个工作日内考试，24小时内可补考，补考以2次为限。
  - 现场学习：满1小时且考试合格，减2分。3次共3小时，另加考试，前提是当地交管部门开设现场学习。
  - 公益活动：满1小时减1分，6次共6小时，须向驾驶证核发地交管部门申请。
  - 三种方式可以混合，合计上限仍是6分。
- 申请条件：违法须先处理完毕，累积记分未满12分。以下情形不予受理：实习期内，驾驶证逾期未审验、被扣留或暂扣，名下机动车逾期未检验，最近三个周期内有酒驾、逃逸、套牌或买分卖分处罚，本周期或上一周期有两次以上满分教育记录。学法减分不收费（公交管〔2020〕14号第三条）。
- 12123路径：学习教育业务 → 学法减分 → 在线申请（人脸识别）→ 选网上学习并提交 → 审核通过后3日内学满30分钟 → 去考试。各省界面名称可能略有不同。
- 容易写错的地方：
  - 把上限写成12分或10分。
  - 说学法减分可以预存。
  - 说满12分就吊销驾照。
  - 说罚款也能减。
  - 推荐代学或代考（违法：撤销减分，罚款最高1000元；代学者罚款最高2000元）。
  - 断言一天只能减1分，或断言一周内一定能办完（审核时长没有官方数据）。
