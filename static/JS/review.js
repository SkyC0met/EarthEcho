document.addEventListener('DOMContentLoaded', function () {
    // Star rating click handlers
    const stars = document.querySelectorAll('.rating-wrapper img');
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.id;
            updateStarRating(rating);
        });
    });

    // Clear button handler
    const clearButton = document.querySelector('.rating-wrapper button');
    if (clearButton) {
        clearButton.addEventListener('click', clearStarRating);
    }

    // Review form submit handler
    document.getElementById('reviewForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(this);

        // CSRF token from hidden input
        const csrfToken = document.querySelector('input[name="csrf_token"]').value;

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const reviewsContainer = document.getElementById('reviews');
                const newReview = document.createElement('div');
                newReview.classList.add('review');
                newReview.innerHTML = `
                    <p>Username: ${data.username}</p>
                    <p>Date and Time: ${data.timestamp}</p>
                    <p>Rating: ${data.rating}</p>
                    <p>Review: ${data.review}</p>
                    <hr>
                `;
                reviewsContainer.prepend(newReview);
                clearRatingAndReviewInputs();

                // Fetch updated reviews and rating distribution
                fetchReviews(currentPage);
            } else {
                console.error('Error response:', data.message);
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
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

    // Display reviews with pagination
    let currentPage = parseInt(document.getElementById('currentPage').value) || 1;
    const reviewsPerPage = parseInt(document.getElementById('reviewsPerPage').value) || 3;
    const reviewsContainer = document.getElementById('reviews');
    const showMoreBtn = document.getElementById('showMoreBtn');
    let isShowingAllReviews = false; // Track if all reviews are shown

    // Fetch reviews function
    function fetchReviews(page) {
        fetch(`/get_reviews?page=${page}&limit=${reviewsPerPage}`)
            .then(response => response.json())
            .then(data => {
                console.log('Fetched Reviews Data:', data);

                if (data.reviews && data.reviews.length > 0) {
                    data.reviews.forEach(review => {
                        const reviewElement = document.createElement('div');
                        reviewElement.classList.add('review');
                        reviewElement.innerHTML = `
                            <p>Username: ${review.username}</p>
                            <p>Date and Time: ${review.timestamp}</p>
                            <p>Rating: ${review.rating}</p>
                            <p>Review: ${review.review}</p>
                            <hr>
                        `;
                        reviewsContainer.appendChild(reviewElement);
                    });

                    // Update average rating
                    const averageRatingElem = document.getElementById('averageRating');
                    if (averageRatingElem) {
                        const averageRating = parseFloat(data.average_rating);
                        averageRatingElem.innerHTML = `Average Rating: ${isNaN(averageRating) ? 'N/A' : averageRating.toFixed(1)} / 5`;
                    }

                    // Update rating distribution chart
                    updateRatingChart(data.rating_distribution);

                    currentPage++;
                    document.getElementById('currentPage').value = currentPage;

                    if (data.reviews.length < reviewsPerPage) {
                        showMoreBtn.textContent = 'Show Less'; // Change to make it become show less
                        isShowingAllReviews = true;
                    }
                } else {
                    showMoreBtn.style.display = 'none'; // Hide button if no more reviews
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
    }

    // Update rating chart function
    function updateRatingChart(ratingDistribution) {
        console.log('Updating Rating Chart with:', ratingDistribution);

        const ctx = document.getElementById('ratingChart').getContext('2d');

        // Destroy the existing chart if it exists
        if (window.ratingChart && window.ratingChart.destroy) {
            window.ratingChart.destroy();
        }

        // Create a new chart
        window.ratingChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
                datasets: [{
                    label: 'no of reviews',
                    data: ratingDistribution,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    barThickness: 30,
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        bottom: 50
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                        }

                    },
                    y: {
                        beginAtZero: true,
                    }
                }
            }
        });
    }

    // Initial load
    fetchReviews(currentPage);

    // Show more button handler
    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', function (event) {
            event.preventDefault();
            if (isShowingAllReviews) {
                reviewsContainer.innerHTML = ''; // Clear all reviews
                currentPage = 1;
                document.getElementById('currentPage').value = currentPage;
                fetchReviews(currentPage);
                showMoreBtn.textContent = 'Show More';
                isShowingAllReviews = false;
            } else {
                fetchReviews(currentPage);
            }
        });
    }
});
