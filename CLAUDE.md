# מדריך תוכן ופיתוח - אתר מנעולן בצרפתית (France-locksmith)

המדריך הזה מחייב כל כתיבה, עריכה או הוספה של תוכן לאתר, ע"י אדם או ע"י AI.

## 1. השפה: צרפתית בלבד

- **כל** טקסט שמופיע באתר כתוב בצרפתית בלבד: כותרות, פסקאות, כפתורים, תפריטים, alt של תמונות, meta title, meta description, schema, הודעות שגיאה, עמוד 404. אין אף מילה באנגלית או בעברית בתוכן הגלוי.
- חריג יחיד: מונחים אמריקאיים שהלקוח מחפש בפועל, ותמיד אחרי המונח הצרפתי, למשל: « pêne dormant (deadbolt) », « télécommande (key fob) ». מותגים (Schlage, Kwikset, Medeco) נשארים כמו שהם.
- רמת השפה: צרפתית סטנדרטית בינלאומית, תקנית ואיכותית מאוד, ברמה של כותב צרפתי מקצועי. בלי סלנג קוויבקי, בלי ביטויים צרפתיים-פריזאיים מדי.
- הקהל: דוברי צרפתית שגרים בארה"ב (צרפתים, קנדים, האיטים, בלגים, שווייצרים, דוברי צרפתית מאפריקה, לואיזיאנה). לכן: דולרים ($), יחידות אמריקאיות כשצריך, מונחים אמריקאיים (ZIP code, HOA, landlord → « propriétaire bailleur »), מותגים אמריקאיים.
- טיפוגרפיה צרפתית: רווח לפני « ; : ! ? » (סקריפט ה-build ממיר אוטומטית לרווח בלתי שביר), מירכאות « », אותיות רישיות עם הטעמה (À, É).

## 2. קול וטון

- גוף ראשון רבים בלבד: « nous », « on », « notre équipe ». אף פעם לא « l'entreprise » או « le serrurier » בגוף שלישי על עצמנו.
- פונים לקורא ב-« vous ».
- טון: אנושי, חם, ישיר, מקצועי. כמו מנעולן ותיק שמסביר ללקוח בטלפון מה הולך לקרות.
- כותבים מניסיון: מה אנחנו רואים בשטח, מה אנחנו בודקים, מה הטעויות הנפוצות של לקוחות, מתי אנחנו ממליצים לא להחליף. דעה ברורה עדיפה על ניסוח ניטרלי.
- לא ממציאים נתונים, סטטיסטיקות, ציטוטים, ביקורות, לקוחות או סיפורים ספציפיים עם שמות. לא ממציאים מחירים.
- לא מוסיפים שם עסק, טלפון, כתובת או אימייל בתוך הטקסט. הם יגיעו מ-`build.py` (משתני CONFIG) כשיינתנו.

## 3. מבנה עמוד שירות

- פסקאות קצרות: 1 עד 3 משפטים, עד ~60 מילים לפסקה.
- אורך: 650-900 מילים לעמוד שירות.
- H1 אחד. אחריו פתיחה של 2-3 פסקאות שעונה מיד על השאלה של המחפש (חשוב לגוגל ול-AI Overviews / ChatGPT / Perplexity).
- כותרות H2 בניסוח של שאלה או מצב אמיתי של לקוח, למשל « Que faisons-nous en arrivant ? », לא « Avantages de notre service ».
- כל עמוד כולל: גרפיקה (SVG ב-hero, נוצרת אוטומטית לפי `icon`), « fiche express » (3 שורות), שלבי עבודה (3-4), FAQ של 3-4 שאלות (נכנס אוטומטית ל-FAQPage schema).
- תשובות ה-FAQ: משפט ראשון שעונה ישירות, ואז הסבר קצר.
- רשימות רק כשהתוכן באמת רשימה (כלים, סימנים, שלבים). לא להפוך כל פסקה לבולטים.

## 4. קישוריות פנימית (חובה)

- בכל עמוד שירות יש **2 עד 3** קישורים פנימיים בתוך גוף הטקסט, לעמודי שירות רלוונטיים באתר.
- הקישור משולב בתוך משפט טבעי, בהקשר שבאמת קשור, עם anchor text תיאורי בצרפתית (למשל « [faire un rekey de la serrure](/rekey-serrure/) »). אסור « cliquez ici », אסור קישורים בסוף העמוד כרשימה.
- לא לקשר פעמיים לאותו עמוד באותו עמוד, ולא לקשר לעמוד עצמו.
- פורמט כתובת: `/slug/` עם לוכסן בסוף.
- סקריפט `build.py` בודק ומתריע אם עמוד יוצא עם פחות מ-2 או יותר מ-3 קישורים, או עם קישור שבור.

## 5. איסור מוחלט: כתיבה שנשמעת כמו AI או בוט

המטרה: אף משפט באתר לא נראה כמו טקסט שנוצר ע"י בינה מלאכותית. הרשימה מבוססת על מחקר: המדריך "Signs of AI writing" של ויקיפדיה, מחקר Pangram (סימנים שמופיעים פי 2 עד 12 יותר בטקסט AI), ורשימות של מילים שבוטים משתמשים בהן יותר מדי בצרפתית ובאנגלית.

### 5.1 פיסוק וסימנים אסורים
- **אסור מקף ארוך (—) ומקף בינוני (–)**. בכלל. משתמשים בפסיק, נקודה או סוגריים. (ה-build נכשל אם מופיע.)
- אסור אימוג'י, חיצים (→ ⇒), ✅ ⚠ ★, סימנים כמו ≈.
- אסור הדגשה (bold) בתוך פסקאות. מקסימום מילה אחת מודגשת בכל העמוד, ועדיף אפס.
- אסור נקודתיים בכותרות בסגנון « Rapidité : notre priorité ».

### 5.2 מילים וביטויים אסורים (צרפתית)
plonger dans / plongeons · il est essentiel de noter que · il est important de souligner · crucial · essentiel (כשאפשר בלי) · incontournable · primordial · véritable / véritablement · réellement · essentiellement · en effet (בפתיחת משפט) · ainsi (בפתיחת משפט, יותר מפעם אחת בעמוד) · de plus / par ailleurs / en outre (ברצף) · en conclusion / pour conclure / en résumé / en somme · que ce soit pour… ou pour… · dans un monde où… · à l'ère de… · au cœur de · naviguer (במובן מטאפורי) · paysage (במובן מטאפורי) · un éventail de · une gamme complète de · solutions sur mesure · expertise inégalée · service de qualité supérieure · tranquillité d'esprit (מותר פעם אחת לכל היותר באתר כולו) · n'hésitez pas à · faire la différence · optimal / optimiser · garantir votre sécurité · votre sécurité est notre priorité · fiable et efficace · rapide et efficace · professionnel et courtois · effectuer (→ faire) · utiliser (כשאפשר se servir de / prendre) · débuter (→ commencer) · faciliter · proactif · holistique · robuste · synergie · levier · « Bien sûr ! » · « Excellente question ».

### 5.3 תבניות אסורות
- « Ce n'est pas X, c'est Y » / « Il ne s'agit pas seulement de X, mais de Y ».
- « Non seulement X, mais aussi Y ».
- שלשות קבועות: שלושה שמות תואר או שלושה פריטים ברצף בכל משפט שני (« rapide, fiable et abordable »). אם יש רשימה, שיהיו בה 2, 4 או 5 פריטים לפעמים.
- פתיחה ב"חימום": « Vous êtes-vous déjà demandé… », « Imaginez la scène… », « Dans cet article, nous allons voir… ».
- סיכום שחוזר על כל העמוד בסוף. העמוד נגמר כשנגמר התוכן.
- טקסט שמחמיא לעצמו (« notre service exceptionnel », « une équipe passionnée »).
- ניפוח חשיבות: « joue un rôle clé », « représente un enjeu majeur », « témoigne de ».
- שני משפטים קצרים מודבקים לאפקט דרמטי ברצף (« Rapide. Efficace. »).
- גידור יתר: « peut potentiellement », « dans certains cas, il se peut que ».
- כל הפסקאות באותו אורך ובאותו מבנה. צריך לגוון: משפט קצר, משפט ארוך, שאלה, משפט עם מספר מדויק.
- כל H2 באותו תבנית דקדוקית. לגוון.
- טון חיובי מדי לאורך כל הטקסט. מותר להגיד « ça arrive souvent et c'est agaçant », מותר להגיד ללקוח שהוא לא צריך שירות.

### 5.4 מה כן עושים כדי להישמע אנושי
- פרטים מוחשיים מהשטח: שם של מנגנון (cylindre, goupilles, gâche, pêne demi-tour), מותגים, מצבים אמיתיים (« la clé tourne dans le vide », « la porte frotte en hiver »).
- מספרים מדויקים ולא טווחים כלליים, רק כשהם עובדות ידועות (למשל « un cylindre standard compte cinq ou six goupilles »).
- דעה: « Honnêtement, pour une porte de garage qui ne sert jamais, on vous déconseille la serrure connectée. »
- לגוון אורך משפטים. מותר להתחיל משפט ב-« Et » או « Mais ».
- לכתוב כמו שמדברים עם לקוח, לא כמו חוברת שיווקית.

## 6. SEO ו-AI Search

- meta title: עד ~60 תווים, מילת מפתח עיקרית בהתחלה, בצרפתית.
- meta description: 140-160 תווים, משפט שעונה ומזמין.
- slug: צרפתית בלי הטעמות, מילים מופרדות במקף, קצר.
- מילת המפתח העיקרית ב-H1, בפסקה הראשונה ובאחד ה-H2, באופן טבעי. בלי דחיסה.
- פסקת הפתיחה עונה על השאלה בתוך 40-60 מילים (מצוטטת ע"י מנועי AI).
- schema נוצר אוטומטית: WebPage, Service, BreadcrumbList, FAQPage. כשיתקבלו פרטי העסק, מוסיפים Locksmith (LocalBusiness) ב-CONFIG.
- `llms.txt` ו-`sitemap.xml` נוצרים אוטומטית.

## 7. טכני

- HTML/CSS טהור. מקור התוכן: `content/pages/*.md` (YAML front matter + Markdown). הרצת `python3 build.py` מייצרת את האתר הסטטי בתיקייה `public/` שמתפרסמת ב-Vercel.
- אין JavaScript חיצוני, אין ספריות, אין תמונות כבדות. גרפיקה = SVG inline. פונט אחד בלבד (Fraunces 600, woff2, preload), שאר הטקסט בפונט מערכת.
- CSS inline בכל עמוד (אין בקשה חוסמת).
- פרטי העסק (שם, טלפון, כתובת, אימייל, דומיין) נמצאים ב-CONFIG בראש `build.py`. כל עוד הם ריקים, הם לא מוצגים באתר.
- לפני כל commit: `python3 build.py` חייב לעבור בלי שגיאות ובלי אזהרות.

## 8. הוספת עמוד חדש

1. יוצרים `content/pages/<slug>.md` לפי המבנה של עמוד קיים.
2. בוחרים `icon` מתוך האייקונים ב-`icons.py` (או מוסיפים אייקון חדש).
3. מוסיפים 2-3 קישורים פנימיים בגוף הטקסט, וכדאי גם לעדכן 1-2 עמודים קיימים כך שיקשרו לעמוד החדש (בלי לעבור את המקסימום של 3).
4. מריצים `python3 build.py`, מתקנים אזהרות, עושים commit ו-push.
