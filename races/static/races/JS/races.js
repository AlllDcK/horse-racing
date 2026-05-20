function startRace(winnerId) {

    const horses = Array.from(document.querySelectorAll(".horse-runner"));
    if (!horses.length) return;

    const finishLine = 95;

    const winnerIdStr = String(winnerId);

    const startTime = performance.now();

    const state = {};

    const baseTime = 6000;

    horses.forEach(horse => {

        const id = horse.id.replace("horse-", "");
        const isWinner = id === winnerIdStr;

        const finishTime = isWinner
            ? baseTime
            : baseTime + 800 + Math.random() * 2500;

        state[id] = {
            time: finishTime,
            phase: Math.random() * Math.PI * 2
        };

        horse.style.left = "0%";
    });

    function ease(t) {
        return t * (2 - t);
    }

    function animate(now) {

        const elapsed = now - startTime;
        let winnerFinished = false;

        horses.forEach(horse => {

            const id = horse.id.replace("horse-", "");
            const s = state[id];

            let progress = Math.min(elapsed / s.time, 1);
            progress = ease(progress);

            let pos = progress * finishLine;

            const wobble = Math.sin(elapsed / 200 + s.phase) * 0.4;
            pos += wobble;

            pos = Math.max(0, Math.min(finishLine, pos));

            horse.style.left = pos + "%";

            if (id === winnerIdStr && progress >= 1) {
                winnerFinished = true;
            }
        });

        if (!winnerFinished) {
            requestAnimationFrame(animate);
        }
    }

    requestAnimationFrame(animate);
}

document.addEventListener("DOMContentLoaded", function () {

    const raceTrack = document.getElementById("race-track");
    if (!raceTrack) return;

    const winnerId = raceTrack.dataset.winner;

    if (winnerId && winnerId !== "None" && winnerId !== "") {
        startRace(winnerId);
    }
});