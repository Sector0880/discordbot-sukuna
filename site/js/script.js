/*global window*/
(function (global) {
    "use strict";
    function Clock(el) {
        var document = global.document;
        this.el = document.getElementById(el);
        this.months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
        this.days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
    }
    Clock.prototype.addZero = function (i) {
        if (i < 10) {
            i = "0" + i;
            return i;
        }
        return i;
    };
    Clock.prototype.updateClock = function () {
        var now, year, month, dayNo, day, hour, minute, second, result, self;
        now = new global.Date();
        year = now.getFullYear();
        month = now.getMonth();
        dayNo = now.getDay();
        day = now.getDate();
        hour = this.addZero(now.getHours());
        minute = this.addZero(now.getMinutes());
        second = this.addZero(now.getSeconds());
        result = "Текущая дата: " + this.days[dayNo] + ", " + day + " " + this.months[month] + " " + hour + ":" + minute + ":" + second + " " + year + " ";
        self = this;
        self.el.innerHTML = result;
        global.setTimeout(function () {
            self.updateClock();
        }, 1000);
    };
    global.Clock = Clock;
}(window));

function addEvent(elm, evType, fn, useCapture) {
    "use strict";
    if (elm.addEventListener) {
        elm.addEventListener(evType, fn, useCapture);
    } else if (elm.attachEvent) {
        elm.attachEvent('on' + evType, fn);
    } else {
        elm['on' + evType] = fn;
    }
}

addEvent(window, "load", function () {
    if (document.getElementById("clock")) {
        var clock = new Clock("clock");
        clock.updateClock();
    }
});


fetch("C:/Users/1/Документы/GitHub/discordbot-sukuna/.db/multipresence/guildsCount.json") // Укажите правильный путь к файлу guildsCount.json
  .then(response => response.json())
  .then(data => {
    const select = document.getElementById("guildsList");

    // Проверяем, существует ли массив с именем 'guilds-list' в структуре JSON файла
    if (data.hasOwnProperty('guilds-list')) {
      // Итерируемся по элементам массива и создаем <option> для каждого элемента
      data['guilds-list'].forEach(guildId => {
        const option = document.createElement("option");
        option.text = guildId;
        option.value = guildId;
        select.add(option);
      });
    } else {
      // Если массив 'guilds-list' не найден, выводим сообщение об ошибке в консоль
      console.error("Массив 'guilds-list' не найден в файле guildsCount.json");
    }
  })
  .catch(error => {
    // Если произошла ошибка при загрузке или разборе JSON файла, выводим сообщение об ошибке в консоль
    console.error("Ошибка:", error);
  });