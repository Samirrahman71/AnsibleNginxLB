// Simple hit counter visualization for the load balancer demo
document.addEventListener('DOMContentLoaded', function() {
    // Get server name from the page
    const serverName = document.querySelector('.server-badge').classList[1];
    
    // Initialize counters in localStorage if they don't exist
    if (!localStorage.getItem('app1_hits')) {
        localStorage.setItem('app1_hits', '0');
        localStorage.setItem('app2_hits', '0');
        localStorage.setItem('app3_hits', '0');
    }
    
    // Increment the count for the current server
    const currentHits = parseInt(localStorage.getItem(serverName + '_hits')) || 0;
    localStorage.setItem(serverName + '_hits', (currentHits + 1).toString());
    
    // Get all counts
    const app1Hits = parseInt(localStorage.getItem('app1_hits')) || 0;
    const app2Hits = parseInt(localStorage.getItem('app2_hits')) || 0;
    const app3Hits = parseInt(localStorage.getItem('app3_hits')) || 0;
    const totalHits = app1Hits + app2Hits + app3Hits;
    
    // Create the visualization
    const statsContainer = document.getElementById('load-distribution');
    if (statsContainer) {
        // Calculate percentages
        const app1Percent = totalHits > 0 ? Math.round((app1Hits / totalHits) * 100) : 0;
        const app2Percent = totalHits > 0 ? Math.round((app2Hits / totalHits) * 100) : 0;
        const app3Percent = totalHits > 0 ? Math.round((app3Hits / totalHits) * 100) : 0;
        
        statsContainer.innerHTML = `
            <h3>Your Load Distribution</h3>
            <p>Based on your browser visits</p>
            <div class="distribution-bars">
                <div class="distribution-bar">
                    <div class="bar-label">Server 1</div>
                    <div class="bar-container">
                        <div class="bar app1" style="width: ${app1Percent}%">${app1Hits} hits</div>
                    </div>
                    <div class="bar-percent">${app1Percent}%</div>
                </div>
                <div class="distribution-bar">
                    <div class="bar-label">Server 2</div>
                    <div class="bar-container">
                        <div class="bar app2" style="width: ${app2Percent}%">${app2Hits} hits</div>
                    </div>
                    <div class="bar-percent">${app2Percent}%</div>
                </div>
                <div class="distribution-bar">
                    <div class="bar-label">Server 3</div>
                    <div class="bar-container">
                        <div class="bar app3" style="width: ${app3Percent}%">${app3Hits} hits</div>
                    </div>
                    <div class="bar-percent">${app3Percent}%</div>
                </div>
            </div>
            <div class="stats-footer">
                <small>Total page loads: ${totalHits}</small>
                <button id="reset-stats" class="reset-button">Reset Statistics</button>
            </div>
        `;
        
        // Add reset button functionality
        document.getElementById('reset-stats').addEventListener('click', function() {
            localStorage.setItem('app1_hits', '0');
            localStorage.setItem('app2_hits', '0');
            localStorage.setItem('app3_hits', '0');
            location.reload();
        });
    }
});
