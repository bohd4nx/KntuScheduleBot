start =
    <tg-emoji emoji-id="6032693626394382504">👤</tg-emoji> Вітаю, <b>{$name}</b>!

    Це бот для перегляду розкладу занять
    <a href="https://kntu.kr.ua/education/hrafik-osvitnoho-protsesu"><b>Центральноукраїнського національного технічного університету.</b></a>

    <tg-emoji emoji-id="5764638872000533034">📚</tg-emoji> Наша група: <b>КН-25</b>

    <tg-emoji emoji-id="5938195768832692153">🎓</tg-emoji> <b>2-й семестр</b>: <code>{ DATETIME($semester_start, dateStyle: "short") } — { DATETIME($semester_end, dateStyle: "short") }</code>

    <tg-emoji emoji-id="6028435952299413210">ℹ️</tg-emoji> Оберіть тип розкладу нижче.

how-to-use =
    <tg-emoji emoji-id="6030848053177486888">❓</tg-emoji> <b>Як користуватися ботом:</b>

    <tg-emoji emoji-id="5962952497197748583">🗓️</tg-emoji> <b>Сьогодні</b> - розклад на поточний день [/today]
    <tg-emoji emoji-id="5962952497197748583">🗓️</tg-emoji> <b>Завтра</b> - розклад на наступний день [/tomorrow]
    <tg-emoji emoji-id="5962952497197748583">🗓️</tg-emoji> <b>Весь тиждень</b> - повний розклад на тиждень [/week]

    <tg-emoji emoji-id="6042098561095570207">⚡</tg-emoji> <b>Бот автоматично визначає тип тижня (чисельник/знаменник)</b>

btn-today = Сьогодні
btn-tomorrow = Завтра
btn-week = Весь тиждень
btn-back = Назад

schedule-today = <tg-emoji emoji-id="5938195768832692153">🗓️</tg-emoji> <b>Розклад на сьогодні</b>
schedule-tomorrow = <tg-emoji emoji-id="5891100675042974129">🗓️</tg-emoji><b>Розклад на завтра</b>
schedule-week = <tg-emoji emoji-id="5890937706803894250">🗓️</tg-emoji> <b>Розклад на тиждень</b>

no-lessons-today = <tg-emoji emoji-id="6041731551845159060">🎉</tg-emoji> Сьогодні пар немає! Відпочивай!
no-lessons-tomorrow = <tg-emoji emoji-id="5967688845397855939">🥂</tg-emoji> Завтра пар немає! Вихідний!
semester-not-started = <tg-emoji emoji-id="6043847274210005137">🙃</tg-emoji> Навчання ще не почалось! Відпочиваємо!

alert-no-lessons-today = 🎉 Сьогодні пар немає! Відпочивай!
alert-no-lessons-tomorrow = 🎉 Завтра пар немає! Вихідний!
alert-semester-not-started = 🙃 Навчання ще не почалось! Відпочиваємо!

lesson-item = <b>{$number}. {$subject}</b> (<code>{$time}</code>)
    {$teachers_count ->
[1] <b>Викладач:</b> {$teacher}
*[other] <b>Викладачі:</b> {$teacher}
    }
    <b>{$room_display}</b>

room-gym = <b>Заняття проходить у спортзалі</b>
room-regular = Аудиторія: <b>{$room}</b>

week-numerator = Чисельник
week-denominator = Знаменник
week-schedule-header = <tg-emoji emoji-id="5936143551854285132">🗓️</tg-emoji> <b>Розклад на тиждень ({ DATETIME($start_date, dateStyle: "short") } — { DATETIME($end_date, dateStyle: "short") })</b> — {$week_type}
day-schedule = <tg-emoji emoji-id="5890937706803894250">🗓️</tg-emoji> <b>{$day} ({ DATETIME($date, dateStyle: "short") })</b> — {$week_type} 
week-day-header = <tg-emoji emoji-id="5890937706803894250">🗓️</tg-emoji> <b>{$day} ({ DATETIME($date, dateStyle: "short") })</b>
