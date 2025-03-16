/**
 * Simple component include system
 * Finds elements with data-include attribute and replaces them with the content of the referenced file
 */
document.addEventListener('DOMContentLoaded', function() {
    // Find all elements with the data-include attribute
    const includes = document.querySelectorAll('[data-include]');
    
    // Process each include
    includes.forEach(function(element) {
        const file = element.getAttribute('data-include');
        
        // Fetch the content of the include file
        fetch(file)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to load ${file}: ${response.status} ${response.statusText}`);
                }
                return response.text();
            })
            .then(html => {
                // Replace the element with the content
                element.innerHTML = html;
                
                // Dispatch an event to notify that the include has been loaded
                element.dispatchEvent(new CustomEvent('include-loaded'));
            })
            .catch(error => {
                console.error(`Error including file ${file}:`, error);
                element.innerHTML = `<p style="color: red;">Error loading component: ${error.message}</p>`;
            });
    });
}); 