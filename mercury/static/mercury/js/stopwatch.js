window.onload = stopwatchLoad;
window.onbeforeunload = function() {
    if (window.stopwatch.running == true) {
        return "The stopwatch is running. Are you sure you want to leave?";
    }
};

function stopwatchLoad() {
    window.stopwatch = new Stopwatch(
        document.querySelector('.stopwatch'),
        document.querySelector('.results'));
}

class Stopwatch {
    constructor(display, results) {
        this.running = false;
        this.display = display;
        this.results = results;
        this.clearTime();
        this.print(this.times);
    }
    
    clearTime() {
        this.times = [ 0, 0, 0 ];
    }
    
    start() {
        if (!this.time) this.time = performance.now();
        if (!this.running) {
            this.running = true;
            requestAnimationFrame(this.step.bind(this));
        }
    }
    
    stop() {
        this.running = false;
        this.time = null;
    }

    lap() {
        let times = this.times;
        let li = document.createElement('li');
        li.innerText = this.format(times);
        this.results.appendChild(li);
    }

    reset() {
        if (!this.time) this.time = performance.now();
        if (this.running) {
            this.running = false;
            requestAnimationFrame(this.step.bind(this));
        }
        this.clearLaps();
        this.clearTime();
        this.print();
    }
    
    clearLaps() {
        clearChildren(this.results);
    }
    
    step(timestamp) {
        if (!this.running) return;
        this.calculate(timestamp);
        this.time = timestamp;
        this.print();
        requestAnimationFrame(this.step.bind(this));
    }
    
    calculate(timestamp) {
        var diff = timestamp - this.time;
        // Hundredths of a second are 100 ms
        this.times[2] += diff / 10;
        // Seconds are 100 hundredths of a second
        if (this.times[2] >= 100) {
            this.times[1] += 1;
            this.times[2] -= 100;
        }
        // Minutes are 60 seconds
        if (this.times[1] >= 60) {
            this.times[0] += 1;
            this.times[1] -= 60;
        }
    }
    
    print() {
        this.display.innerText = this.format(this.times);
    }
    
    format(times) {
        return `\
${padWithZero(times[0], 2)}:\
${padWithZero(times[1], 2)}:\
${padWithZero(Math.floor(times[2]), 2)}`;
    }
}

function padWithZero(value, count) {
    var result = value.toString();
    for (; result.length < count; --count)
        result = '0' + result;
    return result;
}

function clearChildren(node) {
    while (node.lastChild)
        node.removeChild(node.lastChild);
}