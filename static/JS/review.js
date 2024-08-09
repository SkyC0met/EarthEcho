document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.rating-wrapper img');
    const clearButton = document.querySelector('.rating-wrapper button');
    const reviewForm = document.getElementById('reviewForm');
    const reviewsContainer = document.getElementById('reviews');
    const showMoreBtn = document.getElementById('showMoreBtn');
    const currentPageInput = document.getElementById('currentPage');
    const reviewsPerPageInput = document.getElementById('reviewsPerPage');
    const averageRatingElem = document.getElementById('averageRating');
    const ratingChartElem = document.getElementById('ratingChart');
    const postIdInput = document.getElementById('postId'); // Hidden input for post ID

    let currentPage = parseInt(currentPageInput?.value) || 1;
    const reviewsPerPage = parseInt(reviewsPerPageInput?.value) || 3;
    let totalReviews = 0;
    let reviewsDisplayed = 0;
    const postId = postIdInput?.value; // Get the post ID

    // Log postId to verify
    console.log('Post ID:', postId);
    console.log('Show More Button:', showMoreBtn);


    function updateStarRating(clickedRating) {
        stars.forEach(star => star.classList.remove('rating-checked'));
        for (let i = 0; i < clickedRating; i++) {
            stars[i].classList.add('rating-checked');
        }
        document.getElementById('rating').value = clickedRating;
    }

    function clearStarRating() {
        stars.forEach(star => star.classList.remove('rating-checked'));
        document.getElementById('rating').value = '';
    }

    function updateRatingChart(ratingDistribution) {
        if (!ratingChartElem) return;

        const ctx = ratingChartElem.getContext('2d');

        if (window.ratingChart && window.ratingChart.destroy) {
            window.ratingChart.destroy();
        }

        window.ratingChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
                datasets: [{
                    label: 'No. of Reviews',
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

    function fetchReviews(page) {
        if (!postId) return; // Ensure postId is present

        fetch(`/get_reviews?page=${page}&limit=${reviewsPerPage}&post_id=${postId}`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.reviews && data.reviews.length > 0) {
                    totalReviews = data.total_reviews || totalReviews;
                    reviewsDisplayed += data.reviews.length;

                    data.reviews.forEach(review => {
                        const reviewElement = document.createElement('div');
                        reviewElement.classList.add('review');
                        reviewElement.innerHTML = `
                            <p><b>Username:</b> ${review.username}</p>
                            <p><b>Date and Time:</b> ${review.timestamp}</p>
                            <p><b>Rating:</b> ${review.rating}</p>
                            <p><b>Review:</b> ${review.review}</p>
                        `;
                        reviewsContainer.appendChild(reviewElement);
                    });

                    if (averageRatingElem) {
                        const averageRating = parseFloat(data.average_rating);
                        averageRatingElem.textContent = `Average Rating: ${isNaN(averageRating) ? 'N/A' : averageRating.toFixed(1)} / 5`;
                    }

                    updateRatingChart(data.rating_distribution);

                    currentPage++;
                    currentPageInput.value = currentPage;

                    showMoreBtn.textContent = reviewsDisplayed >= totalReviews ? 'Show Less' : 'Show More';
                } else {
                    showMoreBtn.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
    }

    if (stars.length > 0) {
        stars.forEach(star => {
            star.addEventListener('click', function () {
                const rating = this.id;
                updateStarRating(rating);
            });
        });
    }

    if (clearButton) {
        clearButton.addEventListener('click', clearStarRating);
    }

    if (reviewForm) {
        reviewForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(this);
            const csrfToken = document.querySelector('input[name="csrf_token"]').value;

            // Log FormData to verify
            console.log('FormData:', Array.from(formData.entries()));

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
                    window.location.reload();
                } else {
                    console.error('Error response:', data.message);
                    if (data.message === "You have submitted too many reviews today") {
                        alert('You have reached the max number of reviews you can submit today');
                    } else {
                        alert('Error: ' + data.message);
                    }
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                alert('Error submitting review. Please try again later.');
            });
        });
    }

    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', function (event) {
            event.preventDefault();
            if (showMoreBtn.textContent === 'Show Less') {
                reviewsContainer.innerHTML = '';
                currentPage = 1;
                reviewsDisplayed = 0;
                currentPageInput.value = currentPage;
                fetchReviews(currentPage);
                showMoreBtn.textContent = 'Show More';
            } else {
                fetchReviews(currentPage);
            }
        });
    }

    // Initial load
    fetchReviews(currentPage);
});
