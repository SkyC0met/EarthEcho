document.addEventListener('DOMContentLoaded', function () {
    // Setup star rating click handlers
    const stars = document.querySelectorAll('.rating-wrapper img');
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.id;
            updateStarRating(rating);
        });
    });

    // Setup clear button handler
    const clearButton = document.querySelector('.rating-wrapper button');
    if (clearButton) {
        clearButton.addEventListener('click', clearStarRating);
    }

    // Handle form submission
    document.getElementById('reviewForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(this);
        console.log("Form data before sending:");
        for (const [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }

        // Retrieve CSRF token from meta tag or hidden input
        const csrfToken = document.querySelector('input[name="csrf_token"]').value;

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken // Ensure this matches what the server expects
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);
            if (data.status === 'success') {
                const reviewsContainer = document.getElementById('reviews');
                const newReview = document.createElement('div');
                newReview.classList.add('review');
                newReview.innerHTML = `
                    <p>Username: ${data.username}</p>
                    <p>Date: ${data.date}</p>
                    <p>Time: ${data.time}</p>
                    <p>Rating: ${data.rating}</p>
                    <p>Review: ${data.review}</p>
                    <hr>
                `;
                reviewsContainer.prepend(newReview);
                clearRatingAndReviewInputs();
            } else {
                console.error('Error response:', data.message);
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    });
});

// Update star rating display
function updateStarRating(clickedRating) {
    const stars = document.querySelectorAll('.rating-wrapper img');
    stars.forEach(star => star.classList.remove('rating-checked'));

    for (let i = 0; i < clickedRating; i++) {
        stars[i].classList.add('rating-checked');
    }

    document.getElementById('rating').value = clickedRating;
}

// Clear star rating display
function clearStarRating() {
    const stars = document.querySelectorAll('.rating-wrapper img');
    stars.forEach(star => star.classList.remove('rating-checked'));

    document.getElementById('rating').value = '';
}

// Clear rating and review inputs
function clearRatingAndReviewInputs() {
    document.getElementById('rating').value = '';
    document.getElementById('review').value = '';
    clearStarRating();
}
