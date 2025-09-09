import { redirect } from '@sveltejs/kit';
import { building, dev } from '$app/environment';
import { PASSWORD } from '$env/static/private';

const unprotectedRoutes = new Set(['/preview']);

export const load = async ({ url, cookies }) => {
	const { pathname } = url;

	// whitelist dev always. check for password in production
	const isPreviewProtected = PASSWORD !== '' && !building && !dev;

	if (isPreviewProtected) {
		const isProtected = !unprotectedRoutes.has(pathname);
		const isPreviewAuthorized = cookies.get('preview');

		// send unauthenticated users to login page
		if (!isPreviewAuthorized && isProtected) {
			cookies.set('preview-redirect', url.toString(), {
				maxAge: 60 * 60, // 1 hour
				path: '/',
				sameSite: 'strict',
				secure: !dev,
				httpOnly: true
			});

			redirect(303, '/preview');
		}
	}

	return;
};
