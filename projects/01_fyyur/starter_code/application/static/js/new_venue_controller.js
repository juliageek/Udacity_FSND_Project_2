// enable and disable the seeking description text area depending on whether the seeking talent box is checked or not
const seekingTalent = document.getElementById('seeking_talent');
const venueForm = document.getElementById('venue-form');

if(seekingTalent) {
  if (!seekingTalent.checked) {
    document.getElementById('seeking_description').disabled = true;
  }
  seekingTalent.onchange = function(e){
    document.getElementById('seeking_description').disabled = !e.target.checked;
  }
}

// create new venue
if (venueForm) {
    venueForm.onsubmit = function(e) {
      e.preventDefault();
      const errors = document.querySelectorAll('.errors');

      errors.forEach(function(error) {
        error.innerHTML = '';
      })

      const genreSelect = document.getElementById('genres');
      const selectedOptions = Array.from(genreSelect.options).filter(function(option) {
        return option.selected;
      })
      .map(function(option) {
        return option.value;
      })
      fetch('/venues/create', {
        method: 'POST',
        body: JSON.stringify({
          'name': document.getElementById('name').value,
          'city': document.getElementById('city').value,
          'state': document.getElementById('state').value,
          'address': document.getElementById('address').value,
          'phone': document.getElementById('phone').value,
          'image_link': document.getElementById('image_link').value,
          'genres': selectedOptions,
          'facebook_link': document.getElementById('facebook_link').value,
          'website': document.getElementById('website').value,
          'seeking_talent': document.getElementById('seeking_talent').checked,
          'seeking_description': document.getElementById('seeking_description').value
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
          window.location.reload(true);
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