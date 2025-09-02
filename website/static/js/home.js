
// Typed out messages on home page under H1 which stops looping and after last message displayed.
document.addEventListener('DOMContentLoaded', function () {
  const subtitleEl = document.getElementById('typed-output');

  if (subtitleEl) {
    setTimeout(() => {
      new Typed('#typed-output', {
        strings: [
          'Organize your life effortlessly.',
          'Add tasks to your To-Do List.',
          'Schedule events into your Calendar.',
          'Welcome to your personal planner.'
        ],
        typeSpeed: 50,
        backSpeed: 30,
        backDelay: 500,
        loop: false,
        showCursor: true
      });
    }, 1000);
  }
});