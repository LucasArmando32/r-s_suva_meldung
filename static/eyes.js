/* Cursor-Tracking für die Augen des Asbestsanierer-Charakters.
   Die Pupillen bewegen sich in Richtung des Mauszeigers. */
(function () {
    const MAX_OFFSET = 4; // maximale Pupillenverschiebung in SVG-Einheiten

    function updateEyes(mouseX, mouseY) {
        document.querySelectorAll(".worker-eye-group").forEach(function (group) {
            const svg = group.closest("svg");
            if (!svg) return;

            const pupil = group.querySelector(".worker-pupil");
            const shine = group.querySelector(".worker-shine");
            if (!pupil) return;

            // SVG-Koordinaten -> Bildschirmkoordinaten
            const rect = svg.getBoundingClientRect();
            const vb = svg.viewBox.baseVal;
            const scaleX = rect.width / vb.width;
            const scaleY = rect.height / vb.height;

            const eyeCxSvg = parseFloat(group.dataset.eyeCenterX);
            const eyeCySvg = parseFloat(group.dataset.eyeCenterY);
            const eyeScreenX = rect.left + eyeCxSvg * scaleX;
            const eyeScreenY = rect.top + eyeCySvg * scaleY;

            const dx = mouseX - eyeScreenX;
            const dy = mouseY - eyeScreenY;
            const dist = Math.max(Math.hypot(dx, dy), 1);

            const tx = (dx / dist) * MAX_OFFSET;
            const ty = (dy / dist) * MAX_OFFSET;

            pupil.setAttribute("transform", "translate(" + tx + " " + ty + ")");
            if (shine) {
                shine.setAttribute("transform", "translate(" + tx + " " + ty + ")");
            }
        });
    }

    // SVG als Inline-Element laden, damit wir die Augen manipulieren können
    document.querySelectorAll("[data-inline-svg]").forEach(async function (host) {
        try {
            const url = host.dataset.inlineSvg;
            const resp = await fetch(url);
            const svgText = await resp.text();
            host.innerHTML = svgText;
        } catch (err) {
            console.warn("SVG konnte nicht geladen werden:", err);
        }
    });

    document.addEventListener("mousemove", function (e) {
        updateEyes(e.clientX, e.clientY);
    });

    document.addEventListener("touchmove", function (e) {
        if (e.touches && e.touches.length) {
            updateEyes(e.touches[0].clientX, e.touches[0].clientY);
        }
    }, { passive: true });
})();
