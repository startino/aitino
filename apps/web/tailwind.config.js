import { fontFamily } from 'tailwindcss/defaultTheme';
import typographyConfig from './theme/typography.cjs';
import colorConfig from './theme/color.cjs';
import { animationsConfig, keyframesConfig } from './theme/animation.cjs';

/** @type {import('tailwindcss').Config} */

const alpha = '<alpha-value>';

const config = {
	darkMode: ['class'],
	content: ['./src/**/*.{html,js,svelte,ts}', './theme/*.{html,js,svelte,ts,ttf,cjs}'],
	safelist: ['dark'],
	daisyui: {
		themes: [
			{
				futino: {
					primary: '#45dfa4',
					secondary: '#3cddc7',
					accent: '#ffafd3',
					neutral: '#333333',
					'base-100': '#171919',
					info: '#ffafd3',
					success: '#45dfa4',
					warning: '#ffb4ab',
					error: '#690005'
				}
			}
		]
	},
	theme: {
		container: {
			center: true,
			padding: '2rem',
			screens: {
				'2xl': '1400px'
			}
		},
		extend: {
			dropShadow: {
				'pricing-art': [
					'0 0 3px rgb(var(--md-sys-color-tertiary-container) / 0.7)',
					'0 0 3px rgb(var(--md-sys-color-tertiary-container) / 0.7)'
				]
			},
			animation: animationsConfig,
			keyframes: keyframesConfig,
			colors: colorConfig,
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)'
			},
			fontFamily: {
				sans: [...fontFamily.sans]
			},
			typography: ({ colors }) => ({
				...typographyConfig(colors, alpha),
				...{
					DEFAULT: {}
				}
			})
		}
	},
	plugins: [
		require('@tailwindcss/forms'),
		require('@tailwindcss/typography'),
		require('@tailwindcss/aspect-ratio'),
		require('daisyui')
	]
};

export default config;
