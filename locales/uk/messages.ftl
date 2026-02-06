start =
    <tg-emoji emoji-id="5258011929993026890">👤</tg-emoji> Привіт, <b>{$name}</b>!

    <tg-emoji emoji-id="5258334872878980409">🎓</tg-emoji> Це бот для перегляду розкладу <a href="https://kntu.kr.ua/education/hrafik-osvitnoho-protsesu"><b>ЦНТУ</b></a>
    <tg-emoji emoji-id="5226513232549664618">📚</tg-emoji> Група: <b>КН-25</b>

    <tg-emoji emoji-id="5258334872878980409">🎓</tg-emoji> <b>2 Семестр:</b> <code>{ DATETIME($semester_start, dateStyle: "short") } — { DATETIME($semester_end, dateStyle: "short") }</code>

    <tg-emoji emoji-id="5258503720928288433">ℹ</tg-emoji> Обери потрібний розклад нижче

how-to-use =
    <tg-emoji emoji-id="5258503720928288433">ℹ</tg-emoji> <b>Як користуватися ботом:</b>

    <tg-emoji emoji-id="5258105663359294787">🗓️</tg-emoji> <b>Сьогодні</b> - розклад на поточний день
    <tg-emoji emoji-id="5258105663359294787">🗓️</tg-emoji> <b>Завтра</b> - розклад на наступний день
    <tg-emoji emoji-id="5258105663359294787">🗓️</tg-emoji> <b>Весь тиждень</b> - повний розклад на тиждень

    <tg-emoji emoji-id="5323761960829862762">⚡</tg-emoji> <b>Бот автоматично визначає тип тижня (чисельник/знаменник)</b>

btn-today = 🗓️ Сьогодні
btn-tomorrow = 🗓️ Завтра
btn-week = 📊 Весь тиждень
btn-back = ◀️ Назад

schedule-today = <tg-emoji emoji-id="5258105663359294787">🗓️</tg-emoji> <b>Розклад на сьогодні</b>
schedule-tomorrow = <tg-emoji emoji-id="5258105663359294787">🗓️</tg-emoji><b>Розклад на завтра</b>
schedule-week = <tg-emoji emoji-id="5258105663359294787">🗓️</tg-emoji> <b>Розклад на тиждень</b>

alert-no-lessons-today = 🎉 Сьогодні пар немає! Відпочивай!
alert-no-lessons-tomorrow = 🎉 Завтра пар немає! Вихідний!

lesson-item = <b>{$number}. {$subject}</b> (<code>{$time}</code>)
    {$teachers_count ->
[1] <b>Викладач:</b> {$teacher}
*[other] <b>Викладачі:</b> {$teacher}
    } • <b>{$room_display}</b>

room-gym = <b>Спортзал</b>
room-regular = Аудиторія <b>{$room}</b>

week-numerator = Чисельник
week-denominator = Знаменник
week-schedule-header = <tg-emoji emoji-id="5258105663359294787">🗓️</tg-emoji> <b>Розклад на тиждень ({ DATETIME($start_date, dateStyle: "short") } — { DATETIME($end_date, dateStyle: "short") })</b> — {$week_type}
day-schedule = <tg-emoji emoji-id="5258105663359294787">🗓️</tg-emoji> <b>{$day} ({ DATETIME($date, dateStyle: "short") })</b> — {$week_type} 
week-day-header = <tg-emoji emoji-id="5258105663359294787">🗓️</tg-emoji> <b>{$day} ({ DATETIME($date, dateStyle: "short") })</b>
