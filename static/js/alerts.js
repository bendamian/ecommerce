// static/js/alerts.js

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".alert").forEach(el => {
    let timeout = 4000;

    if (el.classList.contains("alert-success")) timeout = 2500;
    if (el.classList.contains("alert-danger")) timeout = 6000;

    setTimeout(() => {
      if (window.bootstrap && bootstrap.Alert) {
        bootstrap.Alert.getOrCreateInstance(el).close();
      } else {
        el.remove();
      }
    }, timeout);
  });
});
