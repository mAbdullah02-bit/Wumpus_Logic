document.getElementById('runBtn').addEventListener('click', runSimulation);

async function runSimulation() {
    const rows = document.getElementById('rows').value;
    const cols = document.getElementById('cols').value;
    const pits = document.getElementById('pits').value;

    const response = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rows, cols, num_pits: pits })
    });

    const data = await response.json();
    animateSteps(data);
}

function animateSteps(data) {
    const gridEl = document.getElementById('wumpusGrid');
    const logEl = document.getElementById('logContent');
    const infStepsEl = document.getElementById('infSteps');
    
    gridEl.style.gridTemplateColumns = `repeat(${data.cols}, 60px)`;
    logEl.innerHTML = ''; // Clear logs

    let i = 0;
    const interval = setInterval(() => {
        if (i >= data.steps.length) {
            clearInterval(interval);
            document.getElementById('agentStatus').innerText = data.survived ? "Success" : "Terminated";
            return;
        }

        const step = data.steps[i];
        renderGrid(data.rows, data.cols, step);
        
        // Update Metrics
        infStepsEl.innerText = step.inference_steps_total;
        document.getElementById('goldStatus').innerText = step.gold ? "YES!" : "No";
        document.getElementById('agentStatus').innerText = "Moving...";

        // Update Logs (last 5 entries)
        logEl.innerHTML = step.log.slice(-10).join('<br>') + '<hr>' + logEl.innerHTML;

        i++;
    }, 600); // 600ms per move for visualization
}

function renderGrid(rows, cols, step) {
    const gridEl = document.getElementById('wumpusGrid');
    gridEl.innerHTML = '';

    for (let r = 1; r <= rows; r++) {
        for (let c = 1; c <= cols; c++) {
            const cell = document.createElement('div');
            const status = step.grid[`${r},${c}`] || 'unknown';
            cell.className = `cell ${status}`;
            
            if (step.pos[0] === r && step.pos[1] === c) {
                cell.classList.add('agent');
                cell.innerText = "AGENT";
            } else {
                cell.innerText = `${r},${c}`;
            }
            gridEl.appendChild(cell);
        }
    }
}
