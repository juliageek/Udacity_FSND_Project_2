const searchInput = document.getElementById('search-venue');

if (searchInput) {
  searchInput.onsubmit = function(e) {
    fetch('/venues/search', {
      method: 'POST',
      body: JSON.stringify({
        'search': e.target.value
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function(res) {
       document.write(res);
    })
    .catch(function(e) {
      console.log('error----', e);
    })
  }
}
