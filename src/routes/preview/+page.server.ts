import { fail, redirect } from '@sveltejs/kit';
import { dev } from '$app/environment';
import { PASSWORD } from '$env/static/private';

export const prerender = false;

export const actions = {
	default: async ({ request, cookies }) => {
		const hasPassword = PASSWORD !== '';

		const form = await request.formData();
		const password = form.get('password');

		if (hasPassword) {
			if (!password) return fail(400, { message: 'Missing password', error: true });

			if (password !== PASSWORD) return fail(400, { message: 'Incorrect password', error: true });

			cookies.set('preview', PASSWORD, {
				maxAge: 60 * 60 * 24 * 365, // 1 year
				path: '/',
				sameSite: 'strict',
				secure: !dev,
				httpOnly: true
			});

			const previewRedirect = cookies.get('preview-redirect');
			cookies.delete('preview-redirect', { path: '/' }); // get rid of it after use

			redirect(303, previewRedirect ?? '/');
		}
	}
};

export const load = async ({ cookies }) => {
	// send authenticated users at login page to home page, makes page ephemeral
	if (cookies.get('preview') || !PASSWORD) redirect(303, '/');
	return;
};
