<script lang="ts">
	import { enhance } from '$app/forms';
	import toast from 'svelte-french-toast';
	import Icon from '$lib/components/atoms/Icon.svelte';

	let { form } = $props();

	let inputEl: HTMLInputElement | undefined = $state();
	let password = $state('');

	const resetInput = () => {
		password = '';
		inputEl?.focus();
	};

	$effect(() => {
		if (form?.error) {
			toast.error(form.message, {
				position: 'top-center'
			});

			resetInput();
		}
	});
</script>

<main
	class="text-primary to-background-offset from-background-primary h-screen w-full bg-gradient-to-br p-8"
>
	<a
		href="https://thedataface.com"
		target="_blank"
		class="absolute inset-x-0 bottom-4 text-center sm:right-4 sm:left-[unset]"
	>
		<span class="sr-only">A project by The DataFace</span>
		<img
			src="/dataface.png"
			class="mx-auto h-12 w-fit object-contain"
			width="996"
			height="724"
			alt="The DataFace"
		/>
	</a>
	<div class="mx-auto grid h-full w-full max-w-full place-content-center md:max-w-xl">
		<h1 class="sr-only">Enter password to continue to the site.</h1>
		<form class="w-full" aria-label="Enter password to enter site" method="POST" use:enhance>
			<div class="flex flex-row flex-wrap items-center gap-4 sm:pl-16">
				<label for="password" class="sr-only">Site password</label>
				<!-- svelte-ignore a11y_autofocus -->
				<input
					id="password"
					name="password"
					type="password"
					placeholder="Enter password"
					autofocus
					class="placeholder:text-secondary border-secondary peer focus:border-b-accent focus:text-primary m-0 block h-12 flex-1 border-x-0 border-t-0 border-b bg-transparent px-2 pb-4 text-center font-sans text-3xl placeholder:text-3xl placeholder:font-light focus:ring-0 focus:outline-none sm:w-auto sm:max-w-xs"
					class:border-accent={form?.error}
					bind:value={password}
					bind:this={inputEl}
				/>

				<button
					type="submit"
					title="submit"
					class="border-secondary hover:text-primary focus:text-primary hover:border-primary focus:border-primary flex h-12 w-full flex-row flex-nowrap items-center justify-center gap-2 border p-3 text-xl leading-none font-semibold transition-colors select-none focus:ring-0 focus:ring-transparent sm:w-12"
					class:opacity-0={password.length === 0}
					class:pointer-events-none={password.length === 0}
					tabindex={password.length ? undefined : -1}
					disabled={password.length === 0}
				>
					<span class="sm:sr-only">Submit</span>
					<Icon
						icon="arrow-right"
						class="block h-6 w-6 transition-transform duration-150 ease-out sm:h-8 sm:w-8"
					/>
				</button>
			</div>
		</form>
	</div>
</main>

<style lang="postcss" type="postcss">
	@reference '$lib/styles/app.css';

	::-moz-selection {
		@apply text-primary bg-secondary;
	}

	::selection {
		@apply text-primary bg-secondary;
	}
</style>
