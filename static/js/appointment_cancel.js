document.addEventListener("DOMContentLoaded", () => {
  const cancelButtons = document.querySelectorAll('[data-bs-target="#cancelAppointmentModal"]');
  const confirmBtn = document.getElementById("confirmCancelBtn");
  const modalServiceTitle = document.getElementById("modalServiceTitle");
  let currentAppointmentId = null;

  if (!confirmBtn) {
    console.error("Кнопка подтверждения отмены не найдена");
    return;
  }

  // Обработчик для кнопок отмены
  cancelButtons.forEach((button) => {
    button.addEventListener("click", () => {
      currentAppointmentId = button.getAttribute("data-appointment-id");
      const serviceTitle = button.getAttribute("data-service-title");
      if (modalServiceTitle) {
        modalServiceTitle.textContent = serviceTitle || "Неизвестная услуга";
      }
    });
  });

  // Обработчик подтверждения отмены
  confirmBtn.addEventListener("click", async () => {
    if (!currentAppointmentId) {
      console.error("ID записи не определён");
      return;
    }

    try {
      const response = await fetch(`/appointments/${currentAppointmentId}/cancel/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")?.value || "",
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}`);
      }

      const result = await response.json();

      // Обновляем интерфейс
      const cancelButton = document.querySelector(`[data-appointment-id="${currentAppointmentId}"]`);
      const item = cancelButton ? cancelButton.closest(".list-group-item") : null;
      if (item) {
        const badge = item.querySelector(".text-end .status-badge");
        if (badge) {
          badge.textContent = "Отменено";
          badge.className = "status-badge status-cancelled";
        }
        cancelButton?.remove();
      }

      // Закрываем модальное окно
      const modalElement = document.getElementById("cancelAppointmentModal");
      const modal = modalElement ? bootstrap.Modal.getInstance(modalElement) : null;
      if (modal) {
        modal.hide();
      } else if (modalElement) {
        new bootstrap.Modal(modalElement).hide();
      }

      // Показываем уведомление
      const successAlert = document.createElement("div");
      successAlert.className = "alert alert-success alert-dismissible fade show mt-3";
      successAlert.role = "alert";
      successAlert.innerHTML = `
        <strong>Успешно!</strong> Запись отменена.
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `;
      const container = document.querySelector(".container.mt-5.mb-5") || document.body;
      container.prepend(successAlert);
      setTimeout(() => successAlert.remove(), 3000);
    } catch (error) {
      console.error("Ошибка при отмене записи:", error);
      alert("Не удалось отменить запись. Попробуйте ещё раз.");
    } finally {
      currentAppointmentId = null;
    }
  });
});
