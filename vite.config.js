import dsv from '@rollup/plugin-dsv';
import yaml from '@rollup/plugin-yaml';
import { enhancedImages } from '@sveltejs/enhanced-img';
import { sveltekit } from '@sveltejs/kit/vite';
import { autoType } from 'd3';
import tailwindcss from '@tailwindcss/vite';

/** @type {import('vite').UserConfig} */
export default {
	plugins: [dsv({ processRow: autoType }), yaml(), enhancedImages(), sveltekit(), tailwindcss()]
};
