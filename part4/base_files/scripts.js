/* ============================================
   GLOBAL FRONT-END SCRIPT
   Handles:
   - Login
   - Place listing + filtering
   - Place details
   - Add review
============================================ */

/* =============================
   SAMPLE PLACE DATA (fallback)
============================= */
const samplePlaces = [
    {
      id: 1,
      name: "Cozy Apartment",
      price: 120,
      host: "Alice",
      image: "images/image1.jpg",
      description: "Nice and cozy.",
      amenities: ["Wi-Fi", "Air Conditioning"],
      reviews: []
    },
    {
      id: 2,
      name: "Beach House",
      price: 250,
      host: "Bob",
      image: "images/image2.jpg",
      description: "Ocean view.",
      amenities: ["Parking", "Wi-Fi"],
      reviews: []
    },
    {
      id: 3,
      name: "Mountain Cabin",
      price: 180,
      host: "Charlie",
      image: "images/image3.jpg",
      description: "Quiet and peaceful.",
      amenities: ["Fireplace", "Heating"],
      reviews: []
    }
];

/* =============================
        COOKIE HELPER
============================= */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
}

/* =============================
     INDEX — CHECK AUTH
============================= */
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!loginLink) return; // not on index.html

    if (!token) {
        loginLink.style.display = 'block';
        displayPlaces(samplePlaces);
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

/* =============================
     INDEX — DISPLAY PLACES
============================= */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = "";

    places.forEach(place => {
        const card = document.createElement('div');
        card.classList.add('place-card');
        card.dataset.price = place.price;

        card.innerHTML = `
            <img src="${place.image}" alt="${place.name}">
            <h3>${place.name}</h3>
            <p class="price">$${place.price} / night</p>
            <p class="host">Host: ${place.host}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(card);
    });
}

/* =============================
     INDEX — FETCH PLACES
============================= */
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Failed to fetch");

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error(error);
        alert("Unable to load places. Showing sample data.");
        displayPlaces(samplePlaces);
    }
}

/* =============================
     INDEX — PRICE FILTER
============================= */
document.addEventListener('DOMContentLoaded', () => {
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const maxPrice = event.target.value;
            const cards = document.querySelectorAll('.place-card');

            cards.forEach(card => {
                const price = parseFloat(card.dataset.price);
                const max = maxPrice === 'All' ? Infinity : parseFloat(maxPrice);
                card.style.display = price <= max ? 'block' : 'none';
            });
        });
    }
});

/* =============================
     LOGIN FORM
============================= */
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication(); // only affects index

    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!email || !password) {
            alert("Please fill all fields.");
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                alert("Login failed.");
                return;
            }

            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;

            window.location.href = "index.html";

        } catch (error) {
            console.error(error);
            alert("Network error.");
        }
    });
});

/* =============================
      PLACE DETAILS PAGE
============================= */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(placeId) {
    const url = `http://127.0.0.1:5000/api/v1/places/${placeId}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch place");

        const place = await response.json();
        displayPlaceDetails(place);

    } catch (error) {
        console.error(error);
        alert("Could not load place details.");
    }
}

function displayPlaceDetails(place) {
    const section = document.getElementById("place-details");
    if (!section) return;

    section.innerHTML = `
        <div class="place-details">
            <img src="${place.image}" alt="${place.name}">
            <div class="place-text">
                <h1>${place.name}</h1>
                <p><strong>Host:</strong> ${place.host}</p>
                <p><strong>Price:</strong> $${place.price}/night</p>
                <p><strong>Description:</strong> ${place.description}</p>
                <p><strong>Amenities:</strong></p>
                <ul>
                    ${place.amenities.map(a => `<li>${a}</li>`).join("")}
                </ul>
            </div>
        </div>

        <h2>Reviews</h2>
        <div id="reviews-section">
            ${place.reviews.length
                ? place.reviews.map(r => `
                    <div class="review-card">
                        <p><strong>${r.user}</strong></p>
                        <p>${r.comment}</p>
                        <p>Rating: ${r.rating}/5</p>
                    </div>
                `).join("")
                : `<p>No reviews yet.</p>`
            }
        </div>
    `;
}

/* =============================
      ADD REVIEW PAGE
============================= */
function checkAuthRedirect() {
    const token = getCookie("token");
    if (!token) window.location.href = "index.html";
    return token;
}

async function submitReview(token, placeId, reviewText) {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/reviews", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                place_id: placeId,
                comment: reviewText
            })
        });

        return response;

    } catch (err) {
        alert("Network error.");
        console.error(err);
    }
}

function handleResponse(response, form) {
    if (response.ok) {
        alert("Review submitted!");
        form.reset();
    } else {
        alert("Failed to submit review.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const reviewForm = document.getElementById("review-form");
    if (!reviewForm) return;

    const token = checkAuthRedirect();
    const placeId = getPlaceIdFromURL();

    reviewForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const reviewText = document.getElementById("review-text").value.trim();
        if (!reviewText) {
            alert("Please write a review.");
            return;
        }

        const response = await submitReview(token, placeId, reviewText);
        handleResponse(response, reviewForm);
    });
});
