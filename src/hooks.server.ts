const preloadTypes = new Set(['js', 'css', 'font']);

export const handle = async ({ event, resolve }) => {
	const response = await resolve(event, {
		preload: ({ type }) => preloadTypes.has(type)
	});
	return response;
};
