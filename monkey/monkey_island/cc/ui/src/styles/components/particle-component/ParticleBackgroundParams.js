export const particleParams = {
  fps_limit: 60,
  particles: {
    color: { value: "#646464" },
    links: {
      color: "#555555",
      distance: 150,
      enable: true,
      opacity: 0.4,
      width: 1,
    },
    move: {
      bounce: false,
      direction: "none",
      enable: true,
      outMode: "out",
      random: false,
      speed: 2,
      straight: false,
    },
    number: { density: { enable: true, area: 800 }, value: 50 },
    shape: { type: "circle" },
    size: { value: 3 },
  },
  detectRetina: true,
};
