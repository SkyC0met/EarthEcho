document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.rating-wrapper img');

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.id;
            updateStarRating(rating);
        });
    });

    // Ensure the clear button works as well
    const clearButton = document.querySelector('.rating-wrapper button');
    if (clearButton) {
        clearButton.addEventListener('click', clearStarRating);
    }
});

function updateStarRating(clickedRating) {
    const stars = document.querySelectorAll('.rating-wrapper img');

    // Remove 'rating-checked' class from all stars
    stars.forEach(star => star.classList.remove('rating-checked'));

    // Add 'rating-checked' class to clicked star and previous stars
    for (let i = 0; i < clickedRating; i++) {
        stars[i].classList.add('rating-checked');
    }

    // Update the hidden input field with the selected rating
    document.getElementById('rating').value = clickedRating;
}

function clearStarRating() {
    const stars = document.querySelectorAll('.rating-wrapper img');

    // Remove 'rating-checked' class from all stars
    stars.forEach(star => star.classList.remove('rating-checked'));

    // Clear the hidden input field
    document.getElementById('rating').value = '';
}

function clearRatingAndReviewInputs() {
    // Clear the rating input
    document.getElementById('rating').value = '';

    // Clear the review textarea
    document.getElementById('review').value = '';

    // Clear the star rating display
    clearStarRating();
}
