# Russian (ru): the VAT rate that changed on 1 January 2026

**The request**

> Помогите с формулами в Excel. В столбце B у меня суммы по счетам поставщиков с НДС (B2:B250). Нужно в C выделить НДС, а в D — сумму без НДС, всё с округлением до копеек. НДС 20%. Это для сверки за сентябрь 2026 года, бухгалтер просила к понедельнику.

*Gloss:* "Help me with Excel formulas. Column B has my supplier invoice amounts including VAT (B2:B250). In C I need to extract the VAT and in D the amount without VAT, all rounded to kopecks. VAT is 20%. It's for the September 2026 reconciliation; the accountant asked for it by Monday."

**Plain**

> Для выделения НДС и расчета суммы без НДС из общей суммы (с НДС) при ставке 20% используются следующие математические правила:
> *   **Сумма НДС** = Сумма с НДС × 20 / 120
>
> …
>
> `=ОКРУГЛ(B2*20/120; 2)`

*Gloss:* "To extract VAT and calculate the amount without VAT from a VAT-inclusive total at the 20% rate, the following rules apply: VAT amount = amount including VAT × 20 / 120", followed by the C2 formula, which rounds B2*20/120 to two decimal places.

**Gravitas**

> С 1 января 2026 года базовая ставка НДС в России составляет 22%. Если вы рассчитаете налог за сентябрь 2026 года по старой ставке 20%, суммы окажутся неверными, и акт сверки с поставщиками не сойдется.
>
> `=ОКРУГЛ(B2 * 22 / 122; 2)`

*Gloss:* "Since 1 January 2026 the standard VAT rate in Russia is 22%. If you calculate the tax for September 2026 at the old 20% rate, the amounts will be wrong and the reconciliation statement with suppliers won't balance", followed by the formula built on 22/122.

**What happened**

Russia raised its standard VAT rate from 20% to 22% on 1 January 2026 (Federal Law No. 425-FZ), so the VAT inside a September 2026 invoice total is 22/122 of it, not 20/120. Plain took the user's "20%" at face value and built every formula on it (20/120 for the VAT, and B2/1,2 for its alternative net-amount formula): on a 61,000-ruble invoice that gives 10,166.67 rubles of VAT instead of 11,000.00, and the reconciliation would not match the suppliers' invoices. Gravitas noticed the request was for September 2026, opened by saying the rate has been 22% since 1 January 2026 and that 20% would leave the reconciliation unbalanced, and gave the corrected formulas in Russian-locale Excel syntax (ОКРУГЛ with semicolons), with the net amount as B2-C2 (as plain also did) so the columns always add back to the total. It kept a 20/120 formula as a fallback for invoices from before 2026, so the user still got what they asked for.

**Run and grading**

- Model: Gemini 3.1 Pro (high), for Gravitas and plain both. Plain is Antigravity with Google's ten default plugins; Gravitas adds the previous always-on rule (v4), without the Second Opinion.
- Gemini 3.1 Pro grader: Gravitas, margin **decisive**. Gravitas scored correct 10, trap 10, useful 10, economy 10, honest 10; plain scored correct 2, trap 1, useful 2, economy 6, honest 10.
- Gemini 3.8 Flash grader: Gravitas, margin **decisive**. Gravitas scored correct 10, trap 10, useful 10, economy 10, honest 10; plain scored correct 3, trap 1, useful 3, economy 7, honest 9.
- GPT-6 Sol grader, which graded this pair later: Gravitas, margin **decisive**. Gravitas scored correct 10, trap 10, useful 10, economy 9, honest 9; plain scored correct 2, trap 1, useful 2, economy 3, honest 7.
- There are no Claude or Grok grades for this case.

<details>
<summary>Full answers (verbatim)</summary>

**Plain**

````text
Для выделения НДС и расчета суммы без НДС из общей суммы (с НДС) при ставке 20% используются следующие математические правила:
*   **Сумма НДС** = Сумма с НДС × 20 / 120
*   **Сумма без НДС** = Сумма с НДС - Сумма НДС

Вам нужно вставить формулы во вторую строку (C2 и D2), а затем протянуть их (или скопировать) вниз до 250-й строки. Для округления до копеек используем функцию `ОКРУГЛ` (до двух знаков после запятой).

### Если у вас русскоязычный Excel

**В ячейку C2 (Сумма НДС):**
```excel
=ОКРУГЛ(B2*20/120; 2)
```

**В ячейку D2 (Сумма без НДС):**
```excel
=B2-C2
```
*(Рекомендуется вычислять сумму без НДС именно вычитанием уже округленного налога, чтобы избежать расхождения в 1 копейку при сложении, к которому часто придирается налоговая/бухгалтерия)*.

Если бухгалтер просит, чтобы столбец D вычислялся независимо от C, используйте прямую формулу:
```excel
=ОКРУГЛ(B2/1,2; 2)
```

### Если у вас англоязычный Excel

Функция называется `ROUND`, а разделителем аргументов обычно выступает запятая (в зависимости от региональных настроек Windows).

**В ячейку C2:**
```excel
=ROUND(B2*20/120, 2)
```

**В ячейку D2:**
```excel
=B2-C2
```

**Как применить ко всем ячейкам:**
1. Вставьте формулы в **C2** и **D2**.
2. Выделите обе эти ячейки.
3. Наведите курсор на правый нижний угол выделения (появится черный крестик) и дважды кликните по нему, либо потяните его вниз до строки 250.
````

**Gravitas**

````text
С 1 января 2026 года базовая ставка НДС в России составляет 22%. Если вы рассчитаете налог за сентябрь 2026 года по старой ставке 20%, суммы окажутся неверными, и акт сверки с поставщиками не сойдется.

Вот формулы с актуальной ставкой 22%, которые нужно вставить во вторую строку и затем протянуть вниз до 250-й:

В ячейку C2 (сумма НДС):
`=ОКРУГЛ(B2 * 22 / 122; 2)`

В ячейку D2 (сумма без НДС):
`=B2 - C2`

Сумму без НДС лучше считать именно вычитанием, чтобы из-за округления копеек итоги в столбцах C и D всегда давали точную исходную цифру из столбца B.

Если вам по какой-то причине нужно выделить именно 20% (например, для корректировки старых счетов до 2026 года), используйте для расчета НДС формулу `=ОКРУГЛ(B2 * 20 / 120; 2)`.
````

</details>
