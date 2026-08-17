var initInlineCopy = function() {
    const copyTags = document.querySelectorAll('copy:not([data-initialized])');
    
    copyTags.forEach(el => {
        el.style.cursor = 'pointer';
        
        el.addEventListener('click', function() {
            const textToCopy = el.innerText;
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Add the 'copied' class for visual feedback
                el.classList.add('copied');
                
                // Remove it after 1.5 seconds
                setTimeout(() => {
                    el.classList.remove('copied');
                }, 1500);
            });
        });
        
        el.setAttribute('data-initialized', 'true');
    });
};

// Initial load
document.addEventListener("DOMContentLoaded", initInlineCopy);

// MkDocs Instant Loading Fix
if (typeof app !== "undefined") {
    app.document$.subscribe(function() {
        initInlineCopy();
    });
}