<script lang="ts" module>
	import toast from 'svelte-french-toast';
	import sleep from '$lib/utils/sleep';

	const toastDuration = 2000;

	interface CopyURLOptions {
		/**
		 * (Optional) Pathname.
		 * - `false` = omit pathname
		 * - `string` = custom pathname
		 * - `true` | `undefined` or `null` = current pathname
		 */
		pathname?: string | boolean | undefined | null;
		/**
		 * (Optional) hash.
		 * - `false` = omit hash
		 * - `string` = custom hash
		 * - `true` | `undefined` | `null` = current hash
		 */
		hash?: string | boolean | undefined | null;
		/**
		 * (Optional) query.
		 * - `false` = omit query
		 * - `URLSearchParams` | `Record<string, string>` = custom query
		 * - `true` | `undefined` | `null` = current query
		 */
		query?: URLSearchParams | Record<string, string> | undefined | false;
	}

	/**
	 * The message for the toast.
	 * - `string` = custom toast message
	 * - `false` = disable toast
	 * - `true` | `undefined` | `null` = use default toast message
	 */
	type ToastMessage = string | false | undefined | null;

	/**
	 * Copy the current URL to the clipboard & fire a toast to signal.
	 *
	 * @param {CopyURLOptions} options
	 * @returns {boolean} Whether the operation was successful.
	 * @example copyURL();
	 * @example copyURL({ pathname: '/custom/path' });
	 * @example copyURL({ hash: 'custom-hash' });
	 * @example copyURL({ query: { foo: 'bar' } });
	 */
	type CopyURL = (urlOptions?: CopyURLOptions, toastMessage?: ToastMessage) => Promise<boolean>;

	export const copyURL: CopyURL = async (
		{ pathname, hash, query } = {},
		toastMessage = 'Link Copied!'
	) => {
		try {
			// start with base url, sans hash & query
			let url = new URL(window.location.toString().split('?')[0].split('#')[0]);

			// add pathname if requested. default to current pathname
			if (pathname !== false) {
				// pass string to add custom pathname
				// pass false to disable
				// anything else will use current pathname
				url.pathname = typeof pathname === 'string' ? pathname : window.location.pathname;
			}

			// add query if requested. default to current query
			if (query !== false) {
				// pass object or URLSearchParams to add custom query
				// pass false to disable
				// anything else will use current query
				if (query instanceof URLSearchParams) url.search = query.toString();
				else if (query instanceof Object) url.search = new URLSearchParams(query).toString();
				else url.search = window.location.search;
			}

			// add hash if requested. default to current hash
			if (hash !== false) {
				// pass string to add custom hash
				// pass false to disable
				// anything else will use current hash
				url.hash = hash ? `#${hash}` : window.location.hash;
			}

			// copy URL to clipboard
			await navigator.clipboard.writeText(url.toString());

			if (toastMessage !== false) {
				const message = typeof toastMessage === 'string' ? toastMessage : 'Link Copied!';
				toast.success(message, {
					duration: toastDuration,
					iconTheme: {
						primary: 'var(--color-background-offset)',
						secondary: 'var(--color-text-offset)'
					}
				});
			}
			return true;
		} catch (err) {
			if (toastMessage !== false) {
				toast.error('Your browser does not support copying to clipboard.', {
					duration: toastDuration
				});
			}

			return false;
		}
	};
</script>

<script lang="ts">
	import { fly, scale } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';
	import { prefersReducedMotion } from '$lib/stores';

	import Icon from '$lib/components/atoms/Icon.svelte';
	import type { IconOptions } from '$lib/components/atoms/Icon.svelte';
	import Button from '$lib/components/interactivity/Button.svelte';

	interface Props {
		children?: import('svelte').Snippet<[any]>;
		size?: 'sm' | 'md' | 'lg';
		color?: 'primary' | 'accent';
		variant?: 'pill' | 'underlined';
		icon?: IconOptions;
		class?: Classes;
		urlOptions?: CopyURLOptions;
		[key: string]: any;
	}

	let {
		children,
		size,
		color,
		variant,
		icon = 'link-variant',
		class: classes = '',
		urlOptions,
		...rest
	}: Props = $props();

	let hasToast = $state(false);
</script>

<Button
	{size}
	{color}
	{variant}
	class={classes}
	disabled={hasToast}
	title="Copy URL{hasToast ? ' (copied!)' : ''}"
	onclick={async () => {
		const isSuccessful = await copyURL({ ...urlOptions });

		if (isSuccessful) {
			// trigger icon animations, local to the button instance
			hasToast = true;
			await sleep(toastDuration);
			hasToast = false;
		}
	}}
	{...rest}
>
	{#if children}
		{@render children({ hasToast })}
	{/if}
	<span class="sr-only">Copy link to share</span>
	{#if !hasToast}
		<div
			in:scale|local={{
				start: 0.95,
				duration: $prefersReducedMotion ? 0 : 300,
				easing: cubicOut
			}}
			class="flex items-center justify-center"
		>
			<Icon {icon} />
		</div>
	{:else}
		<div
			in:fly|local={{ y: 5, duration: $prefersReducedMotion ? 0 : 300, easing: cubicOut }}
			class="flex items-center justify-center"
		>
			<Icon icon="check" />
		</div>
	{/if}
</Button>
