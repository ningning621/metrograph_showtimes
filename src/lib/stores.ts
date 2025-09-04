import { browser } from '$app/environment';
import { readable, writable } from 'svelte/store';
import debounce from 'lodash.debounce';
import Device from 'svelte-device-info';

export const viewport = readable(
	{
		width: 0,
		height: 0,
		screenSize: undefined,
		screens: undefined,
		canHover: undefined
	} as {
		width: number;
		height: number;
		screenSize: string | undefined;
		screens: { [key: string]: boolean } | undefined;
		canHover: boolean | undefined;
	},
	(set) => {
		const onResize = () => {
			const windowW = window.innerWidth;
			const screens = {
				mobile: windowW < 640,
				sm: windowW >= 640 && windowW < 768,
				md: windowW >= 768 && windowW < 1024,
				lg: windowW >= 1024 && windowW < 1280,
				xl: windowW >= 1280 && windowW < 1536,
				'2xl': windowW >= 1536
			};
			const screenSize = Object.keys(screens).filter(
				(val) => screens[val as keyof typeof screens]
			)[0];
			set({
				width: windowW,
				height: window.innerHeight,
				screenSize,
				screens,
				canHover: Device.canHover
			});
		};
		if (browser) {
			onResize();
			window.addEventListener('resize', debounce(onResize, 50));
		}
		return () => {
			if (browser) window.removeEventListener('resize', onResize);
		};
	}
);

/**
 * @description Track the user's motion preference.
 * @see {@link https://geoffrich.net/posts/svelte-prefers-reduced-motion-store/|Original}
 */
const reducedMotionQuery = '(prefers-reduced-motion: reduce)';

const getInitialMotionPreference = () => false;

export const prefersReducedMotion = readable(getInitialMotionPreference(), (set) => {
	const updateMotionPreference = (event: MediaQueryListEvent) => {
		set(event.matches);
	};

	let mediaQueryList: MediaQueryList;

	if (browser) {
		mediaQueryList = window.matchMedia(reducedMotionQuery);
		mediaQueryList.addEventListener('change', updateMotionPreference);
	}

	return () => {
		if (browser) mediaQueryList.removeEventListener('change', updateMotionPreference);
	};
});

/** @description Query parameters controlled through the QueryParamsProvider component. */
export const queryParams = writable({});
