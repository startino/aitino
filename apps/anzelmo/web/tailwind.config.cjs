import { join } from "path";
import fColors from "../../legacy/futino-colors.cjs";
import fAnimations from "../../legacy/futino-animations.cjs";
import fKeyframes from "../../legacy/futino-keyframes.cjs";
import fPadding from "../../legacy/futino-padding.cjs";
import fTypography from "../../legacy/futino-typography.cjs";

const alpha = "<alpha-value>";

const config = {
  content: [
    "./src/**/*.{html,js,svelte,ts}",
    join("../**/*.{html,js,svelte,ts}"),
  ],

  DEFAULTMode: "class",

  theme: {
    extend: {
      backgroundImage: {
        seagul: "url('temp_photography/seagul.jpg')",
        flower: "url('temp_photography/flower.jpg')",
        bird: "url('temp_photography/bird.jpg')",
        lizard: "url('temp_photography/lizard.jpg')",
        ocean: "url('temp_photography/ocean.jpg')",
        photo1: "url('temp_photography/photo1.jpg')",
        photo2: "url('temp_photography/photo2.jpg')",
        photo3: "url('temp_photography/photo3.jpg')",
        photo4: "url('temp_photography/photo4.jpg')",
      },
      fontFamily: {
        bilbo: ["Bilbo Swash Caps"],
        ubuntu: ["Ubuntu"],
      },

      animation: {
        wiggle: "wiggle 1s ease-in-out infinite",
        slideDown: "slideDown 5s ease-in-out 1",
        scroll: "scroll 5s ease-in-out",
      },

      keyframes: {
        wiggle: {
          "0%, 100%": { transform: "rotate(-3deg)" },
          "50%": { transform: "rotate(3deg)" },
        },
        slideDown: {
          "0%, 100%": { transform: "translate(0%,-200%)", opacity: 0 },
          "1%, 99%": { opacity: 1 },
          "20%, 70%": { transform: "translate(0%, 0%)" },
        },
        scroll: {
          "0%": { transform: "translateY(0%)" },
          "100%": { transform: "translateY(100%)" },
        },
      },
      colors: fColors,

      plugins: [],
    },
  },
};

module.exports = config;
