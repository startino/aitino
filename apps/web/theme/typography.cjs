import colorConfig from './color.cjs';

const typography = (colors, alpha) => {
	return {
		main: {
			css: {
				'--tw-prose-body': colors.neutral[300],
				'--tw-prose-headings': colors.white,
				'--tw-prose-lead': colors.neutral[400],
				'--tw-prose-links': colorConfig.tertiary.DEFAULT.replace(alpha, 1),
				'--tw-prose-bold': colors.white,
				'--tw-prose-counters': colors.neutral[400],
				'--tw-prose-bullets': colorConfig.nsecondary.DEFAULT.replace(alpha, 0.4),
				'--tw-prose-hr': colors.neutral[700],
				'--tw-prose-quotes': colors.neutral[100],
				'--tw-prose-quote-borders': colorConfig.secondary.DEFAULT.replace(alpha, 0.3),
				'--tw-prose-captions': colors.neutral[400],
				'--tw-prose-code': colors.white,
				'--tw-prose-pre-code': colors.neutral[300],
				'--tw-prose-pre-bg': 'rgb(0 0 0 / 50%)',
				'--tw-prose-th-borders': colors.neutral[600],
				'--tw-prose-td-borders': colors.neutral[700]
			}
		},
		blog: {
			css: {
				'--tw-prose-body': colorConfig.foreground, // UNSTABLE METHOD! find a better way to do this using <alpha-value>
				'--tw-prose-headings': colorConfig.primary.DEFAULT,
				'--tw-prose-lead': colors.neutral[400],
				'--tw-prose-links': colorConfig.accent.DEFAULT,
				'--tw-prose-bold': colors.white,
				'--tw-prose-counters': colors.neutral[400],
				'--tw-prose-bullets': colorConfig.secondary.DEFAULT.replace(alpha, 0.4),
				'--tw-prose-hr': colors.neutral[700],
				'--tw-prose-quotes': colors.neutral[100],
				'--tw-prose-quote-borders': colorConfig.secondary.DEFAULT.replace(alpha, 0.3),
				'--tw-prose-captions': colors.neutral[400],
				'--tw-prose-code': colors.white,
				'--tw-prose-pre-code': colors.neutral[300],
				'--tw-prose-pre-bg': 'rgb(0 0 0 / 50%)',
				'--tw-prose-th-borders': colors.neutral[600],
				'--tw-prose-td-borders': colors.neutral[700]
			}
		}
	};
};

module.exports = typography;
