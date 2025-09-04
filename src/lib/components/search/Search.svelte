<!-- 
THIS CODE HAS BEEN DEPRECATED AND NEEDS TO BE UPDATED FOR FURTHER USE. 

It currently relies on a modal component that is no longer in use, and will need to be updated to use a dialog component. The snippet below is the prior button that triggered the search for reference. The use of the overlay store is no longer needed and has been removed from the project. For full details on the previous implementation, see this PR: https://github.com/the-dataface/df-sveltekit/pull/94

If you're interested in updating this component, consider using the BitsUI Commmand component: https://bits-ui.com/docs/components/command


<button
	class="border-secondary bg-secondary text-primary hover:border-primary hover:bg-primary focus:border-primary focus:bg-primary flex cursor-pointer flex-row flex-nowrap items-center gap-1.5 rounded-full border py-2 pr-2 pl-4 leading-none transition-colors select-none"
	onclick={() => searching.set('All')}
>
	<Icon icon="search" aria-hidden="true" />
	<span>Search</span>
	{#if browser}
		<div class="text-secondary mr-2 ml-4 flex h-fit flex-row gap-1 text-xs leading-none">
			{#each [navigator?.platform === 'MacIntel' ? '⌘' : 'Ctrl', 'k'] as key}
				<kbd
					class="border-tertiary bg-tertiary text-primary grid place-content-center rounded-sm border px-1 py-0.5"
				>
					{key}
				</kbd>
			{/each}
		</div>
	{/if}
</button> -->

<script module lang="ts">
	import { writable } from 'svelte/store';
	import { persisted } from 'svelte-persisted-store';
	import type { SearchGroup, Tree, Type } from './types';
	import searchGroups from './groups';

	export const searching = writable<Type | false>(false);

	export const query = writable<string>('');

	export const recentSearches = persisted('recent-searches', []);

	export const clear = () => {
		query.set('');
	};

	export const open = (type?: Type) => {
		searching.set(type || 'All');
		overlay.set(true);
	};

	export const close = () => {
		searching.set(false);
		overlay.set(false);
		clear();
	};
</script>

<script lang="ts">
	import { browser } from '$app/environment';
	import { onMount, untrack } from 'svelte';
	import { overlay } from '$lib/stores';
	import Modal from './Modal.svelte';
	import SearchResultsList from './SearchResultsList.svelte';
	import outclick from '$lib/actions/outclick';
	import { focusableChildren } from '$lib/actions/focus';
	import SearchWorker from './search-worker.ts?worker';
	import Icon from '$lib/components/atoms/Icon.svelte';

	let worker: Worker | undefined = $state();
	let ready = $state(false);

	let results: { nodes: Tree[]; query: string } = $state({ nodes: [], query: $query });
	let recentSearchesLocal: string[] = $state([]);

	let searchResultsEl: HTMLDivElement | undefined = $state();

	let uid = $state(1);

	const format = async () => {
		query.set($query.trim());
	};

	onMount(() => {
		if (!browser) return;

		worker = new SearchWorker();

		worker.addEventListener('message', (event) => {
			const { type, payload } = event.data;

			switch (type) {
				case 'ready':
					ready = true;
					break;

				case 'results':
					results = payload;
					break;

				case 'recents':
					recentSearchesLocal = payload;
					break;
			}
		});

		worker.postMessage({ type: 'init', payload: { type: type?.value } });
	});

	const onNavigate = (href: string) => {
		recentSearches.set([href, ...$recentSearches.filter((x) => x !== href)]);
		close();
	};

	let type = $derived($searching && (searchGroups?.[$searching || 'All'] as SearchGroup));

	let inactiveSearchGroups = $derived(
		Object.values(searchGroups).filter((t) => t.value !== type?.value)
	);

	const postMessage = (type: string, payload: any) => {
		if (!ready || !worker) return;
		let id = undefined;
		if (type === 'query') id = untrack(() => uid++);
		worker.postMessage({
			type,
			id,
			payload
		});
	};

	$effect(() => {
		if (!type) return;
		postMessage('query', { query: $query, type: type.value || 'All' });
	});

	$effect(() => {
		postMessage('recents', $recentSearches);
	});

	$effect(() => {
		if (ready && type) searchResultsEl?.scrollTo({ top: 0 });
	});
</script>

<svelte:window
	onkeydown={(e) => {
		if (e.key === 'k' && (navigator.platform === 'MacIntel' ? e.metaKey : e.ctrlKey)) {
			e.preventDefault();
			clear();

			if ($searching) close();
			else searching.set(type?.value || 'All');
		}

		if (e.code === 'Escape') close();
	}}
/>

{#if $searching}
	<Modal id="search-modal" onclose={close}>
		{#snippet closeButton()}
			<span></span>
		{/snippet}

		<div class="mx-auto h-[25rem] max-h-[calc(100%_-_2rem)] w-full overflow-hidden">
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<div
				class="bg-primary relative flex h-fit max-h-full w-full flex-col overflow-hidden rounded text-xl shadow-2xl shadow-gray-900/10"
				use:outclick={close}
				onkeydown={(e) => {
					if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
						e.preventDefault();
						const group = focusableChildren(e.currentTarget);

						// when using arrow keys (as opposed to tab), don't focus buttons
						const selector = 'a, input';

						if (e.key === 'ArrowDown') {
							group.next(selector);
						} else {
							group.prev(selector);
						}
					}
				}}
			>
				<h1 class="sr-only">Search</h1>

				<div class="border-tertiary bg-primary relative flex w-full flex-row flex-nowrap border-b">
					<div class="w-full">
						<label class="flex cursor-text flex-row flex-nowrap items-center pl-4">
							<Icon
								class="text-icon-secondary text-lg leading-none"
								icon="search"
								aria-hidden="true"
							/>
							<!-- svelte-ignore a11y_autofocus -->
							<input
								class="text-primary placeholder:text-secondary w-full border-0 bg-transparent py-4 pr-10 pl-4 font-sans text-lg leading-none outline-none focus:ring-0"
								type="search"
								name="q"
								placeholder={type.placeholder}
								aria-label={type.placeholder}
								aria-describedby="search-description"
								autofocus
								spellcheck="false"
								aria-keyshortcuts={browser
									? (navigator.platform === 'MacIntel' ? '⌘' : 'Ctrl') + 'k'
									: ''}
								onchange={format}
								bind:value={$query}
							/>
						</label>

						<div class="absolute inset-y-0 right-2 grid place-content-center">
							<button
								class="text-icon-secondary hover:bg-secondary hover:text-primary focus:bg-secondary focus:text-primary active:bg-tertiary grid place-content-center rounded p-2 text-lg leading-none transition-all active:scale-[.99]"
								type="button"
								aria-label="Close search"
								onclick={close}
							>
								<Icon icon="close" aria-hidden="true" />
							</button>
						</div>

						<span id="search-description" class="sr-only">Results will update as you type</span>
					</div>
				</div>

				<div class="flex-1 overflow-auto overscroll-y-none" aria-live="assertive">
					{#if $query || type?.showAllOnEmpty}
						{#if results?.nodes?.length}
							<div
								class="h-full max-h-full overflow-auto overscroll-y-none"
								bind:this={searchResultsEl}
							>
								<SearchResultsList
									results={results.nodes}
									query={results.query}
									on:select={(e) => {
										onNavigate(e.detail.href);
									}}
								/>
							</div>
						{:else if $query?.length}
							<p class="text-primary p-4 font-sans text-sm leading-tight font-semibold">
								No results for "{$query}"
							</p>
						{/if}
					{:else}
						<h2
							class="text-secondary px-4 pt-3 font-sans text-xs leading-tight font-semibold uppercase"
							class:pb-3={!recentSearchesLocal?.length}
						>
							{recentSearchesLocal?.length ? 'Recent searches' : 'No recent searches'}
						</h2>
						{#if recentSearchesLocal?.length}
							<ul class="list-none">
								{#each recentSearchesLocal as search, i}
									<li class="relative flex flex-row flex-nowrap items-center justify-between gap-1">
										<a
											class="text-primary hover:bg-secondary focus:bg-secondary flex w-full flex-col px-4 py-3 font-sans"
											href={search.href}
											onclick={() => {
												onNavigate(search.href);
											}}
										>
											<small class="text-tertiary font-sans text-xs leading-none font-semibold"
												>{search?.breadcrumbs.slice(0, -1)?.join('/')}</small
											>
											<strong class="font-sans text-lg leading-tight font-bold"
												>{search?.breadcrumbs?.at(-1)}</strong
											>
										</a>

										<button
											class="hover:bg-secondary focus:bg-secondary text-icon-secondary hover:text-primary focus:text-primary absolute right-2 grid place-content-center rounded p-2 leading-none"
											aria-label="Delete"
											onclick={(e) => {
												$recentSearches = $recentSearches.filter((href) => href !== search.href);

												e.stopPropagation();
												e.preventDefault();
											}}
										>
											<Icon icon="delete" aria-hidden="true" />
										</button>
									</li>
								{/each}
							</ul>
						{/if}
					{/if}

					<ul
						class="border-tertiary bg-primary text-secondary sticky bottom-0 flex flex-col border-t text-xs leading-tight font-medium"
					>
						<li>
							<span class="flex flex-row flex-nowrap items-center gap-2 px-4 py-3">
								<Icon icon="view-grid" aria-hidden="true" />

								<span>
									Or search {#each inactiveSearchGroups as t, i (t)}{#if i > 0}{#if i < inactiveSearchGroups.length - 1},
											{:else}, or
											{/if}{/if}
										<button
											class="text-primary inline underline"
											onclick={() => searching.set(t.value)}>{t.inline}</button
										>{/each}
								</span>
							</span>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</Modal>
{/if}
