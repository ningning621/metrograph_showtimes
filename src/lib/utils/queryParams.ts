import { browser } from '$app/environment';
import { get } from 'svelte/store';
import { queryParams } from '$lib/stores';

/**
 * @description Get query params from the URL and stash them in the `queryParams` store.
 * @param getBackupFromCache Whether to get the query params from local storage if the URL has no
 *                           query params.
 */
export const getParams = (getBackupFromCache = true) => {
	if (!browser) return;
	let params = new URLSearchParams(window.location.search);

	if (params.toString().length == 0 && getBackupFromCache) {
		const paramString = localStorage.getItem('queryParamString');
		if (paramString?.length) {
			params = new URLSearchParams(paramString);
		}
	}

	const paramsObj: Record<string, string> | Record<string, never> = {};

	for (const [key, value] of params.entries()) {
		paramsObj[key] = value;
	}

	queryParams.set(paramsObj);
};

/**
 * @description Set local query params to the query param string in the URL.
 * @param setCache Whether to add the queryParams to local storage for persistance.
 */
export const setParams = (setCache = true) => {
	if (!browser) return;
	const paramString = createParamString(false);

	if (paramString?.length)
		history.pushState(
			{},
			'',
			`${window.location.origin}${window.location.pathname}?${paramString}`
		);

	if (setCache) localStorage.setItem('queryParamString', paramString);
};

/**
 * @description Create a query param string from the `queryParams` store.
 * @param appendBaseUrl Whether to append the base URL to the query param string.
 */
export const createParamString = (appendBaseUrl = true) => {
	const paramsObj = get(queryParams);
	const paramString = new URLSearchParams(paramsObj).toString();

	if (appendBaseUrl) return `${window.location.origin}${window.location.pathname}?${paramString}`;

	return paramString;
};
