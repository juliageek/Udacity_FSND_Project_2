const editArtistForm = document.getElementById('edit-artist-form');
const deleteArtistButton = document.getElementById('delete-artist');

if (editArtistForm) {
 editArtistForm.onsubmit = function(e) {
   e.preventDefault();
   const errors = document.querySelectorAll('.errors');

   errors.forEach(function(error) {
     error.innerHTML = '';
   })

   const artistId = e.target.dataset.id;
   const genreSelect1 = document.getElementById('genres');
   const selectedOptions2 = Array.from(genreSelect1.options).filter(function(option) {
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

   fetch(`/artists/${artistId}/edit`, {
     method: 'POST',
     body: JSON.stringify({
       'name': document.getElementById('name').value,
       'city': document.getElementById('city').value,
       'state_id': document.getElementById('state_id').value,
       'phone': document.getElementById('phone').value,
       'genres': selectedOptions2,
       'image_link': document.getElementById('image_link').value,
       'facebook_link': document.getElementById('facebook_link').value,
       'website': document.getElementById('website').value,
       'seeking_venue': document.getElementById('seeking_venue').checked,
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
       window.location.replace(`/artists/${artistId}`);
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

if (deleteArtistButton) {
  deleteArtistButton.onclick = function(e) {
  const artistId = e.target.dataset.id;

  fetch(`/artists/${artistId}`, {
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
}

