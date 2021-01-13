const editVenueForm = document.getElementById('edit-venue-form');
const deleteButton = document.getElementById('delete-venue');

if (editVenueForm) {
 editVenueForm.onsubmit = function(e) {
   e.preventDefault();
   const errors = document.querySelectorAll('.errors');

   errors.forEach(function(error) {
     error.innerHTML = '';
   })

   const venueId = e.target.dataset.id;
   const genreSelect1 = document.getElementById('genres');
   const selectedOptions1 = Array.from(genreSelect1.options).filter(function(option) {
     return option.selected;
   })
   .map(function(option) {
      return option.value;
   })

   const genreSelect = document.getElementById('genres');
   const selectedOptions = Array.from(genreSelect.options).filter(function(option) {
     return option.selected;
   })
   .map(function(option) {
     return option.value;
   })

   fetch(`/venues/${venueId}/edit`, {
     method: 'POST',
     body: JSON.stringify({
       'name': document.getElementById('name').value,
       'city': document.getElementById('city').value,
       'state': document.getElementById('state').value,
       'address': document.getElementById('address').value,
       'phone': document.getElementById('phone').value,
       'genres': selectedOptions1,
       'image_link': document.getElementById('image_link').value,
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
   .then(function(text) {
     if (text.message === 'Success') {
       window.location.replace(`/venues/${venueId}`);
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

deleteButton.onclick = function(e) {
    const venueId = e.target.dataset.id;

    fetch(`/venues/${venueId}`, {
        method: 'DELETE'
    })
    .then(function(response) {
     return response.json();
   })
   .then(function(text) {
     if (text.message === 'Success') {
       window.location.replace('/');
     }
   })
}