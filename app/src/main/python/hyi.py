# ייבוא חבילת גמטריה לצורך מידע על שנה עברית
import gematriapy as gy

# יבוא חבילת לוח עברי בפייתון
from pyluach import dates, hebrewcal, parshios, gematria, utils

#-------------------------------------------------------------------------
# פונקציות עבור התוכנות הנספחות לכוכבים וזמנים אשר ניתנות לשימוש גם בתוכניות אחרות

# פונקצייה להמרה ממספר השנה העברית לשנה לועזית מקבילה
# אם השנה הלועזית היא במינוס צריך להוסיף עוד שנה כי אין שנה לועזית אפס. אלא שנה עברית 3761 היא שנה 1 לועזית ושנה עברית 3760 היא שנה מינוס אחד
# כברירת מחדל אין שנה לועזית 0
# באמת אצל ההיסטוריונים אכן אין שנת 0 אבל אצל האסטרונומים יש שנת 0
def int_heb_year_to_loazit_year(int_heb_year, loazit_year_zero=-1):
    if loazit_year_zero == -1:
        return int_heb_year - 3760 if int_heb_year >= 3761 else int_heb_year - 3761
    elif loazit_year_zero == 0:
        return int_heb_year - 3760

# פונקציית להדפסת שנה לועזית המקבילה לשנה עברית הכוללת טיפול בשתי שיטות הספירה (עם שנת אפס או בלי שנת אפס) עבור שנים שלפני הספירה הנוצרית
def string_heb_year_to_loazit_year_plus_zero(int_heb_year):
    return f'[שנה לועזית: {int_heb_year_to_loazit_year(int_heb_year)}; (או: {int_heb_year_to_loazit_year(int_heb_year, loazit_year_zero=0)} לשיטה המקובלת באסטרונומיה שקיימת שנה אפס)]' if int_heb_year_to_loazit_year(int_heb_year) <=0 else f'[שנה לועזית: {int_heb_year_to_loazit_year(int_heb_year)}]'

# פונקצייה להמרת שמות חודשים עבריים למספרים ברירת המחדל היא מניסן לאדר וכך מספרי החודשים הם כפי שמקובל בספריית פיי-לוח
def heb_month_name_to_number(heb_month_name, start = "nissan"):
    months_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,12,13] if start == "nissan" else [7,8,9,10,11,12,1,2,3,4,5,6,13,6]
    months_names = ['ניסן','אייר','סיוון','תמוז','אב','אלול','תשרי','מְרַחשְׁוָון','כִּסְלֵיו','טבת','שבט','אדר','אדר-א','אדר-ב']
    for name in range(len(months_names)):
        if months_names[name] == heb_month_name:
            return months_numbers[name]

# הגדרת פונקציית מציאת מספר השנה במחזור 28 שנות חמה לתקופת שמואל "מחזור גדול", עם תנאי ש 0 שווה 28 וכן מספר המחזור שאוחזים בו
def chishuv_shana_bemachzor_28(heb_year):
    machzor_28 = int(heb_year / 28) + 1
    shana_bemachzor_28 = heb_year % 28
    if shana_bemachzor_28 == 0:
        shana_bemachzor_28 = 28
        machzor_28 -= 1
    return machzor_28, shana_bemachzor_28

# הגדרת פונקציית מציאת מספר השנה במחזור 19 השנים הפשוטות והמעוברות "מחזור קטן", עם תנאי ש 0 שווה 19 וכן מספר המחזור שאוחזים בו
# הפונקצייה גם מחזירה האם השנה מעוברת או לא
def chishuv_shana_bemachzor_19(heb_year):
    machzor_19 = int(heb_year / 19) + 1
    shana_bemachzor_19 = heb_year % 19
    if shana_bemachzor_19 == 0:
        shana_bemachzor_19 = 19
        machzor_19 -= 1
    # בדיקה שמחזירה "נכון" אם השנה העברית מעוברת, ו"לא נכון" אם השנה העברית לא מעוברת אלא פשוטה
    meuberet_year = True if shana_bemachzor_19 in [3,6,8,11,14,17,19] else False
    return machzor_19, shana_bemachzor_19, meuberet_year

# פונקצייה שמחזירה "נכון" אם השנה העברית מעוברת, ו"לא נכון" אם השנה העברית לא מעוברת אלא פשוטה
def shana_meuberet(heb_year_bemachzor_19):
    return heb_year in [3,6,8,11,14,17,19]

# הגדרת פונקציית המרה  מ- רשימה הכוללת יום שעה וחלק, אל- חלקים, שלא בתוך רשימה
# פונקציה זו אינה שימושית כרגע בתוכנית זו
def convert_to_chalakim(arr_yom_shaa_chelek):
    yom = arr_yom_shaa_chelek[0]
    shaa = arr_yom_shaa_chelek[1]
    chelek = arr_yom_shaa_chelek[2]
    chalakim = yom * (24 * 1080) + (shaa * 1080) + chelek
    return chalakim

# הגדרת פונקציית המרה מ-חלקים אל- יום שעה וחלק
# חייבים להוסיף 0.0000000001 כדי למנוע שגיאת עיגול עשרונית שעושה חלק אחד פחות
def convert_from_chalakim(chalakim):
    yom = int(chalakim / (24 * 1080))
    shaa = int((chalakim / (24 * 1080) - yom) * 24 + 0.0000000001)
    chelek = int((((chalakim / (24 * 1080) - yom) * 24 + 0.0000000001) - shaa) * 1080)
    # תיקון יום 0 שווה ל 7
    if yom == 0:
        yom = yom + 7
    return [yom, shaa, chelek]


# פונקצייה לחישוב שם היום בעברית עבור מספר יום בשבוע, מיום ראשון עד שבת: לדוגמא יום 1 הוא יום ראשון
def heb_string_day(day):

    heb_string_days = {
        1: 'ראשון',
        2: 'שני',
        3: 'שלישי',
        4: 'רביעי',
        5: 'חמישי',
        6: 'שישי',
        7: 'שבת'
    }

    return heb_string_days.get(day)

# פונקצייה לחישוב שם היום באנגלית עבור מספר יום בשבוע, מיום ראשון עד שבת: לדוגמא יום 1 הוא יום ראשון
def en_string_day(day):

    en_string_days = {
        1: 'Sunday',
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        5: 'Thursday',
        6: 'Friday',
        7: 'Saturday'
    }

    return en_string_days.get(day)


# פונקצייה לחישוב אות היום בעברית עבור מספר יום בשבוע, מיום ראשון עד שבת: לדוגמא יום 1 הוא יום א
def heb_letter_day(day):

    heb_letters_days = {
        1: 'א',
        2: 'ב',
        3: 'ג',
        4: 'ד',
        5: 'ה',
        6: 'ו',
        7: 'ז'
    }

    return heb_letters_days.get(day)


# פונקצייה לקבל שם של כל אחד מהכיוונים שיש בעולם לפי מספר האזימוט כשבר עשרוני
# חובר בעזרת צ'אט גיפיטי
def get_side_name(azimuth):

    directions = {
        0.0: "צפון",
        45.0: "צפון-מזרח",
        90.0: "מזרח",
        135.0: "דרום-מזרח",
        180.0: "דרום",
        225.0: "דרום-מערב",
        270.0: "מערב",
        315.0: "צפון-מערב"
    }
    # זה מה שיהיה כתוב אם הוכנס ערך שגוי
    side_name = "לא ניתן לקבוע כיוון"

    # בדיקה של ערך מדויק
    if azimuth in directions:
        side_name = directions[azimuth]
    else:
        # בדיקה של ערך קרוב לגבול של ערך קיים בטווח של 22.5 מעלות מכל ערך קיים
        for key in directions:
            if key - 22.5 <= azimuth <= key + 22.5:
                side_name = directions[key]
                break

    return side_name



# פונקצייה שמחזירה מידע בכמה תקופת ניסן לפי שמואל מקדימה את מולד ניסן בלוח העברי הקבוע
# פונקצייה זו מבוססת על נוסחאות שבספר שערים ללוח העברי מאת רחמים שר שלום, עמוד 148
def kama_tkufat_nissan_shmuel_lifnei_mold_nisan(heb_year):

    # חישוב מה מספר המחזור שאוחזים בו ומה מספר השנה בתוך המחזור במחזור 19 השנים באמצעות פונקצייה
    machzor_19, shana_bemachzor_19, _ = chishuv_shana_bemachzor_19(heb_year)
    machzorim_shlemim_sheavru = machzor_19 - 1

    # א-תפה: עודף תקופת שמואל על תקופת רב אדא ב-19 שנות המחזור
    atapa_bechalakim = 1565
    # ז-ט-תרמב בחלקים: שיעור הקדימה של תקופת ניסן למולד ניסן בשנה א של המחזור
    zatarmab_bechalakim = 191802

    # הגדרת משתנים עבור המילון
    # (ירח) הפיכה לחלקים של 10 ימים + 21 שעות + 204 חלקים. זהו העודף שיש בשנת חמה של שמואל על 12 חודשים של הלוח העברי
    a = 282084
    # הפיכה לחלקים של 18 ימים + 15 שעות + 589 חלקים. זהו העודף שיש ב 13 חודשי לוח עברי (ירח) על שנת שמש של שמואל
    b = 483349

    # מילון לחישוב כמה חלקים יש להוסיף או להפחית עבור שנים שהם לא השנה הראשונה במחזור
    milon_shmuel = {
        1:0,
        2:a,
        3:a-b,
        4:(2*a)-b,
        5:(3*a)-b,
        6:(3*a)-(2*b),
        7:(4*a)-(2*b),
        8:(4*a)-(3*b),
        9:(5*a)-(3*b),
        10:(6*a)-(3*b),
        11:(6*a)-(4*b),
        12:(7*a)-(4*b),
        13:(8*a)-(4*b),
        14:(8*a)-(5*b),
        15:(9*a)-(5*b),
        16:(10*a)-(5*b),
        17:(10*a)-(6*b),
        18:(11*a)-(6*b),
        19:(11*a)-(7*b),
    }

    # תשובה בכמה חלקים מקדימה תקופת ניסן את מולד ניסן בשנה המבוקשת
    tshuva_bechalakim = machzorim_shlemim_sheavru * atapa_bechalakim - zatarmab_bechalakim + milon_shmuel.get(shana_bemachzor_19)
    # תשובה בחלוקה ליום שעה וחלק
    tshuva = convert_from_chalakim(abs(tshuva_bechalakim))
    return tshuva

# פונקצייה להחזרת מספר השנים שחלפו מאז חורבן בית שני
def get_shana_lechurban_bait_sheni(heb_year_int):
    shnat_hachurban = 3830
    if heb_year_int < shnat_hachurban:
        return f"שנת {abs(heb_year_int - shnat_hachurban + 2)} !לפני! חורבן בית המקדש השני שאירע בשנת ג'תתל (שנת 70 לספירת הנוצרים)"
    return f"שנת {heb_year_int - shnat_hachurban + 1} לחורבן בית המקדש השני שאירע בשנת ג'תתל (שנת 70 לספירת הנוצרים)"

# פונקצייה שמקבלת מספר שנה עברית ומחזירה איזו שנה לשמיטה והאם זו שנת מעשר עני
def get_shana_lashmita_and_maasrot(heb_year_int):
    A = heb_year_int % 7
    shana_lashmita = 7 if A == 0 else A
    shnat_maasrot = "מעשר שני" if shana_lashmita in [1,2,4,5] else "מעשר עני" if shana_lashmita in [3,6] else "שמיטה-הפקר: אין תרומות ומעשרות"
    return shana_lashmita, shnat_maasrot

# הגדרת פונקציית מציאת מספר השנה במחזור 28 שנות חמה לתקופת שמואל המכונה "מחזור גדול", עם תנאי ש 0 שווה 28 וכן מספר המחזור שאוחזים בו
# הפונקצייה גם מחזירה האם השנה מעוברת או לא
def chishuv_shana_bemachzor_28(heb_year):
    machzor_28 = int(heb_year / 28) + 1
    shana_bemachzor_28 = heb_year % 28
    if shana_bemachzor_28 == 0:
        shana_bemachzor_28 = 28
        machzor_28 -= 1
    return shana_bemachzor_28, machzor_28




# הגדרות של פונקציות משתמש

##############################

# הגדרת משתנים כלליים לצורך הפונקציות והחישובים
itaron_chodesh_bechalakim = 39673
molad_baharad_bechalakim = 57444
shavua_bechalakim = 181440


######################

#---------------------------------------------------


# הגדרת פונקציית נוסחת לוינגר שמראה כמה חודשים עברו ממולד בהר"ד עד מולד תשרי של שנה מסויימת
def nuschat_levinger(heb_year):
    sum_heb_months_be_over_from_molad_baharad = int((235 * (heb_year-1) +1) / 19)
    return sum_heb_months_be_over_from_molad_baharad

# מציאת מולד תשרי בחלקים על פי נוסחת לוינגר
# התרגיל הוא הכפלת תוצאת נוסחת לוינגר (מספר החודשים שעברו מבהר"ד) בייתרון חודש בחלקים, הוספת התוצאה לבהר"ד בחלקים, והחלת מודולו שבוע בחלקים על התוצאה הכללית
def chishuv_molad_tishrei_bechalakim(sum_heb_months_be_over_from_molad_baharad):
    molad_tishrei_bechalakim = (sum_heb_months_be_over_from_molad_baharad * itaron_chodesh_bechalakim + molad_baharad_bechalakim) % shavua_bechalakim
    return molad_tishrei_bechalakim


# הקדמה והסבר לפונקצייה הבאה העוסקת בדחיות ראש השנה

# מולד תשרי ביום 1 יכול להיות רק דחיית אד"ו שדוחה ביום אחד.
# מולד תשרי ביום 2 : בכל שנה יכול להיות דחיית זקן שדוחה ביום אחד; ובשנה פשוטה שהיא מוצאי מעוברת יכול להיות דחיית בט"ו תקפ"ט שדוחה ביום אחד.
# מולד תשרי ביום 3: בכל שנה יכול להיות דחיית זקן שדוחה ביומיים (בגלל אד"ו); ובכל שנה פשוטה יכול להיות גם דחיית גטר"ד שדוחה ביומיים (בגלל אד"ו).
# מולד תשרי ביום 4: יכול להיות רק דחיית אד"ו שדוחה ביום אחד.
# מולד תשרי ביום 5: בכל שנה יכול להיות דחיית זקן שדוחה ביומיים (בגלל אד"ו).
# מולד תשרי ביום 6: יכול להיות רק דחיית אד"ו שדוחה ביום אחד.
# מולד תשרי ביום 7: בכל שנה יכול להיות דחיית זקן שדוחה ביומיים (בגלל אד"ו).
# לסיכום: לפי דחיות של ימים, יש שני סוגים: דחייה של יום אחד, או דחייה של יומיים.


# הגדרת פונקציית דחיות ראש השנה. הפונקציה פועלת על שני משתנים:
# הראשון הוא רשימה המכילה את מולד תשרי בשלושה איברים. בדרך כלל רשימת מולד תשרי מתקבלת מהפונקציה המרה מ-חלקים
# השני הוא: משתנה שמכיל את מספר השנה במחזור 19 שנים נתון זה בדרך כלל מתקבל מתוך הפונקצייה סיכום
def dechiot(arr_molad_tishrei,shana_bemachzor_19):
    yom = arr_molad_tishrei[0]
    shaa = arr_molad_tishrei[1]
    chelek = arr_molad_tishrei[2]
    # מקרים שבהם ראש השנה של השנה המבוקשת נדחה ביום אחד: 1. אד"ו (תמיד), 2. זקן בשני, 3. ב-טו-תקפט בפשוטה שהיא מוצאי מעוברת
    if (yom in (1,4,6)) or (yom == 2 and shaa >= 18) or (shana_bemachzor_19 in (4,7,9,12,15,18,1) and yom == 2 and shaa >= 15 and chelek >= 589):
        rosh_hashana_weekday = (yom + 1) % 7
        dechia = 1
    # מקרים שבהם ראש השנה של השנה המבוקשת נדחה ביומיים: 1. זקן בשלישי חמישי או שבת, 2. ג-ט-רד בכל שנה פשוטה
    elif (yom in (3,5,7) and shaa >= 18) or (shana_bemachzor_19 not in (3,6,8,11,14,17,19) and yom == 3 and shaa >= 9 and chelek >= 204):
        rosh_hashana_weekday = (yom + 2) % 7
        dechia = 2
    # בכל המקרים האחרים ראש השנה של השנה המבוקשת לא נדחה, אלא הוא ביום מולד תשרי של השנה המבוקשת
    else:
        rosh_hashana_weekday = yom
        dechia = 0
    # תיקון יום 0 שווה ל 7 {לא יודע למה אבל התיקון לא פועל על שנת 5303. עדכון: כנראה כבר תוקן ופועל גם על 5303}
    if rosh_hashana_weekday == 0:
        rosh_hashana_weekday = rosh_hashana_weekday + 7
    return rosh_hashana_weekday, dechia



# פונקציה המפעילה מספר פונקציות ונותנת רשימה המכילה סיכום של 7 נתונים על שנה מסויימת
# הנתונים שרשימת הסיכום כוללת הם: מספר המחזור ממחזור 19 שנים ומספר השנה במחזור, מספר החודשים שחלפו מבהר"ד, מולד תשרי בחלקים, מולד תשרי לפי יום שעה וחלק, יום בשבוע עבור ראש השנה, האם ראש השנה נדחה ובכמה ימים
def sikum(heb_year):
    machzor_19, shana_bemachzor_19, meuberet_year = chishuv_shana_bemachzor_19(heb_year)
    sum_heb_months_be_over_from_molad_baharad = nuschat_levinger(heb_year)
    molad_tishrei_bechalakim = chishuv_molad_tishrei_bechalakim(sum_heb_months_be_over_from_molad_baharad)
    molad_tishrei = convert_from_chalakim(molad_tishrei_bechalakim)
    rosh_hashana_weekday, dechia = dechiot(molad_tishrei,shana_bemachzor_19)
    return [machzor_19,shana_bemachzor_19, sum_heb_months_be_over_from_molad_baharad, molad_tishrei_bechalakim, molad_tishrei, rosh_hashana_weekday, dechia]


# הגדרת פונקצייה שמחשבת את 13 המולדות הממוצעים בחלקים, שבאים לאחר מולד תשרי של השנה המבוקשת, מתוך מולד תשרי של השנה המבוקשת
# הפונקציה מחזירה רשימה של 13 או 14 מולדות ממוצעים בחלקים, הכוללת את מולד תשרי בחלקים של השנה המבוקשת וכן את המולדות בחלקים של 13 או 14 החודשים הבאים
# אם השנה המבוקשת היא פשוטה, הפונקציה מחזירה רשימה של 13 איברים כי זה כולל מולד תשרי הזה וגם מולד תשרי הבא
# אם השנה המבוקשת היא מעוברת הפונקציה מחזירה רשימה של 14 איברים כנ"ל.
def moladot_chodashim_bechalakim(molad_tishrei_bechalakim, shana_bemachzor_19):
    a = molad_tishrei_bechalakim
    b = (a + itaron_chodesh_bechalakim) % shavua_bechalakim
    c = (b + itaron_chodesh_bechalakim) % shavua_bechalakim
    d = (c + itaron_chodesh_bechalakim) % shavua_bechalakim
    e = (d + itaron_chodesh_bechalakim) % shavua_bechalakim
    f = (e + itaron_chodesh_bechalakim) % shavua_bechalakim
    g = (f + itaron_chodesh_bechalakim) % shavua_bechalakim
    h = (g + itaron_chodesh_bechalakim) % shavua_bechalakim
    i = (h + itaron_chodesh_bechalakim) % shavua_bechalakim
    j = (i + itaron_chodesh_bechalakim) % shavua_bechalakim
    k = (j + itaron_chodesh_bechalakim) % shavua_bechalakim
    l = (k + itaron_chodesh_bechalakim) % shavua_bechalakim
    m = (l + itaron_chodesh_bechalakim) % shavua_bechalakim
    n = (m + itaron_chodesh_bechalakim) % shavua_bechalakim
    if shana_bemachzor_19 in (3,6,8,11,14,17,19):
        return [a,b,c,d,e,f,g,h,i,j,k,l,m,n]
    else:
        return [a,b,c,d,e,f,g,h,i,j,k,l,m]


# הגדרת פונקצייה שלוקחת עותק של הרשימה המתקבלת מפונקציית חישוב מולדות חודשים בחלקים
# וממירה בו כל מולד ל-יום שעה וחלק כך שמתקבלת רשימת של המולדות לפי יום שעה וחלק
def moladot_chodashim(arr_moladot_chodashim_bechalakim):
    a = arr_moladot_chodashim_bechalakim.copy()
    for i in range(len(a)):
        a[i] = convert_from_chalakim(a[i])
    arr_moladot_chodashim = a
    return arr_moladot_chodashim


# פונקצייה לחישוב סימן השנה של שנה עברית, והפרש הימים בין שני ראשי השנה
def siman_hashana(rosh_hashana_1_weekday, rosh_hashana_2_weekday, shana_1_bemachzor_19):

    siman_hashana_A = heb_letter_day(rosh_hashana_1_weekday)


    # חישוב האות האמצעית של סימן השנה כלומר האם השנה המבוקשת היא חסרה כסדרה או שלמה, (ולפי זה ניתן לדעת כמה ימים יש בשנה המבוקשת)
    # חסרה (מרחשוון וכסליו חסרים), כסדרה (מרחשוון חסר וכסליו מלא), או שלמה (מרחשוון וכסליו מלאים)

    # שלב ראשון, חישוב פער הימים בין בין ראש השנה של השנה שלאחריה לבין ראש השנה של השנה המבוקשת כהקדמה לחישוב גד"ה הו"ז
    efresh = (rosh_hashana_2_weekday - rosh_hashana_1_weekday) % 7
    if efresh == 0:
        efresh = efresh + 7

    # שלב שני, חישוב גד"ה הו"ז והסקה ממנו של האות האמצעית של סימן השנה. ח=8, כ=20, ש=300
    if efresh == 3:
        siman_hashana_B = "ח"
    elif efresh == 4:
        siman_hashana_B = "כ"
    #--------------------------------------------
    elif efresh == 5 and shana_1_bemachzor_19 not in (3,6,8,11,14,17,19):
        siman_hashana_B = "ש"
    elif efresh == 5 and shana_1_bemachzor_19 in (3,6,8,11,14,17,19):
        siman_hashana_B = "ח"
    #--------------------------------------------
    elif efresh == 6:
        siman_hashana_B = "כ"
    elif efresh == 7:
        siman_hashana_B = "ש"


    # חישוב האות האחרונה של סימן השנה, כלומר: חישוב באיזה יום בשבוע יחול פסח של השנה המבוקשת
    pesach_1_weekday = (rosh_hashana_2_weekday - 2) % 7
    if pesach_1_weekday == 0:
        pesach_1_weekday = pesach_1_weekday + 7

    siman_hashana_C = heb_letter_day(pesach_1_weekday)

    return [siman_hashana_A, siman_hashana_B, siman_hashana_C], efresh



# פונקציית מיין: סיכום סופי והדפסות עם הגדרות מיוחדות עבור ממשק משתמש גרפי של טקינטר
# פונקצייה זו מופעלת באמצעות הכפתור "חשב נתונים"
def main_result(year):

    # קלט תאריך מהמשתמש
    #kelet = Entry_heb_year.get().replace(' ','').replace("׳","'")

    kelet = year

    #ניסיון לחשב נתונים מתוך שדה קלט עברי
    try:
        # המרת התאריך שהוזן, למספרים וחלוקה למשתנים נפרדים עבור יום חודש ושנה
        shana1 = int(kelet)
    except:

        if "-" in kelet:
            split_kelet = kelet.split("-")
            shana1 = int(split_kelet[1])

        elif "'" in kelet:
            split_kelet = kelet.split("'")
            shana1 = (gy.to_number(split_kelet[0]) * 1000) + gy.to_number(split_kelet[1])
            #print(gy.to_number(split_kelet[1]))

        else:
            if len(kelet) > 0:
                shana1 = gy.to_number(kelet)

    #--------------------

    # חישוב 7 נתונים על השנה המבוקשת באמצעות פונקציית סיכום
    arr_sikum_shana_1 = sikum(shana1)

    # שמירה במשתנים נפרדים של 7 הנתונים המתקבלים מפונקציית סיכום
    machzor_19_shana_1 = arr_sikum_shana_1[0]
    shana_1_bemachzor_19 = arr_sikum_shana_1[1]
    sum_heb_months_be_over_from_molad_baharad_to_shana_1 = arr_sikum_shana_1[2]
    molad_tishrei_1_bechalakim = arr_sikum_shana_1[3]
    molad_tishrei_1 = arr_sikum_shana_1[4]
    rosh_hashana_1_weekday = arr_sikum_shana_1[5]
    dechia1 = arr_sikum_shana_1[6]

    # מכאן והלאה: חישוב כל הנ"ל עבור השנה שלאחריה שהיא השנה הבאה לאחר השנה שהזין המשתמש

    # הגדרה מהי השנה שלאחריה
    shana2 = shana1 + 1

    # חישוב 7 נתונים על השנה שלאחריה באמצעות פונקציית סיכום
    arr_sikum_shana_2 = sikum(shana2)

    # שמירה במשתנים נפרדים של 7 הנתונים המתקבלים מפונקציית סיכום
    machzor_19_shana_2 = arr_sikum_shana_2[0]
    shana_2_bemachzor_19 = arr_sikum_shana_2[1]
    sum_heb_months_be_over_from_molad_baharad_to_shana_2 = arr_sikum_shana_2[2]
    molad_tishrei_2_bechalakim = arr_sikum_shana_2[3]
    molad_tishrei_2 = arr_sikum_shana_2[4]
    rosh_hashana_2_weekday = arr_sikum_shana_2[5]
    dechia2 = arr_sikum_shana_2[6]

    # מכאן והלאה סיכומים כלליים על השנה המבוקשת

    '''# בדיקת תאריך לועזי של ראש השנה בשנה המבוקשת באמצעות חבילת פיי-לוח
    rosh_hashana_heb_pyluach = dates.HebrewDate(shana1, 7, 1)
    rosh_hashana_greg_pyluach = rosh_hashana_heb_pyluach.to_greg()

    # בדיקת תאריך לועזי של פסח בשנה המבוקשת באמצעות חבילת פיי-לוח
    pesach_heb_pyluach = dates.HebrewDate(shana1, 1, 15)
    pesach_greg_pyluach = pesach_heb_pyluach.to_greg()'''


    # סיכום סימן השנה של השנה המבוקשת, והפרש הימים בשבוע בין שני ראשי השנה
    siman_hashana_1, efresh = siman_hashana(rosh_hashana_1_weekday, rosh_hashana_2_weekday, shana_1_bemachzor_19)

    #------------------------------
    # הגדרת היום בשבוע שבו יחולו מספר מועדים בשנה המבוקשת
    pesach_weekday = gy.to_number(siman_hashana_1[2])

    yom_kipur_weekday = (rosh_hashana_1_weekday + 2) % 7
    if yom_kipur_weekday == 0:
        yom_kipur_weekday = yom_kipur_weekday + 7

    sukot_weekday = rosh_hashana_1_weekday

    shavuot_weekday = (pesach_weekday + 1) % 7

    if siman_hashana_1[1] == "ש":
        chanuka_weekday = rosh_hashana_1_weekday
    else:
        chanuka_weekday = (rosh_hashana_1_weekday - 1) % 7

    purim_weekday = (pesach_weekday - 2) % 7

    tisha_beav_weekday = pesach_weekday

    #-----------------------------------------

    # מכאן והלאה חישוב מולדות ממוצעים של כל חודשי השנה המבוקשת

    # קריאה לפונקציית חישוב מולדות חודשים בחלקים, ושמירה של התוצאה
    moladot_chodashim_bechalakim_1 = moladot_chodashim_bechalakim(molad_tishrei_1_bechalakim, shana_1_bemachzor_19)

    # קריאה לפונקציית מולדות חודשים על עותק של מולדות חודשים בחלקים, ושמירת התוצאות
    moladot_chodashim_1 = moladot_chodashim(moladot_chodashim_bechalakim_1)

    # הגדרת רשימות המשמשות את ההדפסה של פונקציית חישוב מולדות חודשים
    chodashim_pshuta = ["תשרי", "מְרַחשְׁוָון", "כִּסְלֵיו", "טבת", "שבט", "אדר", "ניסן", "אייר", "סיוון", "תמוז", "אב", "אלול", "תשרי שלאחריה"]
    chodashim_meuberet = ["תשרי", "מְרַחשְׁוָון", "כסלו", "טבת", "שבט", "אדר ראשון", "אדר שני", "ניסן", "אייר", "סיוון", "תמוז", "אב", "אלול", "תשרי שלאחריה"]
    # עד כאן חישוב מולדות ממוצעים של כל חודשי השנה המבוקשת

    # חישוב מרחק תקופת ניסן לשמואל ממולד ניסן באמצעות פונקצייה
    tshuva = kama_tkufat_nissan_shmuel_lifnei_mold_nisan(shana1)

    # פונקצייה שמחזירה את מספר השנה העברית באותיות ומשתמשת בסיפריית גימטרייה של פיילוח
    def heb_year_string(heb_year, thousands=True, withgershayim=True):
        return gematria._num_to_str(heb_year, thousands=thousands, withgershayim=withgershayim)

    # קבלת מידע על השנה לשמיטה למעשרות ולחורבן ולמחזור 28 שנות חמה באמצעות פונקציות שהגדרתי למעלה
    shana_lashmita, shnat_maasrot = get_shana_lashmita_and_maasrot(shana1)
    shana_lechurban_bait_sheni = get_shana_lechurban_bait_sheni(shana1)
    shana_1_bemachzor_28, machzor_28_shana_1 = chishuv_shana_bemachzor_28(shana1)

    #-----------------------------------------------------------------------
    ############  כל ההדפסות ###############

    hyi_result = []


    # ההדפסות עצמן
    hyi_result.append("#####   תקציר   #####")
    hyi_result.append(f'השנה המבוקשת היא: {shana1} - {heb_year_string(shana1)}')
    hyi_result.append(f'{string_heb_year_to_loazit_year_plus_zero(shana1)}')
    hyi_result.append("")

    # הדפסות של מספר ימי השנה של השנה המבוקשת
    if efresh == 3:
        hyi_result.append("השנה המבוקשת היא שנה פשוטה חסרה (כלומר: בת 353 ימים, מְרַחשְׁוָון וכסליו חסרים)")
    elif efresh == 4:
        hyi_result.append("השנה המבוקשת היא שנה פשוטה כסדרה (כלומר: בת 354 ימים, מְרַחשְׁוָון חסר וכסליו מלא)")
    #--------------------------------------------
    elif efresh == 5 and shana_1_bemachzor_19 not in (3,6,8,11,14,17,19):
        hyi_result.append("השנה המבוקשת היא שנה פשוטה שלמה (כלומר: בת 355 ימים, מְרַחשְׁוָון וכסליו מלאים)")
    elif efresh == 5 and shana_1_bemachzor_19 in (3,6,8,11,14,17,19):
        hyi_result.append("השנה המבוקשת היא שנה מעוברת חסרה (כלומר: בת 383 ימים, מְרַחשְׁוָון וכסליו חסרים)")
    #--------------------------------------------
    elif efresh == 6:
        hyi_result.append("השנה המבוקשת היא שנה מעוברת כסדרה (כלומר: בת 384 ימים, מְרַחשְׁוָון חסר וכסליו מלא)")
    elif efresh == 7:
        hyi_result.append("השנה המבוקשת היא שנה מעוברת שלמה (כלומר: בת 385 ימים, מְרַחשְׁוָון וכסליו מלאים)")
    hyi_result.append("")

    hyi_result.append(f'סימן השנה של השנה המבוקשת הוא:    {siman_hashana_1[0]} {siman_hashana_1[1]} {siman_hashana_1[2]}')
    hyi_result.append("")
    hyi_result.append("[אות ימנית: יום בשבוע שיחול בו ראש השנה]")
    hyi_result.append("[אות אמצעית: האם השנה ח = חסרה, כ = כסדרה, או: ש = שלמה]")
    hyi_result.append("[אות שמאלית: יום בשבוע שיחול בו חג ראשון של פסח]")

    # הדפסות מידע על נתונים נוספים על השנה שנה לשמיטה למעשרות ולחורבן
    hyi_result.append("—————————————————————")
    hyi_result.append("מידע נוסף על השנה המבוקשת")
    hyi_result.append("")
    hyi_result.append(f'מספר השנה במניין שמות השמיטה הוא:   {shana_lashmita}')
    hyi_result.append(f'לפיכך, המעשר שמפרישים השנה הוא:   {shnat_maasrot}')
    hyi_result.append(f'שימו לב שלגבי פירות האילן, שנת המעשרות הנוכחית נכונה רק החל מיום ט"ו בשבט')
    hyi_result.append(f'מספר השנה המבוקשת במחזור קטן (19 שנים פשוטות ומעוברות) הוא: {shana_1_bemachzor_19}   (במחזור {machzor_19_shana_1})')
    hyi_result.append(f'מספר השנה המבוקשת במחזור גדול (28 שנות חמה) הוא: {shana_1_bemachzor_28}   (במחזור {machzor_28_shana_1})')
    hyi_result.append(f'(מספר השנה במחזור הגדול, נכון רק החל מיום תקופת ניסן לשיטת שמואל והלאה - ראו להלן)')
    hyi_result.append(f"זוהי {shana_lechurban_bait_sheni}")

    # הדפסות מידע על נתונים נוספים שאפשר להסיק מתוך סימן השנה
    hyi_result.append("—————————————————————")
    hyi_result.append("מידע על היום בשבוע שבו יחולו מועדים שונים בשנה המבוקשת")
    hyi_result.append("")
    #hyi_result.append("חגים מהתורה")
    #hyi_result.append("")
    hyi_result.append(f'יום הכיפורים יחול ביום: {heb_string_day(yom_kipur_weekday)}')
    hyi_result.append(f'יום ראשון של סוכות יחול ביום: {heb_string_day(sukot_weekday)}')
    hyi_result.append(f'יום ראשון של פסח יחול ביום: {heb_string_day(pesach_weekday)}')
    hyi_result.append(f'חג השבועות יחול ביום: {heb_string_day(shavuot_weekday)}')
    hyi_result.append("")
    #hyi_result.append("מועדים מדרבנן")
    #hyi_result.append("")
    hyi_result.append(f'נר ראשון של חנוכה יחול ביום: {heb_string_day(chanuka_weekday)}')
    hyi_result.append(f'פורים (דפרזים - יד) יחול ביום: {heb_string_day(purim_weekday)}')
    if tisha_beav_weekday == 7:
        hyi_result.append("תשעה באב יחול ביום שבת קודש, והתענית נדחית ליום ראשון")
    else:
        hyi_result.append(f'תשעה באב יחול ביום: {heb_string_day(tisha_beav_weekday)}')

    hyi_result.append("—————————————————————")
    hyi_result.append("#####   פירוט החישובים   #####")
    hyi_result.append("")
    hyi_result.append(f'השנה המבוקשת היא: {shana1} - {heb_year_string(shana1)}')
    hyi_result.append(f'{string_heb_year_to_loazit_year_plus_zero(shana1)}')
    hyi_result.append(f'מספר השנה המבוקשת במחזור 19 שנים פשוטות ומעוברות הוא: {shana_1_bemachzor_19}   (במחזור {machzor_19_shana_1})')
    # הדפסת בדיקה האם השנה המבוקשת היא פשוטה או מעוברת לפי בדיקה בתוך רשימת השנים המעוברות שבמחזור 19 השנים
    if shana_1_bemachzor_19 in (3,6,8,11,14,17,19):
        hyi_result.append(f'לפיכך, ולפי כלל גו"ח אדז"ט: השנה המבוקשת היא שנה מעוברת (כלומר: בת 13 חודשים - שני אדרים)')
    else:
        hyi_result.append(f'לפיכך, ולפי כלל גו"ח אדז"ט: השנה המבוקשת היא שנה פשוטה (כלומר: בת 12 חודשים - אדר אחד)')

    # הדפסת חישוב מספר החודשים שעברו ממולד בהר"ד עד מולד תשרי של השנה המבוקשת
    hyi_result.append(f'סך החודשים שחלפו ממולד בהר"ד למולד תשרי של השנה המבוקשת הוא: {sum_heb_months_be_over_from_molad_baharad_to_shana_1}')
    hyi_result.append(f'מולד תשרי בחלקים של השנה המבוקשת הוא: {molad_tishrei_1_bechalakim}')
    hyi_result.append(f'מולד תשרי של השנה המבוקשת יהיה: ביום - {heb_string_day(molad_tishrei_1[0])}, {molad_tishrei_1[1]} - שעות , ו- {molad_tishrei_1[2]} חלקים')
    # הדפסה האם ראש השנה נדחה ואם כן בכמה ימים
    hyi_result.append(f'ראש השנה של השנה המבוקשת אינו נדחה אלא יחול ביום מולד תשרי' if dechia1 == 0 else f'מספר הימים שבהם נדחה ראש השנה של השנה המבוקשת מיום מולד תשרי:  {dechia1}')
    # הדפסת היום שבו יחול ראש השנה של השנה המבוקשת
    hyi_result.append(f'ראש השנה של השנה המבוקשת יהיה ביום: {heb_string_day(rosh_hashana_1_weekday)}')

    # הדפסת התאריך העברי שבו יחול מולד תשרי של השנה המבוקשת. מתבסס על הכלל שחודש אלול הוא תמיד חסר כלומר: בן 29 יום
    if dechia1 == 0:
        hyi_result.append(f"מולד תשרי של השנה המבוקשת יהיה בתאריך: א' בתשרי {heb_year_string(shana1)}")
    elif dechia1 == 1:
        hyi_result.append(f"מולד תשרי של השנה המבוקשת יהיה בתאריך: כ'ט באלול {heb_year_string(shana1-1)}")
    elif dechia1 == 2:
        hyi_result.append(f"מולד תשרי של השנה המבוקשת יהיה בתאריך: כ'ח באלול {heb_year_string(shana1-1)}")

    # מכאן והלאה הדפסות עבור השנה שלאחריה
    # שורה רווח
    hyi_result.append("")
    hyi_result.append(f'השנה שלאחר השנה המבוקשת (=שנה שלאחריה) היא: {shana2} - {heb_year_string(shana2)}')
    hyi_result.append(f'{string_heb_year_to_loazit_year_plus_zero(shana2)}')
    hyi_result.append(f'מספר השנה שלאחריה במחזור 19 שנים פשוטות ומעוברות הוא: {shana_2_bemachzor_19}   (במחזור {machzor_19_shana_2})')
    # הדפסת בדיקה האם השנה המבוקשת היא פשוטה או מעוברת לפי בדיקה בתוך רשימת השנים המעוברות שבמחזור 19 השנים
    if shana_2_bemachzor_19 in (3,6,8,11,14,17,19):
        hyi_result.append(f'לפיכך, ולפי כלל גו"ח אדז"ט: השנה שלאחריה היא שנה מעוברת (כלומר: בת 13 חודשים - שני אדרים)')
    else:
        hyi_result.append(f'לפיכך, ולפי כלל גו"ח אדז"ט: השנה שלאחריה היא שנה פשוטה (כלומר: בת 12 חודשים - אדר אחד)')

    # הדפסת חישוב מספר החודשים שעברו ממולד בהר"ד עד מולד תשרי של השנה שלאחריה
    hyi_result.append(f'סך החודשים שחלפו ממולד בהר"ד למולד תשרי של השנה שלאחריה הוא: {sum_heb_months_be_over_from_molad_baharad_to_shana_2}')
    hyi_result.append(f'מולד תשרי בחלקים של השנה שלאחריה הוא: {molad_tishrei_2_bechalakim}')
    hyi_result.append(f'מולד תשרי של השנה שלאחריה יהיה: ביום - {heb_string_day(molad_tishrei_2[0])}, {molad_tishrei_2[1]} - שעות, ו- {molad_tishrei_2[2]} חלקים')
    # הדפסה האם ראש השנה של השנה שלאחריה נדחה ואם כן בכמה ימים
    hyi_result.append(f'ראש השנה של השנה שלאחריה אינו נדחה אלא יחול ביום מולד תשרי' if dechia2 == 0 else f'מספר הימים שבהם נדחה ראש השנה של השנה שלאחריה מיום מולד תשרי:  {dechia2}')
    # הדפסת היום שבו יחול ראש השנה של השנה שלאחריה
    hyi_result.append(f'ראש השנה של השנה שלאחריה יהיה ביום: {heb_string_day(rosh_hashana_2_weekday)}')

    # הדפסת התאריך העברי שבו יחול מולד תשרי של השנה שלאחריה. מתבסס על הכלל שחודש אלול הוא תמיד חסר כלומר: בן 29 יום
    if dechia2 == 0:
        hyi_result.append(f"מולד תשרי של השנה שלאחריה יהיה בתאריך: א' בתשרי {heb_year_string(shana2)}")
    elif dechia2 == 1:
        hyi_result.append(f"מולד תשרי של השנה שלאחריה יהיה בתאריך: כ'ט באלול {heb_year_string(shana2-1)}")
    elif dechia2 == 2:
        hyi_result.append(f"מולד תשרי של השנה שלאחריה יהיה בתאריך: כ'ח באלול {heb_year_string(shana2-1)}")

    hyi_result.append("")
    # הדפסת הפרש הימים בין שני ראשי השנים
    hyi_result.append(f'ההפרש בימי השבוע בין ראש השנה של השנה המבוקשת לבין ראש השנה של השנה שלאחריה הוא: {efresh}')
    hyi_result.append(f' :לפיכך, ולפי כלל: גד"ה - בפשוטה, הו"ז - במעוברת')
    # הדפסות של מספר ימי השנה של השנה המבוקשת
    if efresh == 3:
        hyi_result.append("השנה המבוקשת היא שנה פשוטה חסרה (כלומר: בת 353 ימים, מְרַחשְׁוָון וכסליו חסרים)")
    elif efresh == 4:
        hyi_result.append("השנה המבוקשת היא שנה פשוטה כסדרה (כלומר: בת 354 ימים, מְרַחשְׁוָון חסר וכסליו מלא)")
    #--------------------------------------------
    elif efresh == 5 and shana_1_bemachzor_19 not in (3,6,8,11,14,17,19):
        hyi_result.append("השנה המבוקשת היא שנה פשוטה שלמה (כלומר: בת 355 ימים, מְרַחשְׁוָון וכסליו מלאים)")
    elif efresh == 5 and shana_1_bemachzor_19 in (3,6,8,11,14,17,19):
        hyi_result.append("השנה המבוקשת היא שנה מעוברת חסרה (כלומר: בת 383 ימים, מְרַחשְׁוָון וכסליו חסרים)")
    #--------------------------------------------
    elif efresh == 6:
        hyi_result.append("השנה המבוקשת היא שנה מעוברת כסדרה (כלומר: בת 384 ימים, מְרַחשְׁוָון חסר וכסליו מלא)")
    elif efresh == 7:
        hyi_result.append("השנה המבוקשת היא שנה מעוברת שלמה (כלומר: בת 385 ימים, מְרַחשְׁוָון וכסליו מלאים)")


    hyi_result.append("—————————————————————")
    hyi_result.append("רשימת מולדות ממוצעים עבור כל חודשי השנה המבוקשת, כולל מולד תשרי של השנה שלאחריה")
    hyi_result.append("")

    # הדפסת רשימת מולדות כל חודשי השנה תוך בדיקה האם מדובר בשנה פשוטה או מעוברת
    for i in range(len(moladot_chodashim_1)):
        hyi_result.append(f'מולד חודש {chodashim_meuberet[i] if shana_1_bemachzor_19 in (3,6,8,11,14,17,19) else chodashim_pshuta[i]} יהיה: ביום - {heb_string_day(moladot_chodashim_1[i][0])}, {moladot_chodashim_1[i][1]} - שעות, ו- {moladot_chodashim_1[i][2]} חלקים')

    hyi_result.append("")
    hyi_result.append("—————————————————————")
    hyi_result.append("## תכונה ניסיונית! מידע על התקופות שבלוח ##")
    hyi_result.append("")
    hyi_result.append(f'תקופת ניסן לפי שמואל מקדימה את מולד ניסן ב: ימים - {tshuva[1]}; שעות - {tshuva[0]}; חלקים - {tshuva[2]}')
    hyi_result.append("")
    hyi_result.append("—————————————————————")
    hyi_result.append("## מידע כללי על סוגי השנים בלוח העברי ##")
    hyi_result.append("")
    hyi_result.append("בלוח העברי הקבוע קיימים בסך הכל 14 סוגי שנים")
    hyi_result.append("")
    hyi_result.append("שבע סוגי שנים פשוטות")
    hyi_result.append("")
    hyi_result.append("פשוטה חסרה בת 353 ימים: בחג, זחא")
    hyi_result.append("פשוטה כסדרה בת 354 ימים: גכה, הכז")
    hyi_result.append("פשוטה שלמה בת 355 ימים: בשה, השא, זשג")

    hyi_result.append("")
    hyi_result.append("שבע סוגי שנים מעוברות")
    hyi_result.append("")
    hyi_result.append("מעוברת חסרה בת 383 ימים: בחה, החא, זחג")
    hyi_result.append("מעוברת כסדרה בת 384 ימים: גכז")
    hyi_result.append("מעוברת שלמה בת 385 ימים: בשז, השג, זשה")

    return hyi_result



