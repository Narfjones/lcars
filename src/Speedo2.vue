<template>
<div class="wrapper">

  <!-- left border/key -->
  <svg class="range-key" xmlns="http://www.w3.org/2000/svg" width="159" height="600" viewBox="0 0 159 600">
    <defs>
      <linearGradient id="gradient" x1="50%" x2="50%" y1="0%" y2="100%">
        <stop offset="0%" stop-color="#C50000" />
        <stop offset="50%" stop-color="#FFB300" />
        <stop offset="100%" stop-color="#198D00" />
      </linearGradient>
    </defs>
    <path fill="url(#gradient)" fill-rule="evenodd" d="M159 0v2h-13.1a49 49 0 00-48.5 42l-.1.7-65 498A49 49 0 0080.7 598H159v2H62a62 62 0 01-62-62V62A62 62 0 0162 0h97z" />
  </svg>

  <!--  range input label  -->
  <label class="range-label" for="grav">Gravity Preference</label>
  <input name="grav" id="grav" class="gravity-range" type="range" id="vol" min="0" max="100" value="50">

  <!--  the dial  -->
  <div class="dial-wrapper">
    <svg class="dial-ui" xmlns="http://www.w3.org/2000/svg" width="466" height="466" viewBox="0 0 466 466">
      <defs>
        <filter id="shadow" width="126.9%" height="126.9%" x="-13.4%" y="-13.4%" filterUnits="objectBoundingBox">
          <feMorphology in="SourceAlpha" operator="dilate" radius="6.5" result="shadowSpreadOuter1" />
          <feOffset in="shadowSpreadOuter1" result="shadowOffsetOuter1" />
          <feGaussianBlur in="shadowOffsetOuter1" result="shadowBlurOuter1" stdDeviation="10" />
          <feComposite in="shadowBlurOuter1" in2="SourceAlpha" operator="out" result="shadowBlurOuter1" />
          <feColorMatrix in="shadowBlurOuter1" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0" />
        </filter>
      </defs>
      <g fill="none" fill-rule="evenodd" transform="translate(1 1)">
        <circle cx="232" cy="232" r="232" opacity=".4" stroke="var(--ui-blue)" />
        <path class="grav-o-meter" stroke="currentColor" stroke-width="10" d="M377.5 375a204 204 0 10-290.3.7" opacity=".8" />
        <path stroke="#99DFF4" stroke-dasharray="1 14.7" stroke-width="54" d="M377.5 375a204 204 0 10-290.3.7" opacity=".4" />
        <g fill="#0E0E0E" stroke-width="3" transform="translate(59 59)">
          <circle filter="url(#shadow)" cx="173" cy="173" r="175" fill="#000" />
        </g>
        <g class="dial" fill="#0E0E0E" stroke-width="3" transform="translate(59 59)">
          <circle cx="173" cy="173" r="175" stroke="var(--ui-blue)" />
          <circle cx="70" cy="270" r="8" stroke="var(--ui-blue)" />
        </g>
      </g>
    </svg>

    <!--  dial numbers    -->
    <p class="dial-numbers">
      <span class="number thicc">9.8</span>
      <span class="units">M/S/S</span>
    </p>
  </div>
</template>


<script>
console.clear();
// register the plugins to use.
gsap.registerPlugin(Draggable, InertiaPlugin, DrawSVGPlugin);

// target range-slider
const gravity = document.querySelector(".gravity-range");

// setup dial transformOrigin
gsap.set(".dial", { transformOrigin: "50% 50%", rotation: "135deg" });

// ui color
const colorSetter = gsap
  .timeline({ paused: true, defaults: { ease: "none" } })
  .fromTo("body", { "--current-ui": "#198D00" }, { "--current-ui": "#FFB300" })
  .to("body", { "--current-ui": "#C50000" });

// font-weight (variable font)
const gravityWeight = gsap.fromTo(
  "body",
  {
    "--weight": 400
  },
  { "--weight": 900, ease: "none", paused: true }
);

// gravity number
const gNumber = { num: 09.8 };
const gravityNumber = gsap.fromTo(
  gNumber,
  { num: 0.1 },
  { num: 19.6, ease: "none", paused: true }
);

// bounce height
let yBounce = -150;
const bounceOMeter = gsap
  .timeline({ defaults: { duration: 0.5 }, repeatRefresh: true, repeat: -1 })
  .to(".ball", {
    y: () => {
      return yBounce;
    },
    ease: "power2.out"
  })
  .to(".ball", { y: 0, ease: "power2.in" });

// bounceOMeter timescale
const bounceSpeed = gsap.fromTo(
  bounceOMeter,
  { timeScale: 0.1 },
  { paused: true, timeScale: 8, duration: 1, ease: "circ.in" }
);

// gravity meter guage
const gravOMeter = gsap.from(".grav-o-meter", {
  paused: true,
  ease: "none",
  drawSVG: "100% 100%"
});

//  handle range/draggable inputs
const numberEl = document.querySelector(".number");
let isDragging = false;

const handleRangeInput = (isDragging) => {
  // chrome gradient
  gsap.set("body", { "--range-gradient": `${gravity.value}%` });

  // tween progress of the progress ring
  gsap.to([gravOMeter, colorSetter, gravityWeight], {
    progress: (gravity.value - 0) / 100
  });

  // ui rings
  gsap.to(".ring", {
    y: gsap.utils.mapRange(100, 0, 0, 567, gravity.value),
    stagger: { amount: 0.333 }
  });

  // other tweens progress
  gsap.set([gravityNumber, bounceSpeed], {
    progress: gravity.value / 100
  });

  // set bounce height for repreat refresh
  yBounce = gsap.utils.mapRange(0, -100, 0, -450, gravity.value - 100);

  if (gNumber.num < 10) {
    numberEl.innerHTML = `0${gNumber.num.toFixed(1)}`;
  } else {
    numberEl.innerHTML = `${gNumber.num.toFixed(1)}`;
  }

  // is dragging?
  if (isDragging !== true) {
    gsap.to(".dial", {
      duration: 0.5,
      rotate: `${(gravity.value / 100) * 270}deg`
    });
  }
};

handleRangeInput();

// setup input function
gravity.oninput = handleRangeInput;

// create draggable
Draggable.create(".dial", {
  type: "rotation",
  bounds: { maxRotation: 270, minRotation: 0 },
  inertia: true,
  snap: (value) => Math.round(value / (270 / 100)) * (270 / 100),
  onDrag() {
    gravity.value = (this.rotation / this.maxRotation) * 100;
    handleRangeInput(true);
  },
  onThrowUpdate() {
    gravity.value = (this.rotation / this.maxRotation) * 100;
    handleRangeInput(true);
  }
});

</script>


<style>
:root {
  --ui-blue: #99dff4;
  --current-ui: #ffb300;
  --background: #0e0e0e;
  --range-gradient: 50%;
  --weight: 400;
}

body {
  font-family: "Orbitron", sans-serif;
  font-weight: 400 900;
  background: var(--background);
  color: var(--current-ui);
  display: grid;
  place-content: center;
  height: 100vh;
}

.wrapper {
  position: relative;
  width: 1080px;
  height: 600px;
  display: grid;
  place-content: center;
}

.range-key {
  position: absolute;
  left: 0;
  top: 0;
}

.right-border {
  position: absolute;
  right: 0;
  top: 0;
}

.dial-wrapper {
  position: relative;
  width: 466px;
  height: 466px;
  z-index: 3;
  display: grid;
  place-content: center;
}

.dial-ui {
  position: absolute;
  top: 0;
  left: 0;
}

.dial-numbers {
  pointer-events: none;
  position: relative;
  text-align: center;
  line-height: 1;
}

.number {
  font-size: 100px;
}

.units {
  color: var(--ui-blue);
  font-weight: 400;
  display: block;
  font-size: 25px;
  letter-spacing: 4px;
}

.bounce-wrapper {
  height: 400px;
  position: absolute;
  right: 100px;
  top: 100px;
  border: 1px solid currentColor;
  border-bottom: 8px solid;
  width: 120px;
  overflow: hidden;
}

.ball {
  position: absolute;
  bottom: -2px;
  left: 30px;
  border-radius: 100%;
  height: 60px;
  width: 60px;
  border: 3px solid var(--ui-blue);
  z-index: 10;
  will-change: transform;
}

.bounce-simulation {
  display: block;
  text-transform: uppercase;
  position: absolute;
  top: 60px;
  letter-spacing: 1px;
  right: 100px;
  width: 123px;
}

.thicc {
  font-weight: var(--weight);
}

.range-label {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  margin-top: -8px;
  font-size: 16px;
  letter-spacing: 5px;
  text-transform: uppercase;
  text-align: center;
  color: var(--ui-blue);
}

.gravity-range {
  position: absolute;
  color: currentColor;
  top: 0;
  left: 170px;
  width: 600px;
  height: 90px;
  cursor: pointer;
  background-color: transparent;
  transform-origin: top left;
  transform: rotate(-90deg) translateX(-100%);
  appearance: none;

  &,
  &::-webkit-slider-runnable-track,
  &::-webkit-slider-thumb {
    -webkit-appearance: none;
  }

  &::-webkit-slider-runnable-track {
    height: 2px;
    background: linear-gradient(
      to right,
      currentColor var(--range-gradient),
      #364c52 var(--range-gradient),
      #364c52
    );
  }

  &::-moz-range-track {
    height: 2px;
    background: #364c52;
  }

  &::-moz-range-progress {
    background-color: currentColor;
  }

  &::-webkit-slider-thumb {
    width: 30px;
    height: 30px;
    border-radius: 100%;
    background: var(--background);
    border: 1px solid var(--ui-blue);
    margin-top: -14px;
  }
  &::-moz-range-thumb {
    width: 30px;
    height: 30px;
    border-radius: 100%;
    background: var(--background);
    border: 1px solid var(--ui-blue);
  }
}

.ring {
  position: absolute;
  top: 17px;
  left: 215px;
  transform: translate(-50%, -50%);
  border: 1px solid var(--ui-blue);
  border-radius: 100%;
  pointer-events: none;

  &--0 {
    height: 50px;
    width: 50px;
    opacity: 0.7;
  }
  &--1 {
    height: 60px;
    width: 60px;
    opacity: 0.6;
  }
  &--2 {
    height: 70px;
    width: 70px;
    opacity: 0.5;
  } 
  &--3 {
    height: 80px;
    width: 80px;
    opacity: 0.4;
  }
  &--4 {
    height: 90px;
    width: 90px;
    opacity: 0.3;
  }
}

</style>