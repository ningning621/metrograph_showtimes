import { fail, redirect } from '@sveltejs/kit';

export const prerender = false;

export const actions = {
	default: async ({ request, cookies }) => {
		const hasPassword = false;

		const form = await request.formData();
		const password = form.get('password');

		if (hasPassword) {
			if (!password) return fail(400, { message: 'Missing password', error: true });

			const previewRedirect = cookies.get('preview-redirect');
			cookies.delete('preview-redirect', { path: '/' }); // get rid of it after use

			redirect(303, previewRedirect ?? '/');
		}
	}
};

export const load = async ({ cookies }) => {
	// send authenticated users at login page to home page, makes page ephemeral
	if (cookies.get('preview')) redirect(303, '/');
	return;
};
