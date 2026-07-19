const statusInput = document.getElementById("attendance_status");
const guestInput = document.getElementById("guest_count");

function updateGuestField() {
    if (!statusInput || !guestInput) {
        return;
    }

    const isAttending = statusInput.value === "Attending";

    guestInput.disabled = !isAttending;

    if (!isAttending) {
        guestInput.value = 0;
    }
}

if (statusInput && guestInput) {
    statusInput.addEventListener("change", updateGuestField);
    updateGuestField();
}

document.querySelectorAll(".delete-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
        const confirmed = window.confirm(
            "Are you sure you want to delete this attendance record?"
        );

        if (!confirmed) {
            event.preventDefault();
        }
    });
});