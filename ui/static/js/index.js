document.addEventListener('DOMContentLoaded', function() {
  // Function to update time slots for a specific game with difficulty filter
  function updateTimeSlots(gameId, containerId, difficulty) {
    fetch('http://127.0.0.1:5000/api/rounds')
      .then(response => response.json())
      .then(data => {
        const container = document.getElementById(containerId);
        
        // Clear any existing content
        container.innerHTML = '';
        
        // Filter rounds by difficulty
        const filteredRounds = data.rounds.filter(round => 
          round.level_difficulty.toLowerCase() === difficulty.toLowerCase()
        );
        
        if (filteredRounds.length === 0) {
          container.innerHTML = `<div class="text-muted">No ${difficulty} time slots available</div>`;
          return;
        }

        // Loop through filtered rounds and create time chips
        filteredRounds.forEach(round => {
          const anchor = document.createElement('a');
          anchor.href = '#';
          
          const timeChip = document.createElement('div');
          timeChip.className = 'time-chip d-flex align-items-center justify-content-center fs-7 fw-normal';
          timeChip.textContent = round.Time_slote;
          
          anchor.appendChild(timeChip);
          container.appendChild(anchor);
        });
      })
      .catch(error => {
        console.error(`Error fetching data for ${gameId}:`, error);
        const container = document.getElementById(containerId);
        container.innerHTML = '<div class="text-danger">Failed to load time slots</div>';
      });
  }

  // Update time slots for all games with their respective difficulties
  updateTimeSlots('ignition-run', 'ignition-run-time-slots', 'easy');
  updateTimeSlots('turbo-clash', 'turbo-clash-time-slots', 'medium');
  updateTimeSlots('apex-storm', 'apex-storm-time-slots', 'hard');
});