document.getElementById('avatarForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const form = this;
  const updateAvatarUrl = form.getAttribute('data-update-avatar-url'); // Получаем URL из формы
  const formData = new FormData(form);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Показываем индикатор загрузки
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalText = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = 'Загрузка...';

  try {
    console.log('Отправляем запрос на загрузку аватара...');
    const response = await fetch(updateAvatarUrl, { // Используем динамический URL
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': csrftoken
      },
      credentials: 'include'
    });

    console.log('Статус ответа:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Ошибка сервера:', errorText);
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    console.log('Ответ сервера:', result);

    if (result.success) {
      const avatarImg = document.querySelector('.avatar-medium');
      if (avatarImg && result.avatar_url) {
        avatarImg.src = result.avatar_url;
      }
      const avatarModal = bootstrap.Modal.getInstance(document.getElementById('avatarModal'));
      if (avatarModal) {
        avatarModal.hide();
      }
      alert('Аватар успешно обновлён!');
    } else {
      alert(`Ошибка: ${result.error || 'Неизвестная ошибка'}`);
    }
  } catch (error) {
    console.error('Критическая ошибка:', error);
    alert('Произошла ошибка при загрузке. Проверьте консоль для деталей.');
  } finally {
    // Восстанавливаем кнопку
    submitBtn.disabled = false;
    submitBtn.textContent = originalText;
  }
});



    document.addEventListener('DOMContentLoaded', function() {
  const modalBody = document.getElementById('historyRecords');

  async function loadMedicalHistory() {
    try {
      // Показываем индикатор загрузки
      modalBody.innerHTML = '<tr><td colspan="3" class="text-center">Загрузка...</td></tr>';

      const response = await fetch('/api/medical-history/');

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      // Проверяем, что данные пришли и содержат records - добавила в исх
      if (!data || !Array.isArray(data.records)) {
        throw new Error('Неверный формат данных от сервера');
      }

      // Очищаем список перед заполнением
      modalBody.innerHTML = '';

      if (data.records.length === 0) {
        modalBody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Записей не найдено</td></tr>';
        return;
      }

      // Заполняем таблицу данными
      data.records.forEach(record => {
        const row = `
          <tr>
            <td>${record.date}</td>
            <td>${record.service}</td>
            <td>${record.doctor}</td>
          </tr>
        `;
        modalBody.insertAdjacentHTML('beforeend', row);
      });
    } catch (error) {
      console.error('Ошибка загрузки медицинской истории:', error);
      modalBody.innerHTML = '<tr><td colspan="3" class="text-danger">Ошибка загрузки данных</td></tr>';
    }
  }

  // Получаем модальное окно Bootstrap
  const medicalHistoryModal = document.getElementById('medicalHistoryModal');
  if (medicalHistoryModal) {
    medicalHistoryModal.addEventListener('show.bs.modal', loadMedicalHistory);
  } else {
    console.warn('Модальное окно с ID "medicalHistoryModal" не найдено');
  }
});
