// Live Background Particle System
const canvas = document.getElementById("live-bg");
const ctx = canvas ? canvas.getContext("2d") : null;
const video = document.getElementById("video-bg");

// Handle video error gracefully
if (video) {
  video.addEventListener("error", () => {
    video.style.display = "none";
    console.log("Video not found - using particle background only");
  });
}

if (canvas && ctx) {
  let particles = [];
  let mouseX = 0;
  let mouseY = 0;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener("resize", resize);

  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.vx = (Math.random() - 0.5) * 0.5;
      this.vy = (Math.random() - 0.5) * 0.5;
      this.size = Math.random() * 2 + 0.5;
      this.color = Math.random() > 0.5 ? "rgba(0, 240, 255, " : "rgba(139, 92, 246, ";
      this.opacity = Math.random() * 0.5 + 0.3;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      // Mouse interaction
      const dx = mouseX - this.x;
      const dy = mouseY - this.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 150) {
        const force = (150 - dist) / 150;
        this.x -= dx * force * 0.02;
        this.y -= dy * force * 0.02;
      }

      // Wrap edges
      if (this.x < 0) this.x = canvas.width;
      if (this.x > canvas.width) this.x = 0;
      if (this.y < 0) this.y = canvas.height;
      if (this.y > canvas.height) this.y = 0;
    }

    draw() {
      ctx.fillStyle = this.color + this.opacity + ")";
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();

      // Glow effect
      ctx.shadowBlur = 15;
      ctx.shadowColor = this.color + "0.8)";
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  // Create particles
  for (let i = 0; i < 150; i++) {
    particles.push(new Particle());
  }

  // Track mouse
  window.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // Animation loop
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw connections
    particles.forEach((p, i) => {
      particles.slice(i + 1).forEach((p2) => {
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.strokeStyle = `rgba(0, 240, 255, ${(1 - dist / 120) * 0.15})`;
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      });
    });

    // Update and draw particles
    particles.forEach((p) => {
      p.update();
      p.draw();
    });

    requestAnimationFrame(animate);
  }
  animate();
}

// Robot Eye Tracking
const robot = document.getElementById("robot-head");
const face = robot ? robot.querySelector(".robot-face") : null;
const core = robot ? robot.querySelector(".robot-core") : null;
const pupils = robot ? robot.querySelectorAll(".robot-eye .pupil") : [];

if (robot && face) {
  const damp = 12;
  window.addEventListener("mousemove", (e) => {
    const rect = robot.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = (e.clientX - cx) / rect.width;
    const dy = (e.clientY - cy) / rect.height;
    const tiltX = Math.max(Math.min(dy * damp, 10), -10);
    const tiltY = Math.max(Math.min(-dx * damp, 10), -10);
    face.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg) translate(${dx * 10}px, ${dy * 10}px)`;
    if (core) {
      core.style.transform = `rotateX(${tiltX / 1.8}deg) rotateY(${tiltY / 1.8}deg)`;
    }
    const pupilX = Math.max(Math.min(dx * 24, 12), -12);
    const pupilY = Math.max(Math.min(dy * 24, 12), -12);
    pupils.forEach((p) => {
      p.style.transform = `translate(${pupilX}px, ${pupilY}px)`;
    });
  });
}

const copyBtn = document.getElementById("copy-link");
if (copyBtn) {
  copyBtn.addEventListener("click", async () => {
    const link = copyBtn.dataset.link;
    try {
      await navigator.clipboard.writeText(link);
      copyBtn.textContent = "Link copied";
      setTimeout(() => (copyBtn.textContent = "Copy link"), 1500);
    } catch (err) {
      copyBtn.textContent = "Copy failed";
      console.error(err);
    }
  });
}
