// fav.js
function submitFavouriteForm(postId, isFavourite, addFavouriteUrl, removeFavouriteUrl) {
  var form = document.getElementById('favourite-form-' + postId);
  var action = isFavourite ? removeFavouriteUrl : addFavouriteUrl;
  form.action = action;
  form.submit();

  var heart = form.querySelector('.fa-heart');
  heart.classList.toggle('fa-regular');
  heart.classList.toggle('fa-solid');
}

function toggleFavourite(postId) {
  var heart = document.querySelector('#favourite-heart-' + postId);
  var isFavourite = heart.classList.contains('fa-solid');
  
  var addFavouriteUrl = heart.getAttribute('data-add-url');
  var removeFavouriteUrl = heart.getAttribute('data-remove-url');

  submitFavouriteForm(postId, isFavourite, addFavouriteUrl, removeFavouriteUrl);
}

// Attach event listeners after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
  var hearts = document.querySelectorAll('.fa-heart');
  hearts.forEach(function (heart) {
    heart.addEventListener('click', function () {
      var postId = heart.getAttribute('data-post-id');
      toggleFavourite(postId);
    });
  });
});
