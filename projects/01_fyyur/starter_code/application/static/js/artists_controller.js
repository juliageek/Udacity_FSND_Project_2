const searchInputArtist = document.getElementById('search-artist');

if (searchInput) {
  searchInputArtist.onsubmit = function(e) {
    fetch('/artists/search', {
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