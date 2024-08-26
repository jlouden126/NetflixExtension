// Function to extract the movie/show title from the <title> tag
function getTitleFromHead() {
    const titleTag = document.querySelector('title');
    if (titleTag) {
        const fullTitle = titleTag.innerText;
        const movieTitle = fullTitle.replace(' - Netflix', ''); // Remove the " - Netflix" part
        return movieTitle;
    }
    return null;
}

// Function to get the movie name from the "About" section
function getMovieNameFromAboutSection() {
    const aboutSectionStrongTag = document.querySelector('strong');
    if (aboutSectionStrongTag) {
        return aboutSectionStrongTag.innerText.trim(); // Get the text inside <strong>
    }
    return null;
}

// Function to extract the release year from the Netflix page
function getReleaseYearFromNetflix() {
    const releaseYearElement = document.querySelector('.year'); // Adjust selector as needed
    if (releaseYearElement) {
        return releaseYearElement.innerText.trim();
    }
    return null;
}

function isTvShowPage() {
    const show = document.querySelector('.previewModal--section-header.episodeSelector-label.show-single-season'); // Adjust selector as needed
    if (show) {
        return true;
    }
    return false;
}

// Function to inject ratings into the Netflix page
function injectRatings(ratings) {
    // First, check if the ratings are already injected
    if (document.querySelector('.movie-ratings')) {
        return; // Ratings are already injected, no need to inject again
    }

    const ratingElement = document.createElement('div');
    ratingElement.className = 'movie-ratings';
    ratingElement.innerHTML = `IMDb: ${ratings.imdbRating || 'N/A'}, Rotten Tomatoes: ${ratings.rtRating || 'N/A'}, Metacritic: ${ratings.metacriticRating || 'N/A'}`;

    const titleCardDetails = document.querySelector('.videoMetadata--container');
    if (titleCardDetails && !document.querySelector('.movie-ratings')) {
        titleCardDetails.appendChild(ratingElement);
    }
}

function sendMovieDataToBackend(movieTitle, releaseYear) {
    console.log("SNE DBACK")
    if (isTvShowPage()) {
        console.log('Detected TV show, skipping API call.');
        return; // Skip the API call if it's a TV show
    }

    const data = {
        title: movieTitle,
        year: releaseYear
    };

    fetch('http://127.0.0.1:5000/movies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        injectRatings(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Function to observe the presence of the <strong> element
function observeStrongElement() {
    let lastMovieTitle = null;
    let lastReleaseYear = null;

    const observer = new MutationObserver(function(mutationsList) {
        for (let mutation of mutationsList) {
            if (mutation.type === 'childList') {
                const strongElement = document.querySelector('strong');
                if (strongElement) {
                    const movieTitle = getMovieNameFromAboutSection();
                    
                    const releaseYear = getReleaseYearFromNetflix();
                    if (movieTitle && releaseYear && (movieTitle !== lastMovieTitle || releaseYear !== lastReleaseYear)) {
                        console.log(movieTitle, releaseYear);
                        lastMovieTitle = movieTitle;
                        lastReleaseYear = releaseYear;
                        sendMovieDataToBackend(movieTitle, releaseYear);
                    }
                }
            }
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Start observing for the <strong> element
observeStrongElement();