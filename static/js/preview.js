// Add loading state for images
// (This is optional, but included for parity with the original inline script)
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.certificate-image');
    let loadedCount = 0;
    images.forEach(img => {
        if (img.complete) {
            loadedCount++;
        } else {
            img.addEventListener('load', () => {
                loadedCount++;
            });
            img.addEventListener('error', () => {
                loadedCount++;
            });
        }
    });
}); 