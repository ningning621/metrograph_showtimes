<script>
	import SearchResultsList from './SearchResultsList.svelte';
	import { createEventDispatcher } from 'svelte';
	import Icon from '$lib/components/atoms/Icon.svelte';

	/**
	 * @typedef {Object} Props
	 * @property {import('./types').Tree[]} results
	 * @property {string} query
	 * @property {number} [level]
	 */

	/** @type {Props} */
	let { results, query, level = 0 } = $props();

	const dispatch = createEventDispatcher();

	/** @param {string} text */
	function escape(text) {
		return text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
	}

	/**
	 * @param {string} content
	 * @param {string} query
	 */
	function excerpt(content, query) {
		const index = content.toLowerCase().indexOf(query.toLowerCase());
		if (index === -1) {
			return escape(content.slice(0, 100));
		}

		const prefix = index > 20 ? `…${content.slice(index - 15, index)}` : content.slice(0, index);
		const suffix = content.slice(
			index + query.length,
			index + query.length + (80 - (prefix.length + query.length))
		);

		return (
			escape(prefix) +
			`<mark>${escape(content.slice(index, index + query.length))}</mark>` +
			escape(suffix)
		);
	}
</script>

<ul class="relative m-0 list-none divide-y divide-gray-50 p-0">
	{#each results as result}
		<li class="mb-0 list-none p-0">
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<svelte:element
				this={result.href ? 'a' : 'div'}
				class="node level-{level} text-900 flex flex-col gap-1 overflow-x-auto px-4 py-3 font-sans leading-tight {result.href
					? 'hover:bg-secondary focus:bg-secondary'
					: ''}"
				data-sveltekit-preload-data
				href={result.href}
				onclick={() => {
					if (!result?.href) return;
					dispatch('select', { href: result.href });
				}}
				data-has-node={result?.node ? true : undefined}
			>
				<strong
					class="flex w-fit flex-row flex-nowrap items-center gap-1 overflow-hidden leading-tight text-ellipsis whitespace-nowrap"
				>
					<span class="flex flex-1 flex-row flex-nowrap items-center gap-1">
						{#if result?.node?.icon}
							<Icon class="shrink-0" icon={result.node.icon} aria-hidden="true" />
						{/if}
						<span class="flex-1">
							{@html excerpt(result.breadcrumbs[result.breadcrumbs.length - 1], query)}
						</span>
					</span>
				</strong>

				{#if result?.node?.content}
					<span
						class="block overflow-hidden font-sans text-sm leading-tight font-normal text-ellipsis whitespace-nowrap"
						>{@html excerpt(result.node.content, query)}</span
					>
				{/if}
			</svelte:element>

			{#if result?.children?.length > 0}
				<SearchResultsList results={result?.children} {query} level={level + 1} on:select />
			{/if}
		</li>
	{/each}
</ul>

<style lang="postcss">
	@reference '$lib/styles/app.css';

	ul :global(ul) {
		margin-left: 0.8em !important;
		padding-left: 0em;
		border-left: 1px solid var(--colors-red-500);
	}

	li:last-child {
		margin-bottom: 0;
	}

	ul ul li {
		margin: 0;
	}

	.node :global(mark) {
		--highlight-color: var(--colors-green-800);
	}

	.node span :global(mark) {
		background: none;
		color: var(--highlight-color);
	}

	.node strong :global(mark) {
		color: var(--highlight-color);
	}

	ul :global(.node.level-0 strong) {
		@apply text-lg font-bold;
	}

	ul :global(.node.level-1 strong) {
		@apply text-base font-bold;
	}

	ul :global(.node.level-2 strong) {
		@apply text-sm font-bold;
	}
</style>
