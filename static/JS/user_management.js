// Prevent row click from navigating away
document.querySelectorAll(".user-management-table tr").forEach((row) => {
  row.addEventListener("click", (event) => {
    if (
      event.target.tagName !== "BUTTON" &&
      event.target.tagName !== "I"
    ) {
      window.location.href = "user-profile";
    }
  });
});

// Initialize modals for buttons
document.querySelectorAll(".edit-user-btn").forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    const userId = event.currentTarget.closest("tr").dataset.userId;
    // You can load user data into the modal here using userId
    console.log("Edit user", userId);
  });
});

document.querySelectorAll(".delete-user-btn").forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    const userId = event.currentTarget.closest("tr").dataset.userId;
    // Handle delete user action here using userId
    console.log("Delete user", userId);
  });
});