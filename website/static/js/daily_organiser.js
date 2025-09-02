// Day switching tabs
document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".day-tab");

  tabs.forEach((tab) => {
    tab.addEventListener("click", (event) => {
      event.preventDefault(); 
      const selectedDay = tab.textContent.trim();
      const url = new URL(window.location.href);
      url.searchParams.set("day", selectedDay);
      window.location.href = url;
    });
  });

  // Add edit toggle buttons
  document.querySelectorAll(".edit-toggle-btn[data-task-id]").forEach(button => {
    button.addEventListener("click", () => {
      const taskId = button.dataset.taskId;
      toggleEdit(taskId);
    });
  });
});

// Toggle edit form 
function toggleEdit(taskId) {
  const textSpan = document.getElementById(`text-${taskId}`);
  const editForm = document.getElementById(`form-${taskId}`);

  if (!textSpan || !editForm) return;

  if (editForm.classList.contains("visible")) {
    editForm.classList.remove("visible");
    textSpan.style.display = "inline";
  } else {
    editForm.classList.add("visible");
    textSpan.style.display = "none";
  }
}
