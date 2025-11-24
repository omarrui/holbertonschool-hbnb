/* Starter dynamic behavior for HBnB pages */
document.addEventListener('DOMContentLoaded', () => {
	// ===== Utility Functions =====
	function getCookie(name) {
		const match = document.cookie.match(new RegExp('(^|; )' + name + '=([^;]*)'));
		return match ? decodeURIComponent(match[2]) : null;
	}

	function buildPriceFilterOptions(select) {
		if (!select) return;
		select.innerHTML = '';
		const options = [
			{ value: '10', label: 'Up to $10' },
			{ value: '50', label: 'Up to $50' },
			{ value: '100', label: 'Up to $100' },
			{ value: '', label: 'All' }
		];
		options.forEach(opt => {
			const o = document.createElement('option');
			o.value = opt.value; o.textContent = opt.label; select.appendChild(o);
		});
	}

	function normalizePlace(p) {
		return {
			id: p.id,
			name: p.name || p.title || 'Untitled',
			price: (p.price_per_night !== undefined && p.price_per_night !== null) ? p.price_per_night : (p.price || 0),
			description: p.description || '',
			image: p.image_filename || p.image || null,
			average_rating: p.average_rating != null ? p.average_rating : null,
			review_count: p.review_count != null ? p.review_count : 0,
		};
	}

	function showLoading(container) {
		if (!container) return;
		container.innerHTML = '<p class="loading">Loading places...</p>';
	}

	function showError(container, msg) {
		if (!container) return;
		container.innerHTML = `<p class="error-state">${msg}</p>`;
	}

	function showEmpty(container) {
		if (!container) return;
		container.innerHTML = '<p class="empty-state">No places available.</p>';
	}

	async function fetchPlaces(token) {
		const container = document.getElementById('places-cards');
		showLoading(container);
		try {
			const headers = {};
			if (token) headers['Authorization'] = 'Bearer ' + token;
			const resp = await fetch('/api/v1/places/');
			if (!resp.ok) {
				showError(container, 'Failed to load places');
				return [];
			}
			const data = await resp.json();
			if (!Array.isArray(data) || data.length === 0) {
				showEmpty(container);
				return [];
			}
			const normalized = data.map(normalizePlace);
			displayPlaces(normalized);
			return normalized;
		} catch (e) {
			showError(container, 'Network error while loading places');
			return [];
		}
	}

	function displayPlaces(places) {
		const container = document.getElementById('places-cards');
		if (!container) return;
		container.innerHTML = '';
		// Decode token claims to know if admin (for delete buttons)
		const token = getCookie('token');
		let isAdmin = false;
		if (token) {
			try {
				const parts = token.split('.');
				if (parts.length >= 2) {
					const payloadRaw = parts[1].replace(/-/g,'+').replace(/_/g,'/');
					const pad = payloadRaw.length % 4;
					const base64 = pad ? payloadRaw + '='.repeat(4-pad) : payloadRaw;
					const claims = JSON.parse(atob(base64));
					isAdmin = !!claims.is_admin;
				}
			} catch(e){ /* ignore */ }
		}
		places.forEach(pl => {
			const article = document.createElement('article');
			article.className = 'place-card';
			article.setAttribute('data-price', pl.price);
			article.setAttribute('aria-labelledby', 'place-title-' + pl.id);
			const imgTag = pl.image ? `<a href="/place/${pl.id}" class="place-thumb-link" aria-label="View details for ${pl.name}"><div class="place-thumb"><img src="/static/img/${pl.image}" alt="Image of ${pl.name}" loading="lazy"></div></a>` : '';
			const delBtn = isAdmin ? `<button class="place-delete" data-place-id="${pl.id}" aria-label="Delete place">✖</button>` : '';
			let starsHtml = '';
			if (pl.review_count > 0 && pl.average_rating != null) {
				const full = Math.floor(pl.average_rating);
				const hasHalf = (pl.average_rating - full) >= 0.5;
				const totalStars = 5;
				let starElems = [];
				for (let i = 0; i < full; i++) starElems.push('<span class="star full">★</span>');
				if (hasHalf) starElems.push('<span class="star half">★</span>');
				const remaining = totalStars - starElems.length;
				for (let i = 0; i < remaining; i++) starElems.push('<span class="star empty">☆</span>');
				starsHtml = `<div class="rating-block" aria-label="Average rating ${pl.average_rating} over ${pl.review_count} reviews"><div class="rating-stars">${starElems.join('')}</div><div class="rating-summary">${pl.average_rating} / 5 <span class="rating-count">(${pl.review_count})</span></div></div>`;
			} else {
				starsHtml = '<div class="rating-block empty" aria-label="No reviews yet">No reviews</div>';
			}
			article.innerHTML = `
				${imgTag}
				${delBtn}
				<header><h3 id="place-title-${pl.id}" class="place-name">${pl.name}</h3></header>
				${starsHtml}
				<div class="place-price">$${pl.price} <span class="per-night">/night</span></div>
				<footer><a href="/place/${pl.id}" class="details-button" aria-label="View details for ${pl.name}">View Details</a></footer>
			`;
			// Make entire card clickable (except if an inner link was explicitly clicked)
			article.addEventListener('click', (e) => {
				// If user clicked an existing anchor element, let default happen
				if (e.target.closest('a')) return;
				window.location.href = '/place/' + pl.id;
			});
			container.appendChild(article);
		});
		// Bind place delete buttons (admin only)
		[...container.querySelectorAll('.place-delete')].forEach(btn => {
			btn.addEventListener('click', async (e) => {
				e.preventDefault(); e.stopPropagation();
				const pid = btn.dataset.placeId; if (!pid) return;
				btn.disabled = true; btn.textContent = '…';
				try {
					const resp = await fetch(`/api/v1/places/${pid}`, { method: 'DELETE', headers: { 'Authorization': 'Bearer ' + token }});
					if (resp.ok) {
						const card = container.querySelector(`.place-card .place-delete[data-place-id="${pid}"]`)?.closest('.place-card');
						if (card) card.remove();
						if (!container.querySelector('.place-card')) {
							container.innerHTML = '<p class="empty-state">No places available.</p>';
						}
					} else {
						btn.textContent = 'Err'; setTimeout(()=>{ btn.textContent = '✖'; btn.disabled=false; },1500);
					}
				} catch(err){
					btn.textContent = 'Net'; setTimeout(()=>{ btn.textContent = '✖'; btn.disabled=false; },1500);
				}
			});
		});
	}

	function attachPriceFilter() {
		const select = document.getElementById('price-filter');
		if (!select) return;
		buildPriceFilterOptions(select);
		select.addEventListener('change', () => {
			const maxStr = select.value.trim();
			const max = maxStr === '' ? Infinity : parseFloat(maxStr);
			[...document.querySelectorAll('.place-card')].forEach(card => {
				const price = parseFloat(card.getAttribute('data-price'));
				card.style.display = (price <= max) ? '' : 'none';
			});
		});
	}

	function checkAuthenticationAndLoad() {
		const token = getCookie('token');
		// Toggle login link (if present)
		const loginLink = document.querySelector('a.login-button[href="/login"]');
		if (loginLink) {
			if (token) {
				loginLink.style.display = 'none';
			} else {
				loginLink.style.display = '';
			}
		}
		// Load places regardless (public endpoint), still send token if needed later
		fetchPlaces(token).then(() => attachPriceFilter());
	}

	// ===== Place Details (Task 3) =====
	function isPlaceDetailsPage() {
		return window.location.pathname.startsWith('/place/') && document.getElementById('place-details');
	}

	function getPlaceId() {
		// Path form /place/<uuid>
		const m = window.location.pathname.match(/\/place\/(.+)$/);
		if (m && m[1]) return m[1];
		// Fallback query param ?id=...
		const params = new URLSearchParams(window.location.search);
		return params.get('id');
	}

	function showPlaceLoading() {
		const d = document.getElementById('place-details');
		if (d) d.innerHTML = '<p class="loading">Loading place...</p>';
		const r = document.getElementById('reviews-cards');
		if (r) r.innerHTML = '<p class="loading">Loading reviews...</p>';
	}

	function showPlaceError(msg) {
		const d = document.getElementById('place-details');
		if (d) d.innerHTML = `<p class="error-state">${msg}</p>`;
		const r = document.getElementById('reviews-cards');
		if (r) r.innerHTML = '';
	}

	function renderPlaceDetails(place) {
		const d = document.getElementById('place-details');
		if (!d) return;
		const name = place.name || place.title || 'Untitled';
		const price = place.price_per_night != null ? place.price_per_night : (place.price || 0);
		const desc = place.description || 'No description.';
		const image = place.image_filename || place.image || null;
		const avg = place.average_rating;
		const reviewCount = place.review_count || 0;
		let hostDisplay = 'Host: Unknown';
		if (place.host && (place.host.full_name || place.host.first_name)) {
			const full = place.host.full_name || `${place.host.first_name || ''} ${place.host.last_name || ''}`.trim();
			hostDisplay = 'Host: ' + (full || place.host.id || 'Unknown');
		} else if (place.host_id) {
			hostDisplay = 'Host ID: ' + place.host_id;
		}
		const amenities = Array.isArray(place.amenities) ? place.amenities : [];
		// Decode token for admin deletion on detail page
		const token = getCookie('token');
		let isAdmin = false;
		if (token) {
			try {
				const parts = token.split('.');
				if (parts.length >= 2) {
					const payloadRaw = parts[1].replace(/-/g,'+').replace(/_/g,'/');
					const pad = payloadRaw.length % 4;
					const base64 = pad ? payloadRaw + '='.repeat(4-pad) : payloadRaw;
					const claims = JSON.parse(atob(base64));
					isAdmin = !!claims.is_admin;
				}
			} catch(e){}
		}
		const amenityHtml = amenities.length ? `<ul class="amenity-list">${amenities.map(a => `<li class="amenity">${a.name || 'Unnamed'}</li>`).join('')}</ul>` : '<p>No amenities listed.</p>';
		const imgHtml = image ? `<div class="place-image"><img src="/static/img/${image}" alt="Image of ${name}" loading="lazy"></div>` : '';
		let starsSection = '';
		if (reviewCount > 0 && avg != null) {
			const full = Math.floor(avg);
			const hasHalf = (avg - full) >= 0.5;
			const totalStars = 5;
			let starElems = [];
			for (let i = 0; i < full; i++) starElems.push('<span class="star full">★</span>');
			if (hasHalf) starElems.push('<span class="star half">★</span>');
			const remaining = totalStars - starElems.length;
			for (let i = 0; i < remaining; i++) starElems.push('<span class="star empty">☆</span>');
			starsSection = `<div class="detail-rating" aria-label="Average rating ${avg} over ${reviewCount} reviews"><div class="rating-stars">${starElems.join('')}</div><div class="rating-summary">${avg} / 5 (${reviewCount})</div></div>`;
		} else {
			starsSection = '<div class="detail-rating no-reviews" aria-label="No reviews yet">No reviews yet</div>';
		}
		d.innerHTML = `
			<header><h2 id="place-name" class="place-name">${name}</h2><p class="host">${hostDisplay}</p>${isAdmin ? '<button class="place-delete-detail" aria-label="Delete place">Delete Place</button>' : ''}</header>
			${imgHtml}
			<div class="place-info">
				${starsSection}
				<p class="price">Price: $${price} / night</p>
				<p class="description">${desc}</p>
				<div class="amenities"><h3>Amenities</h3>${amenityHtml}</div>
			</div>`;
		// Bind delete on detail page
		if (isAdmin) {
			const del = d.querySelector('.place-delete-detail');
			if (del) {
				del.addEventListener('click', async () => {
					if (!confirm('Delete this place permanently?')) return;
					del.disabled = true; del.textContent = 'Deleting…';
					try {
						const pid = place.id || getPlaceId();
						const resp = await fetch(`/api/v1/places/${pid}`, { method: 'DELETE', headers: { 'Authorization': 'Bearer ' + token }});
						if (resp.ok) {
							window.location.href = '/';
						} else {
							del.textContent = 'Error'; setTimeout(()=>{ del.textContent='Delete Place'; del.disabled=false; },1600);
						}
					} catch(err){
						del.textContent = 'Network'; setTimeout(()=>{ del.textContent='Delete Place'; del.disabled=false; },1600);
					}
				});
			}
		}
	}

	function renderReviews(reviews) {
		const container = document.getElementById('reviews-cards');
		if (!container) return;
		if (!Array.isArray(reviews) || reviews.length === 0) {
			container.innerHTML = '<p class="empty-state">No reviews yet.</p>';
			return;
		}
		// Determine current user claims from token
		const token = getCookie('token');
		let currentUserId = null;
		let isAdmin = false;
		if (token) {
			try {
				const parts = token.split('.');
				if (parts.length >= 2) {
					const payloadRaw = parts[1].replace(/-/g, '+').replace(/_/g, '/');
					// Add padding if needed
					const pad = payloadRaw.length % 4;
					const base64 = pad ? payloadRaw + '='.repeat(4 - pad) : payloadRaw;
					const json = atob(base64);
					const claims = JSON.parse(json);
					currentUserId = claims.user_id || claims.sub || null;
					isAdmin = !!claims.is_admin;
				}
			} catch (e) { /* ignore decode errors */ }
		}
		container.innerHTML = reviews.map(r => {
			const comment = r.comment || r.text || '(no comment)';
			const rating = r.rating != null ? r.rating : '-';
			const canDelete = isAdmin || (currentUserId && r.user_id === currentUserId);
			const delBtn = canDelete ? `<button class="review-delete" data-review-id="${r.id}" aria-label="Delete review">✖</button>` : '';
			return `<div class="review-card" data-review-id="${r.id}">${delBtn}<p class="review-comment">${comment}</p><p class="review-meta">Rating: <span class="rating">${rating}</span></p></div>`;
		}).join('');
		// Bind delete handlers
		[...container.querySelectorAll('.review-delete')].forEach(btn => {
			btn.addEventListener('click', async (e) => {
				e.preventDefault();
				const id = btn.dataset.reviewId;
				if (!id) return;
				btn.disabled = true;
				btn.textContent = '…';
				try {
					const resp = await fetch(`/api/v1/reviews/${id}`, { method: 'DELETE', headers: { 'Authorization': 'Bearer ' + token } });
					if (resp.ok) {
						// Remove card without full reload
						const card = container.querySelector(`.review-card[data-review-id="${id}"]`);
						if (card) card.remove();
						if (!container.querySelector('.review-card')) {
							container.innerHTML = '<p class="empty-state">No reviews yet.</p>';
						}
					} else {
						btn.textContent = 'Err';
						setTimeout(()=>{ btn.textContent='✖'; btn.disabled=false; },1500);
					}
				} catch (err) {
					btn.textContent = 'Net';
					setTimeout(()=>{ btn.textContent='✖'; btn.disabled=false; },1500);
				}
			});
		});
	}

	async function fetchPlaceDetails(token, placeId) {
		showPlaceLoading();
		try {
			const headers = {};
			if (token) headers['Authorization'] = 'Bearer ' + token;
			const resp = await fetch(`/api/v1/places/${placeId}`, { headers });
			if (resp.status === 404) {
				showPlaceError('Place not found');
				return;
			}
			if (!resp.ok) {
				showPlaceError('Failed to load place');
				return;
			}
			const data = await resp.json();
			renderPlaceDetails(data);
			renderReviews(data.reviews);
		} catch (e) {
			showPlaceError('Network error');
		}
	}

	function initPlaceDetailsFlow() {
		const placeId = getPlaceId();
		if (!placeId) {
			showPlaceError('Invalid place ID');
			return;
		}
		const token = getCookie('token');
		// Toggle review form visibility
		const form = document.getElementById('review-form');
		const prompt = document.querySelector('#add-review .login-prompt');
		if (token) {
			if (form) form.style.display = '';
			if (prompt) prompt.style.display = 'none';
			// Star rating interactive setup
			const starWrap = form ? form.querySelector('#star-select') : null;
			const ratingHidden = form ? form.querySelector('#rating') : null;
			if (starWrap && ratingHidden && !starWrap.dataset.enhanced) {
				starWrap.dataset.enhanced = 'true';
				const updateStars = (val) => {
					[...starWrap.querySelectorAll('.star-choice')].forEach(btn => {
						const v = parseInt(btn.dataset.value, 10);
						if (v <= val) {
							btn.textContent = '★';
							btn.classList.add('active');
						} else {
							btn.textContent = '☆';
							btn.classList.remove('active');
						}
					});
				};
				starWrap.addEventListener('click', (e) => {
					const btn = e.target.closest('.star-choice');
					if (!btn) return;
					const val = parseInt(btn.dataset.value, 10);
					if (!isNaN(val)) {
						ratingHidden.value = String(val);
						starWrap.dataset.selected = String(val);
						updateStars(val);
					}
				});
				// Keyboard support
				starWrap.addEventListener('keydown', (e) => {
					const current = parseInt(starWrap.dataset.selected || '0', 10);
					if (['ArrowRight','ArrowUp'].includes(e.key)) {
						const next = Math.min(current + 1, 5);
						ratingHidden.value = String(next);
						starWrap.dataset.selected = String(next);
						updateStars(next);
						e.preventDefault();
					} else if (['ArrowLeft','ArrowDown'].includes(e.key)) {
						const prev = Math.max(current - 1, 1);
						ratingHidden.value = String(prev);
						starWrap.dataset.selected = String(prev);
						updateStars(prev);
						e.preventDefault();
					}
				});
				// Initialize stars empty
				updateStars(0);
			}
			// Attach enhanced AJAX submission for place details page
			if (form && !form.dataset.ajaxBound) {
				form.dataset.ajaxBound = 'true';
				form.addEventListener('submit', async (e) => {
					e.preventDefault();
					const msg = document.getElementById('place-review-msg');
					if (msg) msg.textContent = '';
					const commentField = form.querySelector('#comment');
					const ratingField = form.querySelector('#rating');
					const comment = commentField ? commentField.value.trim() : '';
					const rating = ratingField && ratingField.value ? parseInt(ratingField.value, 10) : null;
					// Comment optionnel: ne plus bloquer si vide
					if (!rating || rating < 1 || rating > 5) { if (msg) msg.textContent = 'Rating must be 1-5.'; return; }
					if (msg) msg.textContent = 'Submitting review...';
					try {
						const resp = await fetch('/api/v1/reviews/', {
							method: 'POST',
							headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
							body: JSON.stringify({ place_id: placeId, comment, rating })
						});
						const data = await resp.json().catch(() => ({}));
						if (resp.status === 201) {
							if (msg) msg.textContent = 'Review added!';
							form.reset();
							// Refresh reviews list without full page reload
							fetchPlaceDetails(token, placeId);
						} else {
							if (msg) msg.textContent = data.error || 'Failed to submit review.';
						}
					} catch (err) {
						if (msg) msg.textContent = 'Network error.';
					}
				});
			}
		} else {
			if (form) form.style.display = 'none';
			if (prompt) prompt.style.display = '';
		}
		fetchPlaceDetails(token, placeId);
	}

	// ===== Create Place (Task 4) =====
	function isCreatePlacePage() {
		return !!document.getElementById('create-place-form');
	}

	async function fetchAmenitiesForForm() {
		const box = document.getElementById('amenities-box');
		if (!box) return;
		try {
			const resp = await fetch('/api/v1/amenities/');
			if (!resp.ok) {
				box.innerHTML = '<p class="error-state">Failed to load amenities.</p>';
				return;
			}
			const data = await resp.json();
			if (!Array.isArray(data) || data.length === 0) {
				box.innerHTML = '<p>No amenities available.</p>';
				return;
			}
			box.innerHTML = data.map(a => {
				return `<label class="amenity-check"><input type="checkbox" name="amenity" value="${a.id}"> ${a.name || 'Unnamed'}</label>`;
			}).join('');
		} catch (e) {
			box.innerHTML = '<p class="error-state">Network error loading amenities.</p>';
		}
	}

	// ===== Add Review (Task 4 - AJAX form) =====
	function isAddReviewPage() {
		return window.location.pathname.includes('/review/add') && document.getElementById('review-form');
	}

	function extractPlaceIdForReview() {
		// Path format: /place/<id>/review/add
		const m = window.location.pathname.match(/\/place\/([^\/]+)\/review\/add/);
		if (m && m[1]) return m[1];
		// Fallback query param ?place_id=...
		const params = new URLSearchParams(window.location.search);
		return params.get('place_id') || params.get('id');
	}

	function initAddReviewFlow() {
		const form = document.getElementById('review-form');
		if (!form) return;
		const token = getCookie('token');
		if (!token) {
			// Requirement: redirect unauthenticated users to index page; provide brief feedback before redirect
			const msg = document.getElementById('review-msg');
			if (msg) { msg.textContent = 'You must be logged in to review. Redirecting...'; }
			setTimeout(() => { window.location.href = '/'; }, 600);
			return;
		}
		const placeId = extractPlaceIdForReview();
		if (!placeId) {
			alert('Invalid place id');
			return;
		}
		let msg = document.getElementById('review-msg');
		if (!msg) {
			msg = document.createElement('div');
			msg.id = 'review-msg';
			form.appendChild(msg);
		}
		form.addEventListener('submit', async (e) => {
			e.preventDefault();
			msg.textContent = '';
			const commentField = form.querySelector('#comment');
			const ratingField = form.querySelector('#rating');
			const comment = commentField ? commentField.value.trim() : '';
			const rating = ratingField && ratingField.value ? parseInt(ratingField.value, 10) : null;
			// Comment optionnel: ne pas bloquer sur champ vide
			if (!rating || rating < 1 || rating > 5) {
				msg.textContent = 'Rating must be between 1 and 5';
				return;
			}
			const payload = { place_id: placeId, comment, rating };
			try {
				const resp = await fetch('/api/v1/reviews/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': 'Bearer ' + token
					},
					body: JSON.stringify(payload)
				});
				const data = await resp.json().catch(() => ({}));
				if (resp.status === 201) {
					msg.textContent = 'Review submitted successfully! Redirecting...';
					form.reset();
					setTimeout(() => { window.location.href = '/place/' + placeId; }, 1000);
				} else {
					msg.textContent = data.error || 'Failed to submit review';
				}
			} catch (err) {
				msg.textContent = 'Network error submitting review.';
			}
		});
	}

	// Enhance standalone add review page star selection
	const standaloneStarWrap = document.querySelector('#review-form #star-select');
	const standaloneRatingHidden = document.querySelector('#review-form #rating');
	if (standaloneStarWrap && standaloneRatingHidden && !standaloneStarWrap.dataset.enhanced) {
		standaloneStarWrap.dataset.enhanced = 'true';
		const updateStarsStandalone = (val) => {
			[...standaloneStarWrap.querySelectorAll('.star-choice')].forEach(btn => {
				const v = parseInt(btn.dataset.value, 10);
				if (v <= val) {
					btn.textContent = '★';
					btn.classList.add('active');
				} else {
					btn.textContent = '☆';
					btn.classList.remove('active');
				}
			});
		};
		standaloneStarWrap.addEventListener('click', (e) => {
			const btn = e.target.closest('.star-choice');
			if (!btn) return;
			const val = parseInt(btn.dataset.value, 10);
			if (!isNaN(val)) {
				standaloneRatingHidden.value = String(val);
				standaloneStarWrap.dataset.selected = String(val);
				updateStarsStandalone(val);
			}
		});
		standaloneStarWrap.addEventListener('keydown', (e) => {
			const current = parseInt(standaloneStarWrap.dataset.selected || '0', 10);
			if (['ArrowRight','ArrowUp'].includes(e.key)) {
				const next = Math.min(current + 1, 5);
				standaloneRatingHidden.value = String(next);
				standaloneStarWrap.dataset.selected = String(next);
				updateStarsStandalone(next);
				e.preventDefault();
			} else if (['ArrowLeft','ArrowDown'].includes(e.key)) {
				const prev = Math.max(current - 1, 1);
				standaloneRatingHidden.value = String(prev);
				standaloneStarWrap.dataset.selected = String(prev);
				updateStarsStandalone(prev);
				e.preventDefault();
			}
		});
		updateStarsStandalone(0);
	}

	function initCreatePlaceFlow() {
		const form = document.getElementById('create-place-form');
		const loginPrompt = document.getElementById('create-place-login');
		const msg = document.getElementById('create-place-msg');
		const token = getCookie('token');
		if (!form) return;
		if (!token) {
			form.style.display = 'none';
			if (loginPrompt) loginPrompt.style.display = '';
			return;
		}
		if (loginPrompt) loginPrompt.style.display = 'none';
		fetchAmenitiesForForm();
		form.addEventListener('submit', async (e) => {
			e.preventDefault();
			msg.textContent = '';
			const title = form.title.value.trim();
			const priceVal = form.price.value.trim();
			const description = form.description.value.trim();
			const latitude = form.latitude.value.trim();
			const longitude = form.longitude.value.trim();
			if (!title || !priceVal) {
				msg.textContent = 'Title and price are required.';
				return;
			}
			const price = parseFloat(priceVal);
			if (isNaN(price) || price < 0) {
				msg.textContent = 'Invalid price value.';
				return;
			}
			let latNum = latitude ? parseFloat(latitude) : null;
			let lonNum = longitude ? parseFloat(longitude) : null;
			if (latNum != null && (latNum < -90 || latNum > 90)) {
				msg.textContent = 'Latitude out of range.';
				return;
			}
			if (lonNum != null && (lonNum < -180 || lonNum > 180)) {
				msg.textContent = 'Longitude out of range.';
				return;
			}
			const amenityIds = [...form.querySelectorAll('input[name="amenity"]:checked')].map(cb => cb.value);
			const payload = {
				title: title,
				description: description || undefined,
				price: price,
				latitude: latNum,
				longitude: lonNum,
				amenities: amenityIds
			};
			try {
				const resp = await fetch('/api/v1/places/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': 'Bearer ' + token
					},
					body: JSON.stringify(payload)
				});
				const data = await resp.json().catch(()=>({}));
				if (resp.status === 201) {
					msg.textContent = 'Place created successfully. Redirecting...';
					const newId = data.id;
					setTimeout(() => {
						if (newId) window.location.href = '/place/' + newId;
						else window.location.href = '/';
					}, 800);
				} else {
					msg.textContent = data.error || 'Failed to create place.';
				}
			} catch (err) {
				msg.textContent = 'Network error creating place.';
			}
		});
	}


	const priceFilter = document.getElementById('price-filter');
	const placesCards = document.getElementById('places-cards');

	// Initial dynamic load for index page
	if (document.getElementById('places-cards')) {
		checkAuthenticationAndLoad();
	}

	// Initialize place details dynamic flow if on detail page
	if (isPlaceDetailsPage()) {
		initPlaceDetailsFlow();
	}

	// Initialize create place flow
	if (isCreatePlacePage()) {
		initCreatePlaceFlow();
	}

	// Initialize add review flow
	if (isAddReviewPage()) {
		initAddReviewFlow();
	}

	// Registration AJAX (independent)
	const registerForm = document.getElementById('register-form');
	if (registerForm) {
		registerForm.addEventListener('submit', async (e) => {
			e.preventDefault();
			const first_name = registerForm.first_name.value.trim();
			const last_name = registerForm.last_name.value.trim();
			const email = registerForm.email.value.trim();
			const password = registerForm.password.value.trim();
			const errorBox = document.getElementById('register-error');
			errorBox.textContent = '';
			if (!first_name || !last_name || !email || !password) {
				errorBox.textContent = 'All fields required';
				return;
			}
			try {
				const resp = await fetch('/api/v1/auth/register', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ first_name, last_name, email, password })
				});
				if (resp.status === 409) {
					const d = await resp.json().catch(()=>({}));
					errorBox.textContent = d.error || 'Email already exists';
					return;
				}
				if (resp.ok) {
					const data = await resp.json();
					if (data.access_token) {
						document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
						window.location.href = '/';
					} else {
						errorBox.textContent = 'Token missing in response';
					}
				} else {
					const errData = await resp.json().catch(()=>({}));
					errorBox.textContent = errData.error || ('Registration failed: ' + resp.status);
				}
			} catch (err) {
				errorBox.textContent = 'Network error: ' + err.message;
			}
		});
	}

	// Login AJAX
	const loginForm = document.getElementById('login-form');
	if (loginForm) {
		loginForm.addEventListener('submit', async (e) => {
			e.preventDefault();
			const email = loginForm.email.value.trim();
			const password = loginForm.password.value.trim();
			const errorBox = document.getElementById('login-error');
			errorBox.textContent = '';
			if (!email || !password) {
				errorBox.textContent = 'Email and password required';
				return;
			}
			try {
				const resp = await fetch('/api/v1/auth/login', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ email, password })
				});
				if (resp.ok) {
					const data = await resp.json();
					if (data.access_token) {
						document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
						window.location.href = '/';
					} else {
						errorBox.textContent = 'Token missing in response';
					}
				} else {
					const errData = await resp.json().catch(() => ({}));
					errorBox.textContent = errData.error || ('Login failed: ' + resp.status);
				}
			} catch (err) {
				errorBox.textContent = 'Network error: ' + err.message;
			}
		});
	}

	// (Legacy simple validation removed; replaced by context-aware AJAX flow)

	// Toggle login/logout button based on token presence
	const hasToken = /(^|; )token=/.test(document.cookie);
	const navLoginLink = document.querySelector('.login-button');
	if (navLoginLink && hasToken) {
		navLoginLink.textContent = 'Logout';
		navLoginLink.addEventListener('click', (e) => {
			e.preventDefault();
			// Clear cookie
			document.cookie = 'token=; Max-Age=0; path=/; SameSite=Lax';
			window.location.href = '/login';
		});
	}
});
