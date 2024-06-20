// rating and review
document.addEventListener('DOMContentLoaded', function () {
    // Select all star rating images and add click event listeners
    const stars = document.querySelectorAll('.rating-wrapper img');
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.id;
            updateStarRating(rating); // Call function to update star rating display
        });
    });

    // Handle click event on clear button to clear star rating
    const clearButton = document.querySelector('.rating-wrapper button');
    if (clearButton) {
        clearButton.addEventListener('click', clearStarRating);
    }

    // Handle form submission via AJAX to prevent page reload
    document.getElementById('reviewForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Prepare form data to be sent via fetch
        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Handle the response (e.g., update the reviews section)
                console.log(data); // Log the response for debugging

                // Create new review HTML element
                const reviewsContainer = document.getElementById('reviews');
                const newReview = document.createElement('div');
                newReview.classList.add('review');
                newReview.innerHTML = `
                    <p>Date: ${data.date}</p>
                    <p>Time: ${data.time}</p>
                    <p>Review: ${data.review}</p>
                    <hr>
                `;
                reviewsContainer.prepend(newReview); // Add new review at the beginning

                clearRatingAndReviewInputs(); // Optional: Clear form inputs
            } else {
                console.error('Error:', data.message); // Log error message for debugging
                alert('Error: ' + data.message); // Optionally show an alert with the error message
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

// Function to update star rating display
function updateStarRating(clickedRating) {
    const stars = document.querySelectorAll('.rating-wrapper img');
    stars.forEach(star => star.classList.remove('rating-checked'));

    for (let i = 0; i < clickedRating; i++) {
        stars[i].classList.add('rating-checked');
    }

    document.getElementById('rating').value = clickedRating; // Update hidden input field with rating value
}

// Function to clear star rating display and hidden input field
function clearStarRating() {
    const stars = document.querySelectorAll('.rating-wrapper img');
    stars.forEach(star => star.classList.remove('rating-checked'));

    document.getElementById('rating').value = ''; // Clear hidden input field value
}

// Function to clear rating and review inputs
function clearRatingAndReviewInputs() {
    document.getElementById('rating').value = ''; // Clear rating input
    document.getElementById('review').value = ''; // Clear review input
    clearStarRating(); // Clear star rating display
}
