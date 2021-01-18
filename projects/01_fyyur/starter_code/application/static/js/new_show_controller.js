const showForm = document.getElementById('show-form');
showDatePicker = document.getElementById('show_date');

// create new artist
if (showForm) {
  showForm.onsubmit = function(e) {
    e.preventDefault();

    fetch('/shows/create', {
      method: 'POST',
      body: JSON.stringify({
        'artist_id': document.getElementById('artist_id').value,
        'venue_id': document.getElementById('venue_id').value,
        'show_date': document.getElementById('show_date').value,
        'show_time': document.getElementById('show_time').value
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function(response) {
      return response.json();
    })
    .then(function (text) {
      if (text.message === 'Success') {
        window.location.replace('/');
      } else {
        Object.entries(text.errors).forEach(function ([key, value]) {
          document.getElementById(`${key}_error`).classList.remove('hidden');
          value.forEach(function (message) {
            const errorMessage = document.createElement('div');
            errorMessage.className = "error"
            errorMessage.innerHTML = message;
            document.getElementById(`${key}_error`).appendChild(errorMessage);
          })
        })
      }
    })
    .catch(function(e) {
      console.log('error----', e);
    })
  }
}