document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    const keywordInput = document.getElementById('keywordInput');
    const searchButton = document.getElementById('searchButton');
    const searchBtnText = document.getElementById('searchBtnText');
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    const loadingState = document.getElementById('loadingState');
    const resultsContainer = document.getElementById('resultsContainer');
    const emptyState = document.getElementById('emptyState');
    const refreshButton = document.getElementById('refreshButton');

    // Stats elements
    const analyzedCount = document.getElementById('analyzedCount');
    const positiveCount = document.getElementById('positiveCount');
    const positivePercent = document.getElementById('positivePercent');
    const negativeCount = document.getElementById('negativeCount');
    const negativePercent = document.getElementById('negativePercent');
    const neutralCount = document.getElementById('neutralCount');
    const neutralPercent = document.getElementById('neutralPercent');
    const tweetsList = document.getElementById('tweetsList');

    let currentKeyword = '';

    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const keyword = keywordInput.value.trim();
        if (keyword) {
            handleSearch(keyword);
        }
    });

    refreshButton.addEventListener('click', () => {
        if (currentKeyword) {
            handleSearch(currentKeyword);
        }
    });

    async function handleSearch(keyword) {
        currentKeyword = keyword;
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ keyword, count: 20 }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to analyze tweets');
            }

            renderResults(data);
        } catch (err) {
            console.error('Error:', err);
            setError(err.message || 'Failed to analyze tweets. Please try again.');
        } finally {
            setLoading(false);
        }
    }

    function setLoading(isLoading) {
        searchButton.disabled = isLoading;
        searchBtnText.textContent = isLoading ? 'Analyzing...' : 'Search & Analyze';

        if (isLoading) {
            loadingState.classList.remove('hidden');
            resultsContainer.classList.add('hidden');
            emptyState.classList.add('hidden');
            errorMessage.classList.add('hidden');
        } else {
            loadingState.classList.add('hidden');
        }
    }

    function setError(message) {
        if (message) {
            errorText.textContent = message;
            errorMessage.classList.remove('hidden');
            resultsContainer.classList.add('hidden');
            emptyState.classList.remove('hidden');
        } else {
            errorMessage.classList.add('hidden');
        }
    }

    function calculatePercentage(value, total) {
        return total > 0 ? ((value / total) * 100).toFixed(1) : 0;
    }

    function renderResults(data) {
        // Update stats
        analyzedCount.textContent = `Analyzed ${data.total} tweets`;

        positiveCount.textContent = data.positive;
        positivePercent.textContent = `${calculatePercentage(data.positive, data.total)}% of total`;

        negativeCount.textContent = data.negative;
        negativePercent.textContent = `${calculatePercentage(data.negative, data.total)}% of total`;

        neutralCount.textContent = data.neutral;
        neutralPercent.textContent = `${calculatePercentage(data.neutral, data.total)}% of total`;

        // Render tweets
        tweetsList.innerHTML = '';
        if (data.tweets && data.tweets.length > 0) {
            data.tweets.forEach((tweet, index) => {
                tweetsList.appendChild(createTweetCard(tweet));
            });
        } else {
            tweetsList.innerHTML = `
                <div class="card p-8 text-center">
                    <p class="text-gray-500">No tweets found</p>
                </div>
            `;
        }

        resultsContainer.classList.remove('hidden');
        emptyState.classList.add('hidden');
    }

    function createTweetCard(tweet) {
        const div = document.createElement('div');

        // Determine styles based on sentiment
        let borderClass = 'border-left-neutral';
        let badgeClass = 'badge-neutral';
        let avatarBg = 'bg-gray-500';
        let initials = 'NU';
        let username = '@neutral_user';

        if (tweet.sentiment === 'Positive') {
            borderClass = 'border-left-positive';
            badgeClass = 'badge-positive';
            avatarBg = 'bg-green-500';
            initials = 'TH';
            username = '@thought_leader';
        } else if (tweet.sentiment === 'Negative') {
            borderClass = 'border-left-negative';
            badgeClass = 'badge-negative';
            avatarBg = 'bg-red-500';
            initials = 'SU';
            username = '@surprised_user';
        }

        if (tweet.username) {
            username = tweet.username;
            initials = username.substring(0, 2).toUpperCase();
        }

        div.className = `tweet-card ${borderClass}`;
        div.innerHTML = `
            <div class="flex items-start gap-3">
                <div class="avatar ${avatarBg} flex-shrink-0">
                    ${initials}
                </div>
                <div class="flex-1 min-w-0">
                    <div class="flex items-start justify-between mb-2">
                        <div class="flex-1">
                            <div class="flex items-center gap-2">
                                <span class="font-semibold text-gray-900 text-sm">
                                    ${username}
                                </span>
                                <span class="text-xs text-gray-500">
                                    ${tweet.handle || '@anonymous'}
                                </span>
                            </div>
                            <div class="text-xs text-gray-500">
                                ${tweet.timestamp || '1d ago'}
                            </div>
                        </div>
                        <span class="badge ${badgeClass} ml-2 flex-shrink-0">
                            ${tweet.sentiment} ${tweet.polarity ? tweet.polarity.toFixed(2) : ''}
                        </span>
                    </div>
                    <p class="text-sm text-gray-700 leading-relaxed">
                        ${tweet.text}
                    </p>
                </div>
            </div>
        `;
        return div;
    }
});
