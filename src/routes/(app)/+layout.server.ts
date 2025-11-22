import { injectSpeedInsights } from '@vercel/speed-insights/sveltekit';
import site from '$lib/site.yaml';

export const prerender = true;
export const trailingSlash = 'never';

injectSpeedInsights();

export const load = async () => {
	return {
		...site
	};
};
