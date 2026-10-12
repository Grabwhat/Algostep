document.addEventListener("DOMContentLoaded", (e) => {
    const mega_container = document.querySelector('.mega-container');
    const parent_container = mega_container.querySelectorAll('.parent-problem-container');

    parent_container.forEach((prob_container) => {
        const container = prob_container.querySelector('#problem-container') || document.querySelector('.problem-container');
        const children = container.querySelectorAll('.prob-container');

        const difficultyColors = {
            easy: 'text-green-500',
            medium: 'text-yellow-500',
            hard: 'text-red-600',
            other: 'text-purple-700'
        };

        children.forEach((problem) => {
            const difficulty = problem.dataset.difficulty.toLowerCase().trim();
            const difficulty_text = problem.querySelector('.difficulty');

            if (!difficulty_text) return;

            const difficultyColor = difficultyColors[difficulty] || difficultyColors[other];
            difficulty_text.classList.add(difficultyColor);
        });
    });
});