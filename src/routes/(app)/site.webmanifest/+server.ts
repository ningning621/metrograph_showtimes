/* eslint-disable camelcase */
import { json } from '@sveltejs/kit';
import site from '$lib/site.yaml';

/** @type {import('./$types').RequestHandler} */
export const GET = () =>
	json({
		name: site.siteName,
		short_name: site.tag,
		description: site.description,
		start_url: '/',
		theme_color: '#ffffff',
		background_color: '#ffffff',
		display: 'minimal-ui',
		icons: [
			{
				src: '/favicon-192x192.png',
				sizes: '192x192',
				type: 'image/png',
				purpose: 'maskable any'
			},
			{
				src: '/favicon-512x512.png',
				sizes: '512x512',
				type: 'image/png',
				purpose: 'maskable any'
			}
		]
	});
