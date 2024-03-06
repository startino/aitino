
import root from '../root.svelte';
import { set_building, set_prerendering } from '__sveltekit/environment';
import { set_assets } from '__sveltekit/paths';
import { set_manifest, set_read_implementation } from '__sveltekit/server';
import { set_private_env, set_public_env, set_safe_public_env } from '../../../node_modules/.pnpm/@sveltejs+kit@2.5.2_@sveltejs+vite-plugin-svelte@3.0.2_svelte@4.2.12_vite@5.1.4/node_modules/@sveltejs/kit/src/runtime/shared-server.js';

export const options = {
	app_dir: "_app",
	app_template_contains_nonce: false,
	csp: {"mode":"auto","directives":{"upgrade-insecure-requests":false,"block-all-mixed-content":false},"reportOnly":{"upgrade-insecure-requests":false,"block-all-mixed-content":false}},
	csrf_check_origin: true,
	embedded: false,
	env_public_prefix: 'PUBLIC_',
	env_private_prefix: '',
	hooks: null, // added lazily, via `get_hooks`
	preload_strategy: "modulepreload",
	root,
	service_worker: false,
	templates: {
		app: ({ head, body, assets, nonce, env }) => "<!doctype html>\r\n<html lang=\"en\" class=\"dark\">\r\n\t<head>\r\n\t\t<meta charset=\"utf-8\" />\r\n\t\t<title>Aitino</title>\r\n\t\t<meta\r\n\t\t\tname=\"description\"\r\n\t\t\tcontent=\"Create a Crew of AI Agents with Aitino - The world's leading web platform in pairing modern AI Agents with communication abililities. By taking the form of node-editors, Aitino harnesses the ability to create teams of AI agents that collaborate to solve complex tasks in real-time.\"\r\n\t\t/>\r\n\t\t<link rel=\"icon\" href=\"" + assets + "/favicon.png\" sizes=\"any\" />\r\n\t\t<link rel=\"icon\" href=\"" + assets + "/logo/logo.svg\" type=\"image/svg+xml\" />\r\n\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\r\n\t\t<meta name=\"google-site-verification\" content=\"dnoWzKQeMa1SegspMoenOTOwuRb_kM2juP8-oRRT7zE\" />\r\n\t\t" + head + "\r\n\r\n\t\t<!-- Google Tag Manager -->\r\n\t\t<script>\r\n\t\t\t(function (w, d, s, l, i) {\r\n\t\t\t\tw[l] = w[l] || [];\r\n\t\t\t\tw[l].push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });\r\n\t\t\t\tvar f = d.getElementsByTagName(s)[0],\r\n\t\t\t\t\tj = d.createElement(s),\r\n\t\t\t\t\tdl = l != 'dataLayer' ? '&l=' + l : '';\r\n\t\t\t\tj.async = true;\r\n\t\t\t\tj.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;\r\n\t\t\t\tf.parentNode.insertBefore(j, f);\r\n\t\t\t})(window, document, 'script', 'dataLayer', 'GTM-NL88SKDC');\r\n\t\t</script>\r\n\t\t<!-- End Google Tag Manager -->\r\n\t</head>\r\n\t<body data-sveltekit-preload-data=\"hover\" class=\"\">\r\n\t\t<!-- Google Tag Manager (noscript) -->\r\n\t\t<noscript\r\n\t\t\t><iframe\r\n\t\t\t\ttitle=\"Google Tag Manager\"\r\n\t\t\t\tsrc=\"https://www.googletagmanager.com/ns.html?id=GTM-NL88SKDC\"\r\n\t\t\t\theight=\"0\"\r\n\t\t\t\twidth=\"0\"\r\n\t\t\t\tstyle=\"display: none; visibility: hidden\"\r\n\t\t\t></iframe\r\n\t\t></noscript>\r\n\t\t<!-- End Google Tag Manager (noscript) -->\r\n\r\n\t\t<div style=\"display: contents\" class=\"h-full overflow-hidden\">" + body + "</div>\r\n\t</body>\r\n</html>\r\n",
		error: ({ status, message }) => "<!doctype html>\n<html lang=\"en\">\n\t<head>\n\t\t<meta charset=\"utf-8\" />\n\t\t<title>" + message + "</title>\n\n\t\t<style>\n\t\t\tbody {\n\t\t\t\t--bg: white;\n\t\t\t\t--fg: #222;\n\t\t\t\t--divider: #ccc;\n\t\t\t\tbackground: var(--bg);\n\t\t\t\tcolor: var(--fg);\n\t\t\t\tfont-family:\n\t\t\t\t\tsystem-ui,\n\t\t\t\t\t-apple-system,\n\t\t\t\t\tBlinkMacSystemFont,\n\t\t\t\t\t'Segoe UI',\n\t\t\t\t\tRoboto,\n\t\t\t\t\tOxygen,\n\t\t\t\t\tUbuntu,\n\t\t\t\t\tCantarell,\n\t\t\t\t\t'Open Sans',\n\t\t\t\t\t'Helvetica Neue',\n\t\t\t\t\tsans-serif;\n\t\t\t\tdisplay: flex;\n\t\t\t\talign-items: center;\n\t\t\t\tjustify-content: center;\n\t\t\t\theight: 100vh;\n\t\t\t\tmargin: 0;\n\t\t\t}\n\n\t\t\t.error {\n\t\t\t\tdisplay: flex;\n\t\t\t\talign-items: center;\n\t\t\t\tmax-width: 32rem;\n\t\t\t\tmargin: 0 1rem;\n\t\t\t}\n\n\t\t\t.status {\n\t\t\t\tfont-weight: 200;\n\t\t\t\tfont-size: 3rem;\n\t\t\t\tline-height: 1;\n\t\t\t\tposition: relative;\n\t\t\t\ttop: -0.05rem;\n\t\t\t}\n\n\t\t\t.message {\n\t\t\t\tborder-left: 1px solid var(--divider);\n\t\t\t\tpadding: 0 0 0 1rem;\n\t\t\t\tmargin: 0 0 0 1rem;\n\t\t\t\tmin-height: 2.5rem;\n\t\t\t\tdisplay: flex;\n\t\t\t\talign-items: center;\n\t\t\t}\n\n\t\t\t.message h1 {\n\t\t\t\tfont-weight: 400;\n\t\t\t\tfont-size: 1em;\n\t\t\t\tmargin: 0;\n\t\t\t}\n\n\t\t\t@media (prefers-color-scheme: dark) {\n\t\t\t\tbody {\n\t\t\t\t\t--bg: #222;\n\t\t\t\t\t--fg: #ddd;\n\t\t\t\t\t--divider: #666;\n\t\t\t\t}\n\t\t\t}\n\t\t</style>\n\t</head>\n\t<body>\n\t\t<div class=\"error\">\n\t\t\t<span class=\"status\">" + status + "</span>\n\t\t\t<div class=\"message\">\n\t\t\t\t<h1>" + message + "</h1>\n\t\t\t</div>\n\t\t</div>\n\t</body>\n</html>\n"
	},
	version_hash: "9nu3ci"
};

export async function get_hooks() {
	return {
		...(await import("../../../src/hooks.server.ts")),
		
	};
}

export { set_assets, set_building, set_manifest, set_prerendering, set_private_env, set_public_env, set_read_implementation, set_safe_public_env };
