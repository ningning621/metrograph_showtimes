import { injectSpeedInsights } from '@vercel/speed-insights/sveltekit';
import { PASSWORD } from '$env/static/private';
import site from '$lib/site.yaml';

export const prerender = !PASSWORD;
export const trailingSlash = 'never';

injectSpeedInsights();

export const load = async () => {
	return {
		...site
	};
};
