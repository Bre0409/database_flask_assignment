document.addEventListener('DOMContentLoaded', () => {
  const monthSelect = document.getElementById('month-select');
  const yearSelect = document.getElementById('year-select');
  const daySelect = document.getElementById('day-select');
  const resetBtn = document.getElementById('reset-btn');
  const calendarGrid = document.getElementById('calendar-grid');
  const prevMonthBtn = document.getElementById('prev-month');
  const nextMonthBtn = document.getElementById('next-month');
  const calendarWrapper = document.querySelector('.calendar-wrapper');

  if (!monthSelect || !yearSelect || !daySelect || !resetBtn || !calendarGrid || !prevMonthBtn || !nextMonthBtn) return;

  const monthNames = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
  ];

  let currentDate = new Date();
  const events = window.calendarEvents || [];

  function populateMonths() {
    monthSelect.innerHTML = '';
    monthNames.forEach((month, index) => {
      const option = document.createElement('option');
      option.value = index;
      option.textContent = month;
      monthSelect.appendChild(option);
    });
  }

  function populateYears() {
    yearSelect.innerHTML = '';
    const currentYear = new Date().getFullYear();
    for (let y = currentYear - 10; y <= currentYear + 10; y++) {
      const option = document.createElement('option');
      option.value = y;
      option.textContent = y;
      yearSelect.appendChild(option);
    }
  }

  function populateDays(year, month) {
    daySelect.innerHTML = '';
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    for (let d = 1; d <= daysInMonth; d++) {
      const option = document.createElement('option');
      option.value = d;
      option.textContent = d;
      daySelect.appendChild(option);
    }
  }

  function renderCalendar(year, month) {
    calendarGrid.innerHTML = '';
    const firstDay = new Date(year, month, 1).getDay();
    const totalDays = new Date(year, month + 1, 0).getDate();

    const today = new Date();
    const isTodayMonth = today.getFullYear() === year && today.getMonth() === month;

    for (let i = 0; i < firstDay; i++) {
      const blank = document.createElement('div');
      blank.className = 'calendar-day empty';
      calendarGrid.appendChild(blank);
    }

    for (let day = 1; day <= totalDays; day++) {
      const dayDiv = document.createElement('div');
      dayDiv.className = 'calendar-day';
      dayDiv.tabIndex = 0;
      dayDiv.textContent = day;

      const dateStr = `${year}-${(month + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
      const dayEvents = events.filter(e => e.date === dateStr);

      if (isTodayMonth && today.getDate() === day) {
        dayDiv.classList.add('today');
      }

      if (dayEvents.length > 0) {
        const eventList = document.createElement('ul');
        eventList.className = 'event-list';

        const tooltip = document.createElement('div');
        tooltip.className = 'event-tooltip';

        dayEvents.forEach(event => {
          const li = document.createElement('li');
          li.textContent = event.title;
          eventList.appendChild(li);

          const p = document.createElement('p');
          p.innerHTML = `<strong>${event.title}</strong><br>${event.description || 'No description.'}`;
          tooltip.appendChild(p);
        });

        dayDiv.appendChild(eventList);
        dayDiv.appendChild(tooltip);

        dayDiv.addEventListener('click', (e) => {
          e.stopPropagation();
          document.querySelectorAll('.event-tooltip').forEach(t => {
            if (t !== tooltip) t.style.display = 'none';
          });
          tooltip.style.display = tooltip.style.display === 'block' ? 'none' : 'block';
        });

        dayDiv.addEventListener('mouseenter', () => {
          tooltip.style.display = 'block';
        });
        dayDiv.addEventListener('mouseleave', () => {
          tooltip.style.display = 'none';
        });
      }

      calendarGrid.appendChild(dayDiv);
    }
  }

  function updateCalendar() {
    const year = parseInt(yearSelect.value);
    const month = parseInt(monthSelect.value);
    populateDays(year, month);

    const today = new Date();
    if (year === today.getFullYear() && month === today.getMonth()) {
      daySelect.value = today.getDate();
    } else {
      daySelect.value = 1;
    }

    renderCalendar(year, month);
  }

  // Dropdowns and calendar
  populateMonths();
  populateYears();

  // Set dropdowns to current date
  monthSelect.value = currentDate.getMonth();
  yearSelect.value = currentDate.getFullYear();
  daySelect.value = currentDate.getDate();

  updateCalendar();

  // Event listeners
  monthSelect.addEventListener('change', updateCalendar);
  yearSelect.addEventListener('change', updateCalendar);

  resetBtn.addEventListener('click', () => {
    currentDate = new Date();
    monthSelect.value = currentDate.getMonth();
    yearSelect.value = currentDate.getFullYear();
    updateCalendar();
  });

  prevMonthBtn.addEventListener('click', () => {
    let month = parseInt(monthSelect.value);
    let year = parseInt(yearSelect.value);
    month--;
    if (month < 0) {
      month = 11;
      year--;
    }
    monthSelect.value = month;
    yearSelect.value = year;
    updateCalendar();
  });

  nextMonthBtn.addEventListener('click', () => {
    let month = parseInt(monthSelect.value);
    let year = parseInt(yearSelect.value);
    month++;
    if (month > 11) {
      month = 0;
      year++;
    }
    monthSelect.value = month;
    yearSelect.value = year;
    updateCalendar();
  });

  // Text bubble containing calender information accesed when clicked touched or hover over saved info
  if (calendarWrapper) {
    calendarWrapper.addEventListener('click', (event) => {
      const isInsideDay = event.target.closest('.calendar-day');
      if (!isInsideDay) {
        document.querySelectorAll('.event-tooltip').forEach(t => t.style.display = 'none');
      }
    });
  }
});


